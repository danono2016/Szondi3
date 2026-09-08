import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_current_case_view import (
    build_current_case_view,
    render_current_case_view_html,
)
from szondi3.clinician_workspace import build_clinician_workspace
from szondi3.longitudinal_comparison import LongitudinalCaseRef
from szondi3.profile import VECTOR_FACTORS
from szondi3.stimuli import FACTORS, SERIES, presentation_rows


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


def _workspace(case_id="CURRENT", offset=0):
    return build_clinician_workspace(
        LongitudinalCaseRef(case_id=case_id, run=_run(start_offset=offset))
    )


class ClinicianCurrentCaseViewTests(unittest.TestCase):
    def test_matrix_uses_exact_szondi_factor_and_vector_order(self):
        view = build_current_case_view(_workspace())

        self.assertEqual(view.factor_order, FACTORS)
        self.assertEqual(
            tuple((item.vector, item.factors) for item in view.vector_groups),
            VECTOR_FACTORS,
        )
        self.assertEqual(
            tuple(item.profile_number for item in view.profiles),
            tuple(range(1, 9)),
        )

    def test_cells_preserve_report_symbols_counts_quantum_and_forced_null_separately(self):
        workspace = _workspace()
        view = build_current_case_view(workspace)

        for observation, row in zip(workspace.report.formal.observations, view.profiles):
            by_factor = {item.factor: item for item in observation.factors}
            for factor in FACTORS:
                source = by_factor[factor]
                cell = row.reaction(factor)
                self.assertEqual(cell.symbol, source.symbol)
                self.assertEqual(cell.sympathetic, source.sympathetic)
                self.assertEqual(cell.unsympathetic, source.unsympathetic)
                self.assertEqual(cell.quantum_level, source.quantum_level)
                self.assertEqual(cell.forced_null, source.forced_null)

    def test_view_summary_is_projection_only(self):
        workspace = _workspace("CASE-1")
        view = build_current_case_view(workspace)

        self.assertEqual(view.case_id, "CASE-1")
        self.assertEqual(view.assessment_ids, workspace.assessment_ids)
        self.assertEqual(view.active_finding_count, workspace.report.summary.finding_count)
        self.assertEqual(view.unresolved_count, workspace.report.summary.unresolved_count)
        self.assertEqual(view.blocked_count, workspace.report.summary.blocked_count)
        self.assertFalse(hasattr(view, "clinical_meaning"))
        self.assertFalse(hasattr(view, "ai_synthesis"))

    def test_html_prioritizes_compact_matrix_and_keeps_raw_details_secondary(self):
        view = build_current_case_view(_workspace())
        html = render_current_case_view_html(view)

        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn("Profil Szondi — caz curent", html)
        self.assertIn('<table class="matrix">', html)
        for vector, _ in VECTOR_FACTORS:
            self.assertIn(f'>{vector}</th>', html)
        for factor in FACTORS:
            self.assertIn(f'<th>{factor}</th>', html)
        for row in view.profiles:
            self.assertIn(f'Detalii profil {row.profile_number}', html)
            for reaction in row.reactions:
                self.assertIn(reaction.symbol, html)
        self.assertIn(
            "Numerele brute, quantum-ul și zero-ul forțat rămân separat inspectabile.",
            html,
        )

    def test_lookup_and_wrong_types_fail_closed(self):
        view = build_current_case_view(_workspace())
        with self.assertRaises(KeyError):
            view.profile(99)
        with self.assertRaises(TypeError):
            view.profile(True)
        with self.assertRaises(TypeError):
            build_current_case_view(object())
        with self.assertRaises(TypeError):
            render_current_case_view_html(object())


if __name__ == "__main__":
    unittest.main()
