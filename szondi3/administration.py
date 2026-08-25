"""Deterministic recording of Szondi's basic choice procedure.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 46-49, Instruktionen Nr. I-II.

This module records formal choices only. It does not score or interpret them.
"""

from dataclasses import dataclass
from typing import Iterable, Literal

from .stimuli import SERIES, presentation_rows

SelectionDirection = Literal["sympathetic", "unsympathetic"]


def _series_card_ids(series: str) -> tuple[str, ...]:
    rows = presentation_rows(series)
    return tuple(card.card_id for row in rows for card in row)


def _require_two_distinct(values: Iterable[str], label: str) -> tuple[str, str]:
    chosen = tuple(values)
    if len(chosen) != 2 or len(set(chosen)) != 2:
        raise ValueError(f"{label} must contain exactly two distinct cards")
    return chosen


@dataclass(frozen=True, slots=True)
class ForegroundSeriesChoice:
    series: str
    sympathetic: tuple[str, str]
    unsympathetic: tuple[str, str]
    remaining: tuple[str, str, str, str]


@dataclass(frozen=True, slots=True)
class ForegroundProtocol:
    series_choices: tuple[ForegroundSeriesChoice, ...]
    sympathetic: tuple[str, ...]
    unsympathetic: tuple[str, ...]
    remaining: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ComplementSeriesChoice:
    series: str
    relative_sympathetic: tuple[str, str]
    relative_unsympathetic: tuple[str, str]


@dataclass(frozen=True, slots=True)
class ComplementProtocol:
    series_choices: tuple[ComplementSeriesChoice, ...]
    relative_sympathetic: tuple[str, ...]
    relative_unsympathetic: tuple[str, ...]


def record_foreground(
    series: str,
    sympathetic: Iterable[str],
    unsympathetic: Iterable[str],
) -> ForegroundSeriesChoice:
    """Record the two sympathetic and two unsympathetic choices from one series."""
    available = _series_card_ids(series)
    positive = _require_two_distinct(sympathetic, "sympathetic")
    negative = _require_two_distinct(unsympathetic, "unsympathetic")
    selected = positive + negative

    if len(set(selected)) != 4:
        raise ValueError("Foreground choices must contain four distinct cards")
    if any(card_id not in available for card_id in selected):
        raise ValueError(f"Foreground choices must all belong to series {series}")

    remaining = tuple(card_id for card_id in available if card_id not in selected)
    return ForegroundSeriesChoice(series, positive, negative, remaining)


def complete_foreground(choices: Iterable[ForegroundSeriesChoice]) -> ForegroundProtocol:
    """Validate and combine one foreground choice for each of the six series."""
    supplied = tuple(choices)
    by_series = {choice.series: choice for choice in supplied}
    if len(supplied) != len(SERIES) or set(by_series) != set(SERIES):
        raise ValueError("Foreground protocol requires exactly one choice for each series I-VI")

    ordered = tuple(by_series[series] for series in SERIES)
    return ForegroundProtocol(
        series_choices=ordered,
        sympathetic=tuple(card for choice in ordered for card in choice.sympathetic),
        unsympathetic=tuple(card for choice in ordered for card in choice.unsympathetic),
        remaining=tuple(card for choice in ordered for card in choice.remaining),
    )


def record_complement(
    foreground: ForegroundSeriesChoice,
    selected: Iterable[str],
    selected_as: SelectionDirection,
) -> ComplementSeriesChoice:
    """Record the second choice among the four cards left from one series.

    Szondi normally asks for the two relatively most unsympathetic cards, while
    explicitly allowing the inverse instruction for some subjects. Both routes
    are normalized here to the same two relative categories.
    """
    chosen = _require_two_distinct(selected, "complement selection")
    if selected_as not in ("sympathetic", "unsympathetic"):
        raise ValueError("selected_as must be 'sympathetic' or 'unsympathetic'")
    if any(card_id not in foreground.remaining for card_id in chosen):
        raise ValueError("Complement choices must come from the four remaining cards")

    other = tuple(card_id for card_id in foreground.remaining if card_id not in chosen)
    if selected_as == "unsympathetic":
        positive, negative = other, chosen
    else:
        positive, negative = chosen, other

    return ComplementSeriesChoice(
        series=foreground.series,
        relative_sympathetic=positive,
        relative_unsympathetic=negative,
    )


def complete_complement(
    foreground: ForegroundProtocol,
    choices: Iterable[ComplementSeriesChoice],
) -> ComplementProtocol:
    """Validate and combine one complement choice for every foreground series."""
    supplied = tuple(choices)
    by_series = {choice.series: choice for choice in supplied}
    if len(supplied) != len(SERIES) or set(by_series) != set(SERIES):
        raise ValueError("Complement protocol requires exactly one choice for each series I-VI")

    foreground_by_series = {choice.series: choice for choice in foreground.series_choices}
    ordered = tuple(by_series[series] for series in SERIES)
    for choice in ordered:
        expected = set(foreground_by_series[choice.series].remaining)
        observed = set(choice.relative_sympathetic + choice.relative_unsympathetic)
        if observed != expected:
            raise ValueError(f"Complement choice does not partition remaining series {choice.series}")

    return ComplementProtocol(
        series_choices=ordered,
        relative_sympathetic=tuple(
            card for choice in ordered for card in choice.relative_sympathetic
        ),
        relative_unsympathetic=tuple(
            card for choice in ordered for card in choice.relative_unsympathetic
        ),
    )
