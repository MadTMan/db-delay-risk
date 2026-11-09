"""Cleaning stops and summarising late rates by group."""

import pandas as pd

from dbdelay.config import DELAY_COLUMN, LATE_THRESHOLD_MIN, STOP_COLUMNS


def prepare_stops(stops: pd.DataFrame) -> pd.DataFrame:
    """Keep stops where lateness can be judged, and add an is_late flag."""
    stops = stops[STOP_COLUMNS]
    missing_delay = stops[DELAY_COLUMN].isna()
    cancelled = stops["arrival_is_canceled"] | stops["departure_is_canceled"]
    kept = stops[~missing_delay & ~cancelled].copy()

    print(f"Total stops:                 {len(stops):,}")
    print(f"Removed, no delay recorded:  {missing_delay.sum():,}")
    print(f"Removed, cancelled:          {cancelled.sum():,}")
    print(f"Kept (the rules can overlap): {len(kept):,}")

    kept["is_late"] = kept[DELAY_COLUMN] >= LATE_THRESHOLD_MIN
    return kept


def late_summary(stops: pd.DataFrame, by: str, min_stops: int) -> pd.DataFrame:
    """Count stops and late stops per group, with the late rate."""
    summary = stops.groupby(by, observed=True).agg(
        stops=("is_late", "size"),
        late_stops=("is_late", "sum"),
    )
    summary["late_rate"] = summary["late_stops"] / summary["stops"]
    enough = summary["stops"] >= min_stops
    return summary[enough].sort_values("late_rate", ascending=False)


def station_names(stops: pd.DataFrame) -> pd.Series:
    """Map each station number (eva) to one readable station name."""
    return stops.drop_duplicates(subset="eva").set_index("eva")["station_name"]


def add_type_late_rate(stops: pd.DataFrame) -> pd.DataFrame:
    """Add each stop's train-type late rate, measured across all stations."""
    type_rate = stops.groupby("train_type", observed=True)["is_late"].mean()
    typed = stops.copy()
    typed["type_late_rate"] = typed["train_type"].map(type_rate).astype("float64")
    return typed


def station_vs_expected(stops: pd.DataFrame, min_stops: int) -> pd.DataFrame:
    """Per station: actual late rate vs the rate its train mix would predict."""
    stations = stops.groupby("eva", observed=True).agg(
        stops=("is_late", "size"),
        late_rate=("is_late", "mean"),
        expected_rate=("type_late_rate", "mean"),
    )
    stations["excess"] = stations["late_rate"] - stations["expected_rate"]
    return stations[stations["stops"] >= min_stops]
