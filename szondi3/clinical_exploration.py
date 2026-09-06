"""Read-only clinician exploration over one canonical Szondi3 case run.

This module adds no calculation, doctrine, executable claim, or narrative meaning.
It only indexes already-produced P1 facts/calculations, P2B findings, uncertainty
states, activation records, and canonical doctrine evidence so a clinician-facing
surface can navigate the existing case without reconstructing relationships.
"""

from __future__ import annotations

from dataclasses import dataclass

from .clinical_case_runner import ClinicalCaseRun
from .clinical_evidence_packet import CanonicalDoctrineEvidence
from .clinical_report import (
    ProfileObservation,
    ReportCalculation,
    ReportFinding,
    ReportUncertainty,
)
from .interpretation import ActivationRecord, ActivationStatus, Fact


@dataclass(frozen=True, slots=True)
class ProfileExploration:
    profile_number: int
    observation: ProfileObservation
    facts: tuple[Fact, ...]
    findings: tuple[ReportFinding, ...]
    uncertainties: tuple[ReportUncertainty, ...]
    suppressed: tuple[ActivationRecord, ...]


@dataclass(frozen=True, slots=True)
class SeriesExploration:
    facts: tuple[Fact, ...]
    calculations: tuple[ReportCalculation, ...]
    findings: tuple[ReportFinding, ...]
    uncertainties: tuple[ReportUncertainty, ...]
    suppressed: tuple[ActivationRecord, ...]


@dataclass(frozen=True, slots=True)
class FindingTrace:
    finding: ReportFinding
    support_facts: tuple[Fact, ...]
    doctrine_evidence: tuple[CanonicalDoctrineEvidence, ...]


@dataclass(frozen=True, slots=True)
class ClinicalExploration:
    """Navigation index over outputs that already exist in ``ClinicalCaseRun``."""

    run: ClinicalCaseRun

    def profile(self, profile_number: int) -> ProfileExploration:
        if not isinstance(profile_number, int) or isinstance(profile_number, bool):
            raise TypeError("profile_number must be an integer")
        if profile_number < 1 or profile_number > self.run.report.header.profile_count:
            raise KeyError(f"Unknown profile number: {profile_number}")

        evaluation_profile = self.run.evaluation.clinical_evaluation.profiles[
            profile_number - 1
        ]
        observation = self.run.report.observations[profile_number - 1]
        if evaluation_profile.profile_number != profile_number:
            raise ValueError("Clinical evaluation profile ordering is inconsistent")
        if observation.profile_number != profile_number:
            raise ValueError("Clinical report profile ordering is inconsistent")

        findings = tuple(
            item
            for item in self.run.report.findings
            if item.scope == "PROFILE" and item.profile_number == profile_number
        )
        uncertainties = tuple(
            item
            for item in self.run.report.uncertainties
            if item.scope == "PROFILE" and item.profile_number == profile_number
        )
        suppressed = tuple(
            item
            for item in evaluation_profile.interpretation.suppressed
            if item.activation_status is ActivationStatus.INACTIVE
        )
        return ProfileExploration(
            profile_number=profile_number,
            observation=observation,
            facts=evaluation_profile.facts,
            findings=findings,
            uncertainties=uncertainties,
            suppressed=suppressed,
        )

    def series(self) -> SeriesExploration:
        series_result = self.run.evaluation.clinical_evaluation.series_result
        findings = tuple(
            item for item in self.run.report.findings if item.scope == "SERIES"
        )
        uncertainties = tuple(
            item for item in self.run.report.uncertainties if item.scope == "SERIES"
        )
        suppressed = tuple(
            item
            for item in series_result.interpretation.suppressed
            if item.activation_status is ActivationStatus.INACTIVE
        )
        return SeriesExploration(
            facts=series_result.facts,
            calculations=self.run.report.calculations,
            findings=findings,
            uncertainties=uncertainties,
            suppressed=suppressed,
        )

    def trace_finding(
        self,
        claim_id: str,
        *,
        scope: str,
        profile_number: int | None = None,
    ) -> FindingTrace:
        """Trace one active finding back to its exact runtime facts and doctrine.

        The method never searches by textual similarity. Every support identity must
        resolve exactly in the same runtime scope, otherwise exploration fails closed.
        """
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValueError("claim_id must be a non-empty string")
        if scope not in {"PROFILE", "SERIES"}:
            raise ValueError("Exploration tracing currently supports PROFILE or SERIES")
        if scope == "PROFILE":
            if not isinstance(profile_number, int) or isinstance(profile_number, bool):
                raise ValueError("PROFILE trace requires a positive profile_number")
            source_facts = self.profile(profile_number).facts
        else:
            if profile_number is not None:
                raise ValueError("SERIES trace must not carry profile_number")
            source_facts = self.series().facts

        matches = tuple(
            item
            for item in self.run.report.findings
            if item.claim_id == claim_id
            and item.scope == scope
            and item.profile_number == profile_number
        )
        if len(matches) != 1:
            raise KeyError(
                f"Unknown or duplicate active finding: {claim_id} @ {scope}/{profile_number}"
            )
        finding = matches[0]

        fact_by_id = {
            fact.fact_id: fact
            for fact in source_facts
            if fact.fact_id is not None
        }
        if len(fact_by_id) != sum(
            1 for fact in source_facts if fact.fact_id is not None
        ):
            raise ValueError("Duplicate runtime fact identity in exploration scope")
        missing_fact_ids = tuple(
            fact_id for fact_id in finding.support_fact_ids if fact_id not in fact_by_id
        )
        if missing_fact_ids:
            raise ValueError(
                "Finding support fact is absent from runtime scope: "
                + ", ".join(missing_fact_ids)
            )
        support_facts = tuple(fact_by_id[fact_id] for fact_id in finding.support_fact_ids)

        doctrine_by_id = {
            item.doctrine_id: item for item in self.run.evidence_packet.canonical_evidence
        }
        if len(doctrine_by_id) != len(self.run.evidence_packet.canonical_evidence):
            raise ValueError("Duplicate canonical doctrine identity in evidence packet")
        missing_doctrine_ids = tuple(
            doctrine_id
            for doctrine_id in finding.doctrine_ids
            if doctrine_id not in doctrine_by_id
        )
        if missing_doctrine_ids:
            raise ValueError(
                "Finding doctrine is absent from canonical evidence packet: "
                + ", ".join(missing_doctrine_ids)
            )
        doctrine_evidence = tuple(
            doctrine_by_id[doctrine_id] for doctrine_id in finding.doctrine_ids
        )
        for evidence in doctrine_evidence:
            if evidence.source_id not in finding.source_ids:
                raise ValueError(
                    "Canonical doctrine source does not match finding provenance: "
                    f"{evidence.doctrine_id} -> {evidence.source_id}"
                )

        return FindingTrace(
            finding=finding,
            support_facts=support_facts,
            doctrine_evidence=doctrine_evidence,
        )


def explore_clinical_case(run: ClinicalCaseRun) -> ClinicalExploration:
    """Build a deterministic exploration index without changing the case run."""
    if not isinstance(run, ClinicalCaseRun):
        raise TypeError("Clinical exploration requires a ClinicalCaseRun")
    if run.evidence_packet.report != run.report:
        raise ValueError("Clinical case report and evidence packet report diverge")
    if run.release.evidence_packet != run.evidence_packet:
        raise ValueError("Clinical case evidence packet and audited release diverge")
    return ClinicalExploration(run=run)
