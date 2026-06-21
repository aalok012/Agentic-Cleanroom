"""Rough USD cost estimate from token counts.

Prices are USD per 1M tokens and may drift over time — update PRICING if they change.
"""

PRICING: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
}


def _rates(model: str) -> dict[str, float]:
    """Prices for a model, matching the longest known prefix (handles dated suffixes)."""
    if model in PRICING:
        return PRICING[model]
    for name in sorted(PRICING, key=len, reverse=True):
        if model.startswith(name):
            return PRICING[name]
    return PRICING["gpt-4o-mini"]


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    rates = _rates(model)
    return input_tokens / 1_000_000 * rates["input"] + output_tokens / 1_000_000 * rates["output"]
