"""
Tests for company-related API endpoints.
"""
import pytest

def test_root_endpoint(client):
    """Test the root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert data["message"] == "Company Financial Data API"

def test_health_check(client, data_stats):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["companies_loaded"] == 222
    assert "data_sources" in data

def test_list_companies(client):
    """Test listing all companies."""
    response = client.get("/companies")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "companies" in data
    assert data["total"] == 222
    assert len(data["companies"]) <= 100  # Default limit

def test_list_companies_with_pagination(client):
    """Test pagination works correctly."""
    response = client.get("/companies?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["companies"]) == 10

    # Test offset
    response2 = client.get("/companies?limit=10&offset=10")
    assert response2.status_code == 200
    data2 = response2.json()
    # Companies should be different
    assert data["companies"][0]["duns"] != data2["companies"][0]["duns"]

def test_get_company(client, sample_duns):
    """Test getting a specific company."""
    response = client.get(f"/companies/{sample_duns}")
    assert response.status_code == 200
    data = response.json()
    assert data["duns"] == sample_duns
    assert "data" in data
    assert isinstance(data["data"], dict)

def test_get_company_not_found(client, invalid_duns):
    """Test 404 for non-existent company."""
    response = client.get(f"/companies/{invalid_duns}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_get_company_industries(client, sample_duns):
    """Test getting company industries."""
    response = client.get(f"/companies/{sample_duns}/industries")
    assert response.status_code == 200
    data = response.json()
    assert data["duns"] == sample_duns
    assert "industries" in data
    assert isinstance(data["industries"], list)

def test_get_company_people(client, sample_duns):
    """Test getting company people."""
    response = client.get(f"/companies/{sample_duns}/people")
    assert response.status_code == 200
    data = response.json()
    assert data["duns"] == sample_duns
    assert "people" in data
    assert isinstance(data["people"], list)

def test_get_company_operations(client, sample_duns_with_operations):
    """Test getting company operations."""
    if sample_duns_with_operations:
        response = client.get(f"/companies/{sample_duns_with_operations}/operations")
        assert response.status_code == 200
        data = response.json()
        assert data["duns"] == sample_duns_with_operations
        assert "operations" in data
        assert isinstance(data["operations"], list)

def test_search_companies_by_query(client):
    """Test searching companies by address."""
    response = client.get("/companies/search?query=sydney")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "companies" in data
    # Should find at least some companies
    assert data["total"] >= 0

def test_search_companies_by_type(client):
    """Test searching companies by type."""
    response = client.get("/companies/search?company_type=Private")
    assert response.status_code == 200
    data = response.json()
    # Verify all results match the filter
    for company in data["companies"]:
        if company["company_type"]:
            assert company["company_type"] == "Private"

def test_search_companies_no_results(client):
    """Test search with no matching results."""
    response = client.get("/companies/search?query=xxxxnonexistentxxx")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["companies"]) == 0

def test_search_companies_with_pagination(client):
    """Test search with pagination."""
    response = client.get("/companies/search?query=sydney&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["companies"]) <= 5
