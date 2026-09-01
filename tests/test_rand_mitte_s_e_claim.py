import unittest

from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_protocol import evaluate_clinical_protocol
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


def _evaluate(s_symbol: str, e_symbol: str):
    series = ProfileSeries(
        (_profile("0", s_symbol, e_symbol, "0", "0", "0", "0", "0"),)
    )
    return evaluate_clinical_protocol(series, production=True)


class RandMitteSEClaimTests(unittest.TestCase):
    def test_exact_s_double_overpressure_with_ordinary_e_positive_activates(self):
        evaluation = _evaluate("+!!", "+")
        packet = build_clinical_evidence_packet(evaluation)
        findings = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000055"
        )

        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding.scope, "PROFILE")
        self.assertEqual(finding.profile_number, 1)
        self.assertEqual(finding.assertion_mode, "CONDITIONAL")
        self.assertEqual(
            finding.doctrine_ids,
            ("DR_SZ_TRIEBPATH_1_000002", "DR_SZ_TRIEBPATH_1_000003"),
        )
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000055",))
        self.assertEqual(
            finding.support_fact_ids,
            (
                "foreground_profile_1:factor:s:base_symbol",
                "foreground_profile_1:factor:s:quantum_level",
                "foreground_profile_1:factor:e:base_symbol",
                "foreground_profile_1:factor:e:quantum_level",
            ),
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000055" and item.scope == "SERIES"
                for item in packet.report.findings
            )
        )

    def test_neighboring_quantum_configurations_do_not_activate(self):
        for s_symbol, e_symbol in (
            ("+!", "+"),
            ("+!!!", "+"),
            ("+!!", "+!"),
            ("+!!", "0"),
            ("-!!", "+"),
        ):
            with self.subTest(s=s_symbol, e=e_symbol):
                evaluation = _evaluate(s_symbol, e_symbol)
                self.assertFalse(
                    any(
                        item.claim_id == "IC_SZONDI_PRIMARY_000055"
                        for item in evaluation.profiles[0].interpretation.findings
                    )
                )

    def test_evidence_packet_accepts_clinician_reviewed_visual_arbitration(self):
        packet = build_clinical_evidence_packet(_evaluate("+!!", "+"))

        general = packet.doctrine("DR_SZ_TRIEBPATH_1_000002")
        exact = packet.doctrine("DR_SZ_TRIEBPATH_1_000003")

        self.assertEqual(general.review_status, "SOURCE_VERIFIED")
        self.assertEqual(exact.review_status, "CLINICIAN_REVIEWED")
        self.assertEqual(exact.source_id, "SZ_TRIEBPATH_1")
        self.assertEqual(exact.source_anchors[0].unit_start, "U001374")
        self.assertEqual(exact.source_anchors[0].unit_end, "U001380")
        self.assertIn("Aggressionsgefahr", exact.source_excerpt)
        self.assertIn("Aggressionsansprüche gutzumachen", exact.source_excerpt)
        self.assertIn("s +!!", exact.doctrinal_statement)
        self.assertIn("e +", exact.doctrinal_statement)

    def test_guard_keeps_behavior_and_defense_success_outside_claim(self):
        packet = build_clinical_evidence_packet(_evaluate("+!!", "+"))
        finding = next(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000055"
        )
        self.assertIn("AI_SZONDI_000055", finding.anti_inference_ids)
        self.assertIn(
            "nu dovada unei agresiuni comportamentale", finding.statement.lower()
        )
        self.assertIn(
            "nu dovada că apărarea este suficientă", finding.statement.lower()
        )


if __name__ == "__main__":
    unittest.main()
