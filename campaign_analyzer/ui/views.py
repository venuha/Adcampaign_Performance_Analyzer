"""The dashboard's four views, all operating on the same filtered data."""

import math

import pandas as pd
import streamlit as st

from campaign_analyzer.charts import (
    funnel_chart,
    platform_chart,
    spend_conversions_chart,
    trend_chart,
)
from campaign_analyzer.config import DIMENSIONS, MEASURES
from campaign_analyzer.filters import search_campaigns, time_series
from campaign_analyzer.metrics import aggregate, metrics, top_campaigns
from campaign_analyzer.ui.components import chart, table


def render_overview(filtered: pd.DataFrame) -> None:
    """Show summary metrics and daily spend versus conversions."""
    totals = metrics(filtered[MEASURES].sum().to_dict())
    labels = [
        ("Spend (USD)", "spend", "$", ",.0f"),
        ("Clicks", "clicks", "", ",.0f"),
        ("Conversions", "conversions", "", ",.0f"),
        ("Revenue (USD)", "revenue", "$", ",.0f"),
        ("ROAS (x)", "ROAS (x)", "", ".2f"),
        ("Ad ROI (%)", "Ad ROI (%)", "", ".1f"),
    ]
    for start in (0, 3):
        for cell, (label, key, prefix, fmt) in zip(st.columns(3), labels[start : start + 3]):
            value = totals[key]
            cell.metric(label, "N/A" if not math.isfinite(value) else prefix + format(value, fmt))
    daily = aggregate(filtered, ["date"])
    chart(spend_conversions_chart(daily))
    st.subheader("Efficiency metrics")
    table(pd.DataFrame([{k: totals[k] for k in ["CTR (%)", "CVR (%)", "CPC (USD)", "CPA (USD)"]}]))
    st.subheader("Top 5 campaigns by Ad ROI")
    leaders = top_campaigns(filtered)
    if leaders.empty:
        st.info("No campaigns with positive spend are available to rank.")
    else:
        table(
            leaders[
                [
                    "campaign_id",
                    "campaign_name",
                    "platform",
                    "campaign_goal",
                    "spend",
                    "conversions",
                    "Ad ROI (%)",
                ]
            ]
        )
    st.caption(
        "Ranked over the selected dates. Zero-spend campaigns are excluded. Compare matching goals and audiences."
    )


def render_platforms(filtered: pd.DataFrame) -> None:
    """Compare channel results for the active filters."""
    grouped = aggregate(filtered, ["platform"])
    measure = st.selectbox(
        "Compare platforms by",
        ["spend", "conversions", "revenue", "ROAS (x)", "Ad ROI (%)", "CPA (USD)"],
    )
    chart(platform_chart(grouped, measure))
    table(grouped)
    st.caption(
        "Compare campaigns with similar goals and audiences before judging channel efficiency."
    )


def render_campaigns(filtered: pd.DataFrame) -> None:
    """Search campaign summaries and export matching rows."""
    query = st.text_input("Search campaign name or ID")
    details = search_campaigns(aggregate(filtered, DIMENSIONS), query)
    if details.empty:
        st.info("No campaigns match your search.")
    else:
        table(details.sort_values("spend", ascending=False))
        st.download_button(
            "Download campaign summary",
            details.to_csv(index=False),
            "campaign_summary.csv",
            "text/csv",
        )
    st.subheader("Campaign funnel")
    st.caption(
        "Uses all campaigns matching the sidebar filters; the table search does not change the funnel."
    )
    chart(funnel_chart(filtered))
    totals = filtered[["impressions", "clicks", "conversions"]].sum()
    counts = [int(totals.impressions), int(totals.clicks), int(totals.conversions)]
    retention = ["—"] + [f"{b / a:.1%}" if a else "N/A" for a, b in zip(counts, counts[1:])]
    st.dataframe(
        pd.DataFrame(
            {
                "Stage": ["Impressions", "Clicks", "Conversions"],
                "Count": counts,
                "Retention from prior stage": retention,
            }
        ),
        hide_index=True,
        width="stretch",
    )


def render_time_series(filtered: pd.DataFrame) -> None:
    """Explore daily, weekly or monthly channel trends."""
    frequency = st.selectbox("Time interval", ["Daily", "Weekly", "Monthly"])
    measure = st.selectbox(
        "Trend metric",
        [
            "spend",
            "clicks",
            "conversions",
            "revenue",
            "CTR (%)",
            "CVR (%)",
            "CPA (USD)",
            "ROAS (x)",
            "Ad ROI (%)",
        ],
    )
    trend = time_series(filtered, frequency)
    chart(trend_chart(trend, measure))
    st.caption(
        "Weeks start on Monday. Boundary weeks and months contain only dates in the selected range. Missing periods have no recorded data."
    )
    table(trend)


def render_definitions() -> None:
    """Explain metric definitions and source assumptions."""
    with st.expander("Metric definitions and data assumptions"):
        st.markdown("""
        - **CTR:** clicks ÷ impressions × 100. **CVR:** conversions ÷ clicks × 100.
        - **CPC:** spend ÷ clicks. **CPA:** spend ÷ conversions.
        - **ROAS:** attributed revenue ÷ ad spend.
        - **Ad ROI:** (attributed revenue − ad spend) ÷ ad spend × 100. This excludes product and operating costs, so it is not net profit ROI.
        - Rates use summed numerators and denominators, rather than averages of daily rates. Zero denominators display N/A or a chart gap.
        - One row represents one campaign on one day. Each campaign has a single platform, audience and goal.
        - Sample conversions represent tracked actions: purchases, leads or engagement actions depending on the goal. Lead and awareness campaigns have zero attributed revenue in this sample.
        - Sample data is fictional, single-currency USD, and uses same-day reporting. Real data should use consistent attribution windows and deduplicated conversions.
        """)
