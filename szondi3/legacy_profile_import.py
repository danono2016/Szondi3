"""Manual import of already-scored historical Szondi profiles.

This module exists for legacy clinical records where the original card-by-card
administration is no longer available but the formal factor reactions were recorded.
It never reconstructs or invents card choices. Imported symbols are treated as
externally supplied formal profile data and then passed through the existing
profile/series -> P2B -> report/evidence/release pipeline.

Supported foreground symbols are the source-defined ordinary/quantum reactions:
0, +, +!, +!!, +!!!, -, -!, -!!, -!!!, ±, ±!.
Forced null (ø) is intentionally not accepted here because this import surface is
for foreground profiles, not experimental-complement reconstruction.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from . import clinical_release
from .clinical_case_runner import ClinicalCaseRun
from .clinical_evidence_packet import build_clinical_evidence_packet
from .clinical_protocol import ClinicalProtocolEvaluation, evaluate_clinical_protocol
from .clinical_release import build_audited_clinical_release
from .clinical_report import build_clinical_report
from .profile import DriveProfile, build_profile
from .scoring import FactorReaction
from .series import ProfileSeries
from .stimuli import FACTORS


VALID_LEGACY_SYMBOLS = frozenset(
    {"0", "+", "+!", "+!!", "+!!!", "-", "-!", "-!!", "-!!!", "±", "±!"}
)
_FACTOR_TOKEN_RE = re.compile(r"^(hy|h|s|e|k|p|d|m)\s*[:=]?\s*(0|\+!{0,3}|-!{0,3}|±!?){1}$")


@dataclass(frozen=True, slots=True)
class LegacyProfileClinicalEvaluation:
    """Compatibility wrapper expected by clinician exploration/workspace layers."""

    clinical_evaluation: ClinicalProtocolEvaluation
    complement_profiles: tuple[()] = ()
    input_mode: str = "MANUAL_LEGACY_PROFILE_SYMBOLS"


def _reaction_from_symbol(factor: str, symbol: str) -> FactorReaction:
    if factor not in FACTORS:
        raise ValueError(f"Factor necunoscut: {factor}")
    symbol = symbol.strip()
    if symbol not in VALID_LEGACY_SYMBOLS:
        raise ValueError(
            f"Reacție invalidă pentru {factor}: {symbol!r}. "
            "Permise: 0, +, +!, +!!, +!!!, -, -!, -!!, -!!!, ±, ±!."
        )

    if symbol == "0":
        kind = "null"
        quantum = 0
    elif symbol.startswith("+"):
        kind = "positive"
        quantum = symbol.count("!")
    elif symbol.startswith("-"):
        kind = "negative"
        quantum = symbol.count("!")
    else:
        kind = "ambivalent"
        quantum = symbol.count("!")

    # Historical-profile import deliberately preserves unknown card-choice counts
    # as None instead of fabricating a sympathetic/unsympathetic distribution.
    return FactorReaction(
        factor=factor,
        sympathetic=None,  # type: ignore[arg-type]
        unsympathetic=None,  # type: ignore[arg-type]
        kind=kind,  # type: ignore[arg-type]
        symbol=symbol,
        quantum_level=quantum,
        forced_null=False,
    )


def _parse_profile_line(line: str, line_number: int) -> DriveProfile:
    cleaned = line.replace("|", " ").replace(",", " ").replace(";", " ")
    tokens = tuple(token for token in cleaned.split() if token)
    if not tokens:
        raise ValueError(f"Profilul {line_number} este gol")

    if len(tokens) == len(FACTORS) and all(token in VALID_LEGACY_SYMBOLS for token in tokens):
        by_factor = dict(zip(FACTORS, tokens, strict=True))
    else:
        by_factor: dict[str, str] = {}
        for token in tokens:
            match = _FACTOR_TOKEN_RE.fullmatch(token)
            if match is None:
                raise ValueError(
                    f"Profilul {line_number}: token invalid {token!r}. "
                    "Folosește fie 8 simboluri în ordinea h s e hy k p d m, "
                    "fie tokenuri etichetate precum h- s+ e+ hy0 k+ p+ d- m-."
                )
            factor, symbol = match.groups()
            if factor in by_factor:
                raise ValueError(f"Profilul {line_number}: factor duplicat {factor}")
            by_factor[factor] = symbol
        missing = tuple(factor for factor in FACTORS if factor not in by_factor)
        extra = tuple(factor for factor in by_factor if factor not in FACTORS)
        if missing or extra or len(by_factor) != len(FACTORS):
            detail = []
            if missing:
                detail.append("lipsesc " + ", ".join(missing))
            if extra:
                detail.append("factori necunoscuți " + ", ".join(extra))
            raise ValueError(f"Profilul {line_number} nu are exact cei 8 factori: {'; '.join(detail)}")

    reactions = tuple(_reaction_from_symbol(factor, by_factor[factor]) for factor in FACTORS)
    return build_profile(reactions)


def profile_series_from_legacy_text(text: str) -> ProfileSeries:
    """Parse one to ten historical foreground profiles from compact text."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Trebuie introdus cel puțin un profil")
    lines = tuple(line.strip() for line in text.splitlines() if line.strip())
    if not 1 <= len(lines) <= 10:
        raise ValueError("Importul clinic acceptă între 1 și 10 profiluri")
    return ProfileSeries(
        tuple(_parse_profile_line(line, index) for index, line in enumerate(lines, start=1))
    )


def legacy_profile_payload(series: ProfileSeries) -> tuple[dict[str, str], ...]:
    """Return a compact non-card payload suitable for future durable import storage."""
    if not isinstance(series, ProfileSeries):
        raise TypeError("legacy_profile_payload requires a ProfileSeries")
    return tuple(
        {reaction.factor: reaction.symbol for reaction in profile.factors}
        for profile in series.profiles
    )


def run_legacy_profile_case_from_verified_checkout(
    series: ProfileSeries,
    *,
    synthesis_contract_version: str,
    synthesis_model: str,
) -> ClinicalCaseRun:
    """Run externally entered formal profiles without inventing source card choices."""
    if not isinstance(series, ProfileSeries):
        raise TypeError("Legacy profile case requires a ProfileSeries")

    evaluation = evaluate_clinical_protocol(series, production=True)
    report = build_clinical_report(evaluation)
    evidence_packet = build_clinical_evidence_packet(evaluation)
    release = build_audited_clinical_release(
        evidence_packet,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=synthesis_contract_version,
        synthesis_model=synthesis_model,
    )
    return ClinicalCaseRun(
        evaluation=LegacyProfileClinicalEvaluation(evaluation),  # type: ignore[arg-type]
        report=report,
        evidence_packet=evidence_packet,
        release=release,
    )
