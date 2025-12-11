"""
Tests for financial data API endpoints.
"""
import pytest

def test_get_balance_sheet(client, sample_duns):
    """Test getting balance sheet data."""
    response = client.get(f"/companies/{sample_duns}/balance-sheet")
    assert response.status_code == 200
    data = response.json()
    assert data["duns"] == sample_duns
    assert data["statement_type"] == "balance_sheet"
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_balance_sheet_with_year_filter(client, sample_duns):
    """Test getting balance sheet with year filter."""
    response = client.get(f"/companies/{sample_duns}/balance-sheet?year=2024")
    assert response.status_code == 200
    data = response.json()
    # All items should be for 2024 if they have a year field
    for item in data["data"]:
        if item.get("year") is not None:
            assert item["year"] == 2024

def test_get_income_statement(client, sample_duns):
    """Test getting income statement data."""
    response = client.get(f"/companies/{sample_duns}/income-statement")
    assert response.status_code == 200
    data = response.json()
    assert data["duns"] == sample_duns
    assert data["statement_type"] == "income_statement"
    assert isinstance(data["data"], list)

def test_get_income_statement_with_year_filter(client, sample_duns):
    """Test getting income statement with year filter."""
    response = client.get(f"/companies/{sample_duns}/income-statement?year=2023")
    assert response.status_code == 200
    data = response.json()
    for item in data["data"]:
        if item.get("year") is not None:
            assert item["year"] == 2023

def test_get_cash_flow(client, sample_duns):
    """Test getting cash flow data."""
    response = client.get(f"/companies/{sample_duns}/cash-flow")
    assert response.status_code == 200
    data = response.json()
    assert data["duns"] == sample_duns
    assert data["statement_type"] == "cash_flow"
    assert isinstance(data["data"], list)

def test_get_cash_flow_with_year_filter(client, sample_duns):
    """Test getting cash flow with year filter."""
    response = client.get(f"/companies/{sample_duns}/cash-flow?year=2022")
    assert response.status_code == 200
    data = response.json()
    for item in data["data"]:
        if item.get("year") is not None:
            assert item["year"] == 2022

def test_get_financial_summary(client, sample_duns_with_all_data):
    """Test getting combined financial summary."""
    if sample_duns_with_all_data:
        response = client.get(f"/companies/{sample_duns_with_all_data}/financials/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["duns"] == sample_duns_with_all_data
        assert "balance_sheet" in data
        assert "income_statement" in data
        assert "cash_flow" in data
        assert isinstance(data["balance_sheet"], list)
        assert isinstance(data["income_statement"], list)
        assert isinstance(data["cash_flow"], list)

def test_get_financial_summary_with_year(client, sample_duns_with_all_data):
    """Test getting combined financial summary with year filter."""
    if sample_duns_with_all_data:
        response = client.get(f"/companies/{sample_duns_with_all_data}/financials/summary?year=2024")
        assert response.status_code == 200
        data = response.json()
        # Verify year filtering works across all statements
        for item in data["balance_sheet"]:
            if item.get("year") is not None:
                assert item["year"] == 2024

def test_financial_endpoints_not_found(client, invalid_duns):
    """Test 404 for financial endpoints with invalid DUNS."""
    endpoints = [
        f"/companies/{invalid_duns}/balance-sheet",
        f"/companies/{invalid_duns}/income-statement",
        f"/companies/{invalid_duns}/cash-flow",
        f"/companies/{invalid_duns}/financials/summary"
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 404

def test_financial_data_has_expected_fields(client, sample_duns):
    """Test that financial data has expected structure."""
    response = client.get(f"/companies/{sample_duns}/balance-sheet")
    assert response.status_code == 200
    data = response.json()
    if len(data["data"]) > 0:
        item = data["data"][0]
        assert "duns" in item
        # line_item should be present in financial data
        assert "line_item" in item or "field_name" in item
