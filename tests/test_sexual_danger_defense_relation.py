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


def _profile(s_vector, sch_vector, quantum_overrides=None):
    quantum_overrides = quantum_overrides or {}
    symbols = {
        "h": s_vector[0],
        "s": s_vector[1],
        "k": sch_vector[0],
        "p": sch_vector[1],
    }
    return build_profile(
        _reaction(
            factor,
            symbols.get(factor, "0"),
            quantum_overrides.get(factor, 0),
        )
        for factor in FACTORS
    )


class SexualDangerDefenseRelationTests(unittest.TestCase):
    def _claim_ids(self, profile):
        result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
        return {item.claim_id for item in result.profiles[0].interpretation.findings}

    def test_exact_source_defined_s_and_sch_pairs_activate_relation(self):
        sexual_danger_positions = (("+", "+"), ("0", "+"), ("+", "0"))
        defense_positions = (("-", "-"), ("-", "0"), ("-", "±"), ("±", "-"))

        for s_vector in sexual_danger_positions:
            for sch_vector in defense_positions:
                with self.subTest(s_vector=s_vector, sch_vector=sch_vector):
                    self.assertIn(
                        "IC_SZONDI_PRIMARY_000070",
                        self._claim_ids(_profile(s_vector, sch_vector)),
                    )

    def test_other_s_configuration_does_not_activate_relation(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000070",
            self._claim_ids(_profile(("-", "+"), ("-", "-"))),
        )

    def test_other_sch_configuration_does_not_activate_relation(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000070",
            self._claim_ids(_profile(("+", "+"), ("+", "+"))),
        )

    def test_quantum_overpressure_is_not_silently_extended(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000070",
            self._claim_ids(
                _profile(("+", "+"), ("-", "-"), quantum_overrides={"h": 1})
            ),
        )


if __name__ == "__main__":
    unittest.main()
