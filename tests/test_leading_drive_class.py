import unittest

from szondi3.linnaeus import leading_drive_classes
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def profile_with_kinds(kinds):
    reactions = []
    for factor, kind in zip(FACTORS, kinds):
        if kind == "null":
            sympathetic, unsympathetic, symbol = 0, 0, "0"
        else:
            sympathetic, unsympathetic, symbol = 2, 0, "+"
        reactions.append(
            FactorReaction(
                factor=factor,
                sympathetic=sympathetic,
                unsympathetic=unsympathetic,
                kind=kind,
                symbol=symbol,
                quantum_level=0,
            )
        )
    return build_profile(reactions)


def series_from_degrees(degrees, profile_count=10):
    profiles = []
    for profile_index in range(profile_count):
        kinds = [
            "null" if profile_index < degree else "positive"
            for degree in degrees
        ]
        profiles.append(profile_with_kinds(kinds))
    return ProfileSeries(tuple(profiles))


class LeadingDriveClassTests(unittest.TestCase):
    def test_unique_greatest_latency_yields_one_haupttriebklasse(self):
        # S: h=0, s=8 -> Sh=8; P=2, Sch=1, C=0.
        series = series_from_degrees((0, 8, 0, 2, 0, 1, 0, 0))
        leaders = leading_drive_classes(series)

        self.assertEqual(tuple(item.designation for item in leaders), ("Sh",))
        self.assertEqual(leaders[0].status.ten_base_magnitude, 8)

    def test_equal_highest_latencies_preserve_both_leading_classes(self):
        # Source all-Ventil pattern: two relatively highest latencies must not be
        # collapsed to an arbitrary single class. Here Sh=4 and Schk=4.
        series = series_from_degrees((0, 4, 1, 0, 0, 4, 0, 0))
        leaders = leading_drive_classes(series)

        self.assertEqual(
            tuple(item.designation for item in leaders),
            ("Sh", "Schk"),
        )
        self.assertEqual(
            tuple(item.status.ten_base_magnitude for item in leaders),
            (4, 4),
        )

    def test_short_series_uses_ten_series_normalization_before_leading_class(self):
        # Six profiles: raw S=3 -> 5, raw P=2 -> 3 under Tabelle 13.
        series = series_from_degrees((0, 3, 0, 2, 0, 1, 0, 0), profile_count=6)
        leaders = leading_drive_classes(series)

        self.assertEqual(tuple(item.designation for item in leaders), ("Sh",))
        self.assertEqual(leaders[0].status.raw_magnitude, 3)
        self.assertEqual(leaders[0].status.ten_base_magnitude, 5)

    def test_all_zero_vector_differences_fail_closed(self):
        series = series_from_degrees((2, 2, 2, 2, 2, 2, 2, 2))

        with self.assertRaisesRegex(ValueError, "all four vectorial TspD values are zero"):
            leading_drive_classes(series)


if __name__ == "__main__":
    unittest.main()
