import os
import unittest
from unittest.mock import patch

from szondi3.clinician_alpha_app_v3 import (
    _AI_REQUEST_TIMEOUT_SECONDS,
    _configured_ai_runner,
    _inject_ai_submit_feedback,
    _normalize_clinician_report_language,
    _run_configured_ai,
)


class ClinicianAlphaAppV3Tests(unittest.TestCase):
    def test_ai_runner_is_absent_without_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
            self.assertIsNone(_configured_ai_runner())

    def test_ai_runner_uses_three_minute_fast_v3_wrapper_when_key_exists(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}, clear=False):
            runner = _configured_ai_runner()
        self.assertIsNotNone(runner)
        self.assertIs(runner.func, _run_configured_ai)
        self.assertEqual(runner.keywords["api_key"], "test-secret")
        self.assertEqual(_AI_REQUEST_TIMEOUT_SECONDS, 180.0)

    @patch("szondi3.clinician_alpha_app_v3.run_openai_clinical_report_fast")
    def test_configured_runner_uses_latency_tuned_transport(self, run_report):
        sentinel = object()
        run_report.return_value = sentinel
        result = _run_configured_ai("packet", api_key="test-secret")
        self.assertIs(result, sentinel)
        run_report.assert_called_once_with(
            "packet",
            api_key="test-secret",
            timeout_seconds=180.0,
        )

    def test_clinician_surface_translates_recurring_germanisms_without_touching_storage(self):
        html = (
            "<h2>Semnificații Szondiene autorizate</h2>"
            "<p>+p desemnează Inflation spre Verdoppelung, Vollkommenheit și Allessein.</p>"
            "<p>+k desemnează Introjektion, Einverleibung, Inbesitznahme și Alleshaben.</p>"
            "<p>Sch ++: kollektive Introinflation, Personabildung și Deflation prin stellungnehmendes Ich.</p>"
            "<p>C --: Kontaktsperre; narzißtische Formen des Ich-Schutzes; Triebgefahr inzestuös, bisexuell, invertiert sau pervers.</p>"
        )
        rendered = _normalize_clinician_report_language(html)
        self.assertIn("Baza interpretativă", rendered)
        self.assertIn("inflație spre dublare, perfecțiune și a fi totul", rendered)
        self.assertIn("introiecție, încorporare, luare în posesie și a avea totul", rendered)
        self.assertIn("introinflație colectivă", rendered)
        self.assertIn("formarea Personei", rendered)
        self.assertIn("deflație/limitare prin Eul care ia poziție", rendered)
        self.assertIn("blocarea contactului", rendered)
        self.assertIn("forme narcisice de protecție a Eului", rendered)
        self.assertIn("primejdie pulsională incestuoasă, bisexuală, inversată sau perversă", rendered)
        for forbidden in (
            "Inflation", "Verdoppelung", "Vollkommenheit", "Allessein",
            "Introjektion", "Einverleibung", "Inbesitznahme", "Alleshaben",
            "Introinflation", "Personabildung", "Deflation", "stellungnehmendes Ich",
            "Kontaktsperre", "Triebgefahr", "inzestuös", "bisexuell", "invertiert",
        ):
            self.assertNotIn(forbidden, rendered)

    def test_clinician_surface_uses_less_audit_like_headings(self):
        html = (
            "<p>Aceste afirmații există independent de AI și reprezintă stratul interpretativ executabil al cazului.</p>"
            "<p>Textul de mai jos face expansiune semantică numai asupra semnificațiilor deja autorizate.</p>"
            "<h4>În termenii lui Szondi</h4><strong>Limită relevantă</strong>"
        )
        rendered = _normalize_clinician_report_language(html)
        self.assertIn("Aceste sensuri sunt stabilite înaintea redactării AI", rendered)
        self.assertIn("dezvoltă numai sensurile deja stabilite pentru acest profil", rendered)
        self.assertIn("Sensul szondian", rendered)
        self.assertIn("Ce nu rezultă de aici", rendered)
        self.assertNotIn("stratul interpretativ executabil", rendered)
        self.assertNotIn("expansiune semantică", rendered)

    def test_language_normalizer_rejects_non_text(self):
        with self.assertRaises(TypeError):
            _normalize_clinician_report_language(None)

    def test_report_feedback_disables_ai_button_and_explains_wait(self):
        html = '<html><body><form method="post" action="/report/ai"><button type="submit">Generează</button></form></body></html>'
        rendered = _inject_ai_submit_feedback(html)
        self.assertIn("Se generează… vă rugăm așteptați", rendered)
        self.assertIn("button.disabled = true", rendered)
        self.assertIn("optimizată pentru latență", rendered)
        self.assertIn("aproximativ 3 minute", rendered)
        self.assertIn("form[action=\"/report/ai\"]", rendered)

    def test_report_feedback_is_injected_only_once(self):
        html = '<html><body><p>Raport</p></body></html>'
        once = _inject_ai_submit_feedback(html)
        twice = _inject_ai_submit_feedback(once)
        self.assertEqual(once, twice)
        self.assertEqual(once.count("data-ai-wait-note"), 2)

    def test_feedback_helper_rejects_non_text(self):
        with self.assertRaises(TypeError):
            _inject_ai_submit_feedback(None)


if __name__ == "__main__":
    unittest.main()
