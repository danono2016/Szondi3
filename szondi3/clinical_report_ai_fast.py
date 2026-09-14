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


_LIVE_VOICE_REFINEMENT = """

LIVE CLINICAL VOICE REFINEMENT — BINDING PRESENTATION RULES
The visible report must read as Romanian clinical prose, not as a translated German
manual and not as an audit artifact.

ROMANIAN FIRST
- Translate the source vocabulary into Romanian in the visible block. Do not repeat
  German merely to prove fidelity when an established Romanian rendering is clear.
- In particular, use Romanian for: dublare, perfecțiune, a fi totul/pretenția de
  totalitate, introiecție, încorporare, luare în posesie, introinflație,
  identificare, identitate, suprapresiune, formarea Personei, deflație/limitare,
  Eul care ia poziție, blocarea contactului, primejdie pulsională and apărare.
- Do not print the German equivalents Verdoppelung, Vollkommenheit, Allessein,
  Introjektion, Einverleibung, Inbesitznahme, Introinflation, Identifizierung,
  Identität, Überdruck, Personabildung, Deflation, stellungnehmendes Ich,
  Kontaktsperre, Triebgefahr or Abwehr in clinician-facing prose.
- Hard historical terms explicitly authorized by the plan remain direct in ROMANIAN
  (for example narcisic, sadism, perversiune, incestuos). Do not soften them.

MAKE THE MECHANISM VISIBLE
- Do not let every micro-scene happen in a lesson, project or abstract task. Across
  the report, vary ordinary contexts when the current unit permits it: learning,
  work, possession, decisions, roles, interpersonal moments or everyday choices.
- Variation is stylistic only. Never import a new psychological meaning from the
  chosen scene and never borrow semantics from a different report-plan unit.
- Prefer a small concrete action, utterance or decision over generic phrases such as
  "într-o situație ipotetică persoana..." whenever the same hypothetical status can
  remain explicit through the example marker.

CLINICAL, NOT AUDIT-LIKE
- Never use the words finding, claim, report-plan, unit_id, support_* or
  anti_inference in visible prose.
- relevant_limit is not a checklist. If needed, use one short sentence that blocks
  the single most important overreach. Do not enumerate every imaginable diagnosis,
  trait or anti-inference.
- Do not repeat the same methodological disclaimer in every field. The report shell
  already states that examples are illustrative.
"""


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
    """Apply latency + live voice controls without changing V3 semantics."""
    request = build_openai_clinical_report_request_v3(packet, model=model)
    request["reasoning"] = {"effort": "none"}
    request["max_output_tokens"] = _output_token_budget(packet)
    request["instructions"] = request.get("instructions", "") + _LIVE_VOICE_REFINEMENT
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
