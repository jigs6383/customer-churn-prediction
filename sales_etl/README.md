# Sales ETL Project

This subproject implements an end-to-end retail sales ETL pipeline:
- extract raw CSV/Excel sales data
- transform and clean the dataset
- load cleaned data into a SQL database
- generate analytics that answer top products, monthly revenue, region performance, and top customers

## Run the pipeline

```bash
python3 -m venv .venv-sales
source .venv-sales/bin/activate
pip install -r sales_etl/requirements.txt
python sales_etl/scripts/run_pipeline.py
```

## Folder structure

- `sales_etl/data/raw/` — raw input files
- `sales_etl/data/processed/` — extracted and cleaned outputs
- `sales_etl/database/` — SQLite database file
- `sales_etl/reports/` — analytics outputs
- `sales_etl/scripts/` — ETL and analytics scripts

## Output questions

The pipeline produces answers for:
- Which products sell the most?
- Monthly revenue trends
- Region-wise sales performance
- Top customers
