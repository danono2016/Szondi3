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


class TriebklasseHealthStatusLimitTests(unittest.TestCase):
    def test_doctrine_preserves_explicit_health_status_limit_and_counterexamples(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "doctrine"
            / "registry"
            / "SZ_TRIEBPATH_2_000003.jsonl"
        )
        doctrine = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(doctrine["doctrineId"], "DR_SZ_TRIEBPATH_2_000003")
        anchor = doctrine["sourceAnchors"][0]
        self.assertEqual(anchor["unitStart"], "U000251")
        self.assertEqual(anchor["unitEnd"], "U000253")
        self.assertEqual(anchor["printedPage"], 254)
        self.assertIn("seelisch krank oder noch gesund", doctrine["sourceExcerpt"])
        self.assertIn("copiilor", doctrine["doctrinalStatement"])
        self.assertIn("socializate", doctrine["doctrinalStatement"])
        self.assertIn("does not implement a syndrome detector", doctrine["scopeNotes"][2])
        self.assertIn("clinical diagnosis algorithm", doctrine["scopeNotes"][2])

    def test_claim_is_source_established_and_does_not_erase_testological_value(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000053"]

        self.assertIs(claim.epistemic_class, EpistemicClass.SOURCE_ESTABLISHED_TRIGGER)
        self.assertEqual(claim.doctrine_ids, ("DR_SZ_TRIEBPATH_2_000003",))
        self.assertEqual(claim.source_ids, ("SZ_TRIEBPATH_2",))
        self.assertIn("nu decid singure", claim.claim)
        self.assertIn("bolnavă psihic sau sănătoasă", claim.claim)
        prohibited = claim.anti_inferences[0].prohibited_conclusion
        self.assertIn("psihotică", prohibited)
        self.assertIn("criză de dezvoltare", prohibited)
        self.assertIn("nu anulează valoarea testologică", prohibited)

    def test_available_latency_proportions_emit_clinical_status_guard(self):
        result = evaluate_clinical_protocol(_latency_series(3), production=True)

        latency = result.series_result.calculation("latency_class_structure")
        self.assertIs(latency.state, CalculationState.AVAILABLE)
        finding = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000053"
        )
        self.assertEqual(
            finding.support_fact_ids,
            ("profile_series:latency_proportions",),
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_TRIEBPATH_2_000003",))
        self.assertIn("Triebklassen", finding.statement)
        self.assertIn("nu decid singure", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000053",))

    def test_under_three_profiles_does_not_route_latency_status_guard(self):
        result = evaluate_clinical_protocol(_latency_series(2), production=True)

        finding_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.series_result.interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000053", finding_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000053", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
