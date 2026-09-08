import unittest

from szondi3.clinician_assessment_session import (
    require_pseudonymous_assessment_id,
    start_assessment_administration,
)


def _submit_foreground_step(session):
    step = session.current_step
    cards = step.card_ids
    return session.submit_foreground(
        sympathetic=cards[:2],
        unsympathetic=cards[2:4],
    )


def _submit_complement_step(session):
    step = session.current_step
    return session.submit_complement(
        selected=step.card_ids[:2],
        selected_as="unsympathetic",
    )


class AssessmentAdministrationSessionTests(unittest.TestCase):
    def test_repeats_canonical_foreground_workflow_until_target_profile_count(self):
        session = start_assessment_administration(
            assessment_id="CASE-001",
            target_profile_count=2,
        )
        self.assertEqual(session.current_profile_number, 1)
        self.assertEqual(session.current_step.series, "I")

        for _ in range(6):
            session = _submit_foreground_step(session)
        self.assertFalse(session.is_complete)
        self.assertEqual(session.completed_profile_count, 1)
        self.assertEqual(session.current_profile_number, 2)
        self.assertEqual(session.current_step.series, "I")

        for _ in range(6):
            session = _submit_foreground_step(session)
        self.assertTrue(session.is_complete)
        self.assertEqual(session.completed_profile_count, 2)
        self.assertIsNone(session.current_step)
        self.assertEqual(len(session.records()), 2)

    def test_complement_mode_completes_foreground_then_exact_remaining_cards(self):
        session = start_assessment_administration(
            assessment_id="CASE-002",
            target_profile_count=1,
            include_complement=True,
        )
        for _ in range(6):
            session = _submit_foreground_step(session)
        self.assertEqual(session.workflow.phase, "COMPLEMENT")
        self.assertEqual(len(session.current_step.card_ids), 4)

        for _ in range(6):
            session = _submit_complement_step(session)
        self.assertTrue(session.is_complete)
        record = session.records()[0]
        self.assertIsNotNone(record.complement)
        self.assertEqual(len(record.complement.relative_sympathetic), 12)
        self.assertEqual(len(record.complement.relative_unsympathetic), 12)

    def test_prior_case_ids_are_preserved_but_do_not_change_administration(self):
        session = start_assessment_administration(
            assessment_id="CASE-003",
            target_profile_count=1,
            prior_case_ids=("CASE-001", "CASE-002"),
        )
        self.assertEqual(session.prior_case_ids, ("CASE-001", "CASE-002"))
        self.assertEqual(session.current_step.series, "I")

    def test_incomplete_records_and_wrong_phase_fail_closed(self):
        session = start_assessment_administration(
            assessment_id="CASE-004",
            target_profile_count=1,
        )
        with self.assertRaises(RuntimeError):
            session.records()
        with self.assertRaises(RuntimeError):
            session.submit_complement(selected=("I-01", "I-02"), selected_as="unsympathetic")

    def test_identity_profile_count_and_prior_identity_validation(self):
        self.assertEqual(require_pseudonymous_assessment_id("PAT_A-2026.09"), "PAT_A-2026.09")
        with self.assertRaises(ValueError):
            require_pseudonymous_assessment_id("Patient Name")
        with self.assertRaises(ValueError):
            start_assessment_administration(
                assessment_id="CASE-005",
                target_profile_count=0,
            )
        with self.assertRaises(ValueError):
            start_assessment_administration(
                assessment_id="CASE-005",
                target_profile_count=1,
                prior_case_ids=("CASE-005",),
            )
        with self.assertRaises(ValueError):
            start_assessment_administration(
                assessment_id="CASE-005",
                target_profile_count=1,
                prior_case_ids=("OLD", "OLD"),
            )


if __name__ == "__main__":
    unittest.main()
