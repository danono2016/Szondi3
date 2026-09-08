import unittest
from html import escape

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_finding_drilldown import (
    build_finding_drilldown,
    render_finding_drilldown_html,
)
from szondi3.clinician_workspace import build_clinician_workspace
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


def _workspace():
    return build_clinician_workspace(
        LongitudinalCaseRef(case_id="CURRENT", run=_run())
    )


class ClinicianFindingDrilldownTests(unittest.TestCase):
    def test_drilldown_is_exact_projection_of_existing_finding_trace(self):
        workspace = _workspace()
        finding = workspace.report.findings[0]
        trace = workspace.trace_current_finding(
            finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )

        drilldown = build_finding_drilldown(
            workspace,
            claim_id=finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )

        self.assertEqual(drilldown.statement, finding.statement)
        self.assertEqual(drilldown.key.claim_id, finding.claim_id)
        self.assertEqual(drilldown.key.scope, finding.scope)
        self.assertEqual(drilldown.key.profile_number, finding.profile_number)
        self.assertEqual(
            tuple(item.fact_id for item in drilldown.support_facts),
            finding.support_fact_ids,
        )
        self.assertEqual(
            tuple(item.fact_id for item in drilldown.support_facts),
            tuple(item.fact_id for item in trace.support_facts),
        )
        self.assertEqual(
            tuple(item.doctrine_id for item in drilldown.doctrine_support),
            finding.doctrine_ids,
        )
        self.assertEqual(
            tuple(item.doctrine_id for item in drilldown.doctrine_support),
            tuple(item.doctrine_id for item in trace.doctrine_evidence),
        )
        self.assertEqual(drilldown.anti_inferences, finding.anti_inferences)

    def test_support_facts_preserve_runtime_fact_fields(self):
        workspace = _workspace()
        finding = workspace.report.findings[0]
        trace = workspace.trace_current_finding(
            finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )
        drilldown = build_finding_drilldown(
            workspace,
            claim_id=finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )

        for source, projected in zip(trace.support_facts, drilldown.support_facts):
            self.assertEqual(projected.key, source.key)
            self.assertEqual(projected.value, source.value)
            self.assertEqual(projected.scope, source.scope)
            self.assertEqual(projected.input_state, source.input_state.value)
            self.assertEqual(projected.calculation_version, source.calculation_version)

    def test_doctrine_projection_preserves_source_excerpt_and_anchors(self):
        workspace = _workspace()
        finding = workspace.report.findings[0]
        trace = workspace.trace_current_finding(
            finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )
        drilldown = build_finding_drilldown(
            workspace,
            claim_id=finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )

        for source, projected in zip(trace.doctrine_evidence, drilldown.doctrine_support):
            self.assertEqual(projected.source_excerpt, source.source_excerpt)
            self.assertEqual(projected.doctrinal_statement, source.doctrinal_statement)
            self.assertEqual(projected.romanian_rendering, source.romanian_rendering)
            self.assertEqual(projected.assertion_strength, source.assertion_strength)
            self.assertEqual(
                tuple(item.printed_page for item in projected.anchors),
                tuple(item.printed_page for item in source.source_anchors),
            )

    def test_html_places_statement_facts_source_and_anti_inferences_in_one_trace(self):
        workspace = _workspace()
        finding = workspace.report.findings[0]
        drilldown = build_finding_drilldown(
            workspace,
            claim_id=finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )
        html = render_finding_drilldown_html(drilldown)

        self.assertIn("De ce apare?", html)
        self.assertIn(escape(finding.statement, quote=True), html)
        self.assertIn("Faptele care au activat constatarea", html)
        self.assertIn("Doctrina și sursa", html)
        self.assertIn("Ce nu autorizează constatarea", html)
        for item in drilldown.support_facts:
            self.assertIn(escape(item.fact_id, quote=True), html)
        for item in drilldown.doctrine_support:
            self.assertIn(escape(item.doctrine_id, quote=True), html)
            self.assertIn(escape(item.source_excerpt, quote=True), html)
        for item in drilldown.anti_inferences:
            self.assertIn(escape(item, quote=True), html)

    def test_unknown_or_wrong_scope_fails_at_existing_trace_boundary(self):
        workspace = _workspace()
        with self.assertRaises(KeyError):
            build_finding_drilldown(
                workspace,
                claim_id="IC_DOES_NOT_EXIST",
                scope="SERIES",
            )
        with self.assertRaises(ValueError):
            build_finding_drilldown(
                workspace,
                claim_id=workspace.report.findings[0].claim_id,
                scope="UNKNOWN",
            )

    def test_wrong_input_types_fail_closed(self):
        with self.assertRaises(TypeError):
            build_finding_drilldown(
                object(),
                claim_id="IC",
                scope="SERIES",
            )
        with self.assertRaises(TypeError):
            render_finding_drilldown_html(object())


if __name__ == "__main__":
    unittest.main()
