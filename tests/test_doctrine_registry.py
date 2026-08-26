import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.validate_doctrine_registry import validate_registry


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "source_catalog.json"


def valid_entry(source_id="SZ_LEHR_1972", layer="SZONDI_PRIMARY", author="SZONDI"):
    return {
        "schemaVersion": 1,
        "doctrineId": f"DR_{source_id}_000001",
        "sourceId": source_id,
        "sourceLayer": layer,
        "authorTradition": author,
        "sourceAnchors": [
            {
                "stream": "BODY",
                "unitStart": "U000001",
                "unitEnd": "U000002",
                "pdfPath": "sources/originals/Szondi Lehrbuch der experimentellen Triebdiagnostik.pdf"
                if source_id == "SZ_LEHR_1972"
                else None,
            }
        ],
        "sourceLanguage": "de",
        "sourceExcerpt": "Begrenzter Quellenausschnitt.",
        "romanianRendering": "Redare românească fidelă.",
        "doctrinalStatement": "Afirmație doctrinară apropiată de sursă.",
        "assertionMode": ["DESCRIPTIVE_CLAIM"],
        "assertionStrength": "ASSERTION",
        "conditions": [],
        "exceptions": [],
        "scopeNotes": [],
        "terms": [],
        "historicallySensitiveTerms": [],
        "hereditaryGeneticContent": False,
        "sexualContent": False,
        "pathodiagnosticContent": False,
        "criminologicalContent": False,
        "relations": [],
        "ambiguities": [],
        "contradictions": [],
        "reviewStatus": "DRAFT_EXTRACTED",
        "reviewNotes": [],
        "executionStatus": "NOT_ASSESSED",
    }


class DoctrineRegistryValidationTests(unittest.TestCase):
    def write_registry(self, entries):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "registry.jsonl"
        path.write_text(
            "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries),
            encoding="utf-8",
        )
        self.addCleanup(temp.cleanup)
        return path

    def assert_invalid(self, entries, message_fragment):
        path = self.write_registry(entries)
        with self.assertRaisesRegex(ValueError, message_fragment):
            validate_registry([path], CATALOG)

    def test_accepts_minimal_source_near_szondi_entry(self):
        path = self.write_registry([valid_entry()])
        validate_registry([path], CATALOG)

    def test_rejects_post_szondi_author_collapsed_into_primary_layer(self):
        entry = valid_entry("DERI_1949", "SZONDI_PRIMARY", "SZONDI")
        entry["sourceAnchors"][0]["pdfPath"] = "sources/originals/Susan Deri - Szondi Introduction.pdf"
        self.assert_invalid([entry], "sourceLayer")

    def test_accepts_deri_only_as_separate_post_szondi_layer(self):
        entry = valid_entry("DERI_1949", "POST_SZONDI_TRADITION", "DERI")
        entry["sourceAnchors"][0]["pdfPath"] = "sources/originals/Susan Deri - Szondi Introduction.pdf"
        path = self.write_registry([entry])
        validate_registry([path], CATALOG)

    def test_rejects_executable_trigger_fields_in_p2a(self):
        entry = valid_entry()
        entry["triggerExpression"] = "profile.S == '+-'"
        self.assert_invalid([entry], "executable fields forbidden")

    def test_rejects_assertion_without_exact_anchor(self):
        entry = valid_entry()
        entry["sourceAnchors"] = []
        self.assert_invalid([entry], "sourceAnchors must be a non-empty array")

    def test_rejects_wrong_source_prefix_in_stable_id(self):
        entry = valid_entry()
        entry["doctrineId"] = "DR_SZ_SA_1948_000001"
        self.assert_invalid([entry], "source prefix")

    def test_rejects_duplicate_doctrine_identity(self):
        first = valid_entry()
        second = deepcopy(first)
        second["doctrinalStatement"] = "Altă afirmație cu identitate reutilizată nepermis."
        self.assert_invalid([first, second], "duplicate doctrineId")

    def test_rejects_orphan_relation_target(self):
        entry = valid_entry()
        entry["relations"] = [
            {
                "type": "QUALIFIES",
                "targetDoctrineId": "DR_SZ_SA_1948_999999",
                "note": "Legătură fără țintă prezentă.",
            }
        ]
        self.assert_invalid([entry], "orphan relation targets")

    def test_accepts_explicit_unresolved_status(self):
        entry = valid_entry()
        entry["reviewStatus"] = "UNRESOLVED"
        entry["ambiguities"] = ["Două redări rămân semantic posibile."]
        path = self.write_registry([entry])
        validate_registry([path], CATALOG)

    def test_allows_literal_hereditary_content_metadata_without_softening(self):
        entry = valid_entry()
        entry["assertionMode"] = ["HEREDITARY_GENETIC_CLAIM", "GENOTROPIC_CLAIM"]
        entry["hereditaryGeneticContent"] = True
        entry["terms"] = ["Genotropismus"]
        entry["doctrinalStatement"] = "Afirmația păstrează literal limbajul ereditar/genotropic al sursei."
        path = self.write_registry([entry])
        validate_registry([path], CATALOG)


if __name__ == "__main__":
    unittest.main()
