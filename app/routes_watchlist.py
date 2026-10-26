from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import WatchlistItem
from app.providers import DemoPriceProvider
from app.schemas import WatchlistCreate, WatchlistItemResponse


init_db()
router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])
provider = DemoPriceProvider()


@router.get("", response_model=list[WatchlistItemResponse])
def list_watchlist(db: Session = Depends(get_db)) -> list[WatchlistItem]:
    return list(db.query(WatchlistItem).order_by(WatchlistItem.ticker).all())


@router.post("", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
def add_watchlist_item(
    item: WatchlistCreate,
    db: Session = Depends(get_db),
) -> WatchlistItem:
    ticker = item.ticker.upper()
    if provider.get_history(ticker) is None:
        raise HTTPException(status_code=404, detail="Unknown ticker")
    if db.query(WatchlistItem).filter_by(ticker=ticker).first() is not None:
        raise HTTPException(status_code=409, detail="Ticker already in watchlist")

    watchlist_item = WatchlistItem(ticker=ticker)
    db.add(watchlist_item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ticker already in watchlist") from None
    db.refresh(watchlist_item)
    return watchlist_item


@router.delete("/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
def remove_watchlist_item(
    ticker: Annotated[str, Path(pattern=r"^[A-Za-z0-9]+$")],
    db: Session = Depends(get_db),
) -> None:
    watchlist_item = db.query(WatchlistItem).filter_by(ticker=ticker.upper()).first()
    if watchlist_item is None:
        raise HTTPException(status_code=404, detail="Ticker not in watchlist")
    db.delete(watchlist_item)
    db.commit()