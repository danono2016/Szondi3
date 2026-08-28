import unittest

from szondi3.interpretation import (
    ActivationStatus,
    ExecutableClaim,
    FactRef,
    InputState,
    Predicate,
    evaluate_claim,
)


class InterpretationTests(unittest.TestCase):
    def claim(self, **overrides):
        values = dict(
            claim_id="IC_SZONDI_PRIMARY_000001",
            rule_version="1",
            source_layer="SZONDI_PRIMARY",
            doctrine_ids=("DR_SZ_LEHR_1972_000313",),
            source_ids=("SZ_LEHR_1972",),
            canonical_anchors=("SZ_LEHR_1972:BODY:U000001",),
            epistemic_class="SOURCE_ESTABLISHED_TRIGGER",
            assertion_mode="LIMITATION",
            source_strength_note="Source limitation retained.",
            claim="A negative root direction does not by itself license repression.",
            trigger_kind="LIMITATION_GUARD",
            required_facts=(Predicate("RootDirectionEvidence", "negative"),),
            anti_inferences=("DO_NOT_INFER_REPRESSION_FROM_ROOT_NEGATIVE_ALONE",),
        )
        values.update(overrides)
        return ExecutableClaim(**values)

    def test_active_claim_preserves_provenance_and_guard(self):
        result = evaluate_claim(
            self.claim(),
            [FactRef("RootDirectionEvidence", "root-1", "negative")],
        )
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertIn("DR_SZ_LEHR_1972_000313", result.provenance_trace)
        self.assertEqual(
            result.anti_inferences,
            ("DO_NOT_INFER_REPRESSION_FROM_ROOT_NEGATIVE_ALONE",),
        )

    def test_nearest_negative_does_not_activate(self):
        result = evaluate_claim(
            self.claim(),
            [FactRef("RootDirectionEvidence", "root-1", "positive")],
        )
        self.assertEqual(result.activation_status, ActivationStatus.INACTIVE)

    def test_ambiguous_p1_fact_fails_closed(self):
        result = evaluate_claim(
            self.claim(),
            [FactRef("RootDirectionEvidence", "root-1", "negative", input_state=InputState.AMBIGUOUS)],
        )
        self.assertEqual(result.activation_status, ActivationStatus.UNRESOLVED_INPUT)

    def test_missing_required_fact_fails_closed(self):
        result = evaluate_claim(self.claim(), [])
        self.assertEqual(result.activation_status, ActivationStatus.UNRESOLVED_INPUT)
        self.assertEqual(result.missing_facts, ("RootDirectionEvidence",))

    def test_missing_context_blocks_locally(self):
        result = evaluate_claim(
            self.claim(context_requirements=("profile_kind",)),
            [FactRef("RootDirectionEvidence", "root-1", "negative")],
        )
        self.assertEqual(result.activation_status, ActivationStatus.BLOCKED_CONTEXT)
        self.assertEqual(result.missing_context, ("profile_kind",))

    def test_claim_without_doctrine_is_rejected(self):
        with self.assertRaises(ValueError):
            self.claim(doctrine_ids=())


if __name__ == "__main__":
    unittest.main()
