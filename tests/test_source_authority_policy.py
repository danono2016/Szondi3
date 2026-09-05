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

    def test_both_triebpathologie_original_pdfs_are_clinician_admitted_and_git_locked(self):
        expected = {
            "SZ_TRIEBPATH_1": (
                "Szondi Triebpathologie 1. Teil.pdf",
                "sources/originals/Szondi Triebpathologie 1. Teil.pdf",
                "de905f28eb96b9da40bd4f6ce7e1cc852c94fe88",
            ),
            "SZ_TRIEBPATH_2": (
                "Szondi Triebpathologie 2. Teil.pdf",
                "sources/originals/Szondi Triebpathologie 2. Teil.pdf",
                "0ed487efd94788c13651032479b2278eabde49f5",
            ),
        }

        for source_id, (title, pdf_path, blob_sha) in expected.items():
            with self.subTest(source_id=source_id):
                source = self.sources[source_id]
                self.assertEqual(source["layer"], "SZONDI_PRIMARY")
                self.assertEqual(source["pdfPath"], pdf_path)
                self.assertEqual(source["projectPdfTitle"], title)
                self.assertEqual(
                    source["projectPdfAuthority"],
                    "PRIMARY_DOCUMENTARY_EVIDENCE_SUPREME_ON_CONFLICT",
                )
                self.assertEqual(
                    source["pdfRepositoryStatus"],
                    "REPOSITORY_BINARY_LOCKED",
                )
                self.assertEqual(self.lock["pdfGitBlobs"][pdf_path], blob_sha)

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
        self.assertEqual(self.lock["expectedCounts"]["pdf"], 10)
        self.assertEqual(len(self.lock["pdfGitBlobs"]), 10)
        self.assertIn(
            "docs/SOURCE_AUTHORITY_POLICY.md",
            self.lock["requiredNormativeDocuments"],
        )
        self.assertIn(
            "equal documentary rank when concordant; original PDF prevails on conflict",
            self.policy_text,
        )
        for source_id in ("SZ_TRIEBPATH_1", "SZ_TRIEBPATH_2"):
            source = self.sources[source_id]
            self.assertEqual(
                source["projectPdfAuthority"],
                "PRIMARY_DOCUMENTARY_EVIDENCE_SUPREME_ON_CONFLICT",
            )
            self.assertEqual(source["pdfRepositoryStatus"], "REPOSITORY_BINARY_LOCKED")


if __name__ == "__main__":
    unittest.main()
