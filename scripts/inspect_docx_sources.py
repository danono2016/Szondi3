#!/usr/bin/env python3
"""Read-only structural inspection of admitted DOCX sources.

This is a Szondi3-native P0 tool. It does not extract canonical doctrine and does
not reuse predecessor exporter code. It verifies admitted DOCX identities and
reports OOXML structures that a later canonical extractor must handle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

INTERESTING = {
    f"{{{W_NS}}}p": "paragraph",
    f"{{{W_NS}}}tbl": "table",
    f"{{{W_NS}}}tr": "tableRow",
    f"{{{W_NS}}}tc": "tableCell",
    f"{{{W_NS}}}t": "text",
    f"{{{W_NS}}}instrText": "fieldInstructionText",
    f"{{{W_NS}}}delText": "deletedText",
    f"{{{W_NS}}}tab": "tab",
    f"{{{W_NS}}}br": "break",
    f"{{{W_NS}}}cr": "carriageReturn",
    f"{{{W_NS}}}sym": "symbol",
    f"{{{W_NS}}}fldChar": "fieldChar",
    f"{{{W_NS}}}footnoteReference": "footnoteReference",
    f"{{{W_NS}}}endnoteReference": "endnoteReference",
    f"{{{W_NS}}}commentReference": "commentReference",
    f"{{{W_NS}}}hyperlink": "hyperlink",
    f"{{{W_NS}}}bookmarkStart": "bookmarkStart",
    f"{{{W_NS}}}drawing": "drawing",
    f"{{{W_NS}}}pict": "legacyPicture",
    f"{{{W_NS}}}object": "embeddedObject",
    f"{{{W_NS}}}altChunk": "alternateChunk",
    f"{{{M_NS}}}oMath": "math",
    f"{{{M_NS}}}oMathPara": "mathParagraph",
    f"{{{M_NS}}}t": "mathText",
    f"{{{A_NS}}}t": "drawingText",
}

TEXT_TAGS = {
    f"{{{W_NS}}}t",
    f"{{{W_NS}}}instrText",
    f"{{{W_NS}}}delText",
    f"{{{M_NS}}}t",
    f"{{{A_NS}}}t",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_xml(data: bytes) -> dict:
    root = ET.fromstring(data)
    counts = Counter()
    all_tags = Counter()
    text_chars = 0
    for elem in root.iter():
        all_tags[elem.tag] += 1
        label = INTERESTING.get(elem.tag)
        if label:
            counts[label] += 1
        if elem.tag in TEXT_TAGS and elem.text:
            text_chars += len(elem.text)
    return {
        "interestingCounts": dict(sorted(counts.items())),
        "textCharacterCount": text_chars,
        "elementTagCount": len(all_tags),
    }


def is_word_xml(name: str) -> bool:
    return name.startswith("word/") and name.endswith(".xml")


def inspect_source(repo: Path, entry: dict) -> dict:
    path = repo / entry["docxPath"]
    if not path.is_file():
        raise RuntimeError(f"Missing admitted DOCX: {entry['docxPath']}")
    actual_hash = sha256(path)
    expected_hash = entry["docxSha256"].lower()
    if actual_hash != expected_hash:
        raise RuntimeError(
            f"SHA-256 mismatch for {entry['sourceId']}: expected {expected_hash}, got {actual_hash}"
        )

    report = {
        "sourceId": entry["sourceId"],
        "layer": entry["layer"],
        "docxPath": entry["docxPath"],
        "sha256": actual_hash,
        "packageParts": [],
        "wordXmlParts": [],
    }

    with zipfile.ZipFile(path, "r") as zf:
        names = sorted(zf.namelist())
        report["packagePartCount"] = len(names)
        report["packageParts"] = names
        for name in names:
            if not is_word_xml(name):
                continue
            try:
                info = inspect_xml(zf.read(name))
            except ET.ParseError as exc:
                raise RuntimeError(f"Malformed XML in {entry['sourceId']}:{name}: {exc}") from exc
            if info["textCharacterCount"] > 0 or any(info["interestingCounts"].values()):
                report["wordXmlParts"].append({"part": name, **info})

    main_document = next((p for p in report["wordXmlParts"] if p["part"] == "word/document.xml"), None)
    if main_document is None:
        raise RuntimeError(f"No parseable word/document.xml in {entry['sourceId']}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="repository root")
    parser.add_argument("--catalog", default="config/source_catalog.json")
    parser.add_argument("--output", default="-", help="JSON output path, or - for stdout")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    catalog_path = repo / args.catalog
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    sources = catalog.get("sources", [])
    if len(sources) != 10:
        raise RuntimeError(f"Expected exactly 10 admitted sources, got {len(sources)}")
    ids = [s["sourceId"] for s in sources]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate sourceId in source catalog")

    result = {
        "inspectionSchemaVersion": 1,
        "purpose": "P0 read-only OOXML structural inventory; not canonical extraction",
        "sourceCount": len(sources),
        "sources": [inspect_source(repo, entry) for entry in sources],
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output == "-":
        sys.stdout.write(rendered)
    else:
        output = repo / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
