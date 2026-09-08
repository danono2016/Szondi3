import unittest
from html import escape

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_integration import ClinicianContextItem, integrate_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_working_report import build_clinician_working_report
from szondi3.clinician_working_report_renderer import render_clinician_working_report_html
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


class ClinicianWorkingReportRendererTests(unittest.TestCase):
    def test_renderer_outputs_clinician_sections_and_preserves_authorized_wording(self):
        integration = integrate_clinical_case(_ref("CURRENT", _run()))
        report = build_clinician_working_report(integration)
        before = report.to_dict()

        html = render_clinician_working_report_html(report)

        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn("Szondi3 — raport clinic de lucru", html)
        self.assertIn("CURRENT", html)
        self.assertIn("Structura formală actuală", html)
        self.assertIn("Constatări Szondiene autorizate", html)
        self.assertIn("Limite și anti-inferențe", html)
        self.assertIn("Trasabilitate doctrinară", html)
        self.assertIn("Trasabilitate tehnică", html)
        for finding in report.findings:
            self.assertIn(escape(finding.statement, quote=True), html)
            self.assertIn(escape(finding.claim_id, quote=True), html)
        self.assertEqual(report.to_dict(), before)

    def test_renderer_escapes_manual_clinician_input(self):
        integration = integrate_clinical_case(
            _ref("CURRENT", _run()),
            clinician_context=(
                ClinicianContextItem(
                    label="context <extern>",
                    text="A & B < C",
                ),
            ),
            clinician_synthesis="<script>alert('x')</script>",
        )
        report = build_clinician_working_report(integration)

        html = render_clinician_working_report_html(report)

        self.assertNotIn("<script>", html)
        self.assertIn("context &lt;extern&gt;", html)
        self.assertIn("A &amp; B &lt; C", html)
        self.assertIn("&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;", html)
        self.assertIn("EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE", html)
        self.assertIn("MANUAL_CLINICIAN_INPUT_ONLY", html)

    def test_renderer_shows_all_structural_longitudinal_differences_without_assigning_meaning(self):
        integration = integrate_clinical_case(
            _ref("B", _run(start_offset=1)),
            prior_cases=(_ref("A", _run(start_offset=0)),),
        )
        report = build_clinician_working_report(integration)
        comparison = report.longitudinal[0]

        html = render_clinician_working_report_html(report)

        self.assertIn("A → B", html)
        self.assertIn(
            "Comparație structurală; sensul clinic al schimbării nu este inferat de renderer.",
            html,
        )
        for issue in comparison.comparability_issues:
            self.assertIn(escape(issue.code, quote=True), html)
            self.assertIn(escape(issue.detail, quote=True), html)

        changed_factor_fields = []
        for factor in comparison.factor_comparisons:
            changed_factor_fields.extend(
                item.label for item in factor.field_diffs if not item.is_identical
            )
            if factor.quantum_total_diff is not None and not factor.quantum_total_diff.is_identical:
                changed_factor_fields.append(factor.quantum_total_diff.label)
        self.assertTrue(changed_factor_fields)
        self.assertIn("Diferențe factoriale detaliate", html)
        for label in changed_factor_fields:
            self.assertIn(escape(label, quote=True), html)

    def test_print_relevant_details_are_explicitly_open(self):
        report = build_clinician_working_report(
            integrate_clinical_case(_ref("CURRENT", _run()))
        )
        html = render_clinician_working_report_html(report)

        if report.provenance:
            self.assertIn('<details class="provenance" open>', html)
        if report.status.suppressed:
            self.assertIn("<details open><summary>Claim-uri neactivate", html)
        self.assertIn("<details open><summary>Manifest de release", html)
        self.assertIn("<details open><summary>Audit structural", html)

    def test_renderer_is_deterministic(self):
        report = build_clinician_working_report(
            integrate_clinical_case(_ref("CURRENT", _run()))
        )
        self.assertEqual(
            render_clinician_working_report_html(report),
            render_clinician_working_report_html(report),
        )

    def test_wrong_input_type_fails(self):
        with self.assertRaises(TypeError):
            render_clinician_working_report_html(object())


if __name__ == "__main__":
    unittest.main()
