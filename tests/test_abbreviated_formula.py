import unittest

from szondi3.abbreviated_formula import abbreviated_fractions_from_tensions
from szondi3.formula import FormulaFactorTension


def tension(factor, raw_degree, decision_degree=None):
    return FormulaFactorTension(
        factor=factor,
        raw_degree=raw_degree,
        ten_base_degree=raw_degree if decision_degree is None else decision_degree,
    )


def pairs(fractions):
    return tuple((item.numerator_factor, item.denominator_factor) for item in fractions)


class AbbreviatedFormulaTests(unittest.TestCase):
    def test_fall_11_printed_simple_abbreviation_is_m_over_s(self):
        tensions = (
            tension("m", 8),
            tension("d", 5),
            tension("k", 5),
            tension("p", 4),
            tension("e", 4),
            tension("hy", 2),
            tension("h", 2),
            tension("s", 1),
        )

        self.assertEqual(pairs(abbreviated_fractions_from_tensions(tensions)), (("m", "s"),))

    def test_fall_16_preserves_equal_root_extrema_as_two_printed_fractions(self):
        tensions = (
            tension("e", 7),
            tension("hy", 3),
            tension("h", 1),
            tension("s", 1),
            tension("p", 1),
            tension("k", 1),
            tension("d", 0),
            tension("m", 0),
        )

        self.assertEqual(
            pairs(abbreviated_fractions_from_tensions(tensions)),
            (("e", "d"), ("e", "m")),
        )

    def test_fall_18_simple_fraction_is_k_over_s_after_short_series_conversion(self):
        # Six-profile raw values 5,4,3,3,2,2,1,0 map through Tabelle 13 to
        # 8,7,5,5,3,3,2,0. The extrema remain k and s, matching the first
        # printed abbreviated fraction k/s. The additional printed kp/hs variant
        # is intentionally not inferred by this primitive.
        tensions = (
            tension("k", 5, 8),
            tension("p", 4, 7),
            tension("m", 3, 5),
            tension("d", 3, 5),
            tension("hy", 2, 3),
            tension("e", 2, 3),
            tension("h", 1, 2),
            tension("s", 0, 0),
        )

        result = abbreviated_fractions_from_tensions(tensions)

        self.assertEqual(pairs(result), (("k", "s"),))
        self.assertEqual(result[0].symptomatic.display_degree, 5)
        self.assertEqual(result[0].root.display_degree, 0)

    def test_equal_maxima_and_minima_generate_all_simple_tie_combinations(self):
        tensions = (
            tension("k", 5),
            tension("p", 5),
            tension("h", 0),
            tension("s", 0),
        )

        self.assertEqual(
            pairs(abbreviated_fractions_from_tensions(tensions)),
            (("k", "h"), ("k", "s"), ("p", "h"), ("p", "s")),
        )

    def test_empty_tension_set_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "at least one factor tension"):
            abbreviated_fractions_from_tensions(())


if __name__ == "__main__":
    unittest.main()
