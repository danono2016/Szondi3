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


class TotalNegationRepressionTests(unittest.TestCase):
    def test_sch_negative_zero_refines_negation_as_source_defined_verdrangung(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"k": ("negative", 0)}),)),
            production=True,
        )

        findings = {
            item.claim_id: item for item in result.profiles[0].interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000010", findings)
        self.assertIn("IC_SZONDI_PRIMARY_000041", findings)

        finding = findings["IC_SZONDI_PRIMARY_000041"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000020",))
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_B",))
        self.assertIn("totale Negation / Verdrängung", finding.statement)
        self.assertIn("absolute Räumung", finding.statement)
        self.assertIn("0p", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000041",))
        self.assertIn("conținutul presupus refulat", finding.anti_inferences[0])
        self.assertIn("Quasi Endstation", finding.anti_inferences[0])
        self.assertIn("Überdruck", finding.anti_inferences[0])

    def test_negative_k_with_nonzero_p_remains_negation_not_total_repression(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"k": ("negative", 0), "p": ("positive", 0)}),)
            ),
            production=True,
        )

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertIn("IC_SZONDI_PRIMARY_000010", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000041", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000041", unresolved_ids)

    def test_negative_k_overpressure_is_not_auto_extended_to_total_repression(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"k": ("negative", 1)}),)),
            production=True,
        )

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertIn("IC_SZONDI_PRIMARY_000010", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000041", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000041", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
