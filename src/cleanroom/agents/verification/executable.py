"""Deterministic contract smoke tests — run canonical I/O without reading test artifacts.

Uses the same subprocess runner as certification, but inputs/expected values come only
from planning contracts (spec-derived), not from the Test Agent.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from src.cleanroom.agents.code.agent import CodeAgent
from src.cleanroom.agents.code.schema.code import GeneratedCode
from src.cleanroom.agents.evaluation.runner import run_case
from src.cleanroom.agents.verification.schema.verification import ContractVerdict, ContractViolation


def executable_verdicts(
    ir: dict,
    code: GeneratedCode,
    only_fr_ids: set[str] | None = None,
    timeout: float = 10.0,
) -> dict[str, ContractVerdict]:
    """Return per-fr_id verdicts from canonical happy-path (and optional failure) calls."""
    contracts = (ir.get("planning") or {}).get("contracts") or []
    by_fr = {c["fr_id"]: c for c in contracts}
    files_by_fr = {f.fr_id: f for f in code.files}
    out: dict[str, ContractVerdict] = {}

    with tempfile.TemporaryDirectory(prefix="cleanroom_exec_") as tmp:
        code_dir = Path(tmp) / "code"
        CodeAgent.write_files(code, code_dir)

        for contract in contracts:
            fr_id = contract["fr_id"]
            if only_fr_ids is not None and fr_id not in only_fr_ids:
                continue
            file = files_by_fr.get(fr_id)
            if file is None or not (file.content or "").strip():
                continue

            violations: list[ContractViolation] = []
            happy = {
                "inputs_json": contract.get("example_inputs_json", "{}"),
                "expected_json": contract.get("expected_return_json", "null"),
                "oracle": "eq",
            }
            ok, reason = run_case(
                code_dir,
                contract.get("file_path", file.path),
                contract.get("signature", ""),
                happy,
                timeout=timeout,
            )
            if not ok:
                violations.append(
                    ContractViolation(
                        contract_clause="canonical_call",
                        observation=(
                            f"fn(**{contract.get('example_inputs_json', '{}')}) must succeed and "
                            f"return {contract.get('expected_return_json', 'null')!r}, but: {reason}"
                        ),
                    )
                )

            failure_json = (contract.get("failure_inputs_json") or "").strip()
            if failure_json and failure_json not in ("{}", ""):
                fail_case = {
                    "inputs_json": failure_json,
                    "expected_json": '{"raises": "ValueError"}',
                    "oracle": "raises",
                }
                ok, reason = run_case(
                    code_dir,
                    contract.get("file_path", file.path),
                    contract.get("signature", ""),
                    fail_case,
                    timeout=timeout,
                )
                if not ok:
                    violations.append(
                        ContractViolation(
                            contract_clause="precondition",
                            observation=(
                                f"fn(**{failure_json}) must raise ValueError for a violated "
                                f"precondition, but: {reason}"
                            ),
                        )
                    )

            out[fr_id] = ContractVerdict(
                fr_id=fr_id,
                verdict="pass" if not violations else "fail",
                violations=violations,
            )
    return out


def merge_verdicts(*groups: dict[str, ContractVerdict]) -> dict[str, ContractVerdict]:
    """Merge verdict groups; any failure in any group fails the contract."""
    merged: dict[str, ContractVerdict] = {}
    for group in groups:
        for fr_id, verdict in group.items():
            existing = merged.get(fr_id)
            if existing is None:
                merged[fr_id] = verdict
                continue
            if existing.verdict == "fail" and verdict.verdict == "fail":
                seen: set[tuple[str, str]] = set()
                combined: list[ContractViolation] = []
                for viol in existing.violations + verdict.violations:
                    key = (viol.contract_clause, viol.observation)
                    if key not in seen:
                        seen.add(key)
                        combined.append(viol)
                merged[fr_id] = ContractVerdict(fr_id=fr_id, verdict="fail", violations=combined)
            elif verdict.verdict == "fail":
                merged[fr_id] = verdict
    return merged
