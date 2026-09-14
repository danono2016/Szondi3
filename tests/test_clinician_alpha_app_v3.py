import os
import unittest
from unittest.mock import patch

from szondi3.clinical_report_ai_v3 import run_openai_clinical_report
from szondi3.clinician_alpha_app_v3 import (
    _configured_ai_runner,
    _inject_ai_submit_feedback,
)


class ClinicianAlphaAppV3Tests(unittest.TestCase):
    def test_ai_runner_is_absent_without_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
            self.assertIsNone(_configured_ai_runner())

    def test_ai_runner_uses_plan_bound_v3_writer_when_key_exists(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}, clear=False):
            runner = _configured_ai_runner()
        self.assertIsNotNone(runner)
        self.assertIs(runner.func, run_openai_clinical_report)
        self.assertEqual(runner.keywords["api_key"], "test-secret")

    def test_report_feedback_disables_ai_button_and_explains_wait(self):
        html = '<html><body><form method="post" action="/report/ai"><button type="submit">Generează</button></form></body></html>'
        rendered = _inject_ai_submit_feedback(html)
        self.assertIn("Se generează… vă rugăm așteptați", rendered)
        self.assertIn("button.disabled = true", rendered)
        self.assertIn("aproximativ 90 de secunde", rendered)
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
