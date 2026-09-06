import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, kind="null", quantum=0):
    base = {
        "null": "0",
        "positive": "+",
        "negative": "-",
        "ambivalent": "±",
    }[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=base + ("!" * quantum),
        quantum_level=quantum,
    )


def _profile(k_kind, p_kind, *, k_quantum=0, p_quantum=0):
    return build_profile(
        _reaction(
            factor,
            *(
                (k_kind, k_quantum)
                if factor == "k"
                else (p_kind, p_quantum)
                if factor == "p"
                else ("null", 0)
            ),
        )
        for factor in FACTORS
    )


def _claim_ids(profile):
    result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
    return {
        item.claim_id: item for item in result.profiles[0].interpretation.findings
    }


class InflationDeflationMechanismTests(unittest.TestCase):
    def test_total_inflation_is_exact_sch_zero_plus(self):
        findings = _claim_ids(_profile("null", "positive"))
        self.assertIn("IC_SZONDI_PRIMARY_000059", findings)
        finding = findings["IC_SZONDI_PRIMARY_000059"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000018",))
        self.assertIn("totale Inflation", finding.statement)
        self.assertIn("Unifunktion", finding.statement)

    def test_zwangsdeflation_is_exact_sch_ambivalent_plus(self):
        findings = _claim_ids(_profile("ambivalent", "positive"))
        self.assertIn("IC_SZONDI_PRIMARY_000060", findings)
        finding = findings["IC_SZONDI_PRIMARY_000060"]
        self.assertIn("Zwangsdeflation", finding.statement)
        self.assertIn("Inflationsgefahr", finding.statement)
        self.assertIn("Zwang", finding.statement)

    def test_hemmung_is_exact_sch_minus_plus(self):
        findings = _claim_ids(_profile("negative", "positive"))
        self.assertIn("IC_SZONDI_PRIMARY_000061", findings)
        finding = findings["IC_SZONDI_PRIMARY_000061"]
        self.assertIn("Hemmung", finding.statement)
        self.assertIn("negierte Inflation", finding.statement)
        self.assertIn("nu se poate stabili", finding.statement)

    def test_introinflation_remains_the_existing_plus_plus_route(self):
        findings = _claim_ids(_profile("positive", "positive"))
        self.assertIn("IC_SZONDI_PRIMARY_000042", findings)
        self.assertNotIn("IC_SZONDI_PRIMARY_000059", findings)
        self.assertNotIn("IC_SZONDI_PRIMARY_000060", findings)
        self.assertNotIn("IC_SZONDI_PRIMARY_000061", findings)

    def test_overpressure_does_not_widen_table_11_routes(self):
        for k_kind, p_kind, claim_id in (
            ("null", "positive", "IC_SZONDI_PRIMARY_000059"),
            ("ambivalent", "positive", "IC_SZONDI_PRIMARY_000060"),
            ("negative", "positive", "IC_SZONDI_PRIMARY_000061"),
        ):
            with self.subTest(claim_id=claim_id):
                findings = _claim_ids(
                    _profile(k_kind, p_kind, p_quantum=1)
                )
                self.assertNotIn(claim_id, findings)


if __name__ == "__main__":
    unittest.main()
