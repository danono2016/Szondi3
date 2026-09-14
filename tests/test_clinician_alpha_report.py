import unittest
from io import BytesIO
from urllib.parse import urlencode

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinical_report_ai import (
    CLINICAL_REPORT_AI_CONTRACT_VERSION,
    ClinicalNarrativeBlock,
    ClinicalReportAIResult,
)
from szondi3.clinician_alpha_app import AlphaClinicianApp
from szondi3.clinician_alpha_report_renderer import (
    _clinical_statement,
    render_clinician_alpha_report_html,
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
        if item.assertion_mode != "LIMITATION" and item.scope in {"PROFILE", "SERIES"}
    )
    block = ClinicalNarrativeBlock(
        block_id="alpha-block-1",
        scope=finding.scope,
        profile_number=finding.profile_number,
        title="Configurația actuală a Eului",
        szondi_reading="Inflation (inflația Eului) este păstrată în formularea directă a lui Szondi.",
        clinical_formulation="Clinic, aceeași mișcare este explicată din mai multe unghiuri fără a adăuga o doctrină nouă.",
        exploration_questions=("Cum se manifestă această direcție în experiența actuală?",),
        relevant_limit="Această reacție nu este transformată automat într-un diagnostic contemporan.",
        support_claim_ids=(finding.claim_id,),
        support_fact_ids=finding.support_fact_ids,
        support_doctrine_ids=finding.doctrine_ids,
        anti_inference_ids_applied=finding.anti_inference_ids,
        illustrative_examples=(
            "Exemplu pur ilustrativ: o scenă imaginară poate clarifica aceeași mișcare fără a descrie persoana.",
        ),
    )
    return ClinicalReportAIResult(
        contract_version=CLINICAL_REPORT_AI_CONTRACT_VERSION,
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

    def test_renderer_keeps_clinical_surface_rich_and_separates_audit(self):
        result = _ai_result(self.workspace)
        html = render_clinician_alpha_report_html(
            self.workspace,
            ai_result=result,
            ai_available=False,
        )
        self.assertIn("Raport clinic de lucru", html)
        self.assertIn("Semnificații Szondiene autorizate", html)
        self.assertIn("În termenii lui Szondi", html)
        self.assertIn("Explicație clinică", html)
        self.assertIn("Exemple ilustrative", html)
        self.assertIn("De explorat clinic", html)
        self.assertIn("Inflation (inflația Eului)", html)
        self.assertIn(result.blocks[0].illustrative_examples[0], html)
        self.assertIn("/report/audit", html)
        self.assertNotIn("PRODUCTION_APPROVED_CLAIMS_ONLY", html)
        self.assertNotIn("Claim-uri neactivate", html)
        self.assertNotIn("Manifest de release", html)
        self.assertNotIn("Trasabilitate doctrinară", html)
        self.assertNotIn("Forța sursei:", html)

    def test_deterministic_meanings_are_visible_before_ai_and_link_to_justification(self):
        finding = next(
            item for item in self.workspace.report.findings
            if item.assertion_mode != "LIMITATION"
        )
        html = render_clinician_alpha_report_html(
            self.workspace,
            ai_result=None,
            ai_available=False,
        )
        self.assertIn(_clinical_statement(finding.statement), html)
        self.assertIn("Sursa și justificarea", html)
        self.assertIn("/finding?", html)
        self.assertIn("există independent de AI", html)

    def test_clinical_statement_removes_english_finding_leakage_only(self):
        source = "Finding-ul descrie forma Sch actuală; finding-ul rămâne testologic."
        rendered = _clinical_statement(source)
        self.assertEqual(
            rendered,
            "Constatarea descrie forma Sch actuală; constatarea rămâne testologic.",
        )
        with self.assertRaises(TypeError):
            _clinical_statement(None)

    def test_unconfigured_ai_state_remains_visible_in_printable_report(self):
        html = render_clinician_alpha_report_html(
            self.workspace,
            ai_result=None,
            ai_available=False,
        )
        self.assertIn("Lectura AI nu este inclusă.", html)
        self.assertIn("AI nu este configurată în această sesiune.", html)
        self.assertNotIn('quiet screen-only">AI nu este configurată', html)

    def test_ai_failure_summary_is_printable_but_technical_detail_is_screen_only(self):
        html = render_clinician_alpha_report_html(
            self.workspace,
            ai_result=None,
            ai_available=True,
            csrf_token="csrf-test",
            ai_error="Clinical report AI request failed with HTTP 400",
        )
        self.assertIn('<div class="error"><strong>Lectura AI nu a putut fi generată.</strong>', html)
        self.assertIn(
            '<span class="screen-only"> Clinical report AI request failed with HTTP 400</span>',
            html,
        )

    def test_print_css_keeps_deterministic_findings_together(self):
        html = render_clinician_alpha_report_html(
            self.workspace,
            ai_result=None,
            ai_available=False,
        )
        self.assertIn(
            ".interpretation,.deterministic-finding{page-break-inside:avoid;break-inside:avoid}",
            html,
        )

    def test_default_report_is_alpha_and_exhaustive_report_moves_to_audit(self):
        app = AlphaClinicianApp(self.workspace)
        captured, html = _get(app, "/report")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Raport clinic de lucru", html)
        self.assertIn("Semnificații Szondiene autorizate", html)
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
        self.assertIn("Generează lectura clinică explicată", before)
        self.assertNotIn(result.blocks[0].clinical_formulation, before)
        first_finding = next(
            item for item in self.workspace.report.findings
            if item.assertion_mode != "LIMITATION"
        )
        self.assertIn(_clinical_statement(first_finding.statement), before)

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
        self.assertIn("Lectură formulată cu AI", after)

    def test_ai_not_configured_fails_closed_without_affecting_report(self):
        app = AlphaClinicianApp(self.workspace)
        captured, html = _post(app, "/report/ai", {"_csrf": app.csrf_token})
        self.assertEqual(captured["status"], "409 Conflict")
        self.assertIn("AI nu este configurată", html)

        captured, report = _get(app, "/report")
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("Raport clinic de lucru", report)
        self.assertIn("Semnificații Szondiene autorizate", report)
        self.assertIn("Lectura AI nu este inclusă.", report)


if __name__ == "__main__":
    unittest.main()
