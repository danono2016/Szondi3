import io
import unittest
from urllib.parse import urlencode

from szondi3.clinical_archive import SQLiteClinicalArchive
from szondi3.clinician_app import ClinicianApp


def _request(app, path, *, method="GET", form=None):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": "",
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
    payload = b"".join(app(environ, start_response))
    return captured, payload


def _start_one_profile(app, assessment_id, *, prior=()):
    form = {
        "_csrf": app.csrf_token,
        "assessment_id": assessment_id,
        "profile_count": "1",
    }
    if prior:
        form["prior_case_id"] = list(prior)
    captured, _ = _request(app, "/assessment/start", method="POST", form=form)
    assert captured["status"] == "303 See Other"


def _complete_current_foreground(app):
    last = None
    for _ in range(6):
        step = app.draft.current_step
        form = {"_csrf": app.csrf_token}
        for index, card_id in enumerate(step.card_ids):
            if index < 2:
                form[f"choice_{card_id}"] = "sympathetic"
            elif index < 4:
                form[f"choice_{card_id}"] = "unsympathetic"
            else:
                form[f"choice_{card_id}"] = ""
        last, _ = _request(app, "/admin/submit", method="POST", form=form)
    return last


class ClinicianAppEndToEndTests(unittest.TestCase):
    def test_empty_app_exposes_new_assessment_and_visual_factor_blind_stimuli(self):
        app = ClinicianApp()
        captured, payload = _request(app, "/")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Începe o evaluare nouă", payload.decode("utf-8"))

        _start_one_profile(app, "CASE-NEW-001")
        captured, payload = _request(app, "/admin")
        html = payload.decode("utf-8")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Profil 1/1", html)
        self.assertIn("seria I", html)
        self.assertIn('src="/stimulus/I-01.webp"', html)
        self.assertNotIn("I-01-k.webp", html)
        self.assertNotIn(">k<", html)

        captured, image = _request(app, "/stimulus/I-01.webp")
        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(captured["headers"]["Content-Type"], "image/webp")
        self.assertTrue(image)
        self.assertEqual(captured["headers"]["X-Frame-Options"], "DENY")

    def test_full_browser_flow_calculates_opens_workspace_and_archives_canonical_record(self):
        with SQLiteClinicalArchive(":memory:") as archive:
            app = ClinicianApp(None, archive=archive)
            _start_one_profile(app, "CASE-E2E-001")
            last = _complete_current_foreground(app)

            self.assertEqual(last["status"], "303 See Other")
            self.assertEqual(last["headers"]["Location"], "/current")
            self.assertIsNone(app.draft)
            self.assertIsNotNone(app.workspace)
            self.assertEqual(app.workspace.current.case_id, "CASE-E2E-001")
            self.assertEqual(app.workspace.report.summary.profile_count, 1)

            archived = archive.load("CASE-E2E-001")
            self.assertEqual(len(archived.administered_records()), 1)
            self.assertEqual(
                archived.summary.git_commit_sha,
                app.workspace.report.release.git_commit_sha,
            )
            self.assertFalse(archived.summary.manual_clinician_text_persisted)

            captured, payload = _request(app, "/current")
            self.assertEqual(captured["status"], "200 OK")
            self.assertIn("Profil Szondi — caz curent", payload.decode("utf-8"))

    def test_invalid_series_submission_does_not_mutate_draft(self):
        app = ClinicianApp()
        _start_one_profile(app, "CASE-BAD-001")
        before = app.draft
        step = before.current_step
        form = {
            "_csrf": app.csrf_token,
            f"choice_{step.card_ids[0]}": "sympathetic",
            f"choice_{step.card_ids[1]}": "unsympathetic",
        }
        captured, payload = _request(app, "/admin/submit", method="POST", form=form)
        self.assertEqual(captured["status"], "400 Bad Request")
        self.assertEqual(app.draft, before)
        self.assertIn("exactly two", payload.decode("utf-8"))

    def test_post_requires_process_csrf_token(self):
        app = ClinicianApp()
        captured, _ = _request(
            app,
            "/assessment/start",
            method="POST",
            form={"_csrf": "wrong", "assessment_id": "CASE-CSRF", "profile_count": "1"},
        )
        self.assertEqual(captured["status"], "403 Forbidden")
        self.assertIsNone(app.draft)

    def test_second_live_assessment_can_explicitly_select_first_for_structural_longitudinal_view(self):
        app = ClinicianApp()
        _start_one_profile(app, "CASE-LONG-001")
        _complete_current_foreground(app)
        self.assertEqual(app.workspace.current.case_id, "CASE-LONG-001")

        _start_one_profile(app, "CASE-LONG-002", prior=("CASE-LONG-001",))
        _complete_current_foreground(app)
        self.assertEqual(app.workspace.current.case_id, "CASE-LONG-002")
        self.assertEqual(tuple(item.case_id for item in app.workspace.history), ("CASE-LONG-001",))
        self.assertEqual(len(app.workspace.integration.longitudinal), 1)

    def test_existing_assessment_id_is_not_overwritten(self):
        with SQLiteClinicalArchive(":memory:") as archive:
            app = ClinicianApp(None, archive=archive)
            _start_one_profile(app, "CASE-IMMUTABLE")
            _complete_current_foreground(app)

            captured, _ = _request(
                app,
                "/assessment/start",
                method="POST",
                form={
                    "_csrf": app.csrf_token,
                    "assessment_id": "CASE-IMMUTABLE",
                    "profile_count": "1",
                },
            )
            self.assertEqual(captured["status"], "400 Bad Request")
            self.assertIsNone(app.draft)
            self.assertEqual(len(archive.list()), 1)


if __name__ == "__main__":
    unittest.main()
