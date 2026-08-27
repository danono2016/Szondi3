import unittest

from szondi3.abbreviated_formula import (
    abbreviated_fraction_candidates_from_tensions,
    extended_abbreviated_formula,
    unique_abbreviated_formula_fraction,
)
from szondi3.formula import FormulaFactorTension
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def tension(factor, raw_degree, decision_degree=None):
    return FormulaFactorTension(
        factor=factor,
        raw_degree=raw_degree,
        ten_base_degree=raw_degree if decision_degree is None else decision_degree,
    )


def pairs(fractions):
    return tuple((item.numerator_factor, item.denominator_factor) for item in fractions)


def series_from_degrees(degrees, profile_count):
    profiles = []
    for profile_index in range(profile_count):
        reactions = []
        for factor, degree in zip(FACTORS, degrees):
            if profile_index < degree:
                sympathetic, unsympathetic, kind, symbol = 0, 0, "null", "0"
            else:
                sympathetic, unsympathetic, kind, symbol = 2, 0, "positive", "+"
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
        profiles.append(build_profile(reactions))
    return ProfileSeries(tuple(profiles))


class AbbreviatedFormulaTests(unittest.TestCase):
    def test_fall_11_printed_simple_abbreviation_is_m_over_s(self):
        tensions = (
            tension("m", 8), tension("d", 5), tension("k", 5), tension("p", 4),
            tension("e", 4), tension("hy", 2), tension("h", 2), tension("s", 1),
        )
        self.assertEqual(pairs(abbreviated_fraction_candidates_from_tensions(tensions)), (("m", "s"),))

    def test_fall_16_tied_roots_are_preserved_only_as_candidates(self):
        tensions = (
            tension("e", 7), tension("hy", 3), tension("h", 1), tension("s", 1),
            tension("p", 1), tension("k", 1), tension("d", 0), tension("m", 0),
        )
        self.assertEqual(
            pairs(abbreviated_fraction_candidates_from_tensions(tensions)),
            (("e", "d"), ("e", "m")),
        )

    def test_fall_18_simple_fraction_is_k_over_s_after_short_series_conversion(self):
        tensions = (
            tension("k", 5, 8), tension("p", 4, 7), tension("m", 3, 5), tension("d", 3, 5),
            tension("hy", 2, 3), tension("e", 2, 3), tension("h", 1, 2), tension("s", 0, 0),
        )
        result = abbreviated_fraction_candidates_from_tensions(tensions)
        self.assertEqual(pairs(result), (("k", "s"),))
        self.assertEqual(result[0].symptomatic.display_degree, 5)
        self.assertEqual(result[0].root.display_degree, 0)

    def test_fall_18_extended_abbreviation_projects_outer_complete_formula_lines(self):
        # FACTORS source order is h,s,e,hy,k,p,d,m. Raw six-profile TspG values
        # 1,0,2,2,5,4,3,3 normalize to 2,0,3,3,8,7,5,5 and uniquely yield
        # complete lines kp / mdhye / hs. Extended abbreviation omits the middle.
        series = series_from_degrees((1, 0, 2, 2, 5, 4, 3, 3), 6)
        result = extended_abbreviated_formula(series)

        self.assertEqual(result.numerator_factors, ("k", "p"))
        self.assertEqual(result.denominator_factors, ("h", "s"))
        self.assertEqual(result.notation, "kp/hs")

    def test_extended_abbreviation_does_not_assume_two_factors_per_outer_line(self):
        # Fall 11 complete lines are m / dkpe / hyhs. The structural projection
        # therefore has one symptomatic factor and three root factors; the middle
        # factors are absent. This is not asserted to be a separately printed Fall
        # 11 abbreviation, only the project-resolved outer-line projection.
        series = series_from_degrees((2, 1, 4, 2, 5, 4, 5, 8), 10)
        result = extended_abbreviated_formula(series)

        self.assertEqual(result.numerator_factors, ("m",))
        self.assertEqual(result.denominator_factors, ("hy", "h", "s"))
        self.assertEqual(result.notation, "m/hyhs")
        self.assertTrue({"d", "k", "p", "e"}.isdisjoint(result.numerator_factors + result.denominator_factors))

    def test_equal_maxima_and_minima_are_candidates_not_an_authoritative_tie_rule(self):
        tensions = (
            tension("k", 5), tension("p", 5), tension("h", 0), tension("s", 0),
        )
        self.assertEqual(
            pairs(abbreviated_fraction_candidates_from_tensions(tensions)),
            (("k", "h"), ("k", "s"), ("p", "h"), ("p", "s")),
        )

    def test_unique_entry_point_fails_closed_for_tied_extrema(self):
        # Fall 16 has one maximal TspG factor (e) and two tied roots (d, m).
        # The source prints both fractions for that case but does not justify a
        # universal selector for arbitrary ties, so the unique entry point must
        # refuse to invent one.
        series = series_from_degrees((1, 1, 7, 3, 1, 1, 0, 0), 10)
        with self.assertRaisesRegex(ValueError, "tied extrema require"):
            unique_abbreviated_formula_fraction(series)

    def test_empty_tension_set_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "at least one factor tension"):
            abbreviated_fraction_candidates_from_tensions(())


if __name__ == "__main__":
    unittest.main()
