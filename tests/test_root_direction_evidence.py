import unittest

from szondi3.linnaeus import leading_root_direction_evidence
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
    profiles = []
    for h_kind in h_kinds:
        # s remains symptomatic (null), so h is the lower-TspG/root factor of S.
        profiles.append(
            profile_with_factor_kinds(
                {
                    "h": h_kind,
                    "s": "null",
                    "e": "null",
                    "hy": "null",
                    "k": "null",
                    "p": "null",
                    "d": "null",
                    "m": "null",
                }
            )
        )
    return ProfileSeries(tuple(profiles))


class RootDirectionEvidenceTests(unittest.TestCase):
    def test_counts_negative_root_direction_without_interpretation(self):
        # A source-style strongly negative root: eight negative reactions and two
        # symptom reactions give h TspG=2 against s TspG=10, hence class Sh.
        series = series_with_h_root(
            ("negative",) * 8 + ("null", "ambivalent")
        )

        evidence = leading_root_direction_evidence(series)

        self.assertEqual(len(evidence), 1)
        item = evidence[0]
        self.assertEqual(item.designation, "Sh")
        self.assertEqual(item.root_factor, "h")
        self.assertEqual(item.positive_reactions, 0)
        self.assertEqual(item.negative_reactions, 8)
        self.assertEqual(item.null_reactions, 1)
        self.assertEqual(item.ambivalent_reactions, 1)
        self.assertEqual(item.directional_reactions, 8)

    def test_mixed_direction_is_preserved_as_counts_not_majority_sign(self):
        # The admitted source defines subclass direction but gives no universal
        # numeric majority threshold for every mixed series. Preserve the evidence.
        series = series_with_h_root(
            ("positive",) * 5 + ("negative",) * 3 + ("null", "ambivalent")
        )

        item = leading_root_direction_evidence(series)[0]

        self.assertEqual(item.designation, "Sh")
        self.assertEqual(item.positive_reactions, 5)
        self.assertEqual(item.negative_reactions, 3)
        self.assertEqual(item.null_reactions, 1)
        self.assertEqual(item.ambivalent_reactions, 1)
        self.assertEqual(item.directional_reactions, 8)

    def test_co_leading_classes_keep_separate_root_direction_evidence(self):
        profiles = []
        for index in range(10):
            profiles.append(
                profile_with_factor_kinds(
                    {
                        "h": "negative" if index < 8 else "null",
                        "s": "null",
                        "k": "positive" if index < 8 else "null",
                        "p": "null",
                        "e": "null",
                        "hy": "null",
                        "d": "null",
                        "m": "null",
                    }
                )
            )
        series = ProfileSeries(tuple(profiles))

        evidence = leading_root_direction_evidence(series)

        self.assertEqual(
            tuple((item.designation, item.root_factor) for item in evidence),
            (("Sh", "h"), ("Schk", "k")),
        )
        self.assertEqual(evidence[0].negative_reactions, 8)
        self.assertEqual(evidence[1].positive_reactions, 8)


if __name__ == "__main__":
    unittest.main()
