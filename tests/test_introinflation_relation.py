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


class IntroinflationRelationTests(unittest.TestCase):
    def test_exact_ordinary_sch_plus_plus_yields_testological_introinflation(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"k": ("positive", 0), "p": ("positive", 0)}),)
            ),
            production=True,
        )

        findings = {
            item.claim_id: item for item in result.profiles[0].interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000009", findings)
        self.assertIn("IC_SZONDI_PRIMARY_000008", findings)
        self.assertIn("IC_SZONDI_PRIMARY_000042", findings)

        finding = findings["IC_SZONDI_PRIMARY_000042"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000027",))
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_B",))
        self.assertIn("Introinflation", finding.statement)
        self.assertIn("Introjektion (+k)", finding.statement)
        self.assertIn("Inflation (+p)", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000042",))
        self.assertIn("Persona jungiene", finding.anti_inferences[0])
        self.assertIn("grandiozității", finding.anti_inferences[0])
        self.assertIn("contactului cu realitatea", finding.anti_inferences[0])
        self.assertIn("Überdruck", finding.anti_inferences[0])

    def test_plus_k_without_plus_p_does_not_create_introinflation(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"k": ("positive", 0)}),)),
            production=True,
        )

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertIn("IC_SZONDI_PRIMARY_000009", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000042", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000042", unresolved_ids)

    def test_plus_plus_with_overpressure_is_not_auto_extended_to_introinflation(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"k": ("positive", 0), "p": ("positive", 1)}),)
            ),
            production=True,
        )

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertIn("IC_SZONDI_PRIMARY_000009", claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000008", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000042", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000042", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
