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


class IntronegationRelationTests(unittest.TestCase):
    def test_sch_ambivalent_zero_emits_intronegation_without_diagnostic_promotion(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"k": ("ambivalent", 0)}),)),
            production=True,
        )

        finding = next(
            item
            for item in result.profiles[0].interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000039"
        )
        self.assertEqual(
            finding.doctrine_ids,
            ("DR_SZ_IA_1956_B_000003", "DR_SZ_IA_1956_B_000004"),
        )
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_B",))
        self.assertIn("Intronegation", finding.statement)
        self.assertIn("Introjektion (+k)", finding.statement)
        self.assertIn("Negation (−k)", finding.statement)
        self.assertIn("Zwang-Ich", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000039",))
        self.assertIn("obsesiv-compulsivă", finding.anti_inferences[0])
        self.assertIn("Zwangsschicksal", finding.anti_inferences[0])
        self.assertIn("masculinitate", finding.anti_inferences[0])

    def test_other_p_phase_does_not_emit_sch_ambivalent_zero_relation(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"k": ("ambivalent", 0), "p": ("positive", 0)}),)
            ),
            production=True,
        )

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000039", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000039", unresolved_ids)

    def test_quantum_overpressure_is_not_auto_extended(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"k": ("ambivalent", 1)}),)),
            production=True,
        )

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000039", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000039", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
