import json
import unittest
from dataclasses import replace

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_integration import ClinicianContextItem, integrate_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_working_report import build_clinician_working_report
from szondi3.longitudinal_comparison import LongitudinalCaseRef
from szondi3.stimuli import SERIES, presentation_rows


def _card_ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def _foreground(offset):
    choices = []
    for series in SERIES:
        cards = _card_ids(series)
        shift = offset % len(cards)
        rotated = cards[shift:] + cards[:shift]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def _run(start_offset=0):
    records = tuple(
        AdministeredTestRecord(_foreground(start_offset + index))
        for index in range(8)
    )
    return run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


def _ref(case_id, run):
    return LongitudinalCaseRef(case_id=case_id, run=run)


class ClinicianWorkingReportTests(unittest.TestCase):
    def test_working_report_preserves_current_authorized_projection(self):
        run = _run()
        integration = integrate_clinical_case(_ref("CURRENT", run))
        report = build_clinician_working_report(integration)
        projection = integration.current.projection

        self.assertEqual(report.summary.current_case_id, "CURRENT")
        self.assertEqual(report.summary.assessment_ids, ("CURRENT",))
        self.assertEqual(report.formal, projection.formal)
        self.assertEqual(report.findings, projection.findings)
        self.assertEqual(report.limits_and_anti_inferences, projection.limits_and_anti_inferences)
        self.assertEqual(report.status, projection.status)
        self.assertEqual(report.experimental_complement, projection.experimental_complement)
        self.assertEqual(report.provenance, projection.provenance)
        self.assertEqual(report.release, projection.release)
        self.assertEqual(report.technical_audit, projection.audit)
        self.assertFalse(hasattr(report, "clinical_meaning"))
        self.assertFalse(hasattr(report, "ai_synthesis"))

    def test_history_longitudinal_context_and_manual_synthesis_reach_report_separately(self):
        a = _ref("A", _run(start_offset=0))
        b = _ref("B", _run(start_offset=1))
        context = (
            ClinicianContextItem(
                label="therapy_context",
                text="Clinician-authored contextual note.",
            ),
        )
        integration = integrate_clinical_case(
            b,
            prior_cases=(a,),
            clinician_context=context,
            clinician_synthesis="Manual clinician synthesis.",
        )
        report = build_clinician_working_report(integration)

        self.assertEqual(report.summary.assessment_ids, ("A", "B"))
        self.assertEqual(report.summary.longitudinal_comparison_count, 1)
        self.assertEqual(tuple(item.case_id for item in report.historical_assessments), ("A",))
        self.assertEqual(report.longitudinal, integration.longitudinal)
        self.assertEqual(report.clinician_context, context)
        self.assertEqual(report.summary.clinician_context_count, 1)
        self.assertEqual(report.clinician_synthesis.text, "Manual clinician synthesis.")
        self.assertEqual(
            report.clinician_synthesis.authorship,
            "MANUAL_CLINICIAN_INPUT_ONLY",
        )

    def test_comparability_issues_are_counted_and_preserved_not_smoothed(self):
        run_a = _run(start_offset=0)
        run_b = _run(start_offset=1)
        altered_manifest = replace(
            run_b.release.manifest,
            doctrine_snapshot_id="different-doctrine-snapshot",
        )
        run_b = replace(
            run_b,
            release=replace(run_b.release, manifest=altered_manifest),
        )
        integration = integrate_clinical_case(
            _ref("B", run_b),
            prior_cases=(_ref("A", run_a),),
        )
        report = build_clinician_working_report(integration)

        codes = {
            issue.code
            for comparison in report.longitudinal
            for issue in comparison.comparability_issues
        }
        self.assertIn("DOCTRINE_SNAPSHOT_MISMATCH", codes)
        self.assertEqual(
            report.summary.comparability_issue_count,
            sum(len(item.comparability_issues) for item in report.longitudinal),
        )

    def test_working_report_is_json_serializable_without_losing_structured_sections(self):
        integration = integrate_clinical_case(
            _ref("CURRENT", _run()),
            clinician_context=(
                ClinicianContextItem(label="context", text="External case context."),
            ),
        )
        report = build_clinician_working_report(integration)
        payload = report.to_dict()

        json.dumps(payload, ensure_ascii=False)
        self.assertEqual(payload["summary"]["current_case_id"], "CURRENT")
        self.assertEqual(
            payload["clinician_context"][0]["epistemic_role"],
            "EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE",
        )
        self.assertIn("findings", payload)
        self.assertIn("longitudinal", payload)
        self.assertIn("provenance", payload)
        self.assertIn("release", payload)

    def test_wrong_input_type_fails(self):
        with self.assertRaises(TypeError):
            build_clinician_working_report(object())


if __name__ == "__main__":
    unittest.main()
