"""Clinician-oriented structured output for the first P2B vertical slice.

This module intentionally returns structured findings rather than polished report
prose. A later reporting layer may render these findings, but it must keep their
assertion strength, provenance and anti-inferences visible.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Iterable, Mapping

from .interpretation import (
    ActivationRecord,
    ActivationStatus,
    AssertionMode,
    Fact,
    LifecycleStatus,
    evaluate_catalogue,
)
from .interpretation_catalogue_sublimation_fate import CLAIMS_BY_ID, INITIAL_CLAIMS


@dataclass(frozen=True, slots=True)
class ClinicianFinding:
    claim_id: str
    statement: str
    assertion_mode: AssertionMode
    lifecycle_status: LifecycleStatus
    doctrine_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    support_fact_ids: tuple[str, ...]
    anti_inference_ids: tuple[str, ...]
    anti_inferences: tuple[str, ...]
    source_strength_note: str
    sensitive_domains: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ClinicalInterpretation:
    findings: tuple[ClinicianFinding, ...]
    suppressed: tuple[ActivationRecord, ...]

    @property
    def has_findings(self) -> bool:
        return bool(self.findings)


def _sensitive_domains(claim) -> tuple[str, ...]:
    domains = []
    for name, label in (
        ("hereditary_genetic_content", "hereditary_genetic"),
        ("sexual_content", "sexual"),
        ("pathodiagnostic_content", "pathodiagnostic"),
        ("criminological_content", "criminological"),
    ):
        if getattr(claim, name):
            domains.append(label)
    return tuple(domains)


@lru_cache(maxsize=1)
def _claim_map() -> Mapping[str, Any]:
    return CLAIMS_BY_ID


def interpret_facts(
    facts: Iterable[Fact],
    *,
    production: bool = False,
    claim_ids: Iterable[str] | None = None,
) -> ClinicalInterpretation:
    """Evaluate source-linked claims and expose only auditable clinician findings."""
    fact_tuple = tuple(facts)
    claims = INITIAL_CLAIMS
    if claim_ids is not None:
        selected = frozenset(claim_ids)
        claims = tuple(claim for claim in INITIAL_CLAIMS if claim.claim_id in selected)
    activations = evaluate_catalogue(claims, fact_tuple, production=production)
    findings = []
    suppressed = []
    claims_by_id = _claim_map()
    for activation in activations:
        if activation.status is not ActivationStatus.ACTIVE:
            suppressed.append(activation)
            continue
        claim = claims_by_id[activation.claim_id]
        findings.append(
            ClinicianFinding(
                claim_id=claim.claim_id,
                statement=claim.proposition_text,
                assertion_mode=claim.assertion_mode,
                lifecycle_status=claim.lifecycle_status,
                doctrine_ids=claim.doctrine_ids,
                source_ids=claim.source_ids,
                support_fact_ids=activation.support_fact_ids,
                anti_inference_ids=tuple(item.anti_inference_id for item in claim.anti_inferences),
                anti_inferences=tuple(item.statement for item in claim.anti_inferences),
                source_strength_note=claim.source_strength_note,
                sensitive_domains=_sensitive_domains(claim),
            )
        )
    return ClinicalInterpretation(findings=tuple(findings), suppressed=tuple(suppressed))
