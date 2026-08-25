"""Deterministic factor counts and formal Wahlreaktionen.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 50-62, especially Tabelle 3.

This is formal test calculation only. The psychological meanings attached to the
reactions belong to later doctrine/interpretation layers and are not implemented here.
"""

from dataclasses import dataclass
from typing import Literal

from .administration import ComplementProtocol, ForegroundProtocol
from .stimuli import FACTORS, catalog

ReactionKind = Literal["null", "positive", "negative", "ambivalent"]


@dataclass(frozen=True, slots=True)
class Reaction:
    sympathetic: int
    unsympathetic: int
    kind: ReactionKind
    symbol: str
    quantum_level: int


@dataclass(frozen=True, slots=True)
class FactorReaction:
    factor: str
    sympathetic: int
    unsympathetic: int
    kind: ReactionKind
    symbol: str
    quantum_level: int
    forced_null: bool = False


_CARD_FACTOR = {card.card_id: card.factor for card in catalog()}


def reaction_from_counts(sympathetic: int, unsympathetic: int) -> Reaction:
    """Classify one factor's 0..6 choices exactly as Lehrbuch Tabelle 3."""
    if not isinstance(sympathetic, int) or not isinstance(unsympathetic, int):
        raise ValueError("Factor counts must be integers")
    if sympathetic < 0 or unsympathetic < 0:
        raise ValueError("Factor counts cannot be negative")
    if sympathetic + unsympathetic > 6:
        raise ValueError("A factor has only six photographs")

    if sympathetic <= 1 and unsympathetic <= 1:
        return Reaction(sympathetic, unsympathetic, "null", "0", 0)

    if sympathetic >= 2 and unsympathetic <= 1:
        quantum = max(0, sympathetic - 3)
        return Reaction(sympathetic, unsympathetic, "positive", "+" + ("!" * quantum), quantum)

    if unsympathetic >= 2 and sympathetic <= 1:
        quantum = max(0, unsympathetic - 3)
        return Reaction(sympathetic, unsympathetic, "negative", "-" + ("!" * quantum), quantum)

    quantum = 1 if max(sympathetic, unsympathetic) == 4 else 0
    return Reaction(sympathetic, unsympathetic, "ambivalent", "±" + ("!" * quantum), quantum)


def _count_factors(card_ids: tuple[str, ...]) -> dict[str, int]:
    counts = {factor: 0 for factor in FACTORS}
    for card_id in card_ids:
        try:
            factor = _CARD_FACTOR[card_id]
        except KeyError as exc:
            raise ValueError(f"Unknown card id in protocol: {card_id}") from exc
        counts[factor] += 1
    return counts


def _factor_reaction(factor: str, sympathetic: int, unsympathetic: int, forced_null: bool = False) -> FactorReaction:
    reaction = reaction_from_counts(sympathetic, unsympathetic)
    if forced_null and reaction.kind != "null":
        raise ValueError("Only a null reaction can be marked as numerically forced")
    return FactorReaction(
        factor=factor,
        sympathetic=reaction.sympathetic,
        unsympathetic=reaction.unsympathetic,
        kind=reaction.kind,
        symbol="ø" if forced_null else reaction.symbol,
        quantum_level=reaction.quantum_level,
        forced_null=forced_null,
    )


def factor_reactions(protocol: ForegroundProtocol) -> tuple[FactorReaction, ...]:
    """Count foreground choices by factor and return the eight formal reactions."""
    positive = _count_factors(protocol.sympathetic)
    negative = _count_factors(protocol.unsympathetic)
    return tuple(
        _factor_reaction(factor, positive[factor], negative[factor])
        for factor in FACTORS
    )


def complement_factor_reactions(
    foreground: ForegroundProtocol,
    complement: ComplementProtocol,
) -> tuple[FactorReaction, ...]:
    """Calculate EKP reactions and identify source-defined Zwangs-Nullreaktionen.

    EKP uses the same reaction table as VGP. A null reaction is numerically forced
    when five or six photographs of that factor were already chosen in VGP, leaving
    only one or zero photographs available for the complement choice. Szondi's
    protocol notation for this forced null is the crossed zero ``ø``.
    """
    positive = _count_factors(complement.relative_sympathetic)
    negative = _count_factors(complement.relative_unsympathetic)
    foreground_positive = _count_factors(foreground.sympathetic)
    foreground_negative = _count_factors(foreground.unsympathetic)

    result = []
    for factor in FACTORS:
        reaction = reaction_from_counts(positive[factor], negative[factor])
        foreground_total = foreground_positive[factor] + foreground_negative[factor]
        forced_null = reaction.kind == "null" and foreground_total >= 5
        result.append(
            _factor_reaction(
                factor,
                positive[factor],
                negative[factor],
                forced_null=forced_null,
            )
        )
    return tuple(result)
