import unittest
from pathlib import Path

from szondi3.stimuli import FACTORS, SERIES, catalog, presentation_rows, validate_assets


EXPECTED = {
    "I": ("k", "s", "p", "d", "h", "e", "m", "hy"),
    "II": ("hy", "m", "e", "h", "d", "p", "s", "k"),
    "III": ("h", "e", "s", "m", "k", "d", "hy", "p"),
    "IV": ("p", "hy", "d", "k", "m", "s", "e", "h"),
    "V": ("e", "d", "hy", "p", "s", "k", "h", "m"),
    "VI": ("m", "h", "k", "s", "p", "hy", "d", "e"),
}


class StimulusFactsTests(unittest.TestCase):
    def test_primary_source_mapping(self):
        cards = catalog()
        self.assertEqual(len(cards), 48)
        self.assertEqual(len({card.card_id for card in cards}), 48)

        for series in SERIES:
            group = [card for card in cards if card.series == series]
            self.assertEqual([card.position for card in group], list(range(1, 9)))
            self.assertEqual(tuple(card.factor for card in group), EXPECTED[series])
            self.assertEqual(set(card.factor for card in group), set(FACTORS))

    def test_image_paths_encode_verified_identity(self):
        for card in catalog():
            self.assertEqual(
                card.image_path,
                f"assets/stimuli/{card.series}-{card.position:02d}-{card.factor}.webp",
            )

    def test_presentation_is_two_rows_of_four_in_position_order(self):
        for series in SERIES:
            rows = presentation_rows(series)
            self.assertEqual(len(rows), 2)
            self.assertEqual([card.position for card in rows[0]], [1, 2, 3, 4])
            self.assertEqual([card.position for card in rows[1]], [5, 6, 7, 8])

    def test_unknown_series_fails(self):
        with self.assertRaises(ValueError):
            presentation_rows("VII")

    def test_repository_asset_set_is_exact(self):
        validate_assets(Path("assets/stimuli"))


if __name__ == "__main__":
    unittest.main()
