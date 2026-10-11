"""Plotly figure builders, independent of Streamlit widgets."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from campaign_analyzer.config import METRIC_LABELS

PLATFORM_COLORS = {
    "Facebook": "#6366f1",
    "Instagram": "#ec4899",
    "Pinterest": "#f59e0b",
    "Twitter": "#14b8a6",
}


def spend_conversions_chart(daily: pd.DataFrame) -> go.Figure:
    """Use separate, labelled axes for USD spend and conversion counts."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=daily.date,
            y=daily.spend,
            name="Spend (USD)",
            line=dict(color="#7c3aed", width=3),
            fill="tozeroy",
            fillcolor="rgba(124,58,237,0.07)",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=daily.date,
            y=daily.conversions,
            name="Conversions",
            line=dict(color="#0d9488", width=3),
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
        color_discrete_map=PLATFORM_COLORS,
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
        color_discrete_map=PLATFORM_COLORS,
        markers=True,
        labels={"period_start": "Period start", measure: label},
        title=f"{label} over time",
    )


def funnel_chart(df: pd.DataFrame) -> go.Figure:
    """Show the measured funnel with readable counts and stage retention."""
    values = [int(df[column].sum()) for column in ["impressions", "clicks", "conversions"]]
    stages = ["Impressions", "Clicks", "Conversions"]
    labels = []
    for index, value in enumerate(values):
        if index == 0:
            retention = "starting stage"
        else:
            previous = values[index - 1]
            retention = f"{value / previous:.1%} of prior stage" if previous else "retention N/A"
        labels.append(f"{value:,} ({retention})")
    fig = go.Figure(
        go.Funnel(
            y=stages,
            x=values,
            text=labels,
            textinfo="text",
            textposition="outside",
            textfont=dict(color="#0f172a"),
            marker=dict(color=["#7c3aed", "#6366f1", "#14b8a6"]),
            hovertemplate="%{y}: %{x:,.0f}<extra></extra>",
        )
    )
    # Funnel area shows actual magnitudes; the table beneath preserves readability
    # when a late stage is too small for its in-chart label.
    fig.update_layout(title="Campaign conversion funnel", margin=dict(l=110, r=240), height=350)
    return fig
