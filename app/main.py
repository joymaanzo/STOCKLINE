from fastapi import FastAPI

from app.routes_stocks import router as stocks_router
from app.routes_watchlist import router as watchlist_router

app = FastAPI()
app.include_router(stocks_router)
app.include_router(watchlist_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}