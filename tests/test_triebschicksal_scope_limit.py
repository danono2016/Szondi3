import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
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
        _reaction(factor, overrides.get(factor, "null")) for factor in FACTORS
    )


class TriebschicksalScopeLimitTests(unittest.TestCase):
    def test_scope_limit_is_emitted_once_at_protocol_level(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"p": "positive"}),)),
            production=True,
        )

        series_findings = {
            item.claim_id: item for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000044", series_findings)
        finding = series_findings["IC_SZONDI_PRIMARY_000044"]
        self.assertEqual(
            finding.doctrine_ids,
            (
                "DR_SZ_SA_1948_000058",
                "DR_SZ_SA_1948_000059",
                "DR_SZ_SA_1948_000060",
                "DR_SZ_SA_1948_000061",
                "DR_SZ_SA_1948_000062",
            ),
        )
        self.assertEqual(finding.source_ids, ("SZ_SA_1948",))
        self.assertIn("Triebschicksal", finding.statement)
        self.assertIn("Gesamtschicksal", finding.statement)
        self.assertIn("Leben ist stets mehr als Triebschicksal", finding.statement)
        self.assertIn("Lebensplan", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000044",))
        self.assertIn("situația socială concretă", finding.anti_inferences[0])
        self.assertIn("biografia", finding.anti_inferences[0])
        self.assertIn("boala ori moartea", finding.anti_inferences[0])

        profile_claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000044", profile_claim_ids)

    def test_scope_limit_remains_present_for_a_full_ten_profile_series(self):
        profiles = tuple(_profile({"k": "positive"}) for _ in range(10))
        result = evaluate_clinical_protocol(ProfileSeries(profiles), production=True)
        claim_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000044", claim_ids)


if __name__ == "__main__":
    unittest.main()
