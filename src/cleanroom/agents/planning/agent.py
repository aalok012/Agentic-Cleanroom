"""Planning Agent.

Walks the functional requirements in dependency order (outer feature order, then inner
FR order from the nested dependency graph) and produces a CONTRACT per FR:

  - signature : a concrete function signature (name, typed params, return type)   [LLM]
  - docstring : Google-style — summary + Args + Returns + Notes (edge cases) [LLM], then
                Constraints (from the feature's NFRs) + Prerequisites (from fr_edges) [deterministic]
  - mvc_layer : model | view | controller                                          [LLM, deterministic fallback]
  - file_path : derived DETERMINISTICALLY from the layer
  - prerequisite_fr_ids : the FR's prerequisites, taken from the inner fr_edges     [deterministic]

DETERMINISTIC-FIRST: ordering, ids, prerequisites, the layer->path mapping, and embedding
the NFR constraints into the docstring are all plain code. The LLM is used only for
interpretation (signature naming, behavioral docstring, layer choice). The LLM never
assigns or invents ids. Token discipline: ONE structured call per feature (never the whole
IR); gpt-4o-mini via with_structured_output().

The planner runs ONCE globally and produces ALL contracts from the SPEC only — no code,
no tests — preserving the isolation the later code/test agents depend on.
"""

import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from src.cleanroom.agents.planning.schema.plan import Contract, FeaturePlan, PlanningOutput
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.prompt_renderer import PromptRenderer

# --- MVC layer keyword fallback (used only when the LLM's layer is unusable) ----
MVC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "model": ("data", "database", "storage", "schema", "model", "entity", "repository",
              "persistence", "record", "vocabulary", "terminology", "standard", "code"),
    "controller": ("function", "behavior", "operation", "integration", "exchange", "process",
                   "service", "controller", "logic", "workflow", "transaction"),
    "view": ("visualization", "report", "display", "ui", "interface", "presentation", "view",
             "dashboard", "render", "screen", "chart", "graph"),
}
_LAYER_DIR = {"model": "models", "view": "views", "controller": "controllers"}


def classify_layer(feature_name: str) -> str | None:
    """Infer the MVC layer of a feature from its name, or None if ambiguous.

    Kept as the deterministic fallback for the planner's layer choice. Matches a keyword
    when a word in the name *starts with* it. This is a LAST RESORT only — with the
    Literal-typed mvc_layer in the schema, the LLM almost always returns a valid layer.
    """
    words = re.findall(r"[a-z]+", (feature_name or "").lower())
    scores = {
        layer: sum(1 for kw in keywords if any(word.startswith(kw) for word in words))
        for layer, keywords in MVC_KEYWORDS.items()
    }
    best = max(scores.values())
    if best == 0:
        return None
    winners = [layer for layer, score in scores.items() if score == best]
    return winners[0] if len(winners) == 1 else None


def feature_of(req_id: str) -> str:
    """Feature id is the first two dot-segments of a requirement id: '2.2.6.6' -> '2.2'."""
    return ".".join(req_id.split(".")[:2])


def _numeric_key(id_str: str) -> tuple[tuple[int, int, str], ...]:
    return tuple((0, int(part), "") if part.isdigit() else (1, 0, part) for part in id_str.split("."))


def _norm_id(raw: str) -> str:
    """Normalize an id the LLM echoed back (e.g. '[2.2.1]') to the bare parser id."""
    return (raw or "").strip().strip("[]").strip()


def _slug(fr_id: str) -> str:
    return re.sub(r"\W", "_", fr_id)


def _func_name(signature: str, fr_id: str) -> str:
    """Deterministic file stem: the function name from the signature, else a slug of the id."""
    match = re.search(r"def\s+([A-Za-z_]\w*)", signature or "")
    if match:
        return match.group(1)
    return "fr_" + _slug(fr_id)


def _normalize_layer(raw: str, feature_name: str) -> str:
    """Coerce the LLM's layer to model|view|controller, falling back to the name-keyword
    classifier, then to 'controller'."""
    layer = (raw or "").strip().lower()
    if layer in _LAYER_DIR:
        return layer
    fallback = classify_layer(feature_name)
    return fallback if fallback in _LAYER_DIR else "controller"


def _file_path(layer: str, signature: str, fr_id: str) -> str:
    """Return a path relative to the project's code output directory.

    Written as {layer_dir}/{func}.py so the Code Agent can write it under any
    base directory without path conflicts.
    """
    return f"{_LAYER_DIR[layer]}/{_func_name(signature, fr_id)}.py"


# A default/placeholder signature the planner emits when the LLM returned no design,
# e.g. "def fr_2_2_6_6() -> None:" — used to flag stub-fallback files for follow-up.
_STUB_FALLBACK_RE = re.compile(r"^def\s+fr_\w+\(\s*\)\s*->\s*None\s*:\s*$")


def _is_stub_fallback(signature: str) -> bool:
    return bool(_STUB_FALLBACK_RE.match((signature or "").strip()))


def _infer_return_type(signature: str) -> str | None:
    """Extract the return type annotation from a function signature.

    E.g. 'def foo(x: int) -> None:' yields 'None', 'def bar() -> dict[str, Any]:' yields 'dict[str, Any]'.
    Returns None if no return type found.
    """
    if not signature:
        return None
    match = re.search(r'->\s*([^:]+):', signature)
    if match:
        return match.group(1).strip()
    return None


def _render_stub(contract) -> str:
    """Render a deterministic, valid-Python skeleton from a contract — no LLM.

    Writes the contract's signature and docstring VERBATIM, a NotImplementedError body, a
    provenance header, and (for stub-fallback signatures) a TODO marker.
    """
    lines = [
        f"# Auto-generated stub from contract {contract.fr_id} "
        f"(feature {contract.feature_id}). Do not edit by hand."
    ]
    if _is_stub_fallback(contract.signature):
        lines.append("# TODO: planner produced no real design for this requirement")

    signature = contract.signature.rstrip()
    if not signature.endswith(":"):
        signature += ":"
    lines.append(signature)

    # Inline triple-quoted docstring keeps contract.docstring a verbatim substring. Guard
    # the rare case where the text ends in a quote (would merge into the closing delimiter).
    doc = contract.docstring or ""
    if doc.endswith('"'):
        doc += "\n"
    lines.append(f'    """{doc}"""')
    lines.append("    raise NotImplementedError")
    return "\n".join(lines) + "\n"


class PlanningAgent:
    def __init__(self, llm=None) -> None:
        # `llm` is injectable so tests/stubs avoid network calls.
        self.llm = llm if llm is not None else get_llm()
        self.renderer = PromptRenderer()

    def plan(self, ir: dict) -> PlanningOutput:
        graph = ir.get("dependency_graph")
        if graph is None:
            raise ValueError("PlanningAgent requires an IR enriched with 'dependency_graph'.")

        by_id = {f.get("id"): f for f in ir.get("features", [])}
        contracts: list[Contract] = []
        notes: list[str] = []

        for fid in self._feature_order(ir, graph):
            feature = by_id.get(fid)
            if not feature or not feature.get("functional_requirements"):
                continue  # NFR-only / empty features yield no contracts

            frs = feature["functional_requirements"]
            fr_order = feature.get("fr_order") or [r["id"] for r in frs]
            text_by_id = {r["id"]: (r.get("text") or r.get("description", "")) for r in frs}
            nfrs = feature.get("non_functional_requirements", [])
            name = feature.get("name", "")

            prereqs: dict[str, list[str]] = defaultdict(list)
            for edge in feature.get("fr_edges", []):
                prereqs[edge["source"]].append(edge["target"])

            designs = self._design_feature(name, fr_order, text_by_id, nfrs)

            for rid in fr_order:
                design = designs.get(rid)
                prereq_ids = prereqs.get(rid, [])
                prereq_notes = self._prereq_notes(prereq_ids, designs)

                if design is None:
                    notes.append(f"FR {rid}: no LLM design returned; used a default contract.")
                    signature = f"def fr_{_slug(rid)}() -> None:"
                    summary = f"Implements requirement {rid}."
                    args, returns, design_notes = [], "", ""
                    layer = _normalize_layer("", name)
                else:
                    signature = design.signature
                    summary = design.summary
                    args, returns = design.args, design.returns
                    design_notes = design.notes
                    layer = _normalize_layer(design.mvc_layer, name)

                contracts.append(
                    Contract(
                        fr_id=rid,
                        feature_id=fid,
                        signature=signature,
                        docstring=self._compose_docstring(
                            summary, args, returns, design_notes, nfrs, prereq_notes, signature
                        ),
                        mvc_layer=layer,
                        file_path=_file_path(layer, signature, rid),
                        prerequisite_fr_ids=prereq_ids,
                    )
                )

        return PlanningOutput(contracts=contracts, notes=notes)

    def enrich(self, ir: dict, output_dir=None) -> dict:
        """Run plan() and fold the result into the IR under 'planning'. Optionally save."""
        planning = self.plan(ir).model_dump()
        enriched = {**ir, "planning": planning}
        if output_dir is not None:
            out = Path(output_dir)
            out.mkdir(parents=True, exist_ok=True)
            (out / f"{ir.get('project_name', 'project')}_planning.json").write_text(
                json.dumps(enriched, indent=2)
            )
        return enriched

    # --- stub materialization (deterministic; no LLM) --------------------------
    @staticmethod
    def _as_contracts(planning_output) -> list[Contract]:
        """Accept a PlanningOutput, a dict (full IR or just the planning block), or a list
        of contracts, and normalize to a list of Contract objects."""
        if isinstance(planning_output, PlanningOutput):
            return planning_output.contracts
        if isinstance(planning_output, dict):
            block = planning_output.get("planning", planning_output)
            raw = block.get("contracts", [])
        elif isinstance(planning_output, list):
            raw = planning_output
        else:
            raise TypeError(f"Cannot read contracts from {type(planning_output).__name__}")
        return [c if isinstance(c, Contract) else Contract(**c) for c in raw]

    @staticmethod
    def materialize_stubs(planning_output, base_dir) -> dict:
        """Write a deterministic .py skeleton for every contract to its file_path.

        Pure file-writing from contracts already produced by plan() — NO LLM, no network.
        Each file gets the contract's signature + docstring verbatim and a
        NotImplementedError body. `file_path` is treated as relative to `base_dir`; parent
        directories are created as needed.

        Returns a summary dict: written paths, collisions (same file_path, disambiguated
        rather than overwritten), stub_fallbacks (placeholder signatures), and any
        parse_failures (files that did not ast.parse).
        """
        base = Path(base_dir)
        written: list[str] = []
        collisions: list[dict] = []
        stub_fallbacks: list[dict] = []
        parse_failures: list[dict] = []
        used: dict[Path, str] = {}  # resolved target -> fr_id that owns it

        for contract in PlanningAgent._as_contracts(planning_output):
            target = base / contract.file_path

            # Collision guard: never silently overwrite a path another contract claimed.
            if target in used:
                conflict_with = used[target]
                target = target.with_name(f"{target.stem}_{_slug(contract.fr_id)}{target.suffix}")
                counter = 2
                while target in used:  # extremely unlikely 3-way clash
                    target = target.with_name(f"{target.stem}_{counter}{target.suffix}")
                    counter += 1
                collisions.append({
                    "fr_id": contract.fr_id,
                    "intended": str(base / contract.file_path),
                    "written": str(target),
                    "conflict_with": conflict_with,
                })

            used[target] = contract.fr_id
            content = _render_stub(contract)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            written.append(str(target))

            if _is_stub_fallback(contract.signature):
                stub_fallbacks.append({"fr_id": contract.fr_id, "path": str(target)})

            try:
                ast.parse(content)
            except SyntaxError as exc:
                parse_failures.append({"path": str(target), "error": str(exc)})

        return {
            "written": written,
            "collisions": collisions,
            "stub_fallbacks": stub_fallbacks,
            "parse_failures": parse_failures,
        }

    # --- helpers ---------------------------------------------------------------
    def _design_feature(self, feature_name, fr_order, text_by_id, nfrs) -> dict:
        """One structured LLM call for a single feature's FRs. Returns {fr_id: FRPlan}."""
        requirements = [{"id": rid, "text": text_by_id.get(rid, "")} for rid in fr_order]
        prompt = self.renderer.render(
            "plan_feature.j2",
            {"feature_name": feature_name, "requirements": requirements, "nfrs": nfrs},
        )
        result: FeaturePlan = self.llm.with_structured_output(FeaturePlan).invoke(prompt)
        return {_norm_id(p.id): p for p in result.plans}

    @staticmethod
    def _prereq_notes(prereq_ids: list[str], designs: dict) -> list[str]:
        """Build the docstring's prerequisite Notes deterministically from fr_edges.

        References each prerequisite by its designed function name (when available) plus
        its requirement id, e.g. "Prerequisite: create_lab_test_request (req 2.2.6.6) ...".
        """
        notes: list[str] = []
        for pid in prereq_ids:
            dep = designs.get(pid)
            fname = _func_name(dep.signature, pid) if dep is not None else None
            if fname:
                notes.append(f"Prerequisite: {fname} (req {pid}) must have run first.")
            else:
                notes.append(f"Prerequisite: requirement {pid} must be satisfied first.")
        return notes

    @staticmethod
    def _compose_docstring(
        summary: str, args, returns: str, design_notes: str, nfrs: list[dict], prereq_notes: list[str],
        signature: str = ""
    ) -> str:
        """Assemble a Google-style docstring deterministically.

        The LLM supplies the summary, the per-arg/return descriptions, and any edge-case
        Notes; the section structure, the NFR Constraints block, and the prerequisite
        Notes are plain code. Returns section is always included (inferred from signature
        if the LLM did not provide one). Edge-case notes (from the LLM) and prerequisite
        notes (from fr_edges) are merged under a single Notes section.
        """
        lines = [(summary or "").strip()]

        if args:
            lines += ["", "Args:"]
            for arg in args:
                lines.append(f"    {arg.name}: {arg.description}")

        return_text = (returns or "").strip()
        if not return_text and signature:
            return_type = _infer_return_type(signature)
            if return_type:
                return_text = return_type + "."

        if return_text:
            lines += ["", "Returns:", f"    {return_text}"]

        if nfrs:
            lines += ["", "Constraints:"]
            for nfr in nfrs:
                lines.append(f"    - {nfr.get('category', '')}: {nfr.get('text', '')}")

        # Merge LLM edge-case notes and deterministic prerequisite notes under one section.
        merged_notes: list[str] = []
        if (design_notes or "").strip():
            merged_notes.append(design_notes.strip())
        merged_notes += prereq_notes
        if merged_notes:
            lines += ["", "Notes:"]
            for note in merged_notes:
                lines.append(f"    {note}")

        return "\n".join(lines).strip()

    @staticmethod
    def _feature_order(ir: dict, graph: dict) -> list[str]:
        """Outer feature order: dependency build order, then cycle members, then any
        FR-bearing feature not yet covered (numeric) so nothing is dropped."""
        ordered = list(graph.get("build_order", []))
        for cycle in graph.get("cycles", []):
            ordered += sorted(cycle, key=_numeric_key)
        seen = set(ordered)
        for feature in ir.get("features", []):
            fid = feature.get("id")
            if feature.get("functional_requirements") and fid not in seen:
                ordered.append(fid)
                seen.add(fid)
        return ordered


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m src.cleanroom.agents.planning.agent <enriched_ir.json>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        enriched_ir = json.load(f)

    out = PlanningAgent().plan(enriched_ir)
    print(f"Contracts ({len(out.contracts)}):\n")
    for c in out.contracts:
        print(f"  [{c.fr_id}] ({c.mvc_layer}) {c.signature}")
        print(f"        -> {c.file_path}   prereqs={c.prerequisite_fr_ids}")
    if out.notes:
        print("\nNotes:")
        for note in out.notes:
            print(f"  - {note}")