import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}


def _reaction(factor: str, symbol: str) -> FactorReaction:
    base = "±" if symbol.startswith("±") else symbol[0]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=_KIND[base],
        symbol=symbol,
        quantum_level=symbol.count("!"),
    )


def _profile(*symbols: str):
    return build_profile(
        _reaction(factor, symbol)
        for factor, symbol in zip(_FACTORS, symbols)
    )


def _fall40_series() -> ProfileSeries:
    return ProfileSeries(
        (
            _profile("+!", "0", "0", "-", "-", "±", "+", "-"),
            _profile("+!", "0", "-", "-", "-", "+", "+", "-"),
            _profile("+", "0", "-", "-", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-"),
            _profile("+", "0", "0", "-", "+", "±", "+", "-!!"),
            _profile("+!", "0", "-", "-!", "+", "±", "+", "-!"),
            _profile("+!", "-", "-", "0", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "0", "±", "±", "+", "-!"),
        )
    )


class HaupttriebklasseSeriesClaimTests(unittest.TestCase):
    def test_fall40_p1_establishes_sh_as_unique_leading_danger_class(self):
        result = evaluate_clinical_protocol(_fall40_series(), production=True)

        tspg = result.series_result.calculation("factor_tension_degrees").value
        self.assertEqual(
            {item.factor: item.degree for item in tspg},
            {"h": 0, "s": 9, "e": 2, "hy": 2, "k": 1, "p": 7, "d": 0, "m": 0},
        )

        tspd = result.series_result.calculation("vector_tension_differences").value
        self.assertEqual(
            {item.vector: item.magnitude for item in tspd},
            {"S": 9, "P": 0, "Sch": 6, "C": 0},
        )

        latency = result.series_result.calculation("latency_class_structure").value
        self.assertEqual(latency.kind, "danger_class")
        self.assertEqual(latency.danger_count, 2)
        self.assertEqual(
            {item.vector: (item.ten_base_magnitude, item.status) for item in latency.statuses},
            {
                "S": (9, "danger"),
                "P": (0, "ventil"),
                "Sch": (6, "danger"),
                "C": (0, "ventil"),
            },
        )

        leaders = result.series_result.calculation("leading_drive_classes").value
        self.assertEqual(tuple(item.designation for item in leaders), ("Sh",))
        self.assertEqual(leaders[0].status.ten_base_magnitude, 9)
        self.assertEqual(leaders[0].status.status, "danger")

    def test_fall40_series_claim_uses_exact_p1_support_and_primary_doctrine(self):
        result = evaluate_clinical_protocol(_fall40_series(), production=True)
        finding = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000015"
        )

        self.assertEqual(
            finding.support_fact_ids,
            (
                "profile_series:profile_count",
                "profile_series:danger_leading_drive_classes",
            ),
        )
        self.assertEqual(
            finding.doctrine_ids,
            (
                "DR_SZ_LEHR_1972_000321",
                "DR_SZ_LEHR_1972_000322",
                "DR_SZ_LEHR_1972_000324",
                "DR_SZ_LEHR_1972_000326",
            ),
        )
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000015",))
        self.assertIn("Haupttriebklasse", finding.statement)
        self.assertIn("Triebgefahr", finding.statement)
        self.assertTrue(
            any("profil dominant" in item for item in finding.anti_inferences)
        )

    def test_same_nine_profiles_do_not_activate_ten_series_claim(self):
        short = ProfileSeries(_fall40_series().profiles[:9])
        result = evaluate_clinical_protocol(short, production=True)
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000015",
            {item.claim_id for item in result.series_result.interpretation.findings},
        )


if __name__ == "__main__":
    unittest.main()
