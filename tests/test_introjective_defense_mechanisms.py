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


def _profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        _reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


def _claim_ids(overrides):
    result = evaluate_clinical_protocol(
        ProfileSeries((_profile(overrides),)),
        production=True,
    )
    return {
        item.claim_id: item for item in result.profiles[0].interpretation.findings
    }


class IntrojectiveDefenseMechanismTests(unittest.TestCase):
    def test_sch_plus_zero_is_totale_introjektion(self):
        findings = _claim_ids({"k": ("positive", 0)})
        finding = findings["IC_SZONDI_PRIMARY_000062"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000019",))
        self.assertIn("totale Introjektion", finding.statement)
        self.assertIn("Einverleibung", finding.statement)
        self.assertIn("Seinsmacht", finding.statement)
        self.assertIn("Habmacht", finding.statement)

    def test_sch_plus_ambivalent_is_inflaprojektive_introjektion(self):
        findings = _claim_ids({"k": ("positive", 0), "p": ("ambivalent", 0)})
        finding = findings["IC_SZONDI_PRIMARY_000063"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000019",))
        self.assertIn("inflaprojektive Introjektion", finding.statement)
        self.assertIn("Vorphase", finding.statement)
        self.assertIn("Projektion", finding.statement)
        self.assertIn("Inflation", finding.statement)

    def test_neighboring_introjective_forms_do_not_collapse(self):
        total = _claim_ids({"k": ("positive", 0)})
        prephase = _claim_ids({"k": ("positive", 0), "p": ("ambivalent", 0)})
        compulsion = _claim_ids({"k": ("ambivalent", 0)})
        self.assertIn("IC_SZONDI_PRIMARY_000062", total)
        self.assertNotIn("IC_SZONDI_PRIMARY_000063", total)
        self.assertIn("IC_SZONDI_PRIMARY_000063", prephase)
        self.assertNotIn("IC_SZONDI_PRIMARY_000062", prephase)
        self.assertIn("IC_SZONDI_PRIMARY_000039", compulsion)
        self.assertNotIn("IC_SZONDI_PRIMARY_000062", compulsion)
        self.assertNotIn("IC_SZONDI_PRIMARY_000063", compulsion)

    def test_quantum_overpressure_is_not_auto_extended(self):
        for overrides in (
            {"k": ("positive", 1)},
            {"k": ("positive", 0), "p": ("ambivalent", 1)},
        ):
            with self.subTest(overrides=overrides):
                findings = _claim_ids(overrides)
                self.assertNotIn("IC_SZONDI_PRIMARY_000062", findings)
                self.assertNotIn("IC_SZONDI_PRIMARY_000063", findings)


if __name__ == "__main__":
    unittest.main()
