from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
METADATA = DATA / "metadata"

STATCAN_TABLES = {
    "labour_force_industry_age": {
        "table_id": "14100023",
        "title": "Labour force characteristics by industry, annual",
        "url": "https://www150.statcan.gc.ca/n1/en/tbl/csv/14100023-eng.zip",
    },
    "absence_industry": {
        "table_id": "14100191",
        "title": "Work absence of full-time employees by industry, annual",
        "url": "https://www150.statcan.gc.ca/n1/en/tbl/csv/14100191-eng.zip",
    },
    "absence_age": {
        "table_id": "14100193",
        "title": "Work absence of full-time employees by age group, annual",
        "url": "https://www150.statcan.gc.ca/n1/en/tbl/csv/14100193-eng.zip",
    },
}
