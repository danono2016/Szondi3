import unittest

from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries, latency_statuses
from szondi3.stimuli import FACTORS


REACTION_FIXTURES = {
    "null": (0, 0, "0"),
    "positive": (2, 0, "+"),
    "ambivalent": (2, 2, "±"),
}


def profile_with_kinds(kinds):
    reactions = []
    for factor, kind in zip(FACTORS, kinds):
        sympathetic, unsympathetic, symbol = REACTION_FIXTURES[kind]
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


def series_from_degrees(degrees, profile_count):
    profiles = []
    for profile_index in range(profile_count):
        kinds = [
            "null" if profile_index < degree else "positive"
            for degree in degrees
        ]
        profiles.append(profile_with_kinds(kinds))
    return ProfileSeries(tuple(profiles))


class LatencyStatusTests(unittest.TestCase):
    def test_ten_series_boundary_five_is_gefahr_four_is_ventil(self):
        # TspG pairs produce TspD S=5, P=4, Sch=6, C=0.
        series = series_from_degrees((5, 0, 4, 0, 7, 1, 2, 2), 10)
        statuses = {item.vector: item for item in latency_statuses(series)}

        self.assertEqual((statuses["S"].raw_magnitude, statuses["S"].ten_base_magnitude), (5, 5))
        self.assertEqual(statuses["S"].status, "danger")
        self.assertEqual(statuses["P"].ten_base_magnitude, 4)
        self.assertEqual(statuses["P"].status, "ventil")
        self.assertEqual(statuses["Sch"].ten_base_magnitude, 6)
        self.assertEqual(statuses["Sch"].status, "danger")
        self.assertEqual(statuses["C"].status, "ventil")

    def test_short_series_uses_tabelle_13_before_threshold(self):
        # With six profiles, Tabelle 13 maps raw 3 -> 5 and raw 2 -> 3.
        series = series_from_degrees((3, 0, 2, 0, 1, 0, 0, 0), 6)
        statuses = {item.vector: item for item in latency_statuses(series)}

        self.assertEqual((statuses["S"].raw_magnitude, statuses["S"].ten_base_magnitude), (3, 5))
        self.assertEqual(statuses["S"].status, "danger")
        self.assertEqual((statuses["P"].raw_magnitude, statuses["P"].ten_base_magnitude), (2, 3))
        self.assertEqual(statuses["P"].status, "ventil")

    def test_fall_18_is_four_ventile_after_conversion(self):
        # Fall 18 has six profiles and raw TspG h=1,s=0,e=2,hy=2,k=5,p=4,d=3,m=3.
        # Its four raw TspD are 1,0,1,0; Tabelle 13 maps 1 -> 2 for six profiles.
        series = series_from_degrees((1, 0, 2, 2, 5, 4, 3, 3), 6)
        statuses = latency_statuses(series)

        self.assertEqual(tuple(item.raw_magnitude for item in statuses), (1, 0, 1, 0))
        self.assertEqual(tuple(item.ten_base_magnitude for item in statuses), (2, 0, 2, 0))
        self.assertEqual(tuple(item.status for item in statuses), ("ventil",) * 4)

    def test_status_requires_at_least_three_profiles(self):
        profile = profile_with_kinds(["positive"] * 8)
        for count in (1, 2):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    latency_statuses(ProfileSeries(tuple(profile for _ in range(count))))


if __name__ == "__main__":
    unittest.main()
