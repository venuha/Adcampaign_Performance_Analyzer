"""Dataset schema, labels, and repository-relative asset paths."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample_campaign_data.csv"
DIMENSIONS = ["campaign_id", "campaign_name", "platform", "audience", "campaign_goal"]
MEASURES = ["impressions", "clicks", "conversions", "spend", "revenue"]
REQUIRED = ["date", *DIMENSIONS, *MEASURES]
DERIVED_METRICS = ["CTR (%)", "CVR (%)", "CPC (USD)", "CPA (USD)", "ROAS (x)", "Ad ROI (%)"]
METRIC_LABELS = {
    "spend": "Spend (USD)",
    "revenue": "Revenue (USD)",
    "impressions": "Impressions",
    "clicks": "Clicks",
    "conversions": "Conversions",
}
