"""Integration tests exercise the actual Streamlit entry point."""

import unittest
from datetime import date

from streamlit.testing.v1 import AppTest

from campaign_analyzer.config import PROJECT_ROOT, SAMPLE_DATA_PATH
from campaign_analyzer.data import load_data


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(str(PROJECT_ROOT / "app.py"), default_timeout=30).run()

    def test_all_views_render(self):
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.tabs), 4)
        self.assertEqual(len(self.app.metric), 6)

    def test_shared_platform_filter_updates_totals(self):
        self.app.multiselect[0].set_value(["Facebook"]).run()
        self.assertFalse(self.app.exception)
        frame = load_data(SAMPLE_DATA_PATH)
        expected = frame[frame.platform == "Facebook"].spend.sum()
        self.assertEqual(self.app.metric[0].value, f"${expected:,.0f}")
        # Platform summary and time-series table use the same filtered channel.
        frames = [item.value for item in self.app.dataframe if "platform" in item.value.columns]
        self.assertEqual(len(frames), 4)
        for frame in frames:
            self.assertEqual(set(frame.platform), {"Facebook"})

    def test_reset_restores_all_filters_after_empty_results(self):
        self.app.date_input[0].set_value((date(2026, 7, 2), date(2026, 8, 2))).run()
        self.app.multiselect[0].set_value([]).run()
        self.app.multiselect[1].set_value(["New customers"]).run()
        self.app.multiselect[2].set_value(["Sales"]).run()
        reset = next(button for button in self.app.button if button.label == "Reset Filters")
        reset.click().run()
        self.assertFalse(self.app.exception)
        self.assertFalse(self.app.warning)
        self.assertEqual(len(self.app.multiselect[0].value), 4)
        self.assertEqual(len(self.app.multiselect[1].value), 3)
        self.assertEqual(len(self.app.multiselect[2].value), 3)
        self.assertEqual(len(self.app.metric), 6)
        self.assertEqual(self.app.date_input[0].value, (date(2026, 7, 1), date(2026, 9, 28)))

    def test_new_analysis_sections_render(self):
        titles = [item.value for item in self.app.subheader]
        self.assertIn("Top 5 campaigns by Ad ROI", titles)
        self.assertIn("Campaign funnel", titles)

    def test_empty_filters_show_message(self):
        self.app.multiselect[0].set_value([]).run()
        self.assertFalse(self.app.exception)
        self.assertTrue(
            any("No campaigns match these filters" in item.value for item in self.app.warning)
        )

    def test_search_and_time_intervals(self):
        for interval in ["Weekly", "Monthly"]:
            self.app.selectbox[1].select(interval).run()
            self.assertFalse(self.app.exception)
        self.app.text_input[0].set_value("unmatched campaign").run()
        self.assertTrue(
            any("No campaigns match your search" in item.value for item in self.app.info)
        )


if __name__ == "__main__":
    unittest.main()
