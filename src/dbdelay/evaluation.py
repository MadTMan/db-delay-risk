"""Scoring two prediction methods day by day (Brier score and a sign test)."""

import pandas as pd
from scipy.stats import binom

from dbdelay.config import ALPHA


def planned_day(stops: pd.DataFrame) -> pd.Series:
    """Calendar day of each stop: planned departure, or planned arrival at final stops."""
    planned = stops["departure_planned_time"].fillna(stops["arrival_planned_time"])
    return planned.dt.normalize()


def brier_by_day(is_late: pd.Series, prob: pd.Series, day: pd.Series) -> pd.Series:
    """Average squared gap between predicted probability and what happened, per day."""
    squared_error = (prob - is_late.astype(float)) ** 2
    return squared_error.groupby(day).mean()


def compare_by_day(is_late: pd.Series, prob_a: pd.Series, prob_b: pd.Series,
                   day: pd.Series) -> pd.DataFrame:
    """Score two methods on the same stops each day. Positive gap means B was better."""
    daily = pd.DataFrame({
        "brier_a": brier_by_day(is_late, prob_a, day),
        "brier_b": brier_by_day(is_late, prob_b, day),
    })
    daily["gap"] = daily["brier_a"] - daily["brier_b"]
    return daily


def min_wins_needed(n_days: int, alpha: float = ALPHA) -> int:
    """Fewest wins out of n_days that a fair coin reaches less than alpha of the time."""
    for wins in range(n_days + 1):
        if binom.sf(wins - 1, n_days, 0.5) < alpha:   # chance of >= wins heads
            return wins
    return n_days + 1   # too few days: no result can be convincing


def summarise_days(daily: pd.DataFrame) -> dict:
    """Count B's wins (tied days are dropped, as in a standard sign test)."""
    decided = daily[daily["gap"] != 0]
    return {
        "days_decided": len(decided),
        "b_wins": int((decided["gap"] > 0).sum()),
        "wins_needed": min_wins_needed(len(decided)),
        "mean_daily_gap": daily["gap"].mean(),
    }
