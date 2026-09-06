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


class SchEntfremdungClaimTests(unittest.TestCase):
    def test_fall40_routes_only_profile_one(self):
        packet = _packet()
        findings = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000024"
        )

        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding.profile_number, 1)
        self.assertEqual(finding.scope, "PROFILE")
        self.assertEqual(finding.assertion_mode, "CONDITIONAL")
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_LEHR_1972_000285",))
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000024",))
        self.assertEqual(
            finding.support_fact_ids,
            (
                "foreground_profile_1:vector:Sch:base_symbols",
                "foreground_profile_1:factor:k:quantum_level",
                "foreground_profile_1:factor:p:quantum_level",
            ),
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000024" and item.scope == "SERIES"
                for item in packet.report.findings
            )
        )

    def test_exact_ordinary_sch_minus_ambivalent_activates_but_quantum_and_neighbours_do_not(self):
        exact = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "0", "-", "±", "0", "0"),)),
            production=True,
        )
        k_overpressure = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "0", "-!", "±", "0", "0"),)),
            production=True,
        )
        p_overpressure = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "0", "-", "±!", "0", "0"),)),
            production=True,
        )
        sch_minus_plus = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "0", "-", "+", "0", "0"),)),
            production=True,
        )
        sch_ambivalent_ambivalent = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "0", "±", "±", "0", "0"),)),
            production=True,
        )

        self.assertTrue(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000024"
                for item in exact.profiles[0].interpretation.findings
            )
        )
        for evaluation in (
            k_overpressure,
            p_overpressure,
            sch_minus_plus,
            sch_ambivalent_ambivalent,
        ):
            self.assertFalse(
                any(
                    item.claim_id == "IC_SZONDI_PRIMARY_000024"
                    for item in evaluation.profiles[0].interpretation.findings
                )
            )

    def test_existing_doctrine_and_guard_keep_the_meaning_testological(self):
        packet = _packet()
        doctrine = packet.doctrine("DR_SZ_LEHR_1972_000285")
        self.assertEqual(doctrine.review_status, "SOURCE_VERIFIED")
        self.assertEqual(doctrine.source_id, "SZ_LEHR_1972")
        self.assertEqual(doctrine.assertion_strength, "ASSERTION")
        self.assertIn("Entfremdung", doctrine.doctrinal_statement)
        self.assertIn("gehemmte Projektion", doctrine.doctrinal_statement)
        self.assertEqual(doctrine.source_anchors[0].unit_start, "U002395")
        self.assertEqual(doctrine.source_anchors[0].unit_end, "U002401")

        finding = next(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000024"
        )
        guard = finding.anti_inferences[0]
        self.assertIn("diagnostic clinic contemporan", guard)
        self.assertIn("realitatea", guard)
        self.assertIn("nosologică", guard)
        self.assertIn("biografie", guard)
        self.assertIn("SERIES", guard)
        self.assertIn("Überdruck", guard)

    def test_synthesis_gate_accepts_exact_bundle_and_rejects_series_or_missing_guard(self):
        packet = _packet()
        exact = SynthesisProposition(
            proposition_id="PROP_SCH_ENTFREMDUNG_001",
            scope="PROFILE",
            profile_number=1,
            text=(
                "În profilul 1, Sch −± fără Überdruck poate fi denumit testologic "
                "«Entfremdung» / «gehemmte Projektion»."
            ),
            support_claim_ids=("IC_SZONDI_PRIMARY_000024",),
            support_fact_ids=(
                "foreground_profile_1:vector:Sch:base_symbols",
                "foreground_profile_1:factor:k:quantum_level",
                "foreground_profile_1:factor:p:quantum_level",
            ),
            support_doctrine_ids=("DR_SZ_LEHR_1972_000285",),
            anti_inference_ids_applied=("AI_SZONDI_000024",),
        )
        self.assertEqual(validate_synthesis_propositions(packet, (exact,)), (exact,))

        promoted = SynthesisProposition(
            proposition_id="PROP_SCH_ENTFREMDUNG_SERIES_BAD",
            scope="SERIES",
            profile_number=None,
            text="Seria ar demonstra un Eu global definit prin Entfremdung.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000024",),
            support_fact_ids=(
                "foreground_profile_1:vector:Sch:base_symbols",
                "foreground_profile_1:factor:k:quantum_level",
                "foreground_profile_1:factor:p:quantum_level",
            ),
            support_doctrine_ids=("DR_SZ_LEHR_1972_000285",),
            anti_inference_ids_applied=("AI_SZONDI_000024",),
        )
        with self.assertRaisesRegex(ValueError, "not active in the proposition scope"):
            validate_synthesis_propositions(packet, (promoted,))

        missing_guard = SynthesisProposition(
            proposition_id="PROP_SCH_ENTFREMDUNG_GUARD_BAD",
            scope="PROFILE",
            profile_number=1,
            text="Sch −± ar permite o concluzie clinică modernă mai puternică.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000024",),
            support_fact_ids=(
                "foreground_profile_1:vector:Sch:base_symbols",
                "foreground_profile_1:factor:k:quantum_level",
                "foreground_profile_1:factor:p:quantum_level",
            ),
            support_doctrine_ids=("DR_SZ_LEHR_1972_000285",),
            anti_inference_ids_applied=(),
        )
        with self.assertRaisesRegex(ValueError, "anti-inference bundle"):
            validate_synthesis_propositions(packet, (missing_guard,))


if __name__ == "__main__":
    unittest.main()
