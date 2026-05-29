import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import DATABASE_FILE, REPORTS_DIR, SQLALCHEMY_URL

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text


def ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def query_database():
    engine = create_engine(SQLALCHEMY_URL, future=True)
    with engine.connect() as conn:
        top_products = pd.read_sql(
            text(
                "SELECT product_name, SUM(sales_amount) AS total_sales, SUM(quantity) AS total_quantity "
                "FROM sales_data GROUP BY product_name ORDER BY total_sales DESC LIMIT 10"
            ),
            conn,
        )
        monthly_revenue = pd.read_sql(
            text(
                "SELECT order_month, SUM(sales_amount) AS monthly_revenue "
                "FROM sales_data GROUP BY order_month ORDER BY order_month"
            ),
            conn,
        )
        region_sales = pd.read_sql(
            text(
                "SELECT region, SUM(sales_amount) AS region_revenue, SUM(quantity) AS total_quantity "
                "FROM sales_data GROUP BY region ORDER BY region_revenue DESC"
            ),
            conn,
        )
        top_customers = pd.read_sql(
            text(
                "SELECT customer_id, SUM(sales_amount) AS total_spend, COUNT(order_id) AS order_count "
                "FROM sales_data GROUP BY customer_id ORDER BY total_spend DESC LIMIT 10"
            ),
            conn,
        )

    return top_products, monthly_revenue, region_sales, top_customers


def save_reports(top_products, monthly_revenue, region_sales, top_customers):
    ensure_dirs()
    top_products.to_csv(REPORTS_DIR / "top_products.csv", index=False)
    monthly_revenue.to_csv(REPORTS_DIR / "monthly_revenue.csv", index=False)
    region_sales.to_csv(REPORTS_DIR / "region_sales.csv", index=False)
    top_customers.to_csv(REPORTS_DIR / "top_customers.csv", index=False)

    summary_path = REPORTS_DIR / "analytics_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as handle:
        handle.write("Top Products\n")
        handle.write(top_products.to_string(index=False))
        handle.write("\n\nMonthly Revenue Trend\n")
        handle.write(monthly_revenue.to_string(index=False))
        handle.write("\n\nRegion-wise Performance\n")
        handle.write(region_sales.to_string(index=False))
        handle.write("\n\nTop Customers\n")
        handle.write(top_customers.to_string(index=False))

    return summary_path


def plot_monthly_revenue(monthly_revenue):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly_revenue["order_month"], monthly_revenue["monthly_revenue"], marker="o")
    ax.set_title("Monthly Revenue Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    output_chart = REPORTS_DIR / "monthly_revenue.png"
    fig.savefig(output_chart)
    plt.close(fig)
    return output_chart


def analyze():
    top_products, monthly_revenue, region_sales, top_customers = query_database()
    summary_path = save_reports(top_products, monthly_revenue, region_sales, top_customers)
    chart_path = plot_monthly_revenue(monthly_revenue)
    print(f"Saved analytics summary to {summary_path}")
    print(f"Saved monthly revenue chart to {chart_path}")
    return top_products, monthly_revenue, region_sales, top_customers


if __name__ == "__main__":
    analyze()
