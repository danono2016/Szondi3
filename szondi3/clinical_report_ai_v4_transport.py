"""Strict transport contract for the experimental V4 clinical writer.

The original V4 request reused one broad passage schema for summary, body and
closing-limit slots even though the parser accepts different ``kind`` values in
those positions.  This module makes the provider-side JSON schema mirror the
parser contract exactly and keeps that transport isolated while V4 is experimental.
"""

from __future__ import annotations

from copy import deepcopy
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .clinical_ai_preview import DEFAULT_PREVIEW_MODEL, OPENAI_RESPONSES_URL
from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_report_ai_v4 import (
    DEFAULT_V4_TIMEOUT_SECONDS,
    _ALLOWED_BODY_KINDS,
    build_openai_clinical_report_request_v4,
)


SUMMARY_KINDS = frozenset({"SYNTHESIS"})
BODY_KINDS = _ALLOWED_BODY_KINDS
LIMIT_KINDS = frozenset({"LIMIT"})


def _passage_schema(kinds: frozenset[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "item_id": {"type": "string"},
            "unit_id": {"type": "string"},
            "kind": {"type": "string", "enum": sorted(kinds)},
            "text": {"type": "string"},
        },
        "required": ["item_id", "unit_id", "kind", "text"],
        "additionalProperties": False,
    }


SUMMARY_ITEM_SCHEMA = _passage_schema(SUMMARY_KINDS)
BODY_ITEM_SCHEMA = _passage_schema(BODY_KINDS)
LIMIT_ITEM_SCHEMA = _passage_schema(LIMIT_KINDS)


STRICT_RESPONSE_SCHEMA_V4: dict[str, Any] = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "array",
            "items": SUMMARY_ITEM_SCHEMA,
            "minItems": 1,
            "maxItems": 4,
        },
        "sections": {
            "type": "array",
            "minItems": 1,
            "maxItems": 6,
            "items": {
                "type": "object",
                "properties": {
                    "section_id": {"type": "string"},
                    "title": {"type": "string"},
                    "lead_unit_id": {"type": "string"},
                    "passages": {
                        "type": "array",
                        "items": BODY_ITEM_SCHEMA,
                        "minItems": 1,
                        "maxItems": 8,
                    },
                },
                "required": ["section_id", "title", "lead_unit_id", "passages"],
                "additionalProperties": False,
            },
        },
        "global_questions": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {
                "type": "object",
                "properties": {
                    "question_id": {"type": "string"},
                    "unit_id": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["question_id", "unit_id", "text"],
                "additionalProperties": False,
            },
        },
        "closing_limits": {
            "type": "array",
            "items": LIMIT_ITEM_SCHEMA,
            "maxItems": 4,
        },
        "appendix_only_unit_ids": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "summary",
        "sections",
        "global_questions",
        "closing_limits",
        "appendix_only_unit_ids",
    ],
    "additionalProperties": False,
}


def build_openai_clinical_report_request_v4_strict(
    packet: ClinicalEvidencePacket,
    *,
    model: str = DEFAULT_PREVIEW_MODEL,
) -> dict[str, Any]:
    """Build the V4 request with a slot-specific schema accepted by the parser."""
    request = deepcopy(build_openai_clinical_report_request_v4(packet, model=model))
    request["text"]["format"]["schema"] = deepcopy(STRICT_RESPONSE_SCHEMA_V4)
    return request


def request_openai_clinical_report_response_v4_strict(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = DEFAULT_V4_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Call Responses API using only the strict V4 provider/parser contract."""
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("OpenAI API key must be supplied explicitly for clinical report AI")
    if timeout_seconds <= 0:
        raise ValueError("Clinical report AI timeout must be positive")

    body = json.dumps(
        build_openai_clinical_report_request_v4_strict(packet, model=model),
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
    except TimeoutError as exc:
        raise RuntimeError(
            "Clinical report AI request exceeded the configured response timeout"
        ) from exc

    try:
        response = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Clinical report AI endpoint returned invalid JSON") from exc
    if not isinstance(response, dict):
        raise RuntimeError("Clinical report AI endpoint returned a non-object JSON payload")
    return response


__all__ = [
    "SUMMARY_KINDS",
    "BODY_KINDS",
    "LIMIT_KINDS",
    "SUMMARY_ITEM_SCHEMA",
    "BODY_ITEM_SCHEMA",
    "LIMIT_ITEM_SCHEMA",
    "STRICT_RESPONSE_SCHEMA_V4",
    "build_openai_clinical_report_request_v4_strict",
    "request_openai_clinical_report_response_v4_strict",
]
