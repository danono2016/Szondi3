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


class AffectContactRelationTests(unittest.TestCase):
    def test_kain_greatest_protection_activates_only_at_ordinary_sch_plus_ambivalent(self):
        finding = _findings(_profile(sch=("+", "±")))["IC_SZONDI_PRIMARY_000075"]
        self.assertIs(finding.assertion_mode, AssertionMode.CATEGORICAL)
        self.assertIn("Kain-Gefahr", finding.statement)
        self.assertIn("mit größtem Erfolg", finding.source_strength_note)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000056",))
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000075",
            _findings(_profile(sch=("+", "±"), quantum_overrides={"p": 1})),
        )

    def test_kain_least_protection_activates_for_introprojection_and_flight(self):
        for sch in (("+", "-"), ("±", "-")):
            with self.subTest(sch=sch):
                finding = _findings(_profile(sch=sch))["IC_SZONDI_PRIMARY_000076"]
                self.assertIs(finding.assertion_mode, AssertionMode.CATEGORICAL)
                self.assertIn("Tötungsansprüchen Kains", finding.statement)
                self.assertIn("AI_SZONDI_000076", finding.anti_inference_ids)
        self.assertNotIn("IC_SZONDI_PRIMARY_000076", _findings(_profile(sch=("-", "-"))))

    def test_abel_frequency_relation_preserves_am_haeufigsten(self):
        for sch in (("0", "±"), ("-", "±")):
            with self.subTest(sch=sch):
                finding = _findings(_profile(sch=sch))["IC_SZONDI_PRIMARY_000077"]
                self.assertIs(finding.assertion_mode, AssertionMode.PROBABLE)
                self.assertIn("Abels", finding.statement)
                self.assertIn("am häufigsten", finding.source_strength_note)
        self.assertNotIn("IC_SZONDI_PRIMARY_000077", _findings(_profile(sch=("-", "-"))))

    def test_contact_barrier_relation_requires_exact_c_and_sch(self):
        for sch in (("0", "+"), ("+", "+")):
            with self.subTest(sch=sch):
                finding = _findings(_profile(c=("-", "-"), sch=sch))["IC_SZONDI_PRIMARY_000078"]
                self.assertIs(finding.assertion_mode, AssertionMode.PROBABLE)
                self.assertIn("Kontaktsperre", finding.statement)
                self.assertIn("narzißtische Formen des Ich-Schutzes", finding.statement)
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000078",
            _findings(_profile(c=("0", "0"), sch=("0", "+"))),
        )
        self.assertNotIn(
            "IC_SZONDI_PRIMARY_000078",
            _findings(_profile(c=("-", "-"), sch=("0", "+"), quantum_overrides={"m": 1})),
        )

    def test_anxiety_claim_now_uses_dedicated_affect_doctrine(self):
        finding = _findings(_profile(sch=("±", "+")))["IC_SZONDI_PRIMARY_000071"]
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000054",))


if __name__ == "__main__":
    unittest.main()
