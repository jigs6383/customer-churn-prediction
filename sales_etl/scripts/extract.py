import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import RAW_DIR, PROCESSED_DIR, DEFAULT_RAW_FILE, EXTRACTED_FILE

import pandas as pd


def ensure_dirs():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def read_raw_files() -> pd.DataFrame:
    source_files = list(RAW_DIR.glob("*.csv")) + list(RAW_DIR.glob("*.xlsx"))
    if not source_files:
        raise FileNotFoundError(
            f"No raw input files found in {RAW_DIR}. Please add CSV or Excel files."
        )

    frames = []
    for path in sorted(source_files):
        if path.suffix.lower() == ".csv":
            frames.append(pd.read_csv(path))
        else:
            frames.append(pd.read_excel(path))

    return pd.concat(frames, ignore_index=True)


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "order_id": "Order ID",
        "order id": "Order ID",
        "product": "Product Name",
        "product_name": "Product Name",
        "customer_id": "Customer ID",
        "customer": "Customer ID",
        "sales_amount": "Sales Amount",
        "sales": "Sales Amount",
        "amount": "Sales Amount",
        "region": "Region",
        "date": "Date",
        "quantity": "Quantity",
        "category": "Category",
        "product_category": "Category",
        "cost": "Cost",
    }
    df = df.rename(columns={c: rename_map.get(c.lower(), c) for c in df.columns})
    return df


def extract():
    ensure_dirs()
    df = read_raw_files()
    df = standardize_columns(df)
    df.to_csv(EXTRACTED_FILE, index=False)
    print(f"Extracted {len(df)} rows to {EXTRACTED_FILE}")
    return df


if __name__ == "__main__":
    extract()
