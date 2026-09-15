import json
import unittest

from szondi3.clinician_alpha_app_v4 import _normalize_provider_response_language


class ClinicianAlphaAppV4LanguageTests(unittest.TestCase):
    def test_known_german_terms_are_translated_before_v4_validation(self):
        response = {
            "id": "resp-language-direct",
            "model": "gpt-5.6-sol",
            "status": "completed",
            "output_text": '{"text":"Allessein, Introjektion și Kontaktsperre"}',
        }
        normalized = _normalize_provider_response_language(response)
        self.assertIn("a fi totul", normalized["output_text"])
        self.assertIn("introiecție", normalized["output_text"])
        self.assertIn("blocarea contactului", normalized["output_text"])
        self.assertNotIn("Allessein", normalized["output_text"])
        self.assertEqual(
            response["output_text"],
            '{"text":"Allessein, Introjektion și Kontaktsperre"}',
        )

    def test_nested_responses_api_output_is_normalized_into_output_text(self):
        response = {
            "id": "resp-language-nested",
            "model": "gpt-5.6-sol",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": '{"text":"Verdoppelung și Vollkommenheit"}',
                        }
                    ],
                }
            ],
        }
        normalized = _normalize_provider_response_language(response)
        self.assertIn("dublare", normalized["output_text"])
        self.assertIn("perfecțiune", normalized["output_text"])
        self.assertNotIn("Verdoppelung", normalized["output_text"])

    def test_known_misplaced_kind_is_not_repaired_before_parser(self):
        payload = {
            "summary": [
                {
                    "item_id": "S1",
                    "unit_id": "U1",
                    "kind": "LIMIT",
                    "text": "Rezumat.",
                }
            ],
            "sections": [],
            "global_questions": [],
            "closing_limits": [],
            "appendix_only_unit_ids": [],
        }
        response = {
            "id": "resp-role-kinds",
            "model": "gpt-5.6-sol",
            "status": "completed",
            "output_text": json.dumps(payload, ensure_ascii=False),
        }

        normalized = _normalize_provider_response_language(response)
        decoded = json.loads(normalized["output_text"])
        self.assertEqual(decoded["summary"][0]["kind"], "LIMIT")
        self.assertEqual(decoded["summary"][0]["text"], "Rezumat.")

    def test_unknown_body_kind_is_not_silently_rewritten(self):
        payload = {
            "summary": [],
            "sections": [
                {
                    "section_id": "SEC1",
                    "title": "Secțiune",
                    "lead_unit_id": "U1",
                    "passages": [
                        {
                            "item_id": "P1",
                            "unit_id": "U1",
                            "kind": "UNKNOWN",
                            "text": "Text.",
                        }
                    ],
                }
            ],
            "global_questions": [],
            "closing_limits": [],
            "appendix_only_unit_ids": [],
        }
        response = {
            "id": "resp-unknown-kind",
            "model": "gpt-5.6-sol",
            "status": "completed",
            "output_text": json.dumps(payload, ensure_ascii=False),
        }

        normalized = _normalize_provider_response_language(response)
        decoded = json.loads(normalized["output_text"])
        self.assertEqual(decoded["sections"][0]["passages"][0]["kind"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
