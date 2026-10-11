"""Interactive channel comparisons with consistent platform colors."""

import altair as alt
import pandas as pd

from campaign_analyzer.charts import PLATFORM_COLORS
from campaign_analyzer.config import METRIC_LABELS


def channel_comparison(summary: pd.DataFrame, measure: str) -> alt.Chart:
    """Highlight channels from the legend without changing global filters."""
    label = METRIC_LABELS.get(measure, measure)
    selection = alt.selection_point(fields=["platform"], bind="legend")
    return (
        alt.Chart(summary)
        .mark_bar(cornerRadiusEnd=8, size=38)
        .encode(
            x=alt.X(f"{measure}:Q", title=label),
            y=alt.Y("platform:N", title=None, sort="-x"),
            color=alt.Color(
                "platform:N",
                scale=alt.Scale(domain=list(PLATFORM_COLORS), range=list(PLATFORM_COLORS.values())),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
            tooltip=[
                alt.Tooltip("platform:N", title="Platform"),
                alt.Tooltip(f"{measure}:Q", title=label, format=",.2f"),
            ],
        )
        .add_params(selection)
        .properties(height=280, title=f"{label} by platform")
        .configure_view(stroke=None)
        .configure_axis(gridColor="#edf0f7", labelColor="#475569", titleColor="#475569")
        .configure_title(anchor="start", color="#1e1b4b", fontSize=18, offset=20)
    )
