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


class SensitiveBeziehungsangstClaimTests(unittest.TestCase):
    def test_fall40_routes_only_the_two_exact_profile_local_findings(self):
        packet = _packet()
        findings = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000023"
        )

        self.assertEqual(len(findings), 2)
        self.assertEqual({item.profile_number for item in findings}, {1, 5})
        for item in findings:
            self.assertEqual(item.scope, "PROFILE")
            self.assertEqual(item.assertion_mode, "CONDITIONAL")
            self.assertEqual(item.doctrine_ids, ("DR_SZ_LEHR_1972_000361",))
            self.assertEqual(item.anti_inference_ids, ("AI_SZONDI_000023",))
            self.assertEqual(
                item.support_fact_ids,
                (
                    f"foreground_profile_{item.profile_number}:vector:P:base_symbols",
                    f"foreground_profile_{item.profile_number}:factor:hy:quantum_level",
                ),
            )

        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000023" and item.scope == "SERIES"
                for item in packet.report.findings
            )
        )

    def test_exact_ordinary_hy_activates_but_hy_overpressure_and_neighbours_do_not(self):
        exact = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "-", "0", "0", "0", "0"),)),
            production=True,
        )
        hy_overpressure = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "-!", "0", "0", "0", "0"),)),
            production=True,
        )
        e_negative = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "-", "-", "0", "0", "0", "0"),)),
            production=True,
        )
        hy_positive = evaluate_clinical_protocol(
            ProfileSeries((_profile("0", "0", "0", "+", "0", "0", "0", "0"),)),
            production=True,
        )

        self.assertTrue(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000023"
                for item in exact.profiles[0].interpretation.findings
            )
        )
        for evaluation in (hy_overpressure, e_negative, hy_positive):
            self.assertFalse(
                any(
                    item.claim_id == "IC_SZONDI_PRIMARY_000023"
                    for item in evaluation.profiles[0].interpretation.findings
                )
            )

    def test_doctrine_and_guard_preserve_historical_term_and_block_stronger_branches(self):
        packet = _packet()
        doctrine = packet.doctrine("DR_SZ_LEHR_1972_000361")
        self.assertEqual(doctrine.review_status, "SOURCE_VERIFIED")
        self.assertEqual(doctrine.source_id, "SZ_LEHR_1972")
        self.assertEqual(doctrine.assertion_strength, "ASSERTION")
        self.assertIn("sensitiven Beziehungsangst", doctrine.source_excerpt)
        self.assertIn("sensitive Beziehungsangst", doctrine.doctrinal_statement)
        self.assertIn("Überdruck", doctrine.doctrinal_statement)
        self.assertEqual(doctrine.source_anchors[0].unit_start, "U001650")
        self.assertEqual(doctrine.source_anchors[0].unit_end, "U001652")
        self.assertEqual(doctrine.source_anchors[1].unit_start, "U001746")
        self.assertEqual(doctrine.source_anchors[1].unit_end, "U001755")

        finding = next(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000023"
        )
        guard = finding.anti_inferences[0]
        self.assertIn("diagnostic psihiatric contemporan", guard)
        self.assertIn("biografie", guard)
        self.assertIn("SERIES", guard)
        self.assertIn("paranoider Zug", guard)
        self.assertIn("in schweren Fällen", guard)
        self.assertIn("hy-Überdruck", guard)


if __name__ == "__main__":
    unittest.main()
