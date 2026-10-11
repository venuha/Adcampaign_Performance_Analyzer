"""Pure filtering and time aggregation helpers used across dashboard views."""

from datetime import date

import pandas as pd

from campaign_analyzer.metrics import aggregate


def filter_data(
    df: pd.DataFrame, start: date, end: date, selections: dict[str, list[str]]
) -> pd.DataFrame:
    """Apply inclusive dates and every selected dimension to the same rows."""
    filtered = df[df.date.between(pd.Timestamp(start), pd.Timestamp(end))]
    for column, values in selections.items():
        filtered = filtered[filtered[column].isin(values)]
    return filtered.copy()


def search_campaigns(details: pd.DataFrame, query: str) -> pd.DataFrame:
    """Search by literal name or ID, ignoring case; an empty query returns all."""
    if not query:
        return details
    return details[
        details.campaign_name.str.contains(query, case=False, regex=False)
        | details.campaign_id.str.contains(query, case=False, regex=False)
    ]


def time_series(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """Aggregate by platform and period; weeks start Monday."""
    frequencies = {"Daily": "D", "Weekly": "W-SUN", "Monthly": "M"}
    if interval not in frequencies:
        raise ValueError(f"Unsupported time interval: {interval}")
    trend = df.copy()
    trend["period_start"] = trend.date.dt.to_period(frequencies[interval]).dt.start_time
    return aggregate(trend, ["period_start", "platform"])
