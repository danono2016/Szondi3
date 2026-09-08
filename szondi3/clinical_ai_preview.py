"""Preview-only bridge from a ClinicalEvidencePacket to one OpenAI model call.

This module is deliberately not a general provider framework. It builds one
closed-world Responses API request, disables model tools, requests structured
propositions, parses the returned JSON, and then reuses Szondi3's deterministic
support-envelope validator before exposing any proposition to downstream code.

No API key is stored here. No model output is a clinical report merely because it
was returned by the provider; validation is mandatory and this path remains
preview-only.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_synthesis import (
    SynthesisProposition,
    build_synthesis_validation_context,
    validate_synthesis_propositions,
)


PREVIEW_CONTRACT_VERSION = "SZONDI3_AI_PREVIEW_V1"
DEFAULT_PREVIEW_MODEL = "gpt-5.6-sol"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"

_PREVIEW_INSTRUCTIONS = """You are the language-synthesis component of Szondi3.

Closed-world rule: for Szondian meaning, the ClinicalEvidencePacket supplied in
this request is the complete universe of available evidence. Do not use general
knowledge, pretraining, web knowledge, remembered Szondi theory, or assumptions
about the person to extend it.

You may formulate only person-specific propositions that are already authorized
by active findings in the packet. Canonical doctrine passages are support for
those findings; they do not independently authorize new case-level conclusions.
Morphology and calculations may be described only when an active finding already
authorizes the clinical meaning you state.

For every proposition:
- preserve PROFILE versus SERIES scope exactly;
- cite the active claim_id that authorizes it;
- copy the complete support_fact_ids bundle of that claim in that exact scope;
- copy the complete doctrine_ids bundle of that claim in that exact scope;
- copy the complete anti_inference_ids bundle of the cited finding(s) into
  anti_inference_ids_applied; these IDs are hard guards against unsupported
  extensions, not instructions to soften an assertion the source actually makes;
- respect the finding's assertion_mode, anti_inferences, source_strength_note,
  sensitive_domains, and any uncertainties present in the packet;
- weaken or omit a proposition only when its actual evidentiary support is weaker
  or absent, never merely because Szondi's authorized wording is severe,
  pathologizing, sexually explicit, criminological, historically uncomfortable,
  or incompatible with contemporary sensitivities.

Voice rule: speak from inside Szondi's conceptual system, not about it from the
standpoint of contemporary psychology. In Romanian, preserve source-authorized
Szondian terminology, diagnostic force, directness, conceptual density, dramatic
oppositions and, where the finding supports it, the baroque tension of Szondi's
clinical language. Do not euphemize, politically sanitize, moralize, modernize or
replace a source-authorized term merely to make it sound more contemporary. Terms
such as Triebgefahr, Aggressionsgefahr, Sadismus, Perversion, Verdrängung,
Projektion, Inflation, Zwang, Gewissen, Schicksal and related historical diagnostic
vocabulary remain available at the strength authorized by the active finding.
Stylistic fidelity is not permission to invent doctrine, intensify beyond the
finding, or add unsupported biography, behavior, diagnosis, prognosis or modern
clinical equivalence.

Forbidden: rescoring, repairing unresolved results, inventing diagnoses or traits,
turning testological labels into global personality facts unless the active claim
itself authorizes that scope, converting qualified claims into certainty, creating
person-level meaning directly from a source passage, or adding any Szondian
proposition unsupported by an active claim.

Write proposition text in Romanian in a recognizably Szondian clinical voice,
subject to the exact evidentiary limits above. Return only the JSON object required
by the response schema. An empty propositions array is valid when the packet does
not authorize a proposition.
"""

_PROPOSITION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "propositions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "proposition_id": {"type": "string"},
                    "scope": {"type": "string", "enum": ["PROFILE", "SERIES"]},
                    "profile_number": {"type": ["integer", "null"]},
                    "text": {"type": "string"},
                    "support_claim_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "support_fact_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "support_doctrine_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "anti_inference_ids_applied": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "proposition_id",
                    "scope",
                    "profile_number",
                    "text",
                    "support_claim_ids",
                    "support_fact_ids",
                    "support_doctrine_ids",
                    "anti_inference_ids_applied",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["propositions"],
    "additionalProperties": False,
}


@dataclass(frozen=True, slots=True)
class PreviewSynthesisResult:
    contract_version: str
    provider: str
    model: str
    response_id: str
    propositions: tuple[SynthesisProposition, ...]


@dataclass(frozen=True, slots=True)
class PreviewRejectedProposition:
    position: int
    proposition_id: str | None
    reason: str


@dataclass(frozen=True, slots=True)
class PreviewResponseInspection:
    contract_version: str
    provider: str
    model: str
    response_id: str
    raw_proposition_count: int
    accepted_propositions: tuple[SynthesisProposition, ...]
    rejected_propositions: tuple[PreviewRejectedProposition, ...]


def build_openai_preview_request(
    packet: ClinicalEvidencePacket,
    *,
    model: str = DEFAULT_PREVIEW_MODEL,
) -> dict[str, Any]:
    """Build the one admitted preview request without performing network I/O."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("AI preview requires a ClinicalEvidencePacket")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Preview model identifier must not be empty")

    packet_json = json.dumps(
        packet.to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "model": model,
        "store": False,
        "tools": [],
        "instructions": _PREVIEW_INSTRUCTIONS,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Generate the structured JSON synthesis propositions using only "
                            "this ClinicalEvidencePacket:\n" + packet_json
                        ),
                    }
                ],
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "szondi3_synthesis_preview",
                "strict": True,
                "schema": _PROPOSITION_SCHEMA,
            }
        },
    }


def _response_output_text(response: dict[str, Any]) -> str:
    if response.get("status") != "completed":
        detail = response.get("incomplete_details") or response.get("error") or "unknown"
        raise ValueError(f"OpenAI preview response is not completed: {detail}")

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
        raise ValueError("OpenAI preview model refused the synthesis request")
    if len(texts) != 1 or not texts[0].strip():
        raise ValueError("OpenAI preview response must contain exactly one output_text payload")
    return texts[0]


def _parse_proposition(raw: Any) -> SynthesisProposition:
    if not isinstance(raw, dict):
        raise ValueError("Each preview proposition must be an object")
    expected = {
        "proposition_id",
        "scope",
        "profile_number",
        "text",
        "support_claim_ids",
        "support_fact_ids",
        "support_doctrine_ids",
        "anti_inference_ids_applied",
    }
    if set(raw) != expected:
        raise ValueError("Preview proposition has missing or unexpected fields")

    array_fields = (
        "support_claim_ids",
        "support_fact_ids",
        "support_doctrine_ids",
        "anti_inference_ids_applied",
    )
    for field_name in array_fields:
        if not isinstance(raw[field_name], list):
            raise ValueError(f"{field_name} must be a JSON array")

    return SynthesisProposition(
        proposition_id=raw["proposition_id"],
        scope=raw["scope"],
        profile_number=raw["profile_number"],
        text=raw["text"],
        support_claim_ids=tuple(raw["support_claim_ids"]),
        support_fact_ids=tuple(raw["support_fact_ids"]),
        support_doctrine_ids=tuple(raw["support_doctrine_ids"]),
        anti_inference_ids_applied=tuple(raw["anti_inference_ids_applied"]),
    )


def _decode_preview_payload(response: dict[str, Any]) -> tuple[dict[str, Any], list[Any]]:
    try:
        decoded = json.loads(_response_output_text(response))
    except json.JSONDecodeError as exc:
        raise ValueError("OpenAI preview output is not valid JSON") from exc
    if not isinstance(decoded, dict) or set(decoded) != {"propositions"}:
        raise ValueError("OpenAI preview JSON must contain only propositions")
    if not isinstance(decoded["propositions"], list):
        raise ValueError("OpenAI preview propositions must be a JSON array")
    return decoded, decoded["propositions"]


def _response_identity(response: dict[str, Any]) -> tuple[str, str]:
    response_id = response.get("id")
    model = response.get("model")
    if not isinstance(response_id, str) or not response_id.strip():
        raise ValueError("OpenAI preview response lacks response id")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("OpenAI preview response lacks model identifier")
    return response_id, model


def parse_openai_preview_response(
    packet: ClinicalEvidencePacket,
    response: dict[str, Any],
) -> PreviewSynthesisResult:
    """Parse provider output and fail closed through the local proposition gate."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("AI preview parsing requires a ClinicalEvidencePacket")
    if not isinstance(response, dict):
        raise TypeError("OpenAI preview response must be a dictionary")

    _, raw_propositions = _decode_preview_payload(response)
    propositions = tuple(_parse_proposition(item) for item in raw_propositions)
    validated = validate_synthesis_propositions(packet, propositions)
    response_id, model = _response_identity(response)

    return PreviewSynthesisResult(
        contract_version=PREVIEW_CONTRACT_VERSION,
        provider="OPENAI_RESPONSES_API",
        model=model,
        response_id=response_id,
        propositions=validated,
    )


def inspect_openai_preview_response(
    packet: ClinicalEvidencePacket,
    response: dict[str, Any],
) -> PreviewResponseInspection:
    """Classify one retained provider response for the controlled O4 experiment.

    This diagnostic path does not weaken the strict release gate. It validates each
    structured proposition independently so the experiment can count accepted and
    rejected items and record the exact local rejection reason. Callers retain the
    raw provider response separately; normal ``parse_openai_preview_response``
    remains all-or-nothing and fail-closed.
    """
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("AI preview inspection requires a ClinicalEvidencePacket")
    if not isinstance(response, dict):
        raise TypeError("OpenAI preview response must be a dictionary")

    _, raw_propositions = _decode_preview_payload(response)
    response_id, model = _response_identity(response)
    validation_context = build_synthesis_validation_context(packet)
    accepted: list[SynthesisProposition] = []
    rejected: list[PreviewRejectedProposition] = []
    accepted_ids: set[str] = set()

    for position, raw in enumerate(raw_propositions, start=1):
        proposition_id = raw.get("proposition_id") if isinstance(raw, dict) else None
        if not isinstance(proposition_id, str) or not proposition_id.strip():
            proposition_id = None
        try:
            proposition = _parse_proposition(raw)
            if proposition.proposition_id in accepted_ids:
                raise ValueError(
                    f"Duplicate proposition identity: {proposition.proposition_id}"
                )
            validate_synthesis_propositions(
                packet,
                (proposition,),
                context=validation_context,
            )
        except (TypeError, ValueError) as exc:
            rejected.append(
                PreviewRejectedProposition(
                    position=position,
                    proposition_id=proposition_id,
                    reason=str(exc),
                )
            )
            continue
        accepted_ids.add(proposition.proposition_id)
        accepted.append(proposition)

    return PreviewResponseInspection(
        contract_version=PREVIEW_CONTRACT_VERSION,
        provider="OPENAI_RESPONSES_API",
        model=model,
        response_id=response_id,
        raw_proposition_count=len(raw_propositions),
        accepted_propositions=tuple(accepted),
        rejected_propositions=tuple(rejected),
    )


def request_openai_preview_response(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = 90.0,
) -> dict[str, Any]:
    """Perform the one admitted provider request and return its retained raw JSON."""
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("OpenAI API key must be supplied explicitly for preview")
    if timeout_seconds <= 0:
        raise ValueError("Preview timeout must be positive")

    body = json.dumps(
        build_openai_preview_request(packet, model=model),
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
        raise RuntimeError(f"OpenAI preview request failed with HTTP {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError("OpenAI preview request failed at the network layer") from exc

    try:
        response = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenAI preview endpoint returned invalid JSON") from exc
    if not isinstance(response, dict):
        raise RuntimeError("OpenAI preview endpoint returned a non-object JSON payload")
    return response


def run_openai_preview(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = 90.0,
) -> PreviewSynthesisResult:
    """Perform one preview model call and return only locally validated output."""
    response = request_openai_preview_response(
        packet,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    return parse_openai_preview_response(packet, response)
