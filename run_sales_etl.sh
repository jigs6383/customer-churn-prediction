#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m venv .venv-sales
source .venv-sales/bin/activate
pip install -r sales_etl/requirements.txt
python sales_etl/scripts/run_pipeline.py
