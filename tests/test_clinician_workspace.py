import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_integration import ClinicianContextItem
from szondi3.clinical_pipeline import AdministeredTestRecord
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


def _ref(case_id, run):
    return LongitudinalCaseRef(case_id=case_id, run=run)


class ClinicianWorkspaceTests(unittest.TestCase):
    def test_workspace_aligns_runtime_exploration_integration_and_report(self):
        a = _ref("A", _run(start_offset=0))
        b = _ref("B", _run(start_offset=1))

        workspace = build_clinician_workspace(b, prior_cases=(a,))

        self.assertEqual(workspace.assessment_ids, ("A", "B"))
        self.assertEqual(workspace.integration.assessment_ids, ("A", "B"))
        self.assertEqual(workspace.report.summary.assessment_ids, ("A", "B"))
        self.assertIs(workspace.assessment("B").run, b.run)
        self.assertIs(workspace.current.run, b.run)
        self.assertIs(workspace.current_exploration.run, b.run)
        self.assertFalse(hasattr(workspace.report, "run"))
        self.assertFalse(hasattr(workspace.report, "exploration"))

    def test_workspace_traces_current_active_finding_without_reconstruction(self):
        workspace = build_clinician_workspace(_ref("CURRENT", _run()))
        self.assertTrue(workspace.report.findings)
        finding = workspace.report.findings[0]

        trace = workspace.trace_current_finding(
            finding.claim_id,
            scope=finding.scope,
            profile_number=finding.profile_number,
        )

        self.assertEqual(trace.finding, finding)
        self.assertEqual(
            tuple(fact.fact_id for fact in trace.support_facts),
            finding.support_fact_ids,
        )
        self.assertEqual(
            tuple(item.doctrine_id for item in trace.doctrine_evidence),
            finding.doctrine_ids,
        )

    def test_history_assessment_keeps_its_own_exploration_index(self):
        a = _ref("A", _run(start_offset=0))
        b = _ref("B", _run(start_offset=1))
        workspace = build_clinician_workspace(b, prior_cases=(a,))

        historical = workspace.assessment("A")
        self.assertIs(historical.run, a.run)
        self.assertIs(historical.exploration.run, a.run)
        self.assertIsNot(historical.exploration.run, workspace.current_exploration.run)

    def test_clinician_input_reaches_integration_and_report_without_becoming_szondi_evidence(self):
        context = (
            ClinicianContextItem(label="therapy_context", text="Manual context."),
        )
        workspace = build_clinician_workspace(
            _ref("CURRENT", _run()),
            clinician_context=context,
            clinician_synthesis="Manual synthesis.",
        )

        self.assertEqual(workspace.integration.clinician_context, context)
        self.assertEqual(workspace.report.clinician_context, context)
        self.assertEqual(
            workspace.report.clinician_context[0].epistemic_role,
            "EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE",
        )
        self.assertEqual(workspace.report.clinician_synthesis.text, "Manual synthesis.")
        self.assertEqual(
            workspace.report.clinician_synthesis.authorship,
            "MANUAL_CLINICIAN_INPUT_ONLY",
        )

    def test_duplicate_case_identity_still_fails_at_existing_integration_boundary(self):
        run = _run()
        with self.assertRaises(ValueError):
            build_clinician_workspace(
                _ref("A", run),
                prior_cases=(_ref("A", run),),
            )

    def test_workspace_lookup_and_input_types_fail_closed(self):
        workspace = build_clinician_workspace(_ref("CURRENT", _run()))
        with self.assertRaises(KeyError):
            workspace.assessment("missing")
        with self.assertRaises(ValueError):
            workspace.assessment(" ")
        with self.assertRaises(TypeError):
            build_clinician_workspace(object())


if __name__ == "__main__":
    unittest.main()
