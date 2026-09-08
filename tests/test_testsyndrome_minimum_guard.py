import json
import unittest
from pathlib import Path

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import EpistemicClass
from szondi3.interpretation_catalogue import CLAIMS_BY_ID
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, kind="null"):
    base = {
        "null": "0",
        "positive": "+",
        "negative": "-",
        "ambivalent": "±",
    }[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=base,
        quantum_level=0,
    )


def _profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        _reaction(factor, overrides.get(factor, "null"))
        for factor in FACTORS
    )


class TestsyndromMinimumGuardTests(unittest.TestCase):
    def test_doctrine_preserves_exact_minimum_and_not_sufficient_boundary(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "doctrine"
            / "registry"
            / "SZ_TRIEBPATH_2_000002.jsonl"
        )
        doctrine = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(doctrine["doctrineId"], "DR_SZ_TRIEBPATH_2_000002")
        self.assertEqual(doctrine["sourceAnchors"][0]["unitStart"], "U000257")
        self.assertEqual(doctrine["sourceAnchors"][0]["unitEnd"], "U000257")
        self.assertEqual(doctrine["sourceAnchors"][0]["printedPage"], 255)
        self.assertIn("minimal drei Faktorenreaktionen", doctrine["sourceExcerpt"])
        self.assertIn("Zwei bestimmte Reaktionen bilden noch keinen Faktorenverband", doctrine["sourceExcerpt"])
        self.assertIn("necessary condition", doctrine["scopeNotes"][0])
        self.assertIn("not encoded as an automatic threshold", doctrine["scopeNotes"][1])

    def test_guard_is_source_established_and_combines_primary_method_limits(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000052"]

        self.assertIs(claim.epistemic_class, EpistemicClass.SOURCE_ESTABLISHED_TRIGGER)
        self.assertEqual(
            claim.doctrine_ids,
            ("DR_SZ_TRIEBPATH_2_000002", "DR_SZ_LEHR_1972_000350"),
        )
        self.assertEqual(claim.source_ids, ("SZ_TRIEBPATH_2", "SZ_LEHR_1972"))
        self.assertIn("cel puțin trei reacții factoriale", claim.claim)
        self.assertIn("nu echivalează automat cu un diagnostic clinic", claim.claim)
        self.assertIn("minimum trei este necesar, nu suficient", claim.anti_inferences[0].prohibited_conclusion)
        self.assertIn("4-6 reacții", claim.anti_inferences[0].prohibited_conclusion)

    def test_two_factor_relation_keeps_local_meaning_but_is_not_promoted_to_syndrome(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"m": "negative", "k": "positive"}),)
            ),
            production=True,
        )

        profile_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        series_findings = {
            item.claim_id: item for item in result.series_result.interpretation.findings
        }

        self.assertIn("IC_SZONDI_PRIMARY_000038", profile_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000052", series_findings)
        guard = series_findings["IC_SZONDI_PRIMARY_000052"]
        self.assertEqual(guard.support_fact_ids, ("profile_series:profile_count",))
        self.assertIn("pereche inter-factorială", guard.statement)
        self.assertIn("-m/+k", guard.anti_inferences[0])
        self.assertIn("Nu transforma un Testsyndrom", guard.anti_inferences[0])

    def test_guard_is_protocol_level_not_a_profile_label(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile(),)),
            production=True,
        )

        self.assertIn(
            "IC_SZONDI_PRIMARY_000052",
            {item.claim_id for item in result.series_result.interpretation.findings},
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000052",
            {item.claim_id for item in result.profiles[0].interpretation.findings},
        )


if __name__ == "__main__":
    unittest.main()
