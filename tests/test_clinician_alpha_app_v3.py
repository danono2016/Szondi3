import os
import unittest
from unittest.mock import patch

from szondi3.clinician_alpha_app_v3 import (
    _AI_REQUEST_TIMEOUT_SECONDS,
    _configured_ai_runner,
    _inject_ai_submit_feedback,
    _run_configured_ai,
)


class ClinicianAlphaAppV3Tests(unittest.TestCase):
    def test_ai_runner_is_absent_without_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
            self.assertIsNone(_configured_ai_runner())

    def test_ai_runner_uses_three_minute_v3_wrapper_when_key_exists(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}, clear=False):
            runner = _configured_ai_runner()
        self.assertIsNotNone(runner)
        self.assertIs(runner.func, _run_configured_ai)
        self.assertEqual(runner.keywords["api_key"], "test-secret")
        self.assertEqual(_AI_REQUEST_TIMEOUT_SECONDS, 180.0)

    @patch("szondi3.clinician_alpha_app_v3.run_openai_clinical_report")
    def test_configured_runner_passes_extended_timeout(self, run_report):
        sentinel = object()
        run_report.return_value = sentinel
        result = _run_configured_ai("packet", api_key="test-secret")
        self.assertIs(result, sentinel)
        run_report.assert_called_once_with(
            "packet",
            api_key="test-secret",
            timeout_seconds=180.0,
        )

    @patch("szondi3.clinician_alpha_app_v3.run_openai_clinical_report")
    def test_socket_timeout_becomes_catchable_runtime_error(self, run_report):
        run_report.side_effect = TimeoutError("The read operation timed out")
        with self.assertRaisesRegex(RuntimeError, "depășit timpul maxim de așteptare"):
            _run_configured_ai("packet", api_key="test-secret")

    def test_report_feedback_disables_ai_button_and_explains_wait(self):
        html = '<html><body><form method="post" action="/report/ai"><button type="submit">Generează</button></form></body></html>'
        rendered = _inject_ai_submit_feedback(html)
        self.assertIn("Se generează… vă rugăm așteptați", rendered)
        self.assertIn("button.disabled = true", rendered)
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
