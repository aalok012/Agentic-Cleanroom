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
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.prompt_renderer import PromptRenderer


class CodeAgent:
    def __init__(self, llm=None) -> None:
        # `llm` is injectable purely so tests can avoid network calls; it is NOT a
        # channel for test data. Defaults to the shared gpt-4o-mini client.
        self.llm = llm if llm is not None else get_llm()
        self.renderer = PromptRenderer()

    def generate(self, ir: dict) -> GeneratedCode:
        """Generate code for every contract, in planning (dependency) order.

        Input is the spec + the spec-derived contracts only. The planner already owns
        the signature, docstring, mvc_layer, file_path and prerequisite ids of each FR;
        this agent only turns each contract into a concrete file body.
        """
        contracts = (ir.get("planning") or {}).get("contracts")
        if not contracts:
            raise ValueError("CodeAgent requires an IR enriched with 'planning.contracts'.")

        req_text = self._requirement_index(ir)        # fr_id -> spec requirement text
        by_fr = {c["fr_id"]: c for c in contracts}     # fr_id -> contract (for prereq signatures)
        files: list[GeneratedFile] = []

        for contract in contracts:                     # already in dependency order
            fr_id = contract["fr_id"]

            # (a) ONLY this FR's contract + its spec text.
            # (b) ONLY the signatures of prerequisite contracts — never their bodies,
            #     and they are taken from the planner's contracts, not from any generated
            #     code, so the input here is purely spec-derived.
            prerequisites = [
                {
                    "fr_id": pid,
                    "layer": by_fr[pid]["mvc_layer"],
                    "signature": by_fr[pid]["signature"],
                }
                for pid in contract.get("prerequisite_fr_ids", [])
                if pid in by_fr
            ]

            prompt = self.renderer.render(
                "generate_code.j2",
                {
                    "fr_id": fr_id,
                    "feature_id": contract["feature_id"],
                    "mvc_layer": contract["mvc_layer"],
                    "signature": contract["signature"],
                    "docstring": contract["docstring"],
                    "requirement": req_text.get(fr_id, ""),
                    "prerequisites": prerequisites,
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

    def enrich(self, ir: dict) -> dict:
        """Run generate() and fold the result into the IR under 'generated_code'."""
        return {**ir, "generated_code": self.generate(ir).model_dump()}

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
                dest = dest.with_name(f"{dest.stem}_{f.fr_id.replace('.', '_')}{dest.suffix}")
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
                index[req["id"]] = req.get("text", req.get("description", ""))
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
