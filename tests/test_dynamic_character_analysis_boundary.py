import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import AssertionMode
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _neutral_profile():
    return build_profile(
        FactorReaction(
            factor=factor,
            sympathetic=0,
            unsympathetic=0,
            kind="null",
            symbol="0",
            quantum_level=0,
        )
        for factor in FACTORS
    )


class DynamicCharacterAnalysisBoundaryTests(unittest.TestCase):
    def test_series_activates_dynamic_character_method_boundary(self):
        result = evaluate_clinical_protocol(ProfileSeries((_neutral_profile(),)), production=True)
        findings = {item.claim_id: item for item in result.series_result.interpretation.findings}
        self.assertIn("IC_SZONDI_PRIMARY_000074", findings)
        finding = findings["IC_SZONDI_PRIMARY_000074"]
        self.assertIs(finding.assertion_mode, AssertionMode.LIMITATION)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000029",))
        self.assertIn("nur eine halbe Analyse", finding.statement)
        self.assertIn("Hintergänger", finding.statement)
        self.assertIn("Ahnentafel", finding.statement)
        self.assertIn("AI_SZONDI_000074", finding.anti_inference_ids)
        self.assertIn("hereditary_genetic", finding.sensitive_domains)


if __name__ == "__main__":
    unittest.main()
