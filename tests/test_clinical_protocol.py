import unittest

from szondi3.clinical_protocol import CalculationState, evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def reaction(factor, kind="null", quantum=0):
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


def profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


class ClinicalProtocolTests(unittest.TestCase):
    def test_single_profile_is_useful_without_fake_series_methods(self):
        series = ProfileSeries((profile({"k": ("negative", 0)}),))

        result = evaluate_clinical_protocol(series)

        self.assertEqual(result.profile_count, 1)
        self.assertEqual(len(result.profiles), 1)
        profile_claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000010", profile_claim_ids)

        self.assertEqual(
            result.series_result.calculation("series_indices").state,
            CalculationState.AVAILABLE,
        )
        self.assertEqual(
            result.series_result.calculation("complete_formula").state,
            CalculationState.NOT_APPLICABLE,
        )
        self.assertEqual(
            result.series_result.calculation("dur_moll_index").state,
            CalculationState.NOT_APPLICABLE,
        )

        # Profile-local evaluation must not be polluted by missing series facts.
        self.assertEqual(result.profiles[0].interpretation.unresolved, ())
        series_claim_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000014", series_claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000029", series_claim_ids)
        unresolved_series_claim_ids = {
            item.claim_id for item in result.series_result.interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000014", unresolved_series_claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000029", unresolved_series_claim_ids)

    def test_eight_profile_protocol_assembles_independent_p1_outputs(self):
        series = ProfileSeries(
            tuple(profile({"s": ("negative", 0)}) for _ in range(8))
        )

        result = evaluate_clinical_protocol(series)

        self.assertEqual(
            result.series_result.calculation("leading_root_direction_evidence").state,
            CalculationState.AVAILABLE,
        )
        self.assertEqual(
            result.series_result.calculation("dur_moll_index").state,
            CalculationState.AVAILABLE,
        )
        self.assertEqual(
            result.series_result.calculation("social_index").state,
            CalculationState.AVAILABLE,
        )

        series_claim_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000001", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000003", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000004", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000005", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000014", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000029", series_claim_ids)
        dynamic_latency = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000029"
        )
        self.assertTrue(dynamic_latency.anti_inferences)
        self.assertIn("DR_SZ_LEHR_1972_000326", dynamic_latency.provenance_trace)
        serial_method = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000014"
        )
        self.assertEqual(
            serial_method.support_fact_ids,
            ("profile_series:profile_count",),
        )

    def test_one_unresolved_method_does_not_erase_other_valid_outputs(self):
        # With s directional and all other factors null, formula grouping has only
        # two TspG levels and therefore remains source-unresolved, while the root
        # direction and proportion methods are still independently available.
        series = ProfileSeries(
            tuple(profile({"s": ("negative", 0)}) for _ in range(8))
        )

        result = evaluate_clinical_protocol(series)

        formula = result.series_result.calculation("complete_formula")
        self.assertEqual(formula.state, CalculationState.UNRESOLVED)
        self.assertTrue(formula.error)
        self.assertEqual(
            result.series_result.calculation("leading_root_direction_evidence").state,
            CalculationState.AVAILABLE,
        )
        self.assertEqual(
            result.series_result.calculation("dur_moll_index").state,
            CalculationState.AVAILABLE,
        )
        self.assertIn(formula, result.unresolved_calculations)

    def test_all_null_series_preserves_linnaeus_ambiguity_but_still_interprets_profiles(self):
        series = ProfileSeries(tuple(profile() for _ in range(8)))

        result = evaluate_clinical_protocol(series)

        self.assertEqual(
            result.series_result.calculation("leading_drive_classes").state,
            CalculationState.UNRESOLVED,
        )
        self.assertEqual(
            result.series_result.calculation("leading_root_direction_evidence").state,
            CalculationState.UNRESOLVED,
        )
        self.assertTrue(
            all(
                any(
                    finding.claim_id == "IC_SZONDI_PRIMARY_000012"
                    for finding in item.interpretation.findings
                )
                for item in result.profiles
            )
        )
        unresolved_series_claim_ids = {
            item.claim_id for item in result.series_result.interpretation.unresolved
        }
        self.assertIn("IC_SZONDI_PRIMARY_000001", unresolved_series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000002", unresolved_series_claim_ids)
        self.assertTrue(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000014"
                for item in result.series_result.interpretation.findings
            )
        )

    def test_production_protocol_emits_approved_claims(self):
        series = ProfileSeries(
            tuple(profile({"s": ("negative", 0)}) for _ in range(8))
        )

        result = evaluate_clinical_protocol(series, production=True)

        self.assertTrue(
            all(
                any(
                    finding.claim_id == "IC_SZONDI_PRIMARY_000012"
                    for finding in item.interpretation.findings
                )
                for item in result.profiles
            )
        )
        series_claim_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000001", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000003", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000004", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000005", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000014", series_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000029", series_claim_ids)
        # Production gating still leaves deterministic P1 calculations intact.
        self.assertEqual(
            result.series_result.calculation("dur_moll_index").state,
            CalculationState.AVAILABLE,
        )

    def test_wrong_input_type_fails_immediately(self):
        with self.assertRaisesRegex(TypeError, "ProfileSeries"):
            evaluate_clinical_protocol(())


if __name__ == "__main__":
    unittest.main()
