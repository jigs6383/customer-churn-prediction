# Customer Churn Prediction

End-to-end machine learning project for predicting whether a customer is likely to churn. The project is designed for a Decision Scientist portfolio: it combines data cleaning, exploratory analysis, predictive modeling, evaluation, business insights, and a simple dashboard/app.

## Business Goal

Customer churn means a customer stops using a company's product or service. The goal of this project is to identify customers who are likely to leave, understand the drivers of churn, and recommend retention actions before revenue is lost.

## Project Structure

```text
Customer-Churn/
├── dataset/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── models/
├── outputs/
│   ├── figures/
│   └── reports/
├── app/
├── docs/
└── sql/
```

## Tech Stack

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn
- Streamlit
- XGBoost optional
- SQL, Excel/Tableau optional for reporting

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start With Sample Data

Generate a portfolio-friendly sample dataset:

```bash
python src/make_sample_data.py
```

Preprocess the data:

```bash
python src/preprocess.py --input dataset/raw/customer_churn_sample.csv --output dataset/processed/churn_clean.csv
```

Run EDA:

```bash
python src/eda.py --input dataset/processed/churn_clean.csv
```

Train models:

```bash
python src/train_model.py --input dataset/processed/churn_clean.csv
```

Launch the Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

## Using the Telco Customer Churn Dataset

Recommended dataset: IBM Sample Telco Customer Churn dataset, often available on Kaggle as `WA_Fn-UseC_-Telco-Customer-Churn.csv`.

Place the CSV here:

```text
dataset/raw/telco_customer_churn.csv
```

Then run:

```bash
python src/preprocess.py --input dataset/raw/telco_customer_churn.csv --output dataset/processed/telco_churn_clean.csv
python src/eda.py --input dataset/processed/telco_churn_clean.csv
python src/train_model.py --input dataset/processed/telco_churn_clean.csv
```

## Portfolio Outputs

- Problem statement: `docs/problem_statement.md`
- Clean dataset: `dataset/processed/`
- EDA charts: `outputs/figures/`
- Model metrics: `outputs/reports/model_metrics.csv`
- Business insights: `docs/business_insights.md`
- Dashboard/app: `app/streamlit_app.py`

## Suggested Timeline

- Week 1: Dataset collection, preprocessing, EDA
- Week 2: Feature engineering, modeling, evaluation
- Week 3: Dashboard, GitHub polish, resume bullet points

