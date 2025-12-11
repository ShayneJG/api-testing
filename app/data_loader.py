"""
Data loader module for loading company CSV data into memory.
"""
import os
from pathlib import Path
from typing import Dict, List
import pandas as pd

# Global data storage
company_data: Dict[str, Dict[str, str]] = {}
balance_sheet_data: Dict[str, List[Dict]] = {}
income_statement_data: Dict[str, List[Dict]] = {}
cash_flow_data: Dict[str, List[Dict]] = {}
industries_data: Dict[str, List[Dict]] = {}
people_data: Dict[str, List[Dict]] = {}
operations_data: Dict[str, List[Dict]] = {}

def get_data_path() -> Path:
    """Get the path to the CompanyData directory."""
    # From app/ directory, go up one level to project root, then into data/CompanyData
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "data" / "CompanyData"
    return data_path

def load_company_info():
    """Load company info CSV files into memory."""
    data_path = get_data_path() / "company_info"

    if not data_path.exists():
        print(f"Warning: {data_path} does not exist")
        return

    for csv_file in data_path.glob("*.csv"):
        duns = csv_file.stem  # filename without extension

        try:
            df = pd.read_csv(csv_file)
            # Convert field/value pairs to dictionary
            company_info = {}
            for _, row in df.iterrows():
                field = row['field']
                value = row['value']
                company_info[field] = value

            company_data[duns] = company_info
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

def load_financial_data(folder_name: str, target_dict: Dict[str, List[Dict]]):
    """Load financial statement CSV files (balance sheet, income statement, cash flow)."""
    data_path = get_data_path() / folder_name

    if not data_path.exists():
        print(f"Warning: {data_path} does not exist")
        return

    for csv_file in data_path.glob("*.csv"):
        duns = csv_file.stem

        try:
            df = pd.read_csv(csv_file)
            # Convert to list of dictionaries
            records = df.to_dict('records')
            target_dict[duns] = records
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

def load_industries():
    """Load industry classification CSV files."""
    data_path = get_data_path() / "industries"

    if not data_path.exists():
        print(f"Warning: {data_path} does not exist")
        return

    for csv_file in data_path.glob("*.csv"):
        duns = csv_file.stem

        try:
            df = pd.read_csv(csv_file)
            records = df.to_dict('records')
            industries_data[duns] = records
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

def load_people():
    """Load people/personnel CSV files."""
    data_path = get_data_path() / "people"

    if not data_path.exists():
        print(f"Warning: {data_path} does not exist")
        return

    for csv_file in data_path.glob("*.csv"):
        duns = csv_file.stem

        try:
            df = pd.read_csv(csv_file)
            records = df.to_dict('records')
            people_data[duns] = records
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

def load_operations():
    """Load operations description CSV files."""
    data_path = get_data_path() / "operations"

    if not data_path.exists():
        print(f"Warning: {data_path} does not exist")
        return

    for csv_file in data_path.glob("*.csv"):
        duns = csv_file.stem

        try:
            df = pd.read_csv(csv_file)
            records = df.to_dict('records')
            operations_data[duns] = records
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

def load_all_data():
    """Load all CSV data into memory."""
    print("Loading company data...")

    load_company_info()
    print(f"Loaded {len(company_data)} companies")

    load_financial_data("balance_sheet", balance_sheet_data)
    print(f"Loaded balance sheets for {len(balance_sheet_data)} companies")

    load_financial_data("income_statement", income_statement_data)
    print(f"Loaded income statements for {len(income_statement_data)} companies")

    load_financial_data("cash_flow_statement", cash_flow_data)
    print(f"Loaded cash flow statements for {len(cash_flow_data)} companies")

    load_industries()
    print(f"Loaded industries for {len(industries_data)} companies")

    load_people()
    print(f"Loaded people for {len(people_data)} companies")

    load_operations()
    print(f"Loaded operations for {len(operations_data)} companies")

    print("Data loading complete!")

def get_all_duns_numbers() -> List[str]:
    """Get list of all DUNS numbers."""
    return list(company_data.keys())
