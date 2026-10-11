"""A responsive presentation layer without external fonts or UI dependencies."""

import streamlit as st


def apply_theme() -> None:
    """Style native Streamlit controls while preserving their accessibility."""
    st.html("""
    <style>
    .stApp {background: linear-gradient(145deg, #f4f5ff 0%, #f8fafc 48%, #edf9f7 100%);}
    [data-testid="stHeader"] {background: transparent;}
    [data-testid="stMainBlockContainer"] {max-width: 1480px; padding-top: 2rem;}
    [data-testid="stSidebar"] {background: #f0f2ff; border-right: 1px solid #dce0f2;}
    .dashboard-hero {padding: 1.7rem 2rem; border-radius: 24px;
      background: linear-gradient(115deg, #312e81, #6d28d9 60%, #0f766e);
      color: white; box-shadow: 0 12px 32px #312e811c; margin-bottom: .75rem;}
    .dashboard-hero .eyebrow {font-size: .72rem; letter-spacing: .16em;
      font-weight: 700; color: #ddd6fe; margin-bottom: .6rem;}
    .dashboard-hero h1 {color: white; font-size: clamp(1.8rem, 3vw, 2.65rem);
      line-height: 1.15; padding: 0; margin: 0 0 .75rem; font-weight: 750;}
    .dashboard-hero p {color: #ede9fe; margin: 0; max-width: 760px; line-height: 1.6;}
    [data-testid="stMetric"] {background: #ffffff; border: 1px solid #e4e7f2;
      border-top: 4px solid #7c3aed; border-radius: 16px; padding: 1.1rem 1.25rem;
      box-shadow: 0 4px 16px #312e8108; min-height: 116px;}
    [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {border-top-color: #0d9488;}
    [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {border-top-color: #db2777;}
    [data-testid="stMetricLabel"] {color: #475569;}
    [data-testid="stMetricValue"] {color: #312e81; font-weight: 700;
      font-size: clamp(1.65rem, 2.5vw, 2.3rem);}
    [data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"] {
      background: #ffffff; border: 1px solid #e4e7f2; border-radius: 18px;
      padding: .4rem; box-shadow: 0 4px 16px #312e8106;}
    [data-testid="stDataFrame"] {border: 1px solid #e4e7f2; border-radius: 14px;}
    [data-baseweb="tab-list"] {gap: .5rem; padding: .35rem; border-radius: 14px;
      background: #e9ecf7; margin: .5rem 0 1rem;}
    [data-baseweb="tab"] {border-radius: 10px; padding: .6rem 1rem; height: auto;}
    [data-baseweb="tab"][aria-selected="true"] {background: white; color: #6d28d9;
      box-shadow: 0 2px 8px #312e8112;}
    [data-testid="stButton"] button, [data-testid="stDownloadButton"] button {
      border-radius: 10px; font-weight: 600;}
    @media (max-width: 640px) {
      .dashboard-hero {padding: 1.3rem; border-radius: 18px;}
      [data-testid="stMainBlockContainer"] {padding: 3.5rem 1rem 1rem;}
      [data-baseweb="tab"] {padding: .6rem .75rem;}
    }
    </style>
    """)


def render_hero() -> None:
    """Render static product branding; CSV values never enter raw HTML."""
    st.html("""
    <section class="dashboard-hero" aria-label="Dashboard introduction">
      <div class="eyebrow">CAMPAIGN INTELLIGENCE · USD</div>
      <h1>Ad Campaign Performance Analyzer</h1>
      <p>Turn campaign data into your next move. Compare channels, follow the funnel,
      and discover where your advertising spend delivers results.</p>
    </section>
    """)
