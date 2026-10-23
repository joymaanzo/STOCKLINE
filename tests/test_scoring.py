from app.indicators import momentum, moving_average_trend, simple_moving_average
from app.scoring import SCORING_CONFIG, score_prices


def test_twenty_day_indicators_use_known_fixture() -> None:
    prices = list(range(1, 21))

    assert simple_moving_average(prices) == 10.5
    assert momentum(prices) == 1900.0
    assert moving_average_trend(prices) == (18 - 10.5) / 10.5 * 100


def test_score_uses_configured_weights_and_is_deterministic() -> None:
    prices = list(range(1, 21))

    first = score_prices(prices)
    second = score_prices(prices)

    assert first == second
    assert first["score"] == 100.0
    assert first["label"] == "Strong indicators"
    assert SCORING_CONFIG["weights"] == {
        "momentum": 0.40,
        "position_vs_sma": 0.40,
        "sma_trend": 0.20,
    }


def test_fewer_than_twenty_points_has_no_numeric_score() -> None:
    result = score_prices(list(range(1, 20)))

    assert result == {"message": "Insufficient data to score"}
    assert "score" not in result


def test_score_labels_cover_documented_thresholds() -> None:
    assert score_prices([100] * 20)["label"] == "Watch"
    assert score_prices([100] * 19 + [90])["label"] == "Weak indicators"
    assert score_prices([100] * 19 + [110])["label"] == "Strong indicators"