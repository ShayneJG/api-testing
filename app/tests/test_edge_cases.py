"""
Tests for edge cases and error handling.
"""
import pytest

def test_list_industries(client):
    """Test listing all industries."""
    response = client.get("/industries")
    assert response.status_code == 200
    data = response.json()
    assert "total_industries" in data
    assert "industries" in data
    assert data["total_industries"] > 0
    assert isinstance(data["industries"], list)

def test_industries_sorted_by_count(client):
    """Test that industries are sorted by company count."""
    response = client.get("/industries")
    assert response.status_code == 200
    data = response.json()
    if len(data["industries"]) > 1:
        # Check that counts are in descending order
        counts = [ind["company_count"] for ind in data["industries"]]
        assert counts == sorted(counts, reverse=True)

def test_industries_no_nan_values(client):
    """Test that industries endpoint handles NaN values."""
    response = client.get("/industries")
    assert response.status_code == 200
    data = response.json()
    # All industry codes should be valid strings
    for industry in data["industries"]:
        assert industry["industry_code"] is not None
        assert industry["industry_code"] != "nan"
        assert industry["industry_code"] != ""

def test_pagination_boundary_conditions(client):
    """Test pagination edge cases."""
    # Offset beyond total
    response = client.get("/companies?limit=10&offset=1000")
    assert response.status_code == 200
    data = response.json()
    assert len(data["companies"]) == 0

    # Very large limit (should be capped at 1000)
    response = client.get("/companies?limit=2000")
    assert response.status_code == 422  # Validation error

def test_invalid_year_parameter(client, sample_duns):
    """Test invalid year parameter handling."""
    # String year should cause validation error
    response = client.get(f"/companies/{sample_duns}/balance-sheet?year=invalid")
    assert response.status_code == 422

def test_negative_pagination_values(client):
    """Test negative pagination values."""
    # Negative offset should cause validation error
    response = client.get("/companies?offset=-1")
    assert response.status_code == 422

    # Negative limit should cause validation error
    response = client.get("/companies?limit=-1")
    assert response.status_code == 422

def test_empty_search_query(client):
    """Test search with empty query."""
    response = client.get("/companies/search?query=")
    assert response.status_code == 200
    # Should return all companies when query is empty

def test_special_characters_in_search(client):
    """Test search with special characters."""
    response = client.get("/companies/search?query=%40%23%24")  # @#$
    assert response.status_code == 200
    # Should handle gracefully even if no results

def test_company_with_missing_optional_data(client, sample_duns):
    """Test handling of companies with missing optional data."""
    response = client.get(f"/companies/{sample_duns}")
    assert response.status_code == 200
    # Should succeed even if some fields are missing

def test_financial_data_with_no_year(client, sample_duns):
    """Test getting all financial data without year filter."""
    response = client.get(f"/companies/{sample_duns}/balance-sheet")
    assert response.status_code == 200
    data = response.json()
    # Should return all years

def test_year_with_no_data(client, sample_duns):
    """Test filtering by year with no data."""
    response = client.get(f"/companies/{sample_duns}/balance-sheet?year=1900")
    assert response.status_code == 200
    data = response.json()
    # Should return empty list, not error
    assert isinstance(data["data"], list)

def test_concurrent_requests(client, sample_duns):
    """Test that API handles concurrent requests."""
    import concurrent.futures

    def make_request():
        return client.get(f"/companies/{sample_duns}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [f.result() for f in futures]

    # All requests should succeed
    assert all(r.status_code == 200 for r in results)

def test_api_documentation_accessible(client):
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/redoc")
    assert response.status_code == 200

def test_openapi_schema_valid(client):
    """Test that OpenAPI schema is valid."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema

def test_case_insensitive_search(client):
    """Test that search is case-insensitive."""
    response1 = client.get("/companies/search?query=sydney")
    response2 = client.get("/companies/search?query=SYDNEY")
    response3 = client.get("/companies/search?query=Sydney")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200

    # Should return same number of results
    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()
    assert data1["total"] == data2["total"] == data3["total"]

def test_industries_pagination(client):
    """Test industries endpoint with pagination."""
    response = client.get("/industries?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["industries"]) <= 5

def test_multiple_search_filters(client):
    """Test search with multiple filters combined."""
    response = client.get("/companies/search?query=sydney&company_type=Private")
    assert response.status_code == 200
    data = response.json()
    # Results should match both filters
    for company in data["companies"]:
        if company["address"]:
            assert "sydney" in company["address"].lower()
        if company["company_type"]:
            assert company["company_type"] == "Private"
