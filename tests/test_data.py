"""Validation tests protect the daily campaign data contract."""

import io
import unittest

import pandas as pd

from campaign_analyzer.data import load_data, validate_data
from tests.helpers import campaign_data


class DataTests(unittest.TestCase):
    def test_load_preserves_leading_zero_identifiers(self):
        loaded = load_data(io.StringIO(campaign_data().to_csv(index=False)))
        self.assertEqual(loaded.campaign_id.iloc[0], "001")

    def test_validation_does_not_mutate_input(self):
        original = campaign_data()
        validate_data(original)
        self.assertEqual(original.date.iloc[0], "2026-07-05")

    def test_invalid_inputs_are_rejected(self):
        cases = {}
        cases["missing column"] = campaign_data().drop(columns="spend")
        cases["empty"] = campaign_data().iloc[:0]
        cases["duplicate"] = pd.concat([campaign_data(), campaign_data().iloc[:1]])
        for name, column, value in [
            ("invalid date", "date", "not-a-date"),
            ("missing date", "date", None),
            ("negative", "spend", -1),
            ("infinite", "spend", float("inf")),
            ("missing numeric", "revenue", None),
            ("nonnumeric", "spend", "unknown"),
            ("fractional count", "clicks", 1.5),
            ("blank text", "audience", " "),
            ("clicks above impressions", "clicks", 1001),
            ("conversions above clicks", "conversions", 101),
            ("inconsistent metadata", "platform", "Pinterest"),
        ]:
            frame = campaign_data().astype(object)
            frame.loc[0, column] = value
            cases[name] = frame
        for name, frame in cases.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_data(frame)


if __name__ == "__main__":
    unittest.main()
