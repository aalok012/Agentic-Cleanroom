"""Recovery loop — the prove-or-test fallback's re-prove + test-informed regen cycle.

Offline: a fake LLM stands in for the code-repair author and ``_certify`` is stubbed with a
canned sequence of certification results, so these lock the deterministic ORCHESTRATION —
escalation schedule, file swapping, the contained clean-room break, and the final per-feature
labels. The repair *quality* and real Dafny re-proving are LLM/solver concerns exercised on a
live --prove --certify run, not here.
"""

from statistics import mean
from types import SimpleNamespace

import pytest

from src.cleanroom.agents.code.agent import CodeAgent
from src.cleanroom.agents.evaluation.schema.certification import (
    CertificationResult,
    FeatureCertification,
)
from src.cleanroom.agents.recovery import loop as loop_mod
from src.cleanroom.agents.recovery.loop import RecoveryLoop, failing_feature_ids


def _ir():
    return {
        "project_name": "demo",
        "features": [
            {"id": "4.1", "name": "Place Order",
             "functional_requirements": [{"id": "4.1.1", "text": "place an order"}]},
            {"id": "4.2", "name": "Cancel Order",
             "functional_requirements": [{"id": "4.2.1", "text": "cancel an order"}]},
        ],
        "planning": {"contracts": [
            {"fr_id": "4.1.1", "feature_id": "4.1", "mvc_layer": "controller",
             "signature": "place_order(name)", "docstring": "d", "file_path": "controllers/place.py",
             "prerequisite_fr_ids": []},
            {"fr_id": "4.2.1", "feature_id": "4.2", "mvc_layer": "controller",
             "signature": "cancel_order(id)", "docstring": "d", "file_path": "controllers/cancel.py",
             "prerequisite_fr_ids": []},
        ]},
        "generated_code": {"files": [
            {"fr_id": "4.1.1", "feature_id": "4.1", "path": "controllers/place.py",
             "mvc_layer": "controller", "content": "# old 4.1\n"},
            {"fr_id": "4.2.1", "feature_id": "4.2", "path": "controllers/cancel.py",
             "mvc_layer": "controller", "content": "# old 4.2\n"},
        ]},
    }


class _FakeLLM:
    """Returns a fixed file body; records the prompts it was given."""

    def __init__(self, capture=None):
        self.capture = capture

    def with_structured_output(self, schema):
        cap = self.capture

        class S:
            def invoke(self, prompt):
                if cap is not None:
                    cap.append(prompt)
                return SimpleNamespace(content="# repaired\n")

        return S()


def _feat(fid: str, p1: float) -> FeatureCertification:
    return FeatureCertification(
        feature_id=fid, name="", n_samples=1, n_test_cases=1,
        passing_samples=int(p1 >= 1.0), pass_at={"pass@1": p1},
        cases_passed=int(p1 >= 1.0), cases_total=1, case_pass_rate=p1,
    )


def _result(pass_map: dict[str, float], failures=None) -> CertificationResult:
    feats = [_feat(fid, p) for fid, p in pass_map.items()]
    return CertificationResult(
        n=1, k_values=[1], features=feats, frs=[],
        aggregate_pass_at={"pass@1": mean(pass_map.values()) if pass_map else 0.0},
        aggregate_case_pass_rate=mean(pass_map.values()) if pass_map else 0.0,
        failures=failures or [],
    )


# --- the test-informed regeneration (the contained clean-room break) ------------
def test_regenerate_with_feedback_targets_only_failing_feature_and_embeds_cases():
    prompts: list = []
    files = CodeAgent(llm=_FakeLLM(prompts), stack="fastapi").regenerate_with_test_feedback(
        _ir(), {"4.1"},
        failures=[{"fr_id": "4.1.1", "description": "place then read",
                   "inputs": '{"name": "x"}', "expected": '{"ok": true}',
                   "reason": "returned None"}],
    )
    assert [f.fr_id for f in files] == ["4.1.1"]          # only the failing feature
    p = prompts[0]
    assert "FAILING TEST CASES" in p                       # the clean-room break is explicit
    assert "returned None" in p and '{"name": "x"}' in p   # the actual failing case is fed in


def test_failing_feature_ids_uses_pass_at_1():
    res = _result({"4.1": 0.0, "4.2": 1.0, "4.3": 0.5})
    assert failing_feature_ids(res) == {"4.1", "4.3"}


# --- loop orchestration (stub certify; fake LLM for regen) ----------------------
class _StubLoop(RecoveryLoop):
    """RecoveryLoop with a canned certification sequence (no oracle subprocess)."""

    def __init__(self, ir, canned, **kw):
        super().__init__(ir, **kw)
        self._canned = list(canned)

    def _certify(self):
        return self._canned.pop(0)


def test_loop_repairs_with_tests_and_labels(tmp_path, monkeypatch):
    monkeypatch.setattr(loop_mod, "get_llm", lambda *a, **k: _FakeLLM())
    ir = _ir()
    loop = _StubLoop(
        ir, canned=[_result({"4.1": 1.0, "4.2": 1.0})],   # after one pass 4.1 now passes
        stack="python", proj=None, proved_feature_ids=set(),
        proved_modules={}, proved_sources={}, code_dir=tmp_path / "code",
        adapter_mode=False, max_loops=2,
    )
    out = loop.run(_result({"4.1": 0.0, "4.2": 1.0}))      # 4.1 starts failing

    assert out["repaired_by_tests"] == ["4.1"]
    assert out["uncertified"] == []
    assert out["labels"]["4.1"] == "TESTED (repaired-with-tests)"
    assert out["labels"]["4.2"] == "TESTED (clean-room)"
    # the repaired file was swapped into generated_code
    new = {f["fr_id"]: f["content"] for f in ir["generated_code"]["files"]}
    assert new["4.1.1"] == "# repaired\n" and new["4.2.1"] == "# old 4.2\n"
    assert len(out["loops"]) == 1                          # stopped early once it passed


def test_loop_gives_up_and_marks_uncertified_with_escalation(tmp_path, monkeypatch):
    monkeypatch.setattr(loop_mod, "get_llm", lambda *a, **k: _FakeLLM())
    loop = _StubLoop(
        _ir(), canned=[_result({"4.1": 0.0, "4.2": 1.0}),  # still failing after pass 1
                       _result({"4.1": 0.0, "4.2": 1.0})],  # still failing after pass 2
        stack="python", proj=None, proved_feature_ids=set(),
        proved_modules={}, proved_sources={}, code_dir=tmp_path / "code",
        adapter_mode=False, max_loops=2,
    )
    out = loop.run(_result({"4.1": 0.0, "4.2": 1.0}))

    assert out["uncertified"] == ["4.1"]
    assert out["labels"]["4.1"] == "UNCERTIFIED"
    assert len(out["loops"]) == 2                           # used the full budget
    # escalation schedule: rounds 6→8, temp 0.4→0.6
    assert [(l["dafny_rounds"], l["code_temp"]) for l in out["loops"]] == [(6, 0.4), (8, 0.6)]
