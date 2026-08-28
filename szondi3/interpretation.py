"""Fail-closed P2B executable interpretation primitives.

This module deliberately does not recalculate P1 facts.  It evaluates explicit,
typed fact states against reviewed claim definitions and preserves provenance,
ambiguity, context requirements, alternatives, and anti-inferences.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class ActivationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNRESOLVED_INPUT = "UNRESOLVED_INPUT"
    BLOCKED_CONTEXT = "BLOCKED_CONTEXT"
    BLOCKED_SOURCE_CONFLICT = "BLOCKED_SOURCE_CONFLICT"


class InputState(str, Enum):
    AVAILABLE = "AVAILABLE"
    AMBIGUOUS = "AMBIGUOUS"
    UNDEFINED = "UNDEFINED"
    MISSING = "MISSING"


@dataclass(frozen=True)
class FactRef:
    fact_type: str
    fact_id: str
    value: Any = None
    scope: str = ""
    input_state: InputState = InputState.AVAILABLE
    calculation_version: str = ""


@dataclass(frozen=True)
class Predicate:
    fact_type: str
    equals: Any = None

    def matches(self, fact: FactRef) -> bool:
        return fact.fact_type == self.fact_type and (
            self.equals is None or fact.value == self.equals
        )


@dataclass(frozen=True)
class ExecutableClaim:
    claim_id: str
    rule_version: str
    source_layer: str
    doctrine_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    canonical_anchors: tuple[str, ...]
    epistemic_class: str
    assertion_mode: str
    source_strength_note: str
    claim: str
    trigger_kind: str
    required_facts: tuple[Predicate, ...] = ()
    context_requirements: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    anti_inferences: tuple[str, ...] = ()
    status: str = "SOURCE_LINKED"

    def __post_init__(self) -> None:
        if not self.doctrine_ids:
            raise ValueError("P2B claim requires doctrine provenance")
        if not self.source_ids or not self.canonical_anchors:
            raise ValueError("P2B claim requires recoverable source provenance")


@dataclass(frozen=True)
class ActivationRecord:
    claim_id: str
    rule_version: str
    activation_status: ActivationStatus
    matched_facts: tuple[str, ...] = ()
    missing_facts: tuple[str, ...] = ()
    missing_context: tuple[str, ...] = ()
    active_alternatives: tuple[str, ...] = ()
    anti_inferences: tuple[str, ...] = ()
    provenance_trace: tuple[str, ...] = ()


def evaluate_claim(
    claim: ExecutableClaim,
    facts: Sequence[FactRef],
    context: Mapping[str, Any] | None = None,
) -> ActivationRecord:
    """Evaluate one P2B claim without inventing or repairing prerequisite facts."""
    context = context or {}
    missing_context = tuple(k for k in claim.context_requirements if k not in context)
    if missing_context:
        return _record(claim, ActivationStatus.BLOCKED_CONTEXT, missing_context=missing_context)

    matched: list[str] = []
    missing: list[str] = []
    for predicate in claim.required_facts:
        candidates = [f for f in facts if f.fact_type == predicate.fact_type]
        if not candidates:
            missing.append(predicate.fact_type)
            continue
        if any(f.input_state != InputState.AVAILABLE for f in candidates):
            return _record(claim, ActivationStatus.UNRESOLVED_INPUT)
        matching = [f for f in candidates if predicate.matches(f)]
        if not matching:
            return _record(claim, ActivationStatus.INACTIVE)
        matched.extend(f.fact_id for f in matching)

    if missing:
        return _record(claim, ActivationStatus.UNRESOLVED_INPUT, missing_facts=tuple(missing))
    return _record(
        claim,
        ActivationStatus.ACTIVE,
        matched_facts=tuple(matched),
        active_alternatives=claim.alternatives,
        anti_inferences=claim.anti_inferences,
    )


def _record(claim: ExecutableClaim, status: ActivationStatus, **kwargs: Any) -> ActivationRecord:
    trace = tuple(claim.doctrine_ids) + tuple(claim.canonical_anchors)
    return ActivationRecord(
        claim_id=claim.claim_id,
        rule_version=claim.rule_version,
        activation_status=status,
        provenance_trace=trace,
        **kwargs,
    )
