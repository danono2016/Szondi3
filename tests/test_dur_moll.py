import unittest
from fractions import Fraction

from szondi3.profile import build_profile
from szondi3.proportions import dur_moll_character, dur_moll_index
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


class DurMollTests(unittest.TestCase):
    def test_visual_inventory_has_all_64_vector_reaction_classifications(self):
        symbols = ("0", "±", "+", "-")
        for vector in ("S", "P", "Sch", "C"):
            observed = {
                (first, second): dur_moll_character(vector, first, second)
                for first in symbols
                for second in symbols
            }
            self.assertEqual(len(observed), 16)
            self.assertEqual(set(observed.values()), {"D", "M"})

    def test_source_examples_s_plus_plus_is_dur_and_s_plus_minus_is_moll(self):
        self.assertEqual(dur_moll_character("S", "+", "+"), "D")
        self.assertEqual(dur_moll_character("S", "+", "-"), "M")

    def test_all_null_eight_series_is_formally_all_moll_without_quantum(self):
        series = ProfileSeries(tuple(profile() for _ in range(8)))

        result = dur_moll_index(series)

        self.assertEqual(result.total_dur, 0)
        self.assertEqual(result.total_moll, 32)
        self.assertEqual(result.dur_percentage, Fraction(0, 1))
        self.assertEqual(result.moll_percentage, Fraction(100, 1))
        self.assertTrue(all(item.moll_reactions == 8 for item in result.vectors))
        self.assertTrue(all(item.dur_quantum == 0 and item.moll_quantum == 0 for item in result.vectors))

    def test_quantum_marks_are_added_to_the_vector_images_dur_or_moll_side(self):
        # Abb. 21 / source example: S ++ is Dur. With +! on both h and s,
        # every S image contributes 1 reaction + 2 quantum units = 3 Dur.
        # The other three all-null vectors are Moll and contribute 1 each.
        series = ProfileSeries(
            tuple(
                profile({"h": ("positive", 1), "s": ("positive", 1)})
                for _ in range(8)
            )
        )

        result = dur_moll_index(series)

        sexual = result.vectors[0]
        self.assertEqual(sexual.vector, "S")
        self.assertEqual(sexual.dur_reactions, 8)
        self.assertEqual(sexual.dur_quantum, 16)
        self.assertEqual(sexual.dur_score, 24)
        self.assertEqual(result.total_dur, 24)
        self.assertEqual(result.total_moll, 24)
        self.assertEqual(result.dur_percentage, Fraction(50, 1))
        self.assertEqual(result.moll_percentage, Fraction(50, 1))

    def test_ten_profile_series_is_admitted(self):
        result = dur_moll_index(ProfileSeries(tuple(profile() for _ in range(10))))
        self.assertEqual(result.total_moll, 40)

    def test_other_profile_counts_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "eight- or ten-profile"):
            dur_moll_index(ProfileSeries(tuple(profile() for _ in range(6))))

    def test_unknown_vector_and_reaction_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "Unknown vector"):
            dur_moll_character("X", "0", "0")
        with self.assertRaisesRegex(ValueError, "Unsupported base vector reaction"):
            dur_moll_character("S", "?", "0")


if __name__ == "__main__":
    unittest.main()
