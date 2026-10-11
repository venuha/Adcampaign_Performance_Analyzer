"""Independent expectations verify metric definitions and aggregation."""

import math
import unittest

from campaign_analyzer.config import DERIVED_METRICS, MEASURES
from campaign_analyzer.data import validate_data
from campaign_analyzer.metrics import aggregate, metrics
from tests.helpers import campaign_data


class MetricTests(unittest.TestCase):
    def test_metric_definitions(self):
        result = metrics(dict(impressions=1000, clicks=100, conversions=10, spend=50, revenue=150))
        expected = {
            "CTR (%)": 10,
            "CVR (%)": 10,
            "CPC (USD)": 0.5,
            "CPA (USD)": 5,
            "ROAS (x)": 3,
            "Ad ROI (%)": 200,
        }
        for metric, value in expected.items():
            with self.subTest(metric=metric):
                self.assertAlmostEqual(result[metric], value)

    def test_rates_use_grouped_totals(self):
        frame = validate_data(campaign_data())
        result = aggregate(frame, ["platform"]).set_index("platform")
        self.assertAlmostEqual(result.loc["Facebook", "CTR (%)"], 1.9)
        self.assertAlmostEqual(result.loc["Facebook", "ROAS (x)"], 2)
        self.assertEqual(result.loc["Facebook", "conversions"], 19)
        for measure in MEASURES:
            self.assertAlmostEqual(result[measure].sum(), frame[measure].sum())

    def test_zero_denominators_are_unavailable(self):
        result = metrics(dict.fromkeys(MEASURES, 0))
        for metric in DERIVED_METRICS:
            self.assertTrue(math.isnan(result[metric]))

    def test_zero_revenue_is_a_real_loss(self):
        result = metrics(dict(impressions=1000, clicks=100, conversions=0, spend=50, revenue=0))
        self.assertEqual(result["Ad ROI (%)"], -100)
        self.assertEqual(result["ROAS (x)"], 0)
        self.assertTrue(math.isnan(result["CPA (USD)"]))

    def test_empty_aggregation_preserves_schema(self):
        result = aggregate(validate_data(campaign_data()).iloc[:0], ["platform"])
        self.assertTrue(result.empty)
        self.assertIn("ROAS (x)", result.columns)


if __name__ == "__main__":
    unittest.main()
