"""Filters, search, and time boundaries have no Streamlit dependency."""

import unittest
from datetime import date

from campaign_analyzer.config import DIMENSIONS
from campaign_analyzer.data import validate_data
from campaign_analyzer.filters import filter_data, search_campaigns, time_series
from campaign_analyzer.metrics import aggregate
from tests.helpers import campaign_data


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.frame = validate_data(campaign_data())

    def test_date_range_is_inclusive_and_filters_combine(self):
        selected = {
            "platform": ["Facebook"],
            "audience": ["New customers"],
            "campaign_goal": ["Sales"],
        }
        result = filter_data(self.frame, date(2026, 7, 6), date(2026, 7, 6), selected)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.spend.sum(), 150)

    def test_empty_selection_returns_no_rows(self):
        self.assertTrue(
            filter_data(self.frame, date(2026, 7, 5), date(2026, 7, 6), {"platform": []}).empty
        )

    def test_search_is_literal_and_case_insensitive(self):
        details = aggregate(self.frame, DIMENSIONS)
        self.assertEqual(len(search_campaigns(details, "[SALE]")), 1)
        self.assertEqual(len(search_campaigns(details, "002")), 1)
        self.assertEqual(len(search_campaigns(details, "")), 2)

    def test_week_changes_on_monday(self):
        result = time_series(self.frame, "Weekly")
        self.assertEqual(
            set(result.period_start.dt.strftime("%Y-%m-%d")), {"2026-06-29", "2026-07-06"}
        )
        self.assertEqual(result.spend.sum(), 300)

    def test_monthly_totals_reconcile(self):
        result = time_series(self.frame, "Monthly")
        self.assertEqual(result.spend.sum(), 300)
        self.assertEqual(result.period_start.iloc[0].date(), date(2026, 7, 1))

    def test_unsupported_interval_fails_clearly(self):
        with self.assertRaises(ValueError):
            time_series(self.frame, "Yearly")


if __name__ == "__main__":
    unittest.main()
