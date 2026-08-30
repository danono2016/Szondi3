import unittest

from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.clinical_synthesis import (
    SynthesisProposition,
    validate_synthesis_propositions,
)
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
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


def _profile(*symbols: str):
    return build_profile(
        _reaction(factor, symbol)
        for factor, symbol in zip(_FACTORS, symbols)
    )


def _fall40_series() -> ProfileSeries:
    return ProfileSeries(
        (
            _profile("+!", "0", "0", "-", "-", "±", "+", "-"),
            _profile("+!", "0", "-", "-", "-", "+", "+", "-"),
            _profile("+", "0", "-", "-", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-"),
            _profile("+", "0", "0", "-", "+", "±", "+", "-!!"),
            _profile("+!", "0", "-", "-!", "+", "±", "+", "-!"),
            _profile("+!", "-", "-", "0", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "0", "±", "±", "+", "-!"),
        )
    )


def _packet():
    return build_clinical_evidence_packet(
        evaluate_clinical_protocol(_fall40_series(), production=True)
    )


class TendernessMoralCensorshipClaimTests(unittest.TestCase):
    def test_fall40_routes_only_exact_profile_local_composite(self):
        packet = _packet()
        findings = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000022"
        )

        self.assertEqual(len(findings), 4)
        self.assertEqual({item.profile_number for item in findings}, {1, 2, 4, 8})
        for item in findings:
            self.assertEqual(item.scope, "PROFILE")
            self.assertEqual(
                item.doctrine_ids,
                ("DR_SZ_TRIEBPATH_1_000001", "DR_SZ_LEHR_1972_000360"),
            )
            self.assertEqual(item.anti_inference_ids, ("AI_SZONDI_000022",))
            self.assertEqual(
                item.support_fact_ids,
                (
                    f"foreground_profile_{item.profile_number}:factor:h:base_symbol",
                    f"foreground_profile_{item.profile_number}:factor:h:quantum_level",
                    f"foreground_profile_{item.profile_number}:factor:hy:base_symbol",
                    f"foreground_profile_{item.profile_number}:factor:hy:quantum_level",
                ),
            )

        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000022" and item.scope == "SERIES"
                for item in packet.report.findings
            )
        )

    def test_doctrine_bundle_preserves_example_and_independent_general_confirmation(self):
        packet = _packet()
        example = packet.doctrine("DR_SZ_TRIEBPATH_1_000001")
        general = packet.doctrine("DR_SZ_LEHR_1972_000360")

        self.assertEqual(example.review_status, "SOURCE_VERIFIED")
        self.assertEqual(example.source_id, "SZ_TRIEBPATH_1")
        self.assertEqual(example.source_anchors[0].unit_start, "U001381")
        self.assertEqual(example.source_anchors[0].unit_end, "U001388")
        self.assertIn("Zwei Beispiele", example.source_excerpt)
        self.assertIn("h = +!", example.source_anchors[0].visual_arbitration_note)
        self.assertIn("hy = −", example.source_anchors[0].visual_arbitration_note)

        self.assertEqual(general.review_status, "SOURCE_VERIFIED")
        self.assertEqual(general.source_id, "SZ_LEHR_1972")
        self.assertEqual(general.source_anchors[0].unit_start, "U000757")
        self.assertEqual(general.source_anchors[1].unit_start, "U001718")
        self.assertEqual(general.source_anchors[2].unit_start, "U001734")
        self.assertIn("Zärtlichkeits-", general.source_excerpt)
        self.assertIn("0 hy", general.source_excerpt)

    def test_exact_quantum_boundary_excludes_h_plus_and_hy_overdruck(self):
        exact = evaluate_clinical_protocol(
            ProfileSeries((_profile("+!", "0", "0", "-", "0", "0", "0", "0"),)),
            production=True,
        )
        h_without_quantum = evaluate_clinical_protocol(
            ProfileSeries((_profile("+", "0", "0", "-", "0", "0", "0", "0"),)),
            production=True,
        )
        hy_overdruck = evaluate_clinical_protocol(
            ProfileSeries((_profile("+!", "0", "0", "-!", "0", "0", "0", "0"),)),
            production=True,
        )
        hy_null = evaluate_clinical_protocol(
            ProfileSeries((_profile("+!", "0", "0", "0", "0", "0", "0", "0"),)),
            production=True,
        )

        self.assertTrue(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000022"
                for item in exact.profiles[0].interpretation.findings
            )
        )
        for evaluation in (h_without_quantum, hy_overdruck, hy_null):
            self.assertFalse(
                any(
                    item.claim_id == "IC_SZONDI_PRIMARY_000022"
                    for item in evaluation.profiles[0].interpretation.findings
                )
            )

    def test_synthesis_gate_accepts_exact_bundle_and_rejects_series_or_guard_drift(self):
        packet = _packet()
        support_facts = (
            "foreground_profile_1:factor:h:base_symbol",
            "foreground_profile_1:factor:h:quantum_level",
            "foreground_profile_1:factor:hy:base_symbol",
            "foreground_profile_1:factor:hy:quantum_level",
        )
        proposition = SynthesisProposition(
            proposition_id="PROP_H_HY_001",
            scope="PROFILE",
            profile_number=1,
            text=(
                "În profilul 1, configurația exactă h +! cu hy − permite lectura "
                "Zärtlichkeitsansprüche încărcate, cu moralische Zensur în direcția "
                "Sich-Verbergen, strict la nivelul configurației de profil."
            ),
            support_claim_ids=("IC_SZONDI_PRIMARY_000022",),
            support_fact_ids=support_facts,
            support_doctrine_ids=(
                "DR_SZ_TRIEBPATH_1_000001",
                "DR_SZ_LEHR_1972_000360",
            ),
            anti_inference_ids_applied=("AI_SZONDI_000022",),
        )
        self.assertEqual(
            validate_synthesis_propositions(packet, (proposition,)),
            (proposition,),
        )

        promoted = SynthesisProposition(
            proposition_id="PROP_H_HY_SERIES_BAD",
            scope="SERIES",
            profile_number=None,
            text="Recurența h +! cu hy − ar demonstra o trăsătură stabilă a seriei.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000022",),
            support_fact_ids=support_facts,
            support_doctrine_ids=(
                "DR_SZ_TRIEBPATH_1_000001",
                "DR_SZ_LEHR_1972_000360",
            ),
            anti_inference_ids_applied=("AI_SZONDI_000022",),
        )
        with self.assertRaisesRegex(ValueError, "not active in the proposition scope"):
            validate_synthesis_propositions(packet, (promoted,))

        missing_guard = SynthesisProposition(
            proposition_id="PROP_H_HY_GUARD_BAD",
            scope="PROFILE",
            profile_number=1,
            text="h +! cu hy − ar demonstra o iubire ascunsă reală.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000022",),
            support_fact_ids=support_facts,
            support_doctrine_ids=(
                "DR_SZ_TRIEBPATH_1_000001",
                "DR_SZ_LEHR_1972_000360",
            ),
            anti_inference_ids_applied=(),
        )
        with self.assertRaisesRegex(ValueError, "anti-inference bundle"):
            validate_synthesis_propositions(packet, (missing_guard,))


if __name__ == "__main__":
    unittest.main()
