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
        self.assertEqual(response["output_text"], '{"text":"Allessein, Introjektion și Kontaktsperre"}')

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


if __name__ == "__main__":
    unittest.main()
