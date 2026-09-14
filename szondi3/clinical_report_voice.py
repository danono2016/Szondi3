"""Executable clinician-facing voice directives for Szondi narrative reports.

This layer adds no doctrine and activates no interpretation. It compiles stylistic
requirements from already-authorized report-plan text: direct Romanian wording,
mandatory visibility of source-authorized hard terms, and the expected role of
clinical examples. The semantic ceiling remains the report plan / evidence packet.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable

from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_report_plan import ClinicalReportPlan, ClinicalReportPlanUnit


CLINICAL_REPORT_VOICE_SPEC_VERSION = "SZONDI_CLINICAL_VOICE_REPORT_SPEC_V1_4"


@dataclass(frozen=True, slots=True)
class HardTermDirective:
    term_ro: str
    search_root: str
    predication_scope: str
    historical_context: bool
    risk_sensitive: bool
    forbidden_attributions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "term_ro": self.term_ro,
            "mandatory_visible": True,
            "predication_scope": self.predication_scope,
            "historical_context": self.historical_context,
            "risk_sensitive": self.risk_sensitive,
            "forbidden_attributions": list(self.forbidden_attributions),
        }


@dataclass(frozen=True, slots=True)
class ClinicalReportVoiceDirective:
    unit_id: str
    example_policy: str
    hard_terms: tuple[HardTermDirective, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "example_policy": self.example_policy,
            "hard_terms": [item.to_dict() for item in self.hard_terms],
        }


@dataclass(frozen=True, slots=True)
class _HardTermRule:
    pattern: re.Pattern[str]
    term_ro: str
    search_root: str
    predication_scope: str
    historical_context: bool = False
    risk_sensitive: bool = False
    forbidden_attributions: tuple[str, ...] = ()


_HARD_TERM_RULES: tuple[_HardTermRule, ...] = (
    _HardTermRule(
        re.compile(r"narzi(?:ß|ss|s)t|narcis", re.IGNORECASE),
        "narcisic",
        "narcis",
        "MECHANISM",
        forbidden_attributions=("diagnostic de tulburare narcisică",),
    ),
    _HardTermRule(
        re.compile(r"sadism|sadismus|sadistisch", re.IGNORECASE),
        "sadism",
        "sadis",
        "MECHANISM",
        forbidden_attributions=("faptă violentă concretă",),
    ),
    _HardTermRule(
        re.compile(r"masochism|masochistisch", re.IGNORECASE),
        "masochism",
        "masochis",
        "MECHANISM",
    ),
    _HardTermRule(
        re.compile(r"homosex", re.IGNORECASE),
        "homosexualitate",
        "homosexual",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("orientarea sexuală a persoanei",),
    ),
    _HardTermRule(
        re.compile(r"bisex", re.IGNORECASE),
        "bisexualitate",
        "bisexual",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("orientarea sexuală a persoanei",),
    ),
    _HardTermRule(
        re.compile(r"invertiert|inversion|inversiune", re.IGNORECASE),
        "inversiune",
        "inversi",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("orientarea sexuală a persoanei",),
    ),
    _HardTermRule(
        re.compile(r"pervers", re.IGNORECASE),
        "perversiune",
        "pervers",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("conduită sexuală concretă", "diagnostic modern"),
    ),
    _HardTermRule(
        re.compile(r"inzestu|incestu|inzest", re.IGNORECASE),
        "incestuos",
        "incest",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("relație incestuoasă concretă",),
    ),
    _HardTermRule(
        re.compile(r"kriminalit|criminalit", re.IGNORECASE),
        "criminalitate",
        "criminal",
        "DOCTRINE_ONLY",
        forbidden_attributions=("persoana este criminală",),
    ),
    _HardTermRule(
        re.compile(r"mörder|ucigaș|ucigas", re.IGNORECASE),
        "ucigaș",
        "uciga",
        "DOCTRINE_ONLY",
        risk_sensitive=True,
        forbidden_attributions=("persoana este ucigașă",),
    ),
    _HardTermRule(
        re.compile(r"\bmord\b|omor|impuls de ucidere", re.IGNORECASE),
        "omor",
        "omor",
        "DOCTRINE_ONLY",
        risk_sensitive=True,
        forbidden_attributions=("risc actual de omor",),
    ),
    _HardTermRule(
        re.compile(r"suizid|sinucid|suicid", re.IGNORECASE),
        "sinucidere",
        "sinucid",
        "DOCTRINE_ONLY",
        risk_sensitive=True,
        forbidden_attributions=("risc suicidar actual",),
    ),
    _HardTermRule(
        re.compile(r"selbstzerstör|autodistr|autodestr", re.IGNORECASE),
        "autodistrugere",
        "autodistr",
        "MECHANISM",
        risk_sensitive=True,
        forbidden_attributions=("risc actual de autodistrugere",),
    ),
    _HardTermRule(
        re.compile(r"schizophren", re.IGNORECASE),
        "schizofrenie",
        "schizofren",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("diagnostic de schizofrenie",),
    ),
    _HardTermRule(
        re.compile(r"paranoi", re.IGNORECASE),
        "paranoia",
        "paranoi",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("diagnostic paranoid",),
    ),
    _HardTermRule(
        re.compile(r"kataton", re.IGNORECASE),
        "catatonie",
        "cataton",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("diagnostic de catatonie",),
    ),
    _HardTermRule(
        re.compile(r"\bmanie\b|manisch", re.IGNORECASE),
        "manie",
        "mani",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("episod maniacal actual",),
    ),
    _HardTermRule(
        re.compile(r"größenwahn|delir de grandoare", re.IGNORECASE),
        "delir de grandoare",
        "delir de grandoare",
        "DOCTRINE_ONLY",
        historical_context=True,
        forbidden_attributions=("delir de grandoare actual",),
    ),
)


# The clinician-facing AI layer is Romanian-first. These source-language terms all
# have clear Romanian renderings in the active product vocabulary. Their presence
# in generated prose is therefore a style failure, not a gain in doctrinal fidelity.
_UNTRANSLATED_GERMANISM = re.compile(
    r"(?:Verdoppelung|Vollkommenheit|Allessein|Introjektion|Einverleibung|"
    r"Inbesitznahme|Introinflation|Identifizierung|Identität|Überdruck|"
    r"Personabildung|Deflation|stellungnehmendes\s+Ich|Kontaktsperre|"
    r"Triebgefahr|\bAbwehr\b|narzi(?:ß|ss)tische\s+Formen\s+des\s+Ich-Schutzes)",
    re.IGNORECASE,
)

_VISIBLE_SOFTWARE_JARGON = re.compile(
    r"(?:\bfinding(?:-ul|-uri|uri|s)?\b|\bclaim(?:-ul|-uri|uri|s)?\b|"
    r"report[- ]plan|support_(?:claim|fact|doctrine)_ids?|unit_id|anti_inference)",
    re.IGNORECASE,
)


def _ordered_distinct(values: Iterable[HardTermDirective]) -> tuple[HardTermDirective, ...]:
    result: list[HardTermDirective] = []
    seen: set[str] = set()
    for item in values:
        if item.term_ro in seen:
            continue
        seen.add(item.term_ro)
        result.append(item)
    return tuple(result)


def _hard_term_source_text(unit: ClinicalReportPlanUnit) -> str:
    """Positive authorized meaning only; anti-inferences never activate vocabulary."""
    return "\n".join(unit.authorized_statements)


def hard_terms_for_unit(unit: ClinicalReportPlanUnit) -> tuple[HardTermDirective, ...]:
    if not isinstance(unit, ClinicalReportPlanUnit):
        raise TypeError("Hard-term compilation requires a ClinicalReportPlanUnit")
    text = _hard_term_source_text(unit)
    matched: list[HardTermDirective] = []
    for rule in _HARD_TERM_RULES:
        if rule.pattern.search(text):
            matched.append(
                HardTermDirective(
                    term_ro=rule.term_ro,
                    search_root=rule.search_root,
                    predication_scope=rule.predication_scope,
                    historical_context=rule.historical_context,
                    risk_sensitive=rule.risk_sensitive,
                    forbidden_attributions=rule.forbidden_attributions,
                )
            )
    return _ordered_distinct(matched)


def build_clinical_report_voice_directives(
    packet: ClinicalEvidencePacket,
    plan: ClinicalReportPlan,
) -> tuple[ClinicalReportVoiceDirective, ...]:
    """Compile style-only directives from the deterministic plan.

    The packet argument keeps this boundary explicit and future-proofs provenance
    checks; v1.4 derives no additional meaning from canonical evidence.
    """
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report voice compilation requires a ClinicalEvidencePacket")
    if not isinstance(plan, ClinicalReportPlan):
        raise TypeError("Clinical report voice compilation requires a ClinicalReportPlan")

    directives: list[ClinicalReportVoiceDirective] = []
    for unit in plan.units:
        hard_terms = hard_terms_for_unit(unit)
        risk_sensitive = any(item.risk_sensitive for item in hard_terms)
        directives.append(
            ClinicalReportVoiceDirective(
                unit_id=unit.unit_id,
                example_policy=(
                    "OPTIONAL_CANONICAL_PREFERRED"
                    if risk_sensitive
                    else "AT_LEAST_ONE_HYPOTHETICAL"
                ),
                hard_terms=hard_terms,
            )
        )
    return tuple(directives)


def voice_directives_payload(
    packet: ClinicalEvidencePacket,
    plan: ClinicalReportPlan,
) -> dict[str, Any]:
    directives = build_clinical_report_voice_directives(packet, plan)
    return {
        "version": CLINICAL_REPORT_VOICE_SPEC_VERSION,
        "units": [item.to_dict() for item in directives],
    }


def _visible_block_text(block: Any) -> str:
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


def validate_clinical_report_voice(
    packet: ClinicalEvidencePacket,
    plan: ClinicalReportPlan,
    blocks: tuple[Any, ...],
) -> None:
    """Fail closed on executable v1.4 style requirements that are machine-checkable."""
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Clinical report voice validation requires a ClinicalEvidencePacket")
    if not isinstance(plan, ClinicalReportPlan):
        raise TypeError("Clinical report voice validation requires a ClinicalReportPlan")
    if not isinstance(blocks, tuple):
        raise TypeError("Clinical report voice validation requires a tuple of blocks")

    directives = {
        item.unit_id: item
        for item in build_clinical_report_voice_directives(packet, plan)
    }
    for block in blocks:
        block_id = getattr(block, "block_id", None)
        try:
            directive = directives[block_id]
        except KeyError as exc:
            raise ValueError(f"Clinical report block is outside voice plan: {block_id}") from exc
        examples = tuple(getattr(block, "illustrative_examples", ()) or ())
        if (
            directive.example_policy == "AT_LEAST_ONE_HYPOTHETICAL"
            and not examples
        ):
            raise ValueError(
                f"Clinical report plan unit {block_id} requires at least one concrete hypothetical example"
            )

        visible_raw = _visible_block_text(block)
        visible = visible_raw.casefold()
        if _VISIBLE_SOFTWARE_JARGON.search(visible_raw):
            raise ValueError(
                f"Clinical report plan unit {block_id} leaks software/audit vocabulary"
            )
        germanism = _UNTRANSLATED_GERMANISM.search(visible_raw)
        if germanism:
            raise ValueError(
                f"Clinical report plan unit {block_id} contains untranslated Germanism: {germanism.group(0)}"
            )
        for hard_term in directive.hard_terms:
            if hard_term.search_root.casefold() not in visible:
                raise ValueError(
                    f"Clinical report plan unit {block_id} euphemizes or omits mandatory hard term: {hard_term.term_ro}"
                )
