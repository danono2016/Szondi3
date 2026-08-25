"""Formal Triebprofil structure.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972): S(h,s), P(e,hy), Sch(k,p), C(d,m).

This module only groups already-calculated factor reactions. It assigns no
clinical or doctrinal meaning to a vector configuration.
"""

from dataclasses import dataclass
from typing import Iterable

from .scoring import FactorReaction
from .stimuli import FACTORS

VECTOR_FACTORS = (
    ("S", ("h", "s")),
    ("P", ("e", "hy")),
    ("Sch", ("k", "p")),
    ("C", ("d", "m")),
)


@dataclass(frozen=True, slots=True)
class VectorReaction:
    name: str
    factors: tuple[str, str]
    symbols: tuple[str, str]


@dataclass(frozen=True, slots=True)
class DriveProfile:
    factors: tuple[FactorReaction, ...]
    vectors: tuple[VectorReaction, ...]


def build_profile(reactions: Iterable[FactorReaction]) -> DriveProfile:
    """Build the four-vector formal profile from exactly eight factor reactions."""
    supplied = tuple(reactions)
    by_factor = {reaction.factor: reaction for reaction in supplied}
    if len(supplied) != len(FACTORS) or set(by_factor) != set(FACTORS):
        raise ValueError("A drive profile requires exactly one reaction for each of the eight factors")

    ordered_factors = tuple(by_factor[factor] for factor in FACTORS)
    vectors = tuple(
        VectorReaction(
            name=name,
            factors=factors,
            symbols=(by_factor[factors[0]].symbol, by_factor[factors[1]].symbol),
        )
        for name, factors in VECTOR_FACTORS
    )
    return DriveProfile(factors=ordered_factors, vectors=vectors)
