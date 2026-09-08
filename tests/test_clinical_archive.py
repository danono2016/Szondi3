import tempfile
import unittest
from pathlib import Path

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_archive import (
    SQLiteClinicalArchive,
    administered_records_from_payload,
    administered_records_to_payload,
)
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


def _records():
    return tuple(
        AdministeredTestRecord(_foreground(index))
        for index in range(8)
    )


def _workspace(records, *, context=(), synthesis=None):
    run = run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )
    return build_clinician_workspace(
        LongitudinalCaseRef(case_id="CASE-001", run=run),
        clinician_context=context,
        clinician_synthesis=synthesis,
    )


class ClinicalArchiveTests(unittest.TestCase):
    def test_protocol_round_trip_rebuilds_canonical_administered_records(self):
        records = _records()
        payload = administered_records_to_payload(records)
        rebuilt = administered_records_from_payload(payload)
        self.assertEqual(rebuilt, records)

    def test_archive_round_trip_preserves_protocol_and_release_identity(self):
        records = _records()
        workspace = _workspace(records)
        with SQLiteClinicalArchive(":memory:") as archive:
            summary = archive.save(
                assessment_id="CASE-001",
                records=records,
                workspace=workspace,
            )
            loaded = archive.load("CASE-001")

            self.assertEqual(loaded.administered_records(), records)
            self.assertEqual(loaded.summary, summary)
            self.assertEqual(
                loaded.summary.git_commit_sha,
                workspace.report.release.git_commit_sha,
            )
            self.assertEqual(len(archive.list()), 1)

    def test_manual_clinician_text_is_not_persisted_in_unencrypted_archive(self):
        records = _records()
        workspace = _workspace(
            records,
            context=(ClinicianContextItem(label="therapy", text="Sensitive manual note."),),
            synthesis="Sensitive manual synthesis.",
        )
        with SQLiteClinicalArchive(":memory:") as archive:
            archive.save(
                assessment_id="CASE-001",
                records=records,
                workspace=workspace,
            )
            loaded = archive.load("CASE-001")

            rendered = str(loaded.report_payload)
            self.assertNotIn("Sensitive manual note.", rendered)
            self.assertNotIn("Sensitive manual synthesis.", rendered)
            self.assertEqual(loaded.report_payload["clinician_context"], [])
            self.assertIsNone(loaded.report_payload["clinician_synthesis"]["text"])
            self.assertFalse(loaded.summary.manual_clinician_text_persisted)

    def test_archive_refuses_non_pseudonymous_ids_and_overwrite(self):
        records = _records()
        workspace = _workspace(records)
        with SQLiteClinicalArchive(":memory:") as archive:
            with self.assertRaises(ValueError):
                archive.save(
                    assessment_id="Patient Name",
                    records=records,
                    workspace=workspace,
                )
            archive.save(
                assessment_id="CASE-001",
                records=records,
                workspace=workspace,
            )
            with self.assertRaises(ValueError):
                archive.save(
                    assessment_id="CASE-001",
                    records=records,
                    workspace=workspace,
                )

    def test_disk_archive_must_live_outside_repository(self):
        import szondi3.clinical_archive as module

        with self.assertRaises(ValueError):
            SQLiteClinicalArchive(module._REPO_ROOT / "forbidden-clinical.sqlite")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clinical.sqlite"
            with SQLiteClinicalArchive(path) as archive:
                self.assertEqual(archive.list(), ())
            self.assertTrue(path.exists())

    def test_archive_requires_record_count_matching_report_profiles(self):
        records = _records()
        workspace = _workspace(records)
        with SQLiteClinicalArchive(":memory:") as archive:
            with self.assertRaises(ValueError):
                archive.save(
                    assessment_id="CASE-001",
                    records=records[:-1],
                    workspace=workspace,
                )


if __name__ == "__main__":
    unittest.main()
