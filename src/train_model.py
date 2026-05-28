import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


TARGET = "Churn"
MODELS_DIR = Path("models")
REPORTS_DIR = Path("outputs/reports")


def evaluate_model(name: str, model, x_test, y_test) -> dict:
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    return {
        "model": name,
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
    }


def train(input_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    if TARGET not in df.columns:
        raise ValueError(f"Target column '{TARGET}' not found in {input_path}")

    x = df.drop(columns=[TARGET])
    y = df[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "decision_tree": DecisionTreeClassifier(max_depth=6, random_state=42, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=250,
            max_depth=8,
            random_state=42,
            class_weight="balanced",
        ),
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    metrics = []
    best_name = None
    best_score = -1
    best_model = None

    for name, model in models.items():
        model.fit(x_train, y_train)
        result = evaluate_model(name, model, x_test, y_test)
        metrics.append(result)
        if result["f1"] > best_score:
            best_name = name
            best_score = result["f1"]
            best_model = model

    metrics_df = pd.DataFrame(metrics)
    metrics_df.drop(columns=["confusion_matrix"]).to_csv(REPORTS_DIR / "model_metrics.csv", index=False)

    with (REPORTS_DIR / "confusion_matrices.json").open("w") as file:
        json.dump({item["model"]: item["confusion_matrix"] for item in metrics}, file, indent=2)

    joblib.dump(best_model, MODELS_DIR / "best_model.joblib")
    joblib.dump(list(x.columns), MODELS_DIR / "feature_columns.joblib")

    if hasattr(best_model, "feature_importances_"):
        importance_df = pd.DataFrame(
            {"feature": x.columns, "importance": best_model.feature_importances_}
        ).sort_values("importance", ascending=False)
        importance_df.to_csv(REPORTS_DIR / "feature_importance.csv", index=False)

    print(f"Best model: {best_name} with F1={best_score:.3f}")
    print(f"Saved model to {MODELS_DIR / 'best_model.joblib'}")
    return metrics_df


def main() -> None:
    parser = argparse.ArgumentParser(description="Train churn prediction models.")
    parser.add_argument("--input", required=True, help="Path to clean churn CSV.")
    args = parser.parse_args()
    train(args.input)


if __name__ == "__main__":
    main()

