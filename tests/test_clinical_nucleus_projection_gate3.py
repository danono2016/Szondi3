import unittest

from szondi3.clinical_composition import (
    CONSTITUENT_EXPLAINS_COMPOSITE,
    EXPLICIT_DOCTRINAL_BRIDGE,
    NULL_SYNTHESIS,
    SAME_TRIGGER_EXTENDS_MEANING,
)
from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_nucleus_projection import build_clinical_nucleus_projection
from szondi3.clinical_protocol import evaluate_clinical_protocol
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


def _profile(**overrides):
    return build_profile(
        _reaction(factor, overrides.get(factor, "0"))
        for factor in FACTORS
    )


def _packet(profile):
    evaluation = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
    return build_clinical_evidence_packet(evaluation)


def _projection(profile):
    packet = _packet(profile)
    return packet, build_clinical_nucleus_projection(packet)


def _ordered_distinct(values):
    return tuple(dict.fromkeys(values))


class ClinicalNucleusProjectionGate3Tests(unittest.TestCase):
    def test_reference_case_exposes_internal_n1_composition_and_keeps_n2_n3_separate(self):
        packet, projected = _projection(
            _profile(h="-", s="+", e="+", hy="0", k="+", p="+", d="-", m="-")
        )
        profile = projected.profile(1)

        n1 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000042")
        self.assertIn("IC_SZONDI_PRIMARY_000008", n1.support_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000009", n1.support_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000073", n1.support_claim_ids)
        self.assertIn(
            CONSTITUENT_EXPLAINS_COMPOSITE,
            {relation.relation_type for relation in n1.relations},
        )
        self.assertIn(
            SAME_TRIGGER_EXTENDS_MEANING,
            {relation.relation_type for relation in n1.relations},
        )
        self.assertEqual(tuple(item.relation_id for item in n1.relations), n1.relation_ids)

        n2 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000038")
        n3 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000078")
        self.assertEqual(len({n1.nucleus_id, n2.nucleus_id, n3.nucleus_id}), 3)
        self.assertEqual(profile.global_synthesis_mode, NULL_SYNTHESIS)
        self.assertIn(n2.nucleus_id, n1.coexistence_only_with)
        self.assertIn(n3.nucleus_id, n1.coexistence_only_with)
        self.assertIn(n3.nucleus_id, n2.coexistence_only_with)

        finding_index = {
            finding.claim_id: finding
            for finding in packet.report.findings
            if finding.scope == "PROFILE"
            and finding.profile_number == 1
            and finding.assertion_mode != "LIMITATION"
        }
        self.assertEqual(tuple(item.claim_id for item in n1.claim_envelopes), n1.support_claim_ids)
        for envelope in n1.claim_envelopes:
            finding = finding_index[envelope.claim_id]
            self.assertEqual(envelope.statement, finding.statement)
            self.assertEqual(envelope.assertion_mode, finding.assertion_mode)
            self.assertEqual(envelope.source_strength_note, finding.source_strength_note)
            self.assertEqual(envelope.doctrine_ids, finding.doctrine_ids)
            self.assertEqual(envelope.source_ids, finding.source_ids)
            self.assertEqual(envelope.support_fact_ids, finding.support_fact_ids)
            self.assertEqual(envelope.anti_inference_ids, finding.anti_inference_ids)
            self.assertEqual(envelope.anti_inferences, finding.anti_inferences)

        self.assertEqual(
            n1.authorized_meanings,
            tuple(envelope.statement for envelope in n1.claim_envelopes),
        )
        self.assertEqual(
            n1.doctrine_ids,
            _ordered_distinct(
                doctrine_id
                for envelope in n1.claim_envelopes
                for doctrine_id in envelope.doctrine_ids
            ),
        )
        self.assertEqual(
            n1.source_ids,
            _ordered_distinct(
                source_id
                for envelope in n1.claim_envelopes
                for source_id in envelope.source_ids
            ),
        )
        self.assertEqual(
            tuple(item.fact_id for item in n1.support_facts),
            _ordered_distinct(
                fact_id
                for envelope in n1.claim_envelopes
                for fact_id in envelope.support_fact_ids
            ),
        )
        self.assertEqual(
            n1.anti_inference_ids,
            _ordered_distinct(
                anti_id
                for envelope in n1.claim_envelopes
                for anti_id in envelope.anti_inference_ids
            ),
        )
        self.assertEqual(
            n1.anti_inferences,
            _ordered_distinct(
                text
                for envelope in n1.claim_envelopes
                for text in envelope.anti_inferences
            ),
        )
        self.assertEqual(
            n1.sensitive_domains,
            _ordered_distinct(
                domain
                for claim_id in n1.support_claim_ids
                for domain in finding_index[claim_id].sensitive_domains
            ),
        )

        dump = projected.render_clinical_dump()
        self.assertIn("GLOBAL_SYNTHESIS=NULL_SYNTHESIS", dump)
        self.assertIn("AUTHORIZED_RELATIONS", dump)
        self.assertIn("CONSTITUENT_EXPLAINS_COMPOSITE", dump)
        self.assertIn("SAME_TRIGGER_EXTENDS_MEANING", dump)
        self.assertIn("COEXISTENCE_ONLY_WITH=", dump)
        self.assertIn("CANNOT_ASSERT", dump)

    def test_control_a_makes_null_synthesis_and_no_bridge_explicit(self):
        _, projected = _projection(
            _profile(h="+", s="0", e="0", hy="0", k="0", p="0", d="+", m="-")
        )
        profile = projected.profile(1)

        sexual = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000017")
        ego = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000012")
        contact = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000020")
        target_ids = {sexual.nucleus_id, ego.nucleus_id, contact.nucleus_id}

        self.assertEqual(len(target_ids), 3)
        self.assertEqual(profile.global_synthesis_mode, NULL_SYNTHESIS)
        for nucleus in (sexual, ego, contact):
            self.assertEqual(
                set(nucleus.coexistence_only_with) & target_ids,
                target_ids - {nucleus.nucleus_id},
            )

        target_pairs = {
            frozenset((item.left_nucleus_id, item.right_nucleus_id))
            for item in profile.no_bridge_relations
            if item.left_nucleus_id in target_ids and item.right_nucleus_id in target_ids
        }
        self.assertEqual(len(target_pairs), 3)

        dump = projected.render_clinical_dump()
        self.assertIn("GLOBAL_SYNTHESIS=NULL_SYNTHESIS", dump)
        self.assertIn("IC_SZONDI_PRIMARY_000017", dump)
        self.assertIn("IC_SZONDI_PRIMARY_000012", dump)
        self.assertIn("IC_SZONDI_PRIMARY_000020", dump)
        self.assertIn("COEXISTENCE_ONLY_WITH=", dump)

    def test_control_b_preserves_probable_oft_bridge_and_full_provenance(self):
        packet, projected = _projection(_profile(e="±", hy="0", k="+", p="0"))
        profile = projected.profile(1)
        nucleus = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000086")

        bridge = next(
            relation
            for relation in nucleus.relations
            if relation.anchor_claim_id == "IC_SZONDI_PRIMARY_000086"
        )
        self.assertEqual(bridge.relation_type, EXPLICIT_DOCTRINAL_BRIDGE)

        envelope = next(
            item
            for item in nucleus.claim_envelopes
            if item.claim_id == "IC_SZONDI_PRIMARY_000086"
        )
        self.assertEqual(envelope.assertion_mode, "PROBABLE")
        self.assertIn("oft", envelope.source_strength_note)
        self.assertEqual(envelope.doctrine_ids, ("DR_SZ_IA_1956_B_000055",))
        self.assertIn("AI_SZONDI_000086", envelope.anti_inference_ids)

        source_finding = next(
            finding
            for finding in packet.report.findings
            if finding.scope == "PROFILE"
            and finding.profile_number == 1
            and finding.claim_id == "IC_SZONDI_PRIMARY_000086"
        )
        self.assertEqual(envelope.source_ids, source_finding.source_ids)
        self.assertTrue(set(envelope.source_ids).issubset(set(nucleus.source_ids)))
        self.assertIn("DR_SZ_IA_1956_B_000055", nucleus.doctrine_ids)

        facts = {item.fact_id: item.value for item in nucleus.support_facts}
        self.assertEqual(facts["foreground_profile_1:vector:P:base_symbols"], ("±", "0"))
        self.assertEqual(facts["foreground_profile_1:vector:Sch:base_symbols"], ("+", "0"))
        self.assertEqual(facts["foreground_profile_1:factor:e:quantum_level"], 0)
        self.assertEqual(facts["foreground_profile_1:factor:k:quantum_level"], 0)

        dump = projected.render_clinical_dump()
        self.assertIn("EXPLICIT_DOCTRINAL_BRIDGE", dump)
        self.assertIn("IC_SZONDI_PRIMARY_000086 [PROBABLE]", dump)
        self.assertIn("oft", dump)
        self.assertIn("DR_SZ_IA_1956_B_000055", dump)
        self.assertIn("AI_SZONDI_000086", dump)

    def test_control_c_preserves_exact_quantum_historical_term_and_neighboring_negative(self):
        _, projected = _projection(_profile(s="+!!", e="0"))
        profile = projected.profile(1)
        nucleus = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000056")

        envelope = next(
            item
            for item in nucleus.claim_envelopes
            if item.claim_id == "IC_SZONDI_PRIMARY_000056"
        )
        self.assertEqual(envelope.assertion_mode, "CONDITIONAL")
        self.assertIn("Aggressionsgefahr", envelope.statement)
        self.assertIn("AI_SZONDI_000056", envelope.anti_inference_ids)

        facts = {item.fact_id: item.value for item in nucleus.support_facts}
        self.assertEqual(facts["foreground_profile_1:factor:s:base_symbol"], "+")
        self.assertEqual(facts["foreground_profile_1:factor:s:quantum_level"], 2)
        self.assertEqual(facts["foreground_profile_1:factor:e:base_symbol"], "0")
        self.assertEqual(facts["foreground_profile_1:factor:e:quantum_level"], 0)

        dump = projected.render_clinical_dump()
        self.assertIn("Aggressionsgefahr", dump)
        self.assertIn("foreground_profile_1:factor:s:quantum_level -> 2", dump)
        self.assertIn("foreground_profile_1:factor:e:base_symbol -> 0", dump)
        self.assertIn("AI_SZONDI_000056", dump)

        _, neighboring = _projection(_profile(s="+!", e="0"))
        with self.assertRaises(KeyError):
            neighboring.profile(1).nucleus_for_claim("IC_SZONDI_PRIMARY_000056")

    def test_projection_dump_is_deterministic_and_wrong_input_fails_closed(self):
        profile = _profile(h="+", s="0", e="0", hy="0", k="0", p="0", d="+", m="-")
        packet = _packet(profile)

        first = build_clinical_nucleus_projection(packet)
        second = build_clinical_nucleus_projection(packet)
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.render_clinical_dump(), second.render_clinical_dump())

        with self.assertRaisesRegex(TypeError, "ClinicalEvidencePacket"):
            build_clinical_nucleus_projection(object())


if __name__ == "__main__":
    unittest.main()
