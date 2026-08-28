import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.validate_transversal_doctrine import validate_transversal_layer


ROOT = Path(__file__).resolve().parents[1]


class TransversalDoctrineValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.registry_dir = self.root / "registry"
        self.registry_dir.mkdir()
        self.write_jsonl(
            self.registry_dir / "lehr.jsonl",
            [{"doctrineId": "DR_SZ_LEHR_1972_000001"}, {"doctrineId": "DR_SZ_LEHR_1972_000002"}],
        )
        self.write_jsonl(
            self.registry_dir / "ia.jsonl",
            [{"doctrineId": "DR_SZ_IA_1956_A_000001"}, {"doctrineId": "DR_SZ_IA_1956_B_000001"}],
        )
        self.concepts = self.root / "concepts.jsonl"
        self.relations = self.root / "cross_source.jsonl"
        self.questions = self.root / "open_questions.jsonl"

    def write_jsonl(self, path, entries):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries),
            encoding="utf-8",
        )

    def registry_paths(self):
        return sorted(self.registry_dir.glob("*.jsonl"))

    def validate(self):
        return validate_transversal_layer(
            registry_paths=self.registry_paths(),
            concepts_path=self.concepts,
            relations_path=self.relations,
            open_questions_path=self.questions,
        )

    def valid_concept(self):
        return {
            "schemaVersion": 1,
            "conceptId": "DC_000001",
            "preferredLabel": "Negation / Verdrängung",
            "retrievalLabels": ["Negation versus Verdrängung"],
            "germanTerms": ["Negation", "Verdrängung"],
            "romanianLabels": ["negație", "refulare"],
            "aliases": [],
            "linkedDoctrineIds": [
                "DR_SZ_LEHR_1972_000001",
                "DR_SZ_IA_1956_A_000001",
            ],
            "sourceIds": ["SZ_LEHR_1972", "SZ_IA_1956_A"],
            "broaderConceptIds": [],
            "narrowerConceptIds": [],
            "chronologyNotes": [],
            "terminologyNotes": ["Retrieval label only; no normalized modern definition."],
            "unresolvedNotes": [],
            "reviewStatus": "PROPOSED",
        }

    def valid_relation(self):
        return {
            "schemaVersion": 1,
            "relationId": "XR_000001",
            "relationType": "QUALIFIES",
            "fromDoctrineId": "DR_SZ_IA_1956_A_000001",
            "toDoctrineId": "DR_SZ_LEHR_1972_000001",
            "direction": "DIRECTED",
            "relationScope": ["historical_revision"],
            "rationale": "Later primary doctrine qualifies the narrower earlier formulation.",
            "epistemicStatus": "INTEGRATION_INFERRED",
            "chronologyNotes": ["Chronology is recorded but does not by itself erase the earlier doctrine."],
            "evidenceReview": {
                "fromCanonicalReconsulted": False,
                "toCanonicalReconsulted": False,
                "fromPdfReconsulted": False,
                "toPdfReconsulted": False,
                "visualArbitrationRequired": False,
                "reviewNotes": [],
            },
            "reviewStatus": "PROPOSED",
            "notes": [],
        }

    def valid_question(self):
        return {
            "schemaVersion": 1,
            "questionId": "UQ_000001",
            "topic": "Scope of Sch terminology across works",
            "implicatedDoctrineIds": [
                "DR_SZ_LEHR_1972_000001",
                "DR_SZ_IA_1956_B_000001",
            ],
            "issue": "The relation type cannot yet be chosen safely.",
            "evidenceNeeded": ["Reconsult both canonical contexts."],
            "currentEvidence": [],
            "status": "OPEN",
            "notes": [],
        }

    def test_missing_transversal_files_are_valid_before_integration_starts(self):
        self.assertEqual(self.validate(), (0, 0, 0))

    def test_accepts_minimal_cross_source_concept(self):
        self.write_jsonl(self.concepts, [self.valid_concept()])
        self.assertEqual(self.validate(), (1, 0, 0))

    def test_rejects_concept_source_ids_not_derived_from_linked_doctrine(self):
        concept = self.valid_concept()
        concept["sourceIds"] = ["SZ_LEHR_1972"]
        self.write_jsonl(self.concepts, [concept])
        with self.assertRaisesRegex(ValueError, "sourceIds must exactly match"):
            self.validate()

    def test_rejects_orphan_concept_hierarchy_link(self):
        concept = self.valid_concept()
        concept["broaderConceptIds"] = ["DC_999999"]
        self.write_jsonl(self.concepts, [concept])
        with self.assertRaisesRegex(ValueError, "orphan broaderConceptIds"):
            self.validate()

    def test_rejects_executable_fields_anywhere_in_transversal_p2a(self):
        relation = self.valid_relation()
        relation["evidenceReview"]["antiInferences"] = ["Do not infer diagnosis."]
        self.write_jsonl(self.relations, [relation])
        with self.assertRaisesRegex(ValueError, "executable field forbidden"):
            self.validate()

    def test_accepts_proposed_relation_before_reconsultation(self):
        self.write_jsonl(self.relations, [self.valid_relation()])
        self.assertEqual(self.validate(), (0, 1, 0))

    def test_rejects_reviewed_relation_without_bilateral_canonical_reconsultation(self):
        relation = self.valid_relation()
        relation["reviewStatus"] = "SOURCE_RECHECKED"
        self.write_jsonl(self.relations, [relation])
        with self.assertRaisesRegex(ValueError, "requires canonical reconsultation on both sides"):
            self.validate()

    def test_accepts_reviewed_relation_after_bilateral_canonical_reconsultation(self):
        relation = self.valid_relation()
        relation["reviewStatus"] = "ACCEPTED"
        relation["evidenceReview"]["fromCanonicalReconsulted"] = True
        relation["evidenceReview"]["toCanonicalReconsulted"] = True
        self.write_jsonl(self.relations, [relation])
        self.assertEqual(self.validate(), (0, 1, 0))

    def test_rejects_same_source_record_in_cross_source_relation_file(self):
        relation = self.valid_relation()
        relation["fromDoctrineId"] = "DR_SZ_LEHR_1972_000002"
        self.write_jsonl(self.relations, [relation])
        with self.assertRaisesRegex(ValueError, "must belong to different sourceIds"):
            self.validate()

    def test_rejects_orphan_relation_endpoint(self):
        relation = self.valid_relation()
        relation["toDoctrineId"] = "DR_SZ_SA_1948_999999"
        self.write_jsonl(self.relations, [relation])
        with self.assertRaisesRegex(ValueError, "orphan toDoctrineId"):
            self.validate()

    def test_rejects_relation_type_outside_primary_doctrine_vocabulary(self):
        relation = self.valid_relation()
        relation["relationType"] = "SUPERSEDES"
        self.write_jsonl(self.relations, [relation])
        with self.assertRaisesRegex(ValueError, "invalid relationType"):
            self.validate()

    def test_requires_pdf_reconsultation_when_visual_arbitration_is_declared(self):
        relation = self.valid_relation()
        relation["evidenceReview"]["visualArbitrationRequired"] = True
        self.write_jsonl(self.relations, [relation])
        with self.assertRaisesRegex(ValueError, "visual arbitration requires"):
            self.validate()

    def test_accepts_explicit_open_question_instead_of_forced_relation(self):
        self.write_jsonl(self.questions, [self.valid_question()])
        self.assertEqual(self.validate(), (0, 0, 1))

    def test_rejects_orphan_doctrine_in_open_question(self):
        question = self.valid_question()
        question["implicatedDoctrineIds"] = ["DR_SZ_SA_1948_999999"]
        self.write_jsonl(self.questions, [question])
        with self.assertRaisesRegex(ValueError, "orphan implicated doctrineId"):
            self.validate()

    def test_repository_transversal_snapshot_validates(self):
        registry_paths = sorted((ROOT / "doctrine" / "registry").glob("*.jsonl"))
        counts = validate_transversal_layer(
            registry_paths=registry_paths,
            concepts_path=ROOT / "doctrine" / "index" / "concepts.jsonl",
            relations_path=ROOT / "doctrine" / "relations" / "cross_source.jsonl",
            open_questions_path=ROOT / "doctrine" / "unresolved" / "open_questions.jsonl",
        )
        self.assertEqual(counts, (10, 6, 4))


if __name__ == "__main__":
    unittest.main()
