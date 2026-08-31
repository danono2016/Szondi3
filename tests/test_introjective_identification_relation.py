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


class IntrojectiveIdentificationRelationTests(unittest.TestCase):
    def test_m_minus_with_k_plus_emits_introjective_identification(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"m": ("negative", 0), "k": ("positive", 0)}),)
            ),
            production=True,
        )

        finding = next(
            item
            for item in result.profiles[0].interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000038"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_A_000046",))
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_A",))
        self.assertIn("introjektive Identifizierung", finding.statement)
        self.assertIn("Identifizierung nu este echivalentă cu Identität", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000038",))
        self.assertIn("pierdere", finding.anti_inferences[0])
        self.assertIn("identitatea globală", finding.anti_inferences[0])
        self.assertIn("narcisism", finding.anti_inferences[0])

    def test_k_plus_without_m_minus_does_not_emit_relation(self):
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
        self.assertNotIn("IC_SZONDI_PRIMARY_000038", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000038", unresolved_ids)

    def test_quantum_overpressure_is_not_auto_extended(self):
        for overrides in (
            {"m": ("negative", 1), "k": ("positive", 0)},
            {"m": ("negative", 0), "k": ("positive", 1)},
        ):
            with self.subTest(overrides=overrides):
                result = evaluate_clinical_protocol(
                    ProfileSeries((_profile(overrides),)),
                    production=True,
                )
                claim_ids = {
                    item.claim_id
                    for item in result.profiles[0].interpretation.findings
                }
                unresolved_ids = {
                    item.claim_id
                    for item in result.profiles[0].interpretation.unresolved
                }
                self.assertNotIn("IC_SZONDI_PRIMARY_000038", claim_ids)
                self.assertNotIn("IC_SZONDI_PRIMARY_000038", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
