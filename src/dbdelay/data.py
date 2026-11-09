"""Where the monthly data files and the month-named outputs live."""

from pathlib import Path

from dbdelay.config import DATA_DIR, MONTHS


def month_path(month: str) -> Path:
    """Path of the Parquet file for one month, e.g. "2026-07"."""
    if month not in MONTHS:
        raise ValueError(f"Unknown month {month!r}; expected one of {MONTHS}")
    return DATA_DIR / f"data-{month}.parquet"


def month_file(folder: Path, stem: str, extension: str, month: str) -> Path:
    """Output path with the month in its name, e.g. late_rate_by_train_type_2026-07.csv."""
    return folder / f"{stem}_{month}.{extension}"
