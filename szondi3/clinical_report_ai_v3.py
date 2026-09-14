"""Plan-bound closed-world AI writer for the clinician-facing Szondi report.

V3 moves composition authority out of the language model. The deterministic
``ClinicalReportPlan`` decides which already-active P2B findings may occupy one
narrative unit; the v1.3 voice compiler decides machine-checkable presentation
requirements. The model is only the writer inside those boundaries.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .clinical_ai_preview import DEFAULT_PREVIEW_MODEL, OPENAI_RESPONSES_URL
from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_report_ai import (
    ClinicalNarrativeBlock,
    ClinicalReportAIResult,
    _require_visible_text,
    _response_output_text,
    build_clinical_report_ai_payload,
    validate_clinical_report_blocks,
)
from .clinical_report_plan import (
    CLINICAL_REPORT_PLAN_VERSION,
    ClinicalReportPlan,
    build_clinical_report_plan,
)
from .clinical_report_voice import (
    CLINICAL_REPORT_VOICE_SPEC_VERSION,
    validate_clinical_report_voice,
    voice_directives_payload,
)


CLINICAL_REPORT_AI_CONTRACT_VERSION = "SZONDI3_CLINICAL_REPORT_ALPHA_V3"
_ALLOWED_AI_SCOPES = frozenset({"PROFILE", "SERIES"})
_EXAMPLE_PREFIXES = (
    "Exemplu explicativ:",
    "Contrast discriminativ:",
    "Bifurcație ilustrativă:",
    # Legacy V2 markers remain accepted while the renderer transition is staged.
    "Exemplu pur ilustrativ:",
    "O manifestare compatibilă ar putea fi:",
)


_AI_INSTRUCTIONS = """You are the clinician-facing WRITER of Szondi3.

The supplied JSON payload is your COMPLETE universe. Do not use pretraining,
remembered Szondi theory, web knowledge, contemporary diagnostic knowledge or
psychological plausibility to add meaning. The deterministic engine has already
decided WHAT is active and the report_plan has already decided WHAT MAY BE COMPOSED.
You decide only HOW to explain each planned unit in clinically useful Romanian.

BINDING REPORT PLAN
- report_plan.units is mandatory and exhaustive.
- Return EXACTLY one block for every plan unit, in the same order.
- block_id MUST equal unit_id.
- scope and profile_number MUST equal the plan unit.
- Copy support_claim_ids, support_fact_ids, support_doctrine_ids and
  anti_inference_ids_applied EXACTLY from that unit, in the supplied order.
- Never merge two plan units. Never split one plan unit. Never create a bridge
  between separate units. Coexistence in the same profile is not a bridge.
- E.K.P. is outside this writer contract.

CLINICAL VOICE
Write natural Romanian. German is never the main explanatory language. A German
term may appear once when it carries conceptual identity, but immediately explain
it in Romanian. Prefer verbs and movements over stacks of theoretical nouns.
After at most two or three abstract explanatory sentences, make the mechanism
visible through a concrete scene, contrast or bifurcation whenever the unit's
example policy permits it.

For a normal unit, provide at least one concrete hypothetical micro-scene. Good
examples show WHAT THE MECHANISM DOES, not merely repeat the label. When useful,
add a discriminative contrast (what resembles the mechanism but is not yet the
same thing) and/or a bifurcation (two possible outcomes when doctrine leaves the
question open). Examples must stay semantically isolated inside the current plan
unit. They must never import another factor/vector merely because it exists in the
case.

Every example item must begin visibly with one of these exact markers:
- "Exemplu explicativ:"
- "Contrast discriminativ:"
- "Bifurcație ilustrativă:"
- "Exemplu pur ilustrativ:"
- "O manifestare compatibilă ar putea fi:"

For units marked OPTIONAL_CANONICAL_PREFERRED, especially suicide/homicide or
other severe forensic content, do not invent a dramatic patient scene merely to
satisfy style. A concise doctrinal explanation may be safer; if the supplied
canonical material itself contains a case vignette, it may be used only within the
meaning already authorized by the plan.

HARD TERMS: DO NOT SOFTEN THE TERM; CONTROL THE PREDICATION.
voice_directives may mark source-authorized Romanian hard terms as mandatory.
Those terms MUST remain visibly present. Do not replace "narcisic" with a softer
phrase such as "centrat pe sine"; do not replace "sadism" with generic "energie";
do not replace "perversiune" with "sexualitate atipică"; do not replace
"criminalitate" with "dificultăți sociale".

A mandatory term is NOT automatically a fact about the person. Respect each hard
term's predication_scope and forbidden_attributions. DOCTRINE_ONLY means: state
what Szondi/the authorized doctrine names, but do not say that the person IS that
category. Historical sexual terms must remain historically/directly visible when
authorized, while orientation or conduct is not attributed without explicit case
support. Doctrinal suicide/homicide vocabulary is not a current risk assessment.

CLINICAL FORMULATION UNIT
For each plan unit, aim for this progression where semantically possible:
1. Name the movement in direct Romanian.
2. Give a short plain-language formula that makes it graspable.
3. Make it visible in one concrete hypothetical scene.
4. Contrast it with a nearby but different phenomenon when useful.
5. If regulation/outcome is open, show two possible branches without choosing one.
6. Ask one to four interview questions that request real situations rather than
   asking the patient to confirm the theory.
7. State only the case-relevant inference limit supplied by the unit.

Do not write a glossary. Do not explain software. Do not produce a P2B dump. Do not
create a whole-person portrait from independent units. Do not invent biography,
trauma, motive, relationship history, diagnosis, prognosis, heredity, sexual
orientation, committed acts or current risk.

SOURCE FORCE
Preserve assertion strength exactly. Possibility/probability language remains
qualified. A categorical authorized historical term remains categorical at the
DOCTRINAL level, but is not silently promoted to a categorical statement about the
person.

VISIBLE FIELDS
- title: Romanian clinical heading, preferably naming the movement rather than a
  German label.
- szondi_reading: concise source-faithful meaning; Romanian first.
- clinical_formulation: make the same authorized movement intelligible, not milder.
- illustrative_examples: zero to four marked items according to example_policy.
- exploration_questions: one to four concrete clinical questions.
- relevant_limit: one concise boundary when materially needed; otherwise null.

Return only JSON matching the response schema.
"""


_BLOCK_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "blocks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "block_id": {"type": "string"},
                    "scope": {"type": "string", "enum": ["PROFILE", "SERIES"]},
                    "profile_number": {"type": ["integer", "null"]},
                    "title": {"type": "string"},
                    "szondi_reading": {"type": "string"},
                    "clinical_formulation": {"type": "string"},
                    "illustrative_examples": {
                        "type": "array",
                        "items": {"type": "string"},
                        "maxItems": 4,
                    },
                    "exploration_questions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "maxItems": 4,
                    },
                    "relevant_limit": {"type": ["string", "null"]},
                    "support_claim_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                    },
                    "support_fact_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                    },
                    "support_doctrine_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                    },
                    "anti_inference_ids_applied": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "block_id",
                    "scope",
                    "profile_number",
                    "title",
                    "szondi_reading",
                    "clinical_formulation",
                    "illustrative_examples",
                    "exploration_questions",
                    "relevant_limit",
                    "support_claim_ids",
                    "support_fact_ids",
                    "support_doctrine_ids",
                    "anti_inference_ids_applied",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["blocks"],
    "additionalProperties": False,
}


def build_clinical_report_ai_payload_v3(packet: ClinicalEvidencePacket) -> dict[str, Any]:
    """Build the finite evidence universe plus its deterministic writing plan."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report AI V3 requires a ClinicalEvidencePacket")
    plan = build_clinical_report_plan(packet)
    payload = build_clinical_report_ai_payload(packet)
    payload["ai_contract_version"] = CLINICAL_REPORT_AI_CONTRACT_VERSION
    payload["report_plan"] = plan.to_dict()
    payload["voice_directives"] = voice_directives_payload(packet, plan)
    return payload


def build_openai_clinical_report_request_v3(
    packet: ClinicalEvidencePacket,
    *,
    model: str = DEFAULT_PREVIEW_MODEL,
) -> dict[str, Any]:
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical report AI model identifier must not be empty")
    payload = json.dumps(
        build_clinical_report_ai_payload_v3(packet),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "model": model,
        "store": False,
        "tools": [],
        "instructions": _AI_INSTRUCTIONS,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Write the clinician report using only this closed-world planned payload:\n" + payload,
                    }
                ],
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "szondi3_clinical_report_alpha_v3",
                "strict": True,
                "schema": _BLOCK_SCHEMA,
            }
        },
    }


def _parse_block_v3(raw: Any) -> ClinicalNarrativeBlock:
    if not isinstance(raw, dict):
        raise ValueError("Each clinical report V3 block must be an object")
    required = {
        "block_id", "scope", "profile_number", "title", "szondi_reading",
        "clinical_formulation", "illustrative_examples", "exploration_questions",
        "relevant_limit", "support_claim_ids", "support_fact_ids",
        "support_doctrine_ids", "anti_inference_ids_applied",
    }
    if set(raw) != required:
        raise ValueError("Clinical report V3 block has missing or unexpected fields")

    scope = raw["scope"]
    if scope not in _ALLOWED_AI_SCOPES:
        raise ValueError("Clinical report AI V3 accepts only PROFILE or SERIES scope")
    profile_number = raw["profile_number"]
    if profile_number is not None and not isinstance(profile_number, int):
        raise ValueError("profile_number must be an integer or null")

    examples = raw["illustrative_examples"]
    if not isinstance(examples, list) or len(examples) > 4:
        raise ValueError("illustrative_examples must contain zero to four items")
    parsed_examples = tuple(
        _require_visible_text(item, "illustrative_example") for item in examples
    )
    for example in parsed_examples:
        if not example.startswith(_EXAMPLE_PREFIXES):
            raise ValueError(
                "Illustrative examples must use an authorized hypothetical/contrast marker"
            )

    questions = raw["exploration_questions"]
    if not isinstance(questions, list) or not 1 <= len(questions) <= 4:
        raise ValueError("exploration_questions must contain one to four items")
    parsed_questions = tuple(
        _require_visible_text(item, "exploration_question") for item in questions
    )

    relevant_limit = raw["relevant_limit"]
    if relevant_limit is not None:
        relevant_limit = _require_visible_text(relevant_limit, "relevant_limit")

    arrays: dict[str, tuple[str, ...]] = {}
    for field_name in (
        "support_claim_ids", "support_fact_ids", "support_doctrine_ids",
        "anti_inference_ids_applied",
    ):
        value = raw[field_name]
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{field_name} must be a JSON array of strings")
        arrays[field_name] = tuple(value)

    return ClinicalNarrativeBlock(
        block_id=_require_visible_text(raw["block_id"], "block_id"),
        scope=scope,
        profile_number=profile_number,
        title=_require_visible_text(raw["title"], "title"),
        szondi_reading=_require_visible_text(raw["szondi_reading"], "szondi_reading"),
        clinical_formulation=_require_visible_text(
            raw["clinical_formulation"], "clinical_formulation"
        ),
        exploration_questions=parsed_questions,
        relevant_limit=relevant_limit,
        support_claim_ids=arrays["support_claim_ids"],
        support_fact_ids=arrays["support_fact_ids"],
        support_doctrine_ids=arrays["support_doctrine_ids"],
        anti_inference_ids_applied=arrays["anti_inference_ids_applied"],
        illustrative_examples=parsed_examples,
    )


def _validate_plan_binding(
    plan: ClinicalReportPlan,
    blocks: tuple[ClinicalNarrativeBlock, ...],
) -> None:
    if len(blocks) != len(plan.units):
        raise ValueError(
            "Clinical report AI V3 must return exactly one block for every report-plan unit"
        )
    for position, (unit, block) in enumerate(zip(plan.units, blocks), start=1):
        if block.block_id != unit.unit_id:
            raise ValueError(
                f"Clinical report AI V3 block {position} must use planned unit id {unit.unit_id}"
            )
        if block.scope != unit.scope or block.profile_number != unit.profile_number:
            raise ValueError(
                f"Clinical report AI V3 block {unit.unit_id} changed planned scope/profile"
            )
        expected = (
            unit.support_claim_ids,
            unit.support_fact_ids,
            unit.support_doctrine_ids,
            unit.anti_inference_ids,
        )
        actual = (
            block.support_claim_ids,
            block.support_fact_ids,
            block.support_doctrine_ids,
            block.anti_inference_ids_applied,
        )
        if actual != expected:
            raise ValueError(
                f"Clinical report AI V3 block {unit.unit_id} changed its deterministic support envelope"
            )


def validate_clinical_report_blocks_v3(
    packet: ClinicalEvidencePacket,
    blocks: tuple[ClinicalNarrativeBlock, ...],
) -> tuple[ClinicalNarrativeBlock, ...]:
    """Validate plan identity, epistemic support and executable voice requirements."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report AI V3 validation requires a ClinicalEvidencePacket")
    if not isinstance(blocks, tuple):
        raise TypeError("Clinical report AI V3 blocks must be supplied as a tuple")
    plan = build_clinical_report_plan(packet)
    _validate_plan_binding(plan, blocks)
    validated = validate_clinical_report_blocks(packet, blocks)
    validate_clinical_report_voice(packet, plan, validated)
    return validated


def parse_openai_clinical_report_response_v3(
    packet: ClinicalEvidencePacket,
    response: dict[str, Any],
) -> ClinicalReportAIResult:
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report AI V3 parsing requires a ClinicalEvidencePacket")
    if not isinstance(response, dict):
        raise TypeError("Clinical report AI V3 response must be a dictionary")
    try:
        decoded = json.loads(_response_output_text(response))
    except json.JSONDecodeError as exc:
        raise ValueError("Clinical report AI V3 output is not valid JSON") from exc
    if not isinstance(decoded, dict) or set(decoded) != {"blocks"}:
        raise ValueError("Clinical report AI V3 JSON must contain only blocks")
    if not isinstance(decoded["blocks"], list):
        raise ValueError("Clinical report AI V3 blocks must be a JSON array")

    blocks = tuple(_parse_block_v3(item) for item in decoded["blocks"])
    validated = validate_clinical_report_blocks_v3(packet, blocks)
    response_id = response.get("id")
    model = response.get("model")
    if not isinstance(response_id, str) or not response_id.strip():
        raise ValueError("Clinical report AI V3 response lacks response id")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical report AI V3 response lacks model identifier")
    return ClinicalReportAIResult(
        contract_version=CLINICAL_REPORT_AI_CONTRACT_VERSION,
        provider="OPENAI_RESPONSES_API",
        model=model.strip(),
        response_id=response_id.strip(),
        blocks=validated,
    )


def request_openai_clinical_report_response_v3(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = 90.0,
) -> dict[str, Any]:
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("OpenAI API key must be supplied explicitly for clinical report AI")
    if timeout_seconds <= 0:
        raise ValueError("Clinical report AI timeout must be positive")
    body = json.dumps(
        build_openai_clinical_report_request_v3(packet, model=model),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    request = Request(
        OPENAI_RESPONSES_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as handle:
            raw_response = handle.read().decode("utf-8")
    except HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace").strip()
        except Exception:
            detail = ""
        suffix = f": {detail[:500]}" if detail else ""
        raise RuntimeError(
            f"Clinical report AI request failed with HTTP {exc.code}{suffix}"
        ) from exc
    except URLError as exc:
        raise RuntimeError("Clinical report AI request failed at the network layer") from exc
    try:
        response = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Clinical report AI endpoint returned invalid JSON") from exc
    if not isinstance(response, dict):
        raise RuntimeError("Clinical report AI endpoint returned a non-object JSON payload")
    return response


def run_openai_clinical_report(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = 90.0,
) -> ClinicalReportAIResult:
    """Run the plan-bound V3 writer and fail closed on local validation."""
    response = request_openai_clinical_report_response_v3(
        packet,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    return parse_openai_clinical_report_response_v3(packet, response)


__all__ = [
    "CLINICAL_REPORT_AI_CONTRACT_VERSION",
    "CLINICAL_REPORT_PLAN_VERSION",
    "CLINICAL_REPORT_VOICE_SPEC_VERSION",
    "ClinicalNarrativeBlock",
    "ClinicalReportAIResult",
    "build_clinical_report_ai_payload_v3",
    "build_openai_clinical_report_request_v3",
    "parse_openai_clinical_report_response_v3",
    "request_openai_clinical_report_response_v3",
    "run_openai_clinical_report",
    "validate_clinical_report_blocks_v3",
]
