"""Interactive clinician workspace over already-authorized Szondi3 case outputs.

The workspace is deliberately separate from ``ClinicianWorkingReport``. The report
remains a clean export/document contract, while the workspace retains the canonical
``ClinicalCaseRun`` objects and read-only ``ClinicalExploration`` indexes required
for interactive drill-down. No P1 result is recalculated, no P2B claim is activated,
and no additional clinical meaning is introduced here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .clinical_case_runner import ClinicalCaseRun
from .clinical_exploration import ClinicalExploration, FindingTrace, explore_clinical_case
from .clinical_integration import (
    ClinicalIntegration,
    ClinicianContextItem,
    integrate_clinical_case,
)
from .clinician_working_report import (
    ClinicianWorkingReport,
    build_clinician_working_report,
)
from .longitudinal_comparison import LongitudinalCaseRef


@dataclass(frozen=True, slots=True)
class WorkspaceAssessment:
    """One case identity with the canonical run and read-only exploration index."""

    case_id: str
    run: ClinicalCaseRun
    exploration: ClinicalExploration


@dataclass(frozen=True, slots=True)
class ClinicianWorkspace:
    """Interactive product seam for one current case plus ordered history.

    ``integration`` and ``report`` remain the deterministic clinical composition and
    export contracts. ``history`` and ``current`` retain runtime/exploration access
    only for UI navigation and provenance drill-down.
    """

    history: tuple[WorkspaceAssessment, ...]
    current: WorkspaceAssessment
    integration: ClinicalIntegration
    report: ClinicianWorkingReport

    @property
    def assessment_ids(self) -> tuple[str, ...]:
        return tuple(item.case_id for item in self.history) + (self.current.case_id,)

    @property
    def current_exploration(self) -> ClinicalExploration:
        return self.current.exploration

    def assessment(self, case_id: str) -> WorkspaceAssessment:
        """Return one exact workspace assessment without fuzzy identity matching."""
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError("case_id must be a non-empty string")
        matches = tuple(
            item
            for item in self.history + (self.current,)
            if item.case_id == case_id
        )
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate workspace case_id: {case_id}")
        return matches[0]

    def trace_current_finding(
        self,
        claim_id: str,
        *,
        scope: str,
        profile_number: int | None = None,
    ) -> FindingTrace:
        """Trace one active current-case finding through existing exploration data."""
        return self.current.exploration.trace_finding(
            claim_id,
            scope=scope,
            profile_number=profile_number,
        )


def _workspace_assessment(case: LongitudinalCaseRef) -> WorkspaceAssessment:
    return WorkspaceAssessment(
        case_id=case.case_id,
        run=case.run,
        exploration=explore_clinical_case(case.run),
    )


def build_clinician_workspace(
    current: LongitudinalCaseRef,
    *,
    prior_cases: Sequence[LongitudinalCaseRef] = (),
    clinician_context: Sequence[ClinicianContextItem] = (),
    clinician_synthesis: str | None = None,
) -> ClinicianWorkspace:
    """Build the interactive workspace without changing existing case semantics."""
    if not isinstance(current, LongitudinalCaseRef):
        raise TypeError("current must be a LongitudinalCaseRef")

    history_refs = tuple(prior_cases)
    integration = integrate_clinical_case(
        current,
        prior_cases=history_refs,
        clinician_context=clinician_context,
        clinician_synthesis=clinician_synthesis,
    )
    report = build_clinician_working_report(integration)

    history = tuple(_workspace_assessment(item) for item in history_refs)
    current_assessment = _workspace_assessment(current)
    workspace_ids = tuple(item.case_id for item in history) + (current_assessment.case_id,)

    if workspace_ids != integration.assessment_ids:
        raise ValueError("Workspace case ordering diverges from clinical integration")
    if workspace_ids != report.summary.assessment_ids:
        raise ValueError("Workspace case ordering diverges from working report")

    return ClinicianWorkspace(
        history=history,
        current=current_assessment,
        integration=integration,
        report=report,
    )
