import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}
_SCH_PLUS_AMBIVALENT_CLAIMS = {
    "IC_SZONDI_PRIMARY_000013",
    "IC_SZONDI_PRIMARY_000063",
    "IC_SZONDI_PRIMARY_000075",
    "IC_SZONDI_PRIMARY_000081",
}


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


def _profile(k_symbol: str, p_symbol: str):
    symbols = ("0", "0", "0", "0", k_symbol, p_symbol, "0", "0")
    return build_profile(
        _reaction(factor, symbol)
        for factor, symbol in zip(_FACTORS, symbols)
    )


def _active_claim_ids(k_symbol: str, p_symbol: str) -> set[str]:
    result = evaluate_clinical_protocol(
        ProfileSeries((_profile(k_symbol, p_symbol),)),
        production=True,
    )
    return {
        finding.claim_id
        for finding in result.profiles[0].interpretation.findings
    }


class AnnahmeQuantumBoundaryTests(unittest.TestCase):
    def test_ordinary_sch_plus_ambivalent_coactivates_all_four_distinct_claims(self):
        active = _active_claim_ids("+", "±")
        self.assertTrue(_SCH_PLUS_AMBIVALENT_CLAIMS <= active)

    def test_000013_does_not_activate_for_k_overpressure(self):
        for quantum in (1, 2, 3):
            with self.subTest(quantum=quantum):
                active = _active_claim_ids("+" + "!" * quantum, "±")
                self.assertNotIn("IC_SZONDI_PRIMARY_000013", active)
                self.assertTrue(_SCH_PLUS_AMBIVALENT_CLAIMS.isdisjoint(active))

    def test_000013_does_not_activate_for_p_overpressure(self):
        for quantum in (1, 2, 3):
            with self.subTest(quantum=quantum):
                active = _active_claim_ids("+", "±" + "!" * quantum)
                self.assertNotIn("IC_SZONDI_PRIMARY_000013", active)
                self.assertTrue(_SCH_PLUS_AMBIVALENT_CLAIMS.isdisjoint(active))


if __name__ == "__main__":
    unittest.main()
