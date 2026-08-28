"""End-to-end bridge from recorded Szondi choices to the clinical report stack.

This module is intentionally thin: administration remains the authority for valid
card choices, scoring remains the authority for formal reactions, and P2B/report
layers remain responsible for interpretation and presentation. The bridge merely
connects those already-tested layers so a real recorded protocol can travel through
the system without hand-assembling intermediate objects.

Experimental complement profiles are calculated when supplied, but are kept
formal-only here. This module does not silently equate them with a Vorder-/Hinter-
Ich construct or route them into free-reaction series measures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .administration import ComplementProtocol, ForegroundProtocol
from .clinical_protocol import ClinicalProtocolEvaluation, evaluate_clinical_protocol
from .clinical_report import ClinicalReport, build_clinical_report
from .profile import DriveProfile, build_profile
from .scoring import complement_factor_reactions, factor_reactions
from .series import ProfileSeries


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
    interpretation_status: str = "FORMAL_ONLY_NOT_ROUTED_TO_P2B"


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
        return build_clinical_report(
            self.clinical_evaluation,
            therapist_synthesis=therapist_synthesis,
        )


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
    """Calculate the formal EKP profile without assigning clinical semantics."""
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
    Optional complement profiles are retained alongside the result as formal data
    until their clinically intended relationship is explicitly formalized.
    """
    supplied = tuple(records)
    if not 1 <= len(supplied) <= 10:
        raise ValueError("Clinical evaluation requires between one and ten administered tests")
    if any(not isinstance(record, AdministeredTestRecord) for record in supplied):
        raise TypeError("records must contain only AdministeredTestRecord objects")

    foreground_profiles = tuple(
        profile_from_foreground(record.foreground) for record in supplied
    )
    complement_profiles = tuple(
        FormalComplementProfile(
            test_number=index,
            profile=profile_from_complement(record.foreground, record.complement),
        )
        for index, record in enumerate(supplied, start=1)
        if record.complement is not None
    )
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
