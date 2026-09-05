import re
import unittest
from pathlib import Path

from szondi3.interpretation_catalogue_fate_modifiability import INITIAL_CLAIMS


class IAAExecutabilityClosureTests(unittest.TestCase):
    def test_closure_accounts_for_every_current_ia_a_doctrine_once(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "SZ_IA_1956_A_EXECUTABILITY_CLOSURE.md"
        )
        text = path.read_text(encoding="utf-8")
        rows = tuple(
            int(match.group(1))
            for match in re.finditer(r"^\| `([0-9]{6})` \|", text, flags=re.MULTILINE)
        )
        self.assertEqual(rows, tuple(range(1, 52)))

    def test_direct_ia_a_closure_mappings_equal_live_catalogue(self):
        expected = {
            "DR_SZ_IA_1956_A_000038": ("IC_SZONDI_PRIMARY_000087",),
            "DR_SZ_IA_1956_A_000040": (
                "IC_SZONDI_PRIMARY_000050",
                "IC_SZONDI_PRIMARY_000051",
            ),
            "DR_SZ_IA_1956_A_000043": (
                "IC_SZONDI_PRIMARY_000007",
                "IC_SZONDI_PRIMARY_000008",
                "IC_SZONDI_PRIMARY_000009",
                "IC_SZONDI_PRIMARY_000010",
                "IC_SZONDI_PRIMARY_000051",
            ),
            "DR_SZ_IA_1956_A_000045": ("IC_SZONDI_PRIMARY_000051",),
            "DR_SZ_IA_1956_A_000046": ("IC_SZONDI_PRIMARY_000038",),
            "DR_SZ_IA_1956_A_000047": ("IC_SZONDI_PRIMARY_000037",),
            "DR_SZ_IA_1956_A_000048": ("IC_SZONDI_PRIMARY_000050",),
            "DR_SZ_IA_1956_A_000049": ("IC_SZONDI_PRIMARY_000010",),
            "DR_SZ_IA_1956_A_000051": (
                "IC_SZONDI_PRIMARY_000011",
                "IC_SZONDI_PRIMARY_000012",
            ),
        }
        actual = {}
        for doctrine_id in expected:
            actual[doctrine_id] = tuple(
                claim.claim_id
                for claim in INITIAL_CLAIMS
                if doctrine_id in claim.doctrine_ids
            )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
