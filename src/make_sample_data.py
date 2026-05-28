from pathlib import Path

import numpy as np
import pandas as pd


RAW_DIR = Path("dataset/raw")
OUTPUT_PATH = RAW_DIR / "customer_churn_sample.csv"


def make_sample_data(rows: int = 1000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    gender = rng.choice(["Female", "Male"], rows)
    senior_citizen = rng.choice([0, 1], rows, p=[0.84, 0.16])
    partner = rng.choice(["Yes", "No"], rows, p=[0.48, 0.52])
    dependents = rng.choice(["Yes", "No"], rows, p=[0.30, 0.70])
    tenure = rng.integers(1, 73, rows)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], rows, p=[0.55, 0.25, 0.20])
    internet_service = rng.choice(["DSL", "Fiber optic", "No"], rows, p=[0.35, 0.45, 0.20])
    payment_method = rng.choice(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
        rows,
        p=[0.34, 0.22, 0.22, 0.22],
    )
    monthly_charges = np.round(
        rng.normal(65, 22, rows)
        + np.where(internet_service == "Fiber optic", 18, 0)
        - np.where(internet_service == "No", 25, 0),
        2,
    )
    monthly_charges = np.clip(monthly_charges, 18, 120)
    total_charges = np.round(monthly_charges * tenure + rng.normal(0, 80, rows), 2)
    service_count = rng.integers(1, 7, rows)

    logit = (
        -1.4
        + 1.1 * (contract == "Month-to-month")
        + 0.7 * (internet_service == "Fiber optic")
        + 0.5 * (payment_method == "Electronic check")
        + 0.012 * (monthly_charges - 65)
        - 0.025 * tenure
        - 0.12 * service_count
        + 0.35 * senior_citizen
    )
    churn_probability = 1 / (1 + np.exp(-logit))
    churn = rng.binomial(1, churn_probability)

    return pd.DataFrame(
        {
            "customerID": [f"CUST-{i:05d}" for i in range(1, rows + 1)],
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
            "Churn": np.where(churn == 1, "Yes", "No"),
        }
    )


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = make_sample_data()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved sample dataset to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

