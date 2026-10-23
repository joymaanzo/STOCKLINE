import json
from pathlib import Path

from app.providers import DemoPriceProvider, PriceProvider


DATA_PATH = Path("data/demo_prices.json")


def test_demo_data_has_fifteen_tickers_and_sixty_points_each() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    assert data["demo_data"] is True
    assert len(data["tickers"]) == 15
    assert len(data["dates"]) == 60
    assert all(len(record["closes"]) == 60 for record in data["tickers"].values())


def test_demo_provider_implements_price_provider_and_returns_dated_history() -> None:
    provider = DemoPriceProvider()

    assert isinstance(provider, PriceProvider)
    history = provider.get_history("agl")

    assert history is not None
    assert len(history) == 60
    assert history[0] == {"date": "2025-01-01", "close": 100}
    assert history[-1] == {"date": "2025-03-01", "close": 159}


def test_demo_provider_returns_none_for_unknown_ticker() -> None:
    assert DemoPriceProvider().get_history("UNKNOWN") is None


def test_demo_provider_does_not_make_network_calls() -> None:
    assert DemoPriceProvider().get_history("SOL") is not None