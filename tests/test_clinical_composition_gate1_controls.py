import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import AssertionMode
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
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


def _profile(**overrides):
    return build_profile(
        _reaction(factor, overrides.get(factor, "0"))
        for factor in FACTORS
    )


def _findings(profile):
    evaluation = evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
    return tuple(evaluation.profiles[0].interpretation.findings)


def _by_id(findings):
    return {item.claim_id: item for item in findings}


def _non_limitation(findings):
    return tuple(item for item in findings if item.assertion_mode is not AssertionMode.LIMITATION)


def _vector_domains(finding):
    domains = set()
    for fact_id in finding.support_fact_ids:
        for vector in ("S", "P", "Sch", "C"):
            if f":vector:{vector}:" in fact_id:
                domains.add(vector)
    return frozenset(domains)


class ClinicalCompositionGate1ControlTests(unittest.TestCase):
    """Materialize Gate-1 research controls from the production P2B runtime.

    These tests do not define a composition engine. They freeze three deliberately
    different evidence shapes so the report-composition hypothesis can be tested
    against real executable findings rather than hand-invented profiles.
    """

    def test_control_a_has_three_independent_vector_meanings_without_cross_vector_bridge(self):
        # S +0 | P 00 | Sch 00 | C +-
        # The three target meanings are source-authorized independently. For this
        # specimen no active non-limitation finding may bridge two of S / Sch / C.
        findings = _findings(
            _profile(h="+", s="0", e="0", hy="0", k="0", p="0", d="+", m="-")
        )
        index = _by_id(findings)

        self.assertIn("IC_SZONDI_PRIMARY_000017", index)  # S +0
        self.assertIn("IC_SZONDI_PRIMARY_000012", index)  # Sch 00
        self.assertIn("IC_SZONDI_PRIMARY_000020", index)  # C +-

        relevant_domains = frozenset({"S", "Sch", "C"})
        cross_bridges = tuple(
            item
            for item in _non_limitation(findings)
            if len(_vector_domains(item) & relevant_domains) > 1
        )
        self.assertEqual(cross_bridges, ())

    def test_control_b_contains_a_real_level_2_p_sch_bridge_with_source_modality(self):
        # S 00 | P ±0 | Sch +0 | C 00
        # This exact case is already covered by the 000086 production regression:
        # an ordinary P ethical dilemma signature is related by the source to an
        # ordinary Sch defense form with the explicit qualifier "oft".
        findings = _findings(_profile(e="±", hy="0", k="+", p="0"))
        finding = _by_id(findings)["IC_SZONDI_PRIMARY_000086"]

        self.assertIs(finding.assertion_mode, AssertionMode.PROBABLE)
        self.assertIn("oft", finding.source_strength_note)
        self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000055",))
        self.assertEqual(_vector_domains(finding), frozenset({"P", "Sch"}))
        self.assertIn("AI_SZONDI_000086", finding.anti_inference_ids)

    def test_control_c_preserves_exact_quantum_boundary_for_hard_historical_term(self):
        # S 0+!! | P 00 | Sch 00 | C 00
        # 000056 is an exact s+!! / e0 source contrast. Its historical term
        # Aggressionsgefahr must remain bounded by both factor symbols and quantum.
        findings = _findings(_profile(s="+!!", e="0"))
        finding = _by_id(findings)["IC_SZONDI_PRIMARY_000056"]

        self.assertIs(finding.assertion_mode, AssertionMode.CONDITIONAL)
        self.assertEqual(
            finding.doctrine_ids,
            ("DR_SZ_TRIEBPATH_1_000002", "DR_SZ_TRIEBPATH_1_000004"),
        )
        self.assertIn("Aggressionsgefahr", finding.statement)
        self.assertIn("AI_SZONDI_000056", finding.anti_inference_ids)
        self.assertEqual(
            finding.support_fact_ids,
            (
                "foreground_profile_1:factor:s:base_symbol",
                "foreground_profile_1:factor:s:quantum_level",
                "foreground_profile_1:factor:e:base_symbol",
                "foreground_profile_1:factor:e:quantum_level",
            ),
        )

        neighboring = _by_id(_findings(_profile(s="+!", e="0")))
        self.assertNotIn("IC_SZONDI_PRIMARY_000056", neighboring)


if __name__ == "__main__":
    unittest.main()
