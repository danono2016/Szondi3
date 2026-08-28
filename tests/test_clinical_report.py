import json
import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.clinical_report import build_clinical_report
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


class ClinicalReportTests(unittest.TestCase):
    def test_report_keeps_observation_calculation_and_interpretation_separate(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries(tuple(profile({"s": ("negative", 0)}) for _ in range(8)))
        )

        report = build_clinical_report(evaluation)

        self.assertEqual(report.header.profile_count, 8)
        self.assertEqual(len(report.observations), 8)
        self.assertTrue(any(item.name == "dur_moll_index" for item in report.calculations))
        self.assertTrue(any(item.claim_id == "IC_SZONDI_PRIMARY_000001" for item in report.findings))
        self.assertIsNone(report.therapist_synthesis.text)
        self.assertEqual(
            report.therapist_synthesis.authorship,
            "MANUAL_CLINICIAN_INPUT_ONLY",
        )

    def test_report_preserves_anti_inference_and_provenance(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries((profile({"k": ("negative", 0)}),))
        )

        report = build_clinical_report(evaluation)
        finding = next(
            item for item in report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000010"
        )

        self.assertTrue(any("Verdrängung" in item for item in finding.anti_inferences))
        self.assertIn("DR_SZ_IA_1956_A_000049", finding.doctrine_ids)
        self.assertEqual(finding.scope, "PROFILE")
        self.assertEqual(finding.profile_number, 1)

    def test_unresolved_deterministic_calculation_is_visible_not_silently_removed(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries(tuple(profile({"s": ("negative", 0)}) for _ in range(8)))
        )

        report = build_clinical_report(evaluation)

        uncertainty = next(
            item for item in report.uncertainties
            if item.calculation_name == "complete_formula"
        )
        calculation = next(
            item for item in report.calculations
            if item.name == "complete_formula"
        )
        self.assertEqual(uncertainty.kind, "UNRESOLVED_CALCULATION")
        self.assertEqual(calculation.state, "UNRESOLVED")
        self.assertIsNone(calculation.value)
        self.assertTrue(calculation.note)

    def test_unresolved_interpretation_input_is_visible(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries(tuple(profile() for _ in range(8)))
        )

        report = build_clinical_report(evaluation)
        unresolved_claims = {
            item.claim_id for item in report.uncertainties if item.claim_id
        }
        self.assertIn("IC_SZONDI_PRIMARY_000001", unresolved_claims)
        self.assertIn("IC_SZONDI_PRIMARY_000002", unresolved_claims)

    def test_explicit_therapist_synthesis_is_passed_through_not_generated(self):
        evaluation = evaluate_clinical_protocol(ProfileSeries((profile(),)))
        text = "Ipoteză clinică formulată manual după integrarea interviului."

        report = build_clinical_report(evaluation, therapist_synthesis=text)

        self.assertEqual(report.therapist_synthesis.text, text)
        self.assertEqual(report.therapist_synthesis.authorship, "MANUAL_CLINICIAN_INPUT_ONLY")

    def test_preview_is_explicitly_marked_not_for_automatic_clinical_release(self):
        evaluation = evaluate_clinical_protocol(ProfileSeries((profile(),)))
        report = build_clinical_report(evaluation)

        self.assertFalse(report.header.production_mode)
        self.assertEqual(
            report.header.interpretation_release_state,
            "REVIEW_PREVIEW_NOT_FOR_AUTOMATIC_CLINICAL_RELEASE",
        )

    def test_production_report_contains_only_approved_findings(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries((profile({"k": ("negative", 0)}),)),
            production=True,
        )

        report = build_clinical_report(evaluation)

        self.assertTrue(report.header.production_mode)
        finding = next(
            item for item in report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000010"
        )
        self.assertEqual(finding.lifecycle_status, "APPROVED")
        self.assertEqual(
            report.header.interpretation_release_state,
            "PRODUCTION_APPROVED_CLAIMS_ONLY",
        )

    def test_report_to_dict_is_json_serializable_and_keeps_exact_fraction(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries(tuple(profile({"s": ("negative", 0)}) for _ in range(8)))
        )
        report = build_clinical_report(evaluation)

        payload = report.to_dict()
        encoded = json.dumps(payload, ensure_ascii=False)

        self.assertIsInstance(encoded, str)
        dur_moll = next(
            item for item in payload["calculations"]
            if item["name"] == "dur_moll_index"
        )
        self.assertEqual(dur_moll["state"], "AVAILABLE")
        # Nested P1 dataclass values are normalized and exact Fractions are not
        # silently converted to floats.
        self.assertIsInstance(dur_moll["value"], dict)

    def test_wrong_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "ClinicalProtocolEvaluation"):
            build_clinical_report(())


if __name__ == "__main__":
    unittest.main()
