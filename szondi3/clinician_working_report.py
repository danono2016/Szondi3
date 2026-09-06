"""Deterministic clinician working report over ``ClinicalIntegration``.

The working report is the final structured product seam in the current roadmap.
It exposes current Szondi3 findings, formal results, limitations, longitudinal
comparisons, clinician-authored context/synthesis, provenance and release metadata
without generating new clinical meaning or using AI synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from fractions import Fraction
from typing import Any

from .clinical_integration import (
    ClinicalIntegration,
    ClinicianAuthoredSynthesis,
    ClinicianContextItem,
    IntegratedAssessment,
)
from .clinical_exploration_audit import ClinicalExplorationAudit
from .clinical_evidence_packet import CanonicalDoctrineEvidence
from .clinical_release import ClinicalReleaseManifest
from .clinician_report_projection import (
    EvaluationStatusSection,
    ExperimentalComplementSection,
    FindingBoundary,
    FormalReportSection,
)
from .clinical_report import ReportFinding
from .longitudinal_comparison import CaseComparisonResult


@dataclass(frozen=True, slots=True)
class WorkingReportSummary:
    current_case_id: str
    assessment_ids: tuple[str, ...]
    profile_count: int
    finding_count: int
    unresolved_count: int
    blocked_count: int
    longitudinal_comparison_count: int
    comparability_issue_count: int
    interpretation_release_state: str
    clinician_context_count: int
    clinician_synthesis_authorship: str


@dataclass(frozen=True, slots=True)
class ClinicianWorkingReport:
    """Structured clinician-facing report ready for UI/export rendering."""

    summary: WorkingReportSummary
    historical_assessments: tuple[IntegratedAssessment, ...]
    formal: FormalReportSection
    findings: tuple[ReportFinding, ...]
    limits_and_anti_inferences: tuple[FindingBoundary, ...]
    status: EvaluationStatusSection
    experimental_complement: ExperimentalComplementSection
    longitudinal: tuple[CaseComparisonResult, ...]
    clinician_context: tuple[ClinicianContextItem, ...]
    clinician_synthesis: ClinicianAuthoredSynthesis
    provenance: tuple[CanonicalDoctrineEvidence, ...]
    release: ClinicalReleaseManifest
    technical_audit: ClinicalExplorationAudit

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-safe representation for UI/export layers."""
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
    if isinstance(value, (set, frozenset)):
        return [_json_safe(item) for item in sorted(value, key=repr)]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def build_clinician_working_report(
    integration: ClinicalIntegration,
) -> ClinicianWorkingReport:
    """Project one clinical integration workspace into the working-report contract.

    No field is recalculated or semantically reinterpreted. Longitudinal
    comparability issues remain visible; clinician context and synthesis remain
    explicitly authored outside the Szondi evidence chain.
    """
    if not isinstance(integration, ClinicalIntegration):
        raise TypeError("Working report requires a ClinicalIntegration")

    current = integration.current.projection
    comparability_issue_count = sum(
        len(item.comparability_issues) for item in integration.longitudinal
    )

    return ClinicianWorkingReport(
        summary=WorkingReportSummary(
            current_case_id=integration.current.case_id,
            assessment_ids=integration.assessment_ids,
            profile_count=current.formal.header.profile_count,
            finding_count=len(current.findings),
            unresolved_count=len(current.status.unresolved),
            blocked_count=len(current.status.blocked),
            longitudinal_comparison_count=len(integration.longitudinal),
            comparability_issue_count=comparability_issue_count,
            interpretation_release_state=current.formal.header.interpretation_release_state,
            clinician_context_count=len(integration.clinician_context),
            clinician_synthesis_authorship=integration.clinician_synthesis.authorship,
        ),
        historical_assessments=integration.history,
        formal=current.formal,
        findings=current.findings,
        limits_and_anti_inferences=current.limits_and_anti_inferences,
        status=current.status,
        experimental_complement=current.experimental_complement,
        longitudinal=integration.longitudinal,
        clinician_context=integration.clinician_context,
        clinician_synthesis=integration.clinician_synthesis,
        provenance=current.provenance,
        release=current.release,
        technical_audit=current.audit,
    )
