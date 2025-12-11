"""
Pytest configuration and fixtures for testing the API.
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
import data_loader

@pytest.fixture(scope="session", autouse=True)
def load_data():
    """Load data once for all tests."""
    if not data_loader.company_data:  # Only load if not already loaded
        data_loader.load_all_data()
    yield
    # Cleanup if needed

@pytest.fixture(scope="module")
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="session")
def sample_duns():
    """Get a valid DUNS number from loaded data."""
    duns_list = data_loader.get_all_duns_numbers()
    return duns_list[0] if duns_list else None

@pytest.fixture(scope="session")
def sample_duns_with_all_data():
    """Get a DUNS number that has all data types."""
    for duns in data_loader.get_all_duns_numbers():
        if (duns in data_loader.balance_sheet_data and
            duns in data_loader.income_statement_data and
            duns in data_loader.cash_flow_data and
            duns in data_loader.industries_data and
            duns in data_loader.people_data):
            return duns
    return None

@pytest.fixture(scope="session")
def sample_duns_with_operations():
    """Get a DUNS number that has operations data."""
    for duns in data_loader.operations_data.keys():
        return duns
    return None

@pytest.fixture(scope="session")
def invalid_duns():
    """Return an invalid DUNS number."""
    return "999999999"

@pytest.fixture(scope="session")
def data_stats():
    """Return statistics about loaded data for validation."""
    return {
        "total_companies": len(data_loader.company_data),
        "companies_with_balance_sheet": len(data_loader.balance_sheet_data),
        "companies_with_income": len(data_loader.income_statement_data),
        "companies_with_cashflow": len(data_loader.cash_flow_data),
        "companies_with_industries": len(data_loader.industries_data),
        "companies_with_people": len(data_loader.people_data),
        "companies_with_operations": len(data_loader.operations_data),
    }
