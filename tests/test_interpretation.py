import unittest
from fractions import Fraction

from szondi3.clinical_interpretation import interpret_facts
from szondi3.clinical_facts import (
    dur_moll_facts,
    profile_facts,
    root_direction_facts,
    series_index_facts,
    series_profile_count_facts,
    social_index_facts,
)
from szondi3.interpretation import (
    ActivationStatus,
    AssertionMode,
    ClaimDefinition,
    EpistemicClass,
    Fact,
    InputState,
    LifecycleStatus,
    TriggerDefinition,
    TriggerKind,
    evaluate_catalogue,
    evaluate_claim,
)
from szondi3.interpretation_catalogue import CLAIMS_BY_ID, INITIAL_CLAIMS
from szondi3.linnaeus import RootDirectionEvidence
from szondi3.profile import build_profile
from szondi3.proportions import DurMollIndex, SocialIndex
from szondi3.scoring import FactorReaction
from szondi3.series import SeriesIndices
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
        reaction(factor, *overrides.get(factor, ("null", 0))) for factor in FACTORS
    )


class InterpretationCoreTests(unittest.TestCase):
    def test_claim_requires_doctrine_provenance(self):
        with self.assertRaisesRegex(ValueError, "doctrineId"):
            ClaimDefinition(
                schema_version=1,
                claim_id="IC_TEST",
                rule_version=1,
                status=LifecycleStatus.DRAFT,
                source_layer="SZONDI_PRIMARY",
                doctrine_ids=(),
                source_ids=("SZ_TEST",),
                epistemic_class=EpistemicClass.SOURCE_ESTABLISHED_TRIGGER,
                assertion_mode=AssertionMode.LIMITATION,
                source_strength_note="test",
                claim="test",
                trigger=TriggerDefinition(TriggerKind.LIMITATION_GUARD, ()),
            )

    def test_implementation_inference_requires_rationale_and_reversal(self):
        with self.assertRaisesRegex(ValueError, "rationale"):
            ClaimDefinition(
                schema_version=1,
                claim_id="IC_TEST",
                rule_version=1,
                status=LifecycleStatus.DRAFT,
                source_layer="SZONDI_PRIMARY",
                doctrine_ids=("DR_TEST",),
                source_ids=("SZ_TEST",),
                epistemic_class=EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER,
                assertion_mode=AssertionMode.CONDITIONAL,
                source_strength_note="test",
                claim="test",
                trigger=TriggerDefinition(TriggerKind.EXACT_STRUCTURAL, ()),
            )

    def test_missing_fact_fails_closed(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000003"]
        result = evaluate_claim(claim, ())
        self.assertEqual(result.activation_status, ActivationStatus.UNRESOLVED_INPUT)
        self.assertEqual(result.missing_facts, ("series.indices.available",))

    def test_ambiguous_fact_fails_closed(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000003"]
        result = evaluate_claim(
            claim,
            (Fact("series.indices.available", True, input_state=InputState.AMBIGUOUS),),
        )
        self.assertEqual(result.activation_status, ActivationStatus.UNRESOLVED_INPUT)

    def test_production_mode_admits_approved_claims(self):
        facts = (Fact("series.indices.available", True),)
        results = evaluate_catalogue(INITIAL_CLAIMS, facts, production=True)
        self.assertEqual(len(results), len(INITIAL_CLAIMS))
        active_ids = {
            item.claim_id
            for item in results
            if item.activation_status is ActivationStatus.ACTIVE
        }
        self.assertIn("IC_SZONDI_PRIMARY_000003", active_ids)
        self.assertIn("IC_SZONDI_PRIMARY_000004", active_ids)


class ClinicalFactAdapterTests(unittest.TestCase):
    def test_profile_adapter_separates_base_symbol_from_quantum(self):
        facts = {item.key: item for item in profile_facts(profile({"k": ("negative", 2)}))}
        self.assertEqual(facts["profile.factor.k.base_symbol"].value, "-")
        self.assertEqual(facts["profile.factor.k.quantum_level"].value, 2)

    def test_series_profile_count_adapter_adds_no_interpretation(self):
        facts = series_profile_count_facts(10)
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0].key, "series.profile_count")
        self.assertEqual(facts[0].value, 10)
        self.assertEqual(facts[0].fact_id, "profile_series:profile_count")

    def test_series_adapter_preserves_undefined_tspqu(self):
        indices = SeriesIndices(
            null_reactions=8,
            ambivalent_reactions=0,
            total_factor_reactions=80,
            tendenzspannungsquotient=None,
            symptom_percentage=Fraction(10, 1),
        )
        facts = {item.key: item for item in series_index_facts(indices)}
        self.assertEqual(facts["series.tspqu"].input_state, InputState.UNDEFINED)
        self.assertEqual(facts["series.symptom_percentage"].value, Fraction(10, 1))

    def test_root_direction_adapter_does_not_invent_majority_sign(self):
        evidence = (
            RootDirectionEvidence("Schp", "p", 4, 3, 1, 0),
            RootDirectionEvidence("Ss", "s", 0, 7, 1, 0),
        )
        facts = {item.key: item for item in root_direction_facts(evidence)}
        self.assertEqual(facts["linnaeus.ambiguous_root_directions"].value, ("p",))
        self.assertEqual(facts["linnaeus.strict_negative_roots"].value, ("s",))


class InitialCatalogueTests(unittest.TestCase):
    def test_catalogue_has_unique_ids_and_clinician_approval(self):
        self.assertEqual(len(INITIAL_CLAIMS), 18)
        self.assertEqual(len(CLAIMS_BY_ID), len(INITIAL_CLAIMS))
        self.assertTrue(
            all(claim.status is LifecycleStatus.APPROVED for claim in INITIAL_CLAIMS)
        )

    def test_negative_root_activates_anti_repression_guard(self):
        evidence = (RootDirectionEvidence("Ss", "s", 0, 8, 0, 0),)
        result = evaluate_claim(
            CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000001"], root_direction_facts(evidence)
        )
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertEqual(result.anti_inferences[0].anti_inference_id, "AI_SZONDI_000001")

    def test_positive_root_activates_unsatisfied_need_guard(self):
        evidence = (RootDirectionEvidence("Ss", "s", 8, 0, 0, 0),)
        result = evaluate_claim(
            CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000002"], root_direction_facts(evidence)
        )
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)

    def test_tspqu_and_symptom_percentage_guards_activate_from_p1_indices(self):
        indices = SeriesIndices(8, 8, 80, Fraction(1, 1), Fraction(20, 1))
        facts = series_index_facts(indices)
        for claim_id in ("IC_SZONDI_PRIMARY_000003", "IC_SZONDI_PRIMARY_000004"):
            result = evaluate_claim(CLAIMS_BY_ID[claim_id], facts)
            self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)

    def test_dur_moll_guard_activates_from_p1_index(self):
        index = DurMollIndex((), 20, 20, Fraction(50, 1), Fraction(50, 1))
        result = evaluate_claim(
            CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000005"], dur_moll_facts(index)
        )
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)

    def test_social_index_criminality_guard_uses_exact_under_40_condition(self):
        low = SocialIndex((), 39, 61, Fraction(39, 1), Fraction(61, 1))
        boundary = SocialIndex((), 40, 60, Fraction(40, 1), Fraction(60, 1))
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000006"]
        self.assertEqual(
            evaluate_claim(claim, social_index_facts(low)).activation_status,
            ActivationStatus.ACTIVE,
        )
        self.assertEqual(
            evaluate_claim(claim, social_index_facts(boundary)).activation_status,
            ActivationStatus.INACTIVE,
        )

    def test_elementary_ego_projection_and_introjection_are_structural(self):
        facts = profile_facts(profile({"p": ("negative", 0), "k": ("positive", 0)}))
        self.assertEqual(
            evaluate_claim(CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000007"], facts).activation_status,
            ActivationStatus.ACTIVE,
        )
        self.assertEqual(
            evaluate_claim(CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000009"], facts).activation_status,
            ActivationStatus.ACTIVE,
        )

    def test_minus_k_activates_negation_but_keeps_repression_block(self):
        facts = profile_facts(profile({"k": ("negative", 1)}))
        result = evaluate_claim(CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000010"], facts)
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertTrue(
            any("Verdrängung" in item.prohibited_conclusion for item in result.anti_inferences)
        )

    def test_sch_ambivalent_ambivalent_keeps_integration_anti_overreach(self):
        facts = profile_facts(
            profile({"k": ("ambivalent", 0), "p": ("ambivalent", 0)})
        )
        result = evaluate_claim(CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000011"], facts)
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertTrue(result.anti_inferences)
        self.assertIn("DR_SZ_IA_1956_B_000009", result.provenance_trace)

    def test_sch_zero_zero_is_labelled_without_global_person_verdict(self):
        facts = profile_facts(profile())
        result = evaluate_claim(CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000012"], facts)
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertTrue(result.anti_inferences)

    def test_serial_method_claim_activates_only_for_eight_to_ten_profiles(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000014"]
        for count in (8, 9, 10):
            with self.subTest(count=count):
                result = evaluate_claim(claim, series_profile_count_facts(count))
                self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
                self.assertEqual(
                    result.matched_facts[0].fact_id,
                    "profile_series:profile_count",
                )
                self.assertEqual(
                    result.anti_inferences[0].anti_inference_id,
                    "AI_SZONDI_000014",
                )
        for count in (1, 7, 11):
            with self.subTest(count=count):
                result = evaluate_claim(claim, series_profile_count_facts(count))
                self.assertEqual(result.activation_status, ActivationStatus.INACTIVE)

    def test_clinician_preview_and_production_keep_approved_szondian_claim(self):
        facts = profile_facts(profile({"k": ("negative", 0)}))
        preview = interpret_facts(facts)
        finding = next(
            item for item in preview.findings if item.claim_id == "IC_SZONDI_PRIMARY_000010"
        )
        self.assertIn("DR_SZ_IA_1956_A_000049", finding.doctrine_ids)
        self.assertTrue(finding.anti_inferences)
        production = interpret_facts(facts, production=True)
        production_finding = next(
            item for item in production.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000010"
        )
        self.assertEqual(production_finding.lifecycle_status, "APPROVED")


if __name__ == "__main__":
    unittest.main()
