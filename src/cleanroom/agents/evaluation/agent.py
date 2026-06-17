"""Evaluation Agent — pass@k.

The ONE stage where spec-derived CODE and spec-derived TESTS are brought together,
and only AFTER both are frozen. It feeds nothing back into generation; it only
measures, so the clean-room isolation is preserved:

  * Code samples are produced by the Code Agent, which still sees only the spec.
  * The tests were derived by the Test Agent with no view of any code.
  * Certification just scores the two independently-produced artifacts.

Metric: pass@k (Chen et al., 2021 — the HumanEval/Codex metric). For each feature
we generate n independent code samples from the spec, judge each sample against the
feature's spec-derived test cases, count how many pass ALL of them (c), and report

    pass@k = mean_features( 1 - C(n-c, k) / C(n, k) ).

The pass/fail oracle is an LLM judge, because the tests are natural-language
black-box designs (not executable). The judge runs at temperature 0 for stability,
but a model-based oracle is inherently not perfectly deterministic.
"""

import json
import sys
from pathlib import Path
from statistics import mean

from src.cleanroom.agents.evaluation.metric import pass_at_k
from src.cleanroom.agents.evaluation.schema.certification import (
    CertificationResult,
    FeatureCertification,
    FeatureJudgement,
)
from src.cleanroom.agents.code.agent import CodeAgent
from src.cleanroom.agents.test.agent import TestAgent
from src.cleanroom.agents.test.tools.spec_reader import feature_units
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.prompt_renderer import PromptRenderer


class CertificationAgent:
    def __init__(
        self,
        code_llm=None,
        judge_llm=None,
        n: int = 5,
        k_values=(1, 5),
        temperature: float = 0.8,
    ) -> None:
        self.n = n
        self.k_values = [k for k in k_values if k <= n]
        # Samples need diversity -> temperature > 0. The judge wants stability -> 0.
        self.code_llm = code_llm if code_llm is not None else get_llm(temperature=temperature)
        self.judge_llm = judge_llm if judge_llm is not None else get_llm(temperature=0.0)
        self.renderer = PromptRenderer()

    def certify(self, ir: dict) -> CertificationResult:
        if not (ir.get("planning") or {}).get("contracts"):
            raise ValueError("CertificationAgent requires an IR with 'planning.contracts' (run the pipeline first).")

        # Oracle: spec-derived tests. Reuse the IR's if present; else derive them now.
        tests = ir.get("generated_tests") or TestAgent().generate(ir).model_dump()
        feature_cases = {f["feature_id"]: f["cases"] for f in tests["features"] if f["cases"]}
        units = {u["feature_id"]: u for u in feature_units(ir)}

        # Generate n independent code samples. Each call still sees ONLY the spec.
        code_agent = CodeAgent(llm=self.code_llm)
        samples = [code_agent.generate(ir) for _ in range(self.n)]

        notes: list[str] = []
        features_out: list[FeatureCertification] = []
        for feature_id, cases in feature_cases.items():
            unit = units.get(feature_id)
            if unit is None:
                notes.append(f"Feature {feature_id} has tests but no spec unit; skipped.")
                continue

            passing = 0  # c: samples that pass ALL of the feature's test cases
            for sample in samples:
                files, prereq_ifaces = self._feature_code(sample, feature_id, ir)
                if not files:
                    continue  # no code produced for this feature -> this sample fails
                judgement = self._judge(unit, files, prereq_ifaces, cases)
                if judgement.verdicts and all(v.verdict == "pass" for v in judgement.verdicts):
                    passing += 1

            pass_at = {f"pass@{k}": pass_at_k(self.n, passing, k) for k in self.k_values}
            features_out.append(
                FeatureCertification(
                    feature_id=feature_id,
                    name=unit.get("name", ""),
                    n_samples=self.n,
                    n_test_cases=len(cases),
                    passing_samples=passing,
                    pass_at=pass_at,
                )
            )

        aggregate = {
            f"pass@{k}": (mean(f.pass_at[f"pass@{k}"] for f in features_out) if features_out else 0.0)
            for k in self.k_values
        }
        model = getattr(self.code_llm, "model_name", getattr(self.code_llm, "model", ""))
        return CertificationResult(
            model=str(model),
            n=self.n,
            k_values=self.k_values,
            features=features_out,
            aggregate_pass_at=aggregate,
            notes=notes,
        )

    def enrich(self, ir: dict) -> dict:
        """Run certify() and fold the result into the IR under 'certification'."""
        return {**ir, "certification": self.certify(ir).model_dump()}

    def run(self, ir: dict, output_dir: Path = Path("outputs/generated")) -> CertificationResult:
        result = self.certify(ir)
        self.write_report(result, output_dir / ir.get("project_name", "project"))
        return result

    # --- helpers ---------------------------------------------------------------
    def _feature_code(self, sample, feature_id: str, ir: dict):
        """A feature's own generated files + the signatures of its prerequisites, for one sample."""
        contracts = ir["planning"]["contracts"]
        by_fr = {c["fr_id"]: c for c in contracts}
        own_frs = {c["fr_id"] for c in contracts if c["feature_id"] == feature_id}
        prereq_frs = {
            pid
            for c in contracts
            if c["feature_id"] == feature_id
            for pid in c.get("prerequisite_fr_ids", [])
            if pid not in own_frs
        }
        files = [f for f in sample.files if f.fr_id in own_frs]
        # Prerequisite interfaces are the planner's contract signatures (spec-derived),
        # not anything extracted from generated code.
        prereq_ifaces = [
            f"# {by_fr[pid]['file_path']}\n{by_fr[pid]['signature']}"
            for pid in sorted(prereq_frs)
            if pid in by_fr
        ]
        return files, prereq_ifaces

    def _judge(self, unit: dict, files, prereq_ifaces, cases) -> FeatureJudgement:
        prompt = self.renderer.render(
            "judge_feature.j2",
            {
                "feature_id": unit["feature_id"],
                "name": unit.get("name", ""),
                "requirements": unit.get("requirements", []),
                "files": [{"path": f.path, "mvc_layer": f.mvc_layer, "content": f.content} for f in files],
                "prerequisites": prereq_ifaces,
                "test_cases": cases,
            },
        )
        return self.judge_llm.with_structured_output(FeatureJudgement).invoke(prompt)

    @staticmethod
    def write_report(result: CertificationResult, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        ks = result.k_values
        lines = [
            "# Certification report — pass@k",
            "",
            f"_Model: {result.model or 'n/a'} · samples n={result.n} · "
            f"features certified: {len(result.features)}_",
            "",
            "## Aggregate (mean across features)",
        ]
        lines += [f"- **pass@{k}**: {result.aggregate_pass_at.get(f'pass@{k}', 0.0):.3f}" for k in ks]
        lines += [
            "",
            "## Per feature",
            "",
            "| feature | name | cases | c/n | " + " | ".join(f"pass@{k}" for k in ks) + " |",
            "|---|---|---|---|" + "---|" * len(ks),
        ]
        for f in result.features:
            cells = " | ".join(f"{f.pass_at.get(f'pass@{k}', 0.0):.3f}" for k in ks)
            lines.append(
                f"| {f.feature_id} | {f.name} | {f.n_test_cases} | "
                f"{f.passing_samples}/{f.n_samples} | {cells} |"
            )
        if result.notes:
            lines += ["", "## Notes", *[f"- {n}" for n in result.notes]]
        dest = output_dir / "certification_report.md"
        dest.write_text("\n".join(lines) + "\n")
        return dest


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m src.cleanroom.agents.certification.agent <full_ir.json>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as fh:
        enriched_ir = json.load(fh)

    agent = CertificationAgent()
    print(f"Generating {agent.n} code samples per feature and judging them against the spec-derived tests...\n")
    result = agent.run(enriched_ir)
    for f in result.features:
        ks = "  ".join(f"pass@{k}={f.pass_at[f'pass@{k}']:.3f}" for k in result.k_values)
        print(f"  {f.feature_id}  {f.name[:28]:28}  c/n={f.passing_samples}/{f.n_samples}  {ks}")
    print("\nAggregate: " + "  ".join(f"pass@{k}={result.aggregate_pass_at[f'pass@{k}']:.3f}" for k in result.k_values))
    print(f"Report written under outputs/generated/{enriched_ir.get('project_name', 'project')}/")
