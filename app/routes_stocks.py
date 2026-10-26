from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from app.providers import DemoPriceProvider
from app.explanations import build_explanation
from app.schemas import StockAnalysis, StockQuote
from app.scoring import score_prices


router = APIRouter(prefix="/api/stocks", tags=["stocks"])
provider = DemoPriceProvider()
STOCK_NAMES = {
    "AGL": "Anglo American",
    "BHP": "BHP Group",
    "CML": "Coronation Fund Managers",
    "FSR": "FirstRand",
    "GLN": "Glencore",
    "MTN": "MTN Group",
    "NPN": "Naspers",
    "REM": "Remgro",
    "SBK": "Standard Bank",
    "S32": "South32",
    "SHP": "Shoprite",
    "SOL": "Sasol",
    "TKG": "Telkom",
    "VOD": "Vodacom",
    "WHL": "Woolworths Holdings",
}


def _quote(ticker: str) -> StockQuote:
    normalized_ticker = ticker.upper()
    history = provider.get_history(normalized_ticker)
    if history is None:
        raise HTTPException(status_code=404, detail="Unknown ticker")

    latest = history[-1]
    previous = history[-2]
    latest_close = float(latest["close"])
    previous_close = float(previous["close"])
    daily_change = latest_close - previous_close
    daily_change_percent = daily_change / previous_close * 100 if previous_close else 0
    return StockQuote(
        ticker=normalized_ticker,
        name=STOCK_NAMES[normalized_ticker],
        latest_close=latest_close,
        data_date=str(latest["date"]),
        daily_change=round(daily_change, 2),
        daily_change_percent=round(daily_change_percent, 2),
        demo_data=True,
    )


@router.get("", response_model=list[StockQuote])
def list_stocks() -> list[StockQuote]:
    return [_quote(ticker) for ticker in STOCK_NAMES]


@router.get("/search", response_model=list[StockQuote])
def search_stocks(q: Annotated[str, Query()]) -> list[StockQuote]:
    query = q.casefold()
    return [
        _quote(ticker)
        for ticker, name in STOCK_NAMES.items()
        if query in ticker.casefold() or query in name.casefold()
    ]


@router.get("/{ticker}", response_model=StockQuote)
def get_stock(
    ticker: Annotated[str, Path(pattern=r"^[A-Za-z0-9]+$")],
) -> StockQuote:
    return _quote(ticker)


@router.get("/{ticker}/analysis", response_model=StockAnalysis)
def analyze_stock(
    ticker: Annotated[str, Path(pattern=r"^[A-Za-z0-9]+$")],
) -> StockAnalysis:
    quote = _quote(ticker)
    history = provider.get_history(quote.ticker)
    assert history is not None
    result = score_prices([float(point["close"]) for point in history])
    explanation = build_explanation(result)
    return StockAnalysis(
        **quote.model_dump(),
        score=result.get("score"),
        label=result.get("label"),
        breakdown=result.get("breakdown"),
        message=result.get("message"),
        explanation=explanation,
        source="rule-based" if explanation is not None else None,
    )