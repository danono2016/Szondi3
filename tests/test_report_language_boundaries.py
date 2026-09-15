import unittest

from szondi3.clinician_alpha_app_v3 import _normalize_clinician_report_language


class ReportLanguageBoundaryTests(unittest.TestCase):
    def test_standalone_source_term_normalizes_without_corrupting_romanian_noun(self):
        html = "<p>pervers; perversiune.</p>"

        rendered = _normalize_clinician_report_language(html)

        self.assertEqual(rendered, "<p>perversă; perversiune.</p>")
        self.assertNotIn("perversăiune", rendered)

    def test_already_normalized_romanian_adjective_is_not_rewritten(self):
        html = "<p>perversă, pervers.</p>"

        rendered = _normalize_clinician_report_language(html)

        self.assertEqual(rendered, "<p>perversă, perversă.</p>")
        self.assertNotIn("perversăă", rendered)


if __name__ == "__main__":
    unittest.main()
