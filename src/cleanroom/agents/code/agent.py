"""Code Agent.

Generates MVC source code from the specification, walking the planner's per-FR
CONTRACTS one at a time. One LLM call per contract, each scoped to ONLY that
requirement's contract (signature + docstring + spec text) plus the *signatures* of
its prerequisite contracts — never the whole IR, never any test artifact.

==================  STRUCTURAL ISOLATION (the project's core)  ==================
This agent generates code as a pure function of the SPECIFICATION. By construction
it cannot receive anything from testing:

  * No public method takes a test-related parameter (no test_results, failures,
    feedback, expected outputs, etc.). The only input is `ir` (the spec + the
    spec-derived planning contracts).
  * There is no retry/debugging loop that regenerates code from test outcomes.
  * It never imports the test agent and never reads `generated_tests`.

Do not add a feedback path here, even to "improve" results — that isolation is the
whole point of the pipeline.
================================================================================
"""

import json
import sys
from pathlib import Path

from src.cleanroom.agents.code.schema.code import FileImplementation, GeneratedCode, GeneratedFile
from src.cleanroom.agents.planning.agent import PlanningAgent, _slug
from src.cleanroom.utils.contracts import prereq_ifaces, requirement_text
from src.cleanroom.utils.ir import normalize_ir_features
from src.cleanroom.targets import get_target
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.prompt_renderer import PromptRenderer


class CodeAgent:
    def __init__(self, llm=None, stack: str = "python", language: str = "python") -> None:
        # `llm` is injectable purely so tests can avoid network calls; it is NOT a
        # channel for test data. Defaults to the shared gpt-4o-mini client.
        self.llm = llm if llm is not None else get_llm()
        self.renderer = PromptRenderer()
        # Target stack for the run (e.g. "fastapi"). Threaded into the code prompt as
        # STRUCTURAL conventions only — never test-derived — so isolation/pass@k hold.
        self.stack = stack
        # The language target picks the codegen template (python vs java); knowing the target
        # language is structural, not seeing tests — isolation holds.
        self.language = language
        self.target = get_target(language)

    def generate(self, ir: dict, skip_feature_ids: set[str] | None = None) -> GeneratedCode:
        """Generate code for every contract, in planning (dependency) order.

        Input is the spec + the spec-derived contracts only. The planner already owns
        the signature, docstring, mvc_layer, file_path and prerequisite ids of each FR;
        this agent only turns each contract into a concrete file body.

        ``skip_feature_ids`` omits whole features whose logic ships from elsewhere (the Dafny
        proof tier): those features get an adapter via :meth:`generate_adapter` instead.
        """
        contracts = (ir.get("planning") or {}).get("contracts")
        if not contracts:
            raise ValueError("CodeAgent requires an IR enriched with 'planning.contracts'.")
        PlanningAgent.normalize_ir_planning(ir)
        normalize_ir_features(ir)
        contracts = ir["planning"]["contracts"]

        skip = set(skip_feature_ids or ())
        req_text = self._requirement_index(ir)        # fr_id -> spec requirement text
        by_fr = {c["fr_id"]: c for c in contracts}     # fr_id -> contract (for prereq signatures)
        files: list[GeneratedFile] = []

        for contract in contracts:                     # already in dependency order
            if contract["feature_id"] in skip:
                continue
            fr_id = contract["fr_id"]

            # (a) ONLY this FR's contract + its spec text.
            # (b) ONLY the signatures of prerequisite contracts — never their bodies,
            #     and they are taken from the planner's contracts, not from any generated
            #     code, so the input here is purely spec-derived.
            prerequisites = prereq_ifaces(contract, by_fr)

            prompt = self.renderer.render(
                self.target.code_template(),
                {
                    "fr_id": fr_id,
                    "feature_id": contract["feature_id"],
                    "mvc_layer": contract["mvc_layer"],
                    "signature": contract["signature"],
                    "docstring": contract["docstring"],
                    "requirement": req_text.get(fr_id, ""),
                    "prerequisites": prerequisites,
                    "stack": self.stack,
                    "example_inputs_json": contract.get("example_inputs_json", "{}"),
                    "expected_return_json": contract.get("expected_return_json", "null"),
                    "error_mode": contract.get("error_mode", "raise"),
                    "failure_inputs_json": contract.get("failure_inputs_json", ""),
                    "entity_identifier": contract.get("entity_identifier", ""),
                },
            )

            # One structured call per contract. Schema via with_structured_output —
            # no JSON schema in the prompt.
            impl: FileImplementation = self.llm.with_structured_output(FileImplementation).invoke(prompt)

            # The planner owns ids/path/layer; the LLM only supplies the body.
            files.append(
                GeneratedFile(
                    fr_id=fr_id,
                    feature_id=contract["feature_id"],
                    path=contract["file_path"],
                    mvc_layer=contract["mvc_layer"],
                    content=impl.content,
                )
            )

        return GeneratedCode(files=files)

    def generate_adapter(self, ir: dict, feature_id: str, module: str,
                         dafny_source: str) -> GeneratedFile:
        """Write the thin FastAPI glue over a PROVED Dafny core (no business logic here).

        For a feature the proof tier verified, the logic ships as the compiled Dafny module; this
        emits ONE controller file with a route per FR that imports the compiled core, loads/saves
        the state in the DB, marshals request<->Dafny via ``dafny_marshal``, and calls the proved
        ``Normalize(Apply(state, action))``. Still spec-only + the agent's own proved Dafny — it
        never reads tests, so isolation holds.

        ``module`` is the Dafny module base (e.g. ``F4_1``): the compiled core dir is
        ``<module>-py`` and the importable core module is ``<module>Domain``.
        """
        PlanningAgent.normalize_ir_planning(ir)
        normalize_ir_features(ir)
        contracts = [c for c in ir["planning"]["contracts"] if c["feature_id"] == feature_id]
        if not contracts:
            raise ValueError(f"no contracts for feature {feature_id}")
        req_text = self._requirement_index(ir)
        feat = next((f for f in ir.get("features", []) if str(f.get("id")) == str(feature_id)), {})

        prompt = self.renderer.render(
            "generate_adapter.j2",
            {
                "feature_id": feature_id,
                "feature_name": feat.get("name", ""),
                # Dafny's Python backend mangles `_` -> `__` in module names, so the Dafny module
                # `F4_1Domain` compiles to the importable Python module `F4__1Domain`.
                "core_module": f"{module}Domain".replace("_", "__"),
                "core_dir": f"{module}-py",              # compiled core directory (on sys.path, NOT mangled)
                "dafny_source": dafny_source,
                "contracts": [
                    {
                        "fr_id": c["fr_id"],
                        "signature": c.get("signature", ""),
                        "file_path": c.get("file_path", ""),
                        "requirement": req_text.get(c["fr_id"], ""),
                        "contract": c.get("contract", {}),
                        "entity_identifier": c.get("entity_identifier", ""),
                    }
                    for c in contracts
                ],
            },
        )
        impl: FileImplementation = self.llm.with_structured_output(FileImplementation).invoke(prompt)
        path = f"controllers/f{feature_id.replace('.', '_')}_adapter.py"
        return GeneratedFile(
            fr_id=contracts[0]["fr_id"],
            feature_id=feature_id,
            path=path,
            mvc_layer="controller",
            content=impl.content,
        )

    # ===================  TEST-INFORMED REPAIR (RECOVERY ONLY)  ===================
    # DELIBERATE, CONTAINED clean-room break, enabled by the user for the recovery loop:
    # this method — and ONLY this method — receives failing TEST CASES and regenerates code
    # to satisfy them. It is never called on the first pass (that stays clean-room via
    # `generate`); it runs only after a feature has already failed both proof and pass@1.
    # Features repaired here are labelled "TESTED (repaired-with-tests)" so the report never
    # claims a clean-room pass we did not earn. Do NOT call this from `generate`/`run`.
    # =============================================================================
    def regenerate_with_test_feedback(
        self, ir: dict, feature_ids: set[str], failures: list[dict]
    ) -> list[GeneratedFile]:
        """Regenerate the code of the given (failing) features WITH their failing test cases.

        ``failures`` is the certification result's per-case diagnostics
        (fr_id/inputs/expected/reason). For every contract whose feature is in ``feature_ids``
        we re-emit its file, feeding in that FR's failing cases. The Code Agent's temperature is
        set by the caller (the recovery loop escalates it per iteration). Returns the regenerated
        files only — the caller swaps them into ``generated_code`` by fr_id.
        """
        contracts = (ir.get("planning") or {}).get("contracts")
        if not contracts:
            raise ValueError("CodeAgent.regenerate_with_test_feedback requires 'planning.contracts'.")
        PlanningAgent.normalize_ir_planning(ir)
        normalize_ir_features(ir)
        contracts = ir["planning"]["contracts"]
        by_fr = {c["fr_id"]: c for c in contracts}
        req_text = self._requirement_index(ir)
        prior_by_fr = {f["fr_id"]: f["content"]
                       for f in (ir.get("generated_code") or {}).get("files", []) if f.get("fr_id")}

        fails_by_fr: dict[str, list[dict]] = {}
        for d in failures:
            fails_by_fr.setdefault(d.get("fr_id", ""), []).append({
                "description": d.get("description", ""),
                "inputs": d.get("inputs", ""),
                "expected": d.get("expected", ""),
                "reason": d.get("reason", ""),
            })

        feature_ids = set(feature_ids)
        out: list[GeneratedFile] = []
        for contract in contracts:
            if contract["feature_id"] not in feature_ids:
                continue
            fr_id = contract["fr_id"]
            prompt = self.renderer.render(
                "regenerate_with_feedback.j2",
                {
                    "fr_id": fr_id,
                    "feature_id": contract["feature_id"],
                    "mvc_layer": contract["mvc_layer"],
                    "signature": contract["signature"],
                    "docstring": contract["docstring"],
                    "requirement": req_text.get(fr_id, ""),
                    "prerequisites": prereq_ifaces(contract, by_fr),
                    "prior_content": prior_by_fr.get(fr_id, ""),
                    "failing_cases": fails_by_fr.get(fr_id, []),
                    "stack": self.stack,
                    "example_inputs_json": contract.get("example_inputs_json", "{}"),
                    "expected_return_json": contract.get("expected_return_json", "null"),
                    "error_mode": contract.get("error_mode", "raise"),
                    "failure_inputs_json": contract.get("failure_inputs_json", ""),
                    "entity_identifier": contract.get("entity_identifier", ""),
                },
            )
            impl: FileImplementation = self.llm.with_structured_output(FileImplementation).invoke(prompt)
            out.append(GeneratedFile(
                fr_id=fr_id,
                feature_id=contract["feature_id"],
                path=contract["file_path"],
                mvc_layer=contract["mvc_layer"],
                content=impl.content,
            ))
        return out

    def run(self, ir: dict, output_dir: Path = Path("outputs/generated")) -> GeneratedCode:
        """Generate code and write it out, organized by MVC layer."""
        code = self.generate(ir)
        self.write_files(code, output_dir / ir.get("project_name", "project"))
        return code

    @staticmethod
    def write_files(code: GeneratedCode, output_dir: Path) -> list[Path]:
        """Write every generated file under output_dir, using the path from the contract.

        The planning agent sets file_path as '{layer_dir}/{func}.py' (e.g. 'models/func.py'),
        so the final destination is output_dir/models/func.py — matching the contract exactly.
        """
        written: list[Path] = []
        used: set[Path] = set()
        for f in code.files:
            dest = output_dir / f.path
            if dest in used:  # avoid clobbering a same-named file from another contract
                dest = dest.with_name(f"{dest.stem}_{_slug(f.fr_id)}{dest.suffix}")
                f.path = str(dest.relative_to(output_dir))
            used.add(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(f.content)
            written.append(dest)
        return written

    # --- helpers ---------------------------------------------------------------
    @staticmethod
    def _requirement_index(ir: dict) -> dict[str, str]:
        """Map functional-requirement id -> its spec text, from the spec's features."""
        index: dict[str, str] = {}
        for feature in ir.get("features", []):
            for req in feature.get("functional_requirements", []):
                index[req["id"]] = requirement_text(req)
        return index


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m src.cleanroom.agents.code.agent <enriched_ir.json>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as fh:
        enriched_ir = json.load(fh)

    generated_code = CodeAgent().run(enriched_ir)
    for file in generated_code.files:
        print(f"  [{file.mvc_layer}] {file.fr_id} -> {file.path}  ({len(file.content)} chars)")
