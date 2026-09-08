import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, kind="null", quantum=0):
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
        symbol=base + ("!" * quantum),
        quantum_level=quantum,
    )


def _profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        _reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


def _ids(result):
    interpretation = result.profiles[0].interpretation
    return (
        {item.claim_id for item in interpretation.findings},
        {item.claim_id for item in interpretation.unresolved},
    )


class ProfileRelationRegressionTests(unittest.TestCase):
    def test_c_plus_minus_uses_existing_000020_without_duplicate_000035(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"d": ("positive", 0), "m": ("negative", 0)}),)),
            production=True,
        )
        finding_ids, unresolved_ids = _ids(result)

        self.assertIn("IC_SZONDI_PRIMARY_000020", finding_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000035", finding_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000035", unresolved_ids)

    def test_p_zero_minus_uses_existing_000023_without_duplicate_000036(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile({"hy": ("negative", 0)}),)),
            production=True,
        )
        finding_ids, unresolved_ids = _ids(result)

        self.assertIn("IC_SZONDI_PRIMARY_000023", finding_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000036", finding_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000036", unresolved_ids)

    def test_sch_plus_minus_emits_introprojection_without_autism_promotion(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"k": ("positive", 0), "p": ("negative", 0)}),)
            ),
            production=True,
        )

        finding = next(
            item
            for item in result.profiles[0].interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000037"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_A_000047",))
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_A",))
        self.assertIn("Introprojektion", finding.statement)
        self.assertIn("proiecția", finding.statement)
        self.assertIn("introiecția", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000037",))
        self.assertIn("diagnostic de autism", finding.anti_inferences[0])
        self.assertIn("Weltbild", finding.anti_inferences[0])

    def test_sch_plus_minus_with_overpressure_is_not_promoted_to_000037(self):
        result = evaluate_clinical_protocol(
            ProfileSeries(
                (_profile({"k": ("positive", 1), "p": ("negative", 0)}),)
            )
        )
        finding_ids, unresolved_ids = _ids(result)

        self.assertNotIn("IC_SZONDI_PRIMARY_000037", finding_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000037", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
