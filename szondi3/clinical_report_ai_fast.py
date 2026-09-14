"""Low-latency transport profile for the plan-bound clinical report writer V3.

The semantic contract remains V3. This module only tunes provider-side generation
for the fact that Szondi3 has already done the hard deterministic planning locally:
no model reasoning is requested, visible verbosity is kept low, and output is
capped dynamically by the number of planned narrative units.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .clinical_ai_preview import DEFAULT_PREVIEW_MODEL, OPENAI_RESPONSES_URL
from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_report_ai import ClinicalReportAIResult
from .clinical_report_ai_v3 import (
    build_openai_clinical_report_request_v3,
    parse_openai_clinical_report_response_v3,
)
from .clinical_report_plan import build_clinical_report_plan


DEFAULT_FAST_TIMEOUT_SECONDS = 180.0
_MIN_OUTPUT_TOKENS = 3000
_MAX_OUTPUT_TOKENS = 12000
_OUTPUT_TOKENS_PER_PLAN_UNIT = 1200


def _output_token_budget(packet: ClinicalEvidencePacket) -> int:
    """Bound output without starving rich reports on multi-unit cases."""
    unit_count = max(1, len(build_clinical_report_plan(packet).units))
    return max(
        _MIN_OUTPUT_TOKENS,
        min(_MAX_OUTPUT_TOKENS, unit_count * _OUTPUT_TOKENS_PER_PLAN_UNIT),
    )


def build_openai_clinical_report_request_fast(
    packet: ClinicalEvidencePacket,
    *,
    model: str = DEFAULT_PREVIEW_MODEL,
) -> dict[str, Any]:
    """Apply latency controls without changing V3 semantics or structured output."""
    request = build_openai_clinical_report_request_v3(packet, model=model)
    request["reasoning"] = {"effort": "none"}
    request["max_output_tokens"] = _output_token_budget(packet)
    text = dict(request["text"])
    text["verbosity"] = "low"
    request["text"] = text
    return request


def request_openai_clinical_report_response_fast(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = DEFAULT_FAST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("OpenAI API key must be supplied explicitly for clinical report AI")
    if timeout_seconds <= 0:
        raise ValueError("Clinical report AI timeout must be positive")

    body = json.dumps(
        build_openai_clinical_report_request_fast(packet, model=model),
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


def run_openai_clinical_report_fast(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = DEFAULT_FAST_TIMEOUT_SECONDS,
) -> ClinicalReportAIResult:
    """Run the unchanged V3 semantic validator through the low-latency request profile."""
    response = request_openai_clinical_report_response_fast(
        packet,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    return parse_openai_clinical_report_response_v3(packet, response)


__all__ = [
    "DEFAULT_FAST_TIMEOUT_SECONDS",
    "build_openai_clinical_report_request_fast",
    "request_openai_clinical_report_response_fast",
    "run_openai_clinical_report_fast",
]
