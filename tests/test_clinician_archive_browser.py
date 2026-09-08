import unittest
from unittest.mock import patch
from urllib.parse import urlencode

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_archive import ArchivedAssessment, SQLiteClinicalArchive
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_archive_browser import ArchiveBrowsingClinicianApp
from szondi3.clinician_archive_view import (
    build_archived_assessment_view,
    render_archived_assessment_view_fragment,
)
from szondi3.clinician_workspace import build_clinician_workspace
from szondi3.longitudinal_comparison import LongitudinalCaseRef
from szondi3.stimuli import SERIES, presentation_rows


def _card_ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def _foreground(offset=0):
    choices = []
    for series in SERIES:
        cards = _card_ids(series)
        shift = offset % len(cards)
        rotated = cards[shift:] + cards[:shift]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def _records(offset=0):
    return (AdministeredTestRecord(_foreground(offset)),)


def _workspace(case_id="CASE-ARCH-001", offset=0):
    records = _records(offset)
    run = run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )
    return records, build_clinician_workspace(LongitudinalCaseRef(case_id=case_id, run=run))


def _request(app, path, query=""):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    payload = b"".join(
        app(
            {
                "REQUEST_METHOD": "GET",
                "PATH_INFO": path,
                "QUERY_STRING": query,
            },
            start_response,
        )
    ).decode("utf-8")
    return captured, payload


class ArchivedAssessmentViewTests(unittest.TestCase):
    def test_view_projects_only_checksum_verified_snapshot_content(self):
        records, workspace = _workspace()
        with SQLiteClinicalArchive(":memory:") as archive:
            archive.save(assessment_id="CASE-ARCH-001", records=records, workspace=workspace)
            archived = archive.load("CASE-ARCH-001")
            view = build_archived_assessment_view(archived)

        self.assertEqual(view.assessment_id, "CASE-ARCH-001")
        self.assertEqual(view.profile_count, 1)
        self.assertEqual(view.protocol_profile_count, 1)
        self.assertEqual(view.git_commit_sha, workspace.report.release.git_commit_sha)
        self.assertEqual(view.report_payload["clinician_context"], [])
        self.assertIsNone(view.report_payload["clinician_synthesis"]["text"])

        html = render_archived_assessment_view_fragment(view)
        self.assertIn("Snapshot istoric read-only", html)
        self.assertIn("nu rerulează protocolul", html)
        self.assertIn("Profil Szondi salvat", html)
        self.assertIn("Calcule deterministe salvate", html)
        self.assertIn("Constatări salvate", html)
        self.assertIn("Limite salvate", html)
        self.assertIn("Stări nerezolvate, blocate și neactivate", html)
        self.assertIn("Complement experimental (E.K.P.) salvat", html)
        self.assertIn("Comparații longitudinale salvate", html)
        self.assertIn("Protocol administrat", html)
        self.assertIn("Trasabilitate tehnică istorică", html)
        self.assertIn("payload_sha256", html)
        self.assertIn("Raportul JSON salvat", html)
        self.assertIn("Redactată intenționat", html)
        if workspace.report.provenance:
            first = workspace.report.provenance[0]
            self.assertIn(first.doctrine_id, html)
            self.assertIn(first.source_id, html)
            self.assertIn(first.review_status, html)
            self.assertIn(first.source_excerpt, html)
            if first.doctrinal_statement:
                self.assertIn(first.doctrinal_statement, html)

    def test_view_fails_closed_when_report_identity_diverges_from_archive_metadata(self):
        records, workspace = _workspace()
        with SQLiteClinicalArchive(":memory:") as archive:
            archive.save(assessment_id="CASE-ARCH-001", records=records, workspace=workspace)
            loaded = archive.load("CASE-ARCH-001")
        report = dict(loaded.report_payload)
        report["summary"] = dict(report["summary"])
        report["summary"]["current_case_id"] = "OTHER"
        tampered = ArchivedAssessment(
            summary=loaded.summary,
            protocol_payload=loaded.protocol_payload,
            report_payload=report,
        )
        with self.assertRaises(ValueError):
            build_archived_assessment_view(tampered)

    def test_view_fails_closed_if_manual_clinician_text_appears_in_unencrypted_snapshot(self):
        records, workspace = _workspace()
        with SQLiteClinicalArchive(":memory:") as archive:
            archive.save(assessment_id="CASE-ARCH-001", records=records, workspace=workspace)
            loaded = archive.load("CASE-ARCH-001")
        report = dict(loaded.report_payload)
        report["clinician_context"] = [{"label": "therapy", "text": "forbidden"}]
        tampered = ArchivedAssessment(
            summary=loaded.summary,
            protocol_payload=loaded.protocol_payload,
            report_payload=report,
        )
        with self.assertRaises(ValueError):
            build_archived_assessment_view(tampered)

    def test_wrong_view_types_fail_closed(self):
        with self.assertRaises(TypeError):
            build_archived_assessment_view(object())
        with self.assertRaises(TypeError):
            render_archived_assessment_view_fragment(object())


class ClinicianArchiveBrowserTests(unittest.TestCase):
    def test_archive_index_links_to_read_only_snapshot_and_detail_does_not_rerun(self):
        records, workspace = _workspace()
        with SQLiteClinicalArchive(":memory:") as archive:
            archive.save(assessment_id="CASE-ARCH-001", records=records, workspace=workspace)
            app = ArchiveBrowsingClinicianApp(None, archive=archive)

            captured, index = _request(app, "/archive")
            self.assertEqual(captured["status"], "200 OK")
            self.assertIn("Deschide snapshot-ul", index)
            self.assertIn("assessment_id=CASE-ARCH-001", index)

            with patch("szondi3.clinician_app.run_clinical_case_from_verified_checkout") as rerun:
                captured, detail = _request(
                    app,
                    "/archive/view",
                    urlencode({"assessment_id": "CASE-ARCH-001"}),
                )
            self.assertEqual(captured["status"], "200 OK")
            self.assertIn("Evaluare arhivată — CASE-ARCH-001", detail)
            self.assertIn("nu reactivează P2B", detail)
            rerun.assert_not_called()
            self.assertIsNone(app.workspace)
            self.assertEqual(app._live_runs, {})

    def test_archive_detail_unknown_bad_query_and_missing_archive_fail_closed(self):
        with SQLiteClinicalArchive(":memory:") as archive:
            app = ArchiveBrowsingClinicianApp(None, archive=archive)
            captured, _ = _request(app, "/archive/view", "")
            self.assertEqual(captured["status"], "400 Bad Request")
            captured, _ = _request(
                app,
                "/archive/view",
                urlencode({"assessment_id": "CASE-MISSING"}),
            )
            self.assertEqual(captured["status"], "404 Not Found")

        app = ArchiveBrowsingClinicianApp()
        captured, html = _request(
            app,
            "/archive/view",
            urlencode({"assessment_id": "CASE-ARCH-001"}),
        )
        self.assertEqual(captured["status"], "409 Conflict")
        self.assertIn("Arhivă indisponibilă", html)

    def test_corrupted_archived_payload_is_shown_as_invalid_not_repaired(self):
        records, workspace = _workspace()
        with SQLiteClinicalArchive(":memory:") as archive:
            archive.save(assessment_id="CASE-ARCH-001", records=records, workspace=workspace)
            archive._connection.execute(
                "UPDATE archived_assessment SET report_json = ? WHERE assessment_id = ?",
                ('{"corrupt":true}', "CASE-ARCH-001"),
            )
            archive._connection.commit()
            app = ArchiveBrowsingClinicianApp(None, archive=archive)
            captured, html = _request(
                app,
                "/archive/view",
                urlencode({"assessment_id": "CASE-ARCH-001"}),
            )
            self.assertEqual(captured["status"], "409 Conflict")
            self.assertIn("Snapshot invalid", html)
            self.assertIn("nu este rerulată sau reparată automat", html)


if __name__ == "__main__":
    unittest.main()
