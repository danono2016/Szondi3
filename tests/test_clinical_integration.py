import unittest
from dataclasses import replace

from szondi3 import clinical_release
from szondi3.administration import (
    complete_foreground,
    record_foreground,
)
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_integration import (
    ClinicianContextItem,
    integrate_clinical_case,
)
from szondi3.clinical_pipeline import AdministeredTestRecord
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


class ClinicalIntegrationTests(unittest.TestCase):
    def test_single_current_case_projects_without_inventing_longitudinal_content(self):
        run = _run()
        integration = integrate_clinical_case(_ref("CURRENT", run))

        self.assertEqual(integration.assessment_ids, ("CURRENT",))
        self.assertEqual(integration.history, ())
        self.assertEqual(integration.longitudinal, ())
        self.assertEqual(integration.current.case_id, "CURRENT")
        self.assertEqual(
            integration.current.projection.release,
            run.release.manifest,
        )
        self.assertEqual(integration.clinician_context, ())
        self.assertIsNone(integration.clinician_synthesis.text)

    def test_history_is_integrated_in_supplied_order_with_adjacent_comparisons_only(self):
        a = _ref("A", _run(start_offset=0))
        b = _ref("B", _run(start_offset=1))
        c = _ref("C", _run(start_offset=2))

        integration = integrate_clinical_case(c, prior_cases=(a, b))

        self.assertEqual(integration.assessment_ids, ("A", "B", "C"))
        self.assertEqual(tuple(item.case_id for item in integration.history), ("A", "B"))
        self.assertEqual(len(integration.longitudinal), 2)
        self.assertEqual(
            (integration.longitudinal[0].case_id_a, integration.longitudinal[0].case_id_b),
            ("A", "B"),
        )
        self.assertEqual(
            (integration.longitudinal[1].case_id_a, integration.longitudinal[1].case_id_b),
            ("B", "C"),
        )

    def test_clinician_context_and_synthesis_remain_separate_from_szondi_evidence(self):
        run = _run()
        context = (
            ClinicianContextItem(
                label="therapy_context",
                text="Clinician-authored contextual note.",
            ),
        )
        integration = integrate_clinical_case(
            _ref("CURRENT", run),
            clinician_context=context,
            clinician_synthesis="Manual clinician synthesis.",
        )

        self.assertEqual(integration.clinician_context, context)
        self.assertEqual(
            integration.clinician_context[0].epistemic_role,
            "EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE",
        )
        self.assertEqual(
            integration.clinician_synthesis.authorship,
            "MANUAL_CLINICIAN_INPUT_ONLY",
        )
        self.assertEqual(
            integration.clinician_synthesis.text,
            "Manual clinician synthesis.",
        )
        self.assertEqual(
            integration.current.projection.findings,
            tuple(item for item in run.report.findings if item.scope != "EXPERIMENTAL_COMPLEMENT"),
        )
        self.assertFalse(hasattr(run.evidence_packet, "clinician_context"))

    def test_longitudinal_provenance_issues_survive_clinical_integration(self):
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

        self.assertEqual(len(integration.longitudinal), 1)
        comparison = integration.longitudinal[0]
        self.assertIn(
            "DOCTRINE_SNAPSHOT_MISMATCH",
            {item.code for item in comparison.comparability_issues},
        )
        self.assertTrue(comparison.factor_comparisons)
        self.assertTrue(comparison.vector_comparisons)

    def test_duplicate_case_identity_fails_before_clinical_integration(self):
        run_a = _run(start_offset=0)
        run_b = _run(start_offset=1)
        with self.assertRaises(ValueError):
            integrate_clinical_case(
                _ref("SAME", run_b),
                prior_cases=(_ref("SAME", run_a),),
            )

    def test_invalid_clinician_input_fails_without_repair(self):
        run = _run()
        current = _ref("CURRENT", run)

        with self.assertRaises(ValueError):
            ClinicianContextItem(label="", text="context")
        with self.assertRaises(ValueError):
            ClinicianContextItem(label="context", text="   ")
        with self.assertRaises(TypeError):
            integrate_clinical_case(current, clinician_context=(object(),))
        with self.assertRaises(ValueError):
            integrate_clinical_case(current, clinician_synthesis="   ")
        with self.assertRaises(TypeError):
            integrate_clinical_case(object())


if __name__ == "__main__":
    unittest.main()
