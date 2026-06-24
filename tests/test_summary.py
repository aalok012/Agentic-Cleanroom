"""The headline run-metrics summary (verification/test ratios, iterations, PassVer@1)."""

from run_pipeline import _compute_summary


def _metrics():
    return {
        "total_seconds": 142.3,
        "tokens": {"input": 120000, "output": 24000, "calls": 30},
        "proved_feature_ids": [str(i) for i in range(8)],     # 8 proved
        "dafny": {"n_features": 10, "n_verified": 8,
                  "features": [{"rounds": r} for r in [1, 2, 3, 4, 2, 3, 1, 5, 6, 2]]},
        "certification": {"aggregate_case_pass_rate": 0.595,
                          "pass_at_1_feature_ids": ["8"],     # 1 tested feature passes pass@1
                          "n_total_tested_features": 2},
        "recovery": {"loops_run": 1},
    }


def test_summary_metric_definitions():
    s = _compute_summary(_metrics(), {"features": [{"id": str(i)} for i in range(10)]})
    assert s["verification_pass_ratio"] == 0.8          # 8 proved / 10 attempted
    assert s["test_case_pass_ratio"] == 0.595
    assert s["PassVer@1"] == 0.9                         # |{0..7} ∪ {8}| / 10 = 9/10
    assert s["avg_verification_iteration"] == 2.9        # mean Dafny rounds
    assert s["avg_test_iteration"] == 2.0                # 1 initial + 1 recovery pass
    assert s["avg_input_token"] == 4000.0 and s["avg_output_token"] == 800.0
    assert s["total_time"] == 142.3


def test_passver_unions_proved_and_pass_at_1_without_double_counting():
    # A feature both proved AND passing pass@1 (id "b") must count ONCE.
    metrics = {
        "total_seconds": 1.0, "tokens": {"input": 1, "output": 1, "calls": 1},
        "proved_feature_ids": ["a", "b"],
        "certification": {"pass_at_1_feature_ids": ["b", "c"], "n_total_tested_features": 2},
    }
    s = _compute_summary(metrics, {"features": [{"id": x} for x in ("a", "b", "c")]})
    assert s["PassVer@1"] == 1.0                         # |{a,b} ∪ {b,c}| / 3 = 3/3, NOT 4/3


def test_summary_zeros_without_prove_or_certify():
    s = _compute_summary({"total_seconds": 5.0, "tokens": {"input": 10, "output": 2, "calls": 1}},
                         {"features": [{"id": "1"}]})
    assert s["verification_pass_ratio"] == 0.0
    assert s["test_case_pass_ratio"] == 0.0
    assert s["PassVer@1"] == 0.0
    assert s["avg_verification_iteration"] == 0.0 and s["avg_test_iteration"] == 0.0
