import unittest

from szondi3.linnaeus import strict_leading_subclasses
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


REACTIONS = {
    "null": (0, 0, "0"),
    "positive": (2, 0, "+"),
    "negative": (0, 2, "-"),
    "ambivalent": (2, 2, "±"),
}


def profile_with_factor_kinds(kinds_by_factor):
    reactions = []
    for factor in FACTORS:
        kind = kinds_by_factor.get(factor, "null")
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


def series_with_h_root(h_kinds):
    return ProfileSeries(
        tuple(
            profile_with_factor_kinds({"h": kind, "s": "null"})
            for kind in h_kinds
        )
    )


class StrictSubclassTests(unittest.TestCase):
    def test_unmixed_positive_root_yields_positive_subclass(self):
        series = series_with_h_root(("positive",) * 8 + ("null", "ambivalent"))

        subclass = strict_leading_subclasses(series)[0]

        self.assertEqual(subclass.designation, "Sh")
        self.assertEqual(subclass.root_factor, "h")
        self.assertEqual(subclass.sign, "+")
        self.assertEqual(subclass.label, "Sh+")

    def test_unmixed_negative_root_yields_negative_subclass(self):
        series = series_with_h_root(("negative",) * 8 + ("null", "ambivalent"))

        subclass = strict_leading_subclasses(series)[0]

        self.assertEqual(subclass.designation, "Sh")
        self.assertEqual(subclass.sign, "-")
        self.assertEqual(subclass.label, "Sh-")

    def test_mixed_root_direction_fails_closed_instead_of_using_majority(self):
        series = series_with_h_root(
            ("positive",) * 5 + ("negative",) * 3 + ("null", "ambivalent")
        )

        with self.assertRaisesRegex(ValueError, "mixed Wurzelfaktor direction"):
            strict_leading_subclasses(series)

    def test_co_leading_unmixed_roots_retain_separate_subclass_signs(self):
        profiles = []
        for index in range(10):
            profiles.append(
                profile_with_factor_kinds(
                    {
                        "h": "negative" if index < 8 else "null",
                        "s": "null",
                        "k": "positive" if index < 8 else "null",
                        "p": "null",
                    }
                )
            )
        series = ProfileSeries(tuple(profiles))

        subclasses = strict_leading_subclasses(series)

        self.assertEqual(
            tuple(item.label for item in subclasses),
            ("Sh-", "Schk+"),
        )


if __name__ == "__main__":
    unittest.main()
