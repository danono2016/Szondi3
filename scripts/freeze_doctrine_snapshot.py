#!/usr/bin/env python3
"""Build a deterministic manifest for a reviewed doctrine integration snapshot.

The manifest freezes *identity*, not interpretation. It is intended to be run
after the required source-local corpora coexist on one commit (normally main)
and before cross-source concept/relation records are authored against them.

No timestamps are emitted so identical inputs produce byte-identical JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DOCTRINE_ID_RE = re.compile(r"^DR_([A-Z0-9_]+)_([0-9]{6})$")


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def iter_registry_entries(paths: Iterable[Path]):
    for path in sorted(paths, key=lambda item: item.as_posix()):
        raw_bytes = path.read_bytes()
        file_digest = sha256_hex(raw_bytes)
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
                doctrine_id = entry.get("doctrineId")
                source_id = entry.get("sourceId")
                if not isinstance(doctrine_id, str) or not DOCTRINE_ID_RE.fullmatch(doctrine_id):
                    raise ValueError(f"{path}:{line_number}: invalid doctrineId")
                if not isinstance(source_id, str) or not source_id:
                    raise ValueError(f"{path}:{line_number}: invalid sourceId")
                match = DOCTRINE_ID_RE.fullmatch(doctrine_id)
                assert match is not None
                if match.group(1) != source_id:
                    raise ValueError(f"{path}:{line_number}: doctrineId/sourceId mismatch")
                yield path, file_digest, line_number, entry


def digest_entries(entries: list[dict]) -> str:
    payload = b"\n".join(canonical_json_bytes(entry) for entry in sorted(entries, key=lambda x: x["doctrineId"]))
    return sha256_hex(payload)


def build_snapshot(
    *,
    registry_paths: Iterable[Path],
    source_ids: Iterable[str],
    commit_sha: str,
) -> dict:
    if not isinstance(commit_sha, str) or not COMMIT_RE.fullmatch(commit_sha):
        raise ValueError("commit_sha must be a full lowercase 40-hex Git commit SHA")

    selected_sources = sorted(set(source_ids))
    if not selected_sources:
        raise ValueError("at least one sourceId must be selected")
    if any(not isinstance(source_id, str) or not source_id for source_id in selected_sources):
        raise ValueError("sourceIds must be non-empty strings")

    registry_paths = list(registry_paths)
    if not registry_paths:
        raise ValueError("no doctrine registry files supplied")

    entries: list[dict] = []
    seen_ids: set[str] = set()
    by_source: dict[str, list[dict]] = defaultdict(list)
    input_file_counts: Counter[tuple[str, str]] = Counter()

    for path, file_digest, line_number, entry in iter_registry_entries(registry_paths):
        doctrine_id = entry["doctrineId"]
        if doctrine_id in seen_ids:
            raise ValueError(f"duplicate doctrineId in registry snapshot: {doctrine_id}")
        seen_ids.add(doctrine_id)

        source_id = entry["sourceId"]
        if source_id not in selected_sources:
            continue
        entries.append(entry)
        by_source[source_id].append(entry)
        input_file_counts[(path.as_posix(), file_digest)] += 1

    missing_sources = [source_id for source_id in selected_sources if not by_source.get(source_id)]
    if missing_sources:
        raise ValueError(f"selected sourceIds have no doctrine entries: {missing_sources}")

    entries.sort(key=lambda entry: entry["doctrineId"])
    doctrine_ids = [entry["doctrineId"] for entry in entries]
    registry_digest = digest_entries(entries)
    source_digests = {
        source_id: digest_entries(by_source[source_id])
        for source_id in selected_sources
    }
    source_counts = {
        source_id: len(by_source[source_id])
        for source_id in selected_sources
    }
    input_files = [
        {
            "path": path,
            "sha256": digest,
            "selectedDoctrineCount": count,
        }
        for (path, digest), count in sorted(input_file_counts.items())
    ]

    identity_payload = canonical_json_bytes(
        {
            "integrationCommit": commit_sha,
            "selectedSourceIds": selected_sources,
            "registryDigest": registry_digest,
        }
    )
    snapshot_id = f"DS_{sha256_hex(identity_payload)[:16].upper()}"

    return {
        "schemaVersion": 1,
        "purpose": "Deterministic identity manifest for a P2A cross-source integration snapshot; not doctrinal authority.",
        "snapshotId": snapshot_id,
        "integrationCommit": commit_sha,
        "selectedSourceIds": selected_sources,
        "doctrineCount": len(entries),
        "sourceCounts": source_counts,
        "sourceDigests": source_digests,
        "registryDigest": registry_digest,
        "doctrineIds": doctrine_ids,
        "inputFiles": input_files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-dir", type=Path, default=Path("doctrine/registry"))
    parser.add_argument("--source-id", action="append", dest="source_ids", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    paths = sorted(args.registry_dir.glob("*.jsonl"))
    try:
        manifest = build_snapshot(
            registry_paths=paths,
            source_ids=args.source_ids,
            commit_sha=args.commit_sha,
        )
    except ValueError as exc:
        raise SystemExit(f"P2A DOCTRINE SNAPSHOT: FAIL: {exc}") from exc

    rendered = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"P2A DOCTRINE SNAPSHOT: PASS ({manifest['snapshotId']}, {manifest['doctrineCount']} doctrine(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
