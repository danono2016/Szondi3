import unittest
from io import BytesIO
from urllib.parse import urlencode

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinical_report_ai import ClinicalNarrativeBlock, ClinicalReportAIResult
from szondi3.clinician_alpha_app import AlphaClinicianApp
from szondi3.clinician_alpha_report_renderer import render_clinician_alpha_report_html
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


def _run(offset=0):
    records = tuple(
        AdministeredTestRecord(_foreground(offset + index))
        for index in range(8)
    )
    return run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


def _workspace():
    return build_clinician_workspace(
        LongitudinalCaseRef(case_id="ALPHA-CASE", run=_run())
    )


def _ai_result(workspace):
    finding = next(
        item for item in workspace.report.findings
        if item.assertion_mode != "LIMITATION"
    )
    block = ClinicalNarrativeBlock(
        block_id="alpha-block-1",
        scope=finding.scope,
        profile_number=finding.profile_number,
        title="Configurația actuală a Eului",
        szondi_reading="Inflation (inflația Eului) este păstrată în formularea directă a lui Szondi.",
        clinical_formulation="Clinic, se explorează felul în care această tendință se exprimă în situația actuală.",
        exploration_questions=("Cum se manifestă această direcție în experiența actuală?",),
        relevant_limit="Această reacție nu este transformată automat într-un diagnostic contemporan.",
        support_claim_ids=(finding.claim_id,),
        support_fact_ids=finding.support_fact_ids,
        support_doctrine_ids=finding.doctrine_ids,
        anti_inference_ids_applied=finding.anti_inference_ids,
    )
    return ClinicalReportAIResult(
        contract_version="SZONDI3_CLINICAL_REPORT_ALPHA_V1",
        provider="TEST_PROVIDER",
        model="test-model",
        response_id="resp-test",
        blocks=(block,),
    )


def _get(app, path):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    payload = b"".join(
        app(
            {"REQUEST_METHOD": "GET", "PATH_INFO": path, "QUERY_STRING": ""},
            start_response,
        )
    ).decode("utf-8")
    return captured, payload


def _post(app, path, fields):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    body = urlencode(fields).encode("utf-8")
    payload = b"".join(
        app(
            {
                "REQUEST_METHOD": "POST",
                "PATH_INFO": path,
                "QUERY_STRING": "",
                "CONTENT_TYPE": "application/x-www-form-urlencoded",
                "CONTENT_LENGTH": str(len(body)),
                "wsgi.input": BytesIO(body),
            },
            start_response,
        )
    ).decode("utf-8")
    return captured, payload


class ClinicianAlphaReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = _workspace()

    def test_renderer_keeps_clinical_surface_concise_and_separates_audit(self):
        html = render_clinician_alpha_report_html(
            self.workspace,
            ai_result=_ai_result(self.workspace),
            ai_available=False,
        )
        self.assertIn("Raport clinic de lucru", html)
        self.assertIn("În termenii lui Szondi", html)
        self.assertIn("Formulare clinică", html)
        self.assertIn("De explorat clinic", html)
        self.assertIn("Inflation (inflația Eului)", html)
        self.assertIn("/report/audit", html)
        self.assertNotIn("PRODUCTION_APPROVED_CLAIMS_ONLY", html)
        self.assertNotIn("Claim-uri neactivate", html)
        self.assertNotIn("Manifest de release", html)
        self.assertNotIn("Trasabilitate doctrinară", html)
        self.assertNotIn("Forța sursei:", html)

    def test_default_report_is_alpha_and_exhaustive_report_moves_to_audit(self):
        app = AlphaClinicianApp(self.workspace)
        captured, html = _get(app, "/report")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Raport clinic de lucru", html)
        self.assertNotIn("Claim-uri neactivate", html)

        captured, audit = _get(app, "/report/audit")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Szondi3 — raport clinic de lucru", audit)
        self.assertIn("Trasabilitate tehnică", audit)

    def test_ai_generation_is_explicit_csrf_protected_and_ephemeral(self):
        calls = []
        result = _ai_result(self.workspace)

        def runner(packet):
            calls.append(packet)
            return result

        app = AlphaClinicianApp(self.workspace, ai_report_runner=runner)
        captured, before = _get(app, "/report")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Generează formularea clinică AI", before)
        self.assertNotIn(result.blocks[0].clinical_formulation, before)

        captured, _ = _post(app, "/report/ai", {"_csrf": "wrong"})
        self.assertEqual(captured["status"], "403 Forbidden")
        self.assertEqual(calls, [])

        captured, _ = _post(app, "/report/ai", {"_csrf": app.csrf_token})
        self.assertEqual(captured["status"], "303 See Other")
        self.assertEqual(captured["headers"]["Location"], "/report")
        self.assertEqual(len(calls), 1)

        captured, after = _get(app, "/report")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn(result.blocks[0].clinical_formulation, after)
        self.assertIn("Formulare asistată de AI", after)

    def test_ai_not_configured_fails_closed_without_affecting_report(self):
        app = AlphaClinicianApp(self.workspace)
        captured, html = _post(app, "/report/ai", {"_csrf": app.csrf_token})
        self.assertEqual(captured["status"], "409 Conflict")
        self.assertIn("AI nu este configurată", html)

        captured, report = _get(app, "/report")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Raport clinic de lucru", report)


if __name__ == "__main__":
    unittest.main()
