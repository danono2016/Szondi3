import unittest

from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}


def _reaction(factor: str, symbol: str, *, forced_null: bool = False) -> FactorReaction:
    base = "±" if symbol.startswith("±") else symbol[0]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=_KIND[base],
        symbol="ø" if forced_null else symbol,
        quantum_level=symbol.count("!"),
        forced_null=forced_null,
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


def _configuration_counts(packet, vector: str):
    return {
        item.symbols: item.count
        for item in packet.vector(vector).configuration_frequencies
    }


class ClinicalEvidencePacketFall40Tests(unittest.TestCase):
    def test_fall40_packet_fixes_exact_morphology_before_any_narrative_model(self):
        packet = build_clinical_evidence_packet(
            evaluate_clinical_protocol(_fall40_series(), production=True)
        )

        self.assertEqual(packet.schema_version, 1)
        self.assertEqual(packet.report.header.profile_count, 10)
        self.assertTrue(packet.report.header.production_mode)

        h = packet.factor("h")
        self.assertEqual(h.positive_count, 10)
        self.assertEqual(h.tensioned_profiles, (1, 2, 4, 6, 7, 8))
        self.assertEqual(h.quantum_total, 6)

        s = packet.factor("s")
        self.assertEqual(s.null_count, 9)
        self.assertEqual(s.negative_count, 1)
        self.assertEqual(s.base_symbols[6], "-")

        e = packet.factor("e")
        self.assertEqual(e.negative_count, 8)
        self.assertEqual(e.null_count, 2)

        hy = packet.factor("hy")
        self.assertEqual(hy.negative_count, 8)
        self.assertEqual(hy.null_count, 2)
        self.assertEqual(hy.tensioned_profiles, (6,))

        k = packet.factor("k")
        self.assertEqual(k.base_symbols, ("-", "-", "+", "+", "+", "+", "+", "+", "+", "±"))

        p = packet.factor("p")
        self.assertEqual(p.positive_count, 3)
        self.assertEqual(p.ambivalent_count, 7)

        d = packet.factor("d")
        self.assertEqual(d.positive_count, 10)

        m = packet.factor("m")
        self.assertEqual(m.negative_count, 10)
        self.assertEqual(m.tensioned_profiles, (3, 5, 6, 7, 8, 9, 10))
        self.assertEqual(m.quantum_total, 8)

        self.assertEqual(
            _configuration_counts(packet, "P"),
            {("0", "-"): 2, ("-", "-"): 6, ("-", "0"): 2},
        )
        self.assertEqual(
            _configuration_counts(packet, "Sch"),
            {
                ("-", "±"): 1,
                ("-", "+"): 1,
                ("+", "+"): 2,
                ("+", "±"): 5,
                ("±", "±"): 1,
            },
        )
        self.assertEqual(_configuration_counts(packet, "C"), {("+", "-"): 10})
        self.assertEqual(_configuration_counts(packet, "S"), {("+", "0"): 9, ("+", "-"): 1})

        sch_integrated = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000011"
        )
        self.assertEqual(len(sch_integrated), 1)
        self.assertEqual(sch_integrated[0].profile_number, 10)
        self.assertEqual(
            sch_integrated[0].support_fact_ids,
            ("foreground_profile_10:vector:Sch:base_symbols",),
        )
        self.assertIn("SZ_LEHR_1972", sch_integrated[0].source_ids)

        payload = packet.to_dict()
        self.assertNotIn("therapist_synthesis", payload)
        self.assertEqual(payload["profile_count"], 10)
        self.assertEqual(
            payload["interpretation_release_state"],
            "PRODUCTION_APPROVED_CLAIMS_ONLY",
        )
        self.assertTrue(
            all(item["lifecycle_status"] == "APPROVED" for item in payload["findings"])
        )
        payload_sch_integrated = tuple(
            item
            for item in payload["findings"]
            if item["claim_id"] == "IC_SZONDI_PRIMARY_000011"
        )
        self.assertEqual(len(payload_sch_integrated), 1)
        self.assertEqual(
            payload_sch_integrated[0]["support_fact_ids"],
            ["foreground_profile_10:vector:Sch:base_symbols"],
        )

    def test_forced_null_remains_distinct_from_real_zero(self):
        factors = [
            _reaction("h", "+"),
            _reaction("s", "0", forced_null=True),
            _reaction("e", "-"),
            _reaction("hy", "-"),
            _reaction("k", "+"),
            _reaction("p", "±"),
            _reaction("d", "+"),
            _reaction("m", "-"),
        ]
        series = ProfileSeries((build_profile(factors),))
        packet = build_clinical_evidence_packet(evaluate_clinical_protocol(series))

        s = packet.factor("s")
        self.assertEqual(s.null_count, 0)
        self.assertEqual(s.forced_null_count, 1)
        self.assertEqual(s.base_symbols, ("ø",))
        self.assertEqual(packet.vector("S").base_symbols, (("+", "ø"),))


if __name__ == "__main__":
    unittest.main()
