import os

import pytest
from fastapi.testclient import TestClient


DATABASE_URL = os.getenv("DATABASE_URL", "")
POSTGRES_SKIP_REASON = "DATABASE_URL is not set to a Postgres database"
pytestmark = pytest.mark.skipif(
    not DATABASE_URL.startswith(("postgresql://", "postgresql+")),
    reason=POSTGRES_SKIP_REASON,
)

from app.main import app


def test_postgres_watchlist_round_trip() -> None:
    client = TestClient(app)
    client.delete("/api/watchlist/VOD")

    added = client.post("/api/watchlist", json={"ticker": "VOD"})
    assert added.status_code == 201

    listed = client.get("/api/watchlist")
    assert listed.status_code == 200
    assert {item["ticker"] for item in listed.json()} >= {"VOD"}

    removed = client.delete("/api/watchlist/VOD")
    assert removed.status_code == 204