import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, kind="null"):
    symbol = {"null": "0", "positive": "+", "negative": "-", "ambivalent": "±"}[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=symbol,
        quantum_level=0,
    )


class ProjectiveDefenseDifferentiationGuardTests(unittest.TestCase):
    def test_minus_p_does_not_collapse_to_total_projection(self):
        profile = build_profile(
            _reaction(factor, "negative" if factor == "p" else "null")
            for factor in FACTORS
        )
        result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
        finding = next(
            item
            for item in result.profiles[0].interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000058"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000017",))
        self.assertIn("totale Projektion", finding.statement)
        self.assertIn("Deprojektion", finding.statement)
        self.assertIn("Sim­pla prezență", finding.statement.replace("Simpla", "Sim­pla"))
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000058",))
        self.assertIn("Nu colapsa orice -p", finding.anti_inferences[0])

    def test_guard_does_not_fire_without_minus_p(self):
        profile = build_profile(_reaction(factor) for factor in FACTORS)
        result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
        ids = {item.claim_id for item in result.profiles[0].interpretation.findings}
        self.assertNotIn("IC_SZONDI_PRIMARY_000058", ids)


if __name__ == "__main__":
    unittest.main()
