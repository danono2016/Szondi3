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


class SublimationFateMethodGuardTests(unittest.TestCase):
    def setUp(self):
        self.result = evaluate_clinical_protocol(ProfileSeries((_null_profile(),)), production=True)
        self.findings = {
            item.claim_id: item for item in self.result.series_result.interpretation.findings
        }

    def test_sublimation_table_is_not_promoted_to_complete_taxonomy(self):
        finding = self.findings["IC_SZONDI_PRIMARY_000079"]
        self.assertEqual(finding.assertion_mode, AssertionMode.LIMITATION)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000024",))
        self.assertIn("unvollständige Übersicht", finding.statement)
        self.assertIn("Sublimierung mit Negation", finding.statement)
        self.assertIn("taxonomie totală", finding.statement)
        self.assertEqual(finding.support_fact_ids, ("profile_series:profile_count",))
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000079",))

    def test_character_is_only_a_piece_of_fate(self):
        finding = self.findings["IC_SZONDI_PRIMARY_000080"]
        self.assertEqual(finding.assertion_mode, AssertionMode.LIMITATION)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000025",))
        self.assertIn("Stück des Schicksals", finding.statement)
        self.assertIn("nu epuizează Schicksal-ul", finding.statement)
        self.assertEqual(finding.support_fact_ids, ("profile_series:profile_count",))
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000080",))


if __name__ == "__main__":
    unittest.main()
