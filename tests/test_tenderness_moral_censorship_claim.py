import json
import unittest
from pathlib import Path

from szondi3.clinical_protocol import PROFILE_CLAIM_IDS, evaluate_clinical_protocol
from szondi3.interpretation_catalogue import CLAIMS_BY_ID
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}
_ROOT = Path(__file__).resolve().parents[1]


def _reaction(factor: str, symbol: str) -> FactorReaction:
    base = "±" if symbol.startswith("±") else symbol[0]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=_KIND[base],
        symbol=symbol,
        quantum_level=symbol.count("!"),
    )


def _profile(*symbols: str):
    return build_profile(
        _reaction(factor, symbol)
        for factor, symbol in zip(_FACTORS, symbols)
    )


def _doctrine(filename: str) -> dict:
    path = _ROOT / "doctrine" / "registry" / filename
    return json.loads(path.read_text(encoding="utf-8"))


class TendernessMoralCensorshipResearchCandidateTests(unittest.TestCase):
    def test_000022_is_suspended_from_production_catalogue_and_profile_routing(self):
        self.assertNotIn("IC_SZONDI_PRIMARY_000022", CLAIMS_BY_ID)
        self.assertNotIn("IC_SZONDI_PRIMARY_000022", PROFILE_CLAIM_IDS)

    def test_exact_h_plus_quantum_hy_minus_does_not_emit_production_finding(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries((_profile("+!", "0", "0", "-", "0", "0", "0", "0"),)),
            production=True,
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000022"
                for item in evaluation.profiles[0].interpretation.findings
            )
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000022"
                for item in evaluation.series_result.interpretation.findings
            )
        )

    def test_triebpathologie_example_remains_source_verified_open_candidate(self):
        example = _doctrine("SZ_TRIEBPATH_1_000001.jsonl")
        self.assertEqual(example["reviewStatus"], "SOURCE_VERIFIED")
        self.assertEqual(example["executionStatus"], "NOT_ASSESSED")
        self.assertIn("Zwei Beispiele", example["sourceExcerpt"])
        self.assertIn("exemplu primar P2A valid", example["doctrinalStatement"])
        self.assertTrue(
            any("remains open" in note for note in example["reviewNotes"])
        )
        self.assertTrue(
            any("must not be used" in note for note in example["reviewNotes"])
        )

    def test_lehrbuch_record_no_longer_supplies_missing_composite_generalization(self):
        general = _doctrine("SZ_LEHR_1972_000360.jsonl")
        self.assertEqual(general["reviewStatus"], "SOURCE_VERIFIED")
        self.assertEqual(general["executionStatus"], "NOT_ASSESSED")
        self.assertIn("nu sunt combinate aici", general["doctrinalStatement"])
        self.assertTrue(
            any(
                "Do not use this doctrine to infer or complete" in condition
                for condition in general["conditions"]
            )
        )
        self.assertTrue(
            any(
                "exceeded what this source explicitly states" in note
                for note in general["reviewNotes"]
            )
        )


if __name__ == "__main__":
    unittest.main()
