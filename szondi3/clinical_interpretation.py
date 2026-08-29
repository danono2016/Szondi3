"""Clinician-oriented structured output for the first P2B vertical slice.

This module intentionally returns structured findings rather than polished report
prose. A later reporting layer may render these findings, but it must keep their
assertion strength, provenance and anti-inferences visible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .interpretation import (
    ActivationRecord,
    ActivationStatus,
    AssertionMode,
    Fact,
    LifecycleStatus,
    evaluate_catalogue,
)
from .interpretation_catalogue import CLAIMS_BY_ID, INITIAL_CLAIMS


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
    unresolved: tuple[ActivationRecord, ...]
    blocked_context: tuple[ActivationRecord, ...]
    production_mode: bool


def _domains(claim) -> tuple[str, ...]:
    flags = (
        ("sexual", claim.sexual_content),
        ("pathodiagnostic", claim.pathodiagnostic_content),
        ("criminological", claim.criminological_content),
        ("hereditary_genetic", claim.hereditary_genetic_content),
    )
    return tuple(name for name, enabled in flags if enabled)


def _selected_claims(claim_ids: Iterable[str] | None):
    if claim_ids is None:
        return INITIAL_CLAIMS
    requested = tuple(claim_ids)
    unknown = tuple(item for item in requested if item not in CLAIMS_BY_ID)
    if unknown:
        raise ValueError(f"Unknown P2B claim ids: {', '.join(unknown)}")
    return tuple(CLAIMS_BY_ID[item] for item in requested)


def interpret_facts(
    facts: Iterable[Fact],
    *,
    context: Mapping[str, Any] | None = None,
    production: bool = False,
    claim_ids: Iterable[str] | None = None,
) -> ClinicalInterpretation:
    """Evaluate source-linked claims and return auditable clinician-facing findings.

    ``claim_ids`` permits an orchestration layer to evaluate only claims whose
    evidence scope is actually present (for example profile-local versus series-
    level claims). This is a routing mechanism, not a semantic filter: claim
    definitions and their trigger conditions remain unchanged.

    ``production=False`` is an explicit preview/review surface and can expose
    FORMALIZATION_REVIEWED claims. ``production=True`` admits only APPROVED claims;
    the initial tranche intentionally has none until clinician review occurs.
    """
    selected = _selected_claims(claim_ids)
    records = evaluate_catalogue(
        selected,
        tuple(facts),
        context=context,
        production=production,
    )
    findings = []
    unresolved = []
    blocked_context = []
    for record in records:
        if record.activation_status is ActivationStatus.ACTIVE:
            claim = CLAIMS_BY_ID[record.claim_id]
            findings.append(
                ClinicianFinding(
                    claim_id=claim.claim_id,
                    statement=claim.claim,
                    assertion_mode=claim.assertion_mode,
                    lifecycle_status=claim.status,
                    doctrine_ids=claim.doctrine_ids,
                    source_ids=claim.source_ids,
                    support_fact_ids=tuple(
                        fact.fact_id
                        for fact in record.matched_facts
                        if fact.fact_id is not None
                    ),
                    anti_inference_ids=tuple(
                        item.anti_inference_id for item in record.anti_inferences
                    ),
                    anti_inferences=tuple(
                        item.prohibited_conclusion for item in record.anti_inferences
                    ),
                    source_strength_note=claim.source_strength_note,
                    sensitive_domains=_domains(claim),
                )
            )
        elif record.activation_status is ActivationStatus.UNRESOLVED_INPUT:
            unresolved.append(record)
        elif record.activation_status in {
            ActivationStatus.BLOCKED_CONTEXT,
            ActivationStatus.BLOCKED_SOURCE_CONFLICT,
        }:
            blocked_context.append(record)

    return ClinicalInterpretation(
        findings=tuple(findings),
        unresolved=tuple(unresolved),
        blocked_context=tuple(blocked_context),
        production_mode=production,
    )
