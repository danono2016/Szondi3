#!/usr/bin/env python3
"""Validate Szondi3 P2A transversal concept/relation/open-question records.

This validator is deliberately structural. It protects identity, provenance
boundaries, relation vocabulary and the no-P2B-leakage rule. It does not claim
that a cross-source relation is semantically or clinically correct.

The transversal files are optional before integration begins. Once present,
they are validated against the source-local doctrine IDs available in the
registry snapshot.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


DOCTRINE_ID_RE = re.compile(r"^DR_[A-Z0-9_]+_[0-9]{6}$")
CONCEPT_ID_RE = re.compile(r"^DC_[0-9]{6}$")
RELATION_ID_RE = re.compile(r"^XR_[0-9]{6}$")
QUESTION_ID_RE = re.compile(r"^UQ_[0-9]{6}$")

ALLOWED_RELATION_TYPES = {
    "QUALIFIES",
    "NARROWS",
    "EXTENDS",
    "RESTATES",
    "CONTRADICTS",
    "ALTERNATIVE_FORMULATION",
    "EXAMPLE_OF",
    "DEPENDENT_ON",
    "POST_SZONDI_COMMENTARY_ON",
}

ALLOWED_RELATION_DIRECTIONS = {"DIRECTED", "SYMMETRIC"}
ALLOWED_EPISTEMIC_STATUSES = {
    "SOURCE_EXPLICIT",
    "INTEGRATION_INFERRED",
    "UNRESOLVED",
}
ALLOWED_REVIEW_STATUSES = {
    "PROPOSED",
    "SOURCE_RECHECKED",
    "CLINICIAN_REVIEWED",
    "ACCEPTED",
    "UNRESOLVED",
    "REOPENED",
}
ALLOWED_QUESTION_STATUSES = {
    "OPEN",
    "WAITING_SOURCE",
    "WAITING_REVIEW",
    "RESOLVED",
    "RETIRED",
}

FORBIDDEN_EXECUTABLE_FIELDS = {
    "trigger",
    "triggers",
    "triggerExpression",
    "activationStatus",
    "activationCondition",
    "activationConditions",
    "protocolMatch",
    "antiInference",
    "antiInferences",
    "runtimeConfidence",
    "confidenceScore",
    "reportText",
    "narrativeTemplate",
}

CONCEPT_FIELDS = {
    "schemaVersion",
    "conceptId",
    "preferredLabel",
    "retrievalLabels",
    "germanTerms",
    "romanianLabels",
    "aliases",
    "linkedDoctrineIds",
    "sourceIds",
    "broaderConceptIds",
    "narrowerConceptIds",
    "chronologyNotes",
    "terminologyNotes",
    "unresolvedNotes",
    "reviewStatus",
}

RELATION_FIELDS = {
    "schemaVersion",
    "relationId",
    "relationType",
    "fromDoctrineId",
    "toDoctrineId",
    "direction",
    "relationScope",
    "rationale",
    "epistemicStatus",
    "chronologyNotes",
    "evidenceReview",
    "reviewStatus",
    "notes",
}

EVIDENCE_REVIEW_FIELDS = {
    "fromCanonicalReconsulted",
    "toCanonicalReconsulted",
    "fromPdfReconsulted",
    "toPdfReconsulted",
    "visualArbitrationRequired",
    "reviewNotes",
}

QUESTION_FIELDS = {
    "schemaVersion",
    "questionId",
    "topic",
    "implicatedDoctrineIds",
    "issue",
    "evidenceNeeded",
    "currentEvidence",
    "status",
    "notes",
}


def source_from_doctrine_id(doctrine_id: str) -> str:
    if not DOCTRINE_ID_RE.fullmatch(doctrine_id):
        raise ValueError(f"invalid doctrineId: {doctrine_id!r}")
    return doctrine_id[3:].rsplit("_", 1)[0]


def iter_jsonl(path: Path):
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(entry, dict):
                raise ValueError(f"{path}:{line_number}: entry must be a JSON object")
            yield line_number, entry


def load_doctrine_ids(paths: Iterable[Path]) -> set[str]:
    doctrine_ids: set[str] = set()
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw in enumerate(handle, start=1):
                if not raw.strip():
                    continue
                try:
                    entry = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: invalid registry JSON: {exc}") from exc
                doctrine_id = entry.get("doctrineId") if isinstance(entry, dict) else None
                if not isinstance(doctrine_id, str) or not DOCTRINE_ID_RE.fullmatch(doctrine_id):
                    raise ValueError(f"{path}:{line_number}: invalid doctrineId in registry snapshot")
                if doctrine_id in doctrine_ids:
                    raise ValueError(f"duplicate doctrineId in registry snapshot: {doctrine_id}")
                doctrine_ids.add(doctrine_id)
    return doctrine_ids


def require_exact_fields(entry: dict, expected: set[str], where: str) -> None:
    missing = sorted(expected - entry.keys())
    if missing:
        raise ValueError(f"{where}: missing required fields: {missing}")
    unexpected = sorted(entry.keys() - expected)
    if unexpected:
        raise ValueError(f"{where}: unexpected fields: {unexpected}")


def require_string(value, label: str, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: {label} must be a non-empty string")
    return value


def require_string_array(value, label: str, where: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{where}: {label} must be an array of strings")
    if nonempty and not value:
        raise ValueError(f"{where}: {label} must be non-empty")
    if len(value) != len(set(value)):
        raise ValueError(f"{where}: {label} must not contain duplicates")
    return value


def reject_executable_fields(value, where: str, path: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in FORBIDDEN_EXECUTABLE_FIELDS:
                raise ValueError(f"{where}: executable field forbidden in P2A transversal layer: {child_path}")
            reject_executable_fields(child, where, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_executable_fields(child, where, f"{path}[{index}]")


def validate_concepts(entries: list[tuple[str, dict]], doctrine_ids: set[str]) -> None:
    concept_ids: set[str] = set()
    pending_links: list[tuple[str, str, str]] = []

    for where, entry in entries:
        reject_executable_fields(entry, where)
        require_exact_fields(entry, CONCEPT_FIELDS, where)
        if entry["schemaVersion"] != 1:
            raise ValueError(f"{where}: schemaVersion must be 1")

        concept_id = entry["conceptId"]
        if not isinstance(concept_id, str) or not CONCEPT_ID_RE.fullmatch(concept_id):
            raise ValueError(f"{where}: invalid conceptId")
        if concept_id in concept_ids:
            raise ValueError(f"{where}: duplicate conceptId {concept_id}")
        concept_ids.add(concept_id)

        require_string(entry["preferredLabel"], "preferredLabel", where)
        for field in (
            "retrievalLabels",
            "germanTerms",
            "romanianLabels",
            "aliases",
            "chronologyNotes",
            "terminologyNotes",
            "unresolvedNotes",
        ):
            require_string_array(entry[field], field, where)

        linked = require_string_array(entry["linkedDoctrineIds"], "linkedDoctrineIds", where, nonempty=True)
        for doctrine_id in linked:
            if not DOCTRINE_ID_RE.fullmatch(doctrine_id):
                raise ValueError(f"{where}: invalid linked doctrineId {doctrine_id!r}")
            if doctrine_id not in doctrine_ids:
                raise ValueError(f"{where}: orphan linked doctrineId {doctrine_id}")

        source_ids = require_string_array(entry["sourceIds"], "sourceIds", where, nonempty=True)
        expected_sources = {source_from_doctrine_id(item) for item in linked}
        if set(source_ids) != expected_sources:
            raise ValueError(f"{where}: sourceIds must exactly match linked doctrine sources")

        for field in ("broaderConceptIds", "narrowerConceptIds"):
            for target in require_string_array(entry[field], field, where):
                if not CONCEPT_ID_RE.fullmatch(target):
                    raise ValueError(f"{where}: invalid {field} target {target!r}")
                if target == concept_id:
                    raise ValueError(f"{where}: concept cannot link to itself via {field}")
                pending_links.append((where, field, target))

        if entry["reviewStatus"] not in ALLOWED_REVIEW_STATUSES:
            raise ValueError(f"{where}: invalid reviewStatus")

    for where, field, target in pending_links:
        if target not in concept_ids:
            raise ValueError(f"{where}: orphan {field} target {target}")


def validate_relations(entries: list[tuple[str, dict]], doctrine_ids: set[str]) -> None:
    relation_ids: set[str] = set()

    for where, entry in entries:
        reject_executable_fields(entry, where)
        require_exact_fields(entry, RELATION_FIELDS, where)
        if entry["schemaVersion"] != 1:
            raise ValueError(f"{where}: schemaVersion must be 1")

        relation_id = entry["relationId"]
        if not isinstance(relation_id, str) or not RELATION_ID_RE.fullmatch(relation_id):
            raise ValueError(f"{where}: invalid relationId")
        if relation_id in relation_ids:
            raise ValueError(f"{where}: duplicate relationId {relation_id}")
        relation_ids.add(relation_id)

        if entry["relationType"] not in ALLOWED_RELATION_TYPES:
            raise ValueError(f"{where}: invalid relationType")
        if entry["direction"] not in ALLOWED_RELATION_DIRECTIONS:
            raise ValueError(f"{where}: invalid direction")
        if entry["epistemicStatus"] not in ALLOWED_EPISTEMIC_STATUSES:
            raise ValueError(f"{where}: invalid epistemicStatus")
        if entry["reviewStatus"] not in ALLOWED_REVIEW_STATUSES:
            raise ValueError(f"{where}: invalid reviewStatus")

        from_id = entry["fromDoctrineId"]
        to_id = entry["toDoctrineId"]
        for label, doctrine_id in (("fromDoctrineId", from_id), ("toDoctrineId", to_id)):
            if not isinstance(doctrine_id, str) or not DOCTRINE_ID_RE.fullmatch(doctrine_id):
                raise ValueError(f"{where}: invalid {label}")
            if doctrine_id not in doctrine_ids:
                raise ValueError(f"{where}: orphan {label} {doctrine_id}")
        if from_id == to_id:
            raise ValueError(f"{where}: relation endpoints must differ")
        if source_from_doctrine_id(from_id) == source_from_doctrine_id(to_id):
            raise ValueError(f"{where}: cross-source relation endpoints must belong to different sourceIds")

        require_string_array(entry["relationScope"], "relationScope", where, nonempty=True)
        require_string(entry["rationale"], "rationale", where)
        require_string_array(entry["chronologyNotes"], "chronologyNotes", where)
        require_string_array(entry["notes"], "notes", where)

        evidence = entry["evidenceReview"]
        if not isinstance(evidence, dict):
            raise ValueError(f"{where}: evidenceReview must be an object")
        require_exact_fields(evidence, EVIDENCE_REVIEW_FIELDS, f"{where}.evidenceReview")
        for field in (
            "fromCanonicalReconsulted",
            "toCanonicalReconsulted",
            "fromPdfReconsulted",
            "toPdfReconsulted",
            "visualArbitrationRequired",
        ):
            if not isinstance(evidence[field], bool):
                raise ValueError(f"{where}.evidenceReview: {field} must be boolean")
        require_string_array(evidence["reviewNotes"], "reviewNotes", f"{where}.evidenceReview")

        if entry["reviewStatus"] in {"SOURCE_RECHECKED", "CLINICIAN_REVIEWED", "ACCEPTED"}:
            if not evidence["fromCanonicalReconsulted"] or not evidence["toCanonicalReconsulted"]:
                raise ValueError(f"{where}: reviewed relation requires canonical reconsultation on both sides")
        if evidence["visualArbitrationRequired"] and not (
            evidence["fromPdfReconsulted"] or evidence["toPdfReconsulted"]
        ):
            raise ValueError(f"{where}: visual arbitration requires relevant PDF reconsultation")


def validate_open_questions(entries: list[tuple[str, dict]], doctrine_ids: set[str]) -> None:
    question_ids: set[str] = set()

    for where, entry in entries:
        reject_executable_fields(entry, where)
        require_exact_fields(entry, QUESTION_FIELDS, where)
        if entry["schemaVersion"] != 1:
            raise ValueError(f"{where}: schemaVersion must be 1")

        question_id = entry["questionId"]
        if not isinstance(question_id, str) or not QUESTION_ID_RE.fullmatch(question_id):
            raise ValueError(f"{where}: invalid questionId")
        if question_id in question_ids:
            raise ValueError(f"{where}: duplicate questionId {question_id}")
        question_ids.add(question_id)

        require_string(entry["topic"], "topic", where)
        require_string(entry["issue"], "issue", where)
        implicated = require_string_array(
            entry["implicatedDoctrineIds"], "implicatedDoctrineIds", where, nonempty=True
        )
        for doctrine_id in implicated:
            if not DOCTRINE_ID_RE.fullmatch(doctrine_id):
                raise ValueError(f"{where}: invalid implicated doctrineId {doctrine_id!r}")
            if doctrine_id not in doctrine_ids:
                raise ValueError(f"{where}: orphan implicated doctrineId {doctrine_id}")
        for field in ("evidenceNeeded", "currentEvidence", "notes"):
            require_string_array(entry[field], field, where)
        if entry["status"] not in ALLOWED_QUESTION_STATUSES:
            raise ValueError(f"{where}: invalid status")


def read_optional_records(path: Path, label: str) -> list[tuple[str, dict]]:
    if not path.exists():
        return []
    return [(f"{path}:{line}", entry) for line, entry in iter_jsonl(path)]


def validate_transversal_layer(
    *,
    registry_paths: Iterable[Path],
    concepts_path: Path,
    relations_path: Path,
    open_questions_path: Path,
) -> tuple[int, int, int]:
    registry_paths = list(registry_paths)
    if not registry_paths:
        raise ValueError("no doctrine registry files supplied")
    doctrine_ids = load_doctrine_ids(registry_paths)

    concepts = read_optional_records(concepts_path, "concepts")
    relations = read_optional_records(relations_path, "relations")
    questions = read_optional_records(open_questions_path, "open questions")

    validate_concepts(concepts, doctrine_ids)
    validate_relations(relations, doctrine_ids)
    validate_open_questions(questions, doctrine_ids)
    return len(concepts), len(relations), len(questions)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-dir", type=Path, default=Path("doctrine/registry"))
    parser.add_argument("--concepts", type=Path, default=Path("doctrine/index/concepts.jsonl"))
    parser.add_argument("--relations", type=Path, default=Path("doctrine/relations/cross_source.jsonl"))
    parser.add_argument(
        "--open-questions",
        type=Path,
        default=Path("doctrine/unresolved/open_questions.jsonl"),
    )
    args = parser.parse_args()

    registry_paths = sorted(args.registry_dir.glob("*.jsonl"))
    try:
        counts = validate_transversal_layer(
            registry_paths=registry_paths,
            concepts_path=args.concepts,
            relations_path=args.relations,
            open_questions_path=args.open_questions,
        )
    except ValueError as exc:
        raise SystemExit(f"P2A TRANSVERSAL VALIDATION: FAIL: {exc}") from exc

    print(
        "P2A TRANSVERSAL VALIDATION: PASS "
        f"({counts[0]} concept(s), {counts[1]} relation(s), {counts[2]} open question(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
