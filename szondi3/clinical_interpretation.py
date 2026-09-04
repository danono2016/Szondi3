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
from .interpretation_catalogue_fate_modifiability import CLAIMS_BY_ID, INITIAL_CLAIMS


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
    suppressed: tuple[ActivationRecord, ...] = ()

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


def _selected_claims(
    claim_ids: Iterable[str] | None,
    facts: tuple[Fact, ...],
):
    if claim_ids is None:
        return INITIAL_CLAIMS

    selected = set(claim_ids)
    unknown = tuple(sorted(item for item in selected if item not in CLAIMS_BY_ID))
    if unknown:
        raise ValueError(f"Unknown P2B claim ids: {', '.join(unknown)}")

    # Series-level method boundaries apply whenever a profile series is present.
    if any(fact.key == "series.profile_count" for fact in facts):
        selected.update(
            (
                "IC_SZONDI_PRIMARY_000079",
                "IC_SZONDI_PRIMARY_000080",
                "IC_SZONDI_PRIMARY_000085",
                "IC_SZONDI_PRIMARY_000087",
            )
        )

    # The Annahme/Angst comparison is a profile-local relation. Route it only when
    # the exact Sch profile evidence needed by its trigger is actually present.
    if any(fact.key == "profile.vector.Sch.base_symbols" for fact in facts):
        selected.add("IC_SZONDI_PRIMARY_000081")

    # Kontaktlosigkeit and Sch/C relation claims are profile-local conjunctions.
    # Route their candidates only when both C and Sch vector facts exist; exact
    # triggers still decide which source-grounded relation, if any, activates.
    fact_keys = {fact.key for fact in facts}
    if {
        "profile.vector.C.base_symbols",
        "profile.vector.Sch.base_symbols",
    }.issubset(fact_keys):
        selected.update(
            (
                "IC_SZONDI_PRIMARY_000082",
                "IC_SZONDI_PRIMARY_000083",
                "IC_SZONDI_PRIMARY_000084",
            )
        )

    # The ethical/moral dilemma relation is likewise a profile-local conjunction.
    # Its trigger enumerates e± OR hy± exactly, so routing only requires that both
    # P and Sch vector evidence are present; the catalogue decides activation.
    if {
        "profile.vector.P.base_symbols",
        "profile.vector.Sch.base_symbols",
    }.issubset(fact_keys):
        selected.add("IC_SZONDI_PRIMARY_000086")

    return tuple(claim for claim in INITIAL_CLAIMS if claim.claim_id in selected)


def interpret_facts(
    facts: Iterable[Fact],
    *,
    context: Mapping[str, Any] | None = None,
    production: bool = False,
    claim_ids: Iterable[str] | None = None,
) -> ClinicalInterpretation:
    """Evaluate source-linked claims and return auditable clinician-facing findings.

    ``claim_ids`` permits an orchestration layer to evaluate only claims whose
    evidence scope is actually present. ``production=False`` remains an explicit
    preview/review surface; production mode admits only APPROVED claims.
    """
    fact_tuple = tuple(facts)
    claims = _selected_claims(claim_ids, fact_tuple)
    activations = evaluate_catalogue(
        claims,
        fact_tuple,
        context=context,
        production=production,
    )

    findings = []
    unresolved = []
    blocked_context = []
    suppressed = []
    claims_by_id = _claim_map()

    for activation in activations:
        if activation.activation_status is ActivationStatus.ACTIVE:
            claim = claims_by_id[activation.claim_id]
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
                        for fact in activation.matched_facts
                        if fact.fact_id is not None
                    ),
                    anti_inference_ids=tuple(
                        item.anti_inference_id for item in activation.anti_inferences
                    ),
                    anti_inferences=tuple(
                        item.prohibited_conclusion for item in activation.anti_inferences
                    ),
                    source_strength_note=claim.source_strength_note,
                    sensitive_domains=_sensitive_domains(claim),
                )
            )
            continue

        suppressed.append(activation)
        if activation.activation_status is ActivationStatus.UNRESOLVED_INPUT:
            unresolved.append(activation)
        elif activation.activation_status in {
            ActivationStatus.BLOCKED_CONTEXT,
            ActivationStatus.BLOCKED_SOURCE_CONFLICT,
        }:
            blocked_context.append(activation)

    return ClinicalInterpretation(
        findings=tuple(findings),
        unresolved=tuple(unresolved),
        blocked_context=tuple(blocked_context),
        production_mode=production,
        suppressed=tuple(suppressed),
    )
