import unittest

from szondi3.clinical_composition import (
    COEXISTENCE_ONLY,
    CONSTITUENT_EXPLAINS_COMPOSITE,
    EXPLICIT_DOCTRINAL_BRIDGE,
    NULL_SYNTHESIS,
    SAME_SUPPORT_BUNDLE,
    SAME_TRIGGER_EXTENDS_MEANING,
    build_foreground_clinical_composition,
)
from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
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


def _composition(profile):
    evaluation = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
    packet = build_clinical_evidence_packet(evaluation)
    return build_foreground_clinical_composition(packet).profile(1)


def _relation_types(profile_composition):
    return {item.relation_type for item in profile_composition.relations}


class ClinicalCompositionPrototypeTests(unittest.TestCase):
    def test_reference_case_compiles_introinflation_nucleus_without_merging_other_nuclei(self):
        # h- s+ | e+ hy0 | k+ p+ | d- m-
        composed = _composition(
            _profile(h="-", s="+", e="+", hy="0", k="+", p="+", d="-", m="-")
        )

        introinflation = composed.nucleus_for_claim("IC_SZONDI_PRIMARY_000042")
        self.assertIn("IC_SZONDI_PRIMARY_000008", introinflation.support_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000009", introinflation.support_claim_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000073", introinflation.support_claim_ids)

        identification = composed.nucleus_for_claim("IC_SZONDI_PRIMARY_000038")
        contact = composed.nucleus_for_claim("IC_SZONDI_PRIMARY_000078")
        self.assertNotEqual(introinflation.nucleus_id, identification.nucleus_id)
        self.assertNotEqual(introinflation.nucleus_id, contact.nucleus_id)
        self.assertNotEqual(identification.nucleus_id, contact.nucleus_id)
        self.assertEqual(composed.synthesis_mode, NULL_SYNTHESIS)

        relation_types = _relation_types(composed)
        self.assertIn(CONSTITUENT_EXPLAINS_COMPOSITE, relation_types)
        self.assertIn(SAME_TRIGGER_EXTENDS_MEANING, relation_types)
        self.assertIn(SAME_SUPPORT_BUNDLE, relation_types)
        self.assertIn(EXPLICIT_DOCTRINAL_BRIDGE, relation_types)

        no_bridge_pairs = {
            frozenset((item.left_nucleus_id, item.right_nucleus_id))
            for item in composed.no_bridge_relations
        }
        self.assertIn(
            frozenset((introinflation.nucleus_id, identification.nucleus_id)),
            no_bridge_pairs,
        )
        self.assertIn(
            frozenset((introinflation.nucleus_id, contact.nucleus_id)),
            no_bridge_pairs,
        )
        self.assertTrue(
            all(item.relation_type == COEXISTENCE_ONLY for item in composed.no_bridge_relations)
        )

    def test_control_a_remains_three_independent_meanings_with_null_synthesis(self):
        # S +0 | P 00 | Sch 00 | C +-
        composed = _composition(
            _profile(h="+", s="0", e="0", hy="0", k="0", p="0", d="+", m="-")
        )

        sexual = composed.nucleus_for_claim("IC_SZONDI_PRIMARY_000017")
        ego = composed.nucleus_for_claim("IC_SZONDI_PRIMARY_000012")
        contact = composed.nucleus_for_claim("IC_SZONDI_PRIMARY_000020")
        self.assertEqual(len({sexual.nucleus_id, ego.nucleus_id, contact.nucleus_id}), 3)
        self.assertEqual(composed.synthesis_mode, NULL_SYNTHESIS)

        target_ids = {sexual.nucleus_id, ego.nucleus_id, contact.nucleus_id}
        target_pairs = {
            frozenset((item.left_nucleus_id, item.right_nucleus_id))
            for item in composed.no_bridge_relations
            if item.left_nucleus_id in target_ids and item.right_nucleus_id in target_ids
        }
        self.assertEqual(len(target_pairs), 3)

    def test_control_b_preserves_probable_oft_bridge_without_causal_upgrade(self):
        # S 00 | P ±0 | Sch +0 | C 00
        composed = _composition(_profile(e="±", hy="0", k="+", p="0"))
        relation = composed.relation_for_anchor("IC_SZONDI_PRIMARY_000086")

        self.assertEqual(relation.relation_type, EXPLICIT_DOCTRINAL_BRIDGE)
        self.assertEqual(len(relation.claim_envelopes), 1)
        envelope = relation.claim_envelopes[0]
        self.assertEqual(envelope.assertion_mode, "PROBABLE")
        self.assertIn("oft", envelope.source_strength_note)
        self.assertEqual(envelope.doctrine_ids, ("DR_SZ_IA_1956_B_000055",))
        self.assertIn("AI_SZONDI_000086", envelope.anti_inference_ids)

        facts = {item.fact_id: item.value for item in relation.support_facts}
        self.assertEqual(
            facts["foreground_profile_1:vector:P:base_symbols"], ("±", "0")
        )
        self.assertEqual(
            facts["foreground_profile_1:vector:Sch:base_symbols"], ("+", "0")
        )
        self.assertEqual(facts["foreground_profile_1:factor:e:quantum_level"], 0)
        self.assertEqual(facts["foreground_profile_1:factor:k:quantum_level"], 0)

    def test_control_c_preserves_exact_quantum_fact_values_and_historical_boundary(self):
        # S 0+!! | P 00 | Sch 00 | C 00
        composed = _composition(_profile(s="+!!", e="0"))
        relation = composed.relation_for_anchor("IC_SZONDI_PRIMARY_000056")

        self.assertEqual(relation.relation_type, EXPLICIT_DOCTRINAL_BRIDGE)
        envelope = relation.claim_envelopes[0]
        self.assertEqual(envelope.assertion_mode, "CONDITIONAL")
        self.assertIn("Aggressionsgefahr", envelope.statement)
        self.assertIn("AI_SZONDI_000056", envelope.anti_inference_ids)

        facts = {item.fact_id: item.value for item in relation.support_facts}
        self.assertEqual(facts["foreground_profile_1:factor:s:base_symbol"], "+")
        self.assertEqual(facts["foreground_profile_1:factor:s:quantum_level"], 2)
        self.assertEqual(facts["foreground_profile_1:factor:e:base_symbol"], "0")
        self.assertEqual(facts["foreground_profile_1:factor:e:quantum_level"], 0)

        neighboring = _composition(_profile(s="+!", e="0"))
        with self.assertRaises(KeyError):
            neighboring.relation_for_anchor("IC_SZONDI_PRIMARY_000056")

    def test_same_trigger_extension_and_same_bundle_keep_original_claim_envelopes(self):
        composed = _composition(_profile(k="+", p="+"))
        extension = composed.relation_for_anchor("IC_SZONDI_PRIMARY_000073")

        self.assertEqual(extension.relation_type, SAME_TRIGGER_EXTENDS_MEANING)
        self.assertEqual(extension.support_claim_ids, ("IC_SZONDI_PRIMARY_000073",))
        self.assertIn("AI_SZONDI_000073", extension.claim_envelopes[0].anti_inference_ids)

        bundle = next(
            item
            for item in composed.relations
            if item.relation_type == SAME_SUPPORT_BUNDLE
            and "IC_SZONDI_PRIMARY_000042" in item.support_claim_ids
        )
        self.assertIn("IC_SZONDI_PRIMARY_000073", bundle.support_claim_ids)
        self.assertEqual(
            {item.assertion_mode for item in bundle.claim_envelopes},
            {"CONDITIONAL"},
        )

    def test_human_readable_dump_is_deterministic_and_exposes_no_bridge_state(self):
        profile = _profile(h="+", s="0", e="0", hy="0", k="0", p="0", d="+", m="-")
        evaluation = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
        packet = build_clinical_evidence_packet(evaluation)

        first = build_foreground_clinical_composition(packet).render_nucleus_dump()
        second = build_foreground_clinical_composition(packet).render_nucleus_dump()
        self.assertEqual(first, second)
        self.assertIn("synthesis=NULL_SYNTHESIS", first)
        self.assertIn("IC_SZONDI_PRIMARY_000017", first)
        self.assertIn("IC_SZONDI_PRIMARY_000012", first)
        self.assertIn("IC_SZONDI_PRIMARY_000020", first)
        self.assertIn("no-bridge=", first)

    def test_wrong_packet_type_fails_closed(self):
        with self.assertRaisesRegex(TypeError, "ClinicalEvidencePacket"):
            build_foreground_clinical_composition(object())


if __name__ == "__main__":
    unittest.main()
