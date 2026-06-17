"""Test Agent.

Derives black-box test cases from the SPECIFICATION, one feature at a time. One
LLM call per feature, each scoped to ONLY that feature's requirements — never the
whole IR.

==================  STRUCTURAL ISOLATION (the project's core)  ==================
This agent is the mirror image of the Code Agent: tests are a pure function of the
SPECIFICATION, and by construction the agent cannot see the implementation.

  * No public method takes a code-related parameter (no code, implementation,
    source, etc.). The only input is `ir`, and only its spec slice is read.
  * It never imports anything from src/cleanroom/agents/code/.
  * It never reads the 'generated_code' key, even though that key exists in the IR.
    All IR access goes through spec_reader.feature_units, which touches only
    ir['features'].
  * It GENERATES tests; it does not execute them against any implementation. Running
    tests against code is a separate, later certification stage.

Do not let this agent peek at the generated code to "make better tests" — that would
destroy the spec/code separation that is the whole point of the pipeline.
================================================================================
"""

import json
import sys
from pathlib import Path

from src.cleanroom.agents.test.schema.tests import FeatureTests, GeneratedTests
from src.cleanroom.agents.test.tools.spec_reader import feature_units
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.prompt_renderer import PromptRenderer


class TestAgent:
    # Keep pytest from collecting this class as a test (its name starts with "Test").
    __test__ = False

    def __init__(self, llm=None) -> None:
        # `llm` is injectable only so tests can avoid network calls; it is NOT a
        # channel for implementation data. Defaults to the shared gpt-4o-mini client.
        self.llm = llm if llm is not None else get_llm()
        self.renderer = PromptRenderer()

    def generate(self, ir: dict) -> GeneratedTests:
        """Generate tests for every feature from the spec only. Input is the spec."""
        features: list[FeatureTests] = []

        for unit in feature_units(ir):  # the ONLY IR read: features/requirements
            prompt = self.renderer.render(
                "generate_tests.j2",
                {
                    "feature_id": unit["feature_id"],
                    "name": unit["name"],
                    "description": unit["description"],
                    "requirements": unit["requirements"],
                },
            )

            # One structured call per feature. Schema via with_structured_output —
            # no JSON schema in the prompt.
            result = self.llm.with_structured_output(FeatureTests).invoke(prompt)

            # The spec owns feature_id; don't trust the LLM to echo it correctly.
            features.append(FeatureTests(feature_id=unit["feature_id"], cases=list(result.cases)))

        return GeneratedTests(features=features)

    def enrich(self, ir: dict) -> dict:
        """Run generate() and fold the result into the IR under 'generated_tests'."""
        return {**ir, "generated_tests": self.generate(ir).model_dump()}

    def run(self, ir: dict, output_dir: Path = Path("outputs/generated")) -> GeneratedTests:
        """Generate tests from the spec and write them out as browsable files."""
        tests = self.generate(ir)
        self.write_files(tests, output_dir / ir.get("project_name", "project") / "tests")
        return tests

    @staticmethod
    def write_files(tests: GeneratedTests, output_dir: Path) -> list[Path]:
        """Write one human-readable Markdown file per feature under output_dir.

        Pure persistence of the cases the agent already produced — this writer reads
        only the spec-derived `tests`, never any implementation. The cases are
        black-box test *designs* (natural-language inputs/expected), so Markdown is a
        truer representation than a runnable .py stub would be.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for feature in tests.features:
            lines = [
                f"# Generated tests — feature {feature.feature_id}",
                "",
                f"_Black-box test cases derived from the specification. {len(feature.cases)} case(s)._",
                "",
            ]
            for i, case in enumerate(feature.cases, 1):
                lines += [
                    f"## Case {i} — requirement {case.requirement_id}",
                    f"- **Verifies:** {case.description}",
                    f"- **Inputs:** {case.inputs}",
                    f"- **Expected:** {case.expected}",
                    "",
                ]
            dest = output_dir / f"feature_{feature.feature_id}.md"
            dest.write_text("\n".join(lines))
            written.append(dest)
        return written


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m src.cleanroom.agents.test.agent <enriched_ir.json>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as fh:
        enriched_ir = json.load(fh)

    generated_tests = TestAgent().run(enriched_ir)
    total = 0
    for feature in generated_tests.features:
        print(f"Feature {feature.feature_id}: {len(feature.cases)} test case(s)")
        total += len(feature.cases)
    print(f"\n{len(generated_tests.features)} features, {total} test cases total.")
    print(f"Test files written under outputs/generated/{enriched_ir.get('project_name', 'project')}/tests/")
