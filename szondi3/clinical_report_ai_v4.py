"""Global closed-world narrative writer for the clinician-facing Szondi report.

V4 keeps the deterministic report plan as the semantic ceiling but stops treating
plan units as visible report blocks. The model may order the case globally and place
several independently-supported passages under one clinical section. Every visible
text atom is still bound to exactly one deterministic plan unit, so narrative flow
does not become permission for Mosaikspiel.
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
from .clinical_report_ai import (
    ClinicalNarrativeBlock,
    ClinicalReportAIResult,
    _require_visible_text,
    _response_output_text,
    build_clinical_report_ai_payload,
    validate_clinical_report_blocks,
)
from .clinical_report_plan import ClinicalReportPlan, ClinicalReportPlanUnit, build_clinical_report_plan
from .clinical_report_voice import (
    _UNTRANSLATED_GERMANISM,
    _VISIBLE_SOFTWARE_JARGON,
    build_clinical_report_voice_directives,
)


CLINICAL_REPORT_AI_V4_CONTRACT_VERSION = "SZONDI3_CLINICAL_REPORT_GLOBAL_V4"
DEFAULT_V4_TIMEOUT_SECONDS = 180.0
_ALLOWED_BODY_KINDS = frozenset({"EXPLANATION", "EXAMPLE", "CONTRAST", "BIFURCATION"})
_HYPOTHETICAL_CUE = re.compile(
    r"(?:\bde pildă\b|\bde exemplu\b|\bar putea\b|\bs-ar putea\b|\bo manifestare posibilă\b|\bputem imagina\b)",
    re.IGNORECASE,
)

_CANONICAL_HARD_TERM_PATTERNS: dict[str, re.Pattern[str]] = {
    "narcisic": re.compile(r"\bnarcisic(?:ă|e|i)?\b", re.IGNORECASE),
    "sadism": re.compile(r"\bsadism\b", re.IGNORECASE),
    "masochism": re.compile(r"\bmasochism\b", re.IGNORECASE),
    "homosexualitate": re.compile(r"\bhomosexualitate\b", re.IGNORECASE),
    "bisexualitate": re.compile(r"\bbisexualitate\b", re.IGNORECASE),
    "inversiune": re.compile(r"\binversiune\b", re.IGNORECASE),
    "perversiune": re.compile(r"\bperversiune\b", re.IGNORECASE),
    "incestuos": re.compile(r"\b(?:incestuos|incestuoasă|incestuoase|incestuoși)\b", re.IGNORECASE),
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


@dataclass(frozen=True, slots=True)
class ClinicalNarrativePassageV4:
    item_id: str
    unit_id: str
    kind: str
    text: str


@dataclass(frozen=True, slots=True)
class ClinicalGlobalSectionV4:
    section_id: str
    title: str
    lead_unit_id: str
    passages: tuple[ClinicalNarrativePassageV4, ...]


@dataclass(frozen=True, slots=True)
class ClinicalExplorationQuestionV4:
    question_id: str
    unit_id: str
    text: str


@dataclass(frozen=True, slots=True)
class ClinicalReportAIV4Result(ClinicalReportAIResult):
    summary: tuple[ClinicalNarrativePassageV4, ...]
    sections: tuple[ClinicalGlobalSectionV4, ...]
    global_questions: tuple[ClinicalExplorationQuestionV4, ...]
    closing_limits: tuple[ClinicalNarrativePassageV4, ...]
    appendix_only_unit_ids: tuple[str, ...]


_AI_INSTRUCTIONS_V4 = """You are the clinician-facing WRITER of Szondi3.

The supplied JSON is your COMPLETE universe. Do not add remembered Szondi theory,
web knowledge, contemporary diagnosis, psychodynamic plausibility or biography.
The deterministic engine has already decided what meanings are active. The report
plan is a semantic map, NOT a visible report outline.

GLOBAL-WRITER PRINCIPLE
Write the case as a coherent Romanian clinical report. Do NOT produce one visible
mini-report per plan unit. Do NOT repeat a fixed template such as "Sensul szondian / Explicație / Exemplu / Limită" for every meaning. Decide the clinical order of the material, identify what deserves emphasis, and build a readable whole.

PROVENANCE ATOM RULE — BINDING
Every visible text atom in the JSON is bound to exactly ONE report-plan unit_id.
That text may use ONLY the meaning authorized by that unit. If the unit itself is an
authorized bridge, the text may express that bridge. A text atom bound to an atomic
unit may not borrow another unit merely because both coexist in the profile.

A section may contain successive passages bound to different units. This is layout,
not permission to invent a relation between them. The section title is supported
ONLY by lead_unit_id, so choose a lead whose authorized meaning genuinely supports
the title. This is how you may create a global report while preserving anti-Mosaikspiel.

REPORT SHAPE
- summary: 1-4 compact paragraphs. Each paragraph is bound to one unit. Use the most
  clinically informative authorized units; do not manufacture a whole-person verdict.
- sections: 1-6 clinically meaningful sections. A section may weave several passages
  in a useful order, but each passage keeps its own unit_id.
- global_questions: gather the best interview questions at the end instead of asking
  nearly identical questions after every paragraph.
- closing_limits: only the few boundaries that materially protect against overreach.
- appendix_only_unit_ids: plan units deliberately left to the deterministic appendix
  because they would be redundant or peripheral in the narrative. Every plan unit
  must either appear in summary/sections or be listed here. Do not omit a unit merely
  because it is difficult or historically uncomfortable. A unit carrying mandatory
  hard vocabulary must be narrated and may not be hidden in the appendix.

NATURAL CLINICAL PROSE
Write Romanian first. Translate ordinary German terminology. Preserve hard Romanian
historical terms when authorized: narcisic, sadism, homosexualitate, bisexualitate,
inversiune, perversiune, incestuos, criminalitate, ucigaș, sinucidere etc. Do not
soften the term; control the predication. A doctrinal term is not automatically a
fact, identity, diagnosis, act or current risk of the person.

Examples are part of the prose, not a rubric. Use kind=EXAMPLE, CONTRAST or
BIFURCATION as invisible metadata. The visible text should read naturally, e.g.
"De pildă...", "Un contrast util este...", "Două evoluții rămân posibile...".
EXAMPLE passages must explicitly signal hypothetical status through Romanian
conditional/example wording. Prefer concrete actions, decisions, utterances and
ordinary situations. Never invent trauma, family history, relationship facts,
sexual conduct, violence, diagnosis or motives.

The report should explain mechanisms, not translate labels. When a concept is
abstract, show what it does. A useful contrast separates the mechanism from a nearby
phenomenon. A useful bifurcation shows two possible outcomes when the doctrine leaves
the outcome open, without choosing one for the person.

Do not use visible software/audit words such as finding, claim, report-plan, unit_id,
support_* or anti_inference. Do not print German merely to demonstrate fidelity.
Do not produce a glossary or a software summary.

SUMMARY DISCIPLINE
A summary paragraph may be strong and clinically useful, but it still has one unit_id.
If you need a second independent meaning, use a second paragraph. Do not hide an
unauthorized synthesis inside a long sentence.

INTERVIEW QUESTIONS
Ask for concrete episodes: what happened, what the person did, how a limit was
handled, what changed. Do not ask the person to confirm Szondi terminology.

Return only JSON matching the schema.
"""

_ITEM_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "item_id": {"type": "string"},
        "unit_id": {"type": "string"},
        "kind": {
            "type": "string",
            "enum": ["SYNTHESIS", "EXPLANATION", "EXAMPLE", "CONTRAST", "BIFURCATION", "LIMIT"],
        },
        "text": {"type": "string"},
    },
    "required": ["item_id", "unit_id", "kind", "text"],
    "additionalProperties": False,
}

_RESPONSE_SCHEMA_V4: dict[str, Any] = {
    "type": "object",
    "properties": {
        "summary": {"type": "array", "items": _ITEM_SCHEMA, "minItems": 1, "maxItems": 4},
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
                    "passages": {"type": "array", "items": _ITEM_SCHEMA, "minItems": 1, "maxItems": 8},
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
        "closing_limits": {"type": "array", "items": _ITEM_SCHEMA, "maxItems": 4},
        "appendix_only_unit_ids": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "sections", "global_questions", "closing_limits", "appendix_only_unit_ids"],
    "additionalProperties": False,
}


def _output_token_budget(packet: ClinicalEvidencePacket) -> int:
    count = max(1, len(build_clinical_report_plan(packet).units))
    return max(3500, min(10000, 1800 + count * 700))


def build_clinical_report_ai_payload_v4(packet: ClinicalEvidencePacket) -> dict[str, Any]:
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report AI V4 requires a ClinicalEvidencePacket")
    plan = build_clinical_report_plan(packet)
    payload = build_clinical_report_ai_payload(packet)
    payload["ai_contract_version"] = CLINICAL_REPORT_AI_V4_CONTRACT_VERSION
    payload["report_plan"] = plan.to_dict()
    payload["voice_directives"] = {
        "units": [item.to_dict() for item in build_clinical_report_voice_directives(packet, plan)]
    }
    return payload


def build_openai_clinical_report_request_v4(
    packet: ClinicalEvidencePacket,
    *,
    model: str = DEFAULT_PREVIEW_MODEL,
) -> dict[str, Any]:
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical report AI model identifier must not be empty")
    payload = json.dumps(
        build_clinical_report_ai_payload_v4(packet),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "model": model,
        "store": False,
        "tools": [],
        "reasoning": {"effort": "none"},
        "max_output_tokens": _output_token_budget(packet),
        "instructions": _AI_INSTRUCTIONS_V4,
        "input": [{
            "role": "user",
            "content": [{
                "type": "input_text",
                "text": "Write one global clinician report using only this closed-world semantic map:\n" + payload,
            }],
        }],
        "text": {
            "verbosity": "medium",
            "format": {
                "type": "json_schema",
                "name": "szondi3_clinical_report_global_v4",
                "strict": True,
                "schema": _RESPONSE_SCHEMA_V4,
            },
        },
    }


def _plan_index(plan: ClinicalReportPlan) -> dict[str, ClinicalReportPlanUnit]:
    return {unit.unit_id: unit for unit in plan.units}


def _parse_passage(raw: Any, *, expected_kinds: frozenset[str]) -> ClinicalNarrativePassageV4:
    if not isinstance(raw, dict) or set(raw) != {"item_id", "unit_id", "kind", "text"}:
        raise ValueError("Clinical report V4 passage has missing or unexpected fields")
    kind = raw["kind"]
    if kind not in expected_kinds:
        raise ValueError(f"Clinical report V4 passage kind is not allowed here: {kind}")
    text = _require_visible_text(raw["text"], "narrative_text")
    if _VISIBLE_SOFTWARE_JARGON.search(text):
        raise ValueError("Clinical report V4 leaks software/audit vocabulary")
    germanism = _UNTRANSLATED_GERMANISM.search(text)
    if germanism:
        raise ValueError(f"Clinical report V4 contains untranslated Germanism: {germanism.group(0)}")
    if kind == "EXAMPLE" and not _HYPOTHETICAL_CUE.search(text):
        raise ValueError("Clinical report V4 example must visibly remain hypothetical")
    return ClinicalNarrativePassageV4(
        item_id=_require_visible_text(raw["item_id"], "item_id"),
        unit_id=_require_visible_text(raw["unit_id"], "unit_id"),
        kind=kind,
        text=text,
    )


def _parse_question(raw: Any) -> ClinicalExplorationQuestionV4:
    if not isinstance(raw, dict) or set(raw) != {"question_id", "unit_id", "text"}:
        raise ValueError("Clinical report V4 question has missing or unexpected fields")
    text = _require_visible_text(raw["text"], "exploration_question")
    if _VISIBLE_SOFTWARE_JARGON.search(text) or _UNTRANSLATED_GERMANISM.search(text):
        raise ValueError("Clinical report V4 question leaks non-clinical vocabulary")
    return ClinicalExplorationQuestionV4(
        question_id=_require_visible_text(raw["question_id"], "question_id"),
        unit_id=_require_visible_text(raw["unit_id"], "unit_id"),
        text=text,
    )


def _validate_identifiers_and_coverage(
    packet: ClinicalEvidencePacket,
    plan: ClinicalReportPlan,
    summary: tuple[ClinicalNarrativePassageV4, ...],
    sections: tuple[ClinicalGlobalSectionV4, ...],
    questions: tuple[ClinicalExplorationQuestionV4, ...],
    limits: tuple[ClinicalNarrativePassageV4, ...],
    appendix_only: tuple[str, ...],
) -> None:
    known = _plan_index(plan)
    item_ids: set[str] = set()
    section_ids: set[str] = set()
    question_ids: set[str] = set()

    def require_unit(unit_id: str) -> None:
        if unit_id not in known:
            raise ValueError(f"Clinical report V4 cites unknown report-plan unit: {unit_id}")

    for item in summary + tuple(p for s in sections for p in s.passages) + limits:
        require_unit(item.unit_id)
        if item.item_id in item_ids:
            raise ValueError(f"Duplicate clinical report V4 item id: {item.item_id}")
        item_ids.add(item.item_id)

    for section in sections:
        require_unit(section.lead_unit_id)
        if section.section_id in section_ids:
            raise ValueError(f"Duplicate clinical report V4 section id: {section.section_id}")
        section_ids.add(section.section_id)

    for question in questions:
        require_unit(question.unit_id)
        if question.question_id in question_ids:
            raise ValueError(f"Duplicate clinical report V4 question id: {question.question_id}")
        question_ids.add(question.question_id)

    if len(set(appendix_only)) != len(appendix_only):
        raise ValueError("Clinical report V4 appendix_only_unit_ids contains duplicates")
    for unit_id in appendix_only:
        require_unit(unit_id)

    narrative_units = (
        {item.unit_id for item in summary}
        | {section.lead_unit_id for section in sections}
        | {passage.unit_id for section in sections for passage in section.passages}
    )
    visible_units = (
        narrative_units
        | {question.unit_id for question in questions}
        | {item.unit_id for item in limits}
    )
    if visible_units & set(appendix_only):
        raise ValueError("Clinical report V4 unit cannot be both visible and appendix-only")
    if narrative_units | set(appendix_only) != set(known):
        raise ValueError("Clinical report V4 must account for every report-plan unit")

    directives = build_clinical_report_voice_directives(packet, plan)
    hard_term_unit_ids = {
        directive.unit_id for directive in directives if directive.hard_terms
    }
    hidden_hard_terms = hard_term_unit_ids & set(appendix_only)
    if hidden_hard_terms:
        raise ValueError(
            "Clinical report V4 cannot hide mandatory hard vocabulary in the appendix: "
            + ", ".join(sorted(hidden_hard_terms))
        )

    normal_unit_ids = {
        directive.unit_id
        for directive in directives
        if directive.example_policy == "AT_LEAST_ONE_HYPOTHETICAL"
    }
    illustrative_count = sum(
        item.kind in {"EXAMPLE", "CONTRAST", "BIFURCATION"}
        for section in sections for item in section.passages
    )
    narrative_normal = len(narrative_units & normal_unit_ids)
    required_examples = 0 if narrative_normal == 0 else (1 if narrative_normal == 1 else 2)
    if illustrative_count < required_examples:
        raise ValueError("Clinical report V4 is too abstract: insufficient report-level illustration")


def _collect_unit_texts(
    plan: ClinicalReportPlan,
    summary: tuple[ClinicalNarrativePassageV4, ...],
    sections: tuple[ClinicalGlobalSectionV4, ...],
    questions: tuple[ClinicalExplorationQuestionV4, ...],
    limits: tuple[ClinicalNarrativePassageV4, ...],
) -> dict[str, list[str]]:
    texts = {unit.unit_id: [] for unit in plan.units}
    for item in summary:
        texts[item.unit_id].append(item.text)
    for section in sections:
        texts[section.lead_unit_id].append(section.title)
        for passage in section.passages:
            texts[passage.unit_id].append(passage.text)
    for question in questions:
        texts[question.unit_id].append(question.text)
    for item in limits:
        texts[item.unit_id].append(item.text)
    return texts


def _validation_blocks(
    plan: ClinicalReportPlan,
    summary: tuple[ClinicalNarrativePassageV4, ...],
    sections: tuple[ClinicalGlobalSectionV4, ...],
    questions: tuple[ClinicalExplorationQuestionV4, ...],
    limits: tuple[ClinicalNarrativePassageV4, ...],
    appendix_only: tuple[str, ...],
) -> tuple[ClinicalNarrativeBlock, ...]:
    text_map = _collect_unit_texts(plan, summary, sections, questions, limits)
    appendix = set(appendix_only)
    question_map: dict[str, list[str]] = {unit.unit_id: [] for unit in plan.units}
    for question in questions:
        question_map[question.unit_id].append(question.text)
    example_map: dict[str, list[str]] = {unit.unit_id: [] for unit in plan.units}
    for section in sections:
        for passage in section.passages:
            if passage.kind in {"EXAMPLE", "CONTRAST", "BIFURCATION"}:
                example_map[passage.unit_id].append(passage.text)
    limit_map: dict[str, list[str]] = {unit.unit_id: [] for unit in plan.units}
    for item in limits:
        limit_map[item.unit_id].append(item.text)

    blocks: list[ClinicalNarrativeBlock] = []
    for unit in plan.units:
        if unit.unit_id in appendix:
            continue
        texts = text_map[unit.unit_id]
        if not texts:
            raise ValueError(f"Clinical report V4 narrative unit lacks visible text: {unit.unit_id}")
        combined = "\n\n".join(texts)
        blocks.append(
            ClinicalNarrativeBlock(
                block_id=f"V4-{unit.unit_id}",
                scope=unit.scope,
                profile_number=unit.profile_number,
                title=texts[0][:180],
                szondi_reading=combined,
                clinical_formulation=combined,
                exploration_questions=tuple(question_map[unit.unit_id]),
                relevant_limit=(" ".join(limit_map[unit.unit_id]) or None),
                support_claim_ids=unit.support_claim_ids,
                support_fact_ids=unit.support_fact_ids,
                support_doctrine_ids=unit.support_doctrine_ids,
                anti_inference_ids_applied=unit.anti_inference_ids,
                illustrative_examples=tuple(example_map[unit.unit_id]),
            )
        )
    return tuple(blocks)


def _validate_hard_terms(
    packet: ClinicalEvidencePacket,
    plan: ClinicalReportPlan,
    text_map: dict[str, list[str]],
    appendix_only: tuple[str, ...],
) -> None:
    appendix = set(appendix_only)
    directives = {
        item.unit_id: item
        for item in build_clinical_report_voice_directives(packet, plan)
    }
    for unit_id, directive in directives.items():
        if unit_id in appendix:
            continue
        visible = "\n".join(text_map[unit_id])
        for hard_term in directive.hard_terms:
            pattern = _CANONICAL_HARD_TERM_PATTERNS.get(hard_term.term_ro)
            if pattern is not None and not pattern.search(visible):
                raise ValueError(
                    f"Clinical report V4 omits or deforms mandatory hard term: {hard_term.term_ro}"
                )


def validate_clinical_report_v4_result(
    packet: ClinicalEvidencePacket,
    result: ClinicalReportAIV4Result,
) -> ClinicalReportAIV4Result:
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report V4 validation requires a ClinicalEvidencePacket")
    if not isinstance(result, ClinicalReportAIV4Result):
        raise TypeError("Clinical report V4 validation requires a ClinicalReportAIV4Result")
    plan = build_clinical_report_plan(packet)
    _validate_identifiers_and_coverage(
        packet,
        plan,
        result.summary,
        result.sections,
        result.global_questions,
        result.closing_limits,
        result.appendix_only_unit_ids,
    )
    text_map = _collect_unit_texts(
        plan,
        result.summary,
        result.sections,
        result.global_questions,
        result.closing_limits,
    )
    _validate_hard_terms(packet, plan, text_map, result.appendix_only_unit_ids)
    validated_blocks = validate_clinical_report_blocks(
        packet,
        _validation_blocks(
            plan,
            result.summary,
            result.sections,
            result.global_questions,
            result.closing_limits,
            result.appendix_only_unit_ids,
        ),
    )
    object.__setattr__(result, "blocks", validated_blocks)
    return result


def parse_openai_clinical_report_response_v4(
    packet: ClinicalEvidencePacket,
    response: dict[str, Any],
) -> ClinicalReportAIV4Result:
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report V4 parsing requires a ClinicalEvidencePacket")
    if not isinstance(response, dict):
        raise TypeError("Clinical report V4 response must be a dictionary")
    try:
        decoded = json.loads(_response_output_text(response))
    except json.JSONDecodeError as exc:
        raise ValueError("Clinical report V4 output is not valid JSON") from exc
    required = {"summary", "sections", "global_questions", "closing_limits", "appendix_only_unit_ids"}
    if not isinstance(decoded, dict) or set(decoded) != required:
        raise ValueError("Clinical report V4 JSON has missing or unexpected top-level fields")

    summary = tuple(
        _parse_passage(item, expected_kinds=frozenset({"SYNTHESIS"}))
        for item in decoded["summary"]
    )
    sections: list[ClinicalGlobalSectionV4] = []
    for raw in decoded["sections"]:
        if not isinstance(raw, dict) or set(raw) != {"section_id", "title", "lead_unit_id", "passages"}:
            raise ValueError("Clinical report V4 section has missing or unexpected fields")
        title = _require_visible_text(raw["title"], "section_title")
        if _VISIBLE_SOFTWARE_JARGON.search(title) or _UNTRANSLATED_GERMANISM.search(title):
            raise ValueError("Clinical report V4 section title leaks non-clinical vocabulary")
        passages = tuple(
            _parse_passage(item, expected_kinds=_ALLOWED_BODY_KINDS)
            for item in raw["passages"]
        )
        sections.append(
            ClinicalGlobalSectionV4(
                section_id=_require_visible_text(raw["section_id"], "section_id"),
                title=title,
                lead_unit_id=_require_visible_text(raw["lead_unit_id"], "lead_unit_id"),
                passages=passages,
            )
        )

    questions = tuple(_parse_question(item) for item in decoded["global_questions"])
    limits = tuple(
        _parse_passage(item, expected_kinds=frozenset({"LIMIT"}))
        for item in decoded["closing_limits"]
    )
    appendix_only_raw = decoded["appendix_only_unit_ids"]
    if not isinstance(appendix_only_raw, list) or not all(isinstance(item, str) for item in appendix_only_raw):
        raise ValueError("appendix_only_unit_ids must be an array of strings")
    appendix_only = tuple(appendix_only_raw)

    response_id = response.get("id")
    model = response.get("model")
    if not isinstance(response_id, str) or not response_id.strip():
        raise ValueError("Clinical report V4 response lacks response id")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Clinical report V4 response lacks model identifier")

    result = ClinicalReportAIV4Result(
        contract_version=CLINICAL_REPORT_AI_V4_CONTRACT_VERSION,
        provider="OPENAI_RESPONSES_API",
        model=model.strip(),
        response_id=response_id.strip(),
        blocks=(),
        summary=summary,
        sections=tuple(sections),
        global_questions=questions,
        closing_limits=limits,
        appendix_only_unit_ids=appendix_only,
    )
    return validate_clinical_report_v4_result(packet, result)


def request_openai_clinical_report_response_v4(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = DEFAULT_V4_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("OpenAI API key must be supplied explicitly for clinical report AI")
    if timeout_seconds <= 0:
        raise ValueError("Clinical report AI timeout must be positive")
    body = json.dumps(
        build_openai_clinical_report_request_v4(packet, model=model),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    request = Request(
        OPENAI_RESPONSES_URL,
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
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
        raise RuntimeError(f"Clinical report AI request failed with HTTP {exc.code}{suffix}") from exc
    except URLError as exc:
        raise RuntimeError("Clinical report AI request failed at the network layer") from exc
    except TimeoutError as exc:
        raise RuntimeError("Clinical report AI request exceeded the configured response timeout") from exc
    try:
        response = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Clinical report AI endpoint returned invalid JSON") from exc
    if not isinstance(response, dict):
        raise RuntimeError("Clinical report AI endpoint returned a non-object JSON payload")
    return response


def run_openai_clinical_report_v4(
    packet: ClinicalEvidencePacket,
    *,
    api_key: str,
    model: str = DEFAULT_PREVIEW_MODEL,
    timeout_seconds: float = DEFAULT_V4_TIMEOUT_SECONDS,
) -> ClinicalReportAIV4Result:
    response = request_openai_clinical_report_response_v4(
        packet,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    return parse_openai_clinical_report_response_v4(packet, response)


__all__ = [
    "CLINICAL_REPORT_AI_V4_CONTRACT_VERSION",
    "DEFAULT_V4_TIMEOUT_SECONDS",
    "ClinicalNarrativePassageV4",
    "ClinicalGlobalSectionV4",
    "ClinicalExplorationQuestionV4",
    "ClinicalReportAIV4Result",
    "build_clinical_report_ai_payload_v4",
    "build_openai_clinical_report_request_v4",
    "parse_openai_clinical_report_response_v4",
    "request_openai_clinical_report_response_v4",
    "run_openai_clinical_report_v4",
    "validate_clinical_report_v4_result",
]
