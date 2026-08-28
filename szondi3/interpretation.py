"""Fail-closed executable interpretation primitives (P2B).

P2B consumes typed facts produced by the deterministic P1 layer. It does not
recalculate scoring, break P1 ties, or infer missing clinical context. Claim
content remains source-linked and lifecycle-aware so report layers can distinguish
formal source-grounded output from later clinical synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Iterable, Mapping


class InputState(str, Enum):
    AVAILABLE = "AVAILABLE"
    AMBIGUOUS = "AMBIGUOUS"
    UNDEFINED = "UNDEFINED"
    MISSING = "MISSING"


class ActivationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNRESOLVED_INPUT = "UNRESOLVED_INPUT"
    BLOCKED_CONTEXT = "BLOCKED_CONTEXT"
    BLOCKED_SOURCE_CONFLICT = "BLOCKED_SOURCE_CONFLICT"


class AssertionMode(str, Enum):
    DEFINITIONAL = "DEFINITIONAL"
    CATEGORICAL = "CATEGORICAL"
    CONDITIONAL = "CONDITIONAL"
    PROBABLE = "PROBABLE"
    POSSIBLE = "POSSIBLE"
    HYPOTHESIS = "HYPOTHESIS"
    WARNING = "WARNING"
    LIMITATION = "LIMITATION"


class EpistemicClass(str, Enum):
    SOURCE_ESTABLISHED_TRIGGER = "SOURCE_ESTABLISHED_TRIGGER"
    IMPLEMENTATION_INFERRED_TRIGGER = "IMPLEMENTATION_INFERRED_TRIGGER"
    POST_SZONDI_TRIGGER = "POST_SZONDI_TRIGGER"
    UNRESOLVED_NO_RULE = "UNRESOLVED_NO_RULE"


class TriggerKind(str, Enum):
    EXACT_STRUCTURAL = "EXACT_STRUCTURAL"
    CONDITIONAL_CONTEXTUAL = "CONDITIONAL_CONTEXTUAL"
    POLYSEMIC = "POLYSEMIC"
    LIMITATION_GUARD = "LIMITATION_GUARD"
    COMPOSITE = "COMPOSITE"


class LifecycleStatus(str, Enum):
    DRAFT = "DRAFT"
    SOURCE_LINKED = "SOURCE_LINKED"
    FORMALIZATION_REVIEWED = "FORMALIZATION_REVIEWED"
    CLINICIAN_REVIEWED = "CLINICIAN_REVIEWED"
    APPROVED = "APPROVED"
    RETIRED = "RETIRED"
    SUPERSEDED = "SUPERSEDED"


class Operator(str, Enum):
    EQ = "EQ"
    NE = "NE"
    LT = "LT"
    LTE = "LTE"
    GT = "GT"
    GTE = "GTE"
    IN = "IN"
    EXISTS = "EXISTS"


@dataclass(frozen=True, slots=True)
class Fact:
    """Typed P1/context fact made available to the P2B evaluator."""

    key: str
    value: Any = None
    scope: str = "test"
    input_state: InputState = InputState.AVAILABLE
    fact_id: str | None = None
    calculation_version: str | None = None


@dataclass(frozen=True, slots=True)
class Predicate:
    fact_key: str
    operator: Operator
    expected: Any = None


@dataclass(frozen=True, slots=True)
class TriggerDefinition:
    kind: TriggerKind
    predicates: tuple[Predicate, ...]
    context_requirements: tuple[str, ...] = ()
    ambiguity_policy: str = "FAIL_CLOSED"


@dataclass(frozen=True, slots=True)
class AntiInference:
    anti_inference_id: str
    prohibited_conclusion: str
    severity: str = "HARD_BLOCK"


@dataclass(frozen=True, slots=True)
class Alternative:
    alternative_id: str
    statement: str
    assertion_mode: AssertionMode
    required_discriminator: str | None = None


@dataclass(frozen=True, slots=True)
class ClaimDefinition:
    schema_version: int
    claim_id: str
    rule_version: int
    status: LifecycleStatus
    source_layer: str
    doctrine_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    epistemic_class: EpistemicClass
    assertion_mode: AssertionMode
    source_strength_note: str
    claim: str
    trigger: TriggerDefinition
    anti_inferences: tuple[AntiInference, ...] = ()
    alternatives: tuple[Alternative, ...] = ()
    inference_rationale: str | None = None
    reversal_condition: str | None = None
    sexual_content: bool = False
    pathodiagnostic_content: bool = False
    criminological_content: bool = False
    hereditary_genetic_content: bool = False

    def __post_init__(self) -> None:
        if not self.doctrine_ids:
            raise ValueError("Executable claims require at least one doctrineId")
        if not self.source_ids:
            raise ValueError("Executable claims require at least one sourceId")
        if self.rule_version < 1 or self.schema_version < 1:
            raise ValueError("schema_version and rule_version must be positive")
        if self.epistemic_class is EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER:
            if not self.inference_rationale or not self.reversal_condition:
                raise ValueError(
                    "Implementation-inferred triggers require rationale and reversal condition"
                )
        if (
            self.epistemic_class is EpistemicClass.POST_SZONDI_TRIGGER
            and self.source_layer == "SZONDI_PRIMARY"
        ):
            raise ValueError("Post-Szondi triggers cannot be labelled SZONDI_PRIMARY")


@dataclass(frozen=True, slots=True)
class ActivationRecord:
    claim_id: str
    rule_version: int
    activation_status: ActivationStatus
    matched_facts: tuple[Fact, ...] = ()
    missing_facts: tuple[str, ...] = ()
    missing_context: tuple[str, ...] = ()
    active_alternatives: tuple[Alternative, ...] = ()
    anti_inferences: tuple[AntiInference, ...] = ()
    qualifications: tuple[str, ...] = ()
    provenance_trace: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DoctrineRef:
    doctrine_id: str
    source_id: str
    source_layer: str
    anchors: tuple[str, ...]


def _coerce_orderable(value: Any) -> Any:
    """Keep exact Fraction arithmetic comparable without float conversion."""
    if isinstance(value, Fraction):
        return value
    return value


def _matches(predicate: Predicate, value: Any) -> bool:
    op = predicate.operator
    expected = predicate.expected
    if op is Operator.EXISTS:
        return True
    if op is Operator.EQ:
        return value == expected
    if op is Operator.NE:
        return value != expected
    if op is Operator.IN:
        return value in expected

    left = _coerce_orderable(value)
    right = _coerce_orderable(expected)
    if op is Operator.LT:
        return left < right
    if op is Operator.LTE:
        return left <= right
    if op is Operator.GT:
        return left > right
    if op is Operator.GTE:
        return left >= right
    raise ValueError(f"Unsupported predicate operator: {op}")


def evaluate_claim(
    claim: ClaimDefinition,
    facts: Iterable[Fact],
    *,
    context: Mapping[str, Any] | None = None,
) -> ActivationRecord:
    """Evaluate one explicit claim without repairing missing or ambiguous input."""
    context = context or {}
    missing_context = tuple(
        item for item in claim.trigger.context_requirements if item not in context
    )
    provenance = claim.doctrine_ids + claim.source_ids
    if missing_context:
        return ActivationRecord(
            claim_id=claim.claim_id,
            rule_version=claim.rule_version,
            activation_status=ActivationStatus.BLOCKED_CONTEXT,
            missing_context=missing_context,
            provenance_trace=provenance,
        )

    if claim.epistemic_class is EpistemicClass.UNRESOLVED_NO_RULE:
        return ActivationRecord(
            claim_id=claim.claim_id,
            rule_version=claim.rule_version,
            activation_status=ActivationStatus.BLOCKED_SOURCE_CONFLICT,
            provenance_trace=provenance,
        )

    by_key: dict[str, Fact] = {}
    for fact in facts:
        if fact.key in by_key:
            raise ValueError(f"Duplicate fact key supplied to P2B: {fact.key}")
        by_key[fact.key] = fact

    matched: list[Fact] = []
    missing: list[str] = []
    for predicate in claim.trigger.predicates:
        fact = by_key.get(predicate.fact_key)
        if fact is None:
            missing.append(predicate.fact_key)
            continue
        if fact.input_state is not InputState.AVAILABLE:
            return ActivationRecord(
                claim_id=claim.claim_id,
                rule_version=claim.rule_version,
                activation_status=ActivationStatus.UNRESOLVED_INPUT,
                matched_facts=tuple(matched),
                missing_facts=(predicate.fact_key,),
                provenance_trace=provenance,
            )
        if not _matches(predicate, fact.value):
            return ActivationRecord(
                claim_id=claim.claim_id,
                rule_version=claim.rule_version,
                activation_status=ActivationStatus.INACTIVE,
                matched_facts=tuple(matched),
                provenance_trace=provenance,
            )
        matched.append(fact)

    if missing:
        return ActivationRecord(
            claim_id=claim.claim_id,
            rule_version=claim.rule_version,
            activation_status=ActivationStatus.UNRESOLVED_INPUT,
            matched_facts=tuple(matched),
            missing_facts=tuple(missing),
            provenance_trace=provenance,
        )

    return ActivationRecord(
        claim_id=claim.claim_id,
        rule_version=claim.rule_version,
        activation_status=ActivationStatus.ACTIVE,
        matched_facts=tuple(matched),
        active_alternatives=claim.alternatives,
        anti_inferences=claim.anti_inferences,
        provenance_trace=provenance,
    )


def evaluate_catalogue(
    claims: Iterable[ClaimDefinition],
    facts: Iterable[Fact],
    *,
    context: Mapping[str, Any] | None = None,
    production: bool = False,
) -> tuple[ActivationRecord, ...]:
    """Evaluate a catalogue; production mode admits only APPROVED claims."""
    fact_tuple = tuple(facts)
    result = []
    for claim in claims:
        if production and claim.status is not LifecycleStatus.APPROVED:
            continue
        if claim.status in {LifecycleStatus.RETIRED, LifecycleStatus.SUPERSEDED}:
            continue
        result.append(evaluate_claim(claim, fact_tuple, context=context))
    return tuple(result)
