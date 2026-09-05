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


class GeneticInferenceLimitTests(unittest.TestCase):
    def test_genetic_limit_is_emitted_once_at_protocol_level(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"k": "positive"}),)),
            production=True,
        )

        series_findings = {
            item.claim_id: item for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000045", series_findings)
        finding = series_findings["IC_SZONDI_PRIMARY_000045"]
        self.assertEqual(
            finding.doctrine_ids,
            (
                "DR_SZ_SA_1948_000127",
                "DR_SZ_SA_1948_000172",
                "DR_SZ_SA_1948_000243",
            ),
        )
        self.assertEqual(finding.source_ids, ("SZ_SA_1948",))
        self.assertIn("nu constituie o identificare genetică", finding.statement)
        self.assertIn("Familienforschung", finding.statement)
        self.assertIn("terra incognita", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000045",))
        self.assertIn("statut de purtător", finding.anti_inferences[0])
        self.assertIn("alegerea partenerului", finding.anti_inferences[0])
        self.assertIn("riscul de suicid", finding.anti_inferences[0])

        profile_claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000045", profile_claim_ids)

    def test_genetic_limit_does_not_depend_on_one_profile_shape(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"p": "negative", "m": "negative"}),)),
            production=True,
        )
        claim_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000045", claim_ids)


if __name__ == "__main__":
    unittest.main()
