import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, DEFAULT_DATABASE_URL, database_url_from_env
from app.main import app
from app.models import WatchlistItem
from app.routes_watchlist import get_db


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    database_path = tmp_path / "watchlist.db"
    engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db() -> Iterator[Session]:
        with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


def test_database_url_uses_environment_and_default(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert database_url_from_env() == DEFAULT_DATABASE_URL
    monkeypatch.setenv("DATABASE_URL", "sqlite:///custom.db")
    assert database_url_from_env() == "sqlite:///custom.db"


def test_watchlist_crud_and_validation(client: TestClient) -> None:
    assert client.get("/api/watchlist").json() == []

    added = client.post("/api/watchlist", json={"ticker": "agl"})
    assert added.status_code == 201
    assert added.json() == {"ticker": "AGL"}
    assert client.get("/api/watchlist").json() == [{"ticker": "AGL"}]

    duplicate = client.post("/api/watchlist", json={"ticker": "AGL"})
    unknown = client.post("/api/watchlist", json={"ticker": "UNKNOWN"})
    invalid = client.post("/api/watchlist", json={})
    assert duplicate.status_code == 409
    assert unknown.status_code == 404
    assert invalid.status_code == 422

    removed = client.delete("/api/watchlist/agl")
    missing = client.delete("/api/watchlist/AGL")
    assert removed.status_code == 204
    assert missing.status_code == 404
    assert client.get("/api/watchlist").json() == []


def test_file_database_persists_after_reopening(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'persistent.db'}"
    first_engine = create_engine(database_url)
    Base.metadata.create_all(bind=first_engine)
    FirstSession = sessionmaker(bind=first_engine)
    with FirstSession() as session:
        session.add(WatchlistItem(ticker="BHP"))
        session.commit()
    first_engine.dispose()

    reopened_engine = create_engine(database_url)
    ReopenedSession = sessionmaker(bind=reopened_engine)
    with ReopenedSession() as session:
        saved = session.query(WatchlistItem).one()
        assert saved.ticker == "BHP"
    reopened_engine.dispose()