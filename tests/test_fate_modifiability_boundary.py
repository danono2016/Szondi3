import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import AssertionMode
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _null_profile():
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


class FateModifiabilityBoundaryTests(unittest.TestCase):
    def test_familial_drive_dialectic_is_not_rendered_as_fixed_fate(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_null_profile(),)), production=True
        )
        findings = {
            item.claim_id: item for item in result.series_result.interpretation.findings
        }
        finding = findings["IC_SZONDI_PRIMARY_000087"]
        self.assertIs(finding.assertion_mode, AssertionMode.LIMITATION)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_A_000038",))
        self.assertIn("nu o face un destin personal fix", finding.statement)
        self.assertIn("persönliche, bewußte Stellungnahme", finding.statement)
        self.assertIn("Dominanzwechsel", finding.statement)
        self.assertIn("persönlich umstellbar", finding.statement)
        self.assertEqual(finding.support_fact_ids, ("profile_series:profile_count",))
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000087",))
        self.assertIn("hereditary_genetic", finding.sensitive_domains)


if __name__ == "__main__":
    unittest.main()
