"""Deterministic planning boundary for clinician-facing narrative reports.

The planner does not interpret Szondi material. It partitions already-active P2B
findings into narrative units that a language model may formulate. Findings may be
composed only when they share the same deterministic fact bundle in the same
scope/profile -- the same composition rule enforced by the synthesis validator.

This gives the generative layer a finite writing plan instead of asking it to decide
which findings belong together.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .clinical_evidence_packet import ClinicalEvidencePacket


CLINICAL_REPORT_PLAN_VERSION = "SZONDI3_CLINICAL_REPORT_PLAN_V1"
_ALLOWED_PLAN_SCOPES = frozenset({"PROFILE", "SERIES"})


def _ordered_distinct(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


@dataclass(frozen=True, slots=True)
class ClinicalReportPlanUnit:
    """One closed-world semantic unit that may become one narrative block."""

    unit_id: str
    scope: str
    profile_number: int | None
    composition_mode: str
    support_claim_ids: tuple[str, ...]
    support_fact_ids: tuple[str, ...]
    support_doctrine_ids: tuple[str, ...]
    anti_inference_ids: tuple[str, ...]
    authorized_statements: tuple[str, ...]
    anti_inferences: tuple[str, ...]
    source_strength_notes: tuple[str, ...]
    sensitive_domains: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "scope": self.scope,
            "profile_number": self.profile_number,
            "composition_mode": self.composition_mode,
            "support_claim_ids": list(self.support_claim_ids),
            "support_fact_ids": list(self.support_fact_ids),
            "support_doctrine_ids": list(self.support_doctrine_ids),
            "anti_inference_ids": list(self.anti_inference_ids),
            "authorized_statements": list(self.authorized_statements),
            "anti_inferences": list(self.anti_inferences),
            "source_strength_notes": list(self.source_strength_notes),
            "sensitive_domains": list(self.sensitive_domains),
        }


@dataclass(frozen=True, slots=True)
class ClinicalReportPlan:
    """Deterministic report-writing plan derived only from active P2B findings."""

    version: str
    units: tuple[ClinicalReportPlanUnit, ...]

    @property
    def support_signatures(self) -> frozenset[tuple[str, ...]]:
        return frozenset(tuple(sorted(unit.support_claim_ids)) for unit in self.units)

    def unit_for_support_claims(
        self,
        support_claim_ids: tuple[str, ...],
    ) -> ClinicalReportPlanUnit:
        signature = tuple(sorted(support_claim_ids))
        matches = tuple(
            unit
            for unit in self.units
            if tuple(sorted(unit.support_claim_ids)) == signature
        )
        if len(matches) != 1:
            raise KeyError(
                "Unknown or ambiguous clinical report plan support signature: "
                + ", ".join(signature)
            )
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "units": [unit.to_dict() for unit in self.units],
        }


def _eligible_findings(packet: ClinicalEvidencePacket) -> tuple[Any, ...]:
    return tuple(
        finding
        for finding in packet.report.findings
        if finding.assertion_mode != "LIMITATION"
        and finding.scope in _ALLOWED_PLAN_SCOPES
    )


def build_clinical_report_plan(packet: ClinicalEvidencePacket) -> ClinicalReportPlan:
    """Build maximal same-fact-bundle narrative units without adding meaning.

    The planner groups only findings that:
    - are active, non-LIMITATION PROFILE/SERIES findings;
    - live in the same scope and profile; and
    - have exactly the same deterministic support-fact set.

    No factor/vector bridge is inferred from coexistence. E.K.P. is deliberately
    outside this foreground/series plan.
    """
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report planning requires a ClinicalEvidencePacket")

    groups: dict[tuple[str, int | None, frozenset[str]], list[Any]] = {}
    group_order: list[tuple[str, int | None, frozenset[str]]] = []
    for finding in _eligible_findings(packet):
        key = (
            finding.scope,
            finding.profile_number,
            frozenset(finding.support_fact_ids),
        )
        if key not in groups:
            groups[key] = []
            group_order.append(key)
        groups[key].append(finding)

    units: list[ClinicalReportPlanUnit] = []
    profile_counters: dict[tuple[str, int | None], int] = {}
    for key in group_order:
        scope, profile_number, _ = key
        findings = tuple(groups[key])
        counter_key = (scope, profile_number)
        sequence = profile_counters.get(counter_key, 0) + 1
        profile_counters[counter_key] = sequence
        scope_label = "S" if scope == "SERIES" else f"P{profile_number}"
        unit_id = f"RPU-{scope_label}-{sequence:03d}"

        support_claim_ids = _ordered_distinct(
            finding.claim_id for finding in findings
        )
        support_fact_ids = _ordered_distinct(
            fact_id
            for finding in findings
            for fact_id in finding.support_fact_ids
        )
        support_doctrine_ids = _ordered_distinct(
            doctrine_id
            for finding in findings
            for doctrine_id in finding.doctrine_ids
        )
        anti_inference_ids = _ordered_distinct(
            anti_id
            for finding in findings
            for anti_id in finding.anti_inference_ids
        )
        authorized_statements = _ordered_distinct(
            finding.statement for finding in findings
        )
        anti_inferences = _ordered_distinct(
            text
            for finding in findings
            for text in finding.anti_inferences
        )
        source_strength_notes = _ordered_distinct(
            finding.source_strength_note
            for finding in findings
            if finding.source_strength_note
        )
        sensitive_domains = _ordered_distinct(
            domain
            for finding in findings
            for domain in finding.sensitive_domains
        )

        units.append(
            ClinicalReportPlanUnit(
                unit_id=unit_id,
                scope=scope,
                profile_number=profile_number,
                composition_mode=(
                    "SAME_FACT_BUNDLE" if len(support_claim_ids) > 1 else "ATOMIC"
                ),
                support_claim_ids=support_claim_ids,
                support_fact_ids=support_fact_ids,
                support_doctrine_ids=support_doctrine_ids,
                anti_inference_ids=anti_inference_ids,
                authorized_statements=authorized_statements,
                anti_inferences=anti_inferences,
                source_strength_notes=source_strength_notes,
                sensitive_domains=sensitive_domains,
            )
        )

    return ClinicalReportPlan(
        version=CLINICAL_REPORT_PLAN_VERSION,
        units=tuple(units),
    )
