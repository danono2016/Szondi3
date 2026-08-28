"""Deterministic whole-series morphology for clinical interpretation.

This layer counts what is actually present in a ProfileSeries.  It deliberately
assigns no psychological meaning.  The purpose is to prevent the generative
clinical layer from eyeballing frequencies or silently decomposing vector
configurations before the source-defined configuration has been made visible.
"""

from __future__ import annotations

from collections import Counter

from .interpretation import Fact, InputState
from .series import ProfileSeries
from .stimuli import FACTORS

_BASE_SYMBOL_BY_KIND = {
    "null": "0",
    "positive": "+",
    "negative": "-",
    "ambivalent": "±",
}
_TOKEN_BY_SYMBOL = {
    "+": "positive",
    "-": "negative",
    "0": "null",
    "±": "ambivalent",
}


def _base_symbol(reaction) -> str | None:
    if reaction.forced_null:
        return None
    return _BASE_SYMBOL_BY_KIND.get(reaction.kind)


def series_morphology_facts(
    series: ProfileSeries, *, scope: str = "profile_series"
) -> tuple[Fact, ...]:
    """Expose exact factor and vector morphology for an ordered profile series.

    Real null reactions and numerically forced complement nulls are kept distinct.
    Vector configurations containing a forced/undefined reaction are not folded
    into an ordinary ``0`` configuration.
    """
    facts: list[Fact] = [
        Fact(
            key="series.profile_count",
            value=series.profile_count,
            scope=scope,
            fact_id=f"{scope}:profile_count",
        )
    ]

    factor_counts = {factor: Counter() for factor in FACTORS}
    quantum_counts = {factor: Counter() for factor in FACTORS}
    forced_null_counts = Counter()
    vector_counts: dict[str, Counter[tuple[str, str]]] = {}
    vector_undefined = Counter()

    for profile in series.profiles:
        by_factor = {reaction.factor: reaction for reaction in profile.factors}
        for factor in FACTORS:
            reaction = by_factor[factor]
            symbol = _base_symbol(reaction)
            if symbol is None:
                forced_null_counts[factor] += 1
            else:
                factor_counts[factor][symbol] += 1
            quantum_counts[factor][reaction.quantum_level] += 1

        for vector in profile.vectors:
            first, second = vector.factors
            first_symbol = _base_symbol(by_factor[first])
            second_symbol = _base_symbol(by_factor[second])
            vector_counts.setdefault(vector.name, Counter())
            if first_symbol is None or second_symbol is None:
                vector_undefined[vector.name] += 1
            else:
                vector_counts[vector.name][(first_symbol, second_symbol)] += 1

    total_real_nulls = 0
    for factor in FACTORS:
        for symbol, token in _TOKEN_BY_SYMBOL.items():
            count = factor_counts[factor][symbol]
            if symbol == "0":
                total_real_nulls += count
            facts.append(
                Fact(
                    key=f"series.factor.{factor}.base_symbol.{token}.count",
                    value=count,
                    scope=scope,
                    fact_id=f"{scope}:factor:{factor}:base_symbol:{token}:count",
                )
            )
        facts.append(
            Fact(
                key=f"series.factor.{factor}.forced_null.count",
                value=forced_null_counts[factor],
                scope=scope,
                fact_id=f"{scope}:factor:{factor}:forced_null:count",
            )
        )
        for level in range(3):
            facts.append(
                Fact(
                    key=f"series.factor.{factor}.quantum_level.{level}.count",
                    value=quantum_counts[factor][level],
                    scope=scope,
                    fact_id=f"{scope}:factor:{factor}:quantum_level:{level}:count",
                )
            )
        facts.append(
            Fact(
                key=f"series.factor.{factor}.tensioned.count",
                value=sum(count for level, count in quantum_counts[factor].items() if level > 0),
                scope=scope,
                fact_id=f"{scope}:factor:{factor}:tensioned:count",
            )
        )

    facts.append(
        Fact(
            key="series.real_null_reaction.count",
            value=total_real_nulls,
            scope=scope,
            fact_id=f"{scope}:real_null_reaction:count",
        )
    )

    for vector_name, counts in vector_counts.items():
        facts.append(
            Fact(
                key=f"series.vector.{vector_name}.undefined_configuration.count",
                value=vector_undefined[vector_name],
                scope=scope,
                input_state=InputState.AVAILABLE,
                fact_id=f"{scope}:vector:{vector_name}:undefined_configuration:count",
            )
        )
        for first_symbol, first_token in _TOKEN_BY_SYMBOL.items():
            for second_symbol, second_token in _TOKEN_BY_SYMBOL.items():
                count = counts[(first_symbol, second_symbol)]
                facts.append(
                    Fact(
                        key=(
                            f"series.vector.{vector_name}.configuration."
                            f"{first_token}_{second_token}.count"
                        ),
                        value=count,
                        scope=scope,
                        fact_id=(
                            f"{scope}:vector:{vector_name}:configuration:"
                            f"{first_token}_{second_token}:count"
                        ),
                    )
                )

    return tuple(facts)
