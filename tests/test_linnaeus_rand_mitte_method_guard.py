import json
import unittest
from pathlib import Path

from szondi3.clinical_protocol import CalculationState, evaluate_clinical_protocol
from szondi3.interpretation import EpistemicClass
from szondi3.interpretation_catalogue import CLAIMS_BY_ID
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor: str, kind: str) -> FactorReaction:
    symbol = {
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
        symbol=symbol,
        quantum_level=0,
    )


def _latency_series(count: int) -> ProfileSeries:
    profiles = []
    for _ in range(count):
        profiles.append(
            build_profile(
                _reaction(factor, "null" if factor == "h" else "positive")
                for factor in FACTORS
            )
        )
    return ProfileSeries(tuple(profiles))


class LinnaeusRandMitteMethodGuardTests(unittest.TestCase):
    def test_doctrine_preserves_complementarity_and_rapid_orientation_limit(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "doctrine"
            / "registry"
            / "SZ_LEHR_1972_000362.jsonl"
        )
        doctrine = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(doctrine["doctrineId"], "DR_SZ_LEHR_1972_000362")
        anchor = doctrine["sourceAnchors"][0]
        self.assertEqual(anchor["unitStart"], "U004560")
        self.assertEqual(anchor["unitEnd"], "U004561")
        self.assertIn("niemals überflüssig", doctrine["sourceExcerpt"])
        self.assertIn("rasche Orientierung", doctrine["sourceExcerpt"])
        self.assertIn("nu înlocuiește", doctrine["doctrinalStatement"])
        self.assertIn("nu invalidează", doctrine["doctrinalStatement"])
        self.assertIn("not a sequential validity gate", doctrine["scopeNotes"][0])
        self.assertEqual(doctrine["reviewStatus"], "SOURCE_VERIFIED")

    def test_claim_is_source_established_and_guards_only_qualitative_overreach(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000054"]

        self.assertIs(claim.epistemic_class, EpistemicClass.SOURCE_ESTABLISHED_TRIGGER)
        self.assertEqual(
            claim.doctrine_ids,
            (
                "DR_SZ_LEHR_1972_000362",
                "DR_SZ_LEHR_1972_000302",
                "DR_SZ_LEHR_1972_000359",
            ),
        )
        self.assertEqual(claim.source_ids, ("SZ_LEHR_1972",))
        self.assertIn("orientare cantitativă", claim.claim)
        self.assertIn("Abwehrart", claim.claim)
        self.assertIn("nu invalidează", claim.claim)
        prohibited = claim.anti_inferences[0].prohibited_conclusion
        self.assertIn("Schicksalsdiagnose", prohibited)
        self.assertIn("caracterul cronic", prohibited)
        self.assertIn("Nu declara însă Linnäus nevalid", prohibited)

    def test_available_latency_proportions_emit_method_guard_with_same_evidence_scope(self):
        result = evaluate_clinical_protocol(_latency_series(3), production=True)

        latency = result.series_result.calculation("latency_class_structure")
        self.assertIs(latency.state, CalculationState.AVAILABLE)
        findings = {
            item.claim_id: item for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000053", findings)
        self.assertIn("IC_SZONDI_PRIMARY_000054", findings)
        finding = findings["IC_SZONDI_PRIMARY_000054"]
        self.assertEqual(
            finding.support_fact_ids,
            ("profile_series:latency_proportions",),
        )
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000054",))
        self.assertIn("Rand–Mitte", finding.statement)
        self.assertIn("nu invalidează", finding.statement)

    def test_under_three_profiles_does_not_route_method_guard(self):
        result = evaluate_clinical_protocol(_latency_series(2), production=True)

        finding_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.series_result.interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000054", finding_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000054", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
