"""Minimal P4 integration layer for grounded Szondian synthesis.

P4 may organize and relate P3 evidence, but it may not manufacture convergence,
causality, or certainty.  The first implementation therefore exposes only four
bounded relation kinds and intentionally has no ``CAUSES`` relation.

``ClinicalIntegration.to_grounding_payload`` is the direct downstream contract
for a future narrative model.  No separate RAG, graph, or narrative-packet
subsystem is required to establish the first grounded clinical vertical slice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .clinical_evidence import ClinicalEvidence, build_clinical_evidence
from .clinical_protocol import ClinicalProtocolEvaluation


class RelationKind(str, Enum):
    COEXISTENCE = "COEXISTENCE"
    CONTRAST = "CONTRAST"
    LONGITUDINAL_CHANGE = "LONGITUDINAL_CHANGE"
    QUALIFICATION = "QUALIFICATION"


@dataclass(frozen=True, slots=True)
class IntegrationRelation:
    """One explicit, support-addressed relation among already grounded evidence."""

    relation_id: str
    kind: RelationKind
    support_ids: tuple[str, ...]
    statement: str

    def __post_init__(self) -> None:
        if not self.relation_id:
            raise ValueError("Integration relation requires a stable relation_id")
        if not self.support_ids:
            raise ValueError("Integration relation requires at least one support id")
        if not self.statement:
            raise ValueError("Integration relation requires an explicit bounded statement")


@dataclass(frozen=True, slots=True)
class ClinicalIntegration:
    """P4 object consumed directly by downstream narrative rendering."""

    evidence: ClinicalEvidence
    relations: tuple[IntegrationRelation, ...]

    def __post_init__(self) -> None:
        relation_ids = tuple(item.relation_id for item in self.relations)
        if len(relation_ids) != len(set(relation_ids)):
            raise ValueError("Clinical integration contains duplicate relation identities")

        available = set(self.evidence.support_ids)
        for relation in self.relations:
            orphan = tuple(item for item in relation.support_ids if item not in available)
            if orphan:
                raise ValueError(
                    f"Integration relation {relation.relation_id} has orphan support ids: "
                    + ", ".join(orphan)
                )

    def to_grounding_payload(self) -> dict:
        """Return the compact case-specific contract for a narrative model.

        This payload contains only P3/P4 material already authorized by Szondi3:
        deterministic series observations, activated P2B findings with provenance,
        explicit fail-closed boundaries, and typed integration relations.  A model
        receiving this object has no need to recount the raw series or retrieve
        doctrine on its own.
        """
        return {
            "schema_version": 1,
            "profile_count": self.evidence.evaluation.profile_count,
            "production_mode": self.evidence.evaluation.production_mode,
            "factor_patterns": [
                {
                    "pattern_id": item.pattern_id,
                    "factor": item.factor,
                    "symbols": list(item.symbols),
                    "base_symbols": list(item.base_symbols),
                    "positive_profiles": list(item.positive_profiles),
                    "negative_profiles": list(item.negative_profiles),
                    "null_profiles": list(item.null_profiles),
                    "ambivalent_profiles": list(item.ambivalent_profiles),
                    "forced_null_profiles": list(item.forced_null_profiles),
                    "tensioned_profiles": list(item.tensioned_profiles),
                    "quantum_total": item.quantum_total,
                    "transitions": [list(change) for change in item.transitions],
                }
                for item in self.evidence.factor_patterns
            ],
            "findings": [
                {
                    "evidence_id": item.evidence_id,
                    "scope": item.scope,
                    "profile_number": item.profile_number,
                    "claim_id": item.finding.claim_id,
                    "statement": item.finding.statement,
                    "assertion_mode": item.finding.assertion_mode.value,
                    "lifecycle_status": item.finding.lifecycle_status.value,
                    "doctrine_ids": list(item.finding.doctrine_ids),
                    "source_ids": list(item.finding.source_ids),
                    "source_strength_note": item.finding.source_strength_note,
                    "anti_inferences": list(item.finding.anti_inferences),
                    "sensitive_domains": list(item.finding.sensitive_domains),
                }
                for item in self.evidence.findings
            ],
            "boundaries": [
                {
                    "boundary_id": item.boundary_id,
                    "scope": item.scope,
                    "profile_number": item.profile_number,
                    "kind": item.kind,
                    "subject": item.subject,
                    "reason": item.reason,
                }
                for item in self.evidence.boundaries
            ],
            "relations": [
                {
                    "relation_id": item.relation_id,
                    "kind": item.kind.value,
                    "support_ids": list(item.support_ids),
                    "statement": item.statement,
                }
                for item in self.relations
            ],
        }


def _longitudinal_relations(evidence: ClinicalEvidence) -> tuple[IntegrationRelation, ...]:
    result = []
    for pattern in evidence.factor_patterns:
        if not pattern.transitions:
            continue
        rendered = "; ".join(
            f"P{profile}: {before}->{after}"
            for profile, before, after in pattern.transitions
        )
        result.append(
            IntegrationRelation(
                relation_id=f"IR_LONG_{pattern.factor}",
                kind=RelationKind.LONGITUDINAL_CHANGE,
                support_ids=(pattern.pattern_id,),
                statement=(
                    f"Factorul {pattern.factor} prezintă schimbări longitudinale de "
                    f"reacție de bază în serie: {rendered}."
                ),
            )
        )
    return tuple(result)


def build_clinical_integration(
    evidence: ClinicalEvidence | ClinicalProtocolEvaluation,
    *,
    relations: Iterable[IntegrationRelation] = (),
    include_longitudinal_relations: bool = True,
) -> ClinicalIntegration:
    """Build P4 from P3 evidence without free-form reconciliation.

    For convenience an already evaluated protocol may be supplied directly; it is
    first converted through the canonical P3 builder.  Automatic relations are
    limited to deterministic within-factor longitudinal change.  Cross-factor or
    doctrinal synthesis must be supplied later as explicit reviewed relations.
    """
    if isinstance(evidence, ClinicalProtocolEvaluation):
        evidence = build_clinical_evidence(evidence)
    if not isinstance(evidence, ClinicalEvidence):
        raise TypeError("Clinical integration requires ClinicalEvidence or ClinicalProtocolEvaluation")

    supplied = tuple(relations)
    automatic = _longitudinal_relations(evidence) if include_longitudinal_relations else ()
    return ClinicalIntegration(evidence=evidence, relations=automatic + supplied)
