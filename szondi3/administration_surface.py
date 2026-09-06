"""Deterministic UI-facing workflow for one Szondi administration.

The canonical recording rules remain in :mod:`szondi3.administration`. This
module exposes card assets, progress and immutable transitions suitable for a
clinician-facing interface. It does not score or interpret choices.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Iterable, Literal

from .administration import (
    ComplementProtocol,
    ComplementSeriesChoice,
    ForegroundProtocol,
    ForegroundSeriesChoice,
    SelectionDirection,
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from .stimuli import SERIES, Stimulus, catalog, presentation_rows

if TYPE_CHECKING:
    from .clinical_pipeline import AdministeredTestRecord

AdministrationPhase = Literal["FOREGROUND", "COMPLEMENT", "COMPLETE"]


@dataclass(frozen=True, slots=True)
class AdministrationCard:
    """Minimal card identity and asset location for a presentation layer."""

    card_id: str
    position: int
    image_path: str


@dataclass(frozen=True, slots=True)
class AdministrationStep:
    phase: Literal["FOREGROUND", "COMPLEMENT"]
    series: str
    cards: tuple[AdministrationCard, ...]
    presentation_rows: tuple[tuple[AdministrationCard, ...], ...] | None

    @property
    def card_ids(self) -> tuple[str, ...]:
        return tuple(card.card_id for card in self.cards)


@dataclass(frozen=True, slots=True)
class AdministrationProgress:
    phase: AdministrationPhase
    completed_steps: int
    total_steps: int
    foreground_completed: int
    complement_completed: int
    current_series: str | None
    is_complete: bool


@dataclass(frozen=True, slots=True)
class AdministrationWorkflow:
    """Immutable state machine for one foreground and optional complement test."""

    include_complement: bool = False
    foreground_choices: tuple[ForegroundSeriesChoice, ...] = ()
    complement_choices: tuple[ComplementSeriesChoice, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.include_complement, bool):
            raise TypeError("include_complement must be bool")
        if len(self.foreground_choices) > len(SERIES):
            raise ValueError("Foreground workflow cannot contain more than six series")
        if len(self.complement_choices) > len(SERIES):
            raise ValueError("Complement workflow cannot contain more than six series")
        if self.complement_choices and not self.include_complement:
            raise ValueError("Complement choices require include_complement=True")
        if self.complement_choices and len(self.foreground_choices) != len(SERIES):
            raise ValueError("Complement choices require a completed foreground")

        expected_foreground = SERIES[: len(self.foreground_choices)]
        observed_foreground = tuple(choice.series for choice in self.foreground_choices)
        if observed_foreground != expected_foreground:
            raise ValueError("Foreground workflow choices must follow series I-VI in order")

        for choice in self.foreground_choices:
            canonical = record_foreground(
                choice.series,
                choice.sympathetic,
                choice.unsympathetic,
            )
            if choice != canonical:
                raise ValueError(
                    f"Foreground workflow series {choice.series} is inconsistent with canonical recording"
                )

        expected_complement = SERIES[: len(self.complement_choices)]
        observed_complement = tuple(choice.series for choice in self.complement_choices)
        if observed_complement != expected_complement:
            raise ValueError("Complement workflow choices must follow series I-VI in order")

        if self.complement_choices:
            foreground_by_series = {
                choice.series: choice for choice in self.foreground_choices
            }
            for choice in self.complement_choices:
                canonical = record_complement(
                    foreground_by_series[choice.series],
                    choice.relative_unsympathetic,
                    "unsympathetic",
                )
                if choice != canonical:
                    raise ValueError(
                        f"Complement workflow series {choice.series} is inconsistent with canonical recording"
                    )

    @property
    def phase(self) -> AdministrationPhase:
        if len(self.foreground_choices) < len(SERIES):
            return "FOREGROUND"
        if self.include_complement and len(self.complement_choices) < len(SERIES):
            return "COMPLEMENT"
        return "COMPLETE"

    @property
    def progress(self) -> AdministrationProgress:
        foreground_completed = len(self.foreground_choices)
        complement_completed = len(self.complement_choices)
        total_steps = len(SERIES) * (2 if self.include_complement else 1)
        completed_steps = foreground_completed + complement_completed
        if self.phase == "FOREGROUND":
            current_series = SERIES[foreground_completed]
        elif self.phase == "COMPLEMENT":
            current_series = SERIES[complement_completed]
        else:
            current_series = None
        return AdministrationProgress(
            phase=self.phase,
            completed_steps=completed_steps,
            total_steps=total_steps,
            foreground_completed=foreground_completed,
            complement_completed=complement_completed,
            current_series=current_series,
            is_complete=self.phase == "COMPLETE",
        )

    @property
    def current_step(self) -> AdministrationStep | None:
        if self.phase == "COMPLETE":
            return None
        if self.phase == "FOREGROUND":
            series = SERIES[len(self.foreground_choices)]
            rows = tuple(
                tuple(_presentation_card(card) for card in row)
                for row in presentation_rows(series)
            )
            cards = tuple(card for row in rows for card in row)
            return AdministrationStep(
                phase="FOREGROUND",
                series=series,
                cards=cards,
                presentation_rows=rows,
            )

        series = SERIES[len(self.complement_choices)]
        foreground = self.foreground_choices[len(self.complement_choices)]
        by_id = {card.card_id: card for card in catalog()}
        cards = tuple(
            _presentation_card(by_id[card_id]) for card_id in foreground.remaining
        )
        return AdministrationStep(
            phase="COMPLEMENT",
            series=series,
            cards=cards,
            presentation_rows=None,
        )

    def submit_foreground(
        self,
        *,
        sympathetic: Iterable[str],
        unsympathetic: Iterable[str],
    ) -> AdministrationWorkflow:
        if self.phase != "FOREGROUND":
            raise RuntimeError("Foreground submission is not available in the current phase")
        series = SERIES[len(self.foreground_choices)]
        choice = record_foreground(series, sympathetic, unsympathetic)
        return replace(
            self,
            foreground_choices=self.foreground_choices + (choice,),
        )

    def submit_complement(
        self,
        *,
        selected: Iterable[str],
        selected_as: SelectionDirection,
    ) -> AdministrationWorkflow:
        if self.phase != "COMPLEMENT":
            raise RuntimeError("Complement submission is not available in the current phase")
        index = len(self.complement_choices)
        foreground = self.foreground_choices[index]
        choice = record_complement(foreground, selected, selected_as)
        return replace(
            self,
            complement_choices=self.complement_choices + (choice,),
        )

    def foreground_protocol(self) -> ForegroundProtocol:
        if len(self.foreground_choices) != len(SERIES):
            raise RuntimeError("Foreground protocol is not complete")
        return complete_foreground(self.foreground_choices)

    def complement_protocol(self) -> ComplementProtocol | None:
        if not self.include_complement:
            return None
        if len(self.complement_choices) != len(SERIES):
            raise RuntimeError("Complement protocol is not complete")
        return complete_complement(self.foreground_protocol(), self.complement_choices)

    def build_record(self) -> AdministeredTestRecord:
        if self.phase != "COMPLETE":
            raise RuntimeError("Administration must be complete before building a clinical record")
        from .clinical_pipeline import AdministeredTestRecord

        return AdministeredTestRecord(
            foreground=self.foreground_protocol(),
            complement=self.complement_protocol(),
        )


def start_administration(*, include_complement: bool = False) -> AdministrationWorkflow:
    """Start an empty administration workflow."""
    return AdministrationWorkflow(include_complement=include_complement)


def _presentation_card(card: Stimulus) -> AdministrationCard:
    return AdministrationCard(
        card_id=card.card_id,
        position=card.position,
        image_path=card.image_path,
    )
