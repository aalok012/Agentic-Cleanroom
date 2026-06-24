"""Headline run-metrics summary — ALL ratios at FR granularity."""

from run_pipeline import _compute_summary


def _ir():
    # 3 features, 5 FRs total: F1{1.1,1.2}, F2{2.1,2.2}, F3{3.1}
    return {"features": [
        {"id": "1", "functional_requirements": [{"id": "1.1"}, {"id": "1.2"}]},
        {"id": "2", "functional_requirements": [{"id": "2.1"}, {"id": "2.2"}]},
        {"id": "3", "functional_requirements": [{"id": "3.1"}]},
    ]}


def _metrics():
    return {
        "total_seconds": 142.3,
        "tokens": {"input": 120000, "output": 24000, "calls": 30},
        "proved_feature_ids": ["1", "2"],                     # proves FRs 1.1,1.2,2.1,2.2 (4/5)
        "dafny": {"n_features": 3, "n_verified": 2, "features": [
            {"feature_id": "1", "rounds": 2}, {"feature_id": "2", "rounds": 4},
            {"feature_id": "3", "rounds": 6}]},               # F3 attempted, unproved
        "certification": {"aggregate_case_pass_rate": 0.595,
                          "pass_at_1_fr_ids": ["3.1"], "n_total_tested_features": 1},
        "recovery": {"loops_run": 1},
    }


def test_summary_is_fr_level():
    s = _compute_summary(_metrics(), _ir())
    assert s["verification_pass_ratio"] == 0.8       # FRs of proved features {1.1,1.2,2.1,2.2} / 5
    assert s["PassVer@1"] == 1.0                      # {1.1,1.2,2.1,2.2} ∪ {3.1} = 5 / 5 FRs
    assert s["test_case_pass_ratio"] == 0.595
    assert s["avg_verification_iteration"] == 3.6     # FR-weighted: (2*2 + 4*2 + 6*1) / 5
    assert s["avg_test_iteration"] == 2.0             # 1 initial + 1 recovery pass
    assert s["avg_input_token"] == 4000.0 and s["avg_output_token"] == 800.0
    assert s["total_time"] == 142.3


def test_passver_unions_at_fr_level_without_double_counting():
    # FR 1.1 is both proved (via feature "1") AND passes pass@1 → counted once.
    ir = {"features": [
        {"id": "1", "functional_requirements": [{"id": "1.1"}]},
        {"id": "2", "functional_requirements": [{"id": "2.1"}]},
        {"id": "3", "functional_requirements": [{"id": "3.1"}]},
    ]}
    metrics = {
        "total_seconds": 1.0, "tokens": {"input": 1, "output": 1, "calls": 1},
        "proved_feature_ids": ["1"],
        "certification": {"pass_at_1_fr_ids": ["1.1", "2.1"], "n_total_tested_features": 2},
    }
    s = _compute_summary(metrics, ir)
    assert s["PassVer@1"] == round(2 / 3, 4)         # {1.1} ∪ {1.1,2.1} = {1.1,2.1} / 3 FRs, NOT 3/3


def test_summary_zeros_without_prove_or_certify():
    s = _compute_summary({"total_seconds": 5.0, "tokens": {"input": 10, "output": 2, "calls": 1}}, _ir())
    assert s["verification_pass_ratio"] == 0.0 and s["PassVer@1"] == 0.0
    assert s["avg_verification_iteration"] == 0.0 and s["avg_test_iteration"] == 0.0
