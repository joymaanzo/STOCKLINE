from collections.abc import Sequence

from app.indicators import moving_average_trend, momentum, simple_moving_average


SCORING_CONFIG = {
    "weights": {
        "momentum": 0.40,
        "position_vs_sma": 0.40,
        "sma_trend": 0.20,
    },
    "labels": {
        "strong": (70, "Strong indicators"),
        "watch": (40, "Watch"),
        "weak": (0, "Weak indicators"),
    },
    "normalization_scale": 5.0,
}


def _component_score(percent_change: float) -> float:
    scale = SCORING_CONFIG["normalization_scale"]
    return max(0.0, min(100.0, 50.0 + percent_change * scale))


def _label_for_score(score: float) -> str:
    if score >= SCORING_CONFIG["labels"]["strong"][0]:
        return SCORING_CONFIG["labels"]["strong"][1]
    if score >= SCORING_CONFIG["labels"]["watch"][0]:
        return SCORING_CONFIG["labels"]["watch"][1]
    return SCORING_CONFIG["labels"]["weak"][1]


def score_prices(prices: Sequence[float]) -> dict[str, object]:
    if len(prices) < 20:
        return {"message": "Insufficient data to score"}

    moving_average = simple_moving_average(prices)
    price_momentum = momentum(prices)
    trend = moving_average_trend(prices)
    if moving_average in (None, 0) or price_momentum is None or trend is None:
        return {"message": "Insufficient data to score"}

    position = (prices[-1] - moving_average) / moving_average * 100
    components = {
        "momentum": _component_score(price_momentum),
        "position_vs_sma": _component_score(position),
        "sma_trend": _component_score(trend),
    }
    weights = SCORING_CONFIG["weights"]
    score = sum(components[name] * weights[name] for name in components)
    rounded_score = round(score, 2)
    return {
        "score": rounded_score,
        "label": _label_for_score(rounded_score),
        "breakdown": {
            "momentum": price_momentum,
            "position_vs_sma": position,
            "sma_trend": trend,
            "components": components,
            "weights": weights,
        },
    }