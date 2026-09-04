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


def _profile(*, sch=("0", "0"), c=("0", "0"), quantum_overrides=None):
    quantum_overrides = quantum_overrides or {}
    symbols = {"k": sch[0], "p": sch[1], "d": c[0], "m": c[1]}
    return build_profile(
        _reaction(factor, symbols.get(factor, "0"), quantum_overrides.get(factor, 0))
        for factor in FACTORS
    )


def _findings(profile):
    result = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
    return {item.claim_id: item for item in result.profiles[0].interpretation.findings}


class ContactParticipationRelationTests(unittest.TestCase):
    def test_c00_integration_special_case_requires_exact_ordinary_conjunction(self):
        finding = _findings(_profile(c=("0", "0"), sch=("±", "±")))[
            "IC_SZONDI_PRIMARY_000082"
        ]
        self.assertIs(finding.assertion_mode, AssertionMode.CATEGORICAL)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000059",))
        self.assertIn("idee spirituală", finding.statement)
        self.assertIn("Kontaktlosigkeit", finding.source_strength_note)
        self.assertIn("AI_SZONDI_000082", finding.anti_inference_ids)

        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000082",
            _findings(_profile(c=("0", "+"), sch=("±", "±"))),
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000082",
            _findings(
                _profile(
                    c=("0", "0"),
                    sch=("±", "±"),
                    quantum_overrides={"p": 1},
                )
            ),
        )

    def test_c00_abandonment_introjection_special_case_preserves_source_terms(self):
        finding = _findings(_profile(c=("0", "0"), sch=("+", "±")))[
            "IC_SZONDI_PRIMARY_000083"
        ]
        self.assertIs(finding.assertion_mode, AssertionMode.CATEGORICAL)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000059",))
        self.assertIn("mamei care părăsește", finding.statement)
        self.assertIn("blind, skotomisiert", finding.statement)
        self.assertIn("AI_SZONDI_000083", finding.anti_inference_ids)

        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000083",
            _findings(_profile(c=("0", "0"), sch=("+", "+"))),
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000083",
            _findings(
                _profile(
                    c=("0", "0"),
                    sch=("+", "±"),
                    quantum_overrides={"d": 1},
                )
            ),
        )

    def test_problematic_interpersonal_relation_claim_excludes_partial_sch_double_plus(self):
        for sch in (("0", "0"), ("+", "0"), ("+", "-")):
            for c in (("±", "0"), ("±", "+"), ("±", "-"), ("-", "±"), ("±", "±")):
                with self.subTest(sch=sch, c=c):
                    finding = _findings(_profile(c=c, sch=sch))[
                        "IC_SZONDI_PRIMARY_000084"
                    ]
                    self.assertIs(finding.assertion_mode, AssertionMode.CATEGORICAL)
                    self.assertEqual(
                        finding.doctrine_ids,
                        ("DR_SZ_IA_1956_B_000060",),
                    )
                    self.assertIn("stets unsicher, problematisch", finding.statement)
                    self.assertIn("teils auch", finding.source_strength_note)
                    self.assertIn("AI_SZONDI_000084", finding.anti_inference_ids)

        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000084",
            _findings(_profile(c=("±", "0"), sch=("+", "+"))),
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000084",
            _findings(_profile(c=("0", "0"), sch=("+", "0"))),
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000084",
            _findings(
                _profile(
                    c=("±", "0"),
                    sch=("+", "0"),
                    quantum_overrides={"k": 1},
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()
