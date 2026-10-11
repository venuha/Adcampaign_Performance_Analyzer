"""CSV ingestion and validation of the daily campaign dataset."""

from pathlib import Path
from typing import IO

import numpy as np
import pandas as pd

from campaign_analyzer.config import DIMENSIONS, MEASURES, REQUIRED


def load_data(source: Path | IO) -> pd.DataFrame:
    """Read a CSV while preserving text identifiers, then validate it."""
    return validate_data(pd.read_csv(source, dtype={name: str for name in DIMENSIONS}))


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a sorted copy or raise ValueError with an actionable message."""

    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    df = df[REQUIRED].copy()
    if df.empty:
        raise ValueError("The CSV contains no data rows.")
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    if df["date"].isna().any():
        raise ValueError("Dates must be valid YYYY-MM-DD values.")
    for col in DIMENSIONS:
        if df[col].isna().any() or df[col].astype(str).str.strip().eq("").any():
            raise ValueError(f"{col} contains missing or blank values.")
        df[col] = df[col].astype(str).str.strip()
    for col in MEASURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if not np.isfinite(df[col]).all() or (df[col] < 0).any():
            raise ValueError(f"{col} must contain finite, non-negative numbers.")
    for col in ["impressions", "clicks", "conversions"]:
        if (df[col] % 1 != 0).any():
            raise ValueError(f"{col} must contain whole numbers.")
    if (df.clicks > df.impressions).any() or (df.conversions > df.clicks).any():
        raise ValueError("This dataset requires conversions ≤ clicks ≤ impressions.")
    if df.duplicated(["date", "campaign_id"]).any():
        raise ValueError("Duplicate date/campaign_id rows. Use one daily row per campaign.")
    if (df.groupby("campaign_id")[DIMENSIONS[1:]].nunique() > 1).any().any():
        raise ValueError(
            "Each campaign_id must have a consistent name, platform, audience and goal."
        )
    return df.sort_values(["date", "campaign_id"]).reset_index(drop=True)
