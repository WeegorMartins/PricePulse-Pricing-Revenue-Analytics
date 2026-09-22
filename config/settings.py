from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
PROCESSED_DIR = ROOT / "data" / "processed"
POWERBI_DIR = ROOT / "data" / "powerbi"
OUTPUT_DIR = ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"

DB_PATH = PROCESSED_DIR / "pricepulse.duckdb"

MIN_CALENDAR_WEEKS = 52
MIN_PRICE_POINTS = 4
MIN_STORES_WITH_PRICE_CHANGE = 3
MIN_PRICE_CV = 0.01

PRICE_CHANGE_MIN = -0.10
PRICE_CHANGE_MAX = 0.10
PRICE_CHANGE_STEP = 0.01

BASELINE_WEEKS = 8

# SIMULATED analytical assumption.
# This is NOT an observed M5 cost and NOT an industry benchmark.
SIMULATED_COST_RATIO = 0.70

# Restrict candidate prices to historical support by default.
PRICE_SUPPORT_LOWER_QUANTILE = 0.10
PRICE_SUPPORT_UPPER_QUANTILE = 0.90
