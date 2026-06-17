"""Rough USD cost estimate from token counts.

Prices are USD per 1M tokens and may drift over time — update PRICING if they change.
"""

PRICING: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICING.get(model) or PRICING["gpt-4o-mini"]
    return input_tokens / 1_000_000 * rates["input"] + output_tokens / 1_000_000 * rates["output"]
