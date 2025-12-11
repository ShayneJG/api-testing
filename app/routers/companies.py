"""
Company endpoints router.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import data_loader
from models import (
    CompanyInfoResponse,
    CompanyListResponse,
    CompanyListItem,
    IndustriesResponse,
    IndustryListResponse,
    IndustryInfo,
    PeopleResponse,
    OperationsResponse,
    ErrorResponse
)

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get(
    "",
    response_model=CompanyListResponse,
    summary="List all companies",
    description="Get a list of all companies with basic information. Supports pagination."
)
def list_companies(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """List all companies with pagination."""
    all_duns = data_loader.get_all_duns_numbers()

    # Apply pagination
    paginated_duns = all_duns[offset:offset + limit]

    companies = []
    for duns in paginated_duns:
        company_info = data_loader.company_data.get(duns, {})
        companies.append(CompanyListItem(
            duns=duns,
            address=company_info.get("Physical Address"),
            telephone=company_info.get("Telephone Number"),
            company_type=company_info.get("Company Type")
        ))

    return CompanyListResponse(
        total=len(all_duns),
        companies=companies
    )

@router.get(
    "/search",
    response_model=CompanyListResponse,
    summary="Search companies",
    description="Search companies by query string (matches address), company type, or industry code."
)
def search_companies(
    query: Optional[str] = Query(None, description="Search in company address"),
    company_type: Optional[str] = Query(None, description="Filter by company type (e.g., 'Private', 'Publicly Unlisted')"),
    industry_code: Optional[str] = Query(None, description="Filter by industry code (e.g., '7389')"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """Search companies by various criteria."""
    all_duns = data_loader.get_all_duns_numbers()
    filtered_companies = []

    for duns in all_duns:
        company_info = data_loader.company_data.get(duns, {})

        # Apply filters
        if query:
            address = company_info.get("Physical Address", "").lower()
            if query.lower() not in address:
                continue

        if company_type:
            if company_info.get("Company Type") != company_type:
                continue

        if industry_code:
            industries = data_loader.industries_data.get(duns, [])
            industry_codes = [ind.get("industry_code") for ind in industries]
            if industry_code not in industry_codes:
                continue

        # Company matches all filters
        filtered_companies.append(CompanyListItem(
            duns=duns,
            address=company_info.get("Physical Address"),
            telephone=company_info.get("Telephone Number"),
            company_type=company_info.get("Company Type")
        ))

    # Apply pagination
    total = len(filtered_companies)
    paginated = filtered_companies[offset:offset + limit]

    return CompanyListResponse(
        total=total,
        companies=paginated
    )

@router.get(
    "/{duns}",
    response_model=CompanyInfoResponse,
    summary="Get company details",
    description="Get detailed information for a specific company by DUNS number.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_company(duns: str):
    """Get company details by DUNS number."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    return CompanyInfoResponse(
        duns=duns,
        data=data_loader.company_data[duns]
    )

@router.get(
    "/{duns}/industries",
    response_model=IndustriesResponse,
    summary="Get company industries",
    description="Get industry classifications for a specific company.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_company_industries(duns: str):
    """Get industry classifications for a company."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    industries = data_loader.industries_data.get(duns, [])

    return IndustriesResponse(
        duns=duns,
        industries=industries
    )

@router.get(
    "/{duns}/people",
    response_model=PeopleResponse,
    summary="Get company personnel",
    description="Get list of people/personnel for a specific company.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_company_people(duns: str):
    """Get company personnel."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    people = data_loader.people_data.get(duns, [])

    return PeopleResponse(
        duns=duns,
        people=people
    )

@router.get(
    "/{duns}/operations",
    response_model=OperationsResponse,
    summary="Get company operations",
    description="Get operations descriptions for a specific company.",
    responses={404: {"model": ErrorResponse, "description": "Company not found"}}
)
def get_company_operations(duns: str):
    """Get company operations descriptions."""
    if duns not in data_loader.company_data:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    operations = data_loader.operations_data.get(duns, [])

    return OperationsResponse(
        duns=duns,
        operations=operations
    )
