import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import AssertionMode
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, symbol="0", quantum=0):
    kind = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}[symbol]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=symbol + ("!" * quantum),
        quantum_level=quantum,
    )


def _profile(sch_vector, quantum_overrides=None):
    quantum_overrides = quantum_overrides or {}
    symbols = {"k": sch_vector[0], "p": sch_vector[1]}
    return build_profile(
        _reaction(
            factor,
            symbols.get(factor, "0"),
            quantum_overrides.get(factor, 0),
        )
        for factor in FACTORS
    )


class AffectAnxietyDefenseRelationTests(unittest.TestCase):
    def _findings(self, profile):
        result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
        return {item.claim_id: item for item in result.profiles[0].interpretation.findings}

    def test_four_source_defined_sch_positions_activate_frequency_relation(self):
        for sch_vector in (("±", "+"), ("-", "0"), ("±", "±"), ("±", "-")):
            with self.subTest(sch_vector=sch_vector):
                findings = self._findings(_profile(sch_vector))
                self.assertIn("IC_SZONDI_PRIMARY_000071", findings)
                self.assertIs(
                    findings["IC_SZONDI_PRIMARY_000071"].assertion_mode,
                    AssertionMode.PROBABLE,
                )

    def test_other_sch_position_does_not_activate_relation(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000071",
            self._findings(_profile(("0", "+"))),
        )

    def test_quantum_overpressure_is_not_silently_extended(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000071",
            self._findings(_profile(("±", "+"), quantum_overrides={"p": 1})),
        )

    def test_source_frequency_qualifier_is_preserved(self):
        finding = self._findings(_profile(("±", "+")))["IC_SZONDI_PRIMARY_000071"]
        self.assertIn("am häufigsten", finding.source_strength_note)
        self.assertIn("Angstzustände", finding.statement)
        self.assertIn("AI_SZONDI_000071", finding.anti_inference_ids)

    def test_annahme_preserves_the_source_comparison_as_probable(self):
        finding = self._findings(_profile(("+", "±")))["IC_SZONDI_PRIMARY_000081"]
        self.assertIs(finding.assertion_mode, AssertionMode.PROBABLE)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000053",))
        self.assertIn("scheinen", finding.source_strength_note)
        self.assertIn("Angst is rarer", finding.source_strength_note)
        self.assertIn("Sch ±+", finding.statement)
        self.assertIn("AI_SZONDI_000081", finding.anti_inference_ids)

    def test_annahme_comparison_does_not_fire_for_the_four_comparison_positions(self):
        for sch_vector in (("±", "+"), ("-", "0"), ("±", "±"), ("±", "-")):
            with self.subTest(sch_vector=sch_vector):
                self.assertNotIn(
                    "IC_SZONDI_PRIMARY_000081",
                    self._findings(_profile(sch_vector)),
                )

    def test_annahme_comparison_does_not_extend_to_overpressure(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000081",
            self._findings(_profile(("+", "±"), quantum_overrides={"p": 1})),
        )


if __name__ == "__main__":
    unittest.main()
