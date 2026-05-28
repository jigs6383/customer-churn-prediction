import argparse
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "outputs/mpl-cache")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


FIGURE_DIR = Path("outputs/figures")
TARGET = "Churn"


def save_plot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def run_eda(input_path: str) -> None:
    df = pd.read_csv(input_path)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    sns.countplot(data=df, x=TARGET)
    plt.title("Churn Distribution")
    save_plot(FIGURE_DIR / "churn_distribution.png")

    if "MonthlyCharges" in df.columns:
        sns.histplot(data=df, x="MonthlyCharges", hue=TARGET, kde=True)
        plt.title("Monthly Charges vs Churn")
        save_plot(FIGURE_DIR / "monthly_charges_vs_churn.png")

    if "tenure" in df.columns:
        sns.histplot(data=df, x="tenure", hue=TARGET, kde=True)
        plt.title("Tenure vs Churn")
        save_plot(FIGURE_DIR / "tenure_vs_churn.png")

    corr = df.corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap")
    save_plot(FIGURE_DIR / "correlation_heatmap.png")

    summary = df.describe(include="all")
    report_path = Path("outputs/reports/eda_summary.csv")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(report_path)
    print(f"Saved EDA figures to {FIGURE_DIR}")
    print(f"Saved EDA summary to {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EDA for churn data.")
    parser.add_argument("--input", required=True, help="Path to clean churn CSV.")
    args = parser.parse_args()
    run_eda(args.input)


if __name__ == "__main__":
    main()
