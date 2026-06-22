"""Cost estimation — single-model and accurate mixed-model (per-call) pricing."""

from src.cleanroom.utils.cost import estimate_cost, estimate_cost_by_model


def test_single_model_cost():
    # gpt-4o-mini: $0.15/1M in, $0.60/1M out
    assert estimate_cost("gpt-4o-mini", 1_000_000, 1_000_000) == 0.75


def test_dated_suffix_matches_by_prefix():
    assert estimate_cost("gpt-4.1-2025-04-14", 1_000_000, 0) == 2.00  # gpt-4.1 input rate


def test_mixed_model_cost_prices_each_model_separately():
    calls = [
        {"model": "gpt-4.1", "input_tokens": 100_000, "output_tokens": 20_000},
        {"model": "gpt-4o-mini", "input_tokens": 50_000, "output_tokens": 10_000},
    ]
    total, by_model = estimate_cost_by_model(calls)
    # gpt-4.1: 0.1*2.00 + 0.02*8.00 = 0.36 ; gpt-4o-mini: 0.05*0.15 + 0.01*0.60 = 0.0135
    assert by_model["gpt-4.1"]["cost_usd"] == 0.36
    assert by_model["gpt-4o-mini"]["cost_usd"] == 0.0135
    assert total == round(0.36 + 0.0135, 6)
    # and it must beat the naive 'everything at the last model' under-estimate
    assert total > estimate_cost("gpt-4o-mini", 150_000, 30_000)


def test_unknown_model_defaults_without_crashing():
    total, by_model = estimate_cost_by_model([{"model": "", "input_tokens": 1000, "output_tokens": 0}])
    assert total >= 0 and "gpt-4o-mini" in by_model
