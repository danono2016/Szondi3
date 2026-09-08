import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
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


class PersonaFormationTypologyTests(unittest.TestCase):
    def _findings(self, profile):
        result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
        return {item.claim_id: item for item in result.profiles[0].interpretation.findings}

    def test_introprojection_persona_route_is_exact_sch_plus_minus(self):
        findings = self._findings(_profile(("+", "-")))
        finding = findings["IC_SZONDI_PRIMARY_000072"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000027",))
        self.assertIn("Personabildung", finding.statement)
        self.assertIn("Introprojektion", finding.statement)
        self.assertNotIn("IC_SZONDI_PRIMARY_000073", findings)

    def test_collective_introinflation_persona_route_is_exact_sch_plus_plus(self):
        findings = self._findings(_profile(("+", "+")))
        finding = findings["IC_SZONDI_PRIMARY_000073"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000027",))
        self.assertIn("kollektive Introinflation", finding.statement)
        self.assertIn("Allessein", finding.statement)
        self.assertIn("IC_SZONDI_PRIMARY_000073", findings)
        self.assertNotIn("IC_SZONDI_PRIMARY_000072", findings)

    def test_other_sch_position_activates_neither_persona_route(self):
        findings = self._findings(_profile(("0", "+")))
        self.assertNotIn("IC_SZONDI_PRIMARY_000072", findings)
        self.assertNotIn("IC_SZONDI_PRIMARY_000073", findings)

    def test_quantum_overpressure_is_not_silently_extended(self):
        findings = self._findings(_profile(("+", "+"), quantum_overrides={"p": 1}))
        self.assertNotIn("IC_SZONDI_PRIMARY_000073", findings)

    def test_deflation_success_is_not_inferred_from_sch_plus_plus(self):
        finding = self._findings(_profile(("+", "+")))["IC_SZONDI_PRIMARY_000073"]
        self.assertIn("nu rezultă că această Deflation a reușit", finding.statement)
        self.assertIn("AI_SZONDI_000073", finding.anti_inference_ids)


if __name__ == "__main__":
    unittest.main()
