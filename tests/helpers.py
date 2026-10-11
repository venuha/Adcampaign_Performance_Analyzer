"""Small fictional datasets used by the unit tests."""

import pandas as pd


def campaign_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "date": "2026-07-05",
                "campaign_id": "001",
                "campaign_name": "Summer [sale]",
                "platform": "Facebook",
                "audience": "New customers",
                "campaign_goal": "Sales",
                "impressions": 1000,
                "clicks": 100,
                "conversions": 10,
                "spend": 50,
                "revenue": 150,
            },
            {
                "date": "2026-07-06",
                "campaign_id": "001",
                "campaign_name": "Summer [sale]",
                "platform": "Facebook",
                "audience": "New customers",
                "campaign_goal": "Sales",
                "impressions": 9000,
                "clicks": 90,
                "conversions": 9,
                "spend": 150,
                "revenue": 250,
            },
            {
                "date": "2026-07-06",
                "campaign_id": "002",
                "campaign_name": "Lead signup",
                "platform": "Instagram",
                "audience": "Returning customers",
                "campaign_goal": "Leads",
                "impressions": 2000,
                "clicks": 20,
                "conversions": 2,
                "spend": 100,
                "revenue": 0,
            },
        ]
    )
