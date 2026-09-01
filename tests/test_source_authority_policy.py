import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "source_catalog.json"
LOCK = ROOT / "config" / "evidence_lock.json"
POLICY = ROOT / "docs" / "SOURCE_AUTHORITY_POLICY.md"


class SourceAuthorityPolicyTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        self.policy_text = POLICY.read_text(encoding="utf-8")
        self.sources = {
            source["sourceId"]: source for source in self.catalog["sources"]
        }

    def test_pdf_and_abbyy_docx_share_primary_documentary_rank_but_pdf_wins_conflicts(self):
        authority = self.catalog["documentaryAuthorityPolicy"]

        self.assertEqual(
            authority["pdfOriginalRank"], "PRIMARY_DOCUMENTARY_EVIDENCE"
        )
        self.assertEqual(
            authority["docxOcrReplicaRank"], "PRIMARY_DOCUMENTARY_EVIDENCE"
        )
        self.assertEqual(
            authority["docxReplicaProvenance"],
            "USER_CREATED_ABBYY_FINEREADER_OCR_REPLICA_OF_AUTHENTIC_ORIGINAL_PDF",
        )
        self.assertEqual(
            authority["conflictRule"],
            "PDF_ORIGINAL_PREVAILS_OVER_DOCX_OCR_REPLICA",
        )
        self.assertTrue(authority["formatPolicyDoesNotChangeDoctrinalLayer"])

    def test_both_triebpathologie_original_pdfs_are_clinician_admitted_even_before_git_lock(self):
        expected = {
            "SZ_TRIEBPATH_1": "Szondi Triebpathologie 1. Teil.pdf",
            "SZ_TRIEBPATH_2": "Szondi Triebpathologie 2. Teil.pdf",
        }

        for source_id, title in expected.items():
            with self.subTest(source_id=source_id):
                source = self.sources[source_id]
                self.assertEqual(source["layer"], "SZONDI_PRIMARY")
                self.assertIsNone(source["pdfPath"])
                self.assertEqual(source["projectPdfTitle"], title)
                self.assertEqual(
                    source["projectPdfAuthority"],
                    "PRIMARY_DOCUMENTARY_EVIDENCE_SUPREME_ON_CONFLICT",
                )
                self.assertEqual(
                    source["pdfRepositoryStatus"],
                    "CLINICIAN_ADMITTED_PROJECT_ORIGINAL_PENDING_REPOSITORY_BINARY_LOCK",
                )

    def test_documentary_format_policy_does_not_collapse_author_layers(self):
        for source_id in (
            "SZ_SA_1948",
            "SZ_LEHR_1972",
            "SZ_IA_1956_A",
            "SZ_IA_1956_B",
            "SZ_THER_1963_A",
            "SZ_THER_1963_B",
            "SZ_TRIEBPATH_1",
            "SZ_TRIEBPATH_2",
        ):
            self.assertEqual(self.sources[source_id]["layer"], "SZONDI_PRIMARY")

        self.assertEqual(self.sources["DERI_1949"]["layer"], "POST_SZONDI_TRADITION")
        self.assertEqual(self.sources["MELON_1975"]["layer"], "POST_SZONDI_TRADITION")

    def test_repository_binary_lock_remains_distinct_from_documentary_admission(self):
        self.assertEqual(self.lock["expectedCounts"]["pdf"], 8)
        self.assertEqual(len(self.lock["pdfGitBlobs"]), 8)
        self.assertIn(
            "docs/SOURCE_AUTHORITY_POLICY.md",
            self.lock["requiredNormativeDocuments"],
        )
        self.assertIn(
            "equal documentary rank when concordant; original PDF prevails on conflict",
            self.policy_text,
        )
        self.assertIn(
            "It does **not** mean that the PDFs are doctrinally or clinically unadmitted",
            self.policy_text,
        )


if __name__ == "__main__":
    unittest.main()
