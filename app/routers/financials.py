"""
Financial data endpoints router.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import data_loader
from models import FinancialStatementResponse, CombinedFinancialResponse, ErrorResponse

router = APIRouter(prefix="/companies", tags=["financials"])

@router.get(
    "/{duns}/balance-sheet",
    response_model=FinancialStatementResponse,
    summary="Get balance sheet",
    description="Get balance sheet data for a specific company. Optionally filter by year.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_balance_sheet(
    duns: str,
    year: Optional[int] = Query(None, description="Filter by specific year (e.g., 2024)")
):
    """Get balance sheet data for a company."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    balance_sheet = data_loader.balance_sheet_data.get(duns, [])

    # Filter by year if specified
    if year is not None:
        balance_sheet = [item for item in balance_sheet if item.get('year') == year]

    return FinancialStatementResponse(
        duns=duns,
        statement_type="balance_sheet",
        data=balance_sheet
    )

@router.get(
    "/{duns}/income-statement",
    response_model=FinancialStatementResponse,
    summary="Get income statement",
    description="Get income statement data for a specific company. Optionally filter by year.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_income_statement(
    duns: str,
    year: Optional[int] = Query(None, description="Filter by specific year (e.g., 2024)")
):
    """Get income statement data for a company."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    income_statement = data_loader.income_statement_data.get(duns, [])

    # Filter by year if specified
    if year is not None:
        income_statement = [item for item in income_statement if item.get('year') == year]

    return FinancialStatementResponse(
        duns=duns,
        statement_type="income_statement",
        data=income_statement
    )

@router.get(
    "/{duns}/cash-flow",
    response_model=FinancialStatementResponse,
    summary="Get cash flow statement",
    description="Get cash flow statement data for a specific company. Optionally filter by year.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_cash_flow(
    duns: str,
    year: Optional[int] = Query(None, description="Filter by specific year (e.g., 2024)")
):
    """Get cash flow statement data for a company."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    cash_flow = data_loader.cash_flow_data.get(duns, [])

    # Filter by year if specified
    if year is not None:
        cash_flow = [item for item in cash_flow if item.get('year') == year]

    return FinancialStatementResponse(
        duns=duns,
        statement_type="cash_flow",
        data=cash_flow
    )

@router.get(
    "/{duns}/financials/summary",
    response_model=CombinedFinancialResponse,
    summary="Get all financial statements",
    description="Get balance sheet, income statement, and cash flow data in a single response. Optionally filter by year.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_financial_summary(
    duns: str,
    year: Optional[int] = Query(None, description="Filter by specific year (e.g., 2024)")
):
    """Get all financial statements for a company in one response."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    # Get all financial data
    balance_sheet = data_loader.balance_sheet_data.get(duns, [])
    income_statement = data_loader.income_statement_data.get(duns, [])
    cash_flow = data_loader.cash_flow_data.get(duns, [])

    # Filter by year if specified
    if year is not None:
        balance_sheet = [item for item in balance_sheet if item.get('year') == year]
        income_statement = [item for item in income_statement if item.get('year') == year]
        cash_flow = [item for item in cash_flow if item.get('year') == year]

    return CombinedFinancialResponse(
        duns=duns,
        balance_sheet=balance_sheet,
        income_statement=income_statement,
        cash_flow=cash_flow
    )
