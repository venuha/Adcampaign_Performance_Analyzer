"""Integration tests exercise the actual Streamlit entry point."""

import unittest

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
        self.assertEqual(set(self.app.dataframe[1].value.platform), {"Facebook"})
        self.assertEqual(set(self.app.dataframe[3].value.platform), {"Facebook"})

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
