"""Streamlit application orchestration and shared sidebar controls."""

import pandas as pd
import streamlit as st

from campaign_analyzer.cache import load_dashboard_data
from campaign_analyzer.config import SAMPLE_DATA_PATH
from campaign_analyzer.filters import filter_data
from campaign_analyzer.ui.theme import apply_theme, render_hero
from campaign_analyzer.ui.views import (
    render_campaigns,
    render_definitions,
    render_overview,
    render_platforms,
    render_time_series,
)


def reset_filters() -> None:
    """Clear filter widgets so the next render restores this dataset's defaults."""
    for key in ["filter_dates", "filter_platform", "filter_audience", "filter_campaign_goal"]:
        st.session_state.pop(key, None)


def main() -> None:
    """Load and filter the dataset once, then pass it to every view."""
    st.set_page_config(page_title="Ad Campaign Performance Analyzer", page_icon="📊", layout="wide")
    apply_theme()
    render_hero()
    with st.sidebar:
        st.header("Data and filters")
        source = st.file_uploader("Upload a campaign CSV", type=["csv"])
        if source is None:
            st.info("Using synthetic sample data: July–September 2026.")
    try:
        source_bytes = source.getvalue() if source is not None else None
        df = load_dashboard_data(source_bytes)
    except (ValueError, pd.errors.ParserError, UnicodeDecodeError, OSError) as exc:
        st.error(f"Unable to load CSV: {exc}")
        st.stop()
    with st.sidebar:
        # A new CSV gets its own defaults instead of stale values from the last CSV.
        signature = (source.name, source_bytes) if source is not None else None
        if st.session_state.get("filter_dataset", "initial") != signature:
            reset_filters()
            st.session_state["filter_dataset"] = signature
        st.button("Reset Filters", on_click=reset_filters)
        dates = st.date_input(
            "Date range",
            value=(df.date.min().date(), df.date.max().date()),
            min_value=df.date.min().date(),
            max_value=df.date.max().date(),
            key="filter_dates",
        )
        selections = {}
        for column, label in [
            ("platform", "Platform"),
            ("audience", "Audience"),
            ("campaign_goal", "Campaign goal"),
        ]:
            choices = sorted(df[column].unique())
            selections[column] = st.multiselect(
                label, choices, default=choices, key=f"filter_{column}"
            )
        st.download_button(
            "Download sample CSV",
            SAMPLE_DATA_PATH.read_bytes(),
            "sample_campaign_data.csv",
            "text/csv",
        )
    if len(dates) != 2:
        st.info("Select an end date to complete the date range.")
        st.stop()
    filtered = filter_data(df, dates[0], dates[1], selections)
    if filtered.empty:
        st.warning(
            "No campaigns match these filters. Expand the date range or select more filter values."
        )
        st.stop()
    st.caption(
        f"{dates[0]:%d %b %Y} – {dates[1]:%d %b %Y} · "
        f"{filtered.campaign_id.nunique()} campaigns · {len(filtered):,} daily records"
    )
    tabs = st.tabs(["Overview", "Platform Comparison", "Campaign Details", "Time Series"])
    for tab, view in zip(
        tabs, [render_overview, render_platforms, render_campaigns, render_time_series]
    ):
        with tab:
            view(filtered)
    render_definitions()
