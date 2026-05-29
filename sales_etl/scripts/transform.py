import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import PROCESSED_DIR, EXTRACTED_FILE, CLEAN_FILE

import numpy as np
import pandas as pd


def ensure_dirs():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_sales_amount(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def transform():
    ensure_dirs()
    if not EXTRACTED_FILE.exists():
        raise FileNotFoundError(f"Extracted file not found: {EXTRACTED_FILE}")

    df = pd.read_csv(EXTRACTED_FILE)
    df = df.drop_duplicates()
    df = df.rename(columns=str.strip)

    df["Sales Amount"] = df["Sales Amount"].apply(normalize_sales_amount)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).astype(int)
    if "Cost" in df.columns:
        df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
    else:
        df["Cost"] = np.nan

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Order ID", "Product Name", "Customer ID", "Sales Amount", "Date"])
    df = df[df["Sales Amount"] > 0]
    df = df[df["Quantity"] > 0]

    if "Cost" not in df.columns or df["Cost"].isna().all():
        df["Cost"] = df["Sales Amount"] * 0.7

    df["Profit Margin"] = df["Sales Amount"] - df["Cost"]
    df["Order Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Revenue Category"] = pd.cut(
        df["Sales Amount"],
        bins=[-np.inf, 50, 150, np.inf],
        labels=["Low", "Medium", "High"],
    )
    df["Monthly Sales"] = df["Sales Amount"] * df["Quantity"]

    df.to_csv(CLEAN_FILE, index=False)
    print(f"Transformed and cleaned {len(df)} rows to {CLEAN_FILE}")
    return df


if __name__ == "__main__":
    transform()
