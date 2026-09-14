import unittest
from types import SimpleNamespace
from unittest.mock import patch

from szondi3.clinical_report_ai_fast import (
    build_openai_clinical_report_request_fast,
    request_openai_clinical_report_response_fast,
)


class ClinicalReportAIFastTests(unittest.TestCase):
    @patch("szondi3.clinical_report_ai_fast.build_clinical_report_plan")
    @patch("szondi3.clinical_report_ai_fast.build_openai_clinical_report_request_v3")
    def test_fast_profile_keeps_v3_schema_and_sets_latency_controls(
        self,
        build_v3,
        build_plan,
    ):
        base = {
            "model": "gpt-5.6-sol",
            "store": False,
            "tools": [],
            "instructions": "contract",
            "input": [],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "szondi3_clinical_report_alpha_v3",
                }
            },
        }
        build_v3.return_value = base
        build_plan.return_value = SimpleNamespace(units=(1, 2, 3, 4, 5))

        request = build_openai_clinical_report_request_fast(object())

        self.assertEqual(request["reasoning"], {"effort": "none"})
        self.assertEqual(request["text"]["verbosity"], "low")
        self.assertEqual(request["max_output_tokens"], 6000)
        self.assertEqual(
            request["text"]["format"]["name"],
            "szondi3_clinical_report_alpha_v3",
        )
        self.assertEqual(request["tools"], [])
        instructions = request["instructions"]
        self.assertIn("ROMANIAN FIRST", instructions)
        self.assertIn("Do not print the German equivalents", instructions)
        self.assertIn("Do not let every micro-scene happen in a lesson, project", instructions)
        self.assertIn("relevant_limit is not a checklist", instructions)
        self.assertIn("Never use the words finding, claim, report-plan", instructions)

    @patch("szondi3.clinical_report_ai_fast.build_clinical_report_plan")
    @patch("szondi3.clinical_report_ai_fast.build_openai_clinical_report_request_v3")
    def test_output_budget_has_safe_floor_and_ceiling(self, build_v3, build_plan):
        build_v3.return_value = {
            "instructions": "contract",
            "text": {"format": {"type": "json_schema"}},
        }

        build_plan.return_value = SimpleNamespace(units=(1,))
        small = build_openai_clinical_report_request_fast(object())
        self.assertEqual(small["max_output_tokens"], 3000)

        build_plan.return_value = SimpleNamespace(units=tuple(range(20)))
        large = build_openai_clinical_report_request_fast(object())
        self.assertEqual(large["max_output_tokens"], 12000)

    @patch("szondi3.clinical_report_ai_fast.build_openai_clinical_report_request_fast")
    @patch("szondi3.clinical_report_ai_fast.urlopen")
    def test_socket_timeout_is_exposed_as_controlled_runtime_error(
        self,
        urlopen,
        build_fast,
    ):
        build_fast.return_value = {"model": "gpt-5.6-sol"}
        urlopen.side_effect = TimeoutError("The read operation timed out")
        with self.assertRaisesRegex(RuntimeError, "configured response timeout"):
            request_openai_clinical_report_response_fast(
                object(),
                api_key="test-secret",
            )


if __name__ == "__main__":
    unittest.main()
