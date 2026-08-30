import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.freeze_doctrine_snapshot import build_snapshot


COMMIT = "0123456789abcdef0123456789abcdef01234567"


def entry(source_id, number, statement):
    return {
        "schemaVersion": 1,
        "doctrineId": f"DR_{source_id}_{number:06d}",
        "sourceId": source_id,
        "doctrinalStatement": statement,
    }


class DoctrineSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_jsonl(self, name, entries):
        path = self.root / name
        path.write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in entries),
            encoding="utf-8",
        )
        return path

    def test_snapshot_is_deterministic_across_registry_path_order(self):
        lehr = self.write_jsonl(
            "lehr.jsonl",
            [
                entry("SZ_LEHR_1972", 2, "second"),
                entry("SZ_LEHR_1972", 1, "first"),
            ],
        )
        ia = self.write_jsonl(
            "ia.jsonl",
            [entry("SZ_IA_1956_A", 1, "ego")],
        )

        first = build_snapshot(
            registry_paths=[lehr, ia],
            source_ids=["SZ_IA_1956_A", "SZ_LEHR_1972"],
            commit_sha=COMMIT,
        )
        second = build_snapshot(
            registry_paths=[ia, lehr],
            source_ids=["SZ_LEHR_1972", "SZ_IA_1956_A"],
            commit_sha=COMMIT,
        )
        self.assertEqual(first, second)
        self.assertEqual(first["doctrineIds"], sorted(first["doctrineIds"]))
        self.assertEqual(first["doctrineCount"], 3)
        self.assertEqual(first["sourceCounts"]["SZ_LEHR_1972"], 2)
        self.assertEqual(first["sourceCounts"]["SZ_IA_1956_A"], 1)

    def test_snapshot_excludes_unselected_sources(self):
        path = self.write_jsonl(
            "mixed.jsonl",
            [
                entry("SZ_LEHR_1972", 1, "lehr"),
                entry("SZ_IA_1956_A", 1, "ia"),
                entry("DERI_1949", 1, "secondary"),
            ],
        )
        manifest = build_snapshot(
            registry_paths=[path],
            source_ids=["SZ_LEHR_1972", "SZ_IA_1956_A"],
            commit_sha=COMMIT,
        )
        self.assertNotIn("DR_DERI_1949_000001", manifest["doctrineIds"])
        self.assertEqual(manifest["selectedSourceIds"], ["SZ_IA_1956_A", "SZ_LEHR_1972"])

    def test_registry_digest_changes_when_selected_doctrine_content_changes(self):
        original = entry("SZ_LEHR_1972", 1, "original")
        changed = deepcopy(original)
        changed["doctrinalStatement"] = "changed"
        first_path = self.write_jsonl("first.jsonl", [original])
        first = build_snapshot(
            registry_paths=[first_path],
            source_ids=["SZ_LEHR_1972"],
            commit_sha=COMMIT,
        )
        second_path = self.write_jsonl("second.jsonl", [changed])
        second = build_snapshot(
            registry_paths=[second_path],
            source_ids=["SZ_LEHR_1972"],
            commit_sha=COMMIT,
        )
        self.assertNotEqual(first["registryDigest"], second["registryDigest"])
        self.assertNotEqual(first["snapshotId"], second["snapshotId"])

    def test_snapshot_id_changes_with_commit_even_when_registry_is_identical(self):
        path = self.write_jsonl("registry.jsonl", [entry("SZ_LEHR_1972", 1, "same")])
        first = build_snapshot(
            registry_paths=[path],
            source_ids=["SZ_LEHR_1972"],
            commit_sha=COMMIT,
        )
        second = build_snapshot(
            registry_paths=[path],
            source_ids=["SZ_LEHR_1972"],
            commit_sha="fedcba9876543210fedcba9876543210fedcba98",
        )
        self.assertEqual(first["registryDigest"], second["registryDigest"])
        self.assertNotEqual(first["snapshotId"], second["snapshotId"])

    def test_rejects_missing_selected_source(self):
        path = self.write_jsonl("registry.jsonl", [entry("SZ_LEHR_1972", 1, "lehr")])
        with self.assertRaisesRegex(ValueError, "have no doctrine entries"):
            build_snapshot(
                registry_paths=[path],
                source_ids=["SZ_LEHR_1972", "SZ_IA_1956_A"],
                commit_sha=COMMIT,
            )

    def test_rejects_duplicate_doctrine_id(self):
        item = entry("SZ_LEHR_1972", 1, "same id")
        path = self.write_jsonl("registry.jsonl", [item, item])
        with self.assertRaisesRegex(ValueError, "duplicate doctrineId"):
            build_snapshot(
                registry_paths=[path],
                source_ids=["SZ_LEHR_1972"],
                commit_sha=COMMIT,
            )

    def test_rejects_invalid_full_commit_sha(self):
        path = self.write_jsonl("registry.jsonl", [entry("SZ_LEHR_1972", 1, "lehr")])
        with self.assertRaisesRegex(ValueError, "full lowercase 40-hex"):
            build_snapshot(
                registry_paths=[path],
                source_ids=["SZ_LEHR_1972"],
                commit_sha="abc123",
            )

    def test_repository_lehrbuch_snapshot_can_be_built_without_writing_artifact(self):
        root = Path(__file__).resolve().parents[1]
        registry_paths = sorted((root / "doctrine" / "registry").glob("*.jsonl"))
        manifest = build_snapshot(
            registry_paths=registry_paths,
            source_ids=["SZ_LEHR_1972"],
            commit_sha=COMMIT,
        )
        self.assertEqual(manifest["sourceCounts"], {"SZ_LEHR_1972": 174})
        self.assertEqual(manifest["doctrineCount"], 174)
        self.assertTrue(manifest["snapshotId"].startswith("DS_"))


if __name__ == "__main__":
    unittest.main()
