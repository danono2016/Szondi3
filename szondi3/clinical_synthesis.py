"""Controlled handoff from deterministic/P2B layers to generative synthesis.

The generative model should not be asked to rediscover morphology from a printed
series.  This module gives it exact series facts, traceable authorized findings,
and the explicit source-faithful writing policy in one object.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .clinical_protocol import ClinicalProtocolEvaluation
from .clinical_synthesis_policy import (
    DEFAULT_CLINICAL_SYNTHESIS_POLICY,
    ClinicalSynthesisPolicy,
)
from .interpretation import InputState


@dataclass(frozen=True, slots=True)
class SynthesisFact:
    key: str
    value: Any
    input_state: str


@dataclass(frozen=True, slots=True)
class SynthesisFinding:
    scope: str
    profile_number: int | None
    statement: str
    claim_id: str
    doctrine_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    anti_inferences: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ClinicalSynthesisInput:
    profile_count: int
    morphology: tuple[SynthesisFact, ...]
    authorized_findings: tuple[SynthesisFinding, ...]
    instructions: tuple[str, ...]


def build_clinical_synthesis_input(
    evaluation: ClinicalProtocolEvaluation,
    *,
    policy: ClinicalSynthesisPolicy = DEFAULT_CLINICAL_SYNTHESIS_POLICY,
) -> ClinicalSynthesisInput:
    """Prepare the only material a downstream generative synthesis needs.

    Morphology is deterministic. Findings are those already released by P2B for
    the selected production/review mode.  No new doctrinal meaning is created here.
    """
    if not isinstance(evaluation, ClinicalProtocolEvaluation):
        raise TypeError("Clinical synthesis input requires a ClinicalProtocolEvaluation")

    morphology = tuple(
        SynthesisFact(
            key=fact.key,
            value=fact.value,
            input_state=fact.input_state.value,
        )
        for fact in evaluation.series_result.facts
        if fact.key.startswith("series.profile_count")
        or fact.key.startswith("series.factor.")
        or fact.key.startswith("series.vector.")
        or fact.key.startswith("series.real_null_reaction.")
    )

    findings: list[SynthesisFinding] = []
    for profile in evaluation.profiles:
        findings.extend(
            SynthesisFinding(
                scope="PROFILE",
                profile_number=profile.profile_number,
                statement=item.statement,
                claim_id=item.claim_id,
                doctrine_ids=item.doctrine_ids,
                source_ids=item.source_ids,
                anti_inferences=item.anti_inferences,
            )
            for item in profile.interpretation.findings
        )
    findings.extend(
        SynthesisFinding(
            scope="SERIES",
            profile_number=None,
            statement=item.statement,
            claim_id=item.claim_id,
            doctrine_ids=item.doctrine_ids,
            source_ids=item.source_ids,
            anti_inferences=item.anti_inferences,
        )
        for item in evaluation.series_result.interpretation.findings
    )

    return ClinicalSynthesisInput(
        profile_count=evaluation.profile_count,
        morphology=morphology,
        authorized_findings=tuple(findings),
        instructions=policy.instructions,
    )
