"""Clinic-first orchestration of P1 calculations and P2B interpretation.

A ``ClinicalProtocolEvaluation`` is the first aggregate object intended to resemble
what a clinician actually works with: the recorded profile series, per-profile
interpretation, formal series calculations, unresolved P1 states, and series-level
P2B findings in one traceable structure.

The orchestrator may call deterministic P1 functions, but it never repairs their
fail-closed outcomes. Expected P1 ambiguity is captured as ``UNRESOLVED`` and is
made visible to downstream report/UI layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from .abbreviated_formula import extended_abbreviated_formula
from .clinical_facts import (
    complete_formula_facts,
    dur_moll_facts,
    latency_class_facts,
    leading_drive_class_facts,
    profile_facts,
    root_direction_facts,
    series_index_facts,
    series_profile_count_facts,
    social_index_facts,
)
from .clinical_interpretation import ClinicalInterpretation, interpret_facts
from .formula import unique_formula_partition
from .interpretation import Fact
from .linnaeus import (
    leading_drive_classes,
    leading_root_direction_evidence,
    strict_leading_subclasses,
)
from .proportions import dur_moll_index, social_index
from .series import (
    ProfileSeries,
    factor_tension_degrees,
    latency_class_structure,
    series_indices,
    vector_tension_differences,
)


PROFILE_CLAIM_IDS = (
    tuple(f"IC_SZONDI_PRIMARY_{number:06d}" for number in range(7, 14))
    + (
        "IC_SZONDI_PRIMARY_000017",
        "IC_SZONDI_PRIMARY_000018",
        "IC_SZONDI_PRIMARY_000020",
        "IC_SZONDI_PRIMARY_000021",
        "IC_SZONDI_PRIMARY_000023",
        "IC_SZONDI_PRIMARY_000024",
        "IC_SZONDI_PRIMARY_000034",
        "IC_SZONDI_PRIMARY_000037",
    )
)
ROOT_SERIES_CLAIM_IDS = ("IC_SZONDI_PRIMARY_000001", "IC_SZONDI_PRIMARY_000002")
INDEX_SERIES_CLAIM_IDS = ("IC_SZONDI_PRIMARY_000003", "IC_SZONDI_PRIMARY_000004")
DUR_MOLL_CLAIM_IDS = (
    "IC_SZONDI_PRIMARY_000005",
    "IC_SZONDI_PRIMARY_000033",
)
SOCIAL_INDEX_CLAIM_IDS = ("IC_SZONDI_PRIMARY_000006",)
PROPORTION_METHOD_CLAIM_IDS = ("IC_SZONDI_PRIMARY_000032",)
SERIAL_METHOD_CLAIM_IDS = (
    "IC_SZONDI_PRIMARY_000014",
    "IC_SZONDI_PRIMARY_000019",
    "IC_SZONDI_PRIMARY_000030",
    "IC_SZONDI_PRIMARY_000031",
)
LATENCY_SERIES_CLAIM_IDS = (
    "IC_SZONDI_PRIMARY_000015",
    "IC_SZONDI_PRIMARY_000016",
)
DYNAMIC_LATENCY_CLAIM_IDS = ("IC_SZONDI_PRIMARY_000029",)
FORMULA_SERIES_CLAIM_IDS = (
    "IC_SZONDI_PRIMARY_000025",
    "IC_SZONDI_PRIMARY_000026",
    "IC_SZONDI_PRIMARY_000027",
    "IC_SZONDI_PRIMARY_000028",
)


class CalculationState(str, Enum):
    AVAILABLE = "AVAILABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True, slots=True)
class CalculationResult:
    name: str
    state: CalculationState
    value: Any = None
    error: str | None = None

    def __post_init__(self) -> None:
        if self.state is CalculationState.AVAILABLE and self.error is not None:
            raise ValueError("Available calculation cannot carry an error")
        if self.state is CalculationState.UNRESOLVED and not self.error:
            raise ValueError("Unresolved calculation must preserve its fail-closed reason")


@dataclass(frozen=True, slots=True)
class ProfileProtocolResult:
    profile_number: int
    facts: tuple[Fact, ...]
    interpretation: ClinicalInterpretation


@dataclass(frozen=True, slots=True)
class SeriesProtocolResult:
    facts: tuple[Fact, ...]
    calculations: tuple[CalculationResult, ...]
    interpretation: ClinicalInterpretation

    def calculation(self, name: str) -> CalculationResult:
        matches = tuple(item for item in self.calculations if item.name == name)
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate clinical calculation: {name}")
        return matches[0]


@dataclass(frozen=True, slots=True)
class ClinicalProtocolEvaluation:
    series: ProfileSeries
    profiles: tuple[ProfileProtocolResult, ...]
    series_result: SeriesProtocolResult
    production_mode: bool

    @property
    def profile_count(self) -> int:
        return self.series.profile_count

    @property
    def unresolved_calculations(self) -> tuple[CalculationResult, ...]:
        return tuple(
            item
            for item in self.series_result.calculations
            if item.state is CalculationState.UNRESOLVED
        )


def _available(name: str, value: Any) -> CalculationResult:
    return CalculationResult(name=name, state=CalculationState.AVAILABLE, value=value)


def _not_applicable(name: str, reason: str) -> CalculationResult:
    return CalculationResult(
        name=name,
        state=CalculationState.NOT_APPLICABLE,
        error=reason,
    )


def _capture(name: str, operation: Callable[[], Any]) -> CalculationResult:
    """Capture expected fail-closed P1 outcomes without masking programming errors."""
    try:
        return _available(name, operation())
    except (ValueError, TypeError) as exc:
        return CalculationResult(
            name=name,
            state=CalculationState.UNRESOLVED,
            error=str(exc),
        )


def _profile_results(
    series: ProfileSeries, *, production: bool
) -> tuple[ProfileProtocolResult, ...]:
    result = []
    for index, profile in enumerate(series.profiles, start=1):
        facts = profile_facts(profile, scope=f"foreground_profile_{index}")
        interpretation = interpret_facts(
            facts,
            production=production,
            claim_ids=PROFILE_CLAIM_IDS,
        )
        result.append(
            ProfileProtocolResult(
                profile_number=index,
                facts=facts,
                interpretation=interpretation,
            )
        )
    return tuple(result)


def _series_calculations(series: ProfileSeries) -> tuple[CalculationResult, ...]:
    count = series.profile_count
    calculations: list[CalculationResult] = [
        _capture("series_indices", lambda: series_indices(series)),
        _capture("factor_tension_degrees", lambda: factor_tension_degrees(series)),
        _capture("vector_tension_differences", lambda: vector_tension_differences(series)),
    ]

    if count >= 3:
        calculations.extend(
            (
                _capture("latency_class_structure", lambda: latency_class_structure(series)),
                _capture("leading_drive_classes", lambda: leading_drive_classes(series)),
                _capture(
                    "leading_root_direction_evidence",
                    lambda: leading_root_direction_evidence(series),
                ),
                _capture("strict_leading_subclasses", lambda: strict_leading_subclasses(series)),
                _capture("complete_formula", lambda: unique_formula_partition(series)),
                _capture(
                    "extended_abbreviated_formula",
                    lambda: extended_abbreviated_formula(series),
                ),
            )
        )
    else:
        reason = "Trieblinnäus/formula evaluation requires at least three profiles"
        calculations.extend(
            _not_applicable(name, reason)
            for name in (
                "latency_class_structure",
                "leading_drive_classes",
                "leading_root_direction_evidence",
                "strict_leading_subclasses",
                "complete_formula",
                "extended_abbreviated_formula",
            )
        )

    if count in (8, 10):
        calculations.append(_capture("dur_moll_index", lambda: dur_moll_index(series)))
    else:
        calculations.append(
            _not_applicable(
                "dur_moll_index",
                "Dur-Moll method requires an eight- or ten-profile series",
            )
        )

    if count in (8, 9, 10):
        calculations.append(_capture("social_index", lambda: social_index(series)))
    else:
        calculations.append(
            _not_applicable(
                "social_index",
                "Sozialindex requires eight to ten profiles",
            )
        )

    return tuple(calculations)


def _series_facts_and_claims(
    series: ProfileSeries,
    calculations: tuple[CalculationResult, ...],
) -> tuple[tuple[Fact, ...], tuple[str, ...]]:
    by_name = {item.name: item for item in calculations}
    facts: list[Fact] = list(series_profile_count_facts(series.profile_count))
    claim_ids: list[str] = list(SERIAL_METHOD_CLAIM_IDS)

    indices = by_name["series_indices"]
    claim_ids.extend(INDEX_SERIES_CLAIM_IDS)
    if indices.state is CalculationState.AVAILABLE:
        facts.extend(series_index_facts(indices.value))

    leaders = by_name["leading_drive_classes"]
    latency = by_name["latency_class_structure"]
    if leaders.state is CalculationState.AVAILABLE:
        facts.extend(leading_drive_class_facts(leaders.value))
    if series.profile_count >= 3:
        claim_ids.extend(DYNAMIC_LATENCY_CLAIM_IDS)
        if latency.state is CalculationState.AVAILABLE:
            facts.extend(latency_class_facts(latency.value))
    if series.profile_count == 10:
        claim_ids.extend(LATENCY_SERIES_CLAIM_IDS)

    if series.profile_count >= 3:
        root = by_name["leading_root_direction_evidence"]
        claim_ids.extend(ROOT_SERIES_CLAIM_IDS)
        if root.state is CalculationState.AVAILABLE:
            facts.extend(root_direction_facts(root.value))

        formula = by_name["complete_formula"]
        claim_ids.extend(FORMULA_SERIES_CLAIM_IDS)
        if formula.state is CalculationState.AVAILABLE:
            facts.extend(complete_formula_facts(formula.value))

    dur_moll = by_name["dur_moll_index"]
    if series.profile_count in (8, 10):
        claim_ids.extend(DUR_MOLL_CLAIM_IDS)
        if dur_moll.state is CalculationState.AVAILABLE:
            facts.extend(dur_moll_facts(dur_moll.value))

    social = by_name["social_index"]
    if series.profile_count in (8, 9, 10):
        claim_ids.extend(SOCIAL_INDEX_CLAIM_IDS)
        if social.state is CalculationState.AVAILABLE:
            facts.extend(social_index_facts(social.value))

    if (
        dur_moll.state is CalculationState.AVAILABLE
        or social.state is CalculationState.AVAILABLE
    ):
        claim_ids.extend(PROPORTION_METHOD_CLAIM_IDS)

    return tuple(facts), tuple(claim_ids)


def evaluate_clinical_protocol(
    series: ProfileSeries,
    *,
    production: bool = False,
) -> ClinicalProtocolEvaluation:
    """Evaluate one recorded Szondi profile series as an auditable clinical unit.

    The result intentionally contains both successful and unresolved calculations.
    A failure in one P1 method does not erase independent usable outputs, and no
    local ambiguity is repaired by the orchestrator.
    """
    if not isinstance(series, ProfileSeries):
        raise TypeError("Clinical protocol evaluation requires a ProfileSeries")

    profiles = _profile_results(series, production=production)
    calculations = _series_calculations(series)
    facts, claim_ids = _series_facts_and_claims(series, calculations)
    interpretation = interpret_facts(
        facts,
        production=production,
        claim_ids=claim_ids,
    )
    return ClinicalProtocolEvaluation(
        series=series,
        profiles=profiles,
        series_result=SeriesProtocolResult(
            facts=facts,
            calculations=calculations,
            interpretation=interpretation,
        ),
        production_mode=production,
    )
