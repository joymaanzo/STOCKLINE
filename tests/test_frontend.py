from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_dashboard_page_is_served_with_demo_notice_and_controls() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Demo data, not live market prices" in response.text
    assert 'id="search"' in response.text
    assert 'id="loading"' in response.text
    assert 'id="error"' in response.text
    assert 'id="empty"' in response.text
    assert "/app.js" in response.text
    assert "/styles.css" in response.text


def test_dashboard_assets_and_client_behaviors_are_available() -> None:
    javascript = client.get("/app.js")
    styles = client.get("/styles.css")

    assert javascript.status_code == 200
    assert 'fetch("/api/stocks")' in javascript.text
    assert 'No matching shares.' in client.get("/").text or "No matching shares." in javascript.text
    assert 'href="/stock/${stock.ticker}"' in javascript.text
    assert 'method: watched ? "DELETE" : "POST"' in javascript.text
    assert styles.status_code == 200
    assert "@media" in styles.text


def test_stock_detail_page_serves_chart_indicators_and_explanation_markers() -> None:
    response = client.get("/stock/AGL")
    javascript = client.get("/stock.js")

    assert response.status_code == 200
    assert "60-day price history" in response.text
    assert javascript.status_code == 200
    assert "<svg" in javascript.text
    assert "5-day SMA" in response.text
    assert "20-day SMA" in response.text
    assert "20-day momentum" in response.text
    assert "Rule-based explanation" in response.text
    assert "Demo data, not live market prices" in response.text
    assert 'src="/stock.js"' in response.text


def test_stock_detail_assets_include_unknown_and_watchlist_behaviors() -> None:
    javascript = client.get("/stock.js")
    unknown = client.get("/stock/UNKNOWN")

    assert javascript.status_code == 200
    assert "Share not found" in unknown.text
    assert "<polyline" in javascript.text
    assert "/api/watchlist/" in javascript.text
    assert "source" in javascript.text