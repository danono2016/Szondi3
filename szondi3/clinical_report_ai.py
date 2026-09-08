"""Closed-world AI formulation contract for the Alpha clinician report.

This module is deliberately narrower than a general narrative engine. It receives
one already-built ``ClinicalEvidencePacket``, filters it to active case-specific
(non-LIMITATION) findings, asks one model for structured Romanian clinical wording,
and validates every returned block against Szondi3's existing deterministic support
envelope before the block can be shown to a clinician.

The model never scores the test, activates claims, creates doctrine, invents support
percentages, or releases a clinical conclusion autonomously. Output is ephemeral
Alpha material for clinician review.
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


CLINICAL_REPORT_AI_CONTRACT_VERSION = "SZONDI3_CLINICAL_REPORT_ALPHA_V1"

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

Your task is NOT to produce a diagnosis and NOT to summarize every internal claim.
Create concise clinical reading blocks only for the supplied active case-specific
findings. General LIMITATION claims are intentionally absent and must not be
re-created as patient findings.

Each block has four visible layers:
1. title: a short Romanian clinical heading; no technical IDs.
2. szondi_reading: state faithfully what the cited active finding means inside
   Szondi's own conceptual system. Preserve source-authorized baroque, categorical,
   direct, archaic, sexually explicit, pathologizing or historically uncomfortable
   terminology. DO NOT euphemize, politically sanitize, moralize, modernize or
   replace it with bland contemporary psychology. You may use linked doctrine to
   explain the meaning already authorized by the active finding, but doctrine does
   not authorize a new person-level conclusion beyond that finding.
3. clinical_formulation: make the same authorized meaning intelligible in ordinary
   Romanian clinical language WITHOUT softening or replacing Szondi's named/direct
   concepts. Do not turn a reaction/profile state into a stable global trait unless
   the cited finding itself authorizes that scope.
4. exploration_questions: 1 to 4 concise questions/directions for clinical
   exploration. They are hypotheses to examine, never invented biography, behavior,
   trauma, diagnosis, prognosis, identity, heredity or historical fact.

Optional relevant_limit: include ONE concise case-relevant boundary only when the
cited finding's anti-inferences make it materially necessary. Do not flood the
report with general safeguards.

LANGUAGE RULES:
- Visible prose is Romanian.
- Preserve an important German Szondian term when it carries conceptual identity,
  but at its FIRST occurrence immediately give a complete, clear Romanian
  translation/explanation in parentheses. The clinician must not need German.
- If you reproduce any German quotation, immediately provide its complete Romanian
  translation in the same visible field.
- Never expose claim IDs, doctrine IDs, source IDs, hashes, runtime statuses or
  English software vocabulary in title/szondi_reading/clinical_formulation/
  exploration_questions/relevant_limit. IDs belong ONLY in support_* arrays.

FIDELITY RULES:
- If the source/finding says kann, scheint, Annahme, possibility, suspicion or other
  qualified language, preserve that degree of uncertainty. Do not upgrade it.
- Conversely, do not weaken a categorical source-authorized expression merely
  because it is severe or politically uncomfortable.
- Do not invent a modern DSM/ICD equivalence.
- Do not infer a concrete biography or committed act from a testological possibility.
- Do not rescore, normalize, repair nulls, infer quantum, or calculate percentages.
- There are NO interpretive support percentages in this Alpha contract.

ANTI-MOSAIKSPIEL RULE:
A block may cite more than one active claim only if those claims are alternate or
complementary formulations of the SAME deterministic support fact bundle supplied
for the same scope. Never combine independent factors/vectors into a synthetic
whole-person interpretation just because they occur together. If no authorized
bridge exists, keep them in separate blocks.

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
                    "scope": {
                        "type": "string",
                        "enum": ["PROFILE", "SERIES", "EXPERIMENTAL_COMPLEMENT"],
                    },
                    "profile_number": {"type": ["integer", "null"]},
                    "title": {"type": "string"},
                    "szondi_reading": {"type": "string"},
                    "clinical_formulation": {"type": "string"},
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


@dataclass(frozen=True, slots=True)
class ClinicalReportAIResult:
    contract_version: str
    provider: str
    model: str
    response_id: str
    blocks: tuple[ClinicalNarrativeBlock, ...]


def _eligible_findings(packet: ClinicalEvidencePacket) -> tuple[Any, ...]:
    return tuple(
        item for item in packet.report.findings
        if item.assertion_mode != "LIMITATION"
    )


def build_clinical_report_ai_payload(packet: ClinicalEvidencePacket) -> dict[str, Any]:
    """Build a reduced, case-specific closed-world payload for clinical wording."""
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
        item for item in report["findings"]
        if (item["claim_id"], item["scope"], item["profile_number"]) in eligible_keys
    ]

    return {
        "schema_version": packet.schema_version,
        "profile_count": packet.report.header.profile_count,
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
                "name": "szondi3_clinical_report_alpha",
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
    expected = {
        "block_id", "scope", "profile_number", "title", "szondi_reading",
        "clinical_formulation", "exploration_questions", "relevant_limit",
        "support_claim_ids", "support_fact_ids", "support_doctrine_ids",
        "anti_inference_ids_applied",
    }
    if set(raw) != expected:
        raise ValueError("Clinical report block has missing or unexpected fields")
    questions = raw["exploration_questions"]
    if not isinstance(questions, list) or not 1 <= len(questions) <= 4:
        raise ValueError("exploration_questions must contain one to four items")
    parsed_questions = tuple(
        _require_visible_text(item, "exploration_question") for item in questions
    )
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
    )


def validate_clinical_report_blocks(
    packet: ClinicalEvidencePacket,
    blocks: tuple[ClinicalNarrativeBlock, ...],
) -> tuple[ClinicalNarrativeBlock, ...]:
    """Fail closed on support, patient-limit claims and synthetic Mosaikspiel joins."""
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
