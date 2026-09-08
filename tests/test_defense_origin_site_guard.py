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


def _profile():
    return build_profile(_reaction(factor) for factor in FACTORS)


class DefenseOriginSiteGuardTests(unittest.TestCase):
    def test_guard_is_emitted_at_series_level(self):
        result = evaluate_clinical_protocol(ProfileSeries((_profile(),)), production=True)

        finding = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000057"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000015",))
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_B",))
        self.assertIn("Abwehr", finding.statement)
        self.assertIn("toate cele patru Triebgebiete", finding.statement)
        self.assertIn("Sch nu poate fi tratat drept singurul sediu", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000057",))
        self.assertIn("localizarea exclusivă", finding.anti_inferences[0])
        self.assertIn("source-grounded specifică", finding.anti_inferences[0])

        profile_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000057", profile_ids)

    def test_guard_is_not_profile_shape_specific(self):
        profile = build_profile(
            _reaction(
                factor,
                "positive" if factor in {"h", "k"}
                else "negative" if factor in {"hy", "m"}
                else "null",
            )
            for factor in FACTORS
        )
        result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
        series_ids = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        self.assertIn("IC_SZONDI_PRIMARY_000057", series_ids)


if __name__ == "__main__":
    unittest.main()
