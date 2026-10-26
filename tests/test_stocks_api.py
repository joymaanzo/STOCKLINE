from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_stock_list_includes_quote_fields_and_demo_metadata() -> None:
    response = client.get("/api/stocks")

    assert response.status_code == 200
    stocks = response.json()
    assert len(stocks) == 15
    assert stocks[0]["ticker"] == "AGL"
    assert stocks[0]["latest_close"] == 159.0
    assert stocks[0]["data_date"] == "2025-03-01"
    assert stocks[0]["daily_change"] == 1.0
    assert stocks[0]["daily_change_percent"] == 0.63
    assert stocks[0]["demo_data"] is True


def test_search_matches_ticker_and_name_case_insensitively() -> None:
    ticker_match = client.get("/api/stocks/search", params={"q": "agl"})
    name_match = client.get("/api/stocks/search", params={"q": "sHoPrItE"})
    no_match = client.get("/api/stocks/search", params={"q": "not a stock"})

    assert ticker_match.json()[0]["ticker"] == "AGL"
    assert name_match.json()[0]["ticker"] == "SHP"
    assert no_match.json() == []


def test_unknown_stock_returns_not_found() -> None:
    response = client.get("/api/stocks/UNKNOWN")

    assert response.status_code == 404


def test_stock_analysis_returns_score_label_breakdown_and_metadata() -> None:
    response = client.get("/api/stocks/AGL/analysis")

    assert response.status_code == 200
    analysis = response.json()
    assert analysis["score"] == 87.73
    assert analysis["label"] == "Strong indicators"
    assert "momentum" in analysis["breakdown"]
    assert analysis["data_date"] == "2025-03-01"
    assert analysis["demo_data"] is True
    assert analysis["message"] is None
    assert analysis["sma5"] == 157.0
    assert analysis["sma20"] == 149.5


def test_invalid_stock_inputs_return_unprocessable_entity() -> None:
    missing_query = client.get("/api/stocks/search")
    invalid_ticker = client.get("/api/stocks/!!!")

    assert missing_query.status_code == 422
    assert invalid_ticker.status_code == 422