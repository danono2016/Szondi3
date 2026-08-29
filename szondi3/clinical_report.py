"""Structured clinician report built from a ``ClinicalProtocolEvaluation``.

The report layer is deliberately conservative. It organizes what the deterministic
and executable-interpretation layers already know; it does not manufacture a
clinical diagnosis, resolve ambiguity, or write a therapist's synthesis.

The resulting object is suitable for a UI, JSON export, or later document renderer
because calculations, Szondian findings, limitations, unresolved states, and the
manual clinician-authored synthesis slot remain separate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
from enum import Enum
from fractions import Fraction
from typing import Any

from .clinical_protocol import CalculationState, ClinicalProtocolEvaluation
from .interpretation import ActivationStatus


@dataclass(frozen=True, slots=True)
class ReportHeader:
    profile_count: int
    production_mode: bool
    interpretation_release_state: str


@dataclass(frozen=True, slots=True)
class ObservedFactor:
    factor: str
    symbol: str
    sympathetic: int
    unsympathetic: int
    quantum_level: int
    forced_null: bool


@dataclass(frozen=True, slots=True)
class ObservedVector:
    vector: str
    symbols: tuple[str, str]


@dataclass(frozen=True, slots=True)
class ProfileObservation:
    profile_number: int
    factors: tuple[ObservedFactor, ...]
    vectors: tuple[ObservedVector, ...]


@dataclass(frozen=True, slots=True)
class ReportCalculation:
    name: str
    state: str
    value: Any
    note: str | None


@dataclass(frozen=True, slots=True)
class ReportFinding:
    scope: str
    profile_number: int | None
    claim_id: str
    statement: str
    assertion_mode: str
    lifecycle_status: str
    doctrine_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    support_fact_ids: tuple[str, ...]
    anti_inferences: tuple[str, ...]
    source_strength_note: str
    sensitive_domains: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReportUncertainty:
    scope: str
    kind: str
    message: str
    profile_number: int | None = None
    calculation_name: str | None = None
    claim_id: str | None = None


@dataclass(frozen=True, slots=True)
class TherapistSynthesis:
    """Explicitly manual area; no automatic clinical conclusion is inserted here."""

    text: str | None
    authorship: str = "MANUAL_CLINICIAN_INPUT_ONLY"


@dataclass(frozen=True, slots=True)
class ClinicalReport:
    header: ReportHeader
    observations: tuple[ProfileObservation, ...]
    calculations: tuple[ReportCalculation, ...]
    findings: tuple[ReportFinding, ...]
    uncertainties: tuple[ReportUncertainty, ...]
    therapist_synthesis: TherapistSynthesis

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe representation without losing exact fractions."""
        return _json_safe(self)


def _json_safe(value: Any) -> Any:
    if isinstance(value, Fraction):
        return {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "exact": str(value),
        }
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _json_safe(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    # P1 outputs are frozen dataclasses in the current engine; keep a guarded
    # fallback so an unfamiliar value is visible rather than silently dropped.
    return repr(value)


def _observations(evaluation: ClinicalProtocolEvaluation) -> tuple[ProfileObservation, ...]:
    result = []
    for number, profile in enumerate(evaluation.series.profiles, start=1):
        result.append(
            ProfileObservation(
                profile_number=number,
                factors=tuple(
                    ObservedFactor(
                        factor=item.factor,
                        symbol=item.symbol,
                        sympathetic=item.sympathetic,
                        unsympathetic=item.unsympathetic,
                        quantum_level=item.quantum_level,
                        forced_null=item.forced_null,
                    )
                    for item in profile.factors
                ),
                vectors=tuple(
                    ObservedVector(vector=item.name, symbols=item.symbols)
                    for item in profile.vectors
                ),
            )
        )
    return tuple(result)


def _calculations(evaluation: ClinicalProtocolEvaluation) -> tuple[ReportCalculation, ...]:
    return tuple(
        ReportCalculation(
            name=item.name,
            state=item.state.value,
            value=item.value if item.state is CalculationState.AVAILABLE else None,
            note=item.error,
        )
        for item in evaluation.series_result.calculations
    )


def _finding(scope: str, profile_number: int | None, item) -> ReportFinding:
    return ReportFinding(
        scope=scope,
        profile_number=profile_number,
        claim_id=item.claim_id,
        statement=item.statement,
        assertion_mode=item.assertion_mode.value,
        lifecycle_status=item.lifecycle_status.value,
        doctrine_ids=item.doctrine_ids,
        source_ids=item.source_ids,
        support_fact_ids=item.support_fact_ids,
        anti_inferences=item.anti_inferences,
        source_strength_note=item.source_strength_note,
        sensitive_domains=item.sensitive_domains,
    )


def _findings(evaluation: ClinicalProtocolEvaluation) -> tuple[ReportFinding, ...]:
    result: list[ReportFinding] = []
    for profile in evaluation.profiles:
        result.extend(
            _finding("PROFILE", profile.profile_number, item)
            for item in profile.interpretation.findings
        )
    result.extend(
        _finding("SERIES", None, item)
        for item in evaluation.series_result.interpretation.findings
    )
    return tuple(result)


def _activation_uncertainty(scope: str, profile_number: int | None, record) -> ReportUncertainty:
    missing_facts = ", ".join(record.missing_facts)
    missing_context = ", ".join(record.missing_context)
    if record.activation_status is ActivationStatus.UNRESOLVED_INPUT:
        detail = missing_facts or "input ambiguu/nedefinit"
        message = f"Claim-ul nu poate fi evaluat: {detail}."
        kind = "UNRESOLVED_INTERPRETATION_INPUT"
    elif record.activation_status is ActivationStatus.BLOCKED_CONTEXT:
        detail = missing_context or "context clinic necesar absent"
        message = f"Claim-ul este blocat de contextul lipsă: {detail}."
        kind = "BLOCKED_INTERPRETATION_CONTEXT"
    else:
        message = "Claim-ul este blocat de un conflict/nivel de sursă nerezolvat."
        kind = "BLOCKED_SOURCE_CONFLICT"
    return ReportUncertainty(
        scope=scope,
        profile_number=profile_number,
        kind=kind,
        message=message,
        claim_id=record.claim_id,
    )


def _uncertainties(evaluation: ClinicalProtocolEvaluation) -> tuple[ReportUncertainty, ...]:
    result: list[ReportUncertainty] = []

    for calculation in evaluation.series_result.calculations:
        if calculation.state is CalculationState.UNRESOLVED:
            result.append(
                ReportUncertainty(
                    scope="SERIES",
                    kind="UNRESOLVED_CALCULATION",
                    message=calculation.error or "Calcul determinist nerezolvat.",
                    calculation_name=calculation.name,
                )
            )

    for profile in evaluation.profiles:
        interpretation = profile.interpretation
        result.extend(
            _activation_uncertainty("PROFILE", profile.profile_number, item)
            for item in interpretation.unresolved
        )
        result.extend(
            _activation_uncertainty("PROFILE", profile.profile_number, item)
            for item in interpretation.blocked_context
        )

    interpretation = evaluation.series_result.interpretation
    result.extend(
        _activation_uncertainty("SERIES", None, item)
        for item in interpretation.unresolved
    )
    result.extend(
        _activation_uncertainty("SERIES", None, item)
        for item in interpretation.blocked_context
    )
    return tuple(result)


def build_clinical_report(
    evaluation: ClinicalProtocolEvaluation,
    *,
    therapist_synthesis: str | None = None,
) -> ClinicalReport:
    """Build a structured report without generating therapist-level conclusions.

    ``therapist_synthesis`` is accepted only as explicit caller-supplied clinician
    text. When omitted, the synthesis slot is deliberately empty.
    """
    if not isinstance(evaluation, ClinicalProtocolEvaluation):
        raise TypeError("Clinical report requires a ClinicalProtocolEvaluation")

    release_state = (
        "PRODUCTION_APPROVED_CLAIMS_ONLY"
        if evaluation.production_mode
        else "REVIEW_PREVIEW_NOT_FOR_AUTOMATIC_CLINICAL_RELEASE"
    )
    return ClinicalReport(
        header=ReportHeader(
            profile_count=evaluation.profile_count,
            production_mode=evaluation.production_mode,
            interpretation_release_state=release_state,
        ),
        observations=_observations(evaluation),
        calculations=_calculations(evaluation),
        findings=_findings(evaluation),
        uncertainties=_uncertainties(evaluation),
        therapist_synthesis=TherapistSynthesis(text=therapist_synthesis),
    )
