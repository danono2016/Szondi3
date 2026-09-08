import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_integration import ClinicianContextItem
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_input_editor import (
    apply_clinician_input_editor,
    build_clinician_input_editor,
    render_clinician_input_editor_html,
    update_clinician_input_editor,
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
        LongitudinalCaseRef(case_id="B", run=_run(1)),
        prior_cases=(LongitudinalCaseRef(case_id="A", run=_run(0)),),
    )


class ClinicianInputEditorTests(unittest.TestCase):
    def test_editor_reads_existing_manual_input_only(self):
        context = (ClinicianContextItem(label="therapy", text="Existing context."),)
        workspace = build_clinician_workspace(
            LongitudinalCaseRef(case_id="CURRENT", run=_run()),
            clinician_context=context,
            clinician_synthesis="Existing synthesis.",
        )
        state = build_clinician_input_editor(workspace)

        self.assertEqual(state.clinician_context, context)
        self.assertEqual(state.clinician_synthesis, "Existing synthesis.")
        self.assertEqual(
            state.context_epistemic_role,
            "EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE",
        )
        self.assertEqual(state.synthesis_authorship, "MANUAL_CLINICIAN_INPUT_ONLY")

    def test_applying_edits_preserves_exact_case_run_objects_and_szondi_outputs(self):
        workspace = _workspace()
        before_findings = workspace.report.findings
        before_provenance = workspace.report.provenance
        before_release = workspace.report.release
        before_current_run = workspace.current.run
        before_history_runs = tuple(item.run for item in workspace.history)

        state = build_clinician_input_editor(workspace)
        state = update_clinician_input_editor(
            state,
            clinician_context=(
                ClinicianContextItem(label="therapy", text="New clinician context."),
            ),
            clinician_synthesis="New clinician synthesis.",
        )
        updated = apply_clinician_input_editor(workspace, state)

        self.assertIs(updated.current.run, before_current_run)
        self.assertEqual(tuple(item.run for item in updated.history), before_history_runs)
        self.assertEqual(updated.report.findings, before_findings)
        self.assertEqual(updated.report.provenance, before_provenance)
        self.assertEqual(updated.report.release, before_release)
        self.assertEqual(updated.report.clinician_context, state.clinician_context)
        self.assertEqual(updated.report.clinician_synthesis.text, "New clinician synthesis.")

    def test_clear_synthesis_is_explicit_and_context_can_be_replaced_independently(self):
        workspace = build_clinician_workspace(
            LongitudinalCaseRef(case_id="CURRENT", run=_run()),
            clinician_synthesis="To be cleared.",
        )
        state = build_clinician_input_editor(workspace)
        state = update_clinician_input_editor(
            state,
            clinician_context=(ClinicianContextItem(label="new", text="Context."),),
            clear_synthesis=True,
        )
        updated = apply_clinician_input_editor(workspace, state)

        self.assertIsNone(updated.report.clinician_synthesis.text)
        self.assertEqual(updated.report.clinician_context[0].text, "Context.")

    def test_editor_refuses_ambiguous_set_and_clear_or_invalid_input(self):
        state = build_clinician_input_editor(_workspace())
        with self.assertRaises(ValueError):
            update_clinician_input_editor(
                state,
                clinician_synthesis="text",
                clear_synthesis=True,
            )
        with self.assertRaises(ValueError):
            update_clinician_input_editor(state, clinician_synthesis="   ")
        with self.assertRaises(TypeError):
            update_clinician_input_editor(state, clinician_context=(object(),))

    def test_html_labels_manual_material_as_outside_szondi_evidence_chain(self):
        state = update_clinician_input_editor(
            build_clinician_input_editor(_workspace()),
            clinician_context=(
                ClinicianContextItem(label="therapy", text="Clinician text."),
            ),
            clinician_synthesis="Manual synthesis.",
        )
        html = render_clinician_input_editor_html(state)

        self.assertIn("Integrare clinică manuală", html)
        self.assertIn("EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE", html)
        self.assertIn("MANUAL_CLINICIAN_INPUT_ONLY", html)
        self.assertIn("Clinician text.", html)
        self.assertIn("Manual synthesis.", html)
        self.assertIn("nu devin fapte Szondi", html)
        self.assertNotIn("name=\"diagnosis\"", html)

    def test_wrong_types_fail_closed(self):
        with self.assertRaises(TypeError):
            build_clinician_input_editor(object())
        with self.assertRaises(TypeError):
            apply_clinician_input_editor(object(), build_clinician_input_editor(_workspace()))
        with self.assertRaises(TypeError):
            render_clinician_input_editor_html(object())


if __name__ == "__main__":
    unittest.main()
