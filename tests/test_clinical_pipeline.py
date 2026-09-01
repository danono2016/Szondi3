import unittest

from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from szondi3.clinical_pipeline import (
    AdministeredTestRecord,
    evaluate_administered_tests,
    profile_from_complement,
    profile_from_foreground,
)
from szondi3.profile import DriveProfile
from szondi3.stimuli import SERIES, presentation_rows


def ids(series):
    rows = presentation_rows(series)
    return [card.card_id for row in rows for card in row]


def make_foreground(*, offset=0):
    choices = []
    for series in SERIES:
        cards = ids(series)
        # Choose four consecutive cards with a rotated starting point while
        # preserving two sympathetic + two unsympathetic and four remaining.
        rotated = cards[offset:] + cards[:offset]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def make_complement(foreground):
    choices = []
    for choice in foreground.series_choices:
        choices.append(
            record_complement(
                choice,
                selected=choice.remaining[:2],
                selected_as="unsympathetic",
            )
        )
    return complete_complement(foreground, choices)


class AdministrationToClinicalPipelineTests(unittest.TestCase):
    def test_real_foreground_administration_becomes_drive_profile_and_clinical_protocol(self):
        foreground = make_foreground()
        result = evaluate_administered_tests((AdministeredTestRecord(foreground),))

        self.assertEqual(result.test_count, 1)
        self.assertEqual(len(result.foreground_profiles), 1)
        self.assertIsInstance(result.foreground_profiles[0], DriveProfile)
        self.assertEqual(result.clinical_evaluation.profile_count, 1)
        self.assertEqual(len(result.clinical_evaluation.profiles), 1)

    def test_end_to_end_report_can_be_built_from_recorded_choices(self):
        foreground = make_foreground()
        result = evaluate_administered_tests((AdministeredTestRecord(foreground),))

        report = result.build_report(
            therapist_synthesis="Ipoteză clinică formulată manual după interviu."
        )

        self.assertEqual(report.header.profile_count, 1)
        self.assertEqual(len(report.observations), 1)
        self.assertEqual(
            report.therapist_synthesis.text,
            "Ipoteză clinică formulată manual după interviu.",
        )
        self.assertEqual(
            report.therapist_synthesis.authorship,
            "MANUAL_CLINICIAN_INPUT_ONLY",
        )

    def test_repeated_real_administrations_form_one_profile_series(self):
        records = tuple(
            AdministeredTestRecord(make_foreground(offset=offset))
            for offset in range(3)
        )
        result = evaluate_administered_tests(records)

        self.assertEqual(result.test_count, 3)
        self.assertEqual(result.clinical_evaluation.profile_count, 3)
        self.assertEqual(len(result.clinical_evaluation.profiles), 3)
        self.assertEqual(
            result.clinical_evaluation.series_result.calculation("series_indices").state.value,
            "AVAILABLE",
        )

    def test_optional_complement_gets_only_complement_specific_p2b_and_stays_out_of_foreground_series(self):
        foreground = make_foreground()
        complement = make_complement(foreground)
        result = evaluate_administered_tests(
            (AdministeredTestRecord(foreground, complement),),
            production=True,
        )

        self.assertEqual(result.test_count, 1)
        self.assertEqual(result.clinical_evaluation.profile_count, 1)
        self.assertEqual(len(result.foreground_profiles), 1)
        self.assertEqual(len(result.complement_profiles), 1)
        formal = result.complement_profiles[0]
        self.assertIsInstance(formal.profile, DriveProfile)
        self.assertEqual(
            formal.interpretation_status,
            "SOURCE_LINKED_COMPLEMENT_METHOD_ONLY",
        )
        self.assertEqual(
            tuple(item.claim_id for item in formal.interpretation.findings),
            ("IC_SZONDI_PRIMARY_000046",),
        )
        finding = formal.interpretation.findings[0]
        self.assertEqual(
            finding.doctrine_ids,
            (
                "DR_SZ_IA_1956_B_000006",
                "DR_SZ_IA_1956_B_000007",
                "DR_SZ_IA_1956_B_000009",
                "DR_SZ_IA_1956_B_000011",
                "DR_SZ_IA_1956_B_000043",
            ),
        )
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_B",))
        self.assertIn("E.K.P.", finding.statement)
        self.assertIn("Th.K.P.", finding.statement)
        self.assertIn("adevăratul Eu ascuns", finding.anti_inferences[0])
        self.assertIn("succesiune inevitabilă", finding.anti_inferences[0])
        self.assertIn("seriei libere", finding.anti_inferences[0])

        report = result.build_report()
        complement_report_findings = tuple(
            item
            for item in report.findings
            if item.scope == "EXPERIMENTAL_COMPLEMENT"
        )
        self.assertEqual(len(complement_report_findings), 1)
        self.assertEqual(complement_report_findings[0].profile_number, 1)
        self.assertEqual(
            complement_report_findings[0].claim_id,
            "IC_SZONDI_PRIMARY_000046",
        )

    def test_no_complement_means_no_complement_specific_report_finding(self):
        foreground = make_foreground()
        result = evaluate_administered_tests(
            (AdministeredTestRecord(foreground),),
            production=True,
        )
        self.assertEqual(result.complement_profiles, ())
        report = result.build_report()
        self.assertFalse(
            any(item.scope == "EXPERIMENTAL_COMPLEMENT" for item in report.findings)
        )

    def test_complement_must_belong_to_the_supplied_foreground(self):
        foreground_a = make_foreground(offset=0)
        foreground_b = make_foreground(offset=1)
        complement_a = make_complement(foreground_a)

        with self.assertRaisesRegex(ValueError, "does not belong"):
            AdministeredTestRecord(foreground_b, complement_a)

    def test_direct_profile_helpers_keep_scoring_authority_in_p1(self):
        foreground = make_foreground()
        complement = make_complement(foreground)

        foreground_profile = profile_from_foreground(foreground)
        complement_profile = profile_from_complement(foreground, complement)

        self.assertIsInstance(foreground_profile, DriveProfile)
        self.assertIsInstance(complement_profile, DriveProfile)
        self.assertEqual(len(foreground_profile.factors), 8)
        self.assertEqual(len(complement_profile.factors), 8)

    def test_empty_or_too_long_test_series_fails_before_clinical_evaluation(self):
        with self.assertRaisesRegex(ValueError, "between one and ten"):
            evaluate_administered_tests(())

        foreground = make_foreground()
        records = tuple(AdministeredTestRecord(foreground) for _ in range(11))
        with self.assertRaisesRegex(ValueError, "between one and ten"):
            evaluate_administered_tests(records)

    def test_wrong_record_type_and_wrong_profile_helper_types_fail(self):
        foreground = make_foreground()
        complement = make_complement(foreground)

        with self.assertRaisesRegex(TypeError, "AdministeredTestRecord"):
            evaluate_administered_tests((foreground,))
        with self.assertRaisesRegex(TypeError, "ForegroundProtocol"):
            profile_from_foreground(())
        with self.assertRaisesRegex(TypeError, "ForegroundProtocol"):
            profile_from_complement((), complement)
        with self.assertRaisesRegex(TypeError, "ComplementProtocol"):
            profile_from_complement(foreground, ())

    def test_production_path_emits_only_clinician_approved_claims(self):
        foreground = make_foreground()
        result = evaluate_administered_tests(
            (AdministeredTestRecord(foreground),),
            production=True,
        )
        report = result.build_report()

        self.assertTrue(report.header.production_mode)
        self.assertEqual(len(report.observations), 1)
        self.assertGreater(len(report.findings), 0)
        self.assertTrue(
            all(finding.lifecycle_status == "APPROVED" for finding in report.findings)
        )
        self.assertEqual(
            report.header.interpretation_release_state,
            "PRODUCTION_APPROVED_CLAIMS_ONLY",
        )


if __name__ == "__main__":
    unittest.main()
