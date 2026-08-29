import unittest

from szondi3.clinical_evidence import build_clinical_evidence
from szondi3.clinical_integration import (
    IntegrationRelation,
    RelationKind,
    build_clinical_integration,
)
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def reaction(factor, kind="null", quantum=0):
    base = {"null": "0", "positive": "+", "negative": "-", "ambivalent": "±"}[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=base + ("!" * quantum),
        quantum_level=quantum,
    )


def profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


class ClinicalEvidenceTests(unittest.TestCase):
    def test_factor_pattern_counts_series_once_and_preserves_quantum(self):
        series = ProfileSeries(
            (
                profile({"h": ("positive", 1)}),
                profile({"h": ("positive", 0)}),
                profile({"h": ("negative", 2)}),
                profile({"h": ("ambivalent", 0)}),
            )
        )
        evidence = build_clinical_evidence(evaluate_clinical_protocol(series))
        h = evidence.pattern("h")

        self.assertEqual(h.symbols, ("+!", "+", "-!!", "±"))
        self.assertEqual(h.base_symbols, ("+", "+", "-", "±"))
        self.assertEqual(h.positive_profiles, (1, 2))
        self.assertEqual(h.negative_profiles, (3,))
        self.assertEqual(h.ambivalent_profiles, (4,))
        self.assertEqual(h.tensioned_profiles, (1, 3))
        self.assertEqual(h.quantum_total, 3)
        self.assertEqual(h.transitions, ((3, "+", "-"), (4, "-", "±")))

    def test_grounded_findings_have_case_local_unique_ids_and_keep_provenance(self):
        series = ProfileSeries((profile({"k": ("negative", 0)}),))
        evidence = build_clinical_evidence(evaluate_clinical_protocol(series, production=True))

        finding = next(item for item in evidence.findings if item.claim_id == "IC_SZONDI_PRIMARY_000010")
        self.assertEqual(finding.evidence_id, "EF_P01_IC_SZONDI_PRIMARY_000010")
        self.assertIn("DR_SZ_IA_1956_A_000049", finding.finding.doctrine_ids)
        self.assertTrue(finding.finding.anti_inferences)
        self.assertEqual(len(evidence.support_ids), len(set(evidence.support_ids)))

    def test_unresolved_calculation_and_interpretation_are_explicit_boundaries(self):
        series = ProfileSeries(tuple(profile() for _ in range(8)))
        evidence = build_clinical_evidence(evaluate_clinical_protocol(series))

        kinds = {item.kind for item in evidence.boundaries}
        subjects = {item.subject for item in evidence.boundaries}
        self.assertIn("UNRESOLVED_CALCULATION", kinds)
        self.assertIn("complete_formula", subjects)
        self.assertIn("IC_SZONDI_PRIMARY_000001", subjects)
        self.assertIn("IC_SZONDI_PRIMARY_000002", subjects)

    def test_wrong_input_type_fails(self):
        with self.assertRaisesRegex(TypeError, "ClinicalProtocolEvaluation"):
            build_clinical_evidence(())


class ClinicalIntegrationTests(unittest.TestCase):
    def test_first_p4_vocabulary_has_no_causal_relation(self):
        self.assertEqual(
            {item.value for item in RelationKind},
            {"COEXISTENCE", "CONTRAST", "LONGITUDINAL_CHANGE", "QUALIFICATION"},
        )
        with self.assertRaises(ValueError):
            RelationKind("CAUSES")

    def test_longitudinal_change_is_derived_only_from_actual_factor_change(self):
        series = ProfileSeries(
            (
                profile({"h": ("positive", 0), "m": ("negative", 0)}),
                profile({"h": ("positive", 1), "m": ("negative", 0)}),
                profile({"h": ("negative", 0), "m": ("negative", 1)}),
            )
        )
        integration = build_clinical_integration(evaluate_clinical_protocol(series))
        relation_ids = {item.relation_id for item in integration.relations}

        self.assertIn("IR_LONG_h", relation_ids)
        self.assertNotIn("IR_LONG_m", relation_ids)
        h_relation = next(item for item in integration.relations if item.relation_id == "IR_LONG_h")
        self.assertEqual(h_relation.kind, RelationKind.LONGITUDINAL_CHANGE)
        self.assertEqual(h_relation.support_ids, ("SP_FACTOR_h",))

    def test_explicit_relation_must_reference_existing_p3_support(self):
        evidence = build_clinical_evidence(
            evaluate_clinical_protocol(ProfileSeries((profile(),)))
        )
        relation = IntegrationRelation(
            relation_id="IR_TEST",
            kind=RelationKind.COEXISTENCE,
            support_ids=("DOES_NOT_EXIST",),
            statement="Test relation.",
        )
        with self.assertRaisesRegex(ValueError, "orphan support ids"):
            build_clinical_integration(
                evidence,
                relations=(relation,),
                include_longitudinal_relations=False,
            )

    def test_grounding_payload_is_direct_and_provenance_rich(self):
        integration = build_clinical_integration(
            evaluate_clinical_protocol(
                ProfileSeries((profile({"k": ("negative", 0)}),)),
                production=True,
            )
        )
        payload = integration.to_grounding_payload()
        finding = next(
            item for item in payload["findings"]
            if item["claim_id"] == "IC_SZONDI_PRIMARY_000010"
        )

        self.assertEqual(payload["schema_version"], 1)
        self.assertTrue(payload["production_mode"])
        self.assertIn("DR_SZ_IA_1956_A_000049", finding["doctrine_ids"])
        self.assertTrue(finding["anti_inferences"])
        self.assertNotIn("therapist_synthesis", payload)

    def test_duplicate_relation_ids_fail(self):
        evidence = build_clinical_evidence(
            evaluate_clinical_protocol(ProfileSeries((profile(),)))
        )
        first = IntegrationRelation(
            "IR_DUP",
            RelationKind.COEXISTENCE,
            ("SP_FACTOR_h", "SP_FACTOR_s"),
            "Coexistență formală.",
        )
        second = IntegrationRelation(
            "IR_DUP",
            RelationKind.CONTRAST,
            ("SP_FACTOR_e", "SP_FACTOR_hy"),
            "Contrast formal.",
        )
        with self.assertRaisesRegex(ValueError, "duplicate relation"):
            build_clinical_integration(
                evidence,
                relations=(first, second),
                include_longitudinal_relations=False,
            )


if __name__ == "__main__":
    unittest.main()
