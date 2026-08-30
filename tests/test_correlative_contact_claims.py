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


def _fall40_series() -> ProfileSeries:
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
                for factor, symbol in zip(_FACTORS, row)
            )
            for row in rows
        )
    )


def _packet():
    return build_clinical_evidence_packet(
        evaluate_clinical_protocol(_fall40_series(), production=True)
    )


class CorrelativeAndContactClaimTests(unittest.TestCase):
    def test_fall40_routes_one_antimosaic_guard_and_ten_contact_findings(self):
        packet = _packet()
        antimosaic = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000019"
        )
        contact = tuple(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000020"
        )

        self.assertEqual(len(antimosaic), 1)
        self.assertEqual(antimosaic[0].scope, "SERIES")
        self.assertIsNone(antimosaic[0].profile_number)
        self.assertEqual(
            antimosaic[0].support_fact_ids,
            ("profile_series:profile_count",),
        )
        self.assertEqual(
            antimosaic[0].doctrine_ids,
            ("DR_SZ_LEHR_1972_000296", "DR_SZ_LEHR_1972_000297"),
        )
        self.assertEqual(antimosaic[0].anti_inference_ids, ("AI_SZONDI_000019",))

        self.assertEqual(len(contact), 10)
        self.assertEqual({item.profile_number for item in contact}, set(range(1, 11)))
        for item in contact:
            self.assertEqual(item.scope, "PROFILE")
            self.assertEqual(item.doctrine_ids, ("DR_SZ_LEHR_1972_000358",))
            self.assertEqual(item.anti_inference_ids, ("AI_SZONDI_000020",))
            self.assertEqual(
                item.support_fact_ids,
                (f"foreground_profile_{item.profile_number}:vector:C:base_symbols",),
            )

    def test_packet_carries_exact_correlative_and_contact_doctrine(self):
        packet = _packet()
        antimosaic = packet.doctrine("DR_SZ_LEHR_1972_000296")
        self.assertEqual(antimosaic.review_status, "SOURCE_VERIFIED")
        self.assertEqual(antimosaic.source_id, "SZ_LEHR_1972")
        self.assertIn("mzosuzkipiel", antimosaic.source_excerpt)
        self.assertEqual(antimosaic.source_anchors[0].unit_start, "U002974")
        self.assertEqual(antimosaic.source_anchors[0].unit_end, "U002976")

        correlative = packet.doctrine("DR_SZ_LEHR_1972_000297")
        self.assertEqual(correlative.review_status, "SOURCE_VERIFIED")
        self.assertEqual(correlative.source_id, "SZ_LEHR_1972")
        self.assertIn("nicht als Ein^elreaktion isoliert", correlative.source_excerpt)
        self.assertEqual(correlative.source_anchors[0].unit_start, "U002977")
        self.assertEqual(correlative.source_anchors[0].unit_end, "U002982")

        contact = packet.doctrine("DR_SZ_LEHR_1972_000358")
        self.assertEqual(contact.review_status, "SOURCE_VERIFIED")
        self.assertEqual(contact.source_id, "SZ_LEHR_1972")
        self.assertIn("Auf-Suche-Gehen (+ d)", contact.source_excerpt)
        self.assertEqual(contact.source_anchors[1].unit_start, "U002816")
        self.assertEqual(contact.source_anchors[1].unit_end, "U002827")

    def test_synthesis_gate_accepts_exact_antimosaic_and_contact_bundles(self):
        packet = _packet()
        antimosaic = SynthesisProposition(
            proposition_id="PROP_ANTIMOSAIC_001",
            scope="SERIES",
            profile_number=None,
            text=(
                "Sensurile izolate nu sunt transformate prin simplă juxtapunere "
                "într-o descriere individualizată."
            ),
            support_claim_ids=("IC_SZONDI_PRIMARY_000019",),
            support_fact_ids=("profile_series:profile_count",),
            support_doctrine_ids=(
                "DR_SZ_LEHR_1972_000296",
                "DR_SZ_LEHR_1972_000297",
            ),
            anti_inference_ids_applied=("AI_SZONDI_000019",),
        )
        contact = SynthesisProposition(
            proposition_id="PROP_C_PLUS_MINUS_001",
            scope="PROFILE",
            profile_number=1,
            text=(
                "În profilul 1, C +− exprimă simultan desprinderea prin −m și "
                "pornirea în căutare prin +d la nivelul configurației contactuale."
            ),
            support_claim_ids=("IC_SZONDI_PRIMARY_000020",),
            support_fact_ids=("foreground_profile_1:vector:C:base_symbols",),
            support_doctrine_ids=("DR_SZ_LEHR_1972_000358",),
            anti_inference_ids_applied=("AI_SZONDI_000020",),
        )
        self.assertEqual(
            validate_synthesis_propositions(packet, (antimosaic, contact)),
            (antimosaic, contact),
        )

    def test_contact_profile_claim_cannot_be_promoted_to_series(self):
        packet = _packet()
        promoted = SynthesisProposition(
            proposition_id="PROP_C_PLUS_MINUS_SERIES_BAD",
            scope="SERIES",
            profile_number=None,
            text="C +− este patternul relațional global al persoanei.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000020",),
            support_fact_ids=("foreground_profile_1:vector:C:base_symbols",),
            support_doctrine_ids=("DR_SZ_LEHR_1972_000358",),
            anti_inference_ids_applied=("AI_SZONDI_000020",),
        )
        with self.assertRaisesRegex(ValueError, "not active in the proposition scope"):
            validate_synthesis_propositions(packet, (promoted,))

    def test_antimosaic_guard_cannot_be_dropped(self):
        packet = _packet()
        missing_guard = SynthesisProposition(
            proposition_id="PROP_ANTIMOSAIC_BAD",
            scope="SERIES",
            profile_number=None,
            text="Findings-urile formează o descriere globală.",
            support_claim_ids=("IC_SZONDI_PRIMARY_000019",),
            support_fact_ids=("profile_series:profile_count",),
            support_doctrine_ids=(
                "DR_SZ_LEHR_1972_000296",
                "DR_SZ_LEHR_1972_000297",
            ),
            anti_inference_ids_applied=(),
        )
        with self.assertRaisesRegex(ValueError, "anti-inference bundle"):
            validate_synthesis_propositions(packet, (missing_guard,))


if __name__ == "__main__":
    unittest.main()
