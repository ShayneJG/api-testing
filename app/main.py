"""
FastAPI application for Company Financial Data API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import data_loader
from routers import companies, financials, industries

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to load data on startup and cleanup on shutdown.
    """
    # Startup: Load all CSV data into memory
    data_loader.load_all_data()
    yield
    # Shutdown: cleanup if needed
    print("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Company Financial Data API",
    description="""
    REST API serving company financial data from CSV files.

    ## Features

    * **Company Information**: Get detailed company info by DUNS number
    * **Financial Statements**: Access balance sheets, income statements, and cash flow data
    * **Industries**: View industry classifications for companies
    * **Personnel**: Get information about company directors and key personnel
    * **Operations**: View company operations descriptions

    ## Data Coverage

    * 222 companies with DUNS identifiers
    * Financial data spanning 2015-2024 (10 years)
    * 7 data categories per company

    ## Usage

    All endpoints accept DUNS numbers as the primary identifier. Use the `/companies`
    endpoint to browse available companies and get their DUNS numbers.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for public API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router)
app.include_router(financials.router)
app.include_router(industries.router)

# Root endpoint
@app.get(
    "/",
    tags=["health"],
    summary="API Root",
    description="Welcome endpoint with API information"
)
def root():
    """API root endpoint."""
    return {
        "message": "Company Financial Data API",
        "version": "1.0.0",
        "documentation": "/docs",
        "alternative_docs": "/redoc",
        "endpoints": {
            "companies": "/companies",
            "search_companies": "/companies/search",
            "company_detail": "/companies/{duns}",
            "financial_summary": "/companies/{duns}/financials/summary",
            "balance_sheet": "/companies/{duns}/balance-sheet",
            "income_statement": "/companies/{duns}/income-statement",
            "cash_flow": "/companies/{duns}/cash-flow",
            "industries": "/companies/{duns}/industries",
            "people": "/companies/{duns}/people",
            "operations": "/companies/{duns}/operations",
            "all_industries": "/industries"
        }
    }

@app.get(
    "/health",
    tags=["health"],
    summary="Health Check",
    description="Check if the API is running and data is loaded"
)
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "companies_loaded": len(data_loader.company_data),
        "data_sources": {
            "company_info": len(data_loader.company_data),
            "balance_sheets": len(data_loader.balance_sheet_data),
            "income_statements": len(data_loader.income_statement_data),
            "cash_flows": len(data_loader.cash_flow_data),
            "industries": len(data_loader.industries_data),
            "people": len(data_loader.people_data),
            "operations": len(data_loader.operations_data)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
