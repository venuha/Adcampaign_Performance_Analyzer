"""Shared Streamlit chart and table presentation."""

import pandas as pd
import streamlit as st
from plotly.graph_objects import Figure


def chart(fig: Figure) -> None:
    """Render a Plotly chart with consistent sizing and styling."""

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Arial, sans-serif", color="#475569", size=12),
        title_font=dict(size=18, color="#1e1b4b"),
        legend=dict(orientation="h", y=-0.2, x=0),
        legend_title_text="",
        margin=dict(t=65, b=60),
        hoverlabel=dict(bgcolor="#1e1b4b", font_color="#ffffff"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#edf0f7", zerolinecolor="#cbd5e1")
    st.plotly_chart(fig, width="stretch", theme=None)


def table(frame: pd.DataFrame) -> None:
    """Display counts, currencies and rates with readable formatting."""
    display = frame.rename(
        columns={
            "spend": "Spend (USD)",
            "revenue": "Revenue (USD)",
            "impressions": "Impressions",
            "clicks": "Clicks",
            "conversions": "Conversions",
        }
    )
    display = display.rename(
        columns={
            "campaign_id": "Campaign ID",
            "campaign_name": "Campaign",
            "campaign_goal": "Goal",
            "audience": "Audience",
        }
    )
    config = {
        c: st.column_config.NumberColumn(c, format="%.2f")
        for c in display
        if "USD" in c or "(%)" in c or "(x)" in c
    }
    st.dataframe(display, hide_index=True, width="stretch", column_config=config)
