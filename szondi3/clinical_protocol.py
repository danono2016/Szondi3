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
from .p1_errors import P1UnresolvedError
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
        "IC_SZONDI_PRIMARY_000038",
        "IC_SZONDI_PRIMARY_000039",
        "IC_SZONDI_PRIMARY_000041",
        "IC_SZONDI_PRIMARY_000042",
        "IC_SZONDI_PRIMARY_000055",
        "IC_SZONDI_PRIMARY_000056",
        "IC_SZONDI_PRIMARY_000058",
        "IC_SZONDI_PRIMARY_000059",
        "IC_SZONDI_PRIMARY_000060",
        "IC_SZONDI_PRIMARY_000061",
        "IC_SZONDI_PRIMARY_000062",
        "IC_SZONDI_PRIMARY_000063",
        "IC_SZONDI_PRIMARY_000064",
        "IC_SZONDI_PRIMARY_000065",
        "IC_SZONDI_PRIMARY_000066",
        "IC_SZONDI_PRIMARY_000067",
        "IC_SZONDI_PRIMARY_000068",
        "IC_SZONDI_PRIMARY_000069",
        "IC_SZONDI_PRIMARY_000070",
        "IC_SZONDI_PRIMARY_000071",
        "IC_SZONDI_PRIMARY_000072",
        "IC_SZONDI_PRIMARY_000073",
        "IC_SZONDI_PRIMARY_000075",
        "IC_SZONDI_PRIMARY_000076",
        "IC_SZONDI_PRIMARY_000077",
        "IC_SZONDI_PRIMARY_000078",
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
    "IC_SZONDI_PRIMARY_000040",
    "IC_SZONDI_PRIMARY_000043",
    "IC_SZONDI_PRIMARY_000044",
    "IC_SZONDI_PRIMARY_000045",
    "IC_SZONDI_PRIMARY_000050",
    "IC_SZONDI_PRIMARY_000051",
    "IC_SZONDI_PRIMARY_000052",
    "IC_SZONDI_PRIMARY_000057",
    "IC_SZONDI_PRIMARY_000074",
)
LATENCY_SERIES_CLAIM_IDS = (
    "IC_SZONDI_PRIMARY_000015",
    "IC_SZONDI_PRIMARY_000016",
)
DYNAMIC_LATENCY_CLAIM_IDS = (
    "IC_SZONDI_PRIMARY_000029",
    "IC_SZONDI_PRIMARY_000053",
    "IC_SZONDI_PRIMARY_000054",
)
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
    """Capture only typed, source-defined P1 fail-closed states."""
    try:
        return _available(name, operation())
    except P1UnresolvedError as exc:
        return CalculationResult(
            name=name,
            state=CalculationState.UNRESOLVED,
            error=str(exc),
        )


def _sch_polarity_facts(series: ProfileSeries) -> tuple[Fact, ...]:
    """Expose observed +/− directions for k and p without assigning dynamics."""
    scope = "profile_series"
    result: list[Fact] = []
    for factor in ("k", "p"):
        positive_profiles: list[int] = []
        negative_profiles: list[int] = []
        for index, profile in enumerate(series.profiles, start=1):
            reaction = next(item for item in profile.factors if item.factor == factor)
            if reaction.forced_null:
                continue
            if reaction.kind == "positive":
                positive_profiles.append(index)
            elif reaction.kind == "negative":
                negative_profiles.append(index)
        result.extend((
            Fact(key=f"series.sch.{factor}_positive_profiles", value=tuple(positive_profiles), scope=scope, fact_id=f"{scope}:sch:{factor}:positive_profiles"),
            Fact(key=f"series.sch.{factor}_negative_profiles", value=tuple(negative_profiles), scope=scope, fact_id=f"{scope}:sch:{factor}:negative_profiles"),
            Fact(key=f"series.sch.{factor}_opposed_signs_present", value=bool(positive_profiles and negative_profiles), scope=scope, fact_id=f"{scope}:sch:{factor}:opposed_signs_present"),
        ))
    return tuple(result)


def _profile_results(series: ProfileSeries, *, production: bool) -> tuple[ProfileProtocolResult, ...]:
    result = []
    for index, profile in enumerate(series.profiles, start=1):
        facts = profile_facts(profile, scope=f"foreground_profile_{index}")
        interpretation = interpret_facts(facts, production=production, claim_ids=PROFILE_CLAIM_IDS)
        result.append(ProfileProtocolResult(profile_number=index, facts=facts, interpretation=interpretation))
    return tuple(result)


def _series_calculations(series: ProfileSeries) -> tuple[CalculationResult, ...]:
    count = series.profile_count
    calculations: list[CalculationResult] = [
        _capture("series_indices", lambda: series_indices(series)),
        _capture("factor_tension_degrees", lambda: factor_tension_degrees(series)),
        _capture("vector_tension_differences", lambda: vector_tension_differences(series)),
    ]
    if count >= 3:
        calculations.extend((
            _capture("latency_class_structure", lambda: latency_class_structure(series)),
            _capture("leading_drive_classes", lambda: leading_drive_classes(series)),
            _capture("leading_root_direction_evidence", lambda: leading_root_direction_evidence(series)),
            _capture("strict_leading_subclasses", lambda: strict_leading_subclasses(series)),
            _capture("complete_formula", lambda: unique_formula_partition(series)),
            _capture("extended_abbreviated_formula", lambda: extended_abbreviated_formula(series)),
        ))
    else:
        reason = "Trieblinnäus/formula evaluation requires at least three profiles"
        calculations.extend(_not_applicable(name, reason) for name in (
            "latency_class_structure", "leading_drive_classes", "leading_root_direction_evidence",
            "strict_leading_subclasses", "complete_formula", "extended_abbreviated_formula",
        ))
    if count in (8, 10):
        calculations.append(_capture("dur_moll_index", lambda: dur_moll_index(series)))
    else:
        calculations.append(_not_applicable("dur_moll_index", "Dur-Moll method requires an eight- or ten-profile series"))
    if count in (8, 9, 10):
        calculations.append(_capture("social_index", lambda: social_index(series)))
    else:
        calculations.append(_not_applicable("social_index", "Sozialindex requires eight to ten profiles"))
    return tuple(calculations)


def _series_facts_and_claims(series: ProfileSeries, calculations: tuple[CalculationResult, ...]) -> tuple[tuple[Fact, ...], tuple[str, ...]]:
    by_name = {item.name: item for item in calculations}
    facts: list[Fact] = list(series_profile_count_facts(series.profile_count))
    facts.extend(_sch_polarity_facts(series))
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
    if dur_moll.state is CalculationState.AVAILABLE or social.state is CalculationState.AVAILABLE:
        claim_ids.extend(PROPORTION_METHOD_CLAIM_IDS)
    return tuple(facts), tuple(claim_ids)


def evaluate_clinical_protocol(series: ProfileSeries, *, production: bool = False) -> ClinicalProtocolEvaluation:
    """Evaluate one recorded Szondi profile series as an auditable clinical unit."""
    if not isinstance(series, ProfileSeries):
        raise TypeError("Clinical protocol evaluation requires a ProfileSeries")
    profiles = _profile_results(series, production=production)
    calculations = _series_calculations(series)
    facts, claim_ids = _series_facts_and_claims(series, calculations)
    interpretation = interpret_facts(facts, production=production, claim_ids=claim_ids)
    return ClinicalProtocolEvaluation(
        series=series,
        profiles=profiles,
        series_result=SeriesProtocolResult(facts=facts, calculations=calculations, interpretation=interpretation),
        production_mode=production,
    )
