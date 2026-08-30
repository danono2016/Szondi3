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


class AnnahmeAffectClaimTests(unittest.TestCase):
    def test_fall40_routes_five_profile_local_probable_findings(self):
        packet = _packet()
        findings = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000021"
        )

        self.assertEqual(len(findings), 5)
        self.assertEqual({item.profile_number for item in findings}, {4, 5, 6, 8, 9})
        for item in findings:
            self.assertEqual(item.scope, "PROFILE")
            self.assertEqual(item.assertion_mode, "PROBABLE")
            self.assertEqual(item.doctrine_ids, ("DR_SZ_IA_1956_B_000053",))
            self.assertEqual(item.anti_inference_ids, ("AI_SZONDI_000021",))
            self.assertEqual(
                item.support_fact_ids,
                (f"foreground_profile_{item.profile_number}:vector:Sch:base_symbols",),
            )

        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000021" and item.scope == "SERIES"
                for item in packet.report.findings
            )
        )

    def test_doctrine_preserves_source_modality_and_exact_comparison_boundary(self):
        doctrine = _packet().doctrine("DR_SZ_IA_1956_B_000053")
        self.assertEqual(doctrine.review_status, "SOURCE_VERIFIED")
        self.assertEqual(doctrine.source_id, "SZ_IA_1956_B")
        self.assertIn("scheinen", doctrine.source_excerpt)
        self.assertIn("Angst seltener", doctrine.source_excerpt)
        self.assertEqual(doctrine.assertion_strength, "PROBABILITY")
        self.assertEqual(doctrine.source_anchors[0].unit_start, "U001044")
        self.assertEqual(doctrine.source_anchors[0].unit_end, "U001047")
        self.assertEqual(doctrine.source_anchors[0].printed_page, "358-359")
        self.assertIn("Sch ±+", doctrine.doctrinal_statement)
        self.assertIn("Sch −0", doctrine.doctrinal_statement)
        self.assertIn("Sch ±±", doctrine.doctrinal_statement)
        self.assertIn("Sch ±−", doctrine.doctrinal_statement)

    def test_exact_sch_plus_ambivalent_activates_but_other_sch_does_not(self):
        exact = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "0", "+", "±", "0", "0"),)),
            production=True,
        )
        other = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "0", "+", "+", "0", "0"),)),
            production=True,
        )
        self.assertTrue(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000021"
                for item in exact.profiles[0].interpretation.findings
            )
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000021"
                for item in other.profiles[0].interpretation.findings
            )
        )

    def test_synthesis_gate_accepts_exact_bundle_and_rejects_scope_or_guard_drift(self):
        packet = _packet()
        proposition = SynthesisProposition(
            proposition_id="PROP_ANNAHME_AFFECT_001",
            scope="PROFILE",
            profile_number=4,
            text=(
                "În profilul 4, Sch +± este Annahme; în comparația exactă a sursei, "
                "această formă `scheinen` să aibă mai mult succes în Abwehr von "
                "Triebgefahren, iar Angst este descrisă ca mai rară decât la cele "
                "patru Abwehrarten imediat precedente, fără a măsura anxietatea reală."
            ),
            support_claim_ids=("IC_SZONDI_PRIMARY_000021",),
            support_fact_ids=("foreground_profile_4:vector:Sch:base_symbols",),
            support_doctrine_ids=("DR_SZ_IA_1956_B_000053",),
            anti_inference_ids_applied=("AI_SZONDI_000021",),
        )
        self.assertEqual(
            validate_synthesis_propositions(packet, (proposition,)),
            (proposition,),
        )

        promoted = SynthesisProposition(
            proposition_id="PROP_ANNAHME_AFFECT_SERIES_BAD",
            scope="SERIES",
            profile_number=None,
            text="Sch +± ar demonstra la nivelul seriei o anxietate redusă.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000021",),
            support_fact_ids=("foreground_profile_4:vector:Sch:base_symbols",),
            support_doctrine_ids=("DR_SZ_IA_1956_B_000053",),
            anti_inference_ids_applied=("AI_SZONDI_000021",),
        )
        with self.assertRaisesRegex(ValueError, "not active in the proposition scope"):
            validate_synthesis_propositions(packet, (promoted,))

        missing_guard = SynthesisProposition(
            proposition_id="PROP_ANNAHME_AFFECT_GUARD_BAD",
            scope="PROFILE",
            profile_number=4,
            text="Sch +± ar demonstra o anxietate redusă.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000021",),
            support_fact_ids=("foreground_profile_4:vector:Sch:base_symbols",),
            support_doctrine_ids=("DR_SZ_IA_1956_B_000053",),
            anti_inference_ids_applied=(),
        )
        with self.assertRaisesRegex(ValueError, "anti-inference bundle"):
            validate_synthesis_propositions(packet, (missing_guard,))


if __name__ == "__main__":
    unittest.main()
