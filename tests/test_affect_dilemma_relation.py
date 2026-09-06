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


def _profile(*, sch=("0", "0"), pzone=("0", "0"), quantum_overrides=None):
    quantum_overrides = quantum_overrides or {}
    symbols = {
        "e": pzone[0],
        "hy": pzone[1],
        "k": sch[0],
        "p": sch[1],
    }
    return build_profile(
        _reaction(factor, symbols.get(factor, "0"), quantum_overrides.get(factor, 0))
        for factor in FACTORS
    )


def _findings(profile):
    result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
    return {item.claim_id: item for item in result.profiles[0].interpretation.findings}


class AffectDilemmaRelationTests(unittest.TestCase):
    def test_e_ambivalent_or_hy_ambivalent_activates_for_each_authorized_sch(self):
        sch_signatures = (("0", "0"), ("±", "0"), ("+", "0"), ("-", "0"), ("0", "+"))
        p_signatures = (("±", "+"), ("-", "±"), ("±", "±"))
        for sch in sch_signatures:
            for pzone in p_signatures:
                with self.subTest(sch=sch, pzone=pzone):
                    finding = _findings(_profile(sch=sch, pzone=pzone))["IC_SZONDI_PRIMARY_000086"]
                    self.assertIs(finding.assertion_mode, AssertionMode.PROBABLE)
                    self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000055",))
                    self.assertIn("oft", finding.source_strength_note)
                    self.assertIn("AI_SZONDI_000086", finding.anti_inference_ids)

    def test_disjunction_does_not_require_double_ambivalence(self):
        self.assertIn(
            "IC_SZONDI_PRIMARY_000086",
            _findings(_profile(sch=("+", "0"), pzone=("±", "0"))),
        )
        self.assertIn(
            "IC_SZONDI_PRIMARY_000086",
            _findings(_profile(sch=("+", "0"), pzone=("0", "±"))),
        )

    def test_unrelated_p_signature_or_sch_does_not_activate(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000086",
            _findings(_profile(sch=("+", "0"), pzone=("+", "-"))),
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000086",
            _findings(_profile(sch=("-", "+"), pzone=("±", "0"))),
        )

    def test_quantum_overpressure_is_not_silently_generalized(self):
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000086",
            _findings(
                _profile(
                    sch=("0", "+"),
                    pzone=("±", "0"),
                    quantum_overrides={"e": 1},
                )
            ),
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000086",
            _findings(
                _profile(
                    sch=("0", "+"),
                    pzone=("0", "±"),
                    quantum_overrides={"p": 1},
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()
