#!/usr/bin/env python3
"""Deterministic, fail-closed canonical access for admitted Szondi3 DOCX sources.

This module is a Szondi3-native implementation derived from
`docs/CANONICAL_ACCESS_SPEC.md`. It does not consult or reproduce Szondi2
exporter behavior or old canonical addressing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import xml.etree.ElementTree as ET

SCHEMA_VERSION = 1
EXTRACTOR_VERSION = "szondi3-canonical-access/0.1.0"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
V = "urn:schemas-microsoft-com:vml"
O = "urn:schemas-microsoft-com:office:office"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def qn(ns: str, local: str) -> str:
    return f"{{{ns}}}{local}"


def split_tag(tag: str) -> tuple[str, str]:
    if tag.startswith("{") and "}" in tag:
        ns, local = tag[1:].split("}", 1)
        return ns, local
    return "", tag


class CanonicalError(RuntimeError):
    pass


@dataclass(frozen=True)
class PartInfo:
    classification: str
    stream: str | None


STRUCTURAL_EXACT = {
    "word/styles.xml",
    "word/settings.xml",
    "word/numbering.xml",
    "word/fontTable.xml",
    "word/webSettings.xml",
}

HEADER_RE = re.compile(r"^word/header\d+\.xml$")
FOOTER_RE = re.compile(r"^word/footer\d+\.xml$")
THEME_RE = re.compile(r"^word/theme/theme\d+\.xml$")


def classify_word_xml_part(name: str) -> PartInfo:
    if name == "word/document.xml":
        return PartInfo("SUPPORTED_DOCTRINAL_CANDIDATE", "BODY")
    if name == "word/footnotes.xml":
        return PartInfo("SUPPORTED_DOCTRINAL_CANDIDATE", "FOOTNOTE")
    if name == "word/endnotes.xml":
        return PartInfo("SUPPORTED_DOCTRINAL_CANDIDATE", "ENDNOTE")
    if name == "word/comments.xml":
        return PartInfo("SUPPORTED_NON_DOCTRINAL", "COMMENT")
    if HEADER_RE.match(name):
        return PartInfo("SUPPORTED_NON_DOCTRINAL", "HEADER")
    if FOOTER_RE.match(name):
        return PartInfo("SUPPORTED_NON_DOCTRINAL", "FOOTER")
    if name in STRUCTURAL_EXACT or THEME_RE.match(name):
        return PartInfo("SUPPORTED_STRUCTURAL", None)
    raise CanonicalError(f"UNSUPPORTED_POSSIBLY_MEANINGFUL OOXML part: {name}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_json(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def relationship_part_for(part: str) -> str:
    p = Path(part)
    return str(p.parent / "_rels" / (p.name + ".rels")).replace("\\", "/")


def parse_relationships(zf: zipfile.ZipFile, part: str) -> dict[str, dict[str, str]]:
    rel_name = relationship_part_for(part)
    if rel_name not in zf.namelist():
        return {}
    try:
        root = ET.fromstring(zf.read(rel_name))
    except ET.ParseError as exc:
        raise CanonicalError(f"Malformed relationships in {rel_name}: {exc}") from exc
    result: dict[str, dict[str, str]] = {}
    for rel in root:
        ns, local = split_tag(rel.tag)
        if ns != PKG_REL or local != "Relationship":
            raise CanonicalError(f"Unexpected relationship element in {rel_name}: {rel.tag}")
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        rtype = rel.attrib.get("Type")
        if not rid or target is None or not rtype:
            raise CanonicalError(f"Incomplete relationship in {rel_name}")
        result[rid] = {
            "target": target,
            "targetMode": rel.attrib.get("TargetMode", "Internal"),
            "type": rtype,
        }
    return result


PROPERTY_CONTAINERS = {
    "pPr", "rPr", "tblPr", "tblGrid", "trPr", "tcPr", "sectPr", "numPr",
    "tabs", "pBdr", "tblBorders", "tcBorders", "shd", "spacing", "ind",
    "framePr", "textDirection", "tblCellMar", "tblLook", "tblLayout", "tblW",
    "tcMar", "latentStyles", "docDefaults", "style", "styles", "settings",
    "numbering", "abstractNum", "num", "lvl", "font", "fonts", "theme",
}

TRANSPARENT_W = {
    "r", "smartTag", "sdt", "sdtContent", "customXml", "ins", "moveTo",
    "dir", "bdo", "proofErr", "permStart", "permEnd", "bookmarkEnd",
}

KNOWN_NON_TEXT_LEAF_W = {
    "lastRenderedPageBreak", "noBreakHyphen", "softHyphen", "separator",
    "continuationSeparator", "annotationRef", "pgNum", "dayShort", "monthShort",
    "yearShort", "dayLong", "monthLong", "yearLong",
}

KNOWN_FIELD_CODES = {
    "PAGE", "NUMPAGES", "SECTION", "SECTIONPAGES", "TOC", "REF", "PAGEREF",
    "HYPERLINK", "SEQ", "STYLEREF", "DATE", "TIME", "FILENAME", "AUTHOR",
    "TITLE", "SUBJECT", "KEYWORDS", "COMMENTS", "LASTSAVEDBY", "CREATEDATE",
    "SAVEDATE", "PRINTDATE", "IF", "MERGEFIELD", "SYMBOL", "EQ", "QUOTE",
    "DOCPROPERTY", "DOCVARIABLE", "AUTONUM", "AUTONUMLGL", "AUTONUMOUT",
}


@dataclass
class FieldContext:
    stack: list[dict] = field(default_factory=list)
    next_id: int = 0

    def new_id(self) -> str:
        self.next_id += 1
        return f"F{self.next_id:06d}"


class InlineParser:
    def __init__(
        self,
        relationships: dict[str, dict[str, str]],
        part: str,
        field_context: FieldContext | None = None,
    ):
        self.relationships = relationships
        self.part = part
        self.field_context = field_context or FieldContext()
        self.field_stack = self.field_context.stack
        self.segments: list[dict] = []
        self.fields: list[dict] = []
        self.field_events: list[dict] = []
        self.hyperlinks: list[dict] = []
        self.bookmarks: list[dict] = []
        self.references: list[dict] = []
        self.visuals: list[dict] = []
        self.revisions: list[dict] = []
        self.alternate_content: list[dict] = []

    def add_text(self, text: str, kind: str = "TEXT") -> None:
        if not text:
            return
        if self.field_stack and self.field_stack[-1]["state"] == "instruction":
            self.field_stack[-1]["instruction"] += text
            return
        seg = {"kind": kind, "text": text}
        if self.field_stack and self.field_stack[-1]["state"] == "result":
            seg["fieldId"] = self.field_stack[-1]["fieldId"]
            self.field_stack[-1]["result"] += text
        self.segments.append(seg)

    def parse(self, elem: ET.Element, context: str = "content") -> None:
        ns, local = split_tag(elem.tag)

        if context == "property" or local in PROPERTY_CONTAINERS or local.endswith("Pr"):
            for child in elem:
                self.parse(child, "property")
            return

        if ns == W:
            if local == "t":
                self.add_text(elem.text or "")
                return
            if local == "delText":
                self.revisions.append({"kind": "DELETED_TEXT", "text": elem.text or ""})
                return
            if local == "instrText":
                text = elem.text or ""
                if not self.field_stack:
                    raise CanonicalError(f"Field instruction outside field in {self.part}")
                self.field_stack[-1]["instruction"] += text
                return
            if local == "tab":
                self.segments.append({"kind": "TAB"})
                return
            if local in {"br", "cr"}:
                kind = "CARRIAGE_RETURN" if local == "cr" else "BREAK"
                rec = {"kind": kind}
                if local == "br":
                    btype = elem.attrib.get(qn(W, "type"))
                    if btype:
                        rec["breakType"] = btype
                self.segments.append(rec)
                return
            if local == "sym":
                rec = {"kind": "SYMBOL"}
                for attr, key in ((qn(W, "font"), "font"), (qn(W, "char"), "char")):
                    if elem.attrib.get(attr):
                        rec[key] = elem.attrib[attr]
                self.segments.append(rec)
                return
            if local == "fldChar":
                ftype = elem.attrib.get(qn(W, "fldCharType"))
                if ftype == "begin":
                    field_id = self.field_context.new_id()
                    self.field_stack.append({
                        "fieldId": field_id,
                        "state": "instruction",
                        "instruction": "",
                        "result": "",
                    })
                    self.field_events.append({"fieldId": field_id, "event": "BEGIN"})
                elif ftype == "separate":
                    if not self.field_stack:
                        raise CanonicalError(f"Field separator without begin in {self.part}")
                    self.field_stack[-1]["state"] = "result"
                    self.field_events.append({
                        "fieldId": self.field_stack[-1]["fieldId"],
                        "event": "SEPARATE",
                    })
                elif ftype == "end":
                    if not self.field_stack:
                        raise CanonicalError(f"Field end without begin in {self.part}")
                    completed = self.field_stack.pop()
                    self.field_events.append({"fieldId": completed["fieldId"], "event": "END"})
                    instruction = completed["instruction"].strip()
                    code = instruction.split()[0].upper() if instruction else ""
                    if code and code not in KNOWN_FIELD_CODES:
                        raise CanonicalError(
                            f"Unsupported possibly meaningful field instruction {code!r} in {self.part}"
                        )
                    self.fields.append({
                        "fieldId": completed["fieldId"],
                        "instruction": instruction,
                        "fieldCode": code or None,
                        "displayedResult": completed["result"],
                    })
                else:
                    raise CanonicalError(f"Unknown fldCharType {ftype!r} in {self.part}")
                return
            if local == "fldSimple":
                instruction = (elem.attrib.get(qn(W, "instr")) or "").strip()
                code = instruction.split()[0].upper() if instruction else ""
                if code and code not in KNOWN_FIELD_CODES:
                    raise CanonicalError(
                        f"Unsupported possibly meaningful simple field {code!r} in {self.part}"
                    )
                nested = InlineParser(self.relationships, self.part, self.field_context)
                for child in elem:
                    nested.parse(child)
                self.segments.extend(nested.segments)
                self.fields.append({
                    "fieldId": self.field_context.new_id(),
                    "instruction": instruction,
                    "fieldCode": code or None,
                    "displayedResult": segments_to_text(nested.segments),
                    "simpleField": True,
                })
                self._merge_nested(nested, except_fields=True)
                return
            if local == "hyperlink":
                rid = elem.attrib.get(qn(R, "id"))
                anchor = elem.attrib.get(qn(W, "anchor"))
                nested = InlineParser(self.relationships, self.part, self.field_context)
                for child in elem:
                    nested.parse(child)
                text = segments_to_text(nested.segments)
                rec: dict[str, object] = {"text": text}
                if rid:
                    if rid not in self.relationships:
                        raise CanonicalError(f"Unresolved hyperlink relationship {rid} in {self.part}")
                    rec["relationshipId"] = rid
                    rec["relationship"] = self.relationships[rid]
                if anchor:
                    rec["anchor"] = anchor
                self.hyperlinks.append(rec)
                self.segments.extend(nested.segments)
                self._merge_nested(nested)
                return
            if local == "bookmarkStart":
                self.bookmarks.append({
                    "id": elem.attrib.get(qn(W, "id")),
                    "name": elem.attrib.get(qn(W, "name")),
                })
                return
            if local in {"footnoteReference", "endnoteReference", "commentReference"}:
                ident = elem.attrib.get(qn(W, "id"))
                if ident is None:
                    raise CanonicalError(f"Reference without source id in {self.part}")
                self.references.append({"kind": local, "id": ident})
                return
            if local in {"drawing", "pict", "object"}:
                self._parse_visual(elem, local)
                return
            if local == "txbxContent":
                blocks = parse_block_children(
                    list(elem), self.relationships, self.part, "/textbox"
                )
                text = blocks_to_text(blocks)
                self.visuals.append({
                    "kind": "TEXT_BOX",
                    "visualArbitrationRequired": True,
                    "text": text,
                    "blocks": blocks,
                })
                if text:
                    self.add_text(text, "TEXT_BOX_TEXT")
                return
            if local == "AlternateContent":
                self._parse_alternate(elem)
                return
            if local == "del":
                text = "".join((c.text or "") for c in elem.iter() if split_tag(c.tag) == (W, "delText"))
                self.revisions.append({"kind": "DELETION", "text": text})
                return
            if local in TRANSPARENT_W:
                for child in elem:
                    self.parse(child)
                return
            if local in KNOWN_NON_TEXT_LEAF_W:
                self.segments.append({"kind": local.upper()})
                return
            if local in {"p", "tbl", "tr", "tc"}:
                raise CanonicalError(f"Block element {local} encountered in inline context in {self.part}")
            if list(elem):
                for child in elem:
                    self.parse(child)
                return
            if elem.text and elem.text.strip():
                raise CanonicalError(f"Unsupported possibly meaningful element {elem.tag} in {self.part}")
            return

        if ns == MC and local == "AlternateContent":
            self._parse_alternate(elem)
            return
        if ns == A and local == "t":
            self.add_text(elem.text or "", "DRAWING_TEXT")
            return
        if ns == M and local == "t":
            self.add_text(elem.text or "", "MATH_TEXT")
            return
        if ns in {V, O, A, WP}:
            for child in elem:
                self.parse(child)
            return
        if list(elem):
            raise CanonicalError(f"Unsupported possibly meaningful namespace element {elem.tag} in {self.part}")
        if elem.text and elem.text.strip():
            raise CanonicalError(f"Unsupported possibly meaningful text element {elem.tag} in {self.part}")

    def _merge_nested(self, nested: "InlineParser", except_fields: bool = False) -> None:
        if not except_fields:
            self.fields.extend(nested.fields)
        self.field_events.extend(nested.field_events)
        self.hyperlinks.extend(nested.hyperlinks)
        self.bookmarks.extend(nested.bookmarks)
        self.references.extend(nested.references)
        self.visuals.extend(nested.visuals)
        self.revisions.extend(nested.revisions)
        self.alternate_content.extend(nested.alternate_content)

    def _parse_visual(self, elem: ET.Element, kind: str) -> None:
        rec: dict[str, object] = {
            "kind": {"drawing": "DRAWING", "pict": "LEGACY_PICTURE", "object": "EMBEDDED_OBJECT"}[kind],
            "visualArbitrationRequired": True,
        }
        rels: list[dict] = []
        alts: list[dict] = []
        texts: list[str] = []
        text_boxes: list[dict] = []
        for node in elem.iter():
            ns, local = split_tag(node.tag)
            for attr_name, attr_value in node.attrib.items():
                ans, alocal = split_tag(attr_name)
                if ans == R and alocal in {"id", "embed", "link"}:
                    rrec: dict[str, object] = {"relationshipId": attr_value, "attribute": alocal}
                    if attr_value in self.relationships:
                        rrec["relationship"] = self.relationships[attr_value]
                    rels.append(rrec)
            if ns == WP and local == "docPr":
                alt = {k: v for k, v in {
                    "name": node.attrib.get("name"),
                    "title": node.attrib.get("title"),
                    "description": node.attrib.get("descr"),
                }.items() if v}
                if alt:
                    alts.append(alt)
            if ns == A and local == "t" and node.text:
                texts.append(node.text)
            if ns == W and local == "txbxContent":
                blocks = parse_block_children(
                    list(node), self.relationships, self.part, "/visual/textbox"
                )
                text_boxes.append({"blocks": blocks, "text": blocks_to_text(blocks)})
        if rels:
            seen = set()
            unique = []
            for item in rels:
                key = stable_json(item)
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            rec["relationships"] = unique
        if alts:
            rec["alternativeText"] = alts
        if texts:
            rec["graphicText"] = texts
        if text_boxes:
            rec["textBoxes"] = text_boxes
        self.visuals.append(rec)

    def _parse_alternate(self, elem: ET.Element) -> None:
        variants: list[dict] = []
        for child in elem:
            ns, local = split_tag(child.tag)
            if ns != MC or local not in {"Choice", "Fallback"}:
                raise CanonicalError(f"Unsupported AlternateContent branch {child.tag} in {self.part}")
            nested = InlineParser(self.relationships, self.part)
            for grandchild in child:
                nested.parse(grandchild)
            variants.append({
                "branch": local,
                "requires": child.attrib.get("Requires"),
                "text": segments_to_text(nested.segments),
                "segments": nested.segments,
                "visuals": nested.visuals,
            })
        if not variants:
            raise CanonicalError(f"Empty AlternateContent in {self.part}")
        self.alternate_content.append({
            "visualArbitrationRequired": True,
            "variants": variants,
        })

def segments_to_text(segments: list[dict]) -> str:
    pieces: list[str] = []
    for seg in segments:
        kind = seg["kind"]
        if kind in {"TEXT", "DRAWING_TEXT", "MATH_TEXT", "TEXT_BOX_TEXT"}:
            pieces.append(seg.get("text", ""))
        elif kind == "TAB":
            pieces.append("\t")
        elif kind in {"BREAK", "CARRIAGE_RETURN"}:
            pieces.append("\n")
        elif kind == "SYMBOL":
            char = seg.get("char")
            pieces.append(f"[SYM:{char}]" if char else "[SYM]")
    return "".join(pieces)


def parse_paragraph(
    elem: ET.Element,
    relationships: dict[str, dict[str, str]],
    part: str,
    path: str,
    field_context: FieldContext,
) -> dict:
    parser = InlineParser(relationships, part, field_context)
    for child in elem:
        ns, local = split_tag(child.tag)
        if ns == W and local == "pPr":
            parser.parse(child, "property")
        else:
            parser.parse(child)
    rec: dict[str, object] = {
        "kind": "PARAGRAPH",
        "path": path,
        "text": segments_to_text(parser.segments),
        "segments": parser.segments,
    }
    for name, value in (
        ("fields", parser.fields),
        ("fieldEvents", parser.field_events),
        ("hyperlinks", parser.hyperlinks),
        ("bookmarks", parser.bookmarks),
        ("references", parser.references),
        ("visuals", parser.visuals),
        ("revisions", parser.revisions),
        ("alternateContent", parser.alternate_content),
    ):
        if value:
            rec[name] = value
    return rec

def cell_merge_metadata(tc: ET.Element) -> dict:
    result: dict[str, object] = {}
    tcpr = tc.find(qn(W, "tcPr"))
    if tcpr is None:
        return result
    grid_span = tcpr.find(qn(W, "gridSpan"))
    if grid_span is not None:
        val = grid_span.attrib.get(qn(W, "val"))
        if val is not None:
            result["gridSpan"] = val
    vmerge = tcpr.find(qn(W, "vMerge"))
    if vmerge is not None:
        result["verticalMerge"] = vmerge.attrib.get(qn(W, "val"), "continue")
    return result


def structural_metadata(elem: ET.Element) -> dict:
    """Preserve a reviewed structural OOXML subtree without converting it to prose."""
    if elem.text and elem.text.strip():
        raise CanonicalError(f"Unexpected text in structural element {elem.tag}: {elem.text!r}")
    children = [structural_metadata(child) for child in elem]
    rec: dict[str, object] = {
        "tag": elem.tag,
        "attributes": dict(sorted(elem.attrib.items())),
    }
    if children:
        rec["children"] = children
    return rec


def parse_table(
    elem: ET.Element,
    relationships: dict[str, dict[str, str]],
    part: str,
    path: str,
    field_context: FieldContext,
) -> dict:
    rows: list[dict] = []
    row_index = 0
    for child in elem:
        ns, local = split_tag(child.tag)
        if ns == W and local in {"tblPr", "tblGrid"}:
            continue
        if ns != W or local != "tr":
            if local.endswith("Pr"):
                continue
            raise CanonicalError(f"Unsupported table child {child.tag} in {part} at {path}")
        row_index += 1
        cells: list[dict] = []
        row_structural: list[dict] = []
        cell_index = 0
        for rchild in child:
            rns, rlocal = split_tag(rchild.tag)
            if rns == W and rlocal in {"trPr", "tblPrEx"}:
                row_structural.append(structural_metadata(rchild))
                continue
            if rns != W or rlocal != "tc":
                raise CanonicalError(f"Unsupported row child {rchild.tag} in {part} at {path}")
            cell_index += 1
            cpath = f"{path}/row[{row_index}]/cell[{cell_index}]"
            blocks = parse_block_children(
                list(rchild), relationships, part, cpath, field_context
            )
            cell = {"column": cell_index, "path": cpath, "blocks": blocks}
            cell.update(cell_merge_metadata(rchild))
            cells.append(cell)
        row = {"row": row_index, "path": f"{path}/row[{row_index}]", "cells": cells}
        if row_structural:
            row["structuralProperties"] = row_structural
        rows.append(row)
    return {"kind": "TABLE", "path": path, "rows": rows}


def parse_block_children(
    children: list[ET.Element],
    relationships: dict[str, dict[str, str]],
    part: str,
    path: str,
    field_context: FieldContext | None = None,
) -> list[dict]:
    field_context = field_context or FieldContext()
    blocks: list[dict] = []
    p_idx = 0
    t_idx = 0
    for child in children:
        ns, local = split_tag(child.tag)
        if ns == W and local in {"tcPr", "trPr", "tblPr", "sectPr"}:
            continue
        if ns == W and local == "p":
            p_idx += 1
            blocks.append(parse_paragraph(
                child, relationships, part, f"{path}/p[{p_idx}]", field_context
            ))
            continue
        if ns == W and local == "tbl":
            t_idx += 1
            blocks.append(parse_table(
                child, relationships, part, f"{path}/table[{t_idx}]", field_context
            ))
            continue
        if ns == MC and local == "AlternateContent":
            parser = InlineParser(relationships, part, field_context)
            parser.parse(child)
            blocks.append({
                "kind": "ALTERNATE_CONTENT",
                "path": f"{path}/alternate[{len(blocks)+1}]",
                "alternateContent": parser.alternate_content,
            })
            continue
        if local.endswith("Pr"):
            continue
        if child.text and child.text.strip():
            raise CanonicalError(f"Unsupported possibly meaningful block {child.tag} in {part} at {path}")
        if list(child):
            raise CanonicalError(f"Unsupported block wrapper {child.tag} in {part} at {path}")
    return blocks


def require_closed(field_context: FieldContext, location: str) -> None:
    if field_context.stack:
        raise CanonicalError(
            f"Unclosed field(s) {[item['fieldId'] for item in field_context.stack]} at end of {location}"
        )

def blocks_to_text(blocks: list[dict]) -> str:
    pieces: list[str] = []
    for block in blocks:
        if block["kind"] == "PARAGRAPH":
            pieces.append(block.get("text", ""))
        elif block["kind"] == "TABLE":
            for row in block["rows"]:
                pieces.append("\t".join(blocks_to_text(cell["blocks"]) for cell in row["cells"]))
    return "\n".join(pieces)


def collect_references(blocks: list[dict]) -> list[dict]:
    refs: list[dict] = []
    for block in blocks:
        if block["kind"] == "PARAGRAPH":
            refs.extend(block.get("references", []))
        elif block["kind"] == "TABLE":
            for row in block["rows"]:
                for cell in row["cells"]:
                    refs.extend(collect_references(cell["blocks"]))
    return refs


def parse_xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError as exc:
        raise CanonicalError(f"Missing required OOXML part: {name}") from exc
    except ET.ParseError as exc:
        raise CanonicalError(f"Malformed XML in {name}: {exc}") from exc


def element_tag_inventory(root: ET.Element) -> list[str]:
    return sorted({elem.tag for elem in root.iter()})


def record_base(source: dict, source_sha: str, stream: str, unit_id_value: str, kind: str, path: str) -> dict:
    return {
        "canonicalSchemaVersion": SCHEMA_VERSION,
        "extractorVersion": EXTRACTOR_VERSION,
        "sourceId": source["sourceId"],
        "layer": source["layer"],
        "inputSourceFilename": source["docxPath"],
        "inputSourceSha256": source_sha,
        "stream": stream,
        "unitId": unit_id_value,
        "kind": kind,
        "path": path,
    }


def unit_id(n: int) -> str:
    return f"U{n:06d}"


def parse_body(
    zf: zipfile.ZipFile, source: dict, source_sha: str, counters: Counter
) -> tuple[list[dict], list[dict]]:
    part = "word/document.xml"
    root = parse_xml(zf, part)
    relationships = parse_relationships(zf, part)
    body = root.find(qn(W, "body"))
    if body is None:
        raise CanonicalError("word/document.xml has no w:body")
    field_context = FieldContext()
    records: list[dict] = []
    top_index = 0
    for child in body:
        ns, local = split_tag(child.tag)
        if ns == W and local == "sectPr":
            continue
        top_index += 1
        path = f"/body/block[{top_index}]"
        if ns == W and local == "p":
            payload = parse_paragraph(child, relationships, part, path, field_context)
        elif ns == W and local == "tbl":
            payload = parse_table(child, relationships, part, path, field_context)
        elif ns == MC and local == "AlternateContent":
            parser = InlineParser(relationships, part, field_context)
            parser.parse(child)
            payload = {
                "kind": "ALTERNATE_CONTENT",
                "path": path,
                "alternateContent": parser.alternate_content,
            }
        else:
            raise CanonicalError(f"Unsupported possibly meaningful body block {child.tag}")
        counters["BODY"] += 1
        base = record_base(
            source, source_sha, "BODY", unit_id(counters["BODY"]), payload["kind"], path
        )
        base.update({k: v for k, v in payload.items() if k not in {"kind", "path"}})
        records.append(base)
    require_closed(field_context, part)
    return records, collect_references(records)


def parse_notes(
    zf: zipfile.ZipFile,
    source: dict,
    source_sha: str,
    part: str,
    stream: str,
    counters: Counter,
) -> tuple[list[dict], set[str], list[str]]:
    root = parse_xml(zf, part)
    relationships = parse_relationships(zf, part)
    child_name = "footnote" if stream == "FOOTNOTE" else "endnote"
    records: list[dict] = []
    ids: set[str] = set()
    special_ids: list[str] = []
    for note in root:
        ns, local = split_tag(note.tag)
        if ns != W or local != child_name:
            if local.endswith("Pr"):
                continue
            raise CanonicalError(f"Unexpected {stream} child {note.tag} in {part}")
        ident = note.attrib.get(qn(W, "id"))
        if ident is None or ident in ids:
            raise CanonicalError(f"Invalid or duplicate {stream} id {ident}")
        ids.add(ident)
        note_type = note.attrib.get(qn(W, "type"))
        if note_type in {"separator", "continuationSeparator", "continuationNotice"} or ident in {"-1", "0"}:
            special_ids.append(ident)
        field_context = FieldContext()
        blocks = parse_block_children(
            list(note), relationships, part, f"/{child_name}[{ident}]", field_context
        )
        require_closed(field_context, f"{stream} {ident}")
        counters[stream] += 1
        base = record_base(
            source, source_sha, stream, unit_id(counters[stream]), stream, f"/{child_name}[{ident}]"
        )
        base.update({
            "sourceNativeId": ident,
            "noteType": note_type,
            "blocks": blocks,
            "text": blocks_to_text(blocks),
        })
        records.append(base)
    return records, ids, special_ids


def parse_story_part(
    zf: zipfile.ZipFile,
    source: dict,
    source_sha: str,
    part: str,
    stream: str,
    counters: Counter,
) -> list[dict]:
    root = parse_xml(zf, part)
    relationships = parse_relationships(zf, part)
    field_context = FieldContext()
    blocks = parse_block_children(
        list(root), relationships, part, f"/{stream.lower()}[{part}]", field_context
    )
    require_closed(field_context, part)
    counters[stream] += 1
    rec = record_base(
        source,
        source_sha,
        stream,
        unit_id(counters[stream]),
        "STORY_PART",
        f"/{stream.lower()}[{part}]",
    )
    rec.update({"storyPart": part, "blocks": blocks, "text": blocks_to_text(blocks)})
    return [rec]


def parse_comments(
    zf: zipfile.ZipFile, source: dict, source_sha: str, part: str, counters: Counter
) -> list[dict]:
    root = parse_xml(zf, part)
    relationships = parse_relationships(zf, part)
    records: list[dict] = []
    for comment in root:
        ns, local = split_tag(comment.tag)
        if ns != W or local != "comment":
            raise CanonicalError(f"Unexpected comments child {comment.tag}")
        ident = comment.attrib.get(qn(W, "id"))
        if ident is None:
            raise CanonicalError("Comment without w:id")
        field_context = FieldContext()
        blocks = parse_block_children(
            list(comment), relationships, part, f"/comment[{ident}]", field_context
        )
        require_closed(field_context, f"comment {ident}")
        counters["COMMENT"] += 1
        rec = record_base(
            source,
            source_sha,
            "COMMENT",
            unit_id(counters["COMMENT"]),
            "COMMENT",
            f"/comment[{ident}]",
        )
        rec.update({
            "sourceNativeId": ident,
            "author": comment.attrib.get(qn(W, "author")),
            "initials": comment.attrib.get(qn(W, "initials")),
            "blocks": blocks,
            "text": blocks_to_text(blocks),
        })
        records.append(rec)
    return records

def validate_references(body_refs: list[dict], footnote_ids: set[str], endnote_ids: set[str], comment_ids: set[str]) -> None:
    for ref in body_refs:
        kind = ref["kind"]
        ident = ref["id"]
        if kind == "footnoteReference" and ident not in footnote_ids:
            raise CanonicalError(f"Unresolved footnote reference id {ident}")
        if kind == "endnoteReference" and ident not in endnote_ids:
            raise CanonicalError(f"Unresolved endnote reference id {ident}")
        if kind == "commentReference" and ident not in comment_ids:
            raise CanonicalError(f"Unresolved comment reference id {ident}")


def extract_docx_bytes(data: bytes, source: dict, expected_sha: str | None = None) -> tuple[list[dict], dict]:
    source_sha = sha256_bytes(data)
    if expected_sha and source_sha.lower() != expected_sha.lower():
        raise CanonicalError(
            f"DOCX SHA-256 mismatch for {source['sourceId']}: expected {expected_sha}, got {source_sha}"
        )
    import io
    with zipfile.ZipFile(io.BytesIO(data), "r") as docx:
        names = sorted(docx.namelist())
        word_xml = [n for n in names if n.startswith("word/") and n.endswith(".xml")]
        if "word/document.xml" not in word_xml:
            raise CanonicalError("Missing word/document.xml")
        part_infos: dict[str, PartInfo] = {}
        tag_inventory: dict[str, list[str]] = {}
        for name in word_xml:
            info = classify_word_xml_part(name)
            part_infos[name] = info
            root = parse_xml(docx, name)
            tag_inventory[name] = element_tag_inventory(root)

        counters: Counter = Counter()
        records, body_refs = parse_body(docx, source, source_sha, counters)
        footnote_ids: set[str] = set()
        endnote_ids: set[str] = set()
        comment_ids: set[str] = set()
        special_notes: dict[str, list[str]] = {}

        for name in sorted(word_xml):
            if name == "word/document.xml":
                continue
            info = part_infos[name]
            if info.classification == "SUPPORTED_STRUCTURAL":
                continue
            if info.stream == "FOOTNOTE":
                recs, ids, special = parse_notes(docx, source, source_sha, name, "FOOTNOTE", counters)
                records.extend(recs)
                footnote_ids |= ids
                special_notes["FOOTNOTE"] = special
            elif info.stream == "ENDNOTE":
                recs, ids, special = parse_notes(docx, source, source_sha, name, "ENDNOTE", counters)
                records.extend(recs)
                endnote_ids |= ids
                special_notes["ENDNOTE"] = special
            elif info.stream in {"HEADER", "FOOTER"}:
                records.extend(parse_story_part(docx, source, source_sha, name, info.stream, counters))
            elif info.stream == "COMMENT":
                recs = parse_comments(docx, source, source_sha, name, counters)
                records.extend(recs)
                comment_ids |= {str(r["sourceNativeId"]) for r in recs}
            else:
                raise CanonicalError(f"Unimplemented supported part classification for {name}: {info}")

        validate_references(body_refs, footnote_ids, endnote_ids, comment_ids)

        seen: dict[str, set[str]] = defaultdict(set)
        expected_counter: Counter = Counter()
        for rec in records:
            stream = rec["stream"]
            uid = rec["unitId"]
            if uid in seen[stream]:
                raise CanonicalError(f"Duplicate unit id {stream}:{uid}")
            seen[stream].add(uid)
            expected_counter[stream] += 1
            if uid != unit_id(expected_counter[stream]):
                raise CanonicalError(f"Non-deterministic unit order in {stream}: {uid}")

        inventory_parts = []
        record_counts = Counter(r["stream"] for r in records)
        for name in word_xml:
            info = part_infos[name]
            inventory_parts.append({
                "part": name,
                "classification": info.classification,
                "stream": info.stream,
                "elementTags": tag_inventory[name],
            })
        inventory = {
            "canonicalSchemaVersion": SCHEMA_VERSION,
            "extractorVersion": EXTRACTOR_VERSION,
            "sourceId": source["sourceId"],
            "layer": source["layer"],
            "inputSourceFilename": source["docxPath"],
            "inputSourceSha256": source_sha,
            "packagePartCount": len(names),
            "wordXmlPartCount": len(word_xml),
            "parts": inventory_parts,
            "recordCountsByStream": dict(sorted(record_counts.items())),
            "specialNoteIds": special_notes,
        }
        return records, inventory

def write_source_outputs(output_dir: Path, source_id: str, records: list[dict], inventory: dict) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl = output_dir / f"{source_id}.jsonl"
    inv = output_dir / f"{source_id}.inventory.json"
    jsonl_text = "".join(stable_json(record) + "\n" for record in records)
    inv_text = json.dumps(inventory, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    jsonl.write_text(jsonl_text, encoding="utf-8", newline="\n")
    inv.write_text(inv_text, encoding="utf-8", newline="\n")
    return {
        jsonl.name: sha256_file(jsonl),
        inv.name: sha256_file(inv),
    }


def load_catalog(repo: Path, catalog_rel: str) -> list[dict]:
    catalog_path = repo / catalog_rel
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CanonicalError(f"Cannot read source catalog {catalog_path}: {exc}") from exc
    if catalog.get("schemaVersion") != 1:
        raise CanonicalError("Unsupported source catalog schema")
    sources = catalog.get("sources")
    if not isinstance(sources, list) or not sources:
        raise CanonicalError("source_catalog.sources must be a non-empty list")
    ids = [s.get("sourceId") for s in sources]
    if any(not isinstance(i, str) or not i for i in ids) or len(ids) != len(set(ids)):
        raise CanonicalError("Invalid or duplicate sourceId in source catalog")
    return sources


def run(repo: Path, output_dir: Path, source_ids: set[str] | None = None, catalog_rel: str = "config/source_catalog.json") -> dict:
    sources = load_catalog(repo, catalog_rel)
    selected = [s for s in sources if source_ids is None or s["sourceId"] in source_ids]
    if source_ids is not None:
        missing = sorted(source_ids - {s["sourceId"] for s in selected})
        if missing:
            raise CanonicalError(f"Unknown sourceId requested: {missing}")
    hashes: dict[str, dict[str, str]] = {}
    for source in selected:
        path = repo / source["docxPath"]
        if not path.is_file():
            raise CanonicalError(f"Missing admitted DOCX: {source['docxPath']}")
        data = path.read_bytes()
        records, inventory = extract_docx_bytes(data, source, source.get("docxSha256"))
        hashes[source["sourceId"]] = write_source_outputs(output_dir, source["sourceId"], records, inventory)
    manifest = {
        "canonicalSchemaVersion": SCHEMA_VERSION,
        "extractorVersion": EXTRACTOR_VERSION,
        "sources": hashes,
    }
    manifest_path = output_dir / "canonical-hashes.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--catalog", default="config/source_catalog.json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--source-id", action="append", dest="source_ids")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    output = Path(args.output_dir)
    if not output.is_absolute():
        output = repo / output
    run(repo, output, set(args.source_ids) if args.source_ids else None, args.catalog)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CanonicalError, OSError, zipfile.BadZipFile) as exc:
        print(f"CANONICAL ACCESS ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
