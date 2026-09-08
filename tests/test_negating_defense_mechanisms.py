import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, kind="null", quantum=0):
    base = {"null": "0", "positive": "+", "negative": "-", "ambivalent": "±"}[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=base + ("!" * quantum),
        quantum_level=quantum,
    )


def _profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        _reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


def _findings(overrides):
    result = evaluate_clinical_protocol(
        ProfileSeries((_profile(overrides),)),
        production=True,
    )
    return {item.claim_id: item for item in result.profiles[0].interpretation.findings}


class NegatingDefenseMechanismTests(unittest.TestCase):
    def test_ordinary_sch_minus_minus_is_anpassung(self):
        findings = _findings({"k": ("negative", 0), "p": ("negative", 0)})
        finding = findings["IC_SZONDI_PRIMARY_000064"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000020",))
        self.assertIn("projektive Negation / Anpassung", finding.statement)
        self.assertIn("Wunschprojektion", finding.statement)
        self.assertIn("Realität", finding.statement)
        self.assertNotIn("IC_SZONDI_PRIMARY_000065", findings)

    def test_sch_k_minus_double_overpressure_p_minus_is_destruktion(self):
        findings = _findings({"k": ("negative", 2), "p": ("negative", 0)})
        finding = findings["IC_SZONDI_PRIMARY_000065"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000020",))
        self.assertIn("Destruktion", finding.statement)
        self.assertIn("Verneinung", finding.statement)
        self.assertNotIn("IC_SZONDI_PRIMARY_000064", findings)

    def test_other_quantum_levels_are_not_promoted_to_destruktion(self):
        for quantum in (1, 3):
            with self.subTest(quantum=quantum):
                findings = _findings({"k": ("negative", quantum), "p": ("negative", 0)})
                self.assertNotIn("IC_SZONDI_PRIMARY_000064", findings)
                self.assertNotIn("IC_SZONDI_PRIMARY_000065", findings)

    def test_p_overpressure_is_not_absorbed_into_table_13_forms(self):
        findings = _findings({"k": ("negative", 0), "p": ("negative", 1)})
        self.assertNotIn("IC_SZONDI_PRIMARY_000064", findings)
        self.assertNotIn("IC_SZONDI_PRIMARY_000065", findings)


if __name__ == "__main__":
    unittest.main()
