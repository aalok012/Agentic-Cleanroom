"""Verification Agent — independent, reasoning-only contract reviewer.

A distinct reviewer that reads the SPEC-DERIVED contract plus the generated code and reasons
about whether the code satisfies the contract. It is the structural opposite of a tester:

==================  ISOLATION (the project's core)  ==================
  * It NEVER executes the code. No subprocess/exec/eval/importlib/pytest anywhere — judging is
    pure reasoning. The moment it ran the code it would become a tester and break the
    spec/code separation, so it only reads and reasons.
  * It NEVER reads ir['generated_tests'] and never imports anything from agents/test/. Its
    feedback to the Code Agent is phrased strictly as CONTRACT-CLAUSE violations (see
    schema/verification.py) — never as test cases — so no test-derived signal can leak into
    code generation.
  * What it MAY read: ir['features'] (requirement text), ir['contracts'] (behavioral
    contracts), ir['planning']['contracts'] (signature/docstring/layer/prerequisites) and the
    code under review, which is passed in as an argument. All of these are spec-stage or the
    artifact being reviewed — never the test oracle.

Independence is the whole point: a reviewer with its own adversarial prompt and a cold read
catches errors that a self-check would rationalize. By default it runs a single pass with the
same model as the code agent; `verify_model` and `passes` allow stronger (opt-in) independence.
================================================================================
"""

import json
import sys
from collections import Counter
from pathlib import Path

from src.cleanroom.agents.verification.schema.verification import (
    ContractVerdict,
    ContractViolation,
    VerificationResult,
)
from src.cleanroom.utils.contracts import prereq_ifaces, requirement_text
from src.cleanroom.utils.ir import normalize_ir_features
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.prompt_renderer import PromptRenderer


class VerificationAgent:
    def __init__(self, llm=None, verify_model: str = "gpt-4o-mini", passes: int = 1) -> None:
        # `llm` is injectable so tests avoid network calls; it is NOT a channel for test data.
        # passes>1 runs the reviewer several times (with diversity) and only fails on agreement.
        self.passes = max(1, passes)
        temperature = 0.0 if self.passes == 1 else 0.3
        self.llm = llm if llm is not None else get_llm(model=verify_model, temperature=temperature)
        self.verify_model = verify_model
        self.renderer = PromptRenderer()

    def verify_code(self, ir: dict, code, only_fr_ids=None) -> list[ContractVerdict]:
        """Return one verdict per contract (optionally only the given fr_ids).

        `code` is the GeneratedCode under review; only its files' content is read. All other
        inputs are spec-derived. This method never executes anything.
        """
        normalize_ir_features(ir)
        contracts = (ir.get("planning") or {}).get("contracts")
        if not contracts:
            raise ValueError("VerificationAgent requires an IR enriched with 'planning.contracts'.")

        req_text = self._requirement_index(ir)
        by_fr = {c["fr_id"]: c for c in contracts}
        files_by_fr = {f.fr_id: f for f in code.files}
        targets = set(only_fr_ids) if only_fr_ids is not None else None

        verdicts: list[ContractVerdict] = []
        for contract in contracts:
            fr_id = contract["fr_id"]
            if targets is not None and fr_id not in targets:
                continue
            file = files_by_fr.get(fr_id)
            if file is None or not (file.content or "").strip():
                # No code produced for this contract -> a coverage failure, no LLM call needed.
                verdicts.append(
                    ContractVerdict(
                        fr_id=fr_id,
                        verdict="fail",
                        violations=[ContractViolation(
                            contract_clause="coverage",
                            observation="No implementation was generated for this requirement.",
                        )],
                    )
                )
                continue
            verdicts.append(self._verify_contract(contract, file.content, req_text, by_fr))
        return verdicts

    def run(self, ir: dict, output_dir: Path = Path("outputs/generated")) -> VerificationResult:
        """Verify the IR's generated_code once (no revise loop) and write a report.

        The revise loop lives in verification/loop.py; this entry point is for a standalone
        one-shot review of ir['generated_code'].
        """
        code = self._generated_code(ir)
        verdicts = self.verify_code(ir, code)
        result = self._aggregate(verdicts, max_rounds=0, rounds_used=0)
        self.write_report(result, output_dir / ir.get("project_name", "project"))
        return result

    # --- helpers ---------------------------------------------------------------
    def _verify_contract(self, contract: dict, code: str, req_text: dict, by_fr: dict) -> ContractVerdict:
        bc = contract.get("contract") or {}
        prerequisites = prereq_ifaces(contract, by_fr)
        prompt = self.renderer.render(
            "verify_contract.j2",
            {
                "fr_id": contract["fr_id"],
                "feature_id": contract["feature_id"],
                "mvc_layer": contract["mvc_layer"],
                "requirement": req_text.get(contract["fr_id"], ""),
                "signature": contract["signature"],
                "docstring": contract["docstring"],
                "stimulus": bc.get("stimulus", ""),
                "precondition": bc.get("precondition", ""),
                "response": bc.get("response", ""),
                "postcondition": bc.get("postcondition", ""),
                "prerequisites": prerequisites,
                "code": code,
            },
        )
        runner = self.llm.with_structured_output(ContractVerdict)
        if self.passes == 1:
            verdict = runner.invoke(prompt)
            verdict.fr_id = contract["fr_id"]  # the contract owns the id, not the LLM
            return verdict
        return self._quorum(contract["fr_id"], [runner.invoke(prompt) for _ in range(self.passes)])

    @staticmethod
    def _quorum(fr_id: str, verdicts: list[ContractVerdict]) -> ContractVerdict:
        """Unanimous-fail combine: fail only if EVERY pass failed (fewest spurious revisions)."""
        fails = [v for v in verdicts if v.verdict == "fail"]
        if len(fails) == len(verdicts):
            seen: set[tuple] = set()
            merged: list[ContractViolation] = []
            for v in fails:
                for viol in v.violations:
                    key = (viol.contract_clause, viol.observation)
                    if key not in seen:
                        seen.add(key)
                        merged.append(viol)
            return ContractVerdict(fr_id=fr_id, verdict="fail", violations=merged)
        return ContractVerdict(fr_id=fr_id, verdict="pass", violations=[])

    @staticmethod
    def _aggregate(verdicts: list[ContractVerdict], max_rounds: int, rounds_used: int,
                   model: str = "") -> VerificationResult:
        failing = [v.fr_id for v in verdicts if v.verdict == "fail"]
        return VerificationResult(
            model=model,
            max_rounds=max_rounds,
            rounds_used=rounds_used,
            verdicts=verdicts,
            n_contracts=len(verdicts),
            n_passing=sum(1 for v in verdicts if v.verdict == "pass"),
            n_failing=len(failing),
            residual_failures=failing,
        )

    @staticmethod
    def _requirement_index(ir: dict) -> dict[str, str]:
        """Map functional-requirement id -> its spec text, from the spec's features."""
        index: dict[str, str] = {}
        for feature in ir.get("features", []):
            for req in feature.get("functional_requirements", []):
                index[req["id"]] = requirement_text(req)
        return index

    @staticmethod
    def _generated_code(ir: dict):
        from src.cleanroom.agents.code.schema.code import GeneratedCode
        code = ir.get("generated_code")
        if not code:
            raise ValueError("VerificationAgent.run requires ir['generated_code'].")
        return GeneratedCode(**code) if isinstance(code, dict) else code

    @staticmethod
    def write_report(result: VerificationResult, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Verification report — contract conformance",
            "",
            f"_Model: {result.model or 'n/a'} · rounds used: {result.rounds_used}/{result.max_rounds}_",
            "",
            f"- contracts: {result.n_contracts}",
            f"- passing: {result.n_passing}",
            f"- failing: {result.n_failing}",
        ]
        if result.residual_failures:
            lines.append(f"- residual failures: {', '.join(result.residual_failures)}")
        lines += ["", "## Per contract", ""]
        for v in result.verdicts:
            mark = "PASS" if v.verdict == "pass" else "FAIL"
            lines.append(f"- [{mark}] {v.fr_id}")
            for viol in v.violations:
                lines.append(f"    - ({viol.contract_clause}) {viol.observation}")
        dest = output_dir / "verification_report.md"
        dest.write_text("\n".join(lines) + "\n")
        return dest


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m src.cleanroom.agents.verification.agent <full_ir.json>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        enriched_ir = json.load(fh)
    result = VerificationAgent().run(enriched_ir)
    print(f"{result.n_passing}/{result.n_contracts} contracts pass; "
          f"failing: {result.residual_failures or 'none'}")
