from typing import Any

from pydantic import BaseModel, Field


class StockQuote(BaseModel):
    ticker: str
    name: str
    latest_close: float
    data_date: str
    daily_change: float
    daily_change_percent: float
    demo_data: bool


class StockAnalysis(BaseModel):
    ticker: str
    name: str
    latest_close: float
    data_date: str
    demo_data: bool
    score: float | None = None
    label: str | None = None
    breakdown: dict[str, Any] | None = None
    message: str | None = None
    explanation: str | None = None
    source: str | None = None


class WatchlistCreate(BaseModel):
    ticker: str = Field(min_length=1, max_length=10, pattern=r"^[A-Za-z0-9]+$")


class WatchlistItemResponse(BaseModel):
    ticker: str