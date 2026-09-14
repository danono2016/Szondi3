"""Low-latency transport profile for the plan-bound clinical report writer V3.

The semantic contract remains V3. This module tunes provider-side generation for
clinician-facing quality and latency after deterministic planning has already been
done locally: model reasoning stays disabled, output is bounded, and plan-bound
style exemplars make authorized mechanisms concrete without adding doctrine.
"""

from __future__ import annotations

import json
import re
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
from .clinical_report_voice import build_clinical_report_voice_directives


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
  (for example narcisic, sadism, perversiune, incestuos). Spell mandatory hard terms
  correctly; do not create hybrids or malformed words.

MAKE THE MECHANISM VISIBLE
- The report must not stop after naming the concept. clinical_formulation should
  normally contain two to four sentences that explain what the movement DOES.
- For a normal unit, aim for two examples when the support allows it: one concrete
  micro-scene and one contrast or bifurcation. One example remains acceptable when
  a second would add meaning not licensed by the unit.
- Do not let every micro-scene happen in a lesson, project or abstract task. Across
  the report, vary ordinary contexts when the current unit permits it: learning,
  work, possession, decisions, roles, interpersonal moments or everyday choices.
- Variation is stylistic only. Never import a new psychological meaning from the
  chosen scene and never borrow semantics from a different report-plan unit.
- Prefer a small concrete action, utterance or decision over vague nouns such as
  "o posibilitate", "ceva" or "o situație" when a more visible scene can express
  exactly the same authorized movement.
- A useful example lets a clinician imagine what to look for. A useful contrast
  separates the mechanism from something nearby that is not yet the same thing.

CLINICAL, NOT AUDIT-LIKE
- Never use the words finding, claim, report-plan, unit_id, support_* or
  anti_inference in visible prose.
- relevant_limit is not a checklist. If needed, use one short sentence that blocks
  the single most important overreach. Do not enumerate every imaginable diagnosis,
  trait or anti-inference.
- Do not repeat the same methodological disclaimer in every field. The report shell
  already states that examples are illustrative.
"""


# These are style demonstrations selected only when the current plan unit already
# authorizes the corresponding meaning. They are not evidence and must not activate
# or extend doctrine. The model receives only the exemplars matched to its own unit.
def _style_exemplar_for_unit(unit: Any) -> str | None:
    statements = tuple(getattr(unit, "authorized_statements", ()) or ())
    text = "\n".join(statements).casefold()
    unit_id = getattr(unit, "unit_id", "unit")

    if ("blocarea contactului" in text or "kontaktsperre" in text) and "narcis" in text:
        return (
            f"{unit_id}: Exemplu de formă, nu fapt despre caz. "
            "Explică mai întâi direct: «contactul se închide, iar Eul se protejează "
            "prin propria organizare». O micro-scenă suficient de concretă poate arăta "
            "o discuție care se oprește și trecerea de la schimbul cu celălalt la propria "
            "construcție; nu inventa motivul sexual al blocării. Păstrează termenii "
            "istorici autorizați separat, ca vocabular doctrinar, fără a-i atribui persoanei."
        )
    if "sch ++" in text and "introinfla" in text:
        return (
            f"{unit_id}: Exemplu de formă, nu fapt despre caz. "
            "Formula simplă poate fi: «fac ceva al meu și apoi tind să-l duc către o "
            "formă cât mai cuprinzătoare». Fă problema limitei vizibilă printr-o bifurcație: "
            "un lucru important poate fi oprit realist la «pentru acum, aici este destul» "
            "sau limita poate rămâne greu de acceptat; profilul nu alege între ramuri."
        )
    if ("−m" in text or "-m" in text) and "+k" in text and "identific" in text:
        return (
            f"{unit_id}: Exemplu de formă, nu fapt despre caz. "
            "Arată diferența dintre «admir o calitate la cineva» și «preiau acea calitate, "
            "o exersez și devine parte din propriul meu mod de a proceda». Contrastul trebuie "
            "să facă limpede că identificarea nu este identitatea globală a persoanei."
        )
    if "+p" in text and "infla" in text:
        return (
            f"{unit_id}: Exemplu de formă, nu fapt despre caz. "
            "Fă expansiunea vizibilă: o sarcină începută cu un scop precis primește încă "
            "o componentă, apoi încă una, pentru că forma parțială nu pare suficientă. "
            "Nu transforma aceasta automat în perfecționism, grandiozitate sau diagnostic."
        )
    if "+k" in text and "introiec" in text:
        return (
            f"{unit_id}: Exemplu de formă, nu fapt despre caz. "
            "Fă însușirea vizibilă: cineva întâlnește o metodă valoroasă, nu se oprește la "
            "«îmi place», ci o învață, o folosește și o integrează în propriul repertoriu. "
            "Contrastul util este interesul sau admirația fără această preluare."
        )
    return None


def _plan_bound_style_exemplars(packet: ClinicalEvidencePacket) -> str:
    plan = build_clinical_report_plan(packet)
    exemplars = tuple(
        item
        for item in (_style_exemplar_for_unit(unit) for unit in plan.units)
        if item
    )
    if not exemplars:
        return ""
    return (
        "\n\nPLAN-BOUND STYLE EXEMPLARS\n"
        "These demonstrations are attached only to units whose authorized statements already "
        "license the illustrated movement. They teach concreteness and discrimination; they are "
        "NOT additional case facts and must not be copied as biography.\n- "
        + "\n- ".join(exemplars)
        + "\n"
    )


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
    request["instructions"] = (
        request.get("instructions", "")
        + _LIVE_VOICE_REFINEMENT
        + _plan_bound_style_exemplars(packet)
    )
    text = dict(request["text"])
    # Medium restores the explanatory density required by the clinical voice spec;
    # reasoning remains disabled, so we do not pay for redundant doctrinal reasoning.
    text["verbosity"] = "medium"
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


_CANONICAL_HARD_TERM_PATTERNS: dict[str, re.Pattern[str]] = {
    "narcisic": re.compile(r"\bnarcisic(?:ă|e|i)?\b", re.IGNORECASE),
    "sadism": re.compile(r"\bsadism\b", re.IGNORECASE),
    "masochism": re.compile(r"\bmasochism\b", re.IGNORECASE),
    "homosexualitate": re.compile(r"\bhomosexualitate\b", re.IGNORECASE),
    "bisexualitate": re.compile(r"\bbisexualitate\b", re.IGNORECASE),
    "inversiune": re.compile(r"\binversiune\b", re.IGNORECASE),
    "perversiune": re.compile(r"\bperversiune\b", re.IGNORECASE),
    "incestuos": re.compile(r"\bincestuos(?:ă|e|i)?\b", re.IGNORECASE),
    "criminalitate": re.compile(r"\bcriminalitate\b", re.IGNORECASE),
    "ucigaș": re.compile(r"\bucigaș(?:ă|i)?\b", re.IGNORECASE),
    "omor": re.compile(r"\bomor\b", re.IGNORECASE),
    "sinucidere": re.compile(r"\bsinucidere\b", re.IGNORECASE),
    "autodistrugere": re.compile(r"\bautodistrugere\b", re.IGNORECASE),
    "schizofrenie": re.compile(r"\bschizofrenie\b", re.IGNORECASE),
    "paranoia": re.compile(r"\bparanoia\b", re.IGNORECASE),
    "catatonie": re.compile(r"\bcatatonie\b", re.IGNORECASE),
    "manie": re.compile(r"\bmanie\b", re.IGNORECASE),
    "delir de grandoare": re.compile(r"\bdelir de grandoare\b", re.IGNORECASE),
}


def _block_visible_text(block: Any) -> str:
    return "\n".join(
        (
            getattr(block, "title", ""),
            getattr(block, "szondi_reading", ""),
            getattr(block, "clinical_formulation", ""),
            *tuple(getattr(block, "illustrative_examples", ()) or ()),
            *tuple(getattr(block, "exploration_questions", ()) or ()),
            getattr(block, "relevant_limit", "") or "",
        )
    )


def _validate_canonical_hard_term_spellings(
    packet: ClinicalEvidencePacket,
    result: ClinicalReportAIResult,
) -> None:
    """Reject malformed look-alikes such as 'perversăiune' that root checks miss."""
    plan = build_clinical_report_plan(packet)
    directives = {
        item.unit_id: item
        for item in build_clinical_report_voice_directives(packet, plan)
    }
    for block in result.blocks:
        directive = directives.get(block.block_id)
        if directive is None:
            continue
        visible = _block_visible_text(block)
        for hard_term in directive.hard_terms:
            pattern = _CANONICAL_HARD_TERM_PATTERNS.get(hard_term.term_ro)
            if pattern is not None and not pattern.search(visible):
                raise ValueError(
                    f"Clinical report block {block.block_id} misspells or deforms mandatory hard term: {hard_term.term_ro}"
                )


def run_openai_clinical_report_fast(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = DEFAULT_FAST_TIMEOUT_SECONDS,
) -> ClinicalReportAIResult:
    """Run V3 through the latency-tuned request profile and live lexical gate."""
    response = request_openai_clinical_report_response_fast(
        packet,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    result = parse_openai_clinical_report_response_v3(packet, response)
    _validate_canonical_hard_term_spellings(packet, result)
    return result


__all__ = [
    "DEFAULT_FAST_TIMEOUT_SECONDS",
    "build_openai_clinical_report_request_fast",
    "request_openai_clinical_report_response_fast",
    "run_openai_clinical_report_fast",
]
