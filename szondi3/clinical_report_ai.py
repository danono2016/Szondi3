"""Closed-world AI formulation contract for the Alpha clinician report.

The deterministic engine decides which Szondian meanings are active. This module
hands only those meanings, their exact observed morphology, linked canonical
doctrine and anti-inferences to the language model. The model may expand the
meaning semantically, but it may not expand the doctrine.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .clinical_ai_preview import DEFAULT_PREVIEW_MODEL, OPENAI_RESPONSES_URL
from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_synthesis import SynthesisProposition, validate_synthesis_propositions


CLINICAL_REPORT_AI_CONTRACT_VERSION = "SZONDI3_CLINICAL_REPORT_ALPHA_V2"
_ALLOWED_AI_SCOPES = frozenset({"PROFILE", "SERIES"})

# These tokens belong to implementation/audit surfaces. Their presence in visible
# AI prose is a product-contract violation, even when the support envelope is valid.
_FORBIDDEN_VISIBLE_TECHNICAL = re.compile(
    r"(?:IC_SZONDI_PRIMARY_|DR_SZ_|SOURCE_VERIFIED|\bAPPROVED\b|\bAVAILABLE\b|"
    r"\bNOT_APPLICABLE\b|source-grounded|quantum-aware|production mode|"
    r"release policy|synthesis contract)",
    re.IGNORECASE,
)

_AI_INSTRUCTIONS = """You are the clinician-facing language component of Szondi3.

The JSON evidence payload supplied by the user is your COMPLETE universe for this
request. Do not use pretraining, remembered Szondi theory, web knowledge,
contemporary diagnostic knowledge, psychodynamic associations, or assumptions
about the person to add meaning.

GOVERNING PRINCIPLE: semantic expansion without doctrinal expansion.
The deterministic program has already decided WHAT Szondian meanings are active.
Your job is to make those meanings understandable, rich, concrete and clinically
readable in Romanian. You may explain, reformulate, contrast, illustrate and order;
you may not create a new Szondian meaning, a new bridge between findings, or a new
fact about the person.

Do NOT aim for brevity merely for its own sake. A block may be several substantial
paragraphs when each paragraph adds meaning. Avoid filler, generic psychotherapy
language, repetitive disclaimers and ritual phrases that say little. The desired
result is a dense explanatory reading, not a software summary and not a list of
labels.

VISIBLE STRUCTURE OF EACH BLOCK:
1. title: a clear Romanian heading tied to the exact reaction/configuration.
2. szondi_reading: unfold faithfully what the active finding means inside Szondi's
   own conceptual system. Preserve source-authorized baroque, categorical, direct,
   archaic, sexually explicit, pathologizing or historically uncomfortable terms.
   Do NOT euphemize, politically sanitize, moralize or modernize them. Explain the
   important German terms immediately in Romanian at first occurrence.
3. clinical_formulation: explain the SAME authorized content in natural Romanian.
   You may turn the idea around from several angles: what movement or relation the
   term names, what it contrasts with, what a more flexible versus more rigid
   expression of that SAME movement could look like, and why the distinction may be
   useful clinically. These are explanatory perspectives, not extra doctrine.
4. illustrative_examples: zero to two short hypothetical micro-scenes. Every item
   MUST visibly begin with either "Exemplu pur ilustrativ:" or
   "O manifestare compatibilă ar putea fi:". Examples exist only to clarify the
   authorized meaning; they are never evidence that the person actually behaves
   that way. Do not smuggle biography, trauma, diagnosis, motive, relationship
   history or an unauthorized factor-to-factor bridge into an example.
5. exploration_questions: one to four precise questions/directions that help a
   clinician test whether the authorized testological meaning has a correspondent
   in the real case. Questions must not presuppose that the hypothetical example is
   true.
6. relevant_limit: at most one concise case-relevant boundary when materially
   needed by the active finding's anti-inferences. Do not flood the block with
   general method disclaimers.

EXACT MORPHOLOGY RULE:
The payload contains profile_morphology with the exact observed factor symbols,
quantum levels, forced-null flags and vector symbols. When a PROFILE finding concerns
an observed reaction or quantum tension, NAME the exact reaction whenever the
finding and morphology make it available (for example "s +!"), instead of saying
"factorul marcat", "reacția respectivă" or another vague substitute. Morphology is
context for wording; it does NOT authorize an interpretation for a factor/vector
that lacks an active finding.

LANGUAGE RULES:
- Visible prose is Romanian.
- Preserve an important German Szondian term when it carries conceptual identity,
  but at its FIRST occurrence immediately give a complete, clear Romanian
  translation/explanation in parentheses. The clinician must not need German.
- If you reproduce a German quotation, immediately provide its complete Romanian
  translation in the same visible field.
- No English software vocabulary, claim IDs, doctrine IDs, source IDs, hashes or
  runtime statuses in visible prose. IDs belong ONLY in support_* arrays.

FIDELITY RULES:
- Preserve the source's assertion strength. kann/scheint/Annahme/possibility must
  remain qualified; a categorical source-authorized term must not be weakened just
  because it is historically uncomfortable.
- Do not invent a DSM/ICD equivalence.
- Do not infer concrete biography, committed acts, stable global traits, prognosis,
  identity or heredity unless the active finding itself authorizes that exact scope.
- Do not rescore, normalize, repair nulls, infer quantum, calculate percentages or
  create interpretive weights.
- Do not present an illustrative example as a description of this person.

ANTI-MOSAIKSPIEL RULE:
A block may cite more than one active claim only if those claims are alternate or
complementary formulations of the SAME deterministic support fact bundle supplied
for the same scope. Never combine independent factors/vectors into a synthetic
whole-person interpretation merely because they coexist. If an authorized
composition bridge is absent from the payload, keep the findings separate. A
psychologically plausible bridge is still forbidden when it is not authorized.

SCOPE RULE:
Generate blocks only for PROFILE or SERIES findings supplied in active_case_findings.
Do not generate a block for an experimental complement (E.K.P.) in this Alpha
contract. E.K.P. remains a separate testological surface until a dedicated
foreground/complement composition contract exists.

SUPPORT RULE:
For every block copy the COMPLETE support_claim_ids, support_fact_ids,
support_doctrine_ids and anti_inference_ids_applied corresponding to what you cite.
The local validator will reject incomplete or foreign support. An empty blocks array
is valid if no faithful block can be produced.

Return only the JSON required by the response schema.
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
                        "maxItems": 2,
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


@dataclass(frozen=True, slots=True)
class ClinicalNarrativeBlock:
    block_id: str
    scope: str
    profile_number: int | None
    title: str
    szondi_reading: str
    clinical_formulation: str
    exploration_questions: tuple[str, ...]
    relevant_limit: str | None
    support_claim_ids: tuple[str, ...]
    support_fact_ids: tuple[str, ...]
    support_doctrine_ids: tuple[str, ...]
    anti_inference_ids_applied: tuple[str, ...]
    illustrative_examples: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ClinicalReportAIResult:
    contract_version: str
    provider: str
    model: str
    response_id: str
    blocks: tuple[ClinicalNarrativeBlock, ...]


def _eligible_findings(packet: ClinicalEvidencePacket) -> tuple[Any, ...]:
    return tuple(
        item
        for item in packet.report.findings
        if item.assertion_mode != "LIMITATION" and item.scope in _ALLOWED_AI_SCOPES
    )


def build_clinical_report_ai_payload(packet: ClinicalEvidencePacket) -> dict[str, Any]:
    """Build the finite, case-specific evidence universe for clinical wording."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report AI requires a ClinicalEvidencePacket")

    findings = _eligible_findings(packet)
    doctrine_ids = {
        doctrine_id for finding in findings for doctrine_id in finding.doctrine_ids
    }
    evidence = tuple(
        item for item in packet.canonical_evidence if item.doctrine_id in doctrine_ids
    )
    report = packet.report.to_dict()
    eligible_keys = {
        (item.claim_id, item.scope, item.profile_number) for item in findings
    }
    finding_payload = [
        item
        for item in report["findings"]
        if (item["claim_id"], item["scope"], item["profile_number"]) in eligible_keys
    ]

    return {
        "schema_version": packet.schema_version,
        "ai_contract_version": CLINICAL_REPORT_AI_CONTRACT_VERSION,
        "profile_count": packet.report.header.profile_count,
        "profile_morphology": report["observations"],
        "factor_series": [
            {
                "factor": item.factor,
                "symbols": list(item.symbols),
                "base_symbols": list(item.base_symbols),
                "tensioned_profiles": list(item.tensioned_profiles),
                "quantum_total": item.quantum_total,
            }
            for item in packet.factor_series
        ],
        "vector_series": [
            {
                "vector": item.vector,
                "factors": list(item.factors),
                "symbols": [list(pair) for pair in item.symbols],
                "base_symbols": [list(pair) for pair in item.base_symbols],
            }
            for item in packet.vector_series
        ],
        "active_case_findings": finding_payload,
        "canonical_evidence": [
            {
                "doctrine_id": item.doctrine_id,
                "source_id": item.source_id,
                "source_language": item.source_language,
                "source_excerpt": item.source_excerpt,
                "romanian_rendering": item.romanian_rendering,
                "doctrinal_statement": item.doctrinal_statement,
                "assertion_strength": item.assertion_strength,
                "scope_notes": list(item.scope_notes),
            }
            for item in evidence
        ],
        "uncertainties": report["uncertainties"],
    }


def build_openai_clinical_report_request(
    packet: ClinicalEvidencePacket,
    *,
    model: str = DEFAULT_PREVIEW_MODEL,
) -> dict[str, Any]:
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical report AI model identifier must not be empty")
    payload = json.dumps(
        build_clinical_report_ai_payload(packet),
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
                        "text": "Produce the Alpha clinical report blocks using only this payload:\n" + payload,
                    }
                ],
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "szondi3_clinical_report_alpha_v2",
                "strict": True,
                "schema": _BLOCK_SCHEMA,
            }
        },
    }


def _response_output_text(response: dict[str, Any]) -> str:
    if response.get("status") != "completed":
        detail = response.get("incomplete_details") or response.get("error") or "unknown"
        raise ValueError(f"Clinical report AI response is not completed: {detail}")
    direct = response.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct

    texts: list[str] = []
    refusals: list[str] = []
    for item in response.get("output") or ():
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for part in item.get("content") or ():
            if not isinstance(part, dict):
                continue
            if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                texts.append(part["text"])
            elif part.get("type") == "refusal" and isinstance(part.get("refusal"), str):
                refusals.append(part["refusal"])
    if refusals:
        raise ValueError("Clinical report AI model refused the formulation request")
    if len(texts) != 1 or not texts[0].strip():
        raise ValueError("Clinical report AI response must contain exactly one output_text payload")
    return texts[0]


def _require_visible_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    if _FORBIDDEN_VISIBLE_TECHNICAL.search(value):
        raise ValueError(f"{field_name} leaks technical/audit vocabulary")
    return value.strip()


def _parse_block(raw: Any) -> ClinicalNarrativeBlock:
    if not isinstance(raw, dict):
        raise ValueError("Each clinical report block must be an object")
    required = {
        "block_id", "scope", "profile_number", "title", "szondi_reading",
        "clinical_formulation", "exploration_questions", "relevant_limit",
        "support_claim_ids", "support_fact_ids", "support_doctrine_ids",
        "anti_inference_ids_applied",
    }
    allowed = required | {"illustrative_examples"}
    if not required.issubset(raw) or not set(raw).issubset(allowed):
        raise ValueError("Clinical report block has missing or unexpected fields")

    questions = raw["exploration_questions"]
    if not isinstance(questions, list) or not 1 <= len(questions) <= 4:
        raise ValueError("exploration_questions must contain one to four items")
    parsed_questions = tuple(
        _require_visible_text(item, "exploration_question") for item in questions
    )

    examples = raw.get("illustrative_examples", [])
    if not isinstance(examples, list) or len(examples) > 2:
        raise ValueError("illustrative_examples must contain zero to two items")
    parsed_examples = tuple(
        _require_visible_text(item, "illustrative_example") for item in examples
    )
    for example in parsed_examples:
        if not example.startswith(("Exemplu pur ilustrativ:", "O manifestare compatibilă ar putea fi:")):
            raise ValueError("Illustrative examples must be explicitly marked as hypothetical")

    relevant_limit = raw["relevant_limit"]
    if relevant_limit is not None:
        relevant_limit = _require_visible_text(relevant_limit, "relevant_limit")

    array_fields = (
        "support_claim_ids", "support_fact_ids", "support_doctrine_ids",
        "anti_inference_ids_applied",
    )
    for field_name in array_fields:
        if not isinstance(raw[field_name], list):
            raise ValueError(f"{field_name} must be a JSON array")

    return ClinicalNarrativeBlock(
        block_id=_require_visible_text(raw["block_id"], "block_id"),
        scope=raw["scope"],
        profile_number=raw["profile_number"],
        title=_require_visible_text(raw["title"], "title"),
        szondi_reading=_require_visible_text(raw["szondi_reading"], "szondi_reading"),
        clinical_formulation=_require_visible_text(raw["clinical_formulation"], "clinical_formulation"),
        exploration_questions=parsed_questions,
        relevant_limit=relevant_limit,
        support_claim_ids=tuple(raw["support_claim_ids"]),
        support_fact_ids=tuple(raw["support_fact_ids"]),
        support_doctrine_ids=tuple(raw["support_doctrine_ids"]),
        anti_inference_ids_applied=tuple(raw["anti_inference_ids_applied"]),
        illustrative_examples=parsed_examples,
    )


def validate_clinical_report_blocks(
    packet: ClinicalEvidencePacket,
    blocks: tuple[ClinicalNarrativeBlock, ...],
) -> tuple[ClinicalNarrativeBlock, ...]:
    """Fail closed on support, scope and synthetic Mosaikspiel joins."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report validation requires a ClinicalEvidencePacket")
    if not isinstance(blocks, tuple):
        raise TypeError("Clinical report blocks must be supplied as a tuple")

    finding_index = {
        (item.claim_id, item.scope, item.profile_number): item
        for item in packet.report.findings
    }
    block_ids: set[str] = set()
    propositions: list[SynthesisProposition] = []

    for block in blocks:
        if not isinstance(block, ClinicalNarrativeBlock):
            raise TypeError("Unexpected clinical narrative block type")
        if block.scope not in _ALLOWED_AI_SCOPES:
            raise ValueError("Clinical report AI accepts only PROFILE or SERIES scope")
        if block.block_id in block_ids:
            raise ValueError(f"Duplicate clinical report block identity: {block.block_id}")
        block_ids.add(block.block_id)

        matched = []
        for claim_id in block.support_claim_ids:
            key = (claim_id, block.scope, block.profile_number)
            try:
                finding = finding_index[key]
            except KeyError as exc:
                raise ValueError(
                    f"Clinical report block cites inactive claim: {claim_id}"
                ) from exc
            if finding.assertion_mode == "LIMITATION":
                raise ValueError("General LIMITATION claims cannot become patient narrative blocks")
            matched.append(finding)

        if len(matched) > 1:
            fact_bundles = {frozenset(item.support_fact_ids) for item in matched}
            if len(fact_bundles) != 1:
                raise ValueError(
                    "Clinical report block may combine claims only when they share the same deterministic fact bundle"
                )

        visible_text = "\n".join(
            (
                block.title,
                block.szondi_reading,
                block.clinical_formulation,
                *block.illustrative_examples,
                *block.exploration_questions,
                block.relevant_limit or "",
            )
        )
        propositions.append(
            SynthesisProposition(
                proposition_id=block.block_id,
                scope=block.scope,
                profile_number=block.profile_number,
                text=visible_text,
                support_claim_ids=block.support_claim_ids,
                support_fact_ids=block.support_fact_ids,
                support_doctrine_ids=block.support_doctrine_ids,
                anti_inference_ids_applied=block.anti_inference_ids_applied,
            )
        )

    validate_synthesis_propositions(packet, tuple(propositions))
    return blocks


def parse_openai_clinical_report_response(
    packet: ClinicalEvidencePacket,
    response: dict[str, Any],
) -> ClinicalReportAIResult:
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report AI parsing requires a ClinicalEvidencePacket")
    if not isinstance(response, dict):
        raise TypeError("Clinical report AI response must be a dictionary")
    try:
        decoded = json.loads(_response_output_text(response))
    except json.JSONDecodeError as exc:
        raise ValueError("Clinical report AI output is not valid JSON") from exc
    if not isinstance(decoded, dict) or set(decoded) != {"blocks"}:
        raise ValueError("Clinical report AI JSON must contain only blocks")
    if not isinstance(decoded["blocks"], list):
        raise ValueError("Clinical report AI blocks must be a JSON array")

    blocks = tuple(_parse_block(item) for item in decoded["blocks"])
    validated = validate_clinical_report_blocks(packet, blocks)
    response_id = response.get("id")
    model = response.get("model")
    if not isinstance(response_id, str) or not response_id.strip():
        raise ValueError("Clinical report AI response lacks response id")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical report AI response lacks model identifier")
    return ClinicalReportAIResult(
        contract_version=CLINICAL_REPORT_AI_CONTRACT_VERSION,
        provider="OPENAI_RESPONSES_API",
        model=model,
        response_id=response_id,
        blocks=validated,
    )


def request_openai_clinical_report_response(
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
        build_openai_clinical_report_request(packet, model=model),
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
        raise RuntimeError(f"Clinical report AI request failed with HTTP {exc.code}") from exc
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
    response = request_openai_clinical_report_response(
        packet,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    return parse_openai_clinical_report_response(packet, response)
