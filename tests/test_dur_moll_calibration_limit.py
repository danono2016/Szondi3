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


class DurMollCalibrationLimitTests(unittest.TestCase):
    def test_available_dur_moll_emits_historical_calibration_guard_in_production(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(tuple(_profile() for _ in range(8))),
            production=True,
        )

        self.assertEqual(
            result.series_result.calculation("dur_moll_index").state,
            CalculationState.AVAILABLE,
        )
        finding = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000033"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_LEHR_1972_000336",))
        self.assertEqual(finding.source_ids, ("SZ_LEHR_1972",))
        self.assertIn("revalidare", finding.statement)
        self.assertIn("normalitate psihosexuală", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000033",))
        self.assertIn("normă masculină universală", finding.anti_inferences[0])
        self.assertIn("inferență genetică modernă", finding.anti_inferences[0])

    def test_social_index_only_series_does_not_emit_dur_moll_specific_guard(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(tuple(_profile() for _ in range(9)))
        )

        self.assertEqual(
            result.series_result.calculation("dur_moll_index").state,
            CalculationState.NOT_APPLICABLE,
        )
        claim_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.series_result.interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000033", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000033", unresolved_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000032", claim_ids)


if __name__ == "__main__":
    unittest.main()
