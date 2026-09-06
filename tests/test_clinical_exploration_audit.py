import unittest
from dataclasses import replace

from szondi3 import clinical_release
from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_exploration_audit import audit_clinical_exploration
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.stimuli import SERIES, presentation_rows


def _card_ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def _foreground(offset):
    choices = []
    for series in SERIES:
        cards = _card_ids(series)
        rotated = cards[offset:] + cards[:offset]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def _complement(foreground):
    choices = []
    for choice in foreground.series_choices:
        choices.append(
            record_complement(
                choice,
                selected=choice.remaining[:2],
                selected_as="unsympathetic",
            )
        )
    return complete_complement(foreground, choices)


def _run(with_complement=False):
    foregrounds = tuple(_foreground(offset) for offset in range(8))
    records = tuple(
        AdministeredTestRecord(
            foreground,
            _complement(foreground) if with_complement and number == 3 else None,
        )
        for number, foreground in enumerate(foregrounds, start=1)
    )
    return run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


class ClinicalExplorationAuditTests(unittest.TestCase):
    def test_audit_proves_all_active_and_nonactive_runtime_occurrences_are_navigable(self):
        run = _run()
        audit = audit_clinical_exploration(run)
        evaluation = run.evaluation.clinical_evaluation
        expected_nonactive = sum(
            len(profile.interpretation.suppressed) for profile in evaluation.profiles
        ) + len(evaluation.series_result.interpretation.suppressed)

        self.assertEqual(audit.profile_count, 8)
        self.assertEqual(audit.complement_count, 0)
        self.assertEqual(audit.finding_count, len(run.report.findings))
        self.assertEqual(audit.traced_finding_count, len(run.report.findings))
        self.assertEqual(audit.nonactive_occurrence_count, expected_nonactive)
        self.assertEqual(audit.uncertainty_count, len(run.report.uncertainties))
        self.assertGreater(audit.routed_claim_count, 0)

    def test_audit_keeps_experimental_complement_separate_and_packet_exact(self):
        run = _run(with_complement=True)
        audit = audit_clinical_exploration(run)
        complement = run.evaluation.complement_profiles[0]
        packet_complement = run.evidence_packet.experimental_complements[0]

        self.assertEqual(audit.complement_count, 1)
        self.assertEqual(complement.test_number, 3)
        self.assertEqual(packet_complement.test_number, 3)
        self.assertEqual(
            tuple(fact.fact_id for fact in complement.facts),
            tuple(fact.fact_id for fact in packet_complement.facts),
        )
        self.assertTrue(
            all(
                fact.scope == "experimental_complement_3"
                for fact in complement.facts
            )
        )
        self.assertEqual(audit.traced_finding_count, audit.finding_count)

    def test_audit_fails_closed_on_duplicate_active_finding_identity(self):
        run = _run()
        duplicate = run.report.findings[0]
        altered_report = replace(
            run.report,
            findings=run.report.findings + (duplicate,),
        )
        altered_packet = replace(run.evidence_packet, report=altered_report)
        altered_release = replace(run.release, evidence_packet=altered_packet)
        altered_run = replace(
            run,
            report=altered_report,
            evidence_packet=altered_packet,
            release=altered_release,
        )

        with self.assertRaisesRegex(ValueError, "Duplicate active finding identity"):
            audit_clinical_exploration(altered_run)

    def test_audit_fails_closed_when_packet_complement_fact_identity_diverges(self):
        run = _run(with_complement=True)
        packet_complement = run.evidence_packet.experimental_complements[0]
        first_fact = packet_complement.facts[0]
        altered_fact = replace(first_fact, fact_id="experimental_complement_3:tampered")
        altered_complement = replace(
            packet_complement,
            facts=(altered_fact,) + packet_complement.facts[1:],
        )
        altered_packet = replace(
            run.evidence_packet,
            experimental_complements=(altered_complement,),
        )
        altered_release = replace(run.release, evidence_packet=altered_packet)
        altered_run = replace(
            run,
            evidence_packet=altered_packet,
            release=altered_release,
        )

        with self.assertRaisesRegex(ValueError, "complement facts diverge"):
            audit_clinical_exploration(altered_run)

    def test_audit_requires_canonical_case_run(self):
        with self.assertRaises(TypeError):
            audit_clinical_exploration(object())


if __name__ == "__main__":
    unittest.main()
