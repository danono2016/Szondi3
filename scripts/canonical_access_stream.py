#!/usr/bin/env python3
"""Stream-aware canonical access entrypoint.

This module extends the canonical-access core with field state that is preserved
across paragraph/table block boundaries within one OOXML story stream. Word
fields such as TOC can legitimately begin in one paragraph and end in a later
paragraph; treating paragraph boundaries as field boundaries would lose source
structure.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import sys
import zipfile

import canonical_access as core


@dataclass
class FieldContext:
    stack: list[dict] = field(default_factory=list)
    next_id: int = 0

    def new_id(self) -> str:
        self.next_id += 1
        return f"F{self.next_id:06d}"


class InlineParser(core.InlineParser):
    def __init__(self, relationships: dict[str, dict[str, str]], part: str, field_context: FieldContext | None = None):
        super().__init__(relationships, part)
        self.field_context = field_context or FieldContext()
        self.field_stack = self.field_context.stack
        self.field_events: list[dict] = []

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

    def parse(self, elem, context: str = "content") -> None:
        ns, local = core.split_tag(elem.tag)
        if ns == core.W and local == "fldChar":
            ftype = elem.attrib.get(core.qn(core.W, "fldCharType"))
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
                    raise core.CanonicalError(f"Field separator without begin in {self.part}")
                self.field_stack[-1]["state"] = "result"
                self.field_events.append({"fieldId": self.field_stack[-1]["fieldId"], "event": "SEPARATE"})
            elif ftype == "end":
                if not self.field_stack:
                    raise core.CanonicalError(f"Field end without begin in {self.part}")
                completed = self.field_stack.pop()
                self.field_events.append({"fieldId": completed["fieldId"], "event": "END"})
                instruction = completed["instruction"].strip()
                code = instruction.split()[0].upper() if instruction else ""
                if code and code not in core.KNOWN_FIELD_CODES:
                    raise core.CanonicalError(
                        f"Unsupported possibly meaningful field instruction {code!r} in {self.part}"
                    )
                self.fields.append({
                    "fieldId": completed["fieldId"],
                    "instruction": instruction,
                    "fieldCode": code or None,
                    "displayedResult": completed["result"],
                })
            else:
                raise core.CanonicalError(f"Unknown fldCharType {ftype!r} in {self.part}")
            return
        if ns == core.W and local == "fldSimple":
            instruction = (elem.attrib.get(core.qn(core.W, "instr")) or "").strip()
            code = instruction.split()[0].upper() if instruction else ""
            if code and code not in core.KNOWN_FIELD_CODES:
                raise core.CanonicalError(
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
                "displayedResult": core.segments_to_text(nested.segments),
                "simpleField": True,
            })
            self._merge_nested_stream(nested, except_fields=True)
            return
        if ns == core.W and local == "hyperlink":
            rid = elem.attrib.get(core.qn(core.R, "id"))
            anchor = elem.attrib.get(core.qn(core.W, "anchor"))
            nested = InlineParser(self.relationships, self.part, self.field_context)
            for child in elem:
                nested.parse(child)
            text = core.segments_to_text(nested.segments)
            rec: dict[str, object] = {"text": text}
            if rid:
                if rid not in self.relationships:
                    raise core.CanonicalError(f"Unresolved hyperlink relationship {rid} in {self.part}")
                rec["relationshipId"] = rid
                rec["relationship"] = self.relationships[rid]
            if anchor:
                rec["anchor"] = anchor
            self.hyperlinks.append(rec)
            self.segments.extend(nested.segments)
            self._merge_nested_stream(nested)
            return
        super().parse(elem, context)

    def _merge_nested_stream(self, nested: "InlineParser", except_fields: bool = False) -> None:
        if not except_fields:
            self.fields.extend(nested.fields)
        self.field_events.extend(nested.field_events)
        self.hyperlinks.extend(nested.hyperlinks)
        self.bookmarks.extend(nested.bookmarks)
        self.references.extend(nested.references)
        self.visuals.extend(nested.visuals)
        self.revisions.extend(nested.revisions)
        self.alternate_content.extend(nested.alternate_content)


def parse_paragraph(elem, relationships, part: str, path: str, field_context: FieldContext) -> dict:
    parser = InlineParser(relationships, part, field_context)
    for child in elem:
        ns, local = core.split_tag(child.tag)
        if ns == core.W and local == "pPr":
            parser.parse(child, "property")
        else:
            parser.parse(child)
    rec: dict[str, object] = {
        "kind": "PARAGRAPH",
        "path": path,
        "text": core.segments_to_text(parser.segments),
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


def parse_table(elem, relationships, part: str, path: str, field_context: FieldContext) -> dict:
    rows: list[dict] = []
    row_index = 0
    for child in elem:
        ns, local = core.split_tag(child.tag)
        if ns == core.W and local in {"tblPr", "tblGrid"}:
            continue
        if ns != core.W or local != "tr":
            if local.endswith("Pr"):
                continue
            raise core.CanonicalError(f"Unsupported table child {child.tag} in {part} at {path}")
        row_index += 1
        cells: list[dict] = []
        cell_index = 0
        for rchild in child:
            rns, rlocal = core.split_tag(rchild.tag)
            if rns == core.W and rlocal == "trPr":
                continue
            if rns != core.W or rlocal != "tc":
                if rlocal.endswith("Pr"):
                    continue
                raise core.CanonicalError(f"Unsupported row child {rchild.tag} in {part} at {path}")
            cell_index += 1
            cpath = f"{path}/row[{row_index}]/cell[{cell_index}]"
            blocks = parse_block_children(list(rchild), relationships, part, cpath, field_context)
            cell = {"column": cell_index, "path": cpath, "blocks": blocks}
            cell.update(core.cell_merge_metadata(rchild))
            cells.append(cell)
        rows.append({"row": row_index, "path": f"{path}/row[{row_index}]", "cells": cells})
    return {"kind": "TABLE", "path": path, "rows": rows}


def parse_block_children(children, relationships, part: str, path: str, field_context: FieldContext | None = None) -> list[dict]:
    field_context = field_context or FieldContext()
    blocks: list[dict] = []
    p_idx = 0
    t_idx = 0
    for child in children:
        ns, local = core.split_tag(child.tag)
        if ns == core.W and local in {"tcPr", "trPr", "tblPr", "sectPr"}:
            continue
        if ns == core.W and local == "p":
            p_idx += 1
            blocks.append(parse_paragraph(child, relationships, part, f"{path}/p[{p_idx}]", field_context))
            continue
        if ns == core.W and local == "tbl":
            t_idx += 1
            blocks.append(parse_table(child, relationships, part, f"{path}/table[{t_idx}]", field_context))
            continue
        if ns == core.MC and local == "AlternateContent":
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
            raise core.CanonicalError(f"Unsupported possibly meaningful block {child.tag} in {part} at {path}")
        if list(child):
            raise core.CanonicalError(f"Unsupported block wrapper {child.tag} in {part} at {path}")
    return blocks


def require_closed(ctx: FieldContext, location: str) -> None:
    if ctx.stack:
        raise core.CanonicalError(
            f"Unclosed field(s) {[f['fieldId'] for f in ctx.stack]} at end of {location}"
        )


def parse_body(zf, source: dict, source_sha: str, counters: Counter):
    part = "word/document.xml"
    root = core.parse_xml(zf, part)
    relationships = core.parse_relationships(zf, part)
    body = root.find(core.qn(core.W, "body"))
    if body is None:
        raise core.CanonicalError("word/document.xml has no w:body")
    ctx = FieldContext()
    records: list[dict] = []
    top_index = 0
    for child in body:
        ns, local = core.split_tag(child.tag)
        if ns == core.W and local == "sectPr":
            continue
        top_index += 1
        path = f"/body/block[{top_index}]"
        if ns == core.W and local == "p":
            payload = parse_paragraph(child, relationships, part, path, ctx)
        elif ns == core.W and local == "tbl":
            payload = parse_table(child, relationships, part, path, ctx)
        elif ns == core.MC and local == "AlternateContent":
            parser = InlineParser(relationships, part, ctx)
            parser.parse(child)
            payload = {"kind": "ALTERNATE_CONTENT", "path": path, "alternateContent": parser.alternate_content}
        else:
            raise core.CanonicalError(f"Unsupported possibly meaningful body block {child.tag}")
        counters["BODY"] += 1
        base = core.record_base(source, source_sha, "BODY", core.unit_id(counters["BODY"]), payload["kind"], path)
        base.update({k: v for k, v in payload.items() if k not in {"kind", "path"}})
        records.append(base)
    require_closed(ctx, part)
    return records, core.collect_references(records)


def parse_notes(zf, source: dict, source_sha: str, part: str, stream: str, counters: Counter):
    root = core.parse_xml(zf, part)
    relationships = core.parse_relationships(zf, part)
    child_name = "footnote" if stream == "FOOTNOTE" else "endnote"
    records: list[dict] = []
    ids: set[str] = set()
    special_ids: list[str] = []
    for note in root:
        ns, local = core.split_tag(note.tag)
        if ns != core.W or local != child_name:
            if local.endswith("Pr"):
                continue
            raise core.CanonicalError(f"Unexpected {stream} child {note.tag} in {part}")
        ident = note.attrib.get(core.qn(core.W, "id"))
        if ident is None or ident in ids:
            raise core.CanonicalError(f"Invalid or duplicate {stream} id {ident}")
        ids.add(ident)
        note_type = note.attrib.get(core.qn(core.W, "type"))
        if note_type in {"separator", "continuationSeparator", "continuationNotice"} or ident in {"-1", "0"}:
            special_ids.append(ident)
        ctx = FieldContext()
        blocks = parse_block_children(list(note), relationships, part, f"/{child_name}[{ident}]", ctx)
        require_closed(ctx, f"{stream} {ident}")
        counters[stream] += 1
        base = core.record_base(source, source_sha, stream, core.unit_id(counters[stream]), stream, f"/{child_name}[{ident}]")
        base.update({"sourceNativeId": ident, "noteType": note_type, "blocks": blocks, "text": core.blocks_to_text(blocks)})
        records.append(base)
    return records, ids, special_ids


def parse_story_part(zf, source: dict, source_sha: str, part: str, stream: str, counters: Counter):
    root = core.parse_xml(zf, part)
    relationships = core.parse_relationships(zf, part)
    ctx = FieldContext()
    blocks = parse_block_children(list(root), relationships, part, f"/{stream.lower()}[{part}]", ctx)
    require_closed(ctx, part)
    counters[stream] += 1
    rec = core.record_base(source, source_sha, stream, core.unit_id(counters[stream]), "STORY_PART", f"/{stream.lower()}[{part}]")
    rec.update({"storyPart": part, "blocks": blocks, "text": core.blocks_to_text(blocks)})
    return [rec]


def parse_comments(zf, source: dict, source_sha: str, part: str, counters: Counter):
    root = core.parse_xml(zf, part)
    relationships = core.parse_relationships(zf, part)
    records: list[dict] = []
    for comment in root:
        ns, local = core.split_tag(comment.tag)
        if ns != core.W or local != "comment":
            raise core.CanonicalError(f"Unexpected comments child {comment.tag}")
        ident = comment.attrib.get(core.qn(core.W, "id"))
        if ident is None:
            raise core.CanonicalError("Comment without w:id")
        ctx = FieldContext()
        blocks = parse_block_children(list(comment), relationships, part, f"/comment[{ident}]", ctx)
        require_closed(ctx, f"comment {ident}")
        counters["COMMENT"] += 1
        rec = core.record_base(source, source_sha, "COMMENT", core.unit_id(counters["COMMENT"]), "COMMENT", f"/comment[{ident}]")
        rec.update({
            "sourceNativeId": ident,
            "author": comment.attrib.get(core.qn(core.W, "author")),
            "initials": comment.attrib.get(core.qn(core.W, "initials")),
            "blocks": blocks,
            "text": core.blocks_to_text(blocks),
        })
        records.append(rec)
    return records


def install_stream_parser() -> None:
    core.InlineParser = InlineParser
    core.parse_paragraph = parse_paragraph
    core.parse_table = parse_table
    core.parse_block_children = parse_block_children
    core.parse_body = parse_body
    core.parse_notes = parse_notes
    core.parse_story_part = parse_story_part
    core.parse_comments = parse_comments


def main() -> int:
    install_stream_parser()
    return core.main()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (core.CanonicalError, OSError, zipfile.BadZipFile) as exc:
        print(f"CANONICAL ACCESS ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
