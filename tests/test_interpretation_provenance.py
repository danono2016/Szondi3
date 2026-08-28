import json
import unittest
from pathlib import Path

from szondi3.interpretation_catalogue import INITIAL_CLAIMS


class InterpretationProvenanceTests(unittest.TestCase):
    def test_every_initial_claim_resolves_to_current_source_verified_doctrine(self):
        registry = Path(__file__).resolve().parents[1] / "doctrine" / "registry"
        doctrine = {}
        for path in registry.glob("*.jsonl"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                item = json.loads(line)
                doctrine_id = item.get("doctrineId")
                if doctrine_id:
                    doctrine[doctrine_id] = item

        for claim in INITIAL_CLAIMS:
            for doctrine_id in claim.doctrine_ids:
                with self.subTest(claim=claim.claim_id, doctrine=doctrine_id):
                    self.assertIn(doctrine_id, doctrine)
                    item = doctrine[doctrine_id]
                    self.assertEqual(item["sourceLayer"], claim.source_layer)
                    self.assertIn(item["sourceId"], claim.source_ids)
                    self.assertEqual(item["reviewStatus"], "SOURCE_VERIFIED")
                    self.assertTrue(item.get("sourceAnchors"))


if __name__ == "__main__":
    unittest.main()
