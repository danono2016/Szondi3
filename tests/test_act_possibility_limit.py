import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
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


class ActPossibilityLimitTests(unittest.TestCase):
    def test_test_evidence_limits_act_inference_to_possibility(self):
        result = evaluate_clinical_protocol(ProfileSeries((_null_profile(),)))

        finding = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000031"
        )

        self.assertEqual(finding.doctrine_ids, ("DR_SZ_TRIEBPATH_2_000001",))
        self.assertEqual(finding.source_ids, ("SZ_TRIEBPATH_2",))
        self.assertEqual(finding.support_fact_ids, ("profile_series:profile_count",))
        self.assertIn("posibilitatea unei fapte", finding.statement)
        self.assertIn("nu dovedește", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000031",))
        self.assertIn("dovezi independente", finding.anti_inferences[0])


if __name__ == "__main__":
    unittest.main()
