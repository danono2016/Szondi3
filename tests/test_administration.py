import unittest
from dataclasses import replace

from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
    validate_complement_protocol,
    validate_foreground_protocol,
)
from szondi3.scoring import complement_factor_reactions, factor_reactions
from szondi3.stimuli import SERIES, presentation_rows


def ids(series):
    rows = presentation_rows(series)
    return [card.card_id for row in rows for card in row]


def full_foreground():
    choices = []
    for series in SERIES:
        cards = ids(series)
        choices.append(record_foreground(series, cards[:2], cards[2:4]))
    return complete_foreground(choices)


def full_complement(foreground):
    by_series = {choice.series: choice for choice in foreground.series_choices}
    return complete_complement(
        foreground,
        tuple(
            record_complement(
                by_series[series],
                by_series[series].remaining[:2],
                "unsympathetic",
            )
            for series in SERIES
        ),
    )


class BasicAdministrationTests(unittest.TestCase):
    def test_foreground_requires_two_plus_two_distinct_cards_from_one_series(self):
        cards = ids("I")
        choice = record_foreground("I", cards[:2], cards[2:4])
        self.assertEqual(choice.sympathetic, tuple(cards[:2]))
        self.assertEqual(choice.unsympathetic, tuple(cards[2:4]))
        self.assertEqual(choice.remaining, tuple(cards[4:]))

        with self.assertRaises(ValueError):
            record_foreground("I", cards[:1], cards[2:4])
        with self.assertRaises(ValueError):
            record_foreground("I", [cards[0], cards[1]], [cards[1], cards[2]])
        with self.assertRaises(ValueError):
            record_foreground("I", cards[:2], ids("II")[:2])

    def test_complete_foreground_has_six_series_and_twelve_plus_twelve(self):
        protocol = full_foreground()
        self.assertEqual(len(protocol.series_choices), 6)
        self.assertEqual(len(protocol.sympathetic), 12)
        self.assertEqual(len(protocol.unsympathetic), 12)
        self.assertEqual(len(protocol.remaining), 24)

    def test_revalidates_deserialized_foreground_before_scoring(self):
        foreground = full_foreground()
        self.assertIs(validate_foreground_protocol(foreground), foreground)

        malformed = replace(foreground, sympathetic=foreground.sympathetic[:-1])
        with self.assertRaisesRegex(ValueError, "aggregate fields"):
            validate_foreground_protocol(malformed)
        with self.assertRaisesRegex(ValueError, "aggregate fields"):
            factor_reactions(malformed)

        first = foreground.series_choices[0]
        malformed_choice = replace(first, remaining=first.remaining[::-1])
        malformed_series = replace(
            foreground,
            series_choices=(malformed_choice,) + foreground.series_choices[1:],
        )
        with self.assertRaisesRegex(ValueError, "inconsistent with its recorded card choices"):
            validate_foreground_protocol(malformed_series)

    def test_complement_can_record_unsympathetic_selection(self):
        cards = ids("III")
        foreground = record_foreground("III", cards[:2], cards[2:4])
        complement = record_complement(
            foreground,
            selected=foreground.remaining[:2],
            selected_as="unsympathetic",
        )
        self.assertEqual(complement.relative_unsympathetic, foreground.remaining[:2])
        self.assertEqual(complement.relative_sympathetic, foreground.remaining[2:])

    def test_complement_can_record_source_allowed_sympathetic_selection(self):
        cards = ids("IV")
        foreground = record_foreground("IV", cards[:2], cards[2:4])
        complement = record_complement(
            foreground,
            selected=foreground.remaining[:2],
            selected_as="sympathetic",
        )
        self.assertEqual(complement.relative_sympathetic, foreground.remaining[:2])
        self.assertEqual(complement.relative_unsympathetic, foreground.remaining[2:])

    def test_complement_must_use_exactly_two_of_the_four_remaining_cards(self):
        cards = ids("V")
        foreground = record_foreground("V", cards[:2], cards[2:4])
        with self.assertRaises(ValueError):
            record_complement(foreground, foreground.remaining[:1], "unsympathetic")
        with self.assertRaises(ValueError):
            record_complement(foreground, [foreground.remaining[0], cards[0]], "unsympathetic")
        with self.assertRaises(ValueError):
            record_complement(foreground, foreground.remaining[:2], "other")

    def test_complete_complement_has_twelve_plus_twelve(self):
        foreground = full_foreground()
        complement = full_complement(foreground)
        self.assertEqual(len(complement.relative_sympathetic), 12)
        self.assertEqual(len(complement.relative_unsympathetic), 12)

    def test_revalidates_deserialized_complement_before_scoring(self):
        foreground = full_foreground()
        complement = full_complement(foreground)
        self.assertIs(validate_complement_protocol(foreground, complement), complement)

        malformed = replace(
            complement,
            relative_unsympathetic=complement.relative_unsympathetic[:-1],
        )
        with self.assertRaisesRegex(ValueError, "aggregate fields"):
            validate_complement_protocol(foreground, malformed)
        with self.assertRaisesRegex(ValueError, "aggregate fields"):
            complement_factor_reactions(foreground, malformed)


if __name__ == "__main__":
    unittest.main()
