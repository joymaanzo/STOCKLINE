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