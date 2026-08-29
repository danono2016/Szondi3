import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
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


def _profile(*symbols: str):
    return build_profile(
        _reaction(factor, symbol)
        for factor, symbol in zip(_FACTORS, symbols)
    )


def _fall40_series(*, first_h: str = "+!") -> ProfileSeries:
    return ProfileSeries(
        (
            _profile(first_h, "0", "0", "-", "-", "±", "+", "-"),
            _profile("+!", "0", "-", "-", "-", "+", "+", "-"),
            _profile("+", "0", "-", "-", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-"),
            _profile("+", "0", "0", "-", "+", "±", "+", "-!!"),
            _profile("+!", "0", "-", "-!", "+", "±", "+", "-!"),
            _profile("+!", "-", "-", "0", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "0", "±", "±", "+", "-!"),
        )
    )


class ShPlusSeriesClaimTests(unittest.TestCase):
    def test_fall40_p1_establishes_strict_sh_plus_subclass(self):
        result = evaluate_clinical_protocol(_fall40_series(), production=True)

        subclasses = result.series_result.calculation("strict_leading_subclasses")
        self.assertEqual(subclasses.state.value, "AVAILABLE")
        self.assertEqual(tuple(item.label for item in subclasses.value), ("Sh+",))
        self.assertEqual(subclasses.value[0].root_factor, "h")
        self.assertEqual(subclasses.value[0].evidence.positive_reactions, 10)
        self.assertEqual(subclasses.value[0].evidence.negative_reactions, 0)

    def test_fall40_sh_plus_claim_keeps_exact_support_and_anti_inference(self):
        result = evaluate_clinical_protocol(_fall40_series(), production=True)
        finding = next(
            item
            for item in result.series_result.interpretation.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000016"
        )

        self.assertEqual(
            finding.support_fact_ids,
            (
                "profile_series:profile_count",
                "profile_series:danger_leading_drive_classes",
                "profile_series:strict_positive_roots",
            ),
        )
        self.assertEqual(
            finding.doctrine_ids,
            (
                "DR_SZ_LEHR_1972_000323",
                "DR_SZ_LEHR_1972_000157",
                "DR_SZ_LEHR_1972_000171",
                "DR_SZ_LEHR_1972_000313",
            ),
        )
        self.assertEqual(finding.anti_inference_ids, ("AI_SZONDI_000016",))
        self.assertIn("Sh+", finding.statement)
        self.assertIn("Eros-/Liebes-/Bindungsbedürfnis", finding.statement)
        self.assertIn("nevoie nesatisfăcută", finding.statement)

        guard = finding.anti_inferences[0]
        self.assertIn("homosexualității/bisexualității", guard)
        self.assertIn("travestismului", guard)
        self.assertIn("pasivității", guard)
        self.assertIn("Überdruck", guard)
        self.assertIn("factorul s", guard)

    def test_mixed_h_direction_blocks_sh_plus_without_majority_repair(self):
        result = evaluate_clinical_protocol(
            _fall40_series(first_h="-"),
            production=True,
        )

        root_evidence = result.series_result.calculation(
            "leading_root_direction_evidence"
        ).value
        self.assertEqual(root_evidence[0].root_factor, "h")
        self.assertEqual(root_evidence[0].positive_reactions, 9)
        self.assertEqual(root_evidence[0].negative_reactions, 1)

        strict = result.series_result.calculation("strict_leading_subclasses")
        self.assertEqual(strict.state.value, "UNRESOLVED")

        active = {
            item.claim_id for item in result.series_result.interpretation.findings
        }
        self.assertNotIn("IC_SZONDI_PRIMARY_000016", active)

        facts = {item.key: item for item in result.series_result.facts}
        self.assertEqual(facts["linnaeus.strict_positive_roots"].value, ())
        self.assertEqual(facts["linnaeus.ambiguous_root_directions"].value, ("h",))


if __name__ == "__main__":
    unittest.main()
