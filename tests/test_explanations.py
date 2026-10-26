from app.explanations import DISCLAIMER, build_explanation
from app.scoring import score_prices


def test_explanation_quotes_breakdown_values_and_label() -> None:
    result = score_prices([100] * 19 + [90])

    explanation = build_explanation(result)

    assert explanation == (
        "Momentum: -10.00%; position vs 20-day SMA: -9.55%; "
        "5-day vs 20-day SMA trend: -1.51%; label: Weak indicators. "
        f"{DISCLAIMER}"
    )


def test_explanation_is_deterministic_for_fixed_fixture() -> None:
    result = score_prices([100] * 19 + [110])

    assert build_explanation(result) == build_explanation(result)


def test_insufficient_data_has_no_explanation_with_numbers() -> None:
    result = score_prices([100] * 19)

    assert result == {"message": "Insufficient data to score"}
    assert build_explanation(result) is None