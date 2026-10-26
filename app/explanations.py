from collections.abc import Mapping


DISCLAIMER = "This is a heuristic summary of past prices, not a guarantee of returns or advice."


def build_explanation(result: Mapping[str, object]) -> str | None:
    if result.get("message") or result.get("score") is None:
        return None

    breakdown = result["breakdown"]
    if not isinstance(breakdown, Mapping):
        return None
    momentum = breakdown["momentum"]
    position = breakdown["position_vs_sma"]
    trend = breakdown["sma_trend"]
    label = result["label"]
    return (
        f"Momentum: {momentum:.2f}%; position vs 20-day SMA: {position:.2f}%; "
        f"5-day vs 20-day SMA trend: {trend:.2f}%; label: {label}. {DISCLAIMER}"
    )