from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
DATABASE_DIR = ROOT / "database"
REPORTS_DIR = ROOT / "reports"
DEFAULT_RAW_FILE = RAW_DIR / "sample_sales.csv"
EXTRACTED_FILE = PROCESSED_DIR / "extracted_sales.csv"
CLEAN_FILE = PROCESSED_DIR / "sales_clean.csv"
DATABASE_FILE = DATABASE_DIR / "sales.db"

SQLALCHEMY_URL = f"sqlite:///{DATABASE_FILE}"
