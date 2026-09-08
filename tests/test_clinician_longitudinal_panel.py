import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_longitudinal_panel import (
    build_clinician_longitudinal_panel,
    render_clinician_longitudinal_panel_html,
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


def _workspace_with_history():
    return build_clinician_workspace(
        LongitudinalCaseRef(case_id="B", run=_run(1)),
        prior_cases=(LongitudinalCaseRef(case_id="A", run=_run(0)),),
    )


class ClinicianLongitudinalPanelTests(unittest.TestCase):
    def test_panel_projects_existing_comparison_without_new_change_score(self):
        workspace = _workspace_with_history()
        comparison = workspace.integration.longitudinal[0]
        panel = build_clinician_longitudinal_panel(workspace)

        self.assertEqual(panel.assessment_ids, ("A", "B"))
        self.assertEqual(len(panel.pairs), 1)
        pair = panel.pairs[0]
        self.assertEqual((pair.case_id_a, pair.case_id_b), ("A", "B"))
        self.assertEqual(
            pair.comparability_issues,
            tuple((item.code, item.detail) for item in comparison.comparability_issues),
        )
        self.assertFalse(hasattr(pair, "improvement"))
        self.assertFalse(hasattr(pair, "worsening"))
        self.assertFalse(hasattr(pair, "change_score"))

    def test_factor_cells_equal_existing_symbol_sequences_profile_by_profile(self):
        workspace = _workspace_with_history()
        comparison = workspace.integration.longitudinal[0]
        panel = build_clinician_longitudinal_panel(workspace)
        pair = panel.pairs[0]

        source_by_factor = {item.factor: item for item in comparison.factor_comparisons}
        for row in pair.factor_rows:
            source = source_by_factor[row.factor]
            for change in row.reactions:
                index = change.profile_number - 1
                expected_a = (
                    source.symbol_sequence_a[index]
                    if source.symbol_sequence_a is not None and index < len(source.symbol_sequence_a)
                    else None
                )
                expected_b = (
                    source.symbol_sequence_b[index]
                    if source.symbol_sequence_b is not None and index < len(source.symbol_sequence_b)
                    else None
                )
                self.assertEqual(change.symbol_a, expected_a)
                self.assertEqual(change.symbol_b, expected_b)
                self.assertEqual(change.changed, expected_a != expected_b)

    def test_detailed_factor_differences_are_never_dropped(self):
        workspace = _workspace_with_history()
        comparison = workspace.integration.longitudinal[0]
        panel = build_clinician_longitudinal_panel(workspace)
        panel_by_factor = {item.factor: item for item in panel.pairs[0].factor_rows}

        for source in comparison.factor_comparisons:
            expected_labels = [item.label for item in source.field_diffs if not item.is_identical]
            if source.quantum_total_diff is not None and not source.quantum_total_diff.is_identical:
                expected_labels.append(source.quantum_total_diff.label)
            self.assertEqual(
                tuple(item.label for item in panel_by_factor[source.factor].detailed_changes),
                tuple(expected_labels),
            )

    def test_claim_transition_labels_are_structural_presence_or_state_changes_only(self):
        workspace = _workspace_with_history()
        comparison = workspace.integration.longitudinal[0]
        panel = build_clinician_longitudinal_panel(workspace)
        transitions = panel.pairs[0].claim_transitions

        expected = [
            item
            for item in comparison.claim_comparisons
            if item.state_changed or item.present_in_a != item.present_in_b
        ]
        self.assertEqual(len(transitions), len(expected))
        for projected, source in zip(transitions, expected):
            if not source.present_in_a and source.present_in_b:
                kind = "APPEARED"
            elif source.present_in_a and not source.present_in_b:
                kind = "DISAPPEARED"
            else:
                kind = "STATE_CHANGED"
            self.assertEqual(projected.transition_kind, kind)
            self.assertEqual(projected.claim_id, source.key.claim_id)

    def test_html_marks_structural_boundary_and_changed_cells(self):
        panel = build_clinician_longitudinal_panel(_workspace_with_history())
        html = render_clinician_longitudinal_panel_html(panel)

        self.assertIn("Comparație longitudinală", html)
        self.assertIn("A → B", html)
        self.assertIn("STRUCTURAL_COMPARISON_ONLY_NO_IMPROVEMENT_OR_WORSENING_INFERENCE", html)
        changed = [
            item
            for row in panel.pairs[0].factor_rows
            for item in row.reactions
            if item.changed
        ]
        self.assertTrue(changed)
        self.assertIn('class="changed"', html)
        self.assertIn("Diferențele sunt structurale", html)

    def test_single_assessment_has_empty_panel_without_inventing_change(self):
        workspace = build_clinician_workspace(
            LongitudinalCaseRef(case_id="ONLY", run=_run(0))
        )
        panel = build_clinician_longitudinal_panel(workspace)
        self.assertEqual(panel.pairs, ())
        html = render_clinician_longitudinal_panel_html(panel)
        self.assertIn("Nu există încă două evaluări", html)

    def test_wrong_input_types_fail_closed(self):
        with self.assertRaises(TypeError):
            build_clinician_longitudinal_panel(object())
        with self.assertRaises(TypeError):
            render_clinician_longitudinal_panel_html(object())


if __name__ == "__main__":
    unittest.main()
