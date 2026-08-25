"""Deterministic factor counts and formal Wahlreaktionen.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 50-61, especially Tabelle 3.

This is formal test calculation only. The psychological meanings attached to the
reactions belong to later doctrine/interpretation layers and are not implemented here.
"""

from dataclasses import dataclass
from typing import Literal

from .administration import ForegroundProtocol
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
        return Reaction(
            sympathetic,
            unsympathetic,
            "positive",
            "+" + ("!" * quantum),
            quantum,
        )

    if unsympathetic >= 2 and sympathetic <= 1:
        quantum = max(0, unsympathetic - 3)
        return Reaction(
            sympathetic,
            unsympathetic,
            "negative",
            "-" + ("!" * quantum),
            quantum,
        )

    # With six photographs total, both directions >=2 leaves exactly the six
    # ambivalent combinations in Tabelle 3. A 4:2 split is the ambivalent
    # Vollreaktion with one Quantumspannung mark.
    quantum = 1 if max(sympathetic, unsympathetic) == 4 else 0
    return Reaction(
        sympathetic,
        unsympathetic,
        "ambivalent",
        "±" + ("!" * quantum),
        quantum,
    )


def _count_factors(card_ids: tuple[str, ...]) -> dict[str, int]:
    counts = {factor: 0 for factor in FACTORS}
    for card_id in card_ids:
        try:
            factor = _CARD_FACTOR[card_id]
        except KeyError as exc:
            raise ValueError(f"Unknown card id in protocol: {card_id}") from exc
        counts[factor] += 1
    return counts


def factor_reactions(protocol: ForegroundProtocol) -> tuple[FactorReaction, ...]:
    """Count foreground choices by factor and return the eight formal reactions."""
    positive = _count_factors(protocol.sympathetic)
    negative = _count_factors(protocol.unsympathetic)

    result = []
    for factor in FACTORS:
        reaction = reaction_from_counts(positive[factor], negative[factor])
        result.append(
            FactorReaction(
                factor=factor,
                sympathetic=reaction.sympathetic,
                unsympathetic=reaction.unsympathetic,
                kind=reaction.kind,
                symbol=reaction.symbol,
                quantum_level=reaction.quantum_level,
            )
        )
    return tuple(result)
