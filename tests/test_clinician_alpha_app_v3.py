import os
import unittest
from unittest.mock import patch

from szondi3.clinical_report_ai_v3 import run_openai_clinical_report
from szondi3.clinician_alpha_app_v3 import _configured_ai_runner


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


if __name__ == "__main__":
    unittest.main()
