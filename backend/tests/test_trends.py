import unittest

from app.trends import compute_trend


class TrendTests(unittest.TestCase):
    def test_rising_blood_pressure_matches_seed_data(self):
        values = [128, 129, 129, 131, 132, 132, 134, 135, 136, 137]
        trend = compute_trend(values, "mmHg", "Systolic blood pressure", 10)
        self.assertEqual(trend.direction, "rising")
        self.assertEqual(trend.change, 9)
        self.assertEqual(trend.summary, "Systolic blood pressure up 9 mmHg over 10 days")

    def test_falling(self):
        trend = compute_trend([140, 138, 134, 131], "mmHg", "Systolic blood pressure", 4)
        self.assertEqual(trend.direction, "falling")

    def test_stable_within_threshold(self):
        trend = compute_trend([120, 121, 122, 123], "mmHg", "Systolic blood pressure", 4)
        self.assertEqual(trend.direction, "stable")

    def test_not_enough_data(self):
        trend = compute_trend([120, 130], "mmHg", "Systolic blood pressure", 2)
        self.assertEqual(trend.direction, "not_enough_data")
        self.assertIsNone(trend.change)


if __name__ == "__main__":
    unittest.main()
