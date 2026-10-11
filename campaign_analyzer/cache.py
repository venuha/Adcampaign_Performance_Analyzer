"""Bounded caching for validated CSV data; uploads remain session-specific."""

from io import BytesIO

import pandas as pd
import streamlit as st

from campaign_analyzer.config import SAMPLE_DATA_PATH
from campaign_analyzer.data import load_data


@st.cache_data(show_spinner=False, max_entries=2)
def load_sample_csv(content: bytes) -> pd.DataFrame:
    """Cache bundled data by its bytes so file changes invalidate the cache."""
    return load_data(BytesIO(content))


def load_dashboard_data(upload: bytes | None = None) -> pd.DataFrame:
    """Cache the sample globally and uploaded CSVs only in the current session."""
    if upload is None:
        return load_sample_csv(SAMPLE_DATA_PATH.read_bytes())
    cached = st.session_state.get("uploaded_csv_cache")
    if cached is not None and cached[0] == upload:
        return cached[1].copy(deep=True)
    frame = load_data(BytesIO(upload))
    st.session_state["uploaded_csv_cache"] = (upload, frame.copy(deep=True))
    return frame
