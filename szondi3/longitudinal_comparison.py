"""Deterministic structural comparison of completed clinical case runs.

This module implements the Longitudinal Comparison capacity from the product path.
It compares already-produced ``ClinicalCaseRun`` objects without recalculating P1,
adding P2B claims, or assigning Szondian meaning to change. Comparison is based on
stable structural identities and preserves unresolved/blocked activation states.

A small ``LongitudinalCaseRef`` wrapper supplies the external comparison identity
because ``ClinicalCaseRun`` intentionally has no persistence/case identifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from .clinical_case_runner import ClinicalCaseRun
from .clinical_evidence_packet import FactorSeriesEvidence, VectorSeriesEvidence
from .clinical_exploration import explore_clinical_case
from .clinical_release import ClinicalReleaseManifest
from .clinical_report import ReportCalculation, ReportFinding, ReportHeader
from .interpretation import ActivationRecord, ActivationStatus
from .interpretation_catalogue_fate_modifiability import CLAIMS_BY_ID


@dataclass(frozen=True, slots=True)
class LongitudinalCaseRef:
    """External identity plus one already-completed canonical clinical run."""

    case_id: str
    run: ClinicalCaseRun

    def __post_init__(self) -> None:
        if not isinstance(self.case_id, str) or not self.case_id.strip():
            raise ValueError("case_id must be a non-empty string")
        if not isinstance(self.run, ClinicalCaseRun):
            raise TypeError("run must be a ClinicalCaseRun")


@dataclass(frozen=True, slots=True)
class FieldDiff:
    label: str
    value_a: Any
    value_b: Any
    is_identical: bool
    note: str | None = None


@dataclass(frozen=True, slots=True, order=True)
class ClaimOccurrenceKey:
    """Identity of one routed claim occurrence inside a case."""

    scope: str
    profile_number: int | None
    claim_id: str


@dataclass(frozen=True, slots=True)
class ClaimOccurrence:
    key: ClaimOccurrenceKey
    state: ActivationStatus
    support_fact_ids: frozenset[str]
    doctrine_ids: frozenset[str]
    source_ids: frozenset[str]


@dataclass(frozen=True, slots=True)
class ClaimComparison:
    key: ClaimOccurrenceKey
    state_a: ActivationStatus | None
    state_b: ActivationStatus | None
    present_in_a: bool
    present_in_b: bool
    state_changed: bool
    support_fact_ids_a: frozenset[str]
    support_fact_ids_b: frozenset[str]
    doctrine_ids_a: frozenset[str]
    doctrine_ids_b: frozenset[str]
    source_ids_a: frozenset[str]
    source_ids_b: frozenset[str]


@dataclass(frozen=True, slots=True)
class FactorComparison:
    factor: str
    symbol_sequence_a: tuple[str, ...] | None
    symbol_sequence_b: tuple[str, ...] | None
    sequences_identical: bool
    base_symbol_sequence_a: tuple[str, ...] | None
    base_symbol_sequence_b: tuple[str, ...] | None
    base_sequences_identical: bool
    quantum_total_diff: FieldDiff | None
    field_diffs: tuple[FieldDiff, ...]


@dataclass(frozen=True, slots=True)
class VectorComparison:
    vector: str
    symbol_sequence_a: tuple[tuple[str, str], ...] | None
    symbol_sequence_b: tuple[tuple[str, str], ...] | None
    base_symbol_sequence_a: tuple[tuple[str, str], ...] | None
    base_symbol_sequence_b: tuple[tuple[str, str], ...] | None
    configuration_frequencies_a: tuple[Any, ...] | None
    configuration_frequencies_b: tuple[Any, ...] | None
    is_identical: bool


@dataclass(frozen=True, slots=True)
class ComparabilityIssue:
    """Engineering-level comparability condition; it adds no clinical meaning."""

    code: str
    detail: str


@dataclass(frozen=True, slots=True)
class CaseComparisonResult:
    case_id_a: str
    case_id_b: str
    comparability_issues: tuple[ComparabilityIssue, ...]
    header_diffs: tuple[FieldDiff, ...]
    factor_comparisons: tuple[FactorComparison, ...]
    vector_comparisons: tuple[VectorComparison, ...]
    series_calculation_diffs: tuple[FieldDiff, ...]
    claim_comparisons: tuple[ClaimComparison, ...]
    unresolved_or_blocked_a: frozenset[ClaimOccurrenceKey]
    unresolved_or_blocked_b: frozenset[ClaimOccurrenceKey]
    experimental_complement_present_a: bool
    experimental_complement_present_b: bool


def _check_provenance(
    manifest_a: ClinicalReleaseManifest | None,
    manifest_b: ClinicalReleaseManifest | None,
) -> tuple[ComparabilityIssue, ...]:
    """Expose runtime/doctrine/P2B provenance differences without blocking diff."""
    issues: list[ComparabilityIssue] = []

    if manifest_a is None or manifest_b is None:
        issues.append(
            ComparabilityIssue(
                code="RELEASE_MANIFEST_MISSING",
                detail=(
                    "release manifest missing: "
                    f"A={'present' if manifest_a is not None else 'missing'}, "
                    f"B={'present' if manifest_b is not None else 'missing'}"
                ),
            )
        )
        return tuple(issues)

    if manifest_a.git_commit_sha != manifest_b.git_commit_sha:
        issues.append(
            ComparabilityIssue(
                code="RUNTIME_VERSION_MISMATCH",
                detail=(
                    f"git_commit_sha A={manifest_a.git_commit_sha} "
                    f"vs B={manifest_b.git_commit_sha}"
                ),
            )
        )

    if (
        manifest_a.doctrine_snapshot_id != manifest_b.doctrine_snapshot_id
        or manifest_a.doctrine_registry_sha256 != manifest_b.doctrine_registry_sha256
    ):
        issues.append(
            ComparabilityIssue(
                code="DOCTRINE_SNAPSHOT_MISMATCH",
                detail=(
                    "doctrine_snapshot_id "
                    f"A={manifest_a.doctrine_snapshot_id} "
                    f"vs B={manifest_b.doctrine_snapshot_id}; "
                    "doctrine_registry_sha256 "
                    f"A={manifest_a.doctrine_registry_sha256} "
                    f"vs B={manifest_b.doctrine_registry_sha256}"
                ),
            )
        )

    if (
        manifest_a.p2b_release_id != manifest_b.p2b_release_id
        or manifest_a.p2b_catalogue_sha256 != manifest_b.p2b_catalogue_sha256
    ):
        issues.append(
            ComparabilityIssue(
                code="P2B_RELEASE_MISMATCH",
                detail=(
                    f"p2b_release_id A={manifest_a.p2b_release_id} "
                    f"vs B={manifest_b.p2b_release_id}; "
                    "p2b_catalogue_sha256 "
                    f"A={manifest_a.p2b_catalogue_sha256} "
                    f"vs B={manifest_b.p2b_catalogue_sha256}"
                ),
            )
        )

    return tuple(issues)


def _check_comparability(
    case_a: LongitudinalCaseRef,
    case_b: LongitudinalCaseRef,
) -> tuple[ComparabilityIssue, ...]:
    issues: list[ComparabilityIssue] = []
    header_a = case_a.run.report.header
    header_b = case_b.run.report.header

    if header_a.profile_count != header_b.profile_count:
        issues.append(
            ComparabilityIssue(
                code="PROFILE_COUNT_MISMATCH",
                detail=(
                    f"profile_count A={header_a.profile_count} "
                    f"vs B={header_b.profile_count}"
                ),
            )
        )
    if header_a.production_mode != header_b.production_mode:
        issues.append(
            ComparabilityIssue(
                code="PRODUCTION_MODE_MISMATCH",
                detail=(
                    f"production_mode A={header_a.production_mode!r} "
                    f"vs B={header_b.production_mode!r}"
                ),
            )
        )

    complement_a = bool(case_a.run.evaluation.complement_profiles)
    complement_b = bool(case_b.run.evaluation.complement_profiles)
    if complement_a != complement_b:
        issues.append(
            ComparabilityIssue(
                code="EXPERIMENTAL_COMPLEMENT_ASYMMETRY",
                detail=(
                    f"complement present in A={complement_a}, "
                    f"in B={complement_b}"
                ),
            )
        )

    issues.extend(
        _check_provenance(
            getattr(case_a.run.release, "manifest", None),
            getattr(case_b.run.release, "manifest", None),
        )
    )
    return tuple(issues)


def _diff_header(a: ReportHeader, b: ReportHeader) -> tuple[FieldDiff, ...]:
    return (
        FieldDiff(
            "profile_count",
            a.profile_count,
            b.profile_count,
            a.profile_count == b.profile_count,
        ),
        FieldDiff(
            "production_mode",
            a.production_mode,
            b.production_mode,
            a.production_mode == b.production_mode,
        ),
        FieldDiff(
            "interpretation_release_state",
            a.interpretation_release_state,
            b.interpretation_release_state,
            a.interpretation_release_state == b.interpretation_release_state,
        ),
    )


def _factor_map(items: Sequence[FactorSeriesEvidence]) -> dict[str, FactorSeriesEvidence]:
    result: dict[str, FactorSeriesEvidence] = {}
    for item in items:
        if item.factor in result:
            raise ValueError(f"Duplicate factor identity in evidence packet: {item.factor}")
        result[item.factor] = item
    return result


def _diff_factors(
    factors_a: Sequence[FactorSeriesEvidence],
    factors_b: Sequence[FactorSeriesEvidence],
) -> tuple[FactorComparison, ...]:
    by_a = _factor_map(factors_a)
    by_b = _factor_map(factors_b)
    result: list[FactorComparison] = []

    comparable_fields = (
        "positive_count",
        "negative_count",
        "null_count",
        "ambivalent_count",
        "forced_null_count",
        "tensioned_profiles",
    )
    for factor in sorted(set(by_a) | set(by_b)):
        a = by_a.get(factor)
        b = by_b.get(factor)
        symbols_a = a.symbols if a is not None else None
        symbols_b = b.symbols if b is not None else None
        base_a = a.base_symbols if a is not None else None
        base_b = b.base_symbols if b is not None else None

        field_diffs = tuple(
            FieldDiff(
                label=f"{factor}.{name}",
                value_a=getattr(a, name) if a is not None else None,
                value_b=getattr(b, name) if b is not None else None,
                is_identical=(
                    getattr(a, name) if a is not None else None
                ) == (
                    getattr(b, name) if b is not None else None
                ),
            )
            for name in comparable_fields
        )
        quantum_diff = FieldDiff(
            label=f"{factor}.quantum_total",
            value_a=a.quantum_total if a is not None else None,
            value_b=b.quantum_total if b is not None else None,
            is_identical=(
                a.quantum_total if a is not None else None
            ) == (
                b.quantum_total if b is not None else None
            ),
        )
        result.append(
            FactorComparison(
                factor=factor,
                symbol_sequence_a=symbols_a,
                symbol_sequence_b=symbols_b,
                sequences_identical=symbols_a == symbols_b,
                base_symbol_sequence_a=base_a,
                base_symbol_sequence_b=base_b,
                base_sequences_identical=base_a == base_b,
                quantum_total_diff=quantum_diff,
                field_diffs=field_diffs,
            )
        )
    return tuple(result)


def _vector_map(items: Sequence[VectorSeriesEvidence]) -> dict[str, VectorSeriesEvidence]:
    result: dict[str, VectorSeriesEvidence] = {}
    for item in items:
        if item.vector in result:
            raise ValueError(f"Duplicate vector identity in evidence packet: {item.vector}")
        result[item.vector] = item
    return result


def _diff_vectors(
    vectors_a: Sequence[VectorSeriesEvidence],
    vectors_b: Sequence[VectorSeriesEvidence],
) -> tuple[VectorComparison, ...]:
    by_a = _vector_map(vectors_a)
    by_b = _vector_map(vectors_b)
    result: list[VectorComparison] = []
    for vector in sorted(set(by_a) | set(by_b)):
        a = by_a.get(vector)
        b = by_b.get(vector)
        result.append(
            VectorComparison(
                vector=vector,
                symbol_sequence_a=a.symbols if a is not None else None,
                symbol_sequence_b=b.symbols if b is not None else None,
                base_symbol_sequence_a=a.base_symbols if a is not None else None,
                base_symbol_sequence_b=b.base_symbols if b is not None else None,
                configuration_frequencies_a=(
                    a.configuration_frequencies if a is not None else None
                ),
                configuration_frequencies_b=(
                    b.configuration_frequencies if b is not None else None
                ),
                is_identical=a == b,
            )
        )
    return tuple(result)


def _calculation_map(
    calculations: Sequence[ReportCalculation],
) -> dict[str, ReportCalculation]:
    result: dict[str, ReportCalculation] = {}
    for item in calculations:
        if item.name in result:
            raise ValueError(f"Duplicate report calculation identity: {item.name}")
        result[item.name] = item
    return result


def _diff_series_calculations(
    calculations_a: Sequence[ReportCalculation],
    calculations_b: Sequence[ReportCalculation],
) -> tuple[FieldDiff, ...]:
    by_a = _calculation_map(calculations_a)
    by_b = _calculation_map(calculations_b)
    result: list[FieldDiff] = []
    for name in sorted(set(by_a) | set(by_b)):
        a = by_a.get(name)
        b = by_b.get(name)
        note = None
        if a is None:
            note = "absent in A"
        elif b is None:
            note = "absent in B"
        result.append(
            FieldDiff(
                label=f"calculation.{name}",
                value_a=a,
                value_b=b,
                is_identical=a == b,
                note=note,
            )
        )
    return tuple(result)


def _active_occurrence(finding: ReportFinding) -> ClaimOccurrence:
    return ClaimOccurrence(
        key=ClaimOccurrenceKey(
            scope=finding.scope,
            profile_number=finding.profile_number,
            claim_id=finding.claim_id,
        ),
        state=ActivationStatus.ACTIVE,
        support_fact_ids=frozenset(finding.support_fact_ids),
        doctrine_ids=frozenset(finding.doctrine_ids),
        source_ids=frozenset(finding.source_ids),
    )


def _nonactive_occurrence(
    scope: str,
    profile_number: int | None,
    activation: ActivationRecord,
) -> ClaimOccurrence:
    claim = CLAIMS_BY_ID.get(activation.claim_id)
    if claim is None:
        raise ValueError(f"Routed activation has unknown claim id: {activation.claim_id}")
    return ClaimOccurrence(
        key=ClaimOccurrenceKey(
            scope=scope,
            profile_number=profile_number,
            claim_id=activation.claim_id,
        ),
        state=activation.activation_status,
        support_fact_ids=frozenset(
            fact.fact_id for fact in activation.matched_facts if fact.fact_id is not None
        ),
        doctrine_ids=frozenset(claim.doctrine_ids),
        source_ids=frozenset(claim.source_ids),
    )


def _claim_occurrences(run: ClinicalCaseRun) -> dict[ClaimOccurrenceKey, ClaimOccurrence]:
    result: dict[ClaimOccurrenceKey, ClaimOccurrence] = {}

    def add(item: ClaimOccurrence) -> None:
        if item.key in result:
            raise ValueError(
                "Duplicate routed claim occurrence in longitudinal comparison: "
                f"{item.key}"
            )
        result[item.key] = item

    for finding in run.report.findings:
        if finding.scope in {"PROFILE", "SERIES", "EXPERIMENTAL_COMPLEMENT"}:
            add(_active_occurrence(finding))

    evaluation = run.evaluation.clinical_evaluation
    for profile in evaluation.profiles:
        for activation in profile.interpretation.suppressed:
            add(_nonactive_occurrence("PROFILE", profile.profile_number, activation))
    for activation in evaluation.series_result.interpretation.suppressed:
        add(_nonactive_occurrence("SERIES", None, activation))
    for complement in run.evaluation.complement_profiles:
        for activation in complement.interpretation.suppressed:
            add(
                _nonactive_occurrence(
                    "EXPERIMENTAL_COMPLEMENT",
                    complement.test_number,
                    activation,
                )
            )
    return result


def _diff_claims(
    run_a: ClinicalCaseRun,
    run_b: ClinicalCaseRun,
) -> tuple[ClaimComparison, ...]:
    by_a = _claim_occurrences(run_a)
    by_b = _claim_occurrences(run_b)
    result: list[ClaimComparison] = []
    for key in sorted(set(by_a) | set(by_b)):
        a = by_a.get(key)
        b = by_b.get(key)
        state_a = a.state if a is not None else None
        state_b = b.state if b is not None else None
        result.append(
            ClaimComparison(
                key=key,
                state_a=state_a,
                state_b=state_b,
                present_in_a=a is not None,
                present_in_b=b is not None,
                state_changed=state_a != state_b,
                support_fact_ids_a=(
                    a.support_fact_ids if a is not None else frozenset()
                ),
                support_fact_ids_b=(
                    b.support_fact_ids if b is not None else frozenset()
                ),
                doctrine_ids_a=a.doctrine_ids if a is not None else frozenset(),
                doctrine_ids_b=b.doctrine_ids if b is not None else frozenset(),
                source_ids_a=a.source_ids if a is not None else frozenset(),
                source_ids_b=b.source_ids if b is not None else frozenset(),
            )
        )
    return tuple(result)


def _unresolved_or_blocked(run: ClinicalCaseRun) -> frozenset[ClaimOccurrenceKey]:
    blocking = {
        ActivationStatus.UNRESOLVED_INPUT,
        ActivationStatus.BLOCKED_CONTEXT,
        ActivationStatus.BLOCKED_SOURCE_CONFLICT,
    }
    return frozenset(
        key for key, item in _claim_occurrences(run).items() if item.state in blocking
    )


def compare_clinical_cases(
    case_a: LongitudinalCaseRef,
    case_b: LongitudinalCaseRef,
) -> CaseComparisonResult:
    """Compare two validated runs without assigning meaning to the differences.

    Structural comparability issues are reported and comparison continues. Tampered
    or internally inconsistent case runs are not a comparability issue: they fail
    closed through the existing clinical exploration integrity boundary.
    """
    if not isinstance(case_a, LongitudinalCaseRef):
        raise TypeError("case_a must be a LongitudinalCaseRef")
    if not isinstance(case_b, LongitudinalCaseRef):
        raise TypeError("case_b must be a LongitudinalCaseRef")

    explore_clinical_case(case_a.run)
    explore_clinical_case(case_b.run)

    return CaseComparisonResult(
        case_id_a=case_a.case_id,
        case_id_b=case_b.case_id,
        comparability_issues=_check_comparability(case_a, case_b),
        header_diffs=_diff_header(case_a.run.report.header, case_b.run.report.header),
        factor_comparisons=_diff_factors(
            case_a.run.evidence_packet.factor_series,
            case_b.run.evidence_packet.factor_series,
        ),
        vector_comparisons=_diff_vectors(
            case_a.run.evidence_packet.vector_series,
            case_b.run.evidence_packet.vector_series,
        ),
        series_calculation_diffs=_diff_series_calculations(
            case_a.run.report.calculations,
            case_b.run.report.calculations,
        ),
        claim_comparisons=_diff_claims(case_a.run, case_b.run),
        unresolved_or_blocked_a=_unresolved_or_blocked(case_a.run),
        unresolved_or_blocked_b=_unresolved_or_blocked(case_b.run),
        experimental_complement_present_a=bool(case_a.run.evaluation.complement_profiles),
        experimental_complement_present_b=bool(case_b.run.evaluation.complement_profiles),
    )


def compare_clinical_case_sequence(
    cases: Sequence[LongitudinalCaseRef],
) -> tuple[CaseComparisonResult, ...]:
    """Compare only successive pairs A-B, B-C, C-D in the supplied order."""
    supplied = tuple(cases)
    if len(supplied) < 2:
        raise ValueError("At least two clinical cases are required for comparison")
    if any(not isinstance(item, LongitudinalCaseRef) for item in supplied):
        raise TypeError("cases must contain only LongitudinalCaseRef objects")
    return tuple(
        compare_clinical_cases(supplied[index], supplied[index + 1])
        for index in range(len(supplied) - 1)
    )
