"""Deterministic clinician-inspectable projection of foreground clinical nuclei.

Gate 3 stays upstream of every writer.  It does not add Szondian meaning or create
new relations.  It projects the existing ``ClinicalForegroundComposition`` into a
lossless, human-readable contract containing the active claim meanings, authorized
relations, exact support facts, provenance, source modality, anti-inferences and
explicit coexistence-only boundaries.

The scope is deliberately identical to the Gate-2 compiler: PROFILE / foreground
only.  SERIES, E.K.P., longitudinal and clinician-context composition remain outside
this contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .clinical_composition import (
    CLINICAL_COMPOSITION_VERSION,
    ClinicalCompositionClaimEnvelope,
    ClinicalCompositionNoBridge,
    ClinicalCompositionRelation,
    ClinicalCompositionSupportFact,
    _fact_snapshot,
    build_foreground_clinical_composition,
)
from .clinical_evidence_packet import ClinicalEvidencePacket


CLINICAL_NUCLEUS_PROJECTION_VERSION = "SZONDI3_CLINICAL_NUCLEUS_PROJECTION_GATE3_V1"


def _ordered_distinct(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _display_value(value: Any) -> str:
    if isinstance(value, tuple):
        return "(" + ",".join(_display_value(item) for item in value) + ")"
    return str(value)


def _envelope(finding) -> ClinicalCompositionClaimEnvelope:
    return ClinicalCompositionClaimEnvelope(
        claim_id=finding.claim_id,
        statement=finding.statement,
        assertion_mode=finding.assertion_mode,
        source_strength_note=finding.source_strength_note,
        doctrine_ids=finding.doctrine_ids,
        source_ids=finding.source_ids,
        support_fact_ids=finding.support_fact_ids,
        anti_inference_ids=finding.anti_inference_ids,
        anti_inferences=finding.anti_inferences,
    )


def _profile_finding_index(packet: ClinicalEvidencePacket) -> dict[tuple[int, str], Any]:
    result: dict[tuple[int, str], Any] = {}
    for finding in packet.report.findings:
        if finding.scope != "PROFILE" or finding.assertion_mode == "LIMITATION":
            continue
        if finding.profile_number is None:
            raise ValueError(f"PROFILE finding lacks profile number: {finding.claim_id}")
        key = (finding.profile_number, finding.claim_id)
        if key in result:
            raise ValueError(
                "Duplicate foreground finding during nucleus projection: "
                f"profile={finding.profile_number}, claim={finding.claim_id}"
            )
        result[key] = finding
    return result


@dataclass(frozen=True, slots=True)
class ClinicalNucleusProjection:
    """Lossless Gate-3 view of one already-compiled clinical nucleus."""

    nucleus_id: str
    profile_number: int
    member_unit_ids: tuple[str, ...]
    support_claim_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    claim_envelopes: tuple[ClinicalCompositionClaimEnvelope, ...]
    relations: tuple[ClinicalCompositionRelation, ...]
    support_facts: tuple[ClinicalCompositionSupportFact, ...]
    doctrine_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    anti_inference_ids: tuple[str, ...]
    anti_inferences: tuple[str, ...]
    sensitive_domains: tuple[str, ...]
    coexistence_only_with: tuple[str, ...]

    @property
    def authorized_meanings(self) -> tuple[str, ...]:
        """Statements already authorized upstream; no projection prose is invented."""
        return tuple(item.statement for item in self.claim_envelopes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nucleus_id": self.nucleus_id,
            "profile_number": self.profile_number,
            "member_unit_ids": list(self.member_unit_ids),
            "support_claim_ids": list(self.support_claim_ids),
            "relation_ids": list(self.relation_ids),
            "claim_envelopes": [item.to_dict() for item in self.claim_envelopes],
            "relations": [item.to_dict() for item in self.relations],
            "support_facts": [item.to_dict() for item in self.support_facts],
            "doctrine_ids": list(self.doctrine_ids),
            "source_ids": list(self.source_ids),
            "anti_inference_ids": list(self.anti_inference_ids),
            "anti_inferences": list(self.anti_inferences),
            "sensitive_domains": list(self.sensitive_domains),
            "coexistence_only_with": list(self.coexistence_only_with),
        }


@dataclass(frozen=True, slots=True)
class ClinicalProfileNucleusProjection:
    profile_number: int
    global_synthesis_mode: str
    nuclei: tuple[ClinicalNucleusProjection, ...]
    no_bridge_relations: tuple[ClinicalCompositionNoBridge, ...]

    def nucleus_for_claim(self, claim_id: str) -> ClinicalNucleusProjection:
        matches = tuple(
            nucleus for nucleus in self.nuclei if claim_id in nucleus.support_claim_ids
        )
        if len(matches) != 1:
            raise KeyError(
                f"Unknown or ambiguous projected nucleus for claim {claim_id}: "
                f"profile={self.profile_number}"
            )
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_number": self.profile_number,
            "global_synthesis_mode": self.global_synthesis_mode,
            "nuclei": [item.to_dict() for item in self.nuclei],
            "no_bridge_relations": [
                item.to_dict() for item in self.no_bridge_relations
            ],
        }


@dataclass(frozen=True, slots=True)
class ClinicalForegroundNucleusProjection:
    version: str
    composition_version: str
    profiles: tuple[ClinicalProfileNucleusProjection, ...]
    ignored_series_unit_ids: tuple[str, ...]

    def profile(self, profile_number: int) -> ClinicalProfileNucleusProjection:
        matches = tuple(
            item for item in self.profiles if item.profile_number == profile_number
        )
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate projected profile: {profile_number}")
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "composition_version": self.composition_version,
            "profiles": [item.to_dict() for item in self.profiles],
            "ignored_series_unit_ids": list(self.ignored_series_unit_ids),
        }

    def render_clinical_dump(self) -> str:
        """Render a deterministic inspection surface without generating new meaning."""
        lines = [
            f"Clinical nucleus projection {self.version}",
            f"composition={self.composition_version}",
        ]
        for profile in self.profiles:
            lines.append(
                f"PROFILE {profile.profile_number} | "
                f"GLOBAL_SYNTHESIS={profile.global_synthesis_mode}"
            )
            for nucleus in profile.nuclei:
                lines.append(f"  NUCLEUS {nucleus.nucleus_id}")
                lines.append("    units=" + ",".join(nucleus.member_unit_ids))
                lines.append("    claims=" + ",".join(nucleus.support_claim_ids))

                lines.append("    CAN_ASSERT")
                for envelope in nucleus.claim_envelopes:
                    lines.append(
                        f"      {envelope.claim_id} [{envelope.assertion_mode}] "
                        f"{envelope.statement}"
                    )
                    if envelope.source_strength_note:
                        lines.append(
                            "        source_strength=" + envelope.source_strength_note
                        )

                if nucleus.relations:
                    lines.append("    AUTHORIZED_RELATIONS")
                    for relation in nucleus.relations:
                        anchor = relation.anchor_claim_id or "same-support-bundle"
                        lines.append(
                            f"      {relation.relation_id} | {relation.relation_type} "
                            f"| anchor={anchor}"
                        )
                        lines.append(
                            "        member_units=" + ",".join(relation.member_unit_ids)
                        )
                        for envelope in relation.claim_envelopes:
                            lines.append(
                                f"        permits[{envelope.claim_id}]="
                                + envelope.statement
                            )
                else:
                    lines.append("    AUTHORIZED_RELATIONS=NONE")

                lines.append("    SOURCE_MODALITY")
                for envelope in nucleus.claim_envelopes:
                    strength = envelope.source_strength_note or "-"
                    lines.append(
                        f"      {envelope.claim_id}: {envelope.assertion_mode}; "
                        f"strength={strength}"
                    )

                lines.append("    EXACT_SUPPORT")
                for fact in nucleus.support_facts:
                    lines.append(
                        f"      {fact.fact_id} -> {_display_value(fact.value)}"
                    )

                lines.append("    PROVENANCE")
                lines.append("      doctrines=" + ",".join(nucleus.doctrine_ids))
                lines.append("      sources=" + ",".join(nucleus.source_ids))

                if nucleus.anti_inference_ids or nucleus.anti_inferences:
                    lines.append("    CANNOT_ASSERT")
                    for envelope in nucleus.claim_envelopes:
                        if not envelope.anti_inference_ids and not envelope.anti_inferences:
                            continue
                        lines.append(f"      {envelope.claim_id}")
                        if envelope.anti_inference_ids:
                            lines.append(
                                "        anti_ids="
                                + ",".join(envelope.anti_inference_ids)
                            )
                        for text in envelope.anti_inferences:
                            lines.append("        - " + text)
                else:
                    lines.append("    CANNOT_ASSERT=NONE")

                if nucleus.coexistence_only_with:
                    lines.append(
                        "    COEXISTENCE_ONLY_WITH="
                        + ",".join(nucleus.coexistence_only_with)
                    )
                else:
                    lines.append("    COEXISTENCE_ONLY_WITH=NONE")

        if self.ignored_series_unit_ids:
            lines.append(
                "OUT_OF_SCOPE_SERIES_UNITS=" + ",".join(self.ignored_series_unit_ids)
            )
        return "\n".join(lines)


def _coexistence_targets(profile, nucleus_id: str) -> tuple[str, ...]:
    result: list[str] = []
    for relation in profile.no_bridge_relations:
        if relation.left_nucleus_id == nucleus_id:
            result.append(relation.right_nucleus_id)
        elif relation.right_nucleus_id == nucleus_id:
            result.append(relation.left_nucleus_id)
    return _ordered_distinct(result)


def build_clinical_nucleus_projection(
    packet: ClinicalEvidencePacket,
) -> ClinicalForegroundNucleusProjection:
    """Project Gate-2 nuclei into a lossless clinician-inspectable Gate-3 view."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical nucleus projection requires a ClinicalEvidencePacket")

    composition = build_foreground_clinical_composition(packet)
    finding_index = _profile_finding_index(packet)
    projected_profiles: list[ClinicalProfileNucleusProjection] = []

    for profile in composition.profiles:
        relation_index = {item.relation_id: item for item in profile.relations}
        projected_nuclei: list[ClinicalNucleusProjection] = []
        for nucleus in profile.nuclei:
            findings = []
            for claim_id in nucleus.support_claim_ids:
                key = (profile.profile_number, claim_id)
                try:
                    findings.append(finding_index[key])
                except KeyError as exc:
                    raise ValueError(
                        "Composition/projection finding drift: "
                        f"profile={profile.profile_number}, claim={claim_id}"
                    ) from exc

            claim_envelopes = tuple(_envelope(item) for item in findings)
            fact_ids = _ordered_distinct(
                fact_id
                for envelope in claim_envelopes
                for fact_id in envelope.support_fact_ids
            )
            support_facts = _fact_snapshot(
                packet,
                profile_number=profile.profile_number,
                fact_ids=fact_ids,
            )

            relations: list[ClinicalCompositionRelation] = []
            for relation_id in nucleus.relation_ids:
                try:
                    relations.append(relation_index[relation_id])
                except KeyError as exc:
                    raise ValueError(
                        "Composition/projection relation drift: " + relation_id
                    ) from exc

            projected_nuclei.append(
                ClinicalNucleusProjection(
                    nucleus_id=nucleus.nucleus_id,
                    profile_number=profile.profile_number,
                    member_unit_ids=nucleus.unit_ids,
                    support_claim_ids=nucleus.support_claim_ids,
                    relation_ids=nucleus.relation_ids,
                    claim_envelopes=claim_envelopes,
                    relations=tuple(relations),
                    support_facts=support_facts,
                    doctrine_ids=_ordered_distinct(
                        doctrine_id
                        for envelope in claim_envelopes
                        for doctrine_id in envelope.doctrine_ids
                    ),
                    source_ids=_ordered_distinct(
                        source_id
                        for envelope in claim_envelopes
                        for source_id in envelope.source_ids
                    ),
                    anti_inference_ids=_ordered_distinct(
                        anti_id
                        for envelope in claim_envelopes
                        for anti_id in envelope.anti_inference_ids
                    ),
                    anti_inferences=_ordered_distinct(
                        text
                        for envelope in claim_envelopes
                        for text in envelope.anti_inferences
                    ),
                    sensitive_domains=_ordered_distinct(
                        domain for finding in findings for domain in finding.sensitive_domains
                    ),
                    coexistence_only_with=_coexistence_targets(
                        profile, nucleus.nucleus_id
                    ),
                )
            )

        projected_profiles.append(
            ClinicalProfileNucleusProjection(
                profile_number=profile.profile_number,
                global_synthesis_mode=profile.synthesis_mode,
                nuclei=tuple(projected_nuclei),
                no_bridge_relations=profile.no_bridge_relations,
            )
        )

    return ClinicalForegroundNucleusProjection(
        version=CLINICAL_NUCLEUS_PROJECTION_VERSION,
        composition_version=CLINICAL_COMPOSITION_VERSION,
        profiles=tuple(projected_profiles),
        ignored_series_unit_ids=composition.ignored_series_unit_ids,
    )
