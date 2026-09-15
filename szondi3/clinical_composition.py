"""Deterministic foreground composition prototype for clinical reporting.

This module is deliberately upstream of any AI writer.  It compiles already-active
P2B/report-plan meanings into a small reviewed relation vocabulary and otherwise
leaves meanings as coexistence-only nuclei.  It does not discover doctrine, add
clinical meaning, or generate person-level prose.

Gate-2 scope is intentionally narrow: PROFILE findings only.  SERIES, E.K.P.,
longitudinal and clinician-context composition remain outside this contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable

from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_report_plan import ClinicalReportPlanUnit, build_clinical_report_plan


CLINICAL_COMPOSITION_VERSION = "SZONDI3_CLINICAL_COMPOSITION_FOREGROUND_V1"

COEXISTENCE_ONLY = "COEXISTENCE_ONLY"
SAME_SUPPORT_BUNDLE = "SAME_SUPPORT_BUNDLE"
EXPLICIT_DOCTRINAL_BRIDGE = "EXPLICIT_DOCTRINAL_BRIDGE"
CONSTITUENT_EXPLAINS_COMPOSITE = "CONSTITUENT_EXPLAINS_COMPOSITE"
SAME_TRIGGER_EXTENDS_MEANING = "SAME_TRIGGER_EXTENDS_MEANING"

SINGLE_NUCLEUS = "SINGLE_NUCLEUS"
NULL_SYNTHESIS = "NULL_SYNTHESIS"


@dataclass(frozen=True, slots=True)
class ClinicalCompositionSupportFact:
    fact_id: str
    value: Any

    def to_dict(self) -> dict[str, Any]:
        return {"fact_id": self.fact_id, "value": _json_value(self.value)}


@dataclass(frozen=True, slots=True)
class ClinicalCompositionClaimEnvelope:
    """Lossless report-layer envelope for one active claim used by a relation."""

    claim_id: str
    statement: str
    assertion_mode: str
    source_strength_note: str
    doctrine_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    support_fact_ids: tuple[str, ...]
    anti_inference_ids: tuple[str, ...]
    anti_inferences: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "statement": self.statement,
            "assertion_mode": self.assertion_mode,
            "source_strength_note": self.source_strength_note,
            "doctrine_ids": list(self.doctrine_ids),
            "source_ids": list(self.source_ids),
            "support_fact_ids": list(self.support_fact_ids),
            "anti_inference_ids": list(self.anti_inference_ids),
            "anti_inferences": list(self.anti_inferences),
        }


@dataclass(frozen=True, slots=True)
class ClinicalCompositionRelation:
    relation_id: str
    relation_type: str
    profile_number: int
    anchor_claim_id: str | None
    member_unit_ids: tuple[str, ...]
    claim_envelopes: tuple[ClinicalCompositionClaimEnvelope, ...]
    support_facts: tuple[ClinicalCompositionSupportFact, ...]

    @property
    def support_claim_ids(self) -> tuple[str, ...]:
        return tuple(item.claim_id for item in self.claim_envelopes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "relation_id": self.relation_id,
            "relation_type": self.relation_type,
            "profile_number": self.profile_number,
            "anchor_claim_id": self.anchor_claim_id,
            "member_unit_ids": list(self.member_unit_ids),
            "claim_envelopes": [item.to_dict() for item in self.claim_envelopes],
            "support_facts": [item.to_dict() for item in self.support_facts],
        }


@dataclass(frozen=True, slots=True)
class ClinicalCompositionNucleus:
    nucleus_id: str
    profile_number: int
    unit_ids: tuple[str, ...]
    support_claim_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nucleus_id": self.nucleus_id,
            "profile_number": self.profile_number,
            "unit_ids": list(self.unit_ids),
            "support_claim_ids": list(self.support_claim_ids),
            "relation_ids": list(self.relation_ids),
        }


@dataclass(frozen=True, slots=True)
class ClinicalCompositionNoBridge:
    left_nucleus_id: str
    right_nucleus_id: str
    relation_type: str = COEXISTENCE_ONLY

    def to_dict(self) -> dict[str, str]:
        return {
            "left_nucleus_id": self.left_nucleus_id,
            "right_nucleus_id": self.right_nucleus_id,
            "relation_type": self.relation_type,
        }


@dataclass(frozen=True, slots=True)
class ClinicalProfileComposition:
    profile_number: int
    synthesis_mode: str
    nuclei: tuple[ClinicalCompositionNucleus, ...]
    relations: tuple[ClinicalCompositionRelation, ...]
    no_bridge_relations: tuple[ClinicalCompositionNoBridge, ...]

    def nucleus_for_claim(self, claim_id: str) -> ClinicalCompositionNucleus:
        matches = tuple(
            nucleus for nucleus in self.nuclei if claim_id in nucleus.support_claim_ids
        )
        if len(matches) != 1:
            raise KeyError(
                f"Unknown or ambiguous composition nucleus for claim {claim_id}: "
                f"profile={self.profile_number}"
            )
        return matches[0]

    def relation_for_anchor(self, claim_id: str) -> ClinicalCompositionRelation:
        matches = tuple(
            relation for relation in self.relations if relation.anchor_claim_id == claim_id
        )
        if len(matches) != 1:
            raise KeyError(
                f"Unknown or ambiguous composition relation for claim {claim_id}: "
                f"profile={self.profile_number}"
            )
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_number": self.profile_number,
            "synthesis_mode": self.synthesis_mode,
            "nuclei": [item.to_dict() for item in self.nuclei],
            "relations": [item.to_dict() for item in self.relations],
            "no_bridge_relations": [
                item.to_dict() for item in self.no_bridge_relations
            ],
        }


@dataclass(frozen=True, slots=True)
class ClinicalForegroundComposition:
    version: str
    profiles: tuple[ClinicalProfileComposition, ...]
    ignored_series_unit_ids: tuple[str, ...]

    def profile(self, profile_number: int) -> ClinicalProfileComposition:
        matches = tuple(
            item for item in self.profiles if item.profile_number == profile_number
        )
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate composed profile: {profile_number}")
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "profiles": [item.to_dict() for item in self.profiles],
            "ignored_series_unit_ids": list(self.ignored_series_unit_ids),
        }

    def render_nucleus_dump(self) -> str:
        """Return a deterministic, non-generative human-readable research dump."""
        lines = [f"Clinical composition {self.version}"]
        for profile in self.profiles:
            lines.append(
                f"PROFILE {profile.profile_number} | synthesis={profile.synthesis_mode}"
            )
            relation_index = {item.relation_id: item for item in profile.relations}
            for nucleus in profile.nuclei:
                lines.append(
                    f"  {nucleus.nucleus_id} | units={','.join(nucleus.unit_ids)}"
                )
                lines.append(
                    "    claims=" + ",".join(nucleus.support_claim_ids)
                )
                for relation_id in nucleus.relation_ids:
                    relation = relation_index[relation_id]
                    anchor = relation.anchor_claim_id or "bundle"
                    lines.append(
                        f"    relation={relation.relation_type} anchor={anchor}"
                    )
                    for envelope in relation.claim_envelopes:
                        strength = envelope.source_strength_note or "-"
                        lines.append(
                            "      modality="
                            f"{envelope.claim_id}:{envelope.assertion_mode}; strength={strength}"
                        )
                    for fact in relation.support_facts:
                        lines.append(
                            f"      fact={fact.fact_id} -> {_display_value(fact.value)}"
                        )
                    anti_ids = _ordered_distinct(
                        anti_id
                        for envelope in relation.claim_envelopes
                        for anti_id in envelope.anti_inference_ids
                    )
                    if anti_ids:
                        lines.append("      anti=" + ",".join(anti_ids))
            for no_bridge in profile.no_bridge_relations:
                lines.append(
                    "  no-bridge="
                    f"{no_bridge.left_nucleus_id}<->{no_bridge.right_nucleus_id}"
                )
        if self.ignored_series_unit_ids:
            lines.append(
                "IGNORED SERIES UNITS=" + ",".join(self.ignored_series_unit_ids)
            )
        return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class _ReviewedRelationSpec:
    anchor_claim_id: str
    relation_type: str
    member_claim_ids: tuple[str, ...] = ()
    merge_member_units: bool = False


# This is reviewed composition metadata, not new P2B doctrine.  Each entry only
# describes how an already-active executable claim may be organized relative to
# other already-active meanings.  Unknown claims/relations are intentionally not
# guessed and therefore remain separate nuclei.
_REVIEWED_RELATION_SPECS = (
    _ReviewedRelationSpec(
        "IC_SZONDI_PRIMARY_000037",
        CONSTITUENT_EXPLAINS_COMPOSITE,
        ("IC_SZONDI_PRIMARY_000007", "IC_SZONDI_PRIMARY_000009"),
        True,
    ),
    _ReviewedRelationSpec(
        "IC_SZONDI_PRIMARY_000042",
        CONSTITUENT_EXPLAINS_COMPOSITE,
        ("IC_SZONDI_PRIMARY_000008", "IC_SZONDI_PRIMARY_000009"),
        True,
    ),
    _ReviewedRelationSpec(
        "IC_SZONDI_PRIMARY_000072",
        SAME_TRIGGER_EXTENDS_MEANING,
        ("IC_SZONDI_PRIMARY_000037",),
        True,
    ),
    _ReviewedRelationSpec(
        "IC_SZONDI_PRIMARY_000073",
        SAME_TRIGGER_EXTENDS_MEANING,
        ("IC_SZONDI_PRIMARY_000042",),
        True,
    ),
    _ReviewedRelationSpec("IC_SZONDI_PRIMARY_000038", EXPLICIT_DOCTRINAL_BRIDGE),
    _ReviewedRelationSpec("IC_SZONDI_PRIMARY_000055", EXPLICIT_DOCTRINAL_BRIDGE),
    _ReviewedRelationSpec("IC_SZONDI_PRIMARY_000056", EXPLICIT_DOCTRINAL_BRIDGE),
    _ReviewedRelationSpec("IC_SZONDI_PRIMARY_000078", EXPLICIT_DOCTRINAL_BRIDGE),
    _ReviewedRelationSpec("IC_SZONDI_PRIMARY_000086", EXPLICIT_DOCTRINAL_BRIDGE),
)


def _ordered_distinct(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _json_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return value


def _display_value(value: Any) -> str:
    if isinstance(value, tuple):
        return "(" + ",".join(_display_value(item) for item in value) + ")"
    return str(value)


def _base_symbol(symbol: str, *, forced_null: bool = False) -> str:
    if forced_null:
        return "ø"
    if symbol.startswith("±"):
        return "±"
    if not symbol:
        raise ValueError("Cannot derive base symbol from an empty reaction")
    return symbol[0]


def _profile_observation(packet: ClinicalEvidencePacket, profile_number: int):
    matches = tuple(
        item
        for item in packet.report.observations
        if item.profile_number == profile_number
    )
    if len(matches) != 1:
        raise ValueError(
            f"Composition requires exactly one observation for profile {profile_number}"
        )
    return matches[0]


def _resolve_profile_fact(
    packet: ClinicalEvidencePacket,
    *,
    profile_number: int,
    fact_id: str,
) -> Any:
    prefix = f"foreground_profile_{profile_number}:"
    if not fact_id.startswith(prefix):
        raise ValueError(
            "Foreground composition cannot resolve non-profile support fact: " + fact_id
        )

    observation = _profile_observation(packet, profile_number)
    remainder = fact_id[len(prefix) :]
    parts = remainder.split(":")

    if parts == ["quantum_tension_factors"]:
        return tuple(
            item.factor for item in observation.factors if item.quantum_level > 0
        )

    if len(parts) == 3 and parts[0] == "factor":
        factor, field = parts[1], parts[2]
        matches = tuple(item for item in observation.factors if item.factor == factor)
        if len(matches) != 1:
            raise ValueError(f"Unknown factor support fact: {fact_id}")
        reaction = matches[0]
        if field == "base_symbol":
            return _base_symbol(reaction.symbol, forced_null=reaction.forced_null)
        if field == "quantum_level":
            return reaction.quantum_level
        raise ValueError(f"Unknown factor support field: {fact_id}")

    if len(parts) == 3 and parts[0] == "vector" and parts[2] == "base_symbols":
        vector = parts[1]
        matches = tuple(item for item in observation.vectors if item.vector == vector)
        if len(matches) != 1:
            raise ValueError(f"Unknown vector support fact: {fact_id}")
        factor_by_name = {item.factor: item for item in observation.factors}
        vector_factors = {
            "S": ("h", "s"),
            "P": ("e", "hy"),
            "Sch": ("k", "p"),
            "C": ("d", "m"),
        }
        if vector not in vector_factors:
            raise ValueError(f"Unknown vector support fact: {fact_id}")
        return tuple(
            _base_symbol(
                factor_by_name[factor].symbol,
                forced_null=factor_by_name[factor].forced_null,
            )
            for factor in vector_factors[vector]
        )

    raise ValueError(f"Unsupported foreground support fact: {fact_id}")


def _fact_snapshot(
    packet: ClinicalEvidencePacket,
    *,
    profile_number: int,
    fact_ids: Iterable[str],
) -> tuple[ClinicalCompositionSupportFact, ...]:
    return tuple(
        ClinicalCompositionSupportFact(
            fact_id=fact_id,
            value=_resolve_profile_fact(
                packet, profile_number=profile_number, fact_id=fact_id
            ),
        )
        for fact_id in _ordered_distinct(fact_ids)
    )


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
                "Duplicate active foreground finding: "
                f"profile={finding.profile_number}, claim={finding.claim_id}"
            )
        result[key] = finding
    return result


def _profile_units(
    units: tuple[ClinicalReportPlanUnit, ...], profile_number: int
) -> tuple[ClinicalReportPlanUnit, ...]:
    return tuple(
        unit
        for unit in units
        if unit.scope == "PROFILE" and unit.profile_number == profile_number
    )


def _unit_claim_index(
    units: tuple[ClinicalReportPlanUnit, ...],
) -> dict[str, ClinicalReportPlanUnit]:
    result: dict[str, ClinicalReportPlanUnit] = {}
    for unit in units:
        for claim_id in unit.support_claim_ids:
            if claim_id in result:
                raise ValueError(
                    f"Claim occurs in multiple report-plan units: {claim_id}"
                )
            result[claim_id] = unit
    return result


def _same_bundle_relations(
    packet: ClinicalEvidencePacket,
    *,
    profile_number: int,
    units: tuple[ClinicalReportPlanUnit, ...],
    finding_index: dict[tuple[int, str], Any],
) -> list[ClinicalCompositionRelation]:
    relations: list[ClinicalCompositionRelation] = []
    sequence = 0
    for unit in units:
        if unit.composition_mode != "SAME_FACT_BUNDLE":
            continue
        sequence += 1
        findings = tuple(
            finding_index[(profile_number, claim_id)]
            for claim_id in unit.support_claim_ids
        )
        relations.append(
            ClinicalCompositionRelation(
                relation_id=f"CCR-P{profile_number}-B{sequence:03d}",
                relation_type=SAME_SUPPORT_BUNDLE,
                profile_number=profile_number,
                anchor_claim_id=None,
                member_unit_ids=(unit.unit_id,),
                claim_envelopes=tuple(_envelope(item) for item in findings),
                support_facts=_fact_snapshot(
                    packet,
                    profile_number=profile_number,
                    fact_ids=unit.support_fact_ids,
                ),
            )
        )
    return relations


def _reviewed_relations(
    packet: ClinicalEvidencePacket,
    *,
    profile_number: int,
    units: tuple[ClinicalReportPlanUnit, ...],
    finding_index: dict[tuple[int, str], Any],
) -> list[tuple[ClinicalCompositionRelation, bool]]:
    claim_units = _unit_claim_index(units)
    result: list[tuple[ClinicalCompositionRelation, bool]] = []
    for spec in _REVIEWED_RELATION_SPECS:
        anchor_key = (profile_number, spec.anchor_claim_id)
        if anchor_key not in finding_index:
            continue
        if spec.anchor_claim_id not in claim_units:
            raise ValueError(
                f"Active reviewed anchor missing from report plan: {spec.anchor_claim_id}"
            )
        missing_members = tuple(
            claim_id
            for claim_id in spec.member_claim_ids
            if (profile_number, claim_id) not in finding_index or claim_id not in claim_units
        )
        if missing_members:
            raise ValueError(
                "Reviewed composition dependency drift for "
                f"{spec.anchor_claim_id}: missing " + ", ".join(missing_members)
            )

        member_units = _ordered_distinct(
            (
                claim_units[spec.anchor_claim_id].unit_id,
                *(claim_units[claim_id].unit_id for claim_id in spec.member_claim_ids),
            )
        )
        anchor = finding_index[anchor_key]
        suffix = spec.anchor_claim_id.rsplit("_", 1)[-1]
        relation = ClinicalCompositionRelation(
            relation_id=f"CCR-P{profile_number}-{suffix}",
            relation_type=spec.relation_type,
            profile_number=profile_number,
            anchor_claim_id=spec.anchor_claim_id,
            member_unit_ids=member_units,
            claim_envelopes=(_envelope(anchor),),
            support_facts=_fact_snapshot(
                packet,
                profile_number=profile_number,
                fact_ids=anchor.support_fact_ids,
            ),
        )
        result.append((relation, spec.merge_member_units))
    return result


class _DisjointSet:
    def __init__(self, values: Iterable[str]):
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def _compose_profile(
    packet: ClinicalEvidencePacket,
    *,
    profile_number: int,
    units: tuple[ClinicalReportPlanUnit, ...],
    finding_index: dict[tuple[int, str], Any],
) -> ClinicalProfileComposition:
    if not units:
        return ClinicalProfileComposition(
            profile_number=profile_number,
            synthesis_mode=SINGLE_NUCLEUS,
            nuclei=(),
            relations=(),
            no_bridge_relations=(),
        )

    same_bundle = _same_bundle_relations(
        packet,
        profile_number=profile_number,
        units=units,
        finding_index=finding_index,
    )
    reviewed_with_merge = _reviewed_relations(
        packet,
        profile_number=profile_number,
        units=units,
        finding_index=finding_index,
    )
    reviewed = [item[0] for item in reviewed_with_merge]
    relations = tuple(same_bundle + reviewed)

    dsu = _DisjointSet(unit.unit_id for unit in units)
    for relation, merge_member_units in reviewed_with_merge:
        if not merge_member_units or len(relation.member_unit_ids) < 2:
            continue
        first = relation.member_unit_ids[0]
        for unit_id in relation.member_unit_ids[1:]:
            dsu.union(first, unit_id)

    unit_order = {unit.unit_id: index for index, unit in enumerate(units)}
    components: dict[str, list[ClinicalReportPlanUnit]] = {}
    for unit in units:
        components.setdefault(dsu.find(unit.unit_id), []).append(unit)
    ordered_components = sorted(
        components.values(), key=lambda items: min(unit_order[item.unit_id] for item in items)
    )

    relation_by_unit: dict[str, list[str]] = {unit.unit_id: [] for unit in units}
    for relation in relations:
        anchor_unit_id = relation.member_unit_ids[0]
        relation_by_unit[anchor_unit_id].append(relation.relation_id)

    nuclei: list[ClinicalCompositionNucleus] = []
    for sequence, component in enumerate(ordered_components, start=1):
        component = sorted(component, key=lambda item: unit_order[item.unit_id])
        unit_ids = tuple(item.unit_id for item in component)
        claim_ids = _ordered_distinct(
            claim_id for unit in component for claim_id in unit.support_claim_ids
        )
        relation_ids = _ordered_distinct(
            relation_id
            for unit in component
            for relation_id in relation_by_unit[unit.unit_id]
        )
        nuclei.append(
            ClinicalCompositionNucleus(
                nucleus_id=f"CN-P{profile_number}-{sequence:03d}",
                profile_number=profile_number,
                unit_ids=unit_ids,
                support_claim_ids=claim_ids,
                relation_ids=relation_ids,
            )
        )

    no_bridge = tuple(
        ClinicalCompositionNoBridge(left.nucleus_id, right.nucleus_id)
        for left, right in combinations(nuclei, 2)
    )
    synthesis_mode = SINGLE_NUCLEUS if len(nuclei) <= 1 else NULL_SYNTHESIS
    return ClinicalProfileComposition(
        profile_number=profile_number,
        synthesis_mode=synthesis_mode,
        nuclei=tuple(nuclei),
        relations=relations,
        no_bridge_relations=no_bridge,
    )


def build_foreground_clinical_composition(
    packet: ClinicalEvidencePacket,
) -> ClinicalForegroundComposition:
    """Compile reviewed foreground composition without adding clinical semantics.

    Unknown relationships are not inferred.  They remain in separate nuclei and are
    represented pairwise as ``COEXISTENCE_ONLY``.  A profile with more than one
    resulting nucleus therefore has ``NULL_SYNTHESIS`` at the global profile level.
    """
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical composition requires a ClinicalEvidencePacket")

    plan = build_clinical_report_plan(packet)
    finding_index = _profile_finding_index(packet)
    profile_numbers = tuple(
        item.profile_number for item in packet.report.observations
    )
    profiles = tuple(
        _compose_profile(
            packet,
            profile_number=profile_number,
            units=_profile_units(plan.units, profile_number),
            finding_index=finding_index,
        )
        for profile_number in profile_numbers
    )
    ignored_series_unit_ids = tuple(
        unit.unit_id for unit in plan.units if unit.scope == "SERIES"
    )
    return ClinicalForegroundComposition(
        version=CLINICAL_COMPOSITION_VERSION,
        profiles=profiles,
        ignored_series_unit_ids=ignored_series_unit_ids,
    )
