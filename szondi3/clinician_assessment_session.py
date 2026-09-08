"""Clinician-facing state machine for one multi-profile Szondi assessment.

This module composes the already-source-bound :mod:`administration_surface` workflow
across one to ten repeated administrations. It records choices only. It does not
score, interpret, compare, persist, or assign clinical meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import re
from typing import Iterable

from .administration import SelectionDirection
from .administration_surface import (
    AdministrationStep,
    AdministrationWorkflow,
    start_administration,
)
from .clinical_pipeline import AdministeredTestRecord


_ASSESSMENT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


def require_pseudonymous_assessment_id(value: str) -> str:
    """Validate the local product's deliberately non-identifying assessment key."""
    if not isinstance(value, str) or not _ASSESSMENT_ID_RE.fullmatch(value):
        raise ValueError(
            "assessment_id must be a pseudonymous token using only letters, digits, '.', '_' or '-'"
        )
    return value


@dataclass(frozen=True, slots=True)
class AssessmentAdministrationSession:
    """Immutable repeated-administration session before any clinical calculation."""

    assessment_id: str
    target_profile_count: int
    include_complement: bool
    prior_case_ids: tuple[str, ...]
    completed_records: tuple[AdministeredTestRecord, ...]
    workflow: AdministrationWorkflow | None

    def __post_init__(self) -> None:
        require_pseudonymous_assessment_id(self.assessment_id)
        if (
            not isinstance(self.target_profile_count, int)
            or isinstance(self.target_profile_count, bool)
            or not 1 <= self.target_profile_count <= 10
        ):
            raise ValueError("target_profile_count must be an integer from 1 to 10")
        if not isinstance(self.include_complement, bool):
            raise TypeError("include_complement must be bool")
        if any(not isinstance(item, str) or not item for item in self.prior_case_ids):
            raise TypeError("prior_case_ids must contain non-empty strings")
        if len(self.prior_case_ids) != len(set(self.prior_case_ids)):
            raise ValueError("prior_case_ids must be unique")
        if self.assessment_id in self.prior_case_ids:
            raise ValueError("Current assessment_id cannot also be a prior_case_id")
        if any(not isinstance(item, AdministeredTestRecord) for item in self.completed_records):
            raise TypeError("completed_records must contain AdministeredTestRecord objects")
        if len(self.completed_records) > self.target_profile_count:
            raise ValueError("completed_records exceed target_profile_count")

        complete = len(self.completed_records) == self.target_profile_count
        if complete:
            if self.workflow is not None:
                raise ValueError("Completed assessment session cannot retain an active workflow")
        else:
            if not isinstance(self.workflow, AdministrationWorkflow):
                raise TypeError("Incomplete assessment session requires an AdministrationWorkflow")
            if self.workflow.include_complement != self.include_complement:
                raise ValueError("Active workflow complement mode diverges from assessment session")

    @property
    def completed_profile_count(self) -> int:
        return len(self.completed_records)

    @property
    def current_profile_number(self) -> int | None:
        if self.is_complete:
            return None
        return len(self.completed_records) + 1

    @property
    def is_complete(self) -> bool:
        return len(self.completed_records) == self.target_profile_count

    @property
    def current_step(self) -> AdministrationStep | None:
        return None if self.workflow is None else self.workflow.current_step

    def _advance(self, workflow: AdministrationWorkflow) -> "AssessmentAdministrationSession":
        if workflow.phase != "COMPLETE":
            return replace(self, workflow=workflow)

        completed = self.completed_records + (workflow.build_record(),)
        if len(completed) == self.target_profile_count:
            return replace(self, completed_records=completed, workflow=None)
        return replace(
            self,
            completed_records=completed,
            workflow=start_administration(include_complement=self.include_complement),
        )

    def submit_foreground(
        self,
        *,
        sympathetic: Iterable[str],
        unsympathetic: Iterable[str],
    ) -> "AssessmentAdministrationSession":
        if self.workflow is None:
            raise RuntimeError("Assessment administration is already complete")
        return self._advance(
            self.workflow.submit_foreground(
                sympathetic=sympathetic,
                unsympathetic=unsympathetic,
            )
        )

    def submit_complement(
        self,
        *,
        selected: Iterable[str],
        selected_as: SelectionDirection,
    ) -> "AssessmentAdministrationSession":
        if self.workflow is None:
            raise RuntimeError("Assessment administration is already complete")
        return self._advance(
            self.workflow.submit_complement(
                selected=selected,
                selected_as=selected_as,
            )
        )

    def records(self) -> tuple[AdministeredTestRecord, ...]:
        """Expose complete canonical records only after the requested series closes."""
        if not self.is_complete:
            raise RuntimeError("Assessment administration is not complete")
        return self.completed_records


def start_assessment_administration(
    *,
    assessment_id: str,
    target_profile_count: int,
    include_complement: bool = False,
    prior_case_ids: Iterable[str] = (),
) -> AssessmentAdministrationSession:
    """Create the first immutable administration state for a new assessment."""
    prior = tuple(prior_case_ids)
    return AssessmentAdministrationSession(
        assessment_id=require_pseudonymous_assessment_id(assessment_id),
        target_profile_count=target_profile_count,
        include_complement=include_complement,
        prior_case_ids=prior,
        completed_records=(),
        workflow=start_administration(include_complement=include_complement),
    )
