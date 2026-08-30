import unittest

from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_facts import profile_facts
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.clinical_synthesis import (
    SynthesisProposition,
    validate_synthesis_propositions,
)
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


def _fall40_packet():
    return build_clinical_evidence_packet(
        evaluate_clinical_protocol(_fall40_series(), production=True)
    )


def _profile_proposition(
    *,
    proposition_id: str,
    profile_number: int,
    claim_id: str,
    doctrine_id: str,
    anti_inference_id: str,
    text: str,
    anti_inference_ids=None,
):
    if anti_inference_ids is None:
        anti_inference_ids = (anti_inference_id,)
    return SynthesisProposition(
        proposition_id=proposition_id,
        scope="PROFILE",
        profile_number=profile_number,
        text=text,
        support_claim_ids=(claim_id,),
        support_fact_ids=(
            f"foreground_profile_{profile_number}:vector:S:base_symbols",
        ),
        support_doctrine_ids=(doctrine_id,),
        anti_inference_ids_applied=anti_inference_ids,
    )


class SexualVectorConfigurationClaimTests(unittest.TestCase):
    def test_exact_s_plus_zero_and_s_plus_minus_are_configuration_specific(self):
        plus_zero = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000017"]
        plus_minus = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000018"]

        exact_plus_zero = evaluate_claim(
            plus_zero,
            profile_facts(_profile({"h": "+", "s": "0"})),
        )
        self.assertEqual(exact_plus_zero.activation_status, ActivationStatus.ACTIVE)
        self.assertEqual(
            exact_plus_zero.matched_facts[0].value,
            ("+", "0"),
        )
        self.assertEqual(
            exact_plus_zero.anti_inferences[0].anti_inference_id,
            "AI_SZONDI_000017",
        )

        exact_plus_minus = evaluate_claim(
            plus_minus,
            profile_facts(_profile({"h": "+", "s": "-"})),
        )
        self.assertEqual(exact_plus_minus.activation_status, ActivationStatus.ACTIVE)
        self.assertEqual(
            exact_plus_minus.matched_facts[0].value,
            ("+", "-"),
        )
        self.assertEqual(
            exact_plus_minus.anti_inferences[0].anti_inference_id,
            "AI_SZONDI_000018",
        )

        for h, s in (("+", "+"), ("-", "0"), ("±", "-"), ("0", "0")):
            with self.subTest(h=h, s=s):
                facts = profile_facts(_profile({"h": h, "s": s}))
                self.assertEqual(
                    evaluate_claim(plus_zero, facts).activation_status,
                    ActivationStatus.INACTIVE,
                )
                self.assertEqual(
                    evaluate_claim(plus_minus, facts).activation_status,
                    ActivationStatus.INACTIVE,
                )

    def test_fall40_routes_s_plus_zero_to_nine_profiles_and_s_plus_minus_to_profile_seven(self):
        packet = _fall40_packet()

        plus_zero = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000017"
        )
        plus_minus = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000018"
        )

        self.assertEqual(len(plus_zero), 9)
        self.assertEqual(
            {item.profile_number for item in plus_zero},
            {1, 2, 3, 4, 5, 6, 8, 9, 10},
        )
        self.assertEqual(len(plus_minus), 1)
        self.assertEqual(plus_minus[0].profile_number, 7)

        for item in plus_zero:
            self.assertEqual(item.scope, "PROFILE")
            self.assertEqual(item.doctrine_ids, ("DR_SZ_LEHR_1972_000353",))
            self.assertEqual(item.anti_inference_ids, ("AI_SZONDI_000017",))
            self.assertEqual(
                item.support_fact_ids,
                (f"foreground_profile_{item.profile_number}:vector:S:base_symbols",),
            )

        item = plus_minus[0]
        self.assertEqual(item.scope, "PROFILE")
        self.assertEqual(item.doctrine_ids, ("DR_SZ_LEHR_1972_000354",))
        self.assertEqual(item.anti_inference_ids, ("AI_SZONDI_000018",))
        self.assertEqual(
            item.support_fact_ids,
            ("foreground_profile_7:vector:S:base_symbols",),
        )

    def test_packet_carries_source_verified_evidence_for_both_s_configurations(self):
        packet = _fall40_packet()

        plus_zero = packet.doctrine("DR_SZ_LEHR_1972_000353")
        self.assertEqual(plus_zero.review_status, "SOURCE_VERIFIED")
        self.assertEqual(plus_zero.source_id, "SZ_LEHR_1972")
        self.assertIn("Personenbebe", plus_zero.source_excerpt)
        self.assertEqual(plus_zero.source_anchors[0].unit_start, "U001405")
        self.assertEqual(plus_zero.source_anchors[0].unit_end, "U001430")
        self.assertEqual(plus_zero.source_anchors[0].printed_page, 89)

        plus_minus = packet.doctrine("DR_SZ_LEHR_1972_000354")
        self.assertEqual(plus_minus.review_status, "SOURCE_VERIFIED")
        self.assertEqual(plus_minus.source_id, "SZ_LEHR_1972")
        self.assertIn("Passivität und Hingabe", plus_minus.source_excerpt)
        self.assertEqual(plus_minus.source_anchors[0].unit_start, "U001468")
        self.assertEqual(plus_minus.source_anchors[0].unit_end, "U001477")
        self.assertEqual(plus_minus.source_anchors[0].printed_page, 92)

    def test_synthesis_gate_accepts_only_the_exact_profile_support_bundle(self):
        packet = _fall40_packet()
        plus_zero = _profile_proposition(
            proposition_id="PROP_S_PLUS_ZERO_001",
            profile_number=1,
            claim_id="IC_SZONDI_PRIMARY_000017",
            doctrine_id="DR_SZ_LEHR_1972_000353",
            anti_inference_id="AI_SZONDI_000017",
            text=(
                "În profilul 1, S +0 este Unitendenz / Dominanz der Personenliebe "
                "la nivelul Vektorbild-ului sexual."
            ),
        )
        plus_minus = _profile_proposition(
            proposition_id="PROP_S_PLUS_MINUS_001",
            profile_number=7,
            claim_id="IC_SZONDI_PRIMARY_000018",
            doctrine_id="DR_SZ_LEHR_1972_000354",
            anti_inference_id="AI_SZONDI_000018",
            text=(
                "În profilul 7, S +− leagă bejahte Personenliebe de "
                "Passivität/Hingabe la nivelul configurației vectoriale."
            ),
        )

        self.assertEqual(
            validate_synthesis_propositions(packet, (plus_zero, plus_minus)),
            (plus_zero, plus_minus),
        )

        missing_guard = _profile_proposition(
            proposition_id="PROP_S_PLUS_ZERO_BAD",
            profile_number=1,
            claim_id="IC_SZONDI_PRIMARY_000017",
            doctrine_id="DR_SZ_LEHR_1972_000353",
            anti_inference_id="AI_SZONDI_000017",
            text="S +0.",
            anti_inference_ids=(),
        )
        with self.assertRaisesRegex(ValueError, "anti-inference bundle"):
            validate_synthesis_propositions(packet, (missing_guard,))

    def test_profile_claim_cannot_be_promoted_to_series_pattern(self):
        packet = _fall40_packet()
        promoted = SynthesisProposition(
            proposition_id="PROP_S_PLUS_ZERO_SERIES_BAD",
            scope="SERIES",
            profile_number=None,
            text="S +0 este patternul sexual dominant al seriei.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000017",),
            support_fact_ids=("foreground_profile_1:vector:S:base_symbols",),
            support_doctrine_ids=("DR_SZ_LEHR_1972_000353",),
            anti_inference_ids_applied=("AI_SZONDI_000017",),
        )
        with self.assertRaisesRegex(ValueError, "not active in the proposition scope"):
            validate_synthesis_propositions(packet, (promoted,))

    def test_profile_claim_cannot_be_moved_to_a_nonmatching_profile(self):
        packet = _fall40_packet()
        moved = _profile_proposition(
            proposition_id="PROP_S_PLUS_ZERO_PROFILE_7_BAD",
            profile_number=7,
            claim_id="IC_SZONDI_PRIMARY_000017",
            doctrine_id="DR_SZ_LEHR_1972_000353",
            anti_inference_id="AI_SZONDI_000017",
            text="Profilul 7 are S +0.",
        )
        with self.assertRaisesRegex(ValueError, "not active in the proposition scope"):
            validate_synthesis_propositions(packet, (moved,))

    def test_claim_guards_keep_overpressure_and_pathological_extensions_out_of_base_symbols(self):
        plus_zero = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000017"]
        plus_minus = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000018"]

        self.assertIn("Dominanz der Personenliebe", plus_zero.claim)
        blocked_zero = plus_zero.anti_inferences[0].prohibited_conclusion
        self.assertIn("preregenitale", blocked_zero)
        self.assertIn("homosexualității", blocked_zero)
        self.assertIn("quantum-aware", blocked_zero)

        self.assertIn("Passivität/Hingabe", plus_minus.claim)
        blocked_minus = plus_minus.anti_inferences[0].prohibited_conclusion
        self.assertIn("Triebzielinversion", blocked_minus)
        self.assertIn("Masochismus", blocked_minus)
        self.assertIn("Überdruck", blocked_minus)


if __name__ == "__main__":
    unittest.main()
