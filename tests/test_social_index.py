import unittest
from fractions import Fraction

from szondi3.profile import build_profile
from szondi3.proportions import social_character, social_index
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def reaction(factor, kind="null", quantum=0):
    base = {
        "null": "0",
        "positive": "+",
        "negative": "-",
        "ambivalent": "±",
    }[kind]
    symbol = base + ("!" * quantum)
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=symbol,
        quantum_level=quantum,
    )


def profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


class SocialIndexTests(unittest.TestCase):
    def test_visual_inventory_has_all_64_vector_reaction_classifications(self):
        symbols = ("0", "±", "+", "-")
        for vector in ("S", "P", "Sch", "C"):
            observed = {
                (first, second): social_character(vector, first, second)
                for first in symbols
                for second in symbols
            }
            self.assertEqual(len(observed), 16)
            self.assertEqual(set(observed.values()), {"+", "-"})

    def test_source_matrix_spot_checks_from_abb_24(self):
        self.assertEqual(social_character("S", "+", "+"), "+")
        self.assertEqual(social_character("S", "+", "-"), "-")
        self.assertEqual(social_character("P", "0", "±"), "+")
        self.assertEqual(social_character("Sch", "0", "0"), "-")
        self.assertEqual(social_character("C", "-", "+"), "+")
        self.assertEqual(social_character("C", "-", "-"), "-")

    def test_all_null_eight_series_yields_exact_fifty_percent(self):
        # Abb. 24 classifies 00 as soz+ in S and C, soz- in P and Sch.
        series = ProfileSeries(tuple(profile() for _ in range(8)))

        result = social_index(series)

        self.assertEqual(result.total_positive, 16)
        self.assertEqual(result.total_negative, 16)
        self.assertEqual(result.positive_percentage, Fraction(50, 1))
        self.assertEqual(result.negative_percentage, Fraction(50, 1))
        self.assertEqual(
            tuple((item.vector, item.positive_reactions, item.negative_reactions) for item in result.vectors),
            (("S", 8, 0), ("P", 0, 8), ("Sch", 0, 8), ("C", 8, 0)),
        )

    def test_all_quantum_marks_are_added_to_socially_negative_side(self):
        # S++ itself is soz+, but two exclamation marks per profile are added
        # to soz- independently of that base classification.
        series = ProfileSeries(
            tuple(
                profile({"h": ("positive", 1), "s": ("positive", 1)})
                for _ in range(8)
            )
        )

        result = social_index(series)

        sexual = result.vectors[0]
        self.assertEqual(sexual.positive_reactions, 8)
        self.assertEqual(sexual.negative_reactions, 0)
        self.assertEqual(sexual.negative_quantum, 16)
        self.assertEqual(result.total_positive, 16)
        self.assertEqual(result.total_negative, 32)
        self.assertEqual(result.positive_percentage, Fraction(100, 3))
        self.assertEqual(result.negative_percentage, Fraction(200, 3))

    def test_eight_nine_and_ten_profile_series_are_admitted(self):
        for count in (8, 9, 10):
            result = social_index(ProfileSeries(tuple(profile() for _ in range(count))))
            self.assertEqual(result.total_positive + result.total_negative, 4 * count)

    def test_other_profile_counts_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "eight to ten profiles"):
            social_index(ProfileSeries(tuple(profile() for _ in range(7))))

    def test_unknown_vector_and_reaction_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "Unknown vector"):
            social_character("X", "0", "0")
        with self.assertRaisesRegex(ValueError, "Unsupported base vector reaction"):
            social_character("S", "?", "0")


if __name__ == "__main__":
    unittest.main()
