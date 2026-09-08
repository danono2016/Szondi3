import unittest

from szondi3.clinical_protocol import CalculationState, evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _profile():
    return build_profile(
        FactorReaction(
            factor=factor,
            sympathetic=0,
            unsympathetic=0,
            kind="negative" if factor == "s" else "null",
            symbol="-" if factor == "s" else "0",
            quantum_level=0,
        )
        for factor in FACTORS
    )


class ProportionMethodLimitTests(unittest.TestCase):
    def test_social_index_only_series_activates_general_partial_method_limit(self):
        result = evaluate_clinical_protocol(ProfileSeries(tuple(_profile() for _ in range(9))))

        self.assertEqual(
            result.series_result.calculation("dur_moll_index").state,
            CalculationState.NOT_APPLICABLE,
        )
        self.assertEqual(
            result.series_result.calculation("social_index").state,
            CalculationState.AVAILABLE,
        )
        finding = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000032"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_LEHR_1972_000334",))
        self.assertEqual(finding.source_ids, ("SZ_LEHR_1972",))
        self.assertIn("date parțiale", finding.statement)
        self.assertIn("nu constituie", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000032",))
        self.assertIn("rezumat global", finding.anti_inferences[0])

    def test_no_proportion_method_means_no_general_limit_finding(self):
        result = evaluate_clinical_protocol(ProfileSeries((_profile(),)))

        claim_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.series_result.interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000032", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000032", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
