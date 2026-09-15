"""Deterministic replay seam for the experimental V4 provider pipeline.

This module performs no network call.  It reproduces the post-provider path used by
V4: extract exactly one completed Responses API output, normalize the finite known
source-language vocabulary for the Romanian clinician surface, then run the normal
V4 parser and validators.

It exists so transport/protocol and closed-world validation failures can be replayed
in CI without asking a clinician to regenerate a case or spend an API request.
"""

from __future__ import annotations

import re
from typing import Any

from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_report_ai import _response_output_text
from .clinical_report_ai_v4 import (
    ClinicalReportAIV4Result,
    parse_openai_clinical_report_response_v4,
)
from .clinician_alpha_app_v3 import _REPORT_LANGUAGE_REPLACEMENTS


def _normalize_known_source_vocabulary(text: str) -> str:
    """Apply the finite V3 vocabulary map only at complete token/phrase boundaries.

    The renderer's historical plain ``str.replace`` behavior can turn the already
    correct Romanian noun ``perversiune`` into ``perversăiune`` because the German
    adjective ``pervers`` is a prefix of that Romanian word.  Provider normalization
    must not mutate already-Romanian vocabulary, so every mapped source phrase is
    matched only when it is not embedded inside a larger word.
    """
    rendered = text
    for source, target in _REPORT_LANGUAGE_REPLACEMENTS:
        pattern = re.compile(rf"(?<!\w){re.escape(source)}(?!\w)")
        rendered = pattern.sub(lambda _match, replacement=target: replacement, rendered)
    return rendered


def normalize_v4_provider_response_language(
    response: dict[str, Any],
) -> dict[str, Any]:
    """Normalize only known source-language vocabulary, never structural metadata."""
    if not isinstance(response, dict):
        raise TypeError("Clinical report provider response must be a dictionary")

    output_text = _normalize_known_source_vocabulary(_response_output_text(response))
    normalized = dict(response)
    normalized["output_text"] = output_text
    return normalized


def replay_v4_provider_response(
    packet: ClinicalEvidencePacket,
    response: dict[str, Any],
) -> ClinicalReportAIV4Result:
    """Replay provider normalization + V4 parse/validation with no network access."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report V4 replay requires a ClinicalEvidencePacket")
    normalized = normalize_v4_provider_response_language(response)
    return parse_openai_clinical_report_response_v4(packet, normalized)


__all__ = [
    "normalize_v4_provider_response_language",
    "replay_v4_provider_response",
]
