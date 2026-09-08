import io
import unittest
from urllib.parse import urlencode

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_archive import SQLiteClinicalArchive
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_integration import ClinicianContextItem
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_app import ClinicianApp
from szondi3.clinician_input_editor import (
    build_clinician_input_editor,
    render_clinician_input_editor_fragment,
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


def _records(offset=0):
    return tuple(
        AdministeredTestRecord(_foreground(offset + index))
        for index in range(2)
    )


def _run(records):
    return run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


def _workspace(*, context=(), synthesis=None):
    records = _records()
    workspace = build_clinician_workspace(
        LongitudinalCaseRef(case_id="CASE-INTEGRATION", run=_run(records)),
        clinician_context=context,
        clinician_synthesis=synthesis,
    )
    return records, workspace


def _request(app, path, *, method="GET", query="", form=None):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query,
    }
    if form is not None:
        body = urlencode(form, doseq=True).encode("utf-8")
        environ.update(
            {
                "CONTENT_TYPE": "application/x-www-form-urlencoded",
                "CONTENT_LENGTH": str(len(body)),
                "wsgi.input": io.BytesIO(body),
            }
        )
    payload = b"".join(app(environ, start_response)).decode("utf-8")
    return captured, payload


class ClinicianBrowserIntegrationTests(unittest.TestCase):
    def test_live_fragment_requires_csrf_and_exposes_add_remove_controls(self):
        _, workspace = _workspace(
            context=(ClinicianContextItem(label="terapie", text="Context existent."),),
            synthesis="Sinteză existentă.",
        )
        state = build_clinician_input_editor(workspace)

        with self.assertRaises(ValueError):
            render_clinician_input_editor_fragment(
                state,
                form_action="/integration/update",
            )

        html = render_clinician_input_editor_fragment(
            state,
            form_action="/integration/update",
            csrf_token="token",
        )
        self.assertIn('action="/integration/update"', html)
        self.assertIn('name="_csrf" value="token"', html)
        self.assertIn('name="remove_context_1"', html)
        self.assertIn('name="new_context_label"', html)
        self.assertIn('name="new_context_text"', html)
        self.assertIn('name="clinician_synthesis"', html)
        self.assertIn("Aplică în workspace", html)

    def test_browser_form_applies_manual_context_and_synthesis_without_changing_szondi_outputs(self):
        _, workspace = _workspace()
        app = ClinicianApp(workspace)
        before_run = app.workspace.current.run
        before_findings = app.workspace.report.findings
        before_provenance = app.workspace.report.provenance
        before_release = app.workspace.report.release

        captured, html = _request(app, "/integration")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn('action="/integration/update"', html)
        self.assertIn(app.csrf_token, html)
        self.assertIn("numai în memoria procesului", html)

        captured, _ = _request(
            app,
            "/integration/update",
            method="POST",
            form={
                "_csrf": app.csrf_token,
                "new_context_label": "proces terapeutic",
                "new_context_text": "Material clinic introdus de clinician.",
                "clinician_synthesis": "Ipoteză de lucru formulată manual.",
            },
        )
        self.assertEqual(captured["status"], "303 See Other")
        self.assertEqual(captured["headers"]["Location"], "/integration?saved=1")
        self.assertIs(app.workspace.current.run, before_run)
        self.assertEqual(app.workspace.report.findings, before_findings)
        self.assertEqual(app.workspace.report.provenance, before_provenance)
        self.assertEqual(app.workspace.report.release, before_release)
        self.assertEqual(app.workspace.report.clinician_context[0].label, "proces terapeutic")
        self.assertEqual(
            app.workspace.report.clinician_context[0].epistemic_role,
            "EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE",
        )
        self.assertEqual(
            app.workspace.report.clinician_synthesis.text,
            "Ipoteză de lucru formulată manual.",
        )

        captured, html = _request(app, "/integration", query="saved=1")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Modificări aplicate în workspace-ul curent", html)
        self.assertIn("Material clinic introdus de clinician.", html)

    def test_existing_context_can_be_edited_removed_and_synthesis_cleared(self):
        _, workspace = _workspace(
            context=(
                ClinicianContextItem(label="unu", text="Text unu."),
                ClinicianContextItem(label="doi", text="Text doi."),
            ),
            synthesis="Sinteză de șters.",
        )
        app = ClinicianApp(workspace)

        captured, _ = _request(
            app,
            "/integration/update",
            method="POST",
            form={
                "_csrf": app.csrf_token,
                "context_label_1": "unu editat",
                "context_text_1": "Text unu editat.",
                "context_label_2": "doi",
                "context_text_2": "Text doi.",
                "remove_context_2": "1",
                "new_context_label": "",
                "new_context_text": "",
                "clinician_synthesis": "",
            },
        )
        self.assertEqual(captured["status"], "303 See Other")
        self.assertEqual(len(app.workspace.report.clinician_context), 1)
        self.assertEqual(app.workspace.report.clinician_context[0].label, "unu editat")
        self.assertEqual(app.workspace.report.clinician_context[0].text, "Text unu editat.")
        self.assertIsNone(app.workspace.report.clinician_synthesis.text)

    def test_invalid_partial_new_context_and_bad_csrf_do_not_mutate_workspace(self):
        _, workspace = _workspace()
        app = ClinicianApp(workspace)
        before = app.workspace

        captured, html = _request(
            app,
            "/integration/update",
            method="POST",
            form={
                "_csrf": app.csrf_token,
                "new_context_label": "etichetă fără text",
                "new_context_text": "",
                "clinician_synthesis": "",
            },
        )
        self.assertEqual(captured["status"], "400 Bad Request")
        self.assertIs(app.workspace, before)
        self.assertIn("sunt necesare atât eticheta, cât și textul", html)

        captured, _ = _request(
            app,
            "/integration/update",
            method="POST",
            form={
                "_csrf": "wrong",
                "new_context_label": "",
                "new_context_text": "",
                "clinician_synthesis": "",
            },
        )
        self.assertEqual(captured["status"], "403 Forbidden")
        self.assertIs(app.workspace, before)

    def test_unencrypted_archive_snapshot_is_not_rewritten_with_manual_text(self):
        records, workspace = _workspace()
        with SQLiteClinicalArchive(":memory:") as archive:
            original = archive.save(
                assessment_id="CASE-INTEGRATION",
                records=records,
                workspace=workspace,
            )
            app = ClinicianApp(workspace, archive=archive)

            captured, _ = _request(
                app,
                "/integration/update",
                method="POST",
                form={
                    "_csrf": app.csrf_token,
                    "new_context_label": "context sensibil",
                    "new_context_text": "Nu trebuie persistat în store-ul necriptat.",
                    "clinician_synthesis": "Sinteză manuală nepersistată.",
                },
            )
            self.assertEqual(captured["status"], "303 See Other")
            self.assertEqual(len(app.workspace.report.clinician_context), 1)

            archived = archive.load("CASE-INTEGRATION")
            self.assertEqual(archived.summary.payload_sha256, original.payload_sha256)
            self.assertEqual(archived.report_payload["clinician_context"], [])
            self.assertIsNone(archived.report_payload["clinician_synthesis"]["text"])
            self.assertFalse(archived.summary.manual_clinician_text_persisted)


if __name__ == "__main__":
    unittest.main()
