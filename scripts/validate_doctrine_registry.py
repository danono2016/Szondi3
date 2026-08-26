#!/usr/bin/env python3
"""Validate Szondi3 P2A doctrine registry JSONL files.

This validator enforces structural/provenance boundaries only. It does not
claim semantic or doctrinal correctness.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

DOCTRINE_ID_RE = re.compile(r"^DR_([A-Z0-9_]+)_([0-9]{6})$")
UNIT_RE = re.compile(r"^U[0-9]{6}$")

ALLOWED_ASSERTION_MODES = {
    "DEFINITION",
    "DESCRIPTIVE_CLAIM",
    "CAUSAL_CLAIM",
    "HEREDITARY_GENETIC_CLAIM",
    "GENOTROPIC_CLAIM",
    "DIAGNOSTIC_PATHODIAGNOSTIC_CLAIM",
    "PROGNOSTIC_CLAIM",
    "METHOD_RULE",
    "TYPOLOGY_CLASSIFICATION",
    "INTERPRETIVE_ASSOCIATION",
    "EMPIRICAL_GENERALIZATION",
    "NORMATIVE_THERAPEUTIC_CLAIM",
    "OTHER_EXPLICIT",
}

ALLOWED_ASSERTION_STRENGTHS = {
    "POSSIBILITY",
    "HYPOTHESIS",
    "ASSUMPTION",
    "SUSPICION_INDICATION",
    "TENDENCY",
    "PROBABILITY",
    "GENERALIZATION",
    "ASSERTION",
    "DEFINITIONAL",
    "UNCLEAR_SOURCE_STRENGTH",
}

ALLOWED_REVIEW_STATUSES = {
    "DRAFT_EXTRACTED",
    "SOURCE_VERIFIED",
    "CLINICIAN_REVIEWED",
    "ACCEPTED",
    "UNRESOLVED",
    "REOPENED",
}

ALLOWED_RELATIONS = {
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

FORBIDDEN_EXECUTABLE_FIELDS = {
    "trigger",
    "triggers",
    "triggerExpression",
    "activationCondition",
    "activationConditions",
    "protocolMatch",
    "antiInference",
    "antiInferences",
    "runtimeConfidence",
    "confidenceScore",
}

REQUIRED_FIELDS = {
    "schemaVersion",
    "doctrineId",
    "sourceId",
    "sourceLayer",
    "authorTradition",
    "sourceAnchors",
    "sourceLanguage",
    "sourceExcerpt",
    "romanianRendering",
    "doctrinalStatement",
    "assertionMode",
    "assertionStrength",
    "conditions",
    "exceptions",
    "scopeNotes",
    "terms",
    "historicallySensitiveTerms",
    "hereditaryGeneticContent",
    "sexualContent",
    "pathodiagnosticContent",
    "criminologicalContent",
    "relations",
    "ambiguities",
    "contradictions",
    "reviewStatus",
    "reviewNotes",
}


def load_catalog(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["sourceId"]: entry for entry in data["sources"]}


def expected_author(source_id: str) -> str:
    if source_id.startswith("SZ_"):
        return "SZONDI"
    if source_id == "DERI_1949":
        return "DERI"
    if source_id == "MELON_1975":
        return "MELON"
    raise ValueError(f"Unknown admitted source for author mapping: {source_id}")


def iter_entries(paths: Iterable[Path]):
    for path in paths:
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
                yield path, line_number, entry


def require_string(entry: dict, field: str, where: str) -> None:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: {field} must be a non-empty string")


def require_string_array(entry: dict, field: str, where: str) -> None:
    value = entry.get(field)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{where}: {field} must be an array of strings")


def validate_entry(entry: dict, catalog: dict[str, dict], where: str) -> None:
    missing = sorted(REQUIRED_FIELDS - entry.keys())
    if missing:
        raise ValueError(f"{where}: missing required fields: {missing}")

    forbidden = sorted(FORBIDDEN_EXECUTABLE_FIELDS & entry.keys())
    if forbidden:
        raise ValueError(f"{where}: executable fields forbidden in P2A: {forbidden}")

    if entry["schemaVersion"] != 1:
        raise ValueError(f"{where}: schemaVersion must be 1")

    doctrine_id = entry["doctrineId"]
    match = DOCTRINE_ID_RE.fullmatch(doctrine_id) if isinstance(doctrine_id, str) else None
    if not match:
        raise ValueError(f"{where}: invalid doctrineId: {doctrine_id!r}")

    source_id = entry["sourceId"]
    if source_id not in catalog:
        raise ValueError(f"{where}: sourceId is not admitted: {source_id!r}")
    if match.group(1) != source_id:
        raise ValueError(f"{where}: doctrineId source prefix does not match sourceId")

    expected_layer = catalog[source_id]["layer"]
    if entry["sourceLayer"] != expected_layer:
        raise ValueError(
            f"{where}: sourceLayer {entry['sourceLayer']!r} does not match catalog {expected_layer!r}"
        )

    author = expected_author(source_id)
    if entry["authorTradition"] != author:
        raise ValueError(
            f"{where}: authorTradition {entry['authorTradition']!r} does not match {author!r}"
        )

    for field in ("sourceLanguage", "sourceExcerpt", "romanianRendering", "doctrinalStatement"):
        require_string(entry, field, where)

    modes = entry["assertionMode"]
    if not isinstance(modes, list) or not modes or len(modes) != len(set(modes)):
        raise ValueError(f"{where}: assertionMode must be a non-empty unique array")
    unknown_modes = sorted(set(modes) - ALLOWED_ASSERTION_MODES)
    if unknown_modes:
        raise ValueError(f"{where}: invalid assertionMode values: {unknown_modes}")

    if entry["assertionStrength"] not in ALLOWED_ASSERTION_STRENGTHS:
        raise ValueError(f"{where}: invalid assertionStrength")

    if entry["reviewStatus"] not in ALLOWED_REVIEW_STATUSES:
        raise ValueError(f"{where}: invalid reviewStatus")

    for field in (
        "conditions",
        "exceptions",
        "scopeNotes",
        "terms",
        "historicallySensitiveTerms",
        "ambiguities",
        "contradictions",
        "reviewNotes",
    ):
        require_string_array(entry, field, where)

    for field in (
        "hereditaryGeneticContent",
        "sexualContent",
        "pathodiagnosticContent",
        "criminologicalContent",
    ):
        if not isinstance(entry[field], bool):
            raise ValueError(f"{where}: {field} must be boolean")

    anchors = entry["sourceAnchors"]
    if not isinstance(anchors, list) or not anchors:
        raise ValueError(f"{where}: sourceAnchors must be a non-empty array")
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            raise ValueError(f"{where}: sourceAnchors[{index}] must be an object")
        for field in ("stream", "unitStart", "unitEnd"):
            if field not in anchor:
                raise ValueError(f"{where}: sourceAnchors[{index}] missing {field}")
        if not isinstance(anchor["stream"], str) or not anchor["stream"]:
            raise ValueError(f"{where}: sourceAnchors[{index}].stream must be non-empty")
        if not UNIT_RE.fullmatch(anchor["unitStart"]) or not UNIT_RE.fullmatch(anchor["unitEnd"]):
            raise ValueError(f"{where}: invalid canonical unit identifier")
        if int(anchor["unitStart"][1:]) > int(anchor["unitEnd"][1:]):
            raise ValueError(f"{where}: source anchor unitStart is after unitEnd")
        pdf_path = anchor.get("pdfPath")
        if pdf_path is not None and pdf_path != catalog[source_id].get("pdfPath"):
            raise ValueError(f"{where}: source anchor pdfPath does not match source catalog")

    relations = entry["relations"]
    if not isinstance(relations, list):
        raise ValueError(f"{where}: relations must be an array")
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            raise ValueError(f"{where}: relations[{index}] must be an object")
        if relation.get("type") not in ALLOWED_RELATIONS:
            raise ValueError(f"{where}: relations[{index}] has invalid type")
        target = relation.get("targetDoctrineId")
        if not isinstance(target, str) or not DOCTRINE_ID_RE.fullmatch(target):
            raise ValueError(f"{where}: relations[{index}] has invalid targetDoctrineId")

    execution_status = entry.get("executionStatus")
    if execution_status not in (None, "NOT_ASSESSED", "NOT_EXECUTABLE_YET"):
        raise ValueError(f"{where}: invalid executionStatus")


def validate_registry(paths: Iterable[Path], catalog_path: Path) -> None:
    catalog = load_catalog(catalog_path)
    entries = list(iter_entries(paths))
    seen_ids: set[str] = set()
    relation_targets: set[str] = set()

    for path, line_number, entry in entries:
        where = f"{path}:{line_number}"
        validate_entry(entry, catalog, where)
        doctrine_id = entry["doctrineId"]
        if doctrine_id in seen_ids:
            raise ValueError(f"{where}: duplicate doctrineId {doctrine_id}")
        seen_ids.add(doctrine_id)
        relation_targets.update(rel["targetDoctrineId"] for rel in entry["relations"])

    orphan_targets = sorted(relation_targets - seen_ids)
    if orphan_targets:
        raise ValueError(f"orphan relation targets: {orphan_targets}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--catalog", type=Path, default=Path("config/source_catalog.json"))
    args = parser.parse_args()

    registry_paths: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            registry_paths.extend(sorted(path.glob("*.jsonl")))
        else:
            registry_paths.append(path)

    if not registry_paths:
        raise SystemExit("No doctrine registry JSONL files found")

    try:
        validate_registry(registry_paths, args.catalog)
    except ValueError as exc:
        raise SystemExit(f"P2A DOCTRINE REGISTRY VALIDATION: FAIL: {exc}") from exc

    print(f"P2A DOCTRINE REGISTRY VALIDATION: PASS ({len(registry_paths)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
