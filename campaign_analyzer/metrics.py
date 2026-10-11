"""Campaign metrics calculated from additive totals, never averaged rates."""

import pandas as pd

from campaign_analyzer.config import DERIVED_METRICS, MEASURES


def metrics(totals: dict[str, float]) -> dict[str, float]:
    """Calculate efficiency metrics; zero denominators yield NaN."""

    result = totals.copy()

    def ratio(numerator, denominator):
        return numerator / denominator if denominator else float("nan")

    result["CTR (%)"] = 100 * ratio(totals["clicks"], totals["impressions"])
    result["CVR (%)"] = 100 * ratio(totals["conversions"], totals["clicks"])
    result["CPC (USD)"] = ratio(totals["spend"], totals["clicks"])
    result["CPA (USD)"] = ratio(totals["spend"], totals["conversions"])
    result["ROAS (x)"] = ratio(totals["revenue"], totals["spend"])
    result["Ad ROI (%)"] = 100 * ratio(totals["revenue"] - totals["spend"], totals["spend"])
    return result


def aggregate(df: pd.DataFrame, dimensions: list[str]) -> pd.DataFrame:
    """Group additive measures and calculate rates from grouped totals."""
    totals = df.groupby(dimensions, as_index=False)[MEASURES].sum()
    derived = [metrics(row) for row in totals[MEASURES].to_dict("records")]
    if not derived:
        return totals.reindex(columns=[*dimensions, *MEASURES, *DERIVED_METRICS])
    result = pd.DataFrame(derived)
    return pd.concat([totals[dimensions].reset_index(drop=True), result], axis=1)
