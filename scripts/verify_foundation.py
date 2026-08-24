#!/usr/bin/env python3
"""Fail-closed verification of Szondi3's admitted evidence and foundation files.

This script verifies identity and repository structure only. It does not validate
Szondian doctrine, stimulus factor mapping, OCR correctness, or canonical text.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "config" / "evidence_lock.json"
CATALOG_PATH = ROOT / "config" / "source_catalog.json"


class VerificationError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        raise VerificationError(
            f"git {' '.join(args)} failed: {proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def main() -> int:
    require(LOCK_PATH.is_file(), f"Missing evidence lock: {LOCK_PATH}")
    require(CATALOG_PATH.is_file(), f"Missing source catalog: {CATALOG_PATH}")

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    require(lock.get("schemaVersion") == 1, "Unsupported evidence lock schema")
    require(catalog.get("schemaVersion") == 1, "Unsupported source catalog schema")

    sources = catalog.get("sources")
    require(isinstance(sources, list), "source_catalog.sources must be a list")
    require(
        len(sources) == lock["expectedCounts"]["docx"],
        "DOCX catalog count does not match evidence lock",
    )

    source_ids: set[str] = set()
    docx_paths: list[Path] = []
    catalog_pdf_paths: set[str] = set()

    for entry in sources:
        source_id = entry.get("sourceId")
        require(isinstance(source_id, str) and source_id, "Invalid sourceId")
        require(source_id not in source_ids, f"Duplicate sourceId: {source_id}")
        source_ids.add(source_id)

        layer = entry.get("layer")
        require(
            layer in {"SZONDI_PRIMARY", "POST_SZONDI_TRADITION"},
            f"Unexpected source layer for {source_id}: {layer}",
        )

        rel = entry.get("docxPath")
        expected = entry.get("docxSha256")
        require(isinstance(rel, str) and rel, f"Missing DOCX path for {source_id}")
        require(
            isinstance(expected, str) and len(expected) == 64,
            f"Missing/invalid DOCX SHA-256 for {source_id}",
        )
        path = ROOT / rel
        require(path.is_file(), f"Missing admitted DOCX: {rel}")
        actual = sha256(path)
        require(
            actual == expected,
            f"DOCX SHA-256 mismatch for {source_id}: expected {expected}, got {actual}",
        )
        docx_paths.append(path)

        pdf = entry.get("pdfPath")
        if pdf is not None:
            require(isinstance(pdf, str) and pdf, f"Invalid PDF path for {source_id}")
            catalog_pdf_paths.add(pdf)

    actual_docx = sorted((ROOT / "sources" / "text").glob("*.docx"))
    require(
        len(actual_docx) == lock["expectedCounts"]["docx"],
        f"Expected {lock['expectedCounts']['docx']} DOCX files, found {len(actual_docx)}",
    )
    require(
        {p.resolve() for p in actual_docx} == {p.resolve() for p in docx_paths},
        "sources/text DOCX set differs from source catalog",
    )

    pdf_blobs = lock.get("pdfGitBlobs", {})
    require(
        len(pdf_blobs) == lock["expectedCounts"]["pdf"],
        "PDF evidence-lock count mismatch",
    )
    require(
        set(pdf_blobs) == catalog_pdf_paths,
        "PDF paths in evidence lock differ from source catalog",
    )

    actual_pdf = sorted((ROOT / "sources" / "originals").glob("*.pdf"))
    require(
        len(actual_pdf) == lock["expectedCounts"]["pdf"],
        f"Expected {lock['expectedCounts']['pdf']} PDFs, found {len(actual_pdf)}",
    )
    require(
        {str(p.relative_to(ROOT)) for p in actual_pdf} == set(pdf_blobs),
        "sources/originals PDF set differs from evidence lock",
    )

    for rel, expected_blob in sorted(pdf_blobs.items()):
        path = ROOT / rel
        require(path.is_file(), f"Missing admitted PDF: {rel}")
        actual_blob = git("hash-object", rel)
        require(
            actual_blob == expected_blob,
            f"PDF Git blob mismatch for {rel}: expected {expected_blob}, got {actual_blob}",
        )

    stim = lock["stimuli"]
    stim_dir = ROOT / stim["directory"]
    require(stim_dir.is_dir(), f"Missing stimuli directory: {stim['directory']}")
    actual_stimuli = sorted(stim_dir.glob("*.webp"))
    require(
        len(actual_stimuli) == lock["expectedCounts"]["stimuliWebp"],
        f"Expected {lock['expectedCounts']['stimuliWebp']} WebP stimuli, found {len(actual_stimuli)}",
    )
    unexpected = [p.name for p in stim_dir.iterdir() if p.is_file() and p.suffix.lower() != ".webp"]
    require(not unexpected, f"Unexpected non-WebP files in stimuli directory: {unexpected}")

    # A Git tree identity locks filenames, modes and blob identities for the whole set.
    actual_tree = git("rev-parse", f"HEAD:{stim['directory']}")
    require(
        actual_tree == stim["gitTreeSha"],
        f"Stimulus tree mismatch: expected {stim['gitTreeSha']}, got {actual_tree}",
    )

    required_docs = lock.get("requiredNormativeDocuments", [])
    require(required_docs, "Evidence lock must name required normative documents")
    for rel in required_docs:
        require((ROOT / rel).is_file(), f"Missing required normative document: {rel}")

    # Explicit predecessor-authority boundary checks. These are narrow on purpose:
    # future Szondi3 implementation code is allowed; legacy authority artifacts are not.
    forbidden = [
        ROOT / "project-state.json",
        ROOT / "sources" / "canonical-text",
    ]
    for path in forbidden:
        require(not path.exists(), f"Forbidden predecessor authority artifact present: {path.relative_to(ROOT)}")

    cards_csv = list(ROOT.rglob("cards.csv"))
    require(
        not cards_csv,
        "Legacy cards.csv must not enter Szondi3 runtime/evidence paths: "
        + ", ".join(str(p.relative_to(ROOT)) for p in cards_csv),
    )

    print("SZONDI3 FOUNDATION VERIFICATION: PASS")
    print(f"  source catalog entries: {len(sources)}")
    print(f"  admitted DOCX verified by SHA-256: {len(docx_paths)}")
    print(f"  admitted PDF verified by Git blob: {len(pdf_blobs)}")
    print(f"  stimulus WebP count: {len(actual_stimuli)}")
    print(f"  stimulus tree: {actual_tree}")
    print(f"  required normative documents: {len(required_docs)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"SZONDI3 FOUNDATION VERIFICATION: FAIL\n{exc}", file=sys.stderr)
        raise SystemExit(1)
