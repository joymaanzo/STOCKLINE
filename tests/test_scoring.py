from app.indicators import momentum, moving_average_trend, simple_moving_average
from app.scoring import SCORING_CONFIG, score_prices


# Hand calc: SMA=(1+...+20)/20=10.5; momentum=(20-1)/1*100=1900%; 5-day SMA=18;
# trend=(18-10.5)/10.5*100=71.43%.
def test_twenty_day_indicators_use_known_fixture() -> None:
    prices = list(range(1, 21))

    assert simple_moving_average(prices) == 10.5
    assert momentum(prices) == 1900.0
    assert moving_average_trend(prices) == (18 - 10.5) / 10.5 * 100


# Hand calc: the increasing fixture reaches the 0-100 cap for each component;
# final score=0.40*100 + 0.40*100 + 0.20*100=100.0.
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


# Hand calc: 19 points cannot produce a 20-day SMA, momentum, or trend, so the
# acceptance-criteria result is "Insufficient data to score" with no number.
def test_fewer_than_twenty_points_has_no_numeric_score() -> None:
    result = score_prices(list(range(1, 20)))

    assert result == {"message": "Insufficient data to score"}
    assert "score" not in result


# Normalisation: component=max(0.0, min(100.0, 50.0 + percent_change * 5.0)).
# Flat: SMA=100, position=(100-100)/100*100=0%; components=(50, 50, 50);
# total=0.40*50 + 0.40*50 + 0.20*50=50.0 => Watch.
# Down: SMA=99.5, position=(90-99.5)/99.5*100=-9.55%; components=(0, 2.26, 42.46);
# total=0.40*0 + 0.40*2.26 + 0.20*42.46=9.4 => Weak.
# Up: SMA=100.5, position=(110-100.5)/100.5*100=9.45%; components=(100, 97.26, 57.46);
# total=0.40*100 + 0.40*97.26 + 0.20*57.46=90.4 => Strong.
def test_score_labels_cover_documented_thresholds() -> None:
    assert score_prices([100] * 20)["label"] == "Watch"
    assert score_prices([100] * 19 + [90])["label"] == "Weak indicators"
    assert score_prices([100] * 19 + [110])["label"] == "Strong indicators"