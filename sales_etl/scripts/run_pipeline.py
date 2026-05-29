import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from extract import extract
from transform import transform
from load import load
from analytics import analyze


def main():
    os.chdir(ROOT)
    print("Starting Sales ETL pipeline...")
    extract()
    transform()
    load()
    analyze()
    print("Sales ETL pipeline completed.")


if __name__ == "__main__":
    main()
