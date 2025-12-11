# Company Financial Data API

REST API serving company financial data from CSV files. Built with FastAPI and Python 3.13.

## Features

- **222 companies** with DUNS identifiers
- **Financial data** spanning 2015-2024 (10 years)
- **7 data categories**: company info, balance sheets, income statements, cash flow, industries, people, operations
- **Auto-generated documentation** at `/docs` (Swagger UI) and `/redoc` (ReDoc)

## Quick Start

### 1. Install Dependencies

```bash
cd app
pip install -r requirements.txt
```

### 2. Run Locally

```bash
# From the app/ directory
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Company Endpoints

- `GET /companies` - List all companies (with pagination)
- `GET /companies/{duns}` - Get company details
- `GET /companies/{duns}/industries` - Get industry classifications
- `GET /companies/{duns}/people` - Get company personnel
- `GET /companies/{duns}/operations` - Get operations descriptions

### Financial Endpoints

- `GET /companies/{duns}/balance-sheet` - Get balance sheet (optional `year` parameter)
- `GET /companies/{duns}/income-statement` - Get income statement (optional `year` parameter)
- `GET /companies/{duns}/cash-flow` - Get cash flow statement (optional `year` parameter)

### Utility Endpoints

- `GET /` - API root with endpoint information
- `GET /health` - Health check and data load status

## Example Usage

### Get All Companies

```bash
curl http://localhost:8000/companies?limit=10
```

### Get Specific Company

```bash
curl http://localhost:8000/companies/740039581
```

### Get Balance Sheet for 2024

```bash
curl "http://localhost:8000/companies/740039581/balance-sheet?year=2024"
```

## Deployment

### Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize project: `railway init`
4. Deploy: `railway up`
5. Add domain: `railway domain`

### Render

1. Create account at render.com
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r app/requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy

### Fly.io

1. Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
2. Login: `flyctl auth login`
3. Launch: `flyctl launch`
4. Deploy: `flyctl deploy`

## Project Structure

```
app/
├── main.py                  # FastAPI app entry point
├── data_loader.py           # CSV data loading logic
├── models.py                # Pydantic response models
├── routers/
│   ├── companies.py         # Company endpoints
│   └── financials.py        # Financial endpoints
└── requirements.txt         # Python dependencies

data/
└── CompanyData/             # CSV files (7 subdirectories)
```

## Technology Stack

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server
- **Pandas** - Data loading from CSV
- **Pydantic** - Data validation and serialization

## Data Loading

All CSV data is loaded into memory on application startup for fast access. The API serves data from in-memory dictionaries keyed by DUNS number.

## License

Assessment project - data for evaluation purposes only.
