import unittest

from szondi3.administration import complete_foreground, record_foreground
from szondi3.profile import VECTOR_FACTORS, build_profile
from szondi3.scoring import factor_reactions
from szondi3.stimuli import SERIES, presentation_rows


def ids(series):
    rows = presentation_rows(series)
    return [card.card_id for row in rows for card in row]


class DriveProfileTests(unittest.TestCase):
    def test_vector_factor_order_is_source_defined(self):
        self.assertEqual(
            VECTOR_FACTORS,
            (("S", ("h", "s")), ("P", ("e", "hy")), ("Sch", ("k", "p")), ("C", ("d", "m"))),
        )

    def test_profile_groups_all_eight_factor_reactions(self):
        choices = []
        for series in SERIES:
            cards = ids(series)
            choices.append(record_foreground(series, cards[:2], cards[2:4]))
        reactions = factor_reactions(complete_foreground(choices))
        profile = build_profile(reactions)

        self.assertEqual(tuple(v.name for v in profile.vectors), ("S", "P", "Sch", "C"))
        self.assertEqual(tuple(v.factors for v in profile.vectors), (("h", "s"), ("e", "hy"), ("k", "p"), ("d", "m")))
        self.assertEqual(tuple(v.symbols for v in profile.vectors), (("+", "-"), ("+", "+"), ("-", "-"), ("-", "+")))
        self.assertEqual(tuple(r.factor for r in profile.factors), ("h", "s", "e", "hy", "k", "p", "d", "m"))

    def test_profile_rejects_missing_or_duplicate_factor_reactions(self):
        choices = []
        for series in SERIES:
            cards = ids(series)
            choices.append(record_foreground(series, cards[:2], cards[2:4]))
        reactions = factor_reactions(complete_foreground(choices))

        with self.assertRaises(ValueError):
            build_profile(reactions[:-1])
        with self.assertRaises(ValueError):
            build_profile(reactions[:-1] + (reactions[0],))


if __name__ == "__main__":
    unittest.main()
