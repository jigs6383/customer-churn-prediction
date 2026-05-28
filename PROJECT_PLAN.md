# Customer Churn Prediction Project Plan

## Phase 1: Understand the Problem

Output:

- `docs/problem_statement.md`

Key concepts:

- Customer churn
- Business reasons customers leave
- Classification problem basics
- Business impact of churn prediction

## Phase 2: Dataset Collection

Recommended:

- Telco Customer Churn Dataset
- Bank Customer Churn Dataset
- Telecom Customer Dataset

Minimum columns:

- Customer demographics
- Subscription details
- Usage patterns
- Churn status

Starter dataset:

- Generate `dataset/raw/customer_churn_sample.csv` using `src/make_sample_data.py`

## Phase 3: Environment Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Folders are already created:

- `dataset/`
- `notebooks/`
- `src/`
- `models/`
- `outputs/`
- `app/`

## Phase 4: Data Preprocessing

Script:

- `src/preprocess.py`

Tasks covered:

- Load dataset
- Remove duplicates
- Handle missing values
- Encode categorical columns
- Scale numeric features
- Save clean dataset

## Phase 5: Exploratory Data Analysis

Script:

- `src/eda.py`

Charts:

- Churn distribution
- Tenure vs churn
- Monthly charges vs churn
- Correlation heatmap

## Phase 6: Feature Engineering

Features added:

- Tenure group
- Yearly spend
- Service count where available
- Customer lifetime value

## Phase 7: Model Building

Script:

- `src/train_model.py`

Models:

- Logistic Regression
- Decision Tree
- Random Forest

Optional extension:

- XGBoost

## Phase 8: Model Evaluation

Reports:

- `outputs/reports/model_metrics.csv`
- `outputs/reports/confusion_matrices.json`
- `outputs/reports/feature_importance.csv`

Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix

## Phase 9: Business Insights

Template:

- `docs/business_insights.md`

Focus:

- High-risk customers
- Retention recommendations
- Revenue loss estimation

## Phase 10: Visualization Dashboard

App:

- `app/streamlit_app.py`

Run:

```bash
streamlit run app/streamlit_app.py
```

## Phase 11: Deployment

Optional next steps:

- Deploy Streamlit app to Streamlit Community Cloud
- Add a Flask API
- Add Docker
- Add GitHub Actions

