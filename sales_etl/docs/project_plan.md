# Sales ETL Project Plan

## Phase 1: Understand the Problem
- Collect raw sales data from multiple sources.
- Clean and standardize the sales dataset.
- Store data in a relational database.
- Generate answers for product performance, revenue trends, regions, and customer spend.

## Phase 2: Collect Dataset
- Dataset includes Order ID, Product Name, Customer ID, Sales Amount, Region, Date, Quantity, Category.
- Sample input file: `sales_etl/data/raw/sample_sales.csv`

## Phase 3: Extract Layer
- `sales_etl/scripts/extract.py` reads CSV/Excel files.
- Handles missing raw data folder creation.
- Writes extracted output to `sales_etl/data/processed/extracted_sales.csv`.

## Phase 4: Transform Layer
- `sales_etl/scripts/transform.py` removes duplicates and invalid rows.
- Standardizes date formats and numeric columns.
- Adds `Profit Margin`, `Order Month`, `Monthly Sales`, and `Revenue Category`.

## Phase 5: Load Layer
- `sales_etl/scripts/load.py` writes cleaned records into SQLite.
- Creates dimension tables: `customers`, `products`, `regions`.
- Stores transaction rows in `sales_data`.

## Phase 6: Analytics Layer
- `sales_etl/scripts/analytics.py` generates:
  - Top products
  - Monthly revenue trends
  - Region-wise performance
  - Top customers

## Phase 7: Visualization Layer
- Saves a monthly revenue line chart to `sales_etl/reports/monthly_revenue.png`.

## Phase 8: Automation
- `sales_etl/scripts/run_pipeline.py` runs full ETL and reporting in one command.
