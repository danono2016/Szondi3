"""Minimal deterministic gate for AI-authored clinical propositions.

A narrative model may choose wording, but every person-specific proposition must
name the executable claim(s), case fact(s), and canonical doctrine evidence that
already exist together in one ``ClinicalEvidencePacket``. This module validates
only that closed-world support envelope; it does not pretend to solve semantic
faithfulness or anti-inference checking by string heuristics.
"""

from __future__ import annotations

from dataclasses import dataclass

from .clinical_evidence_packet import ClinicalEvidencePacket


@dataclass(frozen=True, slots=True)
class SynthesisProposition:
    proposition_id: str
    scope: str
    profile_number: int | None
    text: str
    support_claim_ids: tuple[str, ...]
    support_fact_ids: tuple[str, ...]
    support_doctrine_ids: tuple[str, ...]


def _distinct_nonempty(values: tuple[str, ...], field_name: str) -> None:
    if not values:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(values)) != len(values):
        raise ValueError(f"{field_name} must not contain duplicates")
    if any(not isinstance(item, str) or not item.strip() for item in values):
        raise ValueError(f"{field_name} must contain non-empty strings")


def validate_synthesis_propositions(
    packet: ClinicalEvidencePacket,
    propositions: tuple[SynthesisProposition, ...],
) -> tuple[SynthesisProposition, ...]:
    """Fail closed unless every proposition is exactly supported by the packet.

    The validator deliberately requires the complete fact/doctrine support bundle
    of every cited finding. A model cannot cite an APPROVED claim while silently
    dropping the fact that activated it or one of the doctrine objects that bounds
    its meaning.
    """
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Synthesis validation requires a ClinicalEvidencePacket")
    if not isinstance(propositions, tuple):
        raise TypeError("Synthesis propositions must be supplied as a tuple")

    proposition_ids: set[str] = set()
    available_doctrine_ids = {item.doctrine_id for item in packet.canonical_evidence}

    for proposition in propositions:
        if not isinstance(proposition, SynthesisProposition):
            raise TypeError("Unexpected synthesis proposition type")
        if not proposition.proposition_id.strip():
            raise ValueError("proposition_id must not be empty")
        if proposition.proposition_id in proposition_ids:
            raise ValueError(f"Duplicate proposition identity: {proposition.proposition_id}")
        proposition_ids.add(proposition.proposition_id)

        if proposition.scope not in {"PROFILE", "SERIES"}:
            raise ValueError(f"Unsupported proposition scope: {proposition.scope}")
        if proposition.scope == "PROFILE":
            if not isinstance(proposition.profile_number, int) or proposition.profile_number < 1:
                raise ValueError("PROFILE proposition requires a positive profile_number")
        elif proposition.profile_number is not None:
            raise ValueError("SERIES proposition must not carry profile_number")
        if not proposition.text.strip():
            raise ValueError("Synthesis proposition text must not be empty")

        _distinct_nonempty(proposition.support_claim_ids, "support_claim_ids")
        _distinct_nonempty(proposition.support_fact_ids, "support_fact_ids")
        _distinct_nonempty(proposition.support_doctrine_ids, "support_doctrine_ids")

        matched_findings = []
        for claim_id in proposition.support_claim_ids:
            matches = tuple(
                finding
                for finding in packet.report.findings
                if finding.claim_id == claim_id
                and finding.scope == proposition.scope
                and finding.profile_number == proposition.profile_number
            )
            if not matches:
                raise ValueError(
                    "Claim is not active in the proposition scope: "
                    f"{claim_id} @ {proposition.scope}/{proposition.profile_number}"
                )
            matched_findings.extend(matches)

        required_fact_ids = {
            fact_id
            for finding in matched_findings
            for fact_id in finding.support_fact_ids
        }
        required_doctrine_ids = {
            doctrine_id
            for finding in matched_findings
            for doctrine_id in finding.doctrine_ids
        }

        if set(proposition.support_fact_ids) != required_fact_ids:
            raise ValueError(
                "Proposition fact support does not exactly match its cited claim support"
            )
        if set(proposition.support_doctrine_ids) != required_doctrine_ids:
            raise ValueError(
                "Proposition doctrine support does not exactly match its cited claim support"
            )
        missing_canonical = required_doctrine_ids - available_doctrine_ids
        if missing_canonical:
            raise ValueError(
                "Proposition references doctrine absent from canonical evidence packet: "
                + ", ".join(sorted(missing_canonical))
            )

    return propositions
