import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.clinical_report import build_clinical_report
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def reaction(factor, kind="null", quantum=0):
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


def profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


class ClinicalProductionSmokeTests(unittest.TestCase):
    def test_mixed_eight_profile_protocol_emits_first_approved_szondian_nucleus(self):
        series = ProfileSeries(
            (
                profile({"p": ("negative", 0)}),
                profile({"p": ("positive", 0)}),
                profile({"k": ("positive", 0)}),
                profile({"k": ("negative", 0)}),
                profile({"k": ("ambivalent", 0), "p": ("ambivalent", 0)}),
                profile(),
                profile({"p": ("negative", 0), "k": ("positive", 0)}),
                profile({"p": ("positive", 0), "k": ("negative", 0)}),
            )
        )

        evaluation = evaluate_clinical_protocol(series, production=True)
        report = build_clinical_report(evaluation)

        self.assertTrue(report.header.production_mode)
        self.assertEqual(
            report.header.interpretation_release_state,
            "PRODUCTION_APPROVED_CLAIMS_ONLY",
        )
        self.assertEqual(report.header.profile_count, 8)
        self.assertEqual(len(report.observations), 8)

        profile_claim_ids = {
            item.claim_id for item in report.findings if item.scope == "PROFILE"
        }
        self.assertTrue(
            {
                "IC_SZONDI_PRIMARY_000007",
                "IC_SZONDI_PRIMARY_000008",
                "IC_SZONDI_PRIMARY_000009",
                "IC_SZONDI_PRIMARY_000010",
                "IC_SZONDI_PRIMARY_000011",
                "IC_SZONDI_PRIMARY_000012",
            }.issubset(profile_claim_ids)
        )

        series_claim_ids = {
            item.claim_id for item in report.findings if item.scope == "SERIES"
        }
        self.assertTrue(
            {
                "IC_SZONDI_PRIMARY_000003",
                "IC_SZONDI_PRIMARY_000004",
                "IC_SZONDI_PRIMARY_000005",
            }.issubset(series_claim_ids)
        )

        self.assertTrue(report.findings)
        self.assertTrue(all(item.lifecycle_status == "APPROVED" for item in report.findings))

        guarded_claims = {
            item.claim_id: item
            for item in report.findings
            if item.claim_id
            in {
                "IC_SZONDI_PRIMARY_000010",
                "IC_SZONDI_PRIMARY_000011",
                "IC_SZONDI_PRIMARY_000012",
            }
        }
        self.assertTrue(all(item.anti_inferences for item in guarded_claims.values()))
        self.assertIsNone(report.therapist_synthesis.text)
        self.assertEqual(
            report.therapist_synthesis.authorship,
            "MANUAL_CLINICIAN_INPUT_ONLY",
        )


if __name__ == "__main__":
    unittest.main()
