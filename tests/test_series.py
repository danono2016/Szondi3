import unittest

from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries, ten_base_count
from szondi3.stimuli import FACTORS


TABLE_13 = {
    3: {1: 3, 2: 7, 3: 10},
    4: {1: 2, 2: 5, 3: 7, 4: 10},
    5: {1: 2, 2: 4, 3: 6, 4: 8, 5: 10},
    6: {1: 2, 2: 3, 3: 5, 4: 7, 5: 8, 6: 10},
    7: {1: 1, 2: 3, 3: 4, 4: 6, 5: 7, 6: 9, 7: 10},
    8: {1: 1, 2: 2, 3: 4, 4: 5, 5: 6, 6: 7, 7: 9, 8: 10},
    9: {1: 1, 2: 2, 3: 3, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10},
}


def null_profile():
    reactions = [
        FactorReaction(
            factor=factor,
            sympathetic=0,
            unsympathetic=0,
            kind="null",
            symbol="0",
            quantum_level=0,
        )
        for factor in FACTORS
    ]
    return build_profile(reactions)


class ProfileSeriesTests(unittest.TestCase):
    def test_series_preserves_order_and_accepts_one_to_ten_profiles(self):
        profile = null_profile()
        for count in range(1, 11):
            with self.subTest(count=count):
                series = ProfileSeries(tuple(profile for _ in range(count)))
                self.assertEqual(len(series.profiles), count)
                self.assertEqual(series.profile_count, count)
                self.assertEqual(series.is_ten_series, count == 10)
                self.assertEqual(series.supports_linnaeus_evaluation, count >= 3)

    def test_series_rejects_empty_or_more_than_ten_profiles(self):
        profile = null_profile()
        with self.assertRaises(ValueError):
            ProfileSeries(())
        with self.assertRaises(ValueError):
            ProfileSeries(tuple(profile for _ in range(11)))

    def test_table_13_all_source_entries(self):
        for profile_count, row in TABLE_13.items():
            for observed_count, expected in row.items():
                with self.subTest(profile_count=profile_count, observed_count=observed_count):
                    self.assertEqual(ten_base_count(profile_count, observed_count), expected)

    def test_zero_and_full_ten_series_are_identity_cases(self):
        for profile_count in range(3, 11):
            self.assertEqual(ten_base_count(profile_count, 0), 0)
        for observed_count in range(0, 11):
            self.assertEqual(ten_base_count(10, observed_count), observed_count)

    def test_ten_base_conversion_fails_outside_source_domain(self):
        invalid = [(2, 1), (11, 1), (3, -1), (3, 4), (10, 11)]
        for profile_count, observed_count in invalid:
            with self.subTest(profile_count=profile_count, observed_count=observed_count):
                with self.assertRaises(ValueError):
                    ten_base_count(profile_count, observed_count)


if __name__ == "__main__":
    unittest.main()
