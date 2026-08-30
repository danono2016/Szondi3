import unittest

from szondi3.formula import (
    formula_partition_candidates,
    formula_role_consensus,
    unique_formula_partition,
)
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


def _fall40_series() -> ProfileSeries:
    return ProfileSeries(
        (
            _profile("+!", "0", "0", "-", "-", "±", "+", "-"),
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


class FormulaRoleConsensusTests(unittest.TestCase):
    def test_fall40_keeps_complete_formula_unresolved_but_exposes_only_invariant_roles(self):
        series = _fall40_series()
        candidates = formula_partition_candidates(series)
        self.assertEqual(len(candidates), 2)
        self.assertTrue(
            all(len(item.symptomatic.factors) in (2, 3) for item in candidates)
        )

        with self.assertRaisesRegex(ValueError, "permits multiple partitions"):
            unique_formula_partition(series)

        consensus = formula_role_consensus(series)
        self.assertEqual(consensus.candidate_count, 2)
        self.assertEqual(consensus.symptomatic_factors, ("s", "p"))
        self.assertEqual(consensus.submanifest_factors, ("e", "hy"))
        self.assertEqual(consensus.root_factors, ("h", "d", "m"))
        self.assertEqual(consensus.variable_factors, ("k",))

    def test_consensus_never_selects_a_variable_factor_role(self):
        consensus = formula_role_consensus(_fall40_series())
        stable = set(
            consensus.symptomatic_factors
            + consensus.submanifest_factors
            + consensus.root_factors
        )
        self.assertTrue(stable.isdisjoint(consensus.variable_factors))
        self.assertEqual(
            stable | set(consensus.variable_factors),
            set(_FACTORS),
        )


if __name__ == "__main__":
    unittest.main()
