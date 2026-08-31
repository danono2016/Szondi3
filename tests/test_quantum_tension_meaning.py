import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, *, kind="null", quantum=0):
    base = {
        "null": "0",
        "positive": "+",
        "negative": "-",
        "ambivalent": "±",
    }[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=base + ("!" * quantum),
        quantum_level=quantum,
    )


def _profile(*, quantum_factor=None):
    return build_profile(
        _reaction(
            factor,
            kind="positive" if factor == quantum_factor else "null",
            quantum=1 if factor == quantum_factor else 0,
        )
        for factor in FACTORS
    )


class QuantumTensionMeaningTests(unittest.TestCase):
    def test_quantum_mark_exposes_factor_and_emits_source_linked_meaning(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile(quantum_factor="h"),)),
            production=True,
        )

        profile_result = result.profiles[0]
        quantum_fact = next(
            fact
            for fact in profile_result.facts
            if fact.key == "profile.quantum_tension_factors"
        )
        self.assertEqual(quantum_fact.value, ("h",))

        finding = next(
            item
            for item in profile_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000034"
        )
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_LEHR_1972_000344",))
        self.assertEqual(finding.source_ids, ("SZ_LEHR_1972",))
        self.assertEqual(
            finding.support_fact_ids,
            ("foreground_profile_1:quantum_tension_factors",),
        )
        self.assertIn("Bedürfnisspannung actuală crescută", finding.statement)
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000034",))
        self.assertIn("severitate psihopatologică", finding.anti_inferences[0])
        self.assertIn("profilului actual", finding.anti_inferences[0])

    def test_profile_without_quantum_marks_does_not_emit_quantum_tension_claim(self):
        result = evaluate_clinical_protocol(ProfileSeries((_profile(),)))

        quantum_fact = next(
            fact
            for fact in result.profiles[0].facts
            if fact.key == "profile.quantum_tension_factors"
        )
        self.assertEqual(quantum_fact.value, ())

        claim_ids = {
            item.claim_id for item in result.profiles[0].interpretation.findings
        }
        unresolved_ids = {
            item.claim_id for item in result.profiles[0].interpretation.unresolved
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000034", claim_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000034", unresolved_ids)


if __name__ == "__main__":
    unittest.main()
