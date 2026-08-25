import unittest

from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from szondi3.scoring import complement_factor_reactions, factor_reactions, reaction_from_counts
from szondi3.stimuli import SERIES, catalog, presentation_rows


TABLE_3 = {
    (0, 0): "0", (1, 0): "0", (0, 1): "0", (1, 1): "0",
    (6, 0): "+!!!", (5, 0): "+!!", (5, 1): "+!!", (4, 0): "+!", (4, 1): "+!",
    (3, 0): "+", (3, 1): "+", (2, 0): "+", (2, 1): "+",
    (0, 6): "-!!!", (0, 5): "-!!", (1, 5): "-!!", (0, 4): "-!", (1, 4): "-!",
    (0, 3): "-", (1, 3): "-", (0, 2): "-", (1, 2): "-",
    (4, 2): "±!", (2, 4): "±!",
    (2, 2): "±", (2, 3): "±", (3, 2): "±", (3, 3): "±",
}


def ids(series):
    rows = presentation_rows(series)
    return [card.card_id for row in rows for card in row]


class FactorReactionTests(unittest.TestCase):
    def test_table_3_all_28_reactions(self):
        self.assertEqual(len(TABLE_3), 28)
        for counts, expected in TABLE_3.items():
            with self.subTest(counts=counts):
                self.assertEqual(reaction_from_counts(*counts).symbol, expected)

    def test_invalid_counts_fail(self):
        for counts in [(-1, 0), (0, -1), (7, 0), (0, 7), (4, 3), (6, 1)]:
            with self.subTest(counts=counts):
                with self.assertRaises(ValueError):
                    reaction_from_counts(*counts)

    def test_quantum_levels_follow_protocol_marks(self):
        self.assertEqual(reaction_from_counts(6, 0).quantum_level, 3)
        self.assertEqual(reaction_from_counts(5, 1).quantum_level, 2)
        self.assertEqual(reaction_from_counts(4, 0).quantum_level, 1)
        self.assertEqual(reaction_from_counts(4, 2).quantum_level, 1)
        self.assertEqual(reaction_from_counts(3, 0).quantum_level, 0)

    def test_foreground_factor_counts_come_from_card_factors(self):
        choices = []
        for series in SERIES:
            cards = ids(series)
            choices.append(record_foreground(series, cards[:2], cards[2:4]))
        protocol = complete_foreground(choices)
        reactions = {reaction.factor: reaction for reaction in factor_reactions(protocol)}

        expected = {
            "h": (2, 1, "+"), "s": (1, 2, "-"),
            "e": (2, 1, "+"), "hy": (2, 1, "+"),
            "k": (1, 2, "-"), "p": (1, 2, "-"),
            "d": (1, 2, "-"), "m": (2, 1, "+"),
        }
        for factor, (positive, negative, symbol) in expected.items():
            reaction = reactions[factor]
            self.assertEqual((reaction.sympathetic, reaction.unsympathetic), (positive, negative))
            self.assertEqual(reaction.symbol, symbol)
            self.assertFalse(reaction.forced_null)

        self.assertEqual(sum(r.sympathetic for r in reactions.values()), 12)
        self.assertEqual(sum(r.unsympathetic for r in reactions.values()), 12)

    def test_ekp_uses_same_reaction_table_and_marks_numerically_forced_null(self):
        cards_by_series = {
            series: [card for card in catalog() if card.series == series]
            for series in SERIES
        }
        foreground_choices = []
        for index, series in enumerate(SERIES):
            group = cards_by_series[series]
            h_card = next(card for card in group if card.factor == "h")
            if index < 5:
                selected = [h_card] + [card for card in group if card.factor != "h"][:3]
            else:
                selected = [card for card in group if card.factor != "h"][:4]
            foreground_choices.append(
                record_foreground(
                    series,
                    [selected[0].card_id, selected[1].card_id],
                    [selected[2].card_id, selected[3].card_id],
                )
            )

        foreground = complete_foreground(foreground_choices)
        complement_choices = [
            record_complement(choice, choice.remaining[:2], "unsympathetic")
            for choice in foreground.series_choices
        ]
        complement = complete_complement(foreground, complement_choices)
        reactions = {r.factor: r for r in complement_factor_reactions(foreground, complement)}

        self.assertEqual(reactions["h"].symbol, "0")
        self.assertTrue(reactions["h"].forced_null)
        self.assertEqual(reactions["h"].sympathetic + reactions["h"].unsympathetic, 1)


if __name__ == "__main__":
    unittest.main()
