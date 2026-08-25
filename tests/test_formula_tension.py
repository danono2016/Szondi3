import unittest

from szondi3.formula import factor_tension_levels, formula_factor_tensions
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


REACTIONS = {
    "null": (0, 0, "0"),
    "positive": (2, 0, "+"),
}


def profile_with_kinds(kinds):
    reactions = []
    for factor, kind in zip(FACTORS, kinds):
        sympathetic, unsympathetic, symbol = REACTIONS[kind]
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


class FormulaFactorTensionTests(unittest.TestCase):
    def test_fall_11_factor_tensions_and_equality_levels(self):
        # Lehrbuch Fall 11 raw TspG row already established in the P1 series tests:
        # h=2, s=1, e=4, hy=2, k=5, p=4, d=5, m=8.
        series = series_from_degrees((2, 1, 4, 2, 5, 4, 5, 8), 10)

        tensions = formula_factor_tensions(series)
        self.assertEqual(
            tuple((item.factor, item.raw_degree, item.ten_base_degree) for item in tensions),
            (
                ("h", 2, 2),
                ("s", 1, 1),
                ("e", 4, 4),
                ("hy", 2, 2),
                ("k", 5, 5),
                ("p", 4, 4),
                ("d", 5, 5),
                ("m", 8, 8),
            ),
        )

        levels = factor_tension_levels(series)
        self.assertEqual(
            tuple(
                (level.degree, tuple(item.factor for item in level.factors))
                for level in levels
            ),
            (
                (8, ("m",)),
                (5, ("k", "d")),
                (4, ("e", "p")),
                (2, ("h", "hy")),
                (1, ("s",)),
            ),
        )

    def test_short_series_uses_tabelle_13_for_formula_numbers(self):
        # Six profiles: raw values 3, 2, 1 normalize to 5, 3, 2.
        series = series_from_degrees((3, 2, 1, 0, 0, 0, 0, 0), 6)
        by_factor = {item.factor: item for item in formula_factor_tensions(series)}

        self.assertEqual(
            (by_factor["h"].raw_degree, by_factor["h"].ten_base_degree),
            (3, 5),
        )
        self.assertEqual(
            (by_factor["s"].raw_degree, by_factor["s"].ten_base_degree),
            (2, 3),
        )
        self.assertEqual(
            (by_factor["e"].raw_degree, by_factor["e"].ten_base_degree),
            (1, 2),
        )

    def test_formula_tension_requires_at_least_three_profiles(self):
        series = series_from_degrees((1, 0, 0, 0, 0, 0, 0, 0), 2)

        with self.assertRaisesRegex(ValueError, "at least three profiles"):
            formula_factor_tensions(series)


if __name__ == "__main__":
    unittest.main()
