import unittest

from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_facts import profile_facts
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import ActivationStatus, evaluate_claim
from szondi3.interpretation_catalogue import CLAIMS_BY_ID
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}


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


def _profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        _reaction(factor, overrides.get(factor, "0"))
        for factor in FACTORS
    )


def _fall40_series() -> ProfileSeries:
    factors = ("h", "s", "e", "hy", "k", "p", "d", "m")
    rows = (
        ("+!", "0", "0", "-", "-", "±", "+", "-"),
        ("+!", "0", "-", "-", "-", "+", "+", "-"),
        ("+", "0", "-", "-", "+", "+", "+", "-!"),
        ("+!", "0", "-", "-", "+", "±", "+", "-"),
        ("+", "0", "0", "-", "+", "±", "+", "-!!"),
        ("+!", "0", "-", "-!", "+", "±", "+", "-!"),
        ("+!", "-", "-", "0", "+", "+", "+", "-!"),
        ("+!", "0", "-", "-", "+", "±", "+", "-!"),
        ("+", "0", "-", "-", "+", "±", "+", "-!"),
        ("+", "0", "-", "0", "±", "±", "+", "-!"),
    )
    return ProfileSeries(
        tuple(
            build_profile(
                _reaction(factor, symbol)
                for factor, symbol in zip(factors, row)
            )
            for row in rows
        )
    )


class SchPlusAmbivalentClaimTests(unittest.TestCase):
    def test_exact_sch_plus_ambivalent_activates_and_nearby_configurations_do_not(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000013"]

        exact = evaluate_claim(
            claim,
            profile_facts(_profile({"k": "+", "p": "±"})),
        )
        self.assertEqual(exact.activation_status, ActivationStatus.ACTIVE)
        self.assertEqual(
            exact.matched_facts[0].key,
            "profile.vector.Sch.base_symbols",
        )
        self.assertEqual(
            exact.matched_facts[0].value,
            ("+", "±"),
        )
        self.assertEqual(
            exact.anti_inferences[0].anti_inference_id,
            "AI_SZONDI_000013",
        )

        for k, p in (("+", "+"), ("-", "±"), ("±", "±"), ("+", "0")):
            with self.subTest(k=k, p=p):
                result = evaluate_claim(
                    claim,
                    profile_facts(_profile({"k": k, "p": p})),
                )
                self.assertEqual(
                    result.activation_status,
                    ActivationStatus.INACTIVE,
                )

    def test_fall40_activates_exact_sch_plus_ambivalent_claim_in_five_profiles(self):
        packet = build_clinical_evidence_packet(
            evaluate_clinical_protocol(_fall40_series(), production=True)
        )

        findings = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000013"
        )

        self.assertEqual(len(findings), 5)
        self.assertEqual(
            {item.profile_number for item in findings},
            {4, 5, 6, 8, 9},
        )
        for item in findings:
            self.assertEqual(
                item.doctrine_ids,
                ("DR_SZ_LEHR_1972_000352",),
            )
            self.assertEqual(
                item.anti_inference_ids,
                ("AI_SZONDI_000013",),
            )
            self.assertEqual(
                item.support_fact_ids,
                (
                    f"foreground_profile_{item.profile_number}:"
                    "vector:Sch:base_symbols",
                ),
            )

        doctrine = packet.doctrine("DR_SZ_LEHR_1972_000352")
        self.assertEqual(doctrine.review_status, "SOURCE_VERIFIED")
        self.assertEqual(doctrine.source_id, "SZ_LEHR_1972")
        self.assertIn("durchschnittlich", doctrine.source_excerpt)
        self.assertEqual(doctrine.source_anchors[0].unit_start, "U002084")
        self.assertEqual(doctrine.source_anchors[0].printed_page, 135)
        self.assertEqual(doctrine.source_anchors[1].unit_start, "U002950")
        self.assertEqual(doctrine.source_anchors[1].printed_page, 201)

    def test_claim_preserves_two_branches_and_blocks_stronger_automatic_inference(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000013"]

        self.assertIn("Annahme der Weiblichkeit", claim.claim)
        self.assertIn("Annahme der Verlassenheit", claim.claim)
        self.assertIn("nu decide", claim.claim)
        blocked = claim.anti_inferences[0].prohibited_conclusion
        self.assertIn("Kastrationskomplex", blocked)
        self.assertIn("Paranoiden", blocked)
        self.assertIn("abandon", blocked)


if __name__ == "__main__":
    unittest.main()
