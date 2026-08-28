import unittest

from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries, latency_class_structure
from szondi3.stimuli import FACTORS


def profile_with_kinds(kinds):
    reactions = []
    for factor, kind in zip(FACTORS, kinds):
        if kind == "null":
            sympathetic, unsympathetic, symbol = 0, 0, "0"
        else:
            sympathetic, unsympathetic, symbol = 2, 0, "+"
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


def series_from_degrees(degrees, profile_count=10):
    profiles = []
    for profile_index in range(profile_count):
        kinds = [
            "null" if profile_index < degree else "positive"
            for degree in degrees
        ]
        profiles.append(profile_with_kinds(kinds))
    return ProfileSeries(tuple(profiles))


class LatencyClassStructureTests(unittest.TestCase):
    def test_danger_class_counts_one_to_four_gefahren(self):
        cases = {
            1: (8, 0, 1, 0, 1, 0, 0, 0),
            2: (8, 0, 7, 0, 1, 0, 0, 0),
            3: (8, 0, 7, 0, 6, 0, 0, 0),
            4: (8, 0, 7, 0, 6, 0, 5, 0),
        }
        for expected_count, degrees in cases.items():
            with self.subTest(expected_count=expected_count):
                structure = latency_class_structure(series_from_degrees(degrees))
                self.assertEqual(structure.kind, "danger_class")
                self.assertEqual(structure.danger_count, expected_count)
                self.assertEqual(structure.ventil_count, 4 - expected_count)
                self.assertEqual(
                    sum(item.status == "danger" for item in structure.statuses),
                    expected_count,
                )

    def test_all_ventile_spread_three_or_four_is_triventil(self):
        # SZ_LEHR_1972 BODY U003912 is OCR-corrupted in canonical text. Direct
        # arbitration against the admitted paired PDF (PDF p. 287 / printed p. 283)
        # resolves the source interval as 3–4. See docs/TRIVENTIL_VISUAL_ARBITRATION.md.
        for expected_spread, degrees in [
            (3, (3, 0, 2, 0, 1, 0, 0, 0)),
            (4, (4, 0, 2, 0, 1, 0, 0, 0)),
        ]:
            with self.subTest(spread=expected_spread):
                structure = latency_class_structure(series_from_degrees(degrees))
                self.assertEqual(structure.kind, "triventil")
                self.assertEqual(structure.danger_count, 0)
                self.assertEqual(structure.ventil_count, 4)
                self.assertEqual(structure.normalized_max, expected_spread)
                self.assertEqual(structure.normalized_min, 0)
                self.assertEqual(structure.spread, expected_spread)

    def test_all_ventile_spread_zero_to_two_is_quadriventil(self):
        for spread, degrees in [
            (0, (2, 2, 2, 2, 2, 2, 2, 2)),
            (1, (1, 0, 1, 0, 0, 0, 0, 0)),
            (2, (2, 0, 1, 0, 0, 0, 0, 0)),
        ]:
            with self.subTest(spread=spread):
                structure = latency_class_structure(series_from_degrees(degrees))
                self.assertEqual(structure.kind, "quadriventil")
                self.assertEqual(structure.danger_count, 0)
                self.assertEqual(structure.ventil_count, 4)
                self.assertEqual(structure.spread, spread)

    def test_fall_18_is_quadriventil_after_tabelle_13_conversion(self):
        # Six profiles; raw TspD = 1,0,1,0. Tabelle 13 maps 1 -> 2.
        structure = latency_class_structure(
            series_from_degrees((1, 0, 2, 2, 5, 4, 3, 3), profile_count=6)
        )
        self.assertEqual(
            tuple(item.ten_base_magnitude for item in structure.statuses),
            (2, 0, 2, 0),
        )
        self.assertEqual(structure.kind, "quadriventil")
        self.assertEqual(structure.spread, 2)


if __name__ == "__main__":
    unittest.main()
