#!/usr/bin/env python3
"""Validate P2A doctrine entries against regenerated canonical access.

This verifier proves evidence-address integrity and exact excerpt presence. It
still does not prove the semantic correctness of Romanian renderings or
normalized doctrinal statements; those remain source/clinician review tasks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def iter_jsonl(paths: Iterable[Path]):
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw in enumerate(handle, start=1):
                if not raw.strip():
                    continue
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
                if not isinstance(value, dict):
                    raise ValueError(f"{path}:{line_number}: JSONL record must be an object")
                yield path, line_number, value


def canonical_paths(canonical_dir: Path) -> list[Path]:
    paths = sorted(path for path in canonical_dir.glob("*.jsonl") if path.is_file())
    if not paths:
        raise ValueError(f"no canonical JSONL files found under {canonical_dir}")
    return paths


def registry_paths(registry_dir: Path) -> list[Path]:
    paths = sorted(path for path in registry_dir.glob("*.jsonl") if path.is_file())
    if not paths:
        raise ValueError(f"no doctrine registry JSONL files found under {registry_dir}")
    return paths


def load_canonical(canonical_dir: Path) -> dict[tuple[str, str, str], dict]:
    index: dict[tuple[str, str, str], dict] = {}
    for path, line_number, record in iter_jsonl(canonical_paths(canonical_dir)):
        # Canonical access intentionally contains structural/non-text units too.
        # Those units need not carry `text`; they remain valid addresses. A
        # doctrine excerpt, however, can only validate if its anchored span
        # contains matching textual content.
        for field in ("sourceId", "stream", "unitId", "path", "layer"):
            if field not in record:
                raise ValueError(f"{path}:{line_number}: canonical record missing {field}")
        if "text" in record and not isinstance(record["text"], str):
            raise ValueError(f"{path}:{line_number}: canonical text must be a string when present")
        key = (record["sourceId"], record["stream"], record["unitId"])
        if key in index:
            raise ValueError(f"duplicate canonical address: {key}")
        index[key] = record
    return index


def unit_number(unit_id: str) -> int:
    if not isinstance(unit_id, str) or len(unit_id) != 7 or not unit_id.startswith("U"):
        raise ValueError(f"invalid unit id {unit_id!r}")
    return int(unit_id[1:])


def validate_entry(entry: dict, canonical: dict[tuple[str, str, str], dict], where: str) -> None:
    source_id = entry.get("sourceId")
    source_layer = entry.get("sourceLayer")
    excerpt = entry.get("sourceExcerpt")
    anchors = entry.get("sourceAnchors")
    doctrine_id = entry.get("doctrineId", "<unknown>")

    if not isinstance(source_id, str) or not source_id:
        raise ValueError(f"{where}: missing sourceId")
    if not isinstance(excerpt, str) or not excerpt:
        raise ValueError(f"{where}: missing sourceExcerpt")
    if not isinstance(anchors, list) or not anchors:
        raise ValueError(f"{where}: missing sourceAnchors")

    anchored_texts: list[str] = []
    for anchor_index, anchor in enumerate(anchors):
        stream = anchor.get("stream")
        start_id = anchor.get("unitStart")
        end_id = anchor.get("unitEnd")
        if not isinstance(stream, str) or not stream:
            raise ValueError(f"{where}: anchor {anchor_index} missing stream")
        start = unit_number(start_id)
        end = unit_number(end_id)
        if start > end:
            raise ValueError(f"{where}: anchor {anchor_index} start after end")

        records: list[dict] = []
        for number in range(start, end + 1):
            unit_id = f"U{number:06d}"
            key = (source_id, stream, unit_id)
            record = canonical.get(key)
            if record is None:
                raise ValueError(
                    f"{where}: {doctrine_id} anchor {anchor_index} references missing canonical {key}"
                )
            if record["layer"] != source_layer:
                raise ValueError(
                    f"{where}: {doctrine_id} sourceLayer {source_layer!r} differs from canonical layer {record['layer']!r}"
                )
            records.append(record)

        structural_path = anchor.get("structuralPath")
        if structural_path is not None and records[0]["path"] != structural_path:
            raise ValueError(
                f"{where}: {doctrine_id} anchor {anchor_index} structuralPath {structural_path!r} "
                f"does not match canonical {records[0]['path']!r}"
            )

        anchored_texts.append(" ".join(record.get("text", "") for record in records))

    evidence_text = " ".join(anchored_texts)
    if excerpt not in evidence_text:
        raise ValueError(
            f"{where}: {doctrine_id} sourceExcerpt is not an exact substring of its anchored canonical evidence"
        )


def validate(registry_dir: Path, canonical_dir: Path) -> int:
    canonical = load_canonical(canonical_dir)
    checked = 0
    for path, line_number, entry in iter_jsonl(registry_paths(registry_dir)):
        validate_entry(entry, canonical, f"{path}:{line_number}")
        checked += 1
    if checked == 0:
        raise ValueError("registry contains no entries")
    return checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-dir", type=Path, default=Path("doctrine/registry"))
    parser.add_argument("--canonical-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        checked = validate(args.registry_dir, args.canonical_dir)
    except ValueError as exc:
        raise SystemExit(f"P2A DOCTRINE EVIDENCE VALIDATION: FAIL: {exc}") from exc

    print(f"P2A DOCTRINE EVIDENCE VALIDATION: PASS ({checked} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
