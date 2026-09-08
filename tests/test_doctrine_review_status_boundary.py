import json
import tempfile
import unittest
from pathlib import Path

from szondi3.clinical_evidence_packet import resolve_canonical_evidence


def _record(review_status: str) -> dict:
    return {
        "doctrineId": "DR_SZ_TEST_000001",
        "sourceId": "SZ_TEST",
        "sourceLayer": "SZONDI_PRIMARY",
        "sourceLanguage": "de",
        "reviewStatus": review_status,
        "sourceAnchors": [
            {
                "stream": "BODY",
                "unitStart": "U000001",
                "unitEnd": "U000001",
                "pdfPath": None,
                "printedPage": None,
                "visualArbitrationNote": None,
            }
        ],
        "sourceExcerpt": "source",
        "romanianRendering": "sursă",
        "doctrinalStatement": "statement",
        "assertionStrength": "ASSERTION",
        "scopeNotes": [],
    }


class DoctrineReviewStatusBoundaryTests(unittest.TestCase):
    def _resolve(self, status: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "test.jsonl").write_text(
                json.dumps(_record(status), ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            return resolve_canonical_evidence(
                ("DR_SZ_TEST_000001",),
                registry_root=root,
            )

    def test_source_verified_and_later_positive_review_states_remain_admissible(self):
        for status in ("SOURCE_VERIFIED", "CLINICIAN_REVIEWED", "ACCEPTED"):
            with self.subTest(status=status):
                evidence = self._resolve(status)
                self.assertEqual(evidence[0].review_status, status)

    def test_draft_unresolved_and_reopened_doctrine_fail_closed(self):
        for status in ("DRAFT_EXTRACTED", "UNRESOLVED", "REOPENED"):
            with self.subTest(status=status):
                with self.assertRaisesRegex(ValueError, "not source-verified"):
                    self._resolve(status)


if __name__ == "__main__":
    unittest.main()
