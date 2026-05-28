import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


TARGET = "Churn"


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def normalize_telco_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if {"MonthlyCharges", "tenure"}.issubset(df.columns):
        df["YearlySpend"] = df["MonthlyCharges"] * 12
        df["CustomerLifetimeValue"] = df["MonthlyCharges"] * df["tenure"]
        df["TenureGroup"] = pd.cut(
            df["tenure"],
            bins=[0, 6, 12, 24, 48, 72, float("inf")],
            labels=["0-6", "7-12", "13-24", "25-48", "49-72", "72+"],
        ).astype(str)
    if "ServiceCount" not in df.columns:
        service_like_cols = [
            col
            for col in df.columns
            if col
            in {
                "PhoneService",
                "MultipleLines",
                "OnlineSecurity",
                "OnlineBackup",
                "DeviceProtection",
                "TechSupport",
                "StreamingTV",
                "StreamingMovies",
            }
        ]
        if service_like_cols:
            df["ServiceCount"] = (df[service_like_cols] == "Yes").sum(axis=1)
    return df


def encode_and_scale(df: pd.DataFrame, artifacts_dir: str = "models") -> pd.DataFrame:
    df = df.copy()

    if TARGET in df.columns:
        df[TARGET] = df[TARGET].map({"Yes": 1, "No": 0, 1: 1, 0: 0}).astype(int)

    id_columns = [col for col in ["customerID", "customer_id"] if col in df.columns]
    df = df.drop(columns=id_columns)

    categorical_cols = [
        col for col in df.select_dtypes(include=["object", "category", "bool"]).columns if col != TARGET
    ]
    encoders = {}
    for col in categorical_cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col].astype(str))
        encoders[col] = encoder

    numeric_cols = [col for col in df.select_dtypes(include=["number"]).columns if col != TARGET]
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    artifacts = {
        "target": TARGET,
        "categorical_cols": categorical_cols,
        "numeric_cols": numeric_cols,
        "feature_columns": [col for col in df.columns if col != TARGET],
        "encoders": encoders,
        "scaler": scaler,
    }
    artifacts_path = Path(artifacts_dir) / "preprocessor.joblib"
    artifacts_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifacts, artifacts_path)
    return df


def preprocess(input_path: str, output_path: str, artifacts_dir: str = "models") -> pd.DataFrame:
    df = pd.read_csv(input_path)
    df = clean_column_names(df)
    df = normalize_telco_types(df)
    df = df.drop_duplicates()
    df = add_features(df)
    df = df.dropna()
    clean_df = encode_and_scale(df, artifacts_dir=artifacts_dir)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output, index=False)
    return clean_df


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess customer churn data.")
    parser.add_argument("--input", required=True, help="Path to raw churn CSV.")
    parser.add_argument("--output", required=True, help="Path for clean CSV.")
    parser.add_argument("--artifacts-dir", default="models", help="Directory for preprocessing artifacts.")
    args = parser.parse_args()

    clean_df = preprocess(args.input, args.output, artifacts_dir=args.artifacts_dir)
    print(f"Saved clean data to {args.output}")
    print(f"Rows: {clean_df.shape[0]}, Columns: {clean_df.shape[1]}")


if __name__ == "__main__":
    main()
