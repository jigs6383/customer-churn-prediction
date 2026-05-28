from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


MODEL_PATH = Path("models/best_model.joblib")
FEATURES_PATH = Path("models/feature_columns.joblib")
PREPROCESSOR_PATH = Path("models/preprocessor.joblib")
METRICS_PATH = Path("outputs/reports/model_metrics.csv")


st.set_page_config(page_title="Customer Churn Prediction", layout="wide")
st.title("Customer Churn Prediction")

if not MODEL_PATH.exists() or not FEATURES_PATH.exists() or not PREPROCESSOR_PATH.exists():
    st.warning("Run preprocessing and training first, then refresh this app.")
    st.stop()

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURES_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["YearlySpend"] = df["MonthlyCharges"] * 12
    df["CustomerLifetimeValue"] = df["MonthlyCharges"] * df["tenure"]
    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=[0, 6, 12, 24, 48, 72, float("inf")],
        labels=["0-6", "7-12", "13-24", "25-48", "49-72", "72+"],
    ).astype(str)
    return df


def transform_for_model(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = add_engineered_features(raw_df)

    for column, encoder in preprocessor["encoders"].items():
        if column in df.columns:
            values = df[column].astype(str)
            known_values = set(encoder.classes_)
            fallback = encoder.classes_[0]
            values = values.where(values.isin(known_values), fallback)
            df[column] = encoder.transform(values)

    numeric_cols = preprocessor["numeric_cols"]
    df[numeric_cols] = preprocessor["scaler"].transform(df[numeric_cols])
    return df[feature_columns]

left, right = st.columns([1, 1])

with left:
    st.subheader("Customer Inputs")
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior_citizen = st.selectbox("Senior citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.slider("Tenure", 1, 72, 12)
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    internet_service = st.selectbox("Internet service", ["DSL", "Fiber optic", "No"])
    payment_method = st.selectbox(
        "Payment method",
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
    )
    monthly_charges = st.slider("Monthly charges", 18.0, 120.0, 70.0)
    total_charges = st.number_input("Total charges", min_value=0.0, value=float(tenure * monthly_charges))
    service_count = st.slider("Service count", 1, 8, 3)

raw_input = pd.DataFrame(
    [
        {
            "gender": gender,
            "SeniorCitizen": senior_citizen,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "Contract": contract,
            "InternetService": internet_service,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "ServiceCount": service_count,
        }
    ]
)
input_df = transform_for_model(raw_input)
probability = model.predict_proba(input_df)[0, 1]
prediction = "Churn" if probability >= 0.5 else "No Churn"

with right:
    st.subheader("Prediction")
    st.metric("Churn probability", f"{probability:.1%}")
    st.metric("Predicted status", prediction)

    if probability >= 0.7:
        st.error("High-risk customer. Recommend immediate retention action.")
    elif probability >= 0.4:
        st.warning("Medium-risk customer. Recommend proactive engagement.")
    else:
        st.success("Low-risk customer.")

if METRICS_PATH.exists():
    st.subheader("Model Evaluation")
    st.dataframe(pd.read_csv(METRICS_PATH), use_container_width=True)
