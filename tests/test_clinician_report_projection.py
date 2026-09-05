import unittest

from szondi3 import clinical_release
from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_report_projection import project_clinician_report
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


class ClinicianReportProjectionTests(unittest.TestCase):
    def test_projection_preserves_authorized_case_outputs_in_separate_sections(self):
        foregrounds = tuple(_foreground(offset) for offset in range(8))
        records = tuple(
            AdministeredTestRecord(
                foreground,
                _complement(foreground) if number == 3 else None,
            )
            for number, foreground in enumerate(foregrounds, start=1)
        )
        run = run_clinical_case(
            records,
            git_commit_sha=clinical_release._verified_checkout_sha(),
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )

        first = project_clinician_report(run)
        second = project_clinician_report(run)
        report = run.report

        self.assertEqual(first, second)
        self.assertEqual(first.formal.header, report.header)
        self.assertEqual(first.formal.observations, report.observations)
        self.assertEqual(first.formal.calculations, report.calculations)
        self.assertEqual(first.formal.factor_series, run.evidence_packet.factor_series)
        self.assertEqual(first.formal.vector_series, run.evidence_packet.vector_series)

        expected_findings = tuple(
            item for item in report.findings if item.scope != "EXPERIMENTAL_COMPLEMENT"
        )
        expected_complement_findings = tuple(
            item for item in report.findings if item.scope == "EXPERIMENTAL_COMPLEMENT"
        )
        self.assertEqual(first.findings, expected_findings)
        self.assertEqual(first.experimental_complement.findings, expected_complement_findings)
        self.assertEqual(
            first.experimental_complement.evidence,
            run.evidence_packet.experimental_complements,
        )

        source_by_claim = {item.claim_id: item for item in report.findings}
        self.assertTrue(first.limits_and_anti_inferences)
        for boundary in first.limits_and_anti_inferences:
            source = source_by_claim[boundary.claim_id]
            self.assertEqual(boundary.statement, source.statement)
            self.assertEqual(boundary.assertion_mode, source.assertion_mode)
            self.assertEqual(boundary.anti_inference_ids, source.anti_inference_ids)
            self.assertEqual(boundary.anti_inferences, source.anti_inferences)

        self.assertEqual(first.provenance, run.evidence_packet.canonical_evidence)
        self.assertEqual(first.release, run.release.manifest)
        self.assertTrue(first.status.suppressed)
        self.assertTrue(
            all(item.activation_status == "INACTIVE" for item in first.status.suppressed)
        )

        expected_unresolved = tuple(
            item
            for item in report.uncertainties
            if item.scope != "EXPERIMENTAL_COMPLEMENT"
            and item.kind.startswith("UNRESOLVED_")
        )
        expected_blocked = tuple(
            item
            for item in report.uncertainties
            if item.scope != "EXPERIMENTAL_COMPLEMENT"
            and item.kind.startswith("BLOCKED_")
        )
        expected_complement_uncertainties = tuple(
            item
            for item in report.uncertainties
            if item.scope == "EXPERIMENTAL_COMPLEMENT"
        )
        self.assertEqual(first.status.unresolved, expected_unresolved)
        self.assertEqual(first.status.blocked, expected_blocked)
        self.assertEqual(
            first.experimental_complement.uncertainties,
            expected_complement_uncertainties,
        )


if __name__ == "__main__":
    unittest.main()
