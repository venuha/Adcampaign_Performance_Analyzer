"""Regression tests for campaign ranking, funnel counts, and CSV caching."""

import unittest
from unittest.mock import patch

from campaign_analyzer.cache import load_dashboard_data, load_sample_csv
from campaign_analyzer.charts import funnel_chart
from campaign_analyzer.data import load_data, validate_data
from campaign_analyzer.metrics import top_campaigns
from tests.helpers import campaign_data


class ExtensionTests(unittest.TestCase):
    def test_ranking_uses_campaign_totals_not_best_daily_roi(self):
        frame = validate_data(campaign_data())
        result = top_campaigns(frame)
        self.assertEqual(list(result.campaign_id), ["001", "002"])
        self.assertAlmostEqual(result.iloc[0]["Ad ROI (%)"], 100)
        self.assertEqual(result.iloc[1]["Ad ROI (%)"], -100)
        self.assertEqual(len(top_campaigns(frame, 1)), 1)

    def test_zero_spend_is_excluded_from_ranking(self):
        frame = validate_data(campaign_data())
        frame.loc[frame.campaign_id == "001", "spend"] = 0
        self.assertEqual(list(top_campaigns(frame).campaign_id), ["002"])

    def test_funnel_counts_and_retention_match_source(self):
        figure = funnel_chart(validate_data(campaign_data()))
        self.assertEqual(list(figure.data[0].x), [12000, 210, 21])
        self.assertIn("10.0%", figure.data[0].text[2])

    def test_zero_funnel_has_unavailable_retention(self):
        frame = validate_data(campaign_data()).iloc[:0]
        figure = funnel_chart(frame)
        self.assertEqual(list(figure.data[0].x), [0, 0, 0])
        self.assertIn("N/A", figure.data[0].text[1])

    def test_sample_cache_invalidates_on_new_bytes_and_returns_copies(self):
        content = campaign_data().to_csv(index=False).encode()
        load_sample_csv.clear()
        with patch("campaign_analyzer.cache.load_data", wraps=load_data) as reader:
            first = load_sample_csv(content)
            first.loc[0, "spend"] = 9999
            second = load_sample_csv(content)
            self.assertEqual(reader.call_count, 1)
            self.assertEqual(second.spend.iloc[0], 50)
            changed = campaign_data()
            changed.loc[0, "spend"] = 60
            third = load_sample_csv(changed.to_csv(index=False).encode())
            self.assertEqual(reader.call_count, 2)
            self.assertEqual(third.spend.iloc[0], 60)
        load_sample_csv.clear()

    def test_upload_cache_is_content_aware_and_session_scoped(self):
        content = campaign_data().to_csv(index=False).encode()
        with patch("campaign_analyzer.cache.st.session_state", {}):
            with patch("campaign_analyzer.cache.load_data", wraps=load_data) as reader:
                frame = load_dashboard_data(content)
                frame.loc[0, "spend"] = 9999
                self.assertEqual(load_dashboard_data(content).spend.iloc[0], 50)
                self.assertEqual(reader.call_count, 1)
                changed = campaign_data()
                changed.loc[0, "spend"] = 60
                self.assertEqual(
                    load_dashboard_data(changed.to_csv(index=False).encode()).spend.iloc[0], 60
                )
                self.assertEqual(reader.call_count, 2)
        with patch("campaign_analyzer.cache.st.session_state", {}):
            with patch("campaign_analyzer.cache.load_data", wraps=load_data) as reader:
                load_dashboard_data(content)
                self.assertEqual(reader.call_count, 1)


if __name__ == "__main__":
    unittest.main()
