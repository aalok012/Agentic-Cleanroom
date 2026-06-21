"""The bounded generate -> verify -> revise loop.

This is the single integration point that makes verification meaningful: it produces ONE
verified GeneratedCode and is called from BOTH places code is generated — run_pipeline.py's
Code stage AND CertificationAgent's per-sample loop — so the pass@k samples are each verified
and revised before they are judged.

The loop is plain sequential Python (no graph framework): generate once, verify all contracts,
then up to `max_rounds` times revise only the failing files and re-verify only those changed
files. Isolation is preserved end to end — the verifier never runs the code and never reads
tests, and the only feedback handed to CodeAgent.revise() is spec-level contract violations.

Deterministic executable smoke tests (canonical I/O from planning contracts) run alongside
the LLM reviewer so signature/import/return-value bugs are caught without test artifacts.
"""

from src.cleanroom.agents.code.agent import CodeAgent
from src.cleanroom.agents.planning.agent import PlanningAgent
from src.cleanroom.agents.verification.agent import VerificationAgent
from src.cleanroom.agents.verification.crosshair_verify import crosshair_verdicts
from src.cleanroom.agents.verification.executable import executable_verdicts, merge_verdicts
from src.cleanroom.agents.verification.schema.verification import VerificationResult


def generate_and_verify(
    ir: dict,
    code_agent: CodeAgent,
    verifier: VerificationAgent,
    max_rounds: int = 2,
):
    """Generate code, then verify/revise up to `max_rounds` times.

    Returns (GeneratedCode, VerificationResult). The GeneratedCode is the (possibly still
    imperfect) revised artifact; the VerificationResult records the final per-contract
    verdicts, how many rounds were used, and any residual failures.
    """
    PlanningAgent.normalize_ir_planning(ir)
    code = code_agent.generate(ir)

    contracts = (ir.get("planning") or {}).get("contracts") or []
    by_fr = {c["fr_id"]: c for c in contracts}
    files_by_fr = {f.fr_id: f for f in code.files}

    def _combined_verdicts(only_fr_ids=None):
        ids = set(only_fr_ids) if only_fr_ids else None
        llm = {
            v.fr_id: v
            for v in verifier.verify_code(ir, code, only_fr_ids=only_fr_ids)
        }
        executable = executable_verdicts(ir, code, only_fr_ids=ids)
        symbolic = crosshair_verdicts(ir, code, only_fr_ids=ids)
        return merge_verdicts(llm, executable, symbolic)

    # verdict per fr_id, kept current as we revise
    verdicts = _combined_verdicts()

    rounds_used = 0
    for _ in range(max_rounds):
        failed = [v for v in verdicts.values() if v.verdict == "fail"]
        if not failed:
            break
        rounds_used += 1
        changed: list[str] = []
        for verdict in failed:
            fr_id = verdict.fr_id
            file = files_by_fr.get(fr_id)
            contract = by_fr.get(fr_id)
            if file is None or contract is None:
                continue  # a missing-file failure can't be revised without a contract/target
            file.content = code_agent.revise(ir, contract, file.content, verdict.violations)
            changed.append(fr_id)
        if not changed:
            break
        verdicts.update(_combined_verdicts(only_fr_ids=changed))

    final = list(verdicts.values())
    result = VerificationAgent._aggregate(
        final, max_rounds=max_rounds, rounds_used=rounds_used, model=verifier.verify_model
    )
    return code, result


def generate_with_executable_fixes(
    ir: dict,
    code_agent: CodeAgent,
    max_rounds: int = 2,
):
    """Generate code, then revise using deterministic canonical I/O checks only.

    No LLM reviewer — cheaper than full ``generate_and_verify``. Uses the same
    subprocess oracle as certification, driven only by planning-contract I/O.
    """
    PlanningAgent.normalize_ir_planning(ir)
    code = code_agent.generate(ir)

    contracts = (ir.get("planning") or {}).get("contracts") or []
    by_fr = {c["fr_id"]: c for c in contracts}
    files_by_fr = {f.fr_id: f for f in code.files}

    def _deterministic(only_fr_ids=None):
        ids = set(only_fr_ids) if only_fr_ids else None
        return merge_verdicts(
            executable_verdicts(ir, code, only_fr_ids=ids),
            crosshair_verdicts(ir, code, only_fr_ids=ids),
        )

    verdicts = _deterministic()
    rounds_used = 0
    for _ in range(max_rounds):
        failed = [v for v in verdicts.values() if v.verdict == "fail"]
        if not failed:
            break
        rounds_used += 1
        changed: list[str] = []
        for verdict in failed:
            fr_id = verdict.fr_id
            file = files_by_fr.get(fr_id)
            contract = by_fr.get(fr_id)
            if file is None or contract is None:
                continue
            file.content = code_agent.revise(ir, contract, file.content, verdict.violations)
            changed.append(fr_id)
        if not changed:
            break
        verdicts.update(_deterministic(only_fr_ids=changed))

    return code
