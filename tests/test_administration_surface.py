import unittest
from dataclasses import replace

from szondi3.administration_surface import AdministrationWorkflow, start_administration
from szondi3.stimuli import SERIES, presentation_rows


def complete_foreground(workflow):
    for _ in SERIES:
        step = workflow.current_step
        cards = step.card_ids
        workflow = workflow.submit_foreground(
            sympathetic=cards[:2],
            unsympathetic=cards[2:4],
        )
    return workflow


class AdministrationSurfaceTests(unittest.TestCase):
    def test_starts_with_series_i_and_source_defined_two_row_presentation(self):
        workflow = start_administration()
        step = workflow.current_step

        self.assertEqual(workflow.phase, "FOREGROUND")
        self.assertEqual(step.series, "I")
        self.assertEqual(step.phase, "FOREGROUND")
        self.assertEqual(tuple(len(row) for row in step.presentation_rows), (4, 4))
        self.assertEqual(
            step.card_ids,
            tuple(
                card.card_id
                for row in presentation_rows("I")
                for card in row
            ),
        )
        self.assertEqual(workflow.progress.completed_steps, 0)
        self.assertEqual(workflow.progress.total_steps, 6)
        self.assertEqual(workflow.progress.current_series, "I")

    def test_valid_foreground_submission_advances_progress_to_next_series(self):
        workflow = start_administration()
        cards = workflow.current_step.card_ids

        advanced = workflow.submit_foreground(
            sympathetic=cards[:2],
            unsympathetic=cards[2:4],
        )

        self.assertEqual(workflow.progress.completed_steps, 0)
        self.assertEqual(advanced.progress.completed_steps, 1)
        self.assertEqual(advanced.progress.foreground_completed, 1)
        self.assertEqual(advanced.current_step.series, "II")

    def test_invalid_foreground_submission_fails_without_mutating_state(self):
        workflow = start_administration()
        cards = workflow.current_step.card_ids

        with self.assertRaises(ValueError):
            workflow.submit_foreground(
                sympathetic=cards[:1],
                unsympathetic=cards[2:4],
            )

        self.assertEqual(workflow.phase, "FOREGROUND")
        self.assertEqual(workflow.progress.completed_steps, 0)
        self.assertEqual(workflow.current_step.series, "I")

    def test_foreground_only_workflow_closes_as_canonical_administered_record(self):
        workflow = complete_foreground(start_administration())

        self.assertEqual(workflow.phase, "COMPLETE")
        self.assertTrue(workflow.progress.is_complete)
        self.assertIsNone(workflow.current_step)
        self.assertEqual(workflow.progress.completed_steps, 6)

        record = workflow.build_record()
        self.assertEqual(
            tuple(choice.series for choice in record.foreground.series_choices),
            SERIES,
        )
        self.assertIsNone(record.complement)

    def test_complement_phase_exposes_exactly_the_four_remaining_cards(self):
        workflow = complete_foreground(start_administration(include_complement=True))
        step = workflow.current_step
        first_foreground = workflow.foreground_choices[0]

        self.assertEqual(workflow.phase, "COMPLEMENT")
        self.assertEqual(step.phase, "COMPLEMENT")
        self.assertEqual(step.series, "I")
        self.assertEqual(step.card_ids, first_foreground.remaining)
        self.assertEqual(len(step.cards), 4)
        self.assertIsNone(step.presentation_rows)
        self.assertEqual(workflow.progress.completed_steps, 6)
        self.assertEqual(workflow.progress.total_steps, 12)

    def test_invalid_complement_submission_fails_without_mutating_state(self):
        workflow = complete_foreground(start_administration(include_complement=True))
        forbidden = workflow.foreground_choices[0].sympathetic[0]
        remaining = workflow.current_step.card_ids

        with self.assertRaises(ValueError):
            workflow.submit_complement(
                selected=(remaining[0], forbidden),
                selected_as="unsympathetic",
            )

        self.assertEqual(workflow.phase, "COMPLEMENT")
        self.assertEqual(workflow.progress.complement_completed, 0)
        self.assertEqual(workflow.current_step.series, "I")

    def test_complement_workflow_closes_as_paired_administered_record(self):
        workflow = complete_foreground(start_administration(include_complement=True))

        for _ in SERIES:
            cards = workflow.current_step.card_ids
            workflow = workflow.submit_complement(
                selected=cards[:2],
                selected_as="unsympathetic",
            )

        self.assertEqual(workflow.phase, "COMPLETE")
        self.assertEqual(workflow.progress.completed_steps, 12)
        record = workflow.build_record()
        self.assertIsNotNone(record.complement)
        self.assertEqual(
            tuple(choice.series for choice in record.complement.series_choices),
            SERIES,
        )

    def test_workflow_rejects_out_of_order_rehydrated_choices(self):
        workflow = start_administration()
        cards = workflow.current_step.card_ids
        workflow = workflow.submit_foreground(
            sympathetic=cards[:2],
            unsympathetic=cards[2:4],
        )
        malformed = replace(workflow.foreground_choices[0], series="II")

        with self.assertRaisesRegex(ValueError, "series I-VI in order"):
            AdministrationWorkflow(foreground_choices=(malformed,))

    def test_record_cannot_be_built_before_administration_is_complete(self):
        with self.assertRaisesRegex(RuntimeError, "must be complete"):
            start_administration().build_record()


if __name__ == "__main__":
    unittest.main()
