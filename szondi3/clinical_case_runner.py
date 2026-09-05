"""Minimal public orchestration entry-point for one administered clinical case."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_pipeline import (
    AdministeredClinicalEvaluation,
    AdministeredTestRecord,
    evaluate_administered_tests,
)
from .clinical_release import (
    AdministeredClinicalEvidencePacket,
    AuditedClinicalRelease,
    build_administered_clinical_evidence_packet,
    build_audited_clinical_release,
)
from .clinical_report import ClinicalReport


@dataclass(frozen=True, slots=True)
class ClinicalCaseRun:
    """Canonical outputs produced by the existing clinical runtime contracts."""

    evaluation: AdministeredClinicalEvaluation
    report: ClinicalReport
    evidence_packet: AdministeredClinicalEvidencePacket
    release: AuditedClinicalRelease


def run_clinical_case(
    records: Iterable[AdministeredTestRecord],
    *,
    git_commit_sha: str,
    synthesis_contract_version: str,
    synthesis_model: str,
) -> ClinicalCaseRun:
    """Run a valid administered case through evaluation, report, evidence and release."""
    evaluation = evaluate_administered_tests(records, production=True)
    report = evaluation.build_report()
    evidence_packet = build_administered_clinical_evidence_packet(evaluation)
    release = build_audited_clinical_release(
        evidence_packet,
        git_commit_sha=git_commit_sha,
        synthesis_contract_version=synthesis_contract_version,
        synthesis_model=synthesis_model,
    )
    return ClinicalCaseRun(
        evaluation=evaluation,
        report=report,
        evidence_packet=evidence_packet,
        release=release,
    )
