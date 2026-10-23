import json
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class PriceProvider(Protocol):
    def get_history(self, ticker: str) -> list[dict[str, str | int]] | None:
        ...


class DemoPriceProvider:
    def __init__(self, path: Path | None = None) -> None:
        data_path = path or Path(__file__).parent.parent / "data" / "demo_prices.json"
        with data_path.open(encoding="utf-8") as data_file:
            self._data = json.load(data_file)

    def get_history(self, ticker: str) -> list[dict[str, str | int]] | None:
        record = self._data["tickers"].get(ticker.upper())
        if record is None:
            return None
        return [
            {"date": date, "close": close}
            for date, close in zip(self._data["dates"], record["closes"])
        ]