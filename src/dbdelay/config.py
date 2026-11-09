"""Project-wide settings: folders, months and the definition of a late stop."""

from pathlib import Path

# Folders, built from this file's location so they work from any working directory.
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data"
REPORTS_DIR = PROJECT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"

MONTHS = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]  # files in data/

DELAY_COLUMN = "delay_in_min"
LATE_THRESHOLD_MIN = 6  # a stop is "late" at this many minutes or more
PLANNED_TIME_COLUMNS = ["departure_planned_time", "arrival_planned_time"]
STOP_COLUMNS = [
    "train_type", "eva", "station_name",
    DELAY_COLUMN, "arrival_is_canceled", "departure_is_canceled",
    *PLANNED_TIME_COLUMNS,
]

ALPHA = 0.05  # accepted chance that ML "wins" by pure luck
