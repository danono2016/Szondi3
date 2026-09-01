"""End-to-end bridge from recorded Szondi choices to the clinical report stack.

This module is intentionally thin: administration remains the authority for valid
card choices, scoring remains the authority for formal reactions, and P2B/report
layers remain responsible for interpretation and presentation. The bridge merely
connects those already-tested layers so a real recorded protocol can travel through
the system without hand-assembling intermediate objects.

Experimental complement profiles are calculated when supplied. They remain outside
the repeated free-reaction foreground series and receive only explicitly authorized
complement-specific P2B interpretation; they are never silently treated as ordinary
foreground profiles or as theoretical complement profiles.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from .administration import ComplementProtocol, ForegroundProtocol
from .clinical_interpretation import ClinicalInterpretation, interpret_facts
from .clinical_protocol import ClinicalProtocolEvaluation, evaluate_clinical_protocol
from .clinical_report import (
    ClinicalReport,
    ReportFinding,
    ReportUncertainty,
    build_clinical_report,
)
from .interpretation import ActivationStatus, Fact, InputState
from .profile import DriveProfile, build_profile
from .scoring import complement_factor_reactions, factor_reactions
from .series import ProfileSeries


EXPERIMENTAL_COMPLEMENT_CLAIM_IDS = (
    "IC_SZONDI_PRIMARY_000046",
    "IC_SZONDI_PRIMARY_000047",
    "IC_SZONDI_PRIMARY_000048",
)

_BASE_SYMBOL_BY_KIND = {
    "null": "0",
    "positive": "+",
    "negative": "-",
    "ambivalent": "±",
}

# Exact Sch pair mapping from Ich-Analyse II, Tabelle 9.
# It is intentionally represented only at the base-symbol level; quantum-overpressure
# and forced-null variants are not normalized into these pairs.
_SCH_THEORETICAL_COMPLEMENT = {
    ("0", "-"): ("±", "+"),
    ("±", "+"): ("0", "-"),
    ("0", "±"): ("±", "0"),
    ("±", "0"): ("0", "±"),
    ("+", "-"): ("-", "+"),
    ("-", "+"): ("+", "-"),
    ("±", "-"): ("0", "+"),
    ("0", "+"): ("±", "-"),
    ("-", "±"): ("+", "0"),
    ("+", "0"): ("-", "±"),
    ("+", "+"): ("-", "-"),
    ("-", "-"): ("+", "+"),
    ("+", "±"): ("-", "0"),
    ("-", "0"): ("+", "±"),
    ("±", "±"): ("0", "0"),
    ("0", "0"): ("±", "±"),
}


@dataclass(frozen=True, slots=True)
class AdministeredTestRecord:
    """One completed foreground administration and its optional complement."""

    foreground: ForegroundProtocol
    complement: ComplementProtocol | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.foreground, ForegroundProtocol):
            raise TypeError("foreground must be a ForegroundProtocol")
        if self.complement is not None and not isinstance(self.complement, ComplementProtocol):
            raise TypeError("complement must be a ComplementProtocol or None")
        if self.complement is not None:
            _validate_complement_pair(self.foreground, self.complement)


@dataclass(frozen=True, slots=True)
class FormalComplementProfile:
    test_number: int
    profile: DriveProfile
    facts: tuple[Fact, ...]
    interpretation: ClinicalInterpretation
    interpretation_status: str = "SOURCE_LINKED_COMPLEMENT_RELATION_P2B"


@dataclass(frozen=True, slots=True)
class AdministeredClinicalEvaluation:
    records: tuple[AdministeredTestRecord, ...]
    foreground_profiles: tuple[DriveProfile, ...]
    complement_profiles: tuple[FormalComplementProfile, ...]
    clinical_evaluation: ClinicalProtocolEvaluation

    @property
    def test_count(self) -> int:
        return len(self.records)

    def build_report(self, *, therapist_synthesis: str | None = None) -> ClinicalReport:
        base = build_clinical_report(
            self.clinical_evaluation,
            therapist_synthesis=therapist_synthesis,
        )
        complement_findings = tuple(
            _complement_report_finding(item.test_number, finding)
            for item in self.complement_profiles
            for finding in item.interpretation.findings
        )
        complement_uncertainties = tuple(
            _complement_report_uncertainty(item.test_number, record)
            for item in self.complement_profiles
            for record in (
                item.interpretation.unresolved + item.interpretation.blocked_context
            )
        )
        return replace(
            base,
            findings=base.findings + complement_findings,
            uncertainties=base.uncertainties + complement_uncertainties,
        )


def _complement_report_finding(test_number: int, item) -> ReportFinding:
    return ReportFinding(
        scope="EXPERIMENTAL_COMPLEMENT",
        profile_number=test_number,
        claim_id=item.claim_id,
        statement=item.statement,
        assertion_mode=item.assertion_mode.value,
        lifecycle_status=item.lifecycle_status.value,
        doctrine_ids=item.doctrine_ids,
        source_ids=item.source_ids,
        support_fact_ids=item.support_fact_ids,
        anti_inference_ids=item.anti_inference_ids,
        anti_inferences=item.anti_inferences,
        source_strength_note=item.source_strength_note,
        sensitive_domains=item.sensitive_domains,
    )


def _complement_report_uncertainty(test_number: int, record) -> ReportUncertainty:
    if record.activation_status is ActivationStatus.UNRESOLVED_INPUT:
        detail = ", ".join(record.missing_facts) or "input complement nerezolvat"
        message = f"Relația complementară nu poate fi evaluată: {detail}."
        kind = "UNRESOLVED_COMPLEMENT_INTERPRETATION_INPUT"
    elif record.activation_status is ActivationStatus.BLOCKED_CONTEXT:
        detail = ", ".join(record.missing_context) or "context complementar absent"
        message = f"Relația complementară este blocată de contextul lipsă: {detail}."
        kind = "BLOCKED_COMPLEMENT_INTERPRETATION_CONTEXT"
    else:
        message = "Relația complementară este blocată de un conflict/nivel de sursă nerezolvat."
        kind = "BLOCKED_COMPLEMENT_SOURCE_CONFLICT"
    return ReportUncertainty(
        scope="EXPERIMENTAL_COMPLEMENT",
        profile_number=test_number,
        kind=kind,
        message=message,
        claim_id=record.claim_id,
    )


def _ordinary_sch_base_symbols(profile: DriveProfile) -> tuple[str, str] | None:
    by_factor = {reaction.factor: reaction for reaction in profile.factors}
    k = by_factor["k"]
    p = by_factor["p"]
    if k.forced_null or p.forced_null:
        return None
    if k.quantum_level != 0 or p.quantum_level != 0:
        return None
    return (_BASE_SYMBOL_BY_KIND[k.kind], _BASE_SYMBOL_BY_KIND[p.kind])


def _experimental_complement_facts(
    test_number: int,
    foreground_profile: DriveProfile,
    complement_profile: DriveProfile,
) -> tuple[Fact, ...]:
    scope = f"experimental_complement_{test_number}"
    facts: list[Fact] = [
        Fact(
            key="protocol.experimental_complement.present",
            value=True,
            scope=scope,
            fact_id=f"{scope}:present",
        )
    ]

    foreground_sch = _ordinary_sch_base_symbols(foreground_profile)
    experimental_sch = _ordinary_sch_base_symbols(complement_profile)
    if foreground_sch is None or experimental_sch is None:
        facts.append(
            Fact(
                key="protocol.experimental_complement.sch_theoretical_relation",
                value=None,
                scope=scope,
                input_state=InputState.UNDEFINED,
                fact_id=f"{scope}:sch_theoretical_relation",
            )
        )
        return tuple(facts)

    expected_sch = _SCH_THEORETICAL_COMPLEMENT[foreground_sch]
    relation = "MATCH" if experimental_sch == expected_sch else "MISMATCH"
    facts.extend(
        (
            Fact(
                key="protocol.experimental_complement.foreground_sch",
                value=foreground_sch,
                scope=scope,
                fact_id=f"{scope}:foreground_sch",
            ),
            Fact(
                key="protocol.experimental_complement.theoretical_sch",
                value=expected_sch,
                scope=scope,
                fact_id=f"{scope}:theoretical_sch",
            ),
            Fact(
                key="protocol.experimental_complement.experimental_sch",
                value=experimental_sch,
                scope=scope,
                fact_id=f"{scope}:experimental_sch",
            ),
            Fact(
                key="protocol.experimental_complement.sch_theoretical_relation",
                value=relation,
                scope=scope,
                fact_id=f"{scope}:sch_theoretical_relation",
            ),
        )
    )
    return tuple(facts)


def _validate_complement_pair(
    foreground: ForegroundProtocol,
    complement: ComplementProtocol,
) -> None:
    """Prevent accidentally pairing a complement with a different foreground."""
    foreground_by_series = {
        choice.series: choice for choice in foreground.series_choices
    }
    complement_by_series = {
        choice.series: choice for choice in complement.series_choices
    }
    if set(foreground_by_series) != set(complement_by_series):
        raise ValueError("Complement and foreground must contain the same six series")

    for series, foreground_choice in foreground_by_series.items():
        complement_choice = complement_by_series[series]
        expected = set(foreground_choice.remaining)
        observed = set(
            complement_choice.relative_sympathetic
            + complement_choice.relative_unsympathetic
        )
        if observed != expected:
            raise ValueError(
                f"Complement protocol does not belong to the supplied foreground in series {series}"
            )


def profile_from_foreground(protocol: ForegroundProtocol) -> DriveProfile:
    """Score one already-validated foreground administration into a DriveProfile."""
    if not isinstance(protocol, ForegroundProtocol):
        raise TypeError("profile_from_foreground requires a ForegroundProtocol")
    return build_profile(factor_reactions(protocol))


def profile_from_complement(
    foreground: ForegroundProtocol,
    complement: ComplementProtocol,
) -> DriveProfile:
    """Calculate the formal EKP profile without assigning unsupported semantics."""
    if not isinstance(foreground, ForegroundProtocol):
        raise TypeError("profile_from_complement requires a ForegroundProtocol")
    if not isinstance(complement, ComplementProtocol):
        raise TypeError("profile_from_complement requires a ComplementProtocol")
    _validate_complement_pair(foreground, complement)
    return build_profile(complement_factor_reactions(foreground, complement))


def evaluate_administered_tests(
    records: Iterable[AdministeredTestRecord],
    *,
    production: bool = False,
) -> AdministeredClinicalEvaluation:
    """Run one to ten actual recorded administrations through P1 -> P2B -> report substrate.

    Only foreground profiles enter the repeated free-reaction ``ProfileSeries``.
    Optional experimental complement profiles remain paired with their own test and
    receive only complement-specific claims whose source-grounding has been reviewed.
    """
    supplied = tuple(records)
    if not 1 <= len(supplied) <= 10:
        raise ValueError("Clinical evaluation requires between one and ten administered tests")
    if any(not isinstance(record, AdministeredTestRecord) for record in supplied):
        raise TypeError("records must contain only AdministeredTestRecord objects")

    foreground_profiles = tuple(
        profile_from_foreground(record.foreground) for record in supplied
    )
    complement_profiles_list: list[FormalComplementProfile] = []
    for index, record in enumerate(supplied, start=1):
        if record.complement is None:
            continue
        profile = profile_from_complement(record.foreground, record.complement)
        facts = _experimental_complement_facts(
            index,
            foreground_profiles[index - 1],
            profile,
        )
        interpretation = interpret_facts(
            facts,
            production=production,
            claim_ids=EXPERIMENTAL_COMPLEMENT_CLAIM_IDS,
        )
        complement_profiles_list.append(
            FormalComplementProfile(
                test_number=index,
                profile=profile,
                facts=facts,
                interpretation=interpretation,
            )
        )
    complement_profiles = tuple(complement_profiles_list)

    clinical_evaluation = evaluate_clinical_protocol(
        ProfileSeries(foreground_profiles),
        production=production,
    )
    return AdministeredClinicalEvaluation(
        records=supplied,
        foreground_profiles=foreground_profiles,
        complement_profiles=complement_profiles,
        clinical_evaluation=clinical_evaluation,
    )
