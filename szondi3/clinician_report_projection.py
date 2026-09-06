"""Deterministic clinician-facing projection of an executed clinical case.

This layer reorganizes existing ClinicalReport, evidence packet, activation, and
release data. It does not calculate P1, activate claims, add interpretation, or use
AI synthesis. Projection is emitted only after the read-only structural exploration
audit proves exact cross-layer traceability.
"""

from __future__ import annotations

from dataclasses import dataclass

from .clinical_case_runner import ClinicalCaseRun
from .clinical_evidence_packet import (
    CanonicalDoctrineEvidence,
    FactorSeriesEvidence,
    VectorSeriesEvidence,
)
from .clinical_exploration_audit import (
    ClinicalExplorationAudit,
    audit_clinical_exploration,
)
from .clinical_release import (
    ClinicalReleaseManifest,
    ExperimentalComplementEvidence,
)
from .clinical_report import (
    ProfileObservation,
    ReportCalculation,
    ReportFinding,
    ReportHeader,
    ReportUncertainty,
)
from .interpretation import ActivationRecord, ActivationStatus


@dataclass(frozen=True, slots=True)
class FormalReportSection:
    header: ReportHeader
    observations: tuple[ProfileObservation, ...]
    calculations: tuple[ReportCalculation, ...]
    factor_series: tuple[FactorSeriesEvidence, ...]
    vector_series: tuple[VectorSeriesEvidence, ...]


@dataclass(frozen=True, slots=True)
class FindingBoundary:
    scope: str
    profile_number: int | None
    claim_id: str
    assertion_mode: str
    statement: str
    anti_inference_ids: tuple[str, ...]
    anti_inferences: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SuppressedClaim:
    scope: str
    profile_number: int | None
    claim_id: str
    activation_status: str
    missing_facts: tuple[str, ...]
    missing_context: tuple[str, ...]
    qualifications: tuple[str, ...]
    provenance_trace: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvaluationStatusSection:
    unresolved: tuple[ReportUncertainty, ...]
    blocked: tuple[ReportUncertainty, ...]
    suppressed: tuple[SuppressedClaim, ...]


@dataclass(frozen=True, slots=True)
class ExperimentalComplementSection:
    findings: tuple[ReportFinding, ...]
    uncertainties: tuple[ReportUncertainty, ...]
    evidence: tuple[ExperimentalComplementEvidence, ...]


@dataclass(frozen=True, slots=True)
class ClinicianReportProjection:
    formal: FormalReportSection
    findings: tuple[ReportFinding, ...]
    limits_and_anti_inferences: tuple[FindingBoundary, ...]
    provenance: tuple[CanonicalDoctrineEvidence, ...]
    experimental_complement: ExperimentalComplementSection
    status: EvaluationStatusSection
    release: ClinicalReleaseManifest
    audit: ClinicalExplorationAudit


def _boundary(finding: ReportFinding) -> FindingBoundary:
    return FindingBoundary(
        scope=finding.scope,
        profile_number=finding.profile_number,
        claim_id=finding.claim_id,
        assertion_mode=finding.assertion_mode,
        statement=finding.statement,
        anti_inference_ids=finding.anti_inference_ids,
        anti_inferences=finding.anti_inferences,
    )


def _suppressed(
    scope: str,
    profile_number: int | None,
    records: tuple[ActivationRecord, ...],
) -> tuple[SuppressedClaim, ...]:
    return tuple(
        SuppressedClaim(
            scope=scope,
            profile_number=profile_number,
            claim_id=record.claim_id,
            activation_status=record.activation_status.value,
            missing_facts=record.missing_facts,
            missing_context=record.missing_context,
            qualifications=record.qualifications,
            provenance_trace=record.provenance_trace,
        )
        for record in records
        if record.activation_status is ActivationStatus.INACTIVE
    )


def _suppressed_claims(run: ClinicalCaseRun) -> tuple[SuppressedClaim, ...]:
    result: list[SuppressedClaim] = []
    evaluation = run.evaluation.clinical_evaluation
    for profile in evaluation.profiles:
        result.extend(
            _suppressed(
                "PROFILE",
                profile.profile_number,
                profile.interpretation.suppressed,
            )
        )
    result.extend(
        _suppressed(
            "SERIES",
            None,
            evaluation.series_result.interpretation.suppressed,
        )
    )
    for complement in run.evaluation.complement_profiles:
        result.extend(
            _suppressed(
                "EXPERIMENTAL_COMPLEMENT",
                complement.test_number,
                complement.interpretation.suppressed,
            )
        )
    return tuple(result)


def project_clinician_report(run: ClinicalCaseRun) -> ClinicianReportProjection:
    """Project one structurally audited case into clinician-facing sections."""
    if not isinstance(run, ClinicalCaseRun):
        raise TypeError("Clinician report projection requires a ClinicalCaseRun")

    audit = audit_clinical_exploration(run)
    report = run.report
    packet = run.evidence_packet
    complement_findings = tuple(
        finding
        for finding in report.findings
        if finding.scope == "EXPERIMENTAL_COMPLEMENT"
    )
    foreground_findings = tuple(
        finding
        for finding in report.findings
        if finding.scope != "EXPERIMENTAL_COMPLEMENT"
    )
    complement_uncertainties = tuple(
        item
        for item in report.uncertainties
        if item.scope == "EXPERIMENTAL_COMPLEMENT"
    )
    ordinary_uncertainties = tuple(
        item
        for item in report.uncertainties
        if item.scope != "EXPERIMENTAL_COMPLEMENT"
    )
    unresolved = tuple(
        item for item in ordinary_uncertainties if item.kind.startswith("UNRESOLVED_")
    )
    blocked = tuple(
        item for item in ordinary_uncertainties if item.kind.startswith("BLOCKED_")
    )
    boundaries = tuple(
        _boundary(finding)
        for finding in report.findings
        if finding.assertion_mode == "LIMITATION" or finding.anti_inferences
    )

    return ClinicianReportProjection(
        formal=FormalReportSection(
            header=report.header,
            observations=report.observations,
            calculations=report.calculations,
            factor_series=packet.factor_series,
            vector_series=packet.vector_series,
        ),
        findings=foreground_findings,
        limits_and_anti_inferences=boundaries,
        provenance=packet.canonical_evidence,
        experimental_complement=ExperimentalComplementSection(
            findings=complement_findings,
            uncertainties=complement_uncertainties,
            evidence=packet.experimental_complements,
        ),
        status=EvaluationStatusSection(
            unresolved=unresolved,
            blocked=blocked,
            suppressed=_suppressed_claims(run),
        ),
        release=run.release.manifest,
        audit=audit,
    )
