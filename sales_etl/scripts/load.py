import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import DATABASE_DIR, DATABASE_FILE, SQLALCHEMY_URL, CLEAN_FILE

import pandas as pd
from sqlalchemy import Column, Date, Float, Integer, MetaData, String, Table, create_engine


metadata = MetaData()

customers = Table(
    "customers",
    metadata,
    Column("customer_id", String, primary_key=True),
)

products = Table(
    "products",
    metadata,
    Column("product_name", String, primary_key=True),
    Column("category", String),
)

regions = Table(
    "regions",
    metadata,
    Column("region", String, primary_key=True),
)

sales_data = Table(
    "sales_data",
    metadata,
    Column("order_id", String, primary_key=True),
    Column("product_name", String),
    Column("customer_id", String),
    Column("region", String),
    Column("date", Date),
    Column("quantity", Integer),
    Column("sales_amount", Float),
    Column("cost", Float),
    Column("profit_margin", Float),
    Column("order_month", String),
    Column("revenue_category", String),
    Column("monthly_sales", Float),
)


def ensure_dirs():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)


def load():
    ensure_dirs()
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"Clean file not found: {CLEAN_FILE}")

    df = pd.read_csv(CLEAN_FILE, parse_dates=["Date"])
    df = df.rename(
        columns={
            "Order ID": "order_id",
            "Product Name": "product_name",
            "Customer ID": "customer_id",
            "Region": "region",
            "Date": "date",
            "Quantity": "quantity",
            "Sales Amount": "sales_amount",
            "Cost": "cost",
            "Category": "category",
            "Profit Margin": "profit_margin",
            "Order Month": "order_month",
            "Revenue Category": "revenue_category",
            "Monthly Sales": "monthly_sales",
        }
    )

    engine = create_engine(SQLALCHEMY_URL, future=True)
    metadata.drop_all(engine)
    metadata.create_all(engine)

    with engine.begin() as conn:
        unique_customers = df[["customer_id"]].drop_duplicates()
        conn.execute(customers.insert(), unique_customers.to_dict(orient="records"))

        unique_products = df[["product_name", "category"]].drop_duplicates()
        conn.execute(products.insert(), unique_products.to_dict(orient="records"))

        unique_regions = df[["region"]].drop_duplicates()
        conn.execute(regions.insert(), unique_regions.to_dict(orient="records"))

        sales_rows = df.to_dict(orient="records")
        conn.execute(sales_data.insert(), sales_rows)
    print(f"Loaded {len(df)} rows into {DATABASE_FILE}")
    return SQLALCHEMY_URL


if __name__ == "__main__":
    load()
