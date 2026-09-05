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


class ClinicalCaseRunnerEndToEndTests(unittest.TestCase):
    def test_runner_uses_the_canonical_full_release_path(self):
        foregrounds = tuple(_foreground(offset) for offset in range(8))
        records = tuple(
            AdministeredTestRecord(
                foreground,
                _complement(foreground) if index == 3 else None,
            )
            for index, foreground in enumerate(foregrounds, start=1)
        )

        run = run_clinical_case(
            records,
            git_commit_sha=clinical_release._verified_checkout_sha(),
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )

        self.assertEqual(run.evaluation.test_count, 8)
        self.assertEqual(run.report.header.profile_count, 8)
        self.assertTrue(run.report.header.production_mode)
        self.assertEqual(run.evidence_packet.report, run.report)
        self.assertEqual(run.release.evidence_packet, run.evidence_packet)
        self.assertEqual(len(run.evidence_packet.experimental_complements), 1)
        self.assertEqual(run.evidence_packet.experimental_complements[0].test_number, 3)
        self.assertTrue(
            any(
                finding.scope == "EXPERIMENTAL_COMPLEMENT"
                and finding.profile_number == 3
                for finding in run.report.findings
            )
        )
        self.assertFalse(run.release.manifest.autonomous_ai_release)
        self.assertEqual(
            run.release.manifest.synthesis_release_policy,
            "PREVIEW_ONLY_MANUAL_CLINICIAN_RELEASE",
        )


if __name__ == "__main__":
    unittest.main()
