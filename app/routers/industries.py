"""
Industries endpoints router.
"""
from fastapi import APIRouter, Query
from typing import Dict
import data_loader
from models import IndustryListResponse, IndustryInfo

router = APIRouter(prefix="/industries", tags=["industries"])

@router.get(
    "",
    response_model=IndustryListResponse,
    summary="List all industries",
    description="Get a list of all unique industries with company counts."
)
def list_industries(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """List all industries with company counts."""
    # Aggregate industries across all companies
    industry_map: Dict[str, Dict] = {}

    for duns, industries_list in data_loader.industries_data.items():
        for industry_item in industries_list:
            code = industry_item.get("industry_code", "")
            description = industry_item.get("industry_description", "")

            # Convert code to string and skip NaN or empty values
            code = str(code) if code is not None and str(code) != "nan" else ""
            description = str(description) if description is not None and str(description) != "nan" else ""

            if code and code != "":  # Skip empty codes
                if code not in industry_map:
                    industry_map[code] = {
                        "industry_code": code,
                        "industry_description": description,
                        "company_count": 0
                    }
                industry_map[code]["company_count"] += 1

    # Convert to list and sort by company count (descending)
    industries_list = [
        IndustryInfo(**ind) for ind in industry_map.values()
    ]
    industries_list.sort(key=lambda x: x.company_count, reverse=True)

    # Apply pagination
    total = len(industries_list)
    paginated = industries_list[offset:offset + limit]

    return IndustryListResponse(
        total_industries=total,
        industries=paginated
    )
