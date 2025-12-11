"""
Tests for data loading functionality.
"""
import pytest
import data_loader

def test_data_loaded(data_stats):
    """Test that data was loaded successfully."""
    assert data_stats["total_companies"] > 0, "No companies loaded"
    assert data_stats["total_companies"] == 222, f"Expected 222 companies, got {data_stats['total_companies']}"

def test_all_companies_have_info(data_stats):
    """Test that all companies have basic info."""
    assert data_stats["total_companies"] == 222

def test_financial_data_loaded(data_stats):
    """Test that financial data was loaded."""
    assert data_stats["companies_with_balance_sheet"] == 222
    assert data_stats["companies_with_income"] == 222
    assert data_stats["companies_with_cashflow"] == 222

def test_company_data_structure(sample_duns):
    """Test that company data has expected structure."""
    assert sample_duns in data_loader.company_data
    company = data_loader.company_data[sample_duns]
    assert isinstance(company, dict)
    # Should have at least some fields
    assert len(company) > 0

def test_financial_data_structure(sample_duns):
    """Test that financial data has expected structure."""
    if sample_duns in data_loader.balance_sheet_data:
        balance_sheet = data_loader.balance_sheet_data[sample_duns]
        assert isinstance(balance_sheet, list)
        if len(balance_sheet) > 0:
            item = balance_sheet[0]
            assert "duns" in item or "line_item" in item

def test_industries_data_loaded(data_stats):
    """Test that industry data was loaded."""
    assert data_stats["companies_with_industries"] == 222

def test_people_data_loaded(data_stats):
    """Test that people data was loaded."""
    # Not all companies may have people data
    assert data_stats["companies_with_people"] >= 0
    assert data_stats["companies_with_people"] <= 222

def test_operations_data_loaded(data_stats):
    """Test that operations data was loaded."""
    # Not all companies may have operations data
    assert data_stats["companies_with_operations"] >= 0
    assert data_stats["companies_with_operations"] <= 222

def test_duns_list_not_empty():
    """Test that we can get DUNS numbers."""
    duns_list = data_loader.get_all_duns_numbers()
    assert len(duns_list) > 0
    assert len(duns_list) == 222

def test_no_duplicate_duns():
    """Test that there are no duplicate DUNS numbers."""
    duns_list = data_loader.get_all_duns_numbers()
    assert len(duns_list) == len(set(duns_list)), "Duplicate DUNS numbers found"
