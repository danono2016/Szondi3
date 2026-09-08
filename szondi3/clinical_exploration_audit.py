"""Fail-closed structural audit for one clinician exploration case.

The audit adds no calculation, doctrine, executable claim, or narrative meaning. It
verifies that the already-produced evaluation, report, evidence packet, audited
release, and read-only exploration surface remain mutually traceable without
cross-scope leakage or silent repair of unresolved states.
"""

from __future__ import annotations

from dataclasses import dataclass

from .clinical_case_runner import ClinicalCaseRun
from .clinical_exploration import ClaimActivationOccurrence, explore_clinical_case
from .interpretation import ActivationStatus, InputState


_SUPPORTED_SCOPES = {"PROFILE", "SERIES", "EXPERIMENTAL_COMPLEMENT"}
_UNCERTAINTY_STATUS = {
    "UNRESOLVED_INTERPRETATION_INPUT": ActivationStatus.UNRESOLVED_INPUT,
    "BLOCKED_INTERPRETATION_CONTEXT": ActivationStatus.BLOCKED_CONTEXT,
    "BLOCKED_SOURCE_CONFLICT": ActivationStatus.BLOCKED_SOURCE_CONFLICT,
    "UNRESOLVED_COMPLEMENT_INTERPRETATION_INPUT": ActivationStatus.UNRESOLVED_INPUT,
    "BLOCKED_COMPLEMENT_INTERPRETATION_CONTEXT": ActivationStatus.BLOCKED_CONTEXT,
    "BLOCKED_COMPLEMENT_SOURCE_CONFLICT": ActivationStatus.BLOCKED_SOURCE_CONFLICT,
}


@dataclass(frozen=True, slots=True)
class ClinicalExplorationAudit:
    """Deterministic summary returned only after all structural checks pass."""

    profile_count: int
    complement_count: int
    finding_count: int
    traced_finding_count: int
    routed_claim_count: int
    nonactive_occurrence_count: int
    uncertainty_count: int


def _scope_identity(scope: str, profile_number: int | None) -> tuple[str, int | None]:
    if scope not in _SUPPORTED_SCOPES:
        raise ValueError(f"Unsupported clinical runtime scope in audit: {scope}")
    if scope == "SERIES":
        if profile_number is not None:
            raise ValueError("SERIES audit identity must not carry profile_number")
        return scope, None
    if not isinstance(profile_number, int) or isinstance(profile_number, bool):
        raise ValueError(f"{scope} audit identity requires a positive integer number")
    if profile_number < 1:
        raise ValueError(f"{scope} audit identity requires a positive integer number")
    return scope, profile_number


def _runtime_nonactive(run: ClinicalCaseRun) -> tuple[ClaimActivationOccurrence, ...]:
    evaluation = run.evaluation.clinical_evaluation
    result: list[ClaimActivationOccurrence] = []
    for profile in evaluation.profiles:
        result.extend(
            ClaimActivationOccurrence(
                scope="PROFILE",
                profile_number=profile.profile_number,
                activation=record,
            )
            for record in profile.interpretation.suppressed
        )
    result.extend(
        ClaimActivationOccurrence(
            scope="SERIES",
            profile_number=None,
            activation=record,
        )
        for record in evaluation.series_result.interpretation.suppressed
    )
    for complement in run.evaluation.complement_profiles:
        result.extend(
            ClaimActivationOccurrence(
                scope="EXPERIMENTAL_COMPLEMENT",
                profile_number=complement.test_number,
                activation=record,
            )
            for record in complement.interpretation.suppressed
        )
    return tuple(result)


def _validate_complement_packet(run: ClinicalCaseRun) -> None:
    evaluated = run.evaluation.complement_profiles
    packet = run.evidence_packet.experimental_complements
    if tuple(item.test_number for item in evaluated) != tuple(
        item.test_number for item in packet
    ):
        raise ValueError("Experimental complement ordering diverges from evidence packet")

    foreground_fact_ids = {
        fact.fact_id
        for profile in run.evaluation.clinical_evaluation.profiles
        for fact in profile.facts
        if fact.fact_id is not None
    }
    foreground_fact_ids.update(
        fact.fact_id
        for fact in run.evaluation.clinical_evaluation.series_result.facts
        if fact.fact_id is not None
    )

    seen_complement_fact_ids: set[str] = set()
    for evaluated_item, packet_item in zip(evaluated, packet):
        expected_scope = f"experimental_complement_{evaluated_item.test_number}"
        if any(fact.scope != expected_scope for fact in evaluated_item.facts):
            raise ValueError("Experimental complement fact escaped its runtime scope")
        evaluated_ids = tuple(fact.fact_id for fact in evaluated_item.facts)
        packet_ids = tuple(fact.fact_id for fact in packet_item.facts)
        if evaluated_ids != packet_ids:
            raise ValueError("Experimental complement facts diverge from evidence packet")
        for fact_id in evaluated_ids:
            if fact_id is None:
                continue
            if fact_id in foreground_fact_ids or fact_id in seen_complement_fact_ids:
                raise ValueError("Experimental complement fact identity leaks across scopes")
            seen_complement_fact_ids.add(fact_id)
        expected_symbols = tuple(
            (reaction.factor, reaction.symbol) for reaction in evaluated_item.profile.factors
        )
        if packet_item.factor_symbols != expected_symbols:
            raise ValueError("Experimental complement profile diverges from evidence packet")


def _validate_uncertainties(run: ClinicalCaseRun, nonactive) -> None:
    by_identity = {}
    for occurrence in nonactive:
        identity = (
            occurrence.scope,
            occurrence.profile_number,
            occurrence.activation.claim_id,
        )
        if identity in by_identity:
            raise ValueError("Duplicate routed non-active claim identity in runtime scope")
        by_identity[identity] = occurrence.activation

    calculation_by_name = {item.name: item for item in run.report.calculations}
    if len(calculation_by_name) != len(run.report.calculations):
        raise ValueError("Duplicate report calculation identity")

    complements = {
        item.test_number: item for item in run.evaluation.complement_profiles
    }
    if len(complements) != len(run.evaluation.complement_profiles):
        raise ValueError("Duplicate experimental complement test number")

    seen = set()
    for uncertainty in run.report.uncertainties:
        scope, number = _scope_identity(uncertainty.scope, uncertainty.profile_number)
        identity = (
            scope,
            number,
            uncertainty.kind,
            uncertainty.claim_id,
            uncertainty.calculation_name,
        )
        if identity in seen:
            raise ValueError("Duplicate report uncertainty identity")
        seen.add(identity)

        if uncertainty.claim_id is not None:
            expected_status = _UNCERTAINTY_STATUS.get(uncertainty.kind)
            if expected_status is None:
                raise ValueError(
                    f"Unknown claim uncertainty kind in audit: {uncertainty.kind}"
                )
            activation = by_identity.get((scope, number, uncertainty.claim_id))
            if activation is None:
                raise ValueError("Report claim uncertainty has no runtime activation")
            if activation.activation_status is not expected_status:
                raise ValueError("Report uncertainty status diverges from runtime activation")
            continue

        if uncertainty.kind == "UNRESOLVED_CALCULATION":
            if scope != "SERIES" or not uncertainty.calculation_name:
                raise ValueError("Unresolved calculation uncertainty has invalid scope")
            calculation = calculation_by_name.get(uncertainty.calculation_name)
            if calculation is None or calculation.state != "UNRESOLVED":
                raise ValueError("Report uncertainty has no unresolved calculation")
            continue

        if uncertainty.kind == "UNRESOLVED_COMPLEMENT_SCH_THEORETICAL_RELATION":
            if scope != "EXPERIMENTAL_COMPLEMENT" or number not in complements:
                raise ValueError("Complement Sch uncertainty has no administered complement")
            relation = tuple(
                fact
                for fact in complements[number].facts
                if fact.key
                == "protocol.experimental_complement.sch_theoretical_relation"
            )
            if len(relation) != 1 or relation[0].input_state is InputState.AVAILABLE:
                raise ValueError("Complement Sch uncertainty diverges from runtime fact state")
            continue

        raise ValueError(f"Unknown report uncertainty kind in audit: {uncertainty.kind}")


def audit_clinical_exploration(run: ClinicalCaseRun) -> ClinicalExplorationAudit:
    """Verify exact cross-layer traceability for one canonical clinical case run.

    Every active finding must resolve through the existing exploration trace to its
    same-scope runtime facts and canonical doctrine. Every routed non-active claim
    must remain discoverable with its original activation record. Report uncertainty
    states must correspond exactly to runtime activation/calculation states. E.K.P.
    evidence is additionally checked for strict scope and packet separation.
    """
    if not isinstance(run, ClinicalCaseRun):
        raise TypeError("Clinical exploration audit requires a ClinicalCaseRun")

    exploration = explore_clinical_case(run)
    evaluation = run.evaluation.clinical_evaluation
    if run.report.header.profile_count != len(evaluation.profiles):
        raise ValueError("Report profile count diverges from clinical evaluation")
    if len(run.report.observations) != len(evaluation.profiles):
        raise ValueError("Report observations diverge from clinical evaluation")

    finding_identities = []
    for finding in run.report.findings:
        scope, number = _scope_identity(finding.scope, finding.profile_number)
        identity = (finding.claim_id, scope, number)
        if identity in finding_identities:
            raise ValueError("Duplicate active finding identity in runtime scope")
        finding_identities.append(identity)
        trace = exploration.trace_finding(
            finding.claim_id,
            scope=scope,
            profile_number=number,
        )
        if trace.finding != finding:
            raise ValueError("Finding trace does not preserve the report finding")

    nonactive = _runtime_nonactive(run)
    _validate_uncertainties(run, nonactive)
    _validate_complement_packet(run)

    routed_claim_ids = tuple(
        sorted(
            {finding.claim_id for finding in run.report.findings}
            | {item.activation.claim_id for item in nonactive}
        )
    )
    for claim_id in routed_claim_ids:
        claim = exploration.claim(claim_id)
        expected_active = tuple(
            finding for finding in run.report.findings if finding.claim_id == claim_id
        )
        if tuple(trace.finding for trace in claim.active) != expected_active:
            raise ValueError("Claim exploration omits or reorders active finding occurrences")
        expected_nonactive = tuple(
            item for item in nonactive if item.activation.claim_id == claim_id
        )
        if claim.nonactive != expected_nonactive:
            raise ValueError("Claim exploration omits or rewrites non-active occurrences")

    return ClinicalExplorationAudit(
        profile_count=len(evaluation.profiles),
        complement_count=len(run.evaluation.complement_profiles),
        finding_count=len(run.report.findings),
        traced_finding_count=len(finding_identities),
        routed_claim_count=len(routed_claim_ids),
        nonactive_occurrence_count=len(nonactive),
        uncertainty_count=len(run.report.uncertainties),
    )
