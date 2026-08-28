"""Adapters from deterministic Szondi3 objects to explicit P2B facts.

These functions only expose values already present in P1 outputs. They do not
perform scoring, choose among ambiguous P1 candidates, or add clinical meaning.
"""

from __future__ import annotations

from typing import Iterable

from .interpretation import Fact, InputState
from .linnaeus import RootDirectionEvidence
from .profile import DriveProfile
from .proportions import DurMollIndex, SocialIndex
from .series import SeriesIndices


_BASE_SYMBOL_BY_KIND = {
    "null": "0",
    "positive": "+",
    "negative": "-",
    "ambivalent": "±",
}


def profile_facts(profile: DriveProfile, *, scope: str = "foreground_profile") -> tuple[Fact, ...]:
    """Expose base factor/vector reactions while keeping quantum level separate."""
    result: list[Fact] = []
    by_factor = {reaction.factor: reaction for reaction in profile.factors}
    for factor, reaction in by_factor.items():
        if reaction.forced_null:
            base_state = InputState.UNDEFINED
        else:
            base_state = InputState.AVAILABLE
        base_symbol = _BASE_SYMBOL_BY_KIND.get(reaction.kind)
        if base_symbol is None:
            base_state = InputState.UNDEFINED
        result.extend(
            (
                Fact(
                    key=f"profile.factor.{factor}.base_symbol",
                    value=base_symbol,
                    scope=scope,
                    input_state=base_state,
                    fact_id=f"{scope}:factor:{factor}:base_symbol",
                ),
                Fact(
                    key=f"profile.factor.{factor}.quantum_level",
                    value=reaction.quantum_level,
                    scope=scope,
                    fact_id=f"{scope}:factor:{factor}:quantum_level",
                ),
            )
        )

    for vector in profile.vectors:
        first, second = vector.factors
        first_reaction = by_factor[first]
        second_reaction = by_factor[second]
        state = (
            InputState.AVAILABLE
            if not first_reaction.forced_null and not second_reaction.forced_null
            else InputState.UNDEFINED
        )
        result.append(
            Fact(
                key=f"profile.vector.{vector.name}.base_symbols",
                value=(
                    _BASE_SYMBOL_BY_KIND.get(first_reaction.kind),
                    _BASE_SYMBOL_BY_KIND.get(second_reaction.kind),
                ),
                scope=scope,
                input_state=state,
                fact_id=f"{scope}:vector:{vector.name}:base_symbols",
            )
        )
    return tuple(result)


def series_index_facts(
    indices: SeriesIndices, *, scope: str = "profile_series"
) -> tuple[Fact, ...]:
    """Expose already-computed series indices, preserving undefined TspQu."""
    tspqu_state = (
        InputState.AVAILABLE
        if indices.tendenzspannungsquotient is not None
        else InputState.UNDEFINED
    )
    return (
        Fact(
            key="series.indices.available",
            value=True,
            scope=scope,
            fact_id=f"{scope}:indices",
        ),
        Fact(
            key="series.tspqu",
            value=indices.tendenzspannungsquotient,
            scope=scope,
            input_state=tspqu_state,
            fact_id=f"{scope}:tspqu",
        ),
        Fact(
            key="series.symptom_percentage",
            value=indices.symptom_percentage,
            scope=scope,
            fact_id=f"{scope}:symptom_percentage",
        ),
    )


def dur_moll_facts(index: DurMollIndex, *, scope: str = "profile_series") -> tuple[Fact, ...]:
    return (
        Fact(
            key="dur_moll.index.available",
            value=True,
            scope=scope,
            fact_id=f"{scope}:dur_moll",
        ),
        Fact(
            key="dur_moll.dur_percentage",
            value=index.dur_percentage,
            scope=scope,
            fact_id=f"{scope}:dur_moll:dur_percentage",
        ),
        Fact(
            key="dur_moll.moll_percentage",
            value=index.moll_percentage,
            scope=scope,
            fact_id=f"{scope}:dur_moll:moll_percentage",
        ),
    )


def social_index_facts(index: SocialIndex, *, scope: str = "profile_series") -> tuple[Fact, ...]:
    return (
        Fact(
            key="social_index.available",
            value=True,
            scope=scope,
            fact_id=f"{scope}:social_index",
        ),
        Fact(
            key="social_index.positive_percentage",
            value=index.positive_percentage,
            scope=scope,
            fact_id=f"{scope}:social_index:positive_percentage",
        ),
        Fact(
            key="social_index.negative_percentage",
            value=index.negative_percentage,
            scope=scope,
            fact_id=f"{scope}:social_index:negative_percentage",
        ),
    )


def root_direction_facts(
    evidence: Iterable[RootDirectionEvidence], *, scope: str = "profile_series"
) -> tuple[Fact, ...]:
    """Expose strict directional roots without inventing a majority rule."""
    items = tuple(evidence)
    strict_positive: list[str] = []
    strict_negative: list[str] = []
    ambiguous: list[str] = []
    undefined: list[str] = []
    for item in items:
        if item.positive_reactions and not item.negative_reactions:
            strict_positive.append(item.root_factor)
        elif item.negative_reactions and not item.positive_reactions:
            strict_negative.append(item.root_factor)
        elif item.positive_reactions and item.negative_reactions:
            ambiguous.append(item.root_factor)
        else:
            undefined.append(item.root_factor)

    return (
        Fact(
            key="linnaeus.strict_positive_roots",
            value=tuple(strict_positive),
            scope=scope,
            fact_id=f"{scope}:strict_positive_roots",
        ),
        Fact(
            key="linnaeus.strict_negative_roots",
            value=tuple(strict_negative),
            scope=scope,
            fact_id=f"{scope}:strict_negative_roots",
        ),
        Fact(
            key="linnaeus.ambiguous_root_directions",
            value=tuple(ambiguous),
            scope=scope,
            fact_id=f"{scope}:ambiguous_root_directions",
        ),
        Fact(
            key="linnaeus.undefined_root_directions",
            value=tuple(undefined),
            scope=scope,
            fact_id=f"{scope}:undefined_root_directions",
        ),
    )
