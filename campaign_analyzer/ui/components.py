"""Shared Streamlit chart and table presentation."""

import pandas as pd
import streamlit as st
from plotly.graph_objects import Figure


def chart(fig: Figure) -> None:
    """Render a Plotly chart with consistent sizing and styling."""

    fig.update_layout(template="plotly_white", legend_title_text="", margin=dict(t=45, b=20))
    st.plotly_chart(fig, width="stretch")


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
    config = {
        c: st.column_config.NumberColumn(c, format="%.2f")
        for c in display
        if "USD" in c or "(%)" in c or "(x)" in c
    }
    st.dataframe(display, hide_index=True, width="stretch", column_config=config)
