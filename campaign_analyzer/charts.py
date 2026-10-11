"""Plotly figure builders, independent of Streamlit widgets."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from campaign_analyzer.config import METRIC_LABELS


def spend_conversions_chart(daily: pd.DataFrame) -> go.Figure:
    """Use separate, labelled axes for USD spend and conversion counts."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=daily.date, y=daily.spend, name="Spend (USD)", line=dict(color="#2563eb")),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=daily.date, y=daily.conversions, name="Conversions", line=dict(color="#059669")
        ),
        secondary_y=True,
    )
    fig.update_layout(title="Daily spend and conversions")
    fig.update_yaxes(title_text="Spend (USD)", secondary_y=False)
    fig.update_yaxes(title_text="Conversions", tickformat=",.0f", secondary_y=True)
    return fig


def platform_chart(summary: pd.DataFrame, measure: str) -> go.Figure:
    """Compare a selected metric across channels."""
    label = METRIC_LABELS.get(measure, measure)
    return px.bar(
        summary.sort_values(measure, ascending=False),
        x="platform",
        y=measure,
        color="platform",
        labels={measure: label, "platform": "Platform"},
        title=f"{label} by platform",
    )


def trend_chart(trend: pd.DataFrame, measure: str) -> go.Figure:
    """Plot chronological channel trends with metric units."""
    label = METRIC_LABELS.get(measure, measure)
    return px.line(
        trend.sort_values("period_start"),
        x="period_start",
        y=measure,
        color="platform",
        markers=True,
        labels={"period_start": "Period start", measure: label},
        title=f"{label} over time",
    )
