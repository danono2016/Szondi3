"""Deterministic source-derived proportion methods.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 332-337, especially Abb. 21.

This module implements only the formal arithmetic of the vectorial Dur-Moll
method: source-tabulated D/M classification of the 16 vector reactions in each
of the four vector spaces, reaction frequencies, quantum-exclamation counts,
D:M scores, and the percentage index. Psychological, sexual, genetic, clinical,
or normative meanings of those proportions belong to later layers.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from .series import ProfileSeries

DurMollKind = Literal["D", "M"]

_BASE_SYMBOL_BY_KIND = {
    "null": "0",
    "positive": "+",
    "negative": "-",
    "ambivalent": "±",
}

# Visual transcription of Lehrbuch Abb. 21. Every vector has exactly the same
# sixteen formal reaction keys, but Szondi assigns their Dur/Moll character
# differently by vector space.
_DUR_MOLL = {
    "S": {
        ("0", "0"): "M",
        ("0", "±"): "M",
        ("0", "+"): "D",
        ("0", "-"): "M",
        ("±", "0"): "D",
        ("±", "±"): "M",
        ("±", "+"): "D",
        ("±", "-"): "M",
        ("+", "0"): "D",
        ("+", "±"): "M",
        ("+", "+"): "D",
        ("+", "-"): "M",
        ("-", "0"): "D",
        ("-", "±"): "D",
        ("-", "+"): "D",
        ("-", "-"): "M",
    },
    "P": {
        ("0", "0"): "M",
        ("0", "±"): "M",
        ("0", "+"): "D",
        ("0", "-"): "M",
        ("±", "0"): "D",
        ("±", "±"): "D",
        ("±", "+"): "D",
        ("±", "-"): "M",
        ("+", "0"): "M",
        ("+", "±"): "M",
        ("+", "+"): "M",
        ("+", "-"): "M",
        ("-", "0"): "D",
        ("-", "±"): "D",
        ("-", "+"): "D",
        ("-", "-"): "D",
    },
    "Sch": {
        ("0", "0"): "M",
        ("0", "±"): "M",
        ("0", "+"): "M",
        ("0", "-"): "M",
        ("±", "0"): "D",
        ("±", "±"): "D",
        ("±", "+"): "D",
        ("±", "-"): "D",
        ("+", "0"): "D",
        ("+", "±"): "M",
        ("+", "+"): "M",
        ("+", "-"): "D",
        ("-", "0"): "D",
        ("-", "±"): "M",
        ("-", "+"): "M",
        ("-", "-"): "D",
    },
    "C": {
        ("0", "0"): "M",
        ("0", "±"): "M",
        ("0", "+"): "D",
        ("0", "-"): "D",
        ("±", "0"): "M",
        ("±", "±"): "M",
        ("±", "+"): "M",
        ("±", "-"): "D",
        ("+", "0"): "D",
        ("+", "±"): "M",
        ("+", "+"): "M",
        ("+", "-"): "D",
        ("-", "0"): "D",
        ("-", "±"): "D",
        ("-", "+"): "M",
        ("-", "-"): "D",
    },
}


@dataclass(frozen=True, slots=True)
class VectorDurMollCounts:
    """Formal Dur/Moll counts for one vector across an 8- or 10-profile series."""

    vector: str
    dur_reactions: int
    moll_reactions: int
    dur_quantum: int
    moll_quantum: int

    @property
    def dur_score(self) -> int:
        return self.dur_reactions + self.dur_quantum

    @property
    def moll_score(self) -> int:
        return self.moll_reactions + self.moll_quantum


@dataclass(frozen=True, slots=True)
class DurMollIndex:
    """Aggregate formal Dur/Moll scores and exact percentages."""

    vectors: tuple[VectorDurMollCounts, ...]
    total_dur: int
    total_moll: int
    dur_percentage: Fraction
    moll_percentage: Fraction


def dur_moll_character(vector: str, first_symbol: str, second_symbol: str) -> DurMollKind:
    """Return Szondi's D/M class for one base vector reaction from Abb. 21."""
    try:
        table = _DUR_MOLL[vector]
    except KeyError as exc:
        raise ValueError(f"Unknown vector for Dur-Moll classification: {vector}") from exc
    try:
        return table[(first_symbol, second_symbol)]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported base vector reaction for Dur-Moll classification: {first_symbol} {second_symbol}"
        ) from exc


def _base_symbol(reaction) -> str:
    if reaction.forced_null:
        raise ValueError("Zwangs-Nullreaktion cannot enter foreground Dur-Moll calculation")
    try:
        return _BASE_SYMBOL_BY_KIND[reaction.kind]
    except KeyError as exc:
        raise ValueError(f"Unsupported factor reaction kind: {reaction.kind}") from exc


def dur_moll_index(series: ProfileSeries) -> DurMollIndex:
    """Calculate the vectorial Dur-Moll proportions and percentage index.

    Lehrbuch instructs the method on an Achter- or Zehnerserie. Each vector image
    contributes one D/M reaction count according to Abb. 21. Every exclamation
    mark (quantum unit) on the two factors of that vector is then added to the same
    D or M side as the vector image. Per-vector proportion scores are therefore
    ``sum(reactions) + sum(exclamation marks)``. The aggregate %Dur is
    total_D * 100 / (total_D + total_M); %Moll is the remainder to 100.
    """
    if series.profile_count not in (8, 10):
        raise ValueError("Dur-Moll method requires an eight- or ten-profile series")

    vector_order = ("S", "P", "Sch", "C")
    accum = {
        vector: {"D_re": 0, "M_re": 0, "D_q": 0, "M_q": 0}
        for vector in vector_order
    }

    for profile in series.profiles:
        by_factor = {reaction.factor: reaction for reaction in profile.factors}
        for vector in profile.vectors:
            first_factor, second_factor = vector.factors
            first = by_factor[first_factor]
            second = by_factor[second_factor]
            kind = dur_moll_character(vector.name, _base_symbol(first), _base_symbol(second))
            accum[vector.name][f"{kind}_re"] += 1
            accum[vector.name][f"{kind}_q"] += first.quantum_level + second.quantum_level

    vectors = tuple(
        VectorDurMollCounts(
            vector=vector,
            dur_reactions=accum[vector]["D_re"],
            moll_reactions=accum[vector]["M_re"],
            dur_quantum=accum[vector]["D_q"],
            moll_quantum=accum[vector]["M_q"],
        )
        for vector in vector_order
    )

    total_dur = sum(item.dur_score for item in vectors)
    total_moll = sum(item.moll_score for item in vectors)
    total = total_dur + total_moll
    if total == 0:
        raise ValueError("Dur-Moll percentage denominator cannot be zero")

    dur_percentage = Fraction(total_dur * 100, total)
    moll_percentage = Fraction(total_moll * 100, total)
    return DurMollIndex(
        vectors=vectors,
        total_dur=total_dur,
        total_moll=total_moll,
        dur_percentage=dur_percentage,
        moll_percentage=moll_percentage,
    )
