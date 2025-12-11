"""
Pydantic models for API request/response validation.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# Company Info Models
class CompanyInfoResponse(BaseModel):
    """Response model for company information."""
    duns: str
    data: Dict[str, Any] = Field(
        description="Company information as field/value pairs"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "duns": "740039581",
                "data": {
                    "Physical Address": "123 Main St, Sydney, NSW, Australia",
                    "Telephone Number": "02 12345678",
                    "Company Type": "Publicly Unlisted"
                }
            }
        }

class CompanyListItem(BaseModel):
    """Summary info for company in list view."""
    duns: str
    address: Optional[str] = None
    telephone: Optional[str] = None
    company_type: Optional[str] = None

class CompanyListResponse(BaseModel):
    """Response for list of companies."""
    total: int
    companies: List[CompanyListItem]

# Financial Statement Models
class FinancialLineItem(BaseModel):
    """A single financial statement line item."""
    duns: str
    line_item: str
    year: Optional[int] = None
    value: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "duns": "740039581",
                "line_item": "Total Assets ($000s)",
                "year": 2024,
                "value": "$56,136"
            }
        }

class FinancialStatementResponse(BaseModel):
    """Response for financial statement data."""
    duns: str
    statement_type: str
    data: List[Dict[str, Any]]

# Industry Models
class IndustryItem(BaseModel):
    """Industry classification item."""
    duns: str
    industry_code: Optional[str] = None
    industry_description: Optional[str] = None
    is_primary: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "duns": "740039581",
                "industry_code": "7389",
                "industry_description": "Business Services, Not Elsewhere Classified",
                "is_primary": 1
            }
        }

class IndustriesResponse(BaseModel):
    """Response for industry classifications."""
    duns: str
    industries: List[Dict[str, Any]]

# People Models
class PersonItem(BaseModel):
    """Person/personnel item."""
    duns: str
    person_name: Optional[str] = None
    title: Optional[str] = None
    responsibilities: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "duns": "740039581",
                "person_name": "John Smith",
                "title": "Director",
                "responsibilities": "Director,Company Secretary"
            }
        }

class PeopleResponse(BaseModel):
    """Response for company personnel."""
    duns: str
    people: List[Dict[str, Any]]

# Operations Models
class OperationsItem(BaseModel):
    """Operations description item."""
    duns: str
    field_name: Optional[str] = None
    field_value: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "duns": "742298797",
                "field_name": "Operations",
                "field_value": "The company operates in the mining sector..."
            }
        }

class OperationsResponse(BaseModel):
    """Response for operations descriptions."""
    duns: str
    operations: List[Dict[str, Any]]

# Combined Financial Summary
class CombinedFinancialResponse(BaseModel):
    """Response for all financial statements combined."""
    duns: str
    balance_sheet: List[Dict[str, Any]]
    income_statement: List[Dict[str, Any]]
    cash_flow: List[Dict[str, Any]]

# Industry Summary
class IndustryInfo(BaseModel):
    """Industry information with company count."""
    industry_code: str
    industry_description: str
    company_count: int

class IndustryListResponse(BaseModel):
    """Response for industry listing."""
    total_industries: int
    industries: List[IndustryInfo]

# Error Response
class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Company with DUNS 999999999 not found"
            }
        }
