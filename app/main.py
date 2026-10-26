import json
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Path as FastAPIPath
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routes_stocks import router as stocks_router
from app.routes_watchlist import router as watchlist_router
from app.providers import DemoPriceProvider

app = FastAPI()
app.include_router(stocks_router)
app.include_router(watchlist_router)
STATIC_DIR = Path(__file__).parent / "static"


@app.get("/stock/{ticker}", response_class=HTMLResponse)
def stock_page(
    ticker: Annotated[str, FastAPIPath(pattern=r"^[A-Za-z0-9]+$")],
) -> HTMLResponse:
    page = (STATIC_DIR / "stock.html").read_text(encoding="utf-8")
    history = DemoPriceProvider().get_history(ticker)
    history_json = json.dumps(history) if history is not None else "null"
    page = page.replace("__TICKER__", ticker.upper()).replace("__HISTORY__", history_json)
    return HTMLResponse(page)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.mount(
    "/",
    StaticFiles(directory=STATIC_DIR, html=True),
    name="static",
)