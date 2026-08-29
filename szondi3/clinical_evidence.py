"""Minimal P3 clinical-evidence layer for Szondi3.

This module does not reinterpret P1 and does not add doctrine.  It turns an
already evaluated clinical protocol into a stable, case-specific evidence object
that downstream integration and narrative rendering can consume without
recounting the profile series or losing fail-closed boundaries.

The layer deliberately stays small: longitudinal factor patterns, uniquely
addressable P2B findings, and explicit unresolved/blocking boundaries.  A graph
database or generic node/edge framework is not required for these semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from .clinical_interpretation import ClinicianFinding
from .clinical_protocol import CalculationState, ClinicalProtocolEvaluation
from .interpretation import ActivationStatus
from .stimuli import FACTORS


_BASE_SYMBOL_BY_KIND = {
    "null": "0",
    "positive": "+",
    "negative": "-",
    "ambivalent": "±",
}


@dataclass(frozen=True, slots=True)
class FactorSeriesPattern:
    """Deterministic longitudinal observations for one factor.

    ``symbols`` preserves the exact P1 display symbols, including quantum marks.
    ``base_symbols`` strips only quantum intensity while preserving a forced null
    as ``ø`` instead of silently treating it as a free null reaction.
    Profile-number tuples are one-based and therefore directly inspectable against
    the recorded series.
    """

    pattern_id: str
    factor: str
    symbols: tuple[str, ...]
    base_symbols: tuple[str, ...]
    positive_profiles: tuple[int, ...]
    negative_profiles: tuple[int, ...]
    null_profiles: tuple[int, ...]
    ambivalent_profiles: tuple[int, ...]
    forced_null_profiles: tuple[int, ...]
    tensioned_profiles: tuple[int, ...]
    quantum_total: int

    @property
    def profile_count(self) -> int:
        return len(self.symbols)

    @property
    def is_base_constant(self) -> bool:
        return len(set(self.base_symbols)) == 1

    @property
    def transitions(self) -> tuple[tuple[int, str, str], ...]:
        """Return genuine base-reaction changes as (profile, before, after)."""
        return tuple(
            (index + 1, self.base_symbols[index - 1], self.base_symbols[index])
            for index in range(1, len(self.base_symbols))
            if self.base_symbols[index] != self.base_symbols[index - 1]
        )


@dataclass(frozen=True, slots=True)
class GroundedFinding:
    """One activated P2B finding with case-local stable evidence identity."""

    evidence_id: str
    scope: str
    profile_number: int | None
    finding: ClinicianFinding

    @property
    def claim_id(self) -> str:
        return self.finding.claim_id


@dataclass(frozen=True, slots=True)
class GroundingBoundary:
    """An explicit reason why downstream synthesis must not fill a gap."""

    boundary_id: str
    scope: str
    kind: str
    subject: str
    reason: str
    profile_number: int | None = None


@dataclass(frozen=True, slots=True)
class ClinicalEvidence:
    """Case-specific P3 evidence derived from one ClinicalProtocolEvaluation."""

    evaluation: ClinicalProtocolEvaluation
    factor_patterns: tuple[FactorSeriesPattern, ...]
    findings: tuple[GroundedFinding, ...]
    boundaries: tuple[GroundingBoundary, ...]

    def pattern(self, factor: str) -> FactorSeriesPattern:
        matches = tuple(item for item in self.factor_patterns if item.factor == factor)
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate factor pattern: {factor}")
        return matches[0]

    @property
    def support_ids(self) -> tuple[str, ...]:
        return tuple(item.pattern_id for item in self.factor_patterns) + tuple(
            item.evidence_id for item in self.findings
        )


def _factor_patterns(evaluation: ClinicalProtocolEvaluation) -> tuple[FactorSeriesPattern, ...]:
    result = []
    for factor in FACTORS:
        reactions = tuple(
            next(item for item in profile.factors if item.factor == factor)
            for profile in evaluation.series.profiles
        )
        base_symbols = tuple(
            "ø" if item.forced_null else _BASE_SYMBOL_BY_KIND[item.kind]
            for item in reactions
        )
        result.append(
            FactorSeriesPattern(
                pattern_id=f"SP_FACTOR_{factor}",
                factor=factor,
                symbols=tuple(item.symbol for item in reactions),
                base_symbols=base_symbols,
                positive_profiles=tuple(
                    index for index, item in enumerate(reactions, start=1)
                    if item.kind == "positive" and not item.forced_null
                ),
                negative_profiles=tuple(
                    index for index, item in enumerate(reactions, start=1)
                    if item.kind == "negative" and not item.forced_null
                ),
                null_profiles=tuple(
                    index for index, item in enumerate(reactions, start=1)
                    if item.kind == "null" and not item.forced_null
                ),
                ambivalent_profiles=tuple(
                    index for index, item in enumerate(reactions, start=1)
                    if item.kind == "ambivalent" and not item.forced_null
                ),
                forced_null_profiles=tuple(
                    index for index, item in enumerate(reactions, start=1)
                    if item.forced_null
                ),
                tensioned_profiles=tuple(
                    index for index, item in enumerate(reactions, start=1)
                    if item.quantum_level > 0
                ),
                quantum_total=sum(item.quantum_level for item in reactions),
            )
        )
    return tuple(result)


def _findings(evaluation: ClinicalProtocolEvaluation) -> tuple[GroundedFinding, ...]:
    result: list[GroundedFinding] = []
    for profile in evaluation.profiles:
        for item in profile.interpretation.findings:
            result.append(
                GroundedFinding(
                    evidence_id=f"EF_P{profile.profile_number:02d}_{item.claim_id}",
                    scope="PROFILE",
                    profile_number=profile.profile_number,
                    finding=item,
                )
            )
    for item in evaluation.series_result.interpretation.findings:
        result.append(
            GroundedFinding(
                evidence_id=f"EF_SERIES_{item.claim_id}",
                scope="SERIES",
                profile_number=None,
                finding=item,
            )
        )
    ids = tuple(item.evidence_id for item in result)
    if len(ids) != len(set(ids)):
        raise ValueError("Clinical evidence contains duplicate finding identities")
    return tuple(result)


def _activation_boundaries(evaluation: ClinicalProtocolEvaluation) -> list[GroundingBoundary]:
    result: list[GroundingBoundary] = []

    def add(scope: str, profile_number: int | None, record) -> None:
        if record.activation_status is ActivationStatus.UNRESOLVED_INPUT:
            detail = ", ".join(record.missing_facts) or "ambiguous or undefined input"
            kind = "UNRESOLVED_INTERPRETATION_INPUT"
        elif record.activation_status is ActivationStatus.BLOCKED_CONTEXT:
            detail = ", ".join(record.missing_context) or "required context absent"
            kind = "BLOCKED_INTERPRETATION_CONTEXT"
        else:
            detail = "source conflict or unresolved source rule"
            kind = "BLOCKED_SOURCE_CONFLICT"
        prefix = f"P{profile_number:02d}" if profile_number is not None else "SERIES"
        result.append(
            GroundingBoundary(
                boundary_id=f"GB_{prefix}_{record.claim_id}_{kind}",
                scope=scope,
                profile_number=profile_number,
                kind=kind,
                subject=record.claim_id,
                reason=detail,
            )
        )

    for profile in evaluation.profiles:
        for record in profile.interpretation.unresolved + profile.interpretation.blocked_context:
            add("PROFILE", profile.profile_number, record)
    for record in (
        evaluation.series_result.interpretation.unresolved
        + evaluation.series_result.interpretation.blocked_context
    ):
        add("SERIES", None, record)
    return result


def _boundaries(evaluation: ClinicalProtocolEvaluation) -> tuple[GroundingBoundary, ...]:
    result = _activation_boundaries(evaluation)
    for calculation in evaluation.series_result.calculations:
        if calculation.state is CalculationState.UNRESOLVED:
            result.append(
                GroundingBoundary(
                    boundary_id=f"GB_CALC_{calculation.name}",
                    scope="SERIES",
                    kind="UNRESOLVED_CALCULATION",
                    subject=calculation.name,
                    reason=calculation.error or "deterministic calculation unresolved",
                )
            )
    ids = tuple(item.boundary_id for item in result)
    if len(ids) != len(set(ids)):
        raise ValueError("Clinical evidence contains duplicate grounding boundaries")
    return tuple(result)


def build_clinical_evidence(evaluation: ClinicalProtocolEvaluation) -> ClinicalEvidence:
    """Build the minimal traceable P3 object without adding clinical inference."""
    if not isinstance(evaluation, ClinicalProtocolEvaluation):
        raise TypeError("Clinical evidence requires a ClinicalProtocolEvaluation")
    return ClinicalEvidence(
        evaluation=evaluation,
        factor_patterns=_factor_patterns(evaluation),
        findings=_findings(evaluation),
        boundaries=_boundaries(evaluation),
    )
