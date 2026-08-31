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


class ContactParoxysmalRelationTests(unittest.TestCase):
    def test_c_plus_minus_emits_detachment_and_search_without_pathology_promotion(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"d": ("positive", 0), "m": ("negative", 0)}),)),
            production=True,
        )

        finding = next(
            item
            for item in result.profiles[0].interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000035"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_LEHR_1972_000358",))
        self.assertEqual(finding.source_ids, ("SZ_LEHR_1972",))
        self.assertIn("desprinderea / eliberarea", finding.statement)
        self.assertIn("pornirea în căutare", finding.statement)
        self.assertIn("pas fiziologic de dezvoltare", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000035",))
        self.assertIn("infidelității", finding.anti_inferences[0])
        self.assertIn("depresiei", finding.anti_inferences[0])
        self.assertIn("autismului", finding.anti_inferences[0])

    def test_p_zero_minus_without_overpressure_emits_sensitive_beziehungsangst(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"hy": ("negative", 0)}),)),
            production=True,
        )

        finding = next(
            item
            for item in result.profiles[0].interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000036"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_LEHR_1972_000361",))
        self.assertEqual(finding.source_ids, ("SZ_LEHR_1972",))
        self.assertIn("sensitive Beziehungsangst", finding.statement)
        self.assertIn("noțiune szondiană testologică", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000036",))
        self.assertIn("anxietate socială", finding.anti_inferences[0])
        self.assertIn("paranoia", finding.anti_inferences[0])

    def test_p_zero_minus_with_hy_overpressure_is_excluded(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"hy": ("negative", 1)}),))
        )

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000036", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000036", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
