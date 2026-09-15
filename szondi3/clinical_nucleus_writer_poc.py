"""Offline/replayable proof-of-concept writer contract over a NarrativePlan.

This module is intentionally not wired to the launcher and performs no network call.
It defines the structured writer request/response boundary and a replay parser that
can validate deterministic scope bindings before any future semantic prose validator.

Semantic authority comes from the projected nucleus envelopes and relation IDs.
`speech_act` only constrains how an item is used; it does not create meaning.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .clinical_ai_preview import DEFAULT_PREVIEW_MODEL
from .clinical_narrative_plan import (
    EDITORIAL_REPORT_SCOPE,
    NUCLEUS_SCOPE,
    ClinicalNarrativePlan,
)
from .clinical_nucleus_projection import ClinicalForegroundNucleusProjection
from .clinical_report_ai import _require_visible_text, _response_output_text


CLINICAL_NUCLEUS_WRITER_POC_VERSION = "SZONDI3_CLINICAL_NUCLEUS_WRITER_POC_V1"

EXPLANATION = "EXPLANATION"
HYPOTHETICAL = "HYPOTHETICAL"
QUESTION = "QUESTION"
EDITORIAL = "EDITORIAL"
LIMIT = "LIMIT"

_ALLOWED_SPEECH_ACTS = frozenset(
    {EXPLANATION, HYPOTHETICAL, QUESTION, EDITORIAL, LIMIT}
)


# Kept separate so a later ablation can reuse exactly the same style instructions
# with raw atomic findings versus nucleus projection / NarrativePlan.
NUCLEUS_WRITER_STYLE_INSTRUCTIONS = """Write clear clinician-facing Romanian.
Preserve important Szondian terms when they carry conceptual identity and explain
them immediately in Romanian. Be concrete without inventing biography, diagnosis,
history, acts or motives. Preserve the source's certainty and historical force.
Avoid software/audit vocabulary in visible prose. Hypothetical material must remain
visibly hypothetical; questions must remain questions rather than findings."""


_NUCLEUS_WRITER_CONTRACT_INSTRUCTIONS = f"""You are an experimental Szondi3 writer POC.

The supplied projection plus NarrativePlan are your COMPLETE semantic universe.
Do not use remembered Szondi theory, general psychodynamic knowledge, web knowledge
or plausible biography to add meaning.

The deterministic NarrativePlan already decides section existence, order and scope.

SCOPE RULES
- NUCLEUS_SCOPE: use only claim_ids and relation_ids allowed by that section.
  A relation may be expressed only if its relation_id is allowed there.
- EDITORIAL_REPORT_SCOPE: describe only the structure of the evidence. You may say
  that several nuclei/directions exist, that they are separate, or that the global
  mode is NULL_SYNTHESIS. claim_ids and relation_ids must be empty here.
- NULL_SYNTHESIS means: no authorized global semantic bridge. It does NOT forbid an
  editorial opening or closing. Never turn separate nuclei into one underlying
  psychodynamic mechanism.

SPEECH ACTS
- EXPLANATION: explain authorized nucleus meaning.
- HYPOTHETICAL: illustrate authorized meaning without asserting biography.
- QUESTION: ask what should be explored; do not turn the question into a finding.
- EDITORIAL: report-map language only; no new semantic bridge.
- LIMIT: express only a boundary already present in the nucleus material.

Return narrative items in NarrativePlan section order. Every plan section must have
at least one item. Nucleus items must cite at least one allowed claim_id. relation_ids
are optional and may contain only relations from the same nucleus. Editorial items
must have nucleus_id=null and empty claim_ids/relation_ids.

Do not imitate or reconstruct a hidden gold report. Do not infer which nuclei relate;
the plan and relation IDs are authoritative.

{NUCLEUS_WRITER_STYLE_INSTRUCTIONS}

Return only JSON matching the schema.
"""


_ITEM_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "item_id": {"type": "string"},
        "section_id": {"type": "string"},
        "scope_type": {
            "type": "string",
            "enum": [NUCLEUS_SCOPE, EDITORIAL_REPORT_SCOPE],
        },
        "nucleus_id": {"type": ["string", "null"]},
        "claim_ids": {"type": "array", "items": {"type": "string"}},
        "relation_ids": {"type": "array", "items": {"type": "string"}},
        "speech_act": {
            "type": "string",
            "enum": sorted(_ALLOWED_SPEECH_ACTS),
        },
        "text": {"type": "string"},
    },
    "required": [
        "item_id",
        "section_id",
        "scope_type",
        "nucleus_id",
        "claim_ids",
        "relation_ids",
        "speech_act",
        "text",
    ],
    "additionalProperties": False,
}

NUCLEUS_WRITER_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": _ITEM_SCHEMA,
            "minItems": 1,
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}


@dataclass(frozen=True, slots=True)
class ClinicalNucleusWriterItem:
    item_id: str
    section_id: str
    scope_type: str
    nucleus_id: str | None
    claim_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    speech_act: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "section_id": self.section_id,
            "scope_type": self.scope_type,
            "nucleus_id": self.nucleus_id,
            "claim_ids": list(self.claim_ids),
            "relation_ids": list(self.relation_ids),
            "speech_act": self.speech_act,
            "text": self.text,
        }


@dataclass(frozen=True, slots=True)
class ClinicalNucleusWriterPOCResult:
    contract_version: str
    provider: str
    model: str
    response_id: str
    items: tuple[ClinicalNucleusWriterItem, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_version": self.contract_version,
            "provider": self.provider,
            "model": self.model,
            "response_id": self.response_id,
            "items": [item.to_dict() for item in self.items],
        }


def _validate_plan_projection_alignment(
    projection: ClinicalForegroundNucleusProjection,
    plan: ClinicalNarrativePlan,
) -> None:
    if not isinstance(projection, ClinicalForegroundNucleusProjection):
        raise TypeError(
            "Clinical nucleus writer requires a ClinicalForegroundNucleusProjection"
        )
    if not isinstance(plan, ClinicalNarrativePlan):
        raise TypeError("Clinical nucleus writer requires a ClinicalNarrativePlan")
    if plan.projection_version != projection.version:
        raise ValueError("NarrativePlan/projection version mismatch")

    profile = projection.profile(plan.profile_number)
    projected_ids = tuple(item.nucleus_id for item in profile.nuclei)
    if projected_ids != plan.nucleus_ids:
        raise ValueError("NarrativePlan/projection nucleus drift")
    if profile.global_synthesis_mode != plan.global_synthesis_mode:
        raise ValueError("NarrativePlan/projection synthesis-mode drift")


def build_clinical_nucleus_writer_payload(
    projection: ClinicalForegroundNucleusProjection,
    plan: ClinicalNarrativePlan,
) -> dict[str, Any]:
    """Build the finite semantic payload consumed by the writer POC."""
    _validate_plan_projection_alignment(projection, plan)
    profile = projection.profile(plan.profile_number)
    return {
        "contract_version": CLINICAL_NUCLEUS_WRITER_POC_VERSION,
        "profile_projection": profile.to_dict(),
        "narrative_plan": plan.to_dict(),
    }


def build_openai_clinical_nucleus_writer_request(
    projection: ClinicalForegroundNucleusProjection,
    plan: ClinicalNarrativePlan,
    *,
    model: str = DEFAULT_PREVIEW_MODEL,
) -> dict[str, Any]:
    """Build a strict provider request without sending it over the network."""
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical nucleus writer model identifier must not be empty")
    payload = json.dumps(
        build_clinical_nucleus_writer_payload(projection, plan),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "model": model,
        "store": False,
        "tools": [],
        "reasoning": {"effort": "none"},
        "instructions": _NUCLEUS_WRITER_CONTRACT_INSTRUCTIONS,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Realize this deterministic NarrativePlan using only the "
                            "supplied nucleus projection:\n" + payload
                        ),
                    }
                ],
            }
        ],
        "text": {
            "verbosity": "medium",
            "format": {
                "type": "json_schema",
                "name": "szondi3_clinical_nucleus_writer_poc_v1",
                "strict": True,
                "schema": NUCLEUS_WRITER_RESPONSE_SCHEMA,
            },
        },
    }


def _parse_string_array(raw: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(raw, list):
        raise ValueError(f"{field_name} must be a JSON array")
    result: list[str] = []
    for value in raw:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must contain only non-empty strings")
        if value in result:
            raise ValueError(f"{field_name} contains a duplicate identifier: {value}")
        result.append(value)
    return tuple(result)


def _parse_item(raw: Any) -> ClinicalNucleusWriterItem:
    required = {
        "item_id",
        "section_id",
        "scope_type",
        "nucleus_id",
        "claim_ids",
        "relation_ids",
        "speech_act",
        "text",
    }
    if not isinstance(raw, dict) or set(raw) != required:
        raise ValueError("Clinical nucleus writer item has missing or unexpected fields")
    if raw["scope_type"] not in {NUCLEUS_SCOPE, EDITORIAL_REPORT_SCOPE}:
        raise ValueError("Clinical nucleus writer item has unknown scope_type")
    if raw["speech_act"] not in _ALLOWED_SPEECH_ACTS:
        raise ValueError("Clinical nucleus writer item has unknown speech_act")
    nucleus_id = raw["nucleus_id"]
    if nucleus_id is not None and (
        not isinstance(nucleus_id, str) or not nucleus_id.strip()
    ):
        raise ValueError("nucleus_id must be null or a non-empty string")

    return ClinicalNucleusWriterItem(
        item_id=_require_visible_text(raw["item_id"], "item_id"),
        section_id=_require_visible_text(raw["section_id"], "section_id"),
        scope_type=raw["scope_type"],
        nucleus_id=nucleus_id,
        claim_ids=_parse_string_array(raw["claim_ids"], "claim_ids"),
        relation_ids=_parse_string_array(raw["relation_ids"], "relation_ids"),
        speech_act=raw["speech_act"],
        text=_require_visible_text(raw["text"], "narrative_text"),
    )


def validate_clinical_nucleus_writer_items(
    plan: ClinicalNarrativePlan,
    items: tuple[ClinicalNucleusWriterItem, ...],
) -> tuple[ClinicalNucleusWriterItem, ...]:
    """Validate structural/scope binding only; free-prose semantics remain for next gate."""
    if not isinstance(plan, ClinicalNarrativePlan):
        raise TypeError("Clinical nucleus writer validation requires a ClinicalNarrativePlan")
    if not isinstance(items, tuple):
        raise TypeError("Clinical nucleus writer items must be supplied as a tuple")

    item_ids: set[str] = set()
    section_counts = {section.section_id: 0 for section in plan.sections}
    last_order = 0

    for item in items:
        if not isinstance(item, ClinicalNucleusWriterItem):
            raise TypeError("Unexpected clinical nucleus writer item type")
        if item.item_id in item_ids:
            raise ValueError(f"Duplicate clinical nucleus writer item: {item.item_id}")
        item_ids.add(item.item_id)

        section = plan.section(item.section_id)
        if section.order < last_order:
            raise ValueError("Clinical nucleus writer items violate NarrativePlan order")
        last_order = section.order
        section_counts[section.section_id] += 1

        if item.scope_type != section.scope_type:
            raise ValueError("Writer item scope_type does not match NarrativePlan section")
        if item.speech_act not in section.allowed_speech_acts:
            raise ValueError("Writer item speech_act is not allowed by NarrativePlan section")

        if section.scope_type == EDITORIAL_REPORT_SCOPE:
            if item.nucleus_id is not None:
                raise ValueError("Editorial writer item must not bind to a nucleus")
            if item.claim_ids or item.relation_ids:
                raise ValueError(
                    "Editorial writer item cannot consume claim or relation authority"
                )
            continue

        if item.nucleus_id != section.nucleus_id:
            raise ValueError("Writer item nucleus_id does not match NarrativePlan section")
        if not item.claim_ids:
            raise ValueError("Nucleus writer item must cite at least one allowed claim")
        if not set(item.claim_ids).issubset(section.allowed_claim_ids):
            raise ValueError("Writer item cites a claim outside its nucleus")
        if not set(item.relation_ids).issubset(section.allowed_relation_ids):
            raise ValueError("Writer item cites a relation outside its nucleus")
        if item.relation_ids and not section.semantic_bridge_allowed:
            raise ValueError("Writer item cites a semantic bridge where none is authorized")

    missing_sections = tuple(
        section_id for section_id, count in section_counts.items() if count == 0
    )
    if missing_sections:
        raise ValueError(
            "Clinical nucleus writer omitted NarrativePlan sections: "
            + ", ".join(missing_sections)
        )
    return items


def replay_clinical_nucleus_writer_response(
    projection: ClinicalForegroundNucleusProjection,
    plan: ClinicalNarrativePlan,
    response: dict[str, Any],
) -> ClinicalNucleusWriterPOCResult:
    """Replay one provider-shaped response with no network access."""
    _validate_plan_projection_alignment(projection, plan)
    if not isinstance(response, dict):
        raise TypeError("Clinical nucleus writer response must be a dictionary")
    try:
        decoded = json.loads(_response_output_text(response))
    except json.JSONDecodeError as exc:
        raise ValueError("Clinical nucleus writer output is not valid JSON") from exc
    if not isinstance(decoded, dict) or set(decoded) != {"items"}:
        raise ValueError("Clinical nucleus writer JSON must contain only items")
    if not isinstance(decoded["items"], list):
        raise ValueError("Clinical nucleus writer items must be a JSON array")

    items = validate_clinical_nucleus_writer_items(
        plan, tuple(_parse_item(item) for item in decoded["items"])
    )

    response_id = response.get("id")
    model = response.get("model")
    if not isinstance(response_id, str) or not response_id.strip():
        raise ValueError("Clinical nucleus writer response lacks response id")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical nucleus writer response lacks model identifier")

    return ClinicalNucleusWriterPOCResult(
        contract_version=CLINICAL_NUCLEUS_WRITER_POC_VERSION,
        provider="OPENAI_RESPONSES_API_REPLAY",
        model=model,
        response_id=response_id,
        items=items,
    )


__all__ = [
    "CLINICAL_NUCLEUS_WRITER_POC_VERSION",
    "NUCLEUS_WRITER_STYLE_INSTRUCTIONS",
    "NUCLEUS_WRITER_RESPONSE_SCHEMA",
    "ClinicalNucleusWriterItem",
    "ClinicalNucleusWriterPOCResult",
    "build_clinical_nucleus_writer_payload",
    "build_openai_clinical_nucleus_writer_request",
    "validate_clinical_nucleus_writer_items",
    "replay_clinical_nucleus_writer_response",
]
