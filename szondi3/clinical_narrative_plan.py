"""Minimal deterministic narrative planning over Gate-3 clinical nuclei.

The NarrativePlan decides only structure that can be fixed before language generation:
section existence/order, epistemic scope, rhetorical purpose and the exact claims/relations
available inside each nucleus section.  It does not write clinical prose and does not
add semantic relations.

`NULL_SYNTHESIS` has one precise meaning here: no authorized global semantic bridge.
It does not suppress editorial opening/closing sections that describe the structure
of the evidence without turning separate nuclei into one psychodynamic mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .clinical_composition import NULL_SYNTHESIS
from .clinical_nucleus_projection import (
    CLINICAL_NUCLEUS_PROJECTION_VERSION,
    ClinicalForegroundNucleusProjection,
)


CLINICAL_NARRATIVE_PLAN_VERSION = "SZONDI3_CLINICAL_NARRATIVE_PLAN_V1"

NUCLEUS_SCOPE = "NUCLEUS_SCOPE"
EDITORIAL_REPORT_SCOPE = "EDITORIAL_REPORT_SCOPE"

OPENING = "OPENING"
EXPLAIN = "EXPLAIN"
CLOSING = "CLOSING"

EXPLANATION = "EXPLANATION"
HYPOTHETICAL = "HYPOTHETICAL"
QUESTION = "QUESTION"
EDITORIAL = "EDITORIAL"
LIMIT = "LIMIT"

_NUCLEUS_SPEECH_ACTS = (EXPLANATION, HYPOTHETICAL, QUESTION, LIMIT)
_EDITORIAL_SPEECH_ACTS = (EDITORIAL,)


@dataclass(frozen=True, slots=True)
class ClinicalNarrativePlanSection:
    section_id: str
    order: int
    scope_type: str
    purpose: str
    nucleus_id: str | None
    allowed_nucleus_ids: tuple[str, ...]
    allowed_claim_ids: tuple[str, ...]
    allowed_relation_ids: tuple[str, ...]
    allowed_speech_acts: tuple[str, ...]
    semantic_bridge_allowed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_id": self.section_id,
            "order": self.order,
            "scope_type": self.scope_type,
            "purpose": self.purpose,
            "nucleus_id": self.nucleus_id,
            "allowed_nucleus_ids": list(self.allowed_nucleus_ids),
            "allowed_claim_ids": list(self.allowed_claim_ids),
            "allowed_relation_ids": list(self.allowed_relation_ids),
            "allowed_speech_acts": list(self.allowed_speech_acts),
            "semantic_bridge_allowed": self.semantic_bridge_allowed,
        }


@dataclass(frozen=True, slots=True)
class ClinicalNarrativePlan:
    version: str
    projection_version: str
    profile_number: int
    global_synthesis_mode: str
    nucleus_ids: tuple[str, ...]
    no_bridge_pairs: tuple[tuple[str, str], ...]
    sections: tuple[ClinicalNarrativePlanSection, ...]

    def section(self, section_id: str) -> ClinicalNarrativePlanSection:
        matches = tuple(item for item in self.sections if item.section_id == section_id)
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate narrative section: {section_id}")
        return matches[0]

    def section_for_nucleus(self, nucleus_id: str) -> ClinicalNarrativePlanSection:
        matches = tuple(
            item
            for item in self.sections
            if item.scope_type == NUCLEUS_SCOPE and item.nucleus_id == nucleus_id
        )
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate narrative nucleus: {nucleus_id}")
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "projection_version": self.projection_version,
            "profile_number": self.profile_number,
            "global_synthesis_mode": self.global_synthesis_mode,
            "nucleus_ids": list(self.nucleus_ids),
            "no_bridge_pairs": [list(pair) for pair in self.no_bridge_pairs],
            "sections": [item.to_dict() for item in self.sections],
        }


def _editorial_section(
    *,
    profile_number: int,
    order: int,
    purpose: str,
    nucleus_ids: tuple[str, ...],
) -> ClinicalNarrativePlanSection:
    suffix = "OPENING" if purpose == OPENING else "CLOSING"
    return ClinicalNarrativePlanSection(
        section_id=f"NP-P{profile_number}-{suffix}",
        order=order,
        scope_type=EDITORIAL_REPORT_SCOPE,
        purpose=purpose,
        nucleus_id=None,
        allowed_nucleus_ids=nucleus_ids,
        allowed_claim_ids=(),
        allowed_relation_ids=(),
        allowed_speech_acts=_EDITORIAL_SPEECH_ACTS,
        semantic_bridge_allowed=False,
    )


def build_clinical_narrative_plan(
    projection: ClinicalForegroundNucleusProjection,
    *,
    profile_number: int,
) -> ClinicalNarrativePlan:
    """Compile the smallest report structure that does not require writer inference.

    Nucleus sections may use only claims/relations already present in their projected
    nucleus.  Editorial sections may name the projected nuclei and report structural
    facts such as `NULL_SYNTHESIS`, but they receive no claim/relation authority and
    therefore cannot create a cross-nucleus semantic bridge.
    """
    if not isinstance(projection, ClinicalForegroundNucleusProjection):
        raise TypeError(
            "Clinical narrative planning requires a ClinicalForegroundNucleusProjection"
        )
    if not isinstance(profile_number, int) or profile_number < 1:
        raise ValueError("Narrative profile number must be a positive integer")

    profile = projection.profile(profile_number)
    nucleus_ids = tuple(item.nucleus_id for item in profile.nuclei)
    if len(set(nucleus_ids)) != len(nucleus_ids):
        raise ValueError(f"Duplicate projected nucleus identity in profile {profile_number}")

    sections: list[ClinicalNarrativePlanSection] = [
        _editorial_section(
            profile_number=profile_number,
            order=1,
            purpose=OPENING,
            nucleus_ids=nucleus_ids,
        )
    ]

    for sequence, nucleus in enumerate(profile.nuclei, start=1):
        sections.append(
            ClinicalNarrativePlanSection(
                section_id=f"NP-P{profile_number}-N{sequence:03d}",
                order=len(sections) + 1,
                scope_type=NUCLEUS_SCOPE,
                purpose=EXPLAIN,
                nucleus_id=nucleus.nucleus_id,
                allowed_nucleus_ids=(nucleus.nucleus_id,),
                allowed_claim_ids=nucleus.support_claim_ids,
                allowed_relation_ids=nucleus.relation_ids,
                allowed_speech_acts=_NUCLEUS_SPEECH_ACTS,
                semantic_bridge_allowed=bool(nucleus.relation_ids),
            )
        )

    sections.append(
        _editorial_section(
            profile_number=profile_number,
            order=len(sections) + 1,
            purpose=CLOSING,
            nucleus_ids=nucleus_ids,
        )
    )

    no_bridge_pairs = tuple(
        (item.left_nucleus_id, item.right_nucleus_id)
        for item in profile.no_bridge_relations
    )

    return ClinicalNarrativePlan(
        version=CLINICAL_NARRATIVE_PLAN_VERSION,
        projection_version=projection.version,
        profile_number=profile_number,
        global_synthesis_mode=profile.global_synthesis_mode,
        nucleus_ids=nucleus_ids,
        no_bridge_pairs=no_bridge_pairs,
        sections=tuple(sections),
    )


__all__ = [
    "CLINICAL_NARRATIVE_PLAN_VERSION",
    "NUCLEUS_SCOPE",
    "EDITORIAL_REPORT_SCOPE",
    "OPENING",
    "EXPLAIN",
    "CLOSING",
    "EXPLANATION",
    "HYPOTHETICAL",
    "QUESTION",
    "EDITORIAL",
    "LIMIT",
    "ClinicalNarrativePlanSection",
    "ClinicalNarrativePlan",
    "build_clinical_narrative_plan",
]
