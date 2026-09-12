import unittest

from szondi3.clinical_facts import profile_facts
from szondi3.interpretation import ActivationStatus, evaluate_claim
from szondi3.interpretation_catalogue import CLAIMS_BY_ID
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
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


def _profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        _reaction(factor, overrides.get(factor, "0"))
        for factor in FACTORS
    )


class SexualVectorQuantumBoundaryTests(unittest.TestCase):
    def test_000017_intentionally_uses_base_symbols_only(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000017"]

        self.assertEqual(
            tuple(predicate.fact_key for predicate in claim.trigger.predicates),
            ("profile.vector.S.base_symbols",),
        )

        for h_symbol in ("+!", "+!!", "+!!!"):
            with self.subTest(h=h_symbol):
                activation = evaluate_claim(
                    claim,
                    profile_facts(_profile({"h": h_symbol, "s": "0"})),
                )
                self.assertEqual(activation.activation_status, ActivationStatus.ACTIVE)
                self.assertEqual(
                    tuple(fact.key for fact in activation.matched_facts),
                    ("profile.vector.S.base_symbols",),
                )
                self.assertEqual(activation.matched_facts[0].value, ("+", "0"))

        self.assertNotIn("preregenitale", claim.claim)
        self.assertNotIn("homosexual", claim.claim.lower())
        guard = claim.anti_inferences[0].prohibited_conclusion
        self.assertIn("preregenitale", guard)
        self.assertIn("quantum-aware", guard)

    def test_000018_intentionally_preserves_base_core_with_h_or_s_overpressure(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000018"]

        self.assertEqual(
            tuple(predicate.fact_key for predicate in claim.trigger.predicates),
            ("profile.vector.S.base_symbols",),
        )

        for h_symbol, s_symbol in (("+!", "-"), ("+", "-!"), ("+!!", "-"), ("+", "-!!")):
            with self.subTest(h=h_symbol, s=s_symbol):
                activation = evaluate_claim(
                    claim,
                    profile_facts(_profile({"h": h_symbol, "s": s_symbol})),
                )
                self.assertEqual(activation.activation_status, ActivationStatus.ACTIVE)
                self.assertEqual(
                    tuple(fact.key for fact in activation.matched_facts),
                    ("profile.vector.S.base_symbols",),
                )
                self.assertEqual(activation.matched_facts[0].value, ("+", "-"))

        self.assertNotIn("Masochismus", claim.claim)
        self.assertNotIn("Triebzielinversion", claim.claim)
        guard = claim.anti_inferences[0].prohibited_conclusion
        self.assertIn("Masochismus", guard)
        self.assertIn("Überdruck", guard)


if __name__ == "__main__":
    unittest.main()
