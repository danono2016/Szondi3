import io
import json
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import canonical_access as ca

W = ca.W
R = ca.R
MC = ca.MC
A = ca.A
WP = ca.WP

SOURCE = {
    "sourceId": "TEST_SOURCE",
    "layer": "SZONDI_PRIMARY",
    "docxPath": "sources/text/test.docx",
}


def document_xml(body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}" xmlns:r="{R}" xmlns:mc="{MC}" xmlns:a="{A}" xmlns:wp="{WP}">
  <w:body>{body}<w:sectPr/></w:body>
</w:document>'''


def make_docx(parts: dict[str, str | bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "<Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'/>")
        for name, content in parts.items():
            zf.writestr(name, content.encode("utf-8") if isinstance(content, str) else content)
    return buf.getvalue()


def extract(parts: dict[str, str | bytes]):
    data = make_docx(parts)
    return ca.extract_docx_bytes(data, SOURCE)


class PartClassificationTests(unittest.TestCase):
    def test_known_part_registry(self):
        self.assertEqual(ca.classify_word_xml_part("word/document.xml").stream, "BODY")
        self.assertEqual(ca.classify_word_xml_part("word/footnotes.xml").stream, "FOOTNOTE")
        self.assertEqual(ca.classify_word_xml_part("word/endnotes.xml").stream, "ENDNOTE")
        self.assertEqual(ca.classify_word_xml_part("word/header123.xml").stream, "HEADER")
        self.assertEqual(ca.classify_word_xml_part("word/footer9.xml").stream, "FOOTER")
        self.assertEqual(ca.classify_word_xml_part("word/styles.xml").classification, "SUPPORTED_STRUCTURAL")
        self.assertEqual(ca.classify_word_xml_part("word/theme/theme1.xml").classification, "SUPPORTED_STRUCTURAL")

    def test_unknown_word_xml_part_fails_closed(self):
        with self.assertRaisesRegex(ca.CanonicalError, "UNSUPPORTED_POSSIBLY_MEANINGFUL"):
            extract({
                "word/document.xml": document_xml("<w:p><w:r><w:t>x</w:t></w:r></w:p>"),
                "word/customSemantic.xml": f"<w:custom xmlns:w='{W}'><w:t>meaning</w:t></w:custom>",
            })


class BodyStructureTests(unittest.TestCase):
    def test_body_order_and_table_hierarchy(self):
        body = f'''
<w:p><w:r><w:t>before</w:t></w:r></w:p>
<w:tbl>
  <w:tblPr/><w:tblGrid/>
  <w:tr>
    <w:tc>
      <w:tcPr><w:gridSpan w:val="2"/><w:vMerge w:val="restart"/></w:tcPr>
      <w:p><w:r><w:t>A</w:t></w:r></w:p>
      <w:tbl><w:tr><w:tc><w:p><w:r><w:t>nested</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
    </w:tc>
    <w:tc><w:p><w:r><w:t>B</w:t></w:r></w:p></w:tc>
  </w:tr>
</w:tbl>
<w:p><w:r><w:t>after</w:t></w:r></w:p>'''
        records, _ = extract({"word/document.xml": document_xml(body)})
        body_records = [r for r in records if r["stream"] == "BODY"]
        self.assertEqual([r["kind"] for r in body_records], ["PARAGRAPH", "TABLE", "PARAGRAPH"])
        self.assertEqual(body_records[0]["text"], "before")
        self.assertEqual(body_records[2]["text"], "after")
        cell = body_records[1]["rows"][0]["cells"][0]
        self.assertEqual(cell["gridSpan"], "2")
        self.assertEqual(cell["verticalMerge"], "restart")
        self.assertEqual([b["kind"] for b in cell["blocks"]], ["PARAGRAPH", "TABLE"])
        self.assertEqual(cell["blocks"][1]["rows"][0]["cells"][0]["blocks"][0]["text"], "nested")

    def test_tabs_and_breaks_are_distinct(self):
        body = '''<w:p>
<w:r><w:t>A</w:t><w:tab/><w:t>B</w:t><w:br w:type="page"/><w:t>C</w:t><w:br/><w:t>D</w:t></w:r>
</w:p>'''
        records, _ = extract({"word/document.xml": document_xml(body)})
        p = records[0]
        kinds = [s["kind"] for s in p["segments"]]
        self.assertEqual(kinds, ["TEXT", "TAB", "TEXT", "BREAK", "TEXT", "BREAK", "TEXT"])
        self.assertEqual(p["segments"][3]["breakType"], "page")
        self.assertEqual(p["text"], "A\tB\nC\nD")

    def test_unit_ids_are_zero_padded_and_monotonic(self):
        body = "".join(f"<w:p><w:r><w:t>{i}</w:t></w:r></w:p>" for i in range(3))
        records, _ = extract({"word/document.xml": document_xml(body)})
        self.assertEqual([r["unitId"] for r in records], ["U000001", "U000002", "U000003"])


class NotesTests(unittest.TestCase):
    def test_note_identity_and_reference_linkage(self):
        body = '<w:p><w:r><w:t>Main</w:t><w:footnoteReference w:id="1"/></w:r></w:p>'
        notes = f'''<w:footnotes xmlns:w="{W}">
<w:footnote w:id="-1" w:type="separator"><w:p/></w:footnote>
<w:footnote w:id="0" w:type="continuationSeparator"><w:p/></w:footnote>
<w:footnote w:id="1"><w:p><w:r><w:t>note one</w:t></w:r></w:p></w:footnote>
</w:footnotes>'''
        records, inventory = extract({"word/document.xml": document_xml(body), "word/footnotes.xml": notes})
        note = next(r for r in records if r["stream"] == "FOOTNOTE" and r["sourceNativeId"] == "1")
        self.assertEqual(note["text"], "note one")
        self.assertIn("-1", inventory["specialNoteIds"]["FOOTNOTE"])
        self.assertEqual(records[0]["references"], [{"kind": "footnoteReference", "id": "1"}])

    def test_unresolved_note_reference_fails(self):
        body = '<w:p><w:r><w:footnoteReference w:id="7"/></w:r></w:p>'
        notes = f'<w:footnotes xmlns:w="{W}"></w:footnotes>'
        with self.assertRaisesRegex(ca.CanonicalError, "Unresolved footnote reference"):
            extract({"word/document.xml": document_xml(body), "word/footnotes.xml": notes})


class StoryPartTests(unittest.TestCase):
    def test_headers_and_footers_preserve_each_story_part_including_empty(self):
        parts = {
            "word/document.xml": document_xml("<w:p><w:r><w:t>body</w:t></w:r></w:p>"),
            "word/header1.xml": f'<w:hdr xmlns:w="{W}"><w:p><w:r><w:t>H1</w:t></w:r></w:p></w:hdr>',
            "word/header2.xml": f'<w:hdr xmlns:w="{W}"><w:p/></w:hdr>',
            "word/footer1.xml": f'<w:ftr xmlns:w="{W}"><w:p><w:r><w:t>F1</w:t></w:r></w:p></w:ftr>',
        }
        records, inventory = extract(parts)
        headers = [r for r in records if r["stream"] == "HEADER"]
        self.assertEqual([r["storyPart"] for r in headers], ["word/header1.xml", "word/header2.xml"])
        self.assertEqual(headers[0]["text"], "H1")
        self.assertEqual(headers[1]["text"], "")
        self.assertEqual(inventory["recordCountsByStream"]["HEADER"], 2)


class InlineSemanticsTests(unittest.TestCase):
    def test_field_instruction_is_separate_from_displayed_result(self):
        body = '''<w:p><w:r>
<w:fldChar w:fldCharType="begin"/><w:instrText> PAGE \\* MERGEFORMAT </w:instrText>
<w:fldChar w:fldCharType="separate"/><w:t>12</w:t><w:fldChar w:fldCharType="end"/>
</w:r></w:p>'''
        records, _ = extract({"word/document.xml": document_xml(body)})
        p = records[0]
        self.assertEqual(p["text"], "12")
        self.assertEqual(p["fields"][0]["fieldCode"], "PAGE")
        self.assertIn("PAGE", p["fields"][0]["instruction"])
        self.assertEqual(p["fields"][0]["displayedResult"], "12")

    def test_unknown_field_instruction_fails_closed(self):
        body = '''<w:p><w:r><w:fldChar w:fldCharType="begin"/><w:instrText> MAGICFIELD x </w:instrText>
<w:fldChar w:fldCharType="separate"/><w:t>x</w:t><w:fldChar w:fldCharType="end"/></w:r></w:p>'''
        with self.assertRaisesRegex(ca.CanonicalError, "Unsupported possibly meaningful field instruction"):
            extract({"word/document.xml": document_xml(body)})

    def test_hyperlink_keeps_visible_text_and_relationship_metadata(self):
        body = '<w:p><w:hyperlink r:id="rId7"><w:r><w:t>visible</w:t></w:r></w:hyperlink></w:p>'
        rels = f'''<Relationships xmlns="{ca.PKG_REL}">
<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="https://example.test" TargetMode="External"/>
</Relationships>'''
        records, _ = extract({
            "word/document.xml": document_xml(body),
            "word/_rels/document.xml.rels": rels,
        })
        p = records[0]
        self.assertEqual(p["text"], "visible")
        self.assertEqual(p["hyperlinks"][0]["relationship"]["target"], "https://example.test")
        self.assertNotIn("https://example.test", p["text"])

    def test_bookmark_is_metadata_not_text(self):
        body = '<w:p><w:bookmarkStart w:id="3" w:name="anchor"/><w:r><w:t>text</w:t></w:r><w:bookmarkEnd w:id="3"/></w:p>'
        records, _ = extract({"word/document.xml": document_xml(body)})
        self.assertEqual(records[0]["text"], "text")
        self.assertEqual(records[0]["bookmarks"][0]["name"], "anchor")


class VisualTests(unittest.TestCase):
    def test_drawing_records_relationship_alt_text_and_arbitration_marker(self):
        body = f'''<w:p><w:r><w:drawing>
<wp:inline><wp:docPr id="1" name="Picture 1" descr="formula image"/>
<a:graphic><a:graphicData><a:blip r:embed="rId9"/></a:graphicData></a:graphic>
</wp:inline></w:drawing></w:r></w:p>'''
        rels = f'''<Relationships xmlns="{ca.PKG_REL}">
<Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
</Relationships>'''
        records, _ = extract({"word/document.xml": document_xml(body), "word/_rels/document.xml.rels": rels})
        visual = records[0]["visuals"][0]
        self.assertTrue(visual["visualArbitrationRequired"])
        self.assertEqual(visual["kind"], "DRAWING")
        self.assertEqual(visual["alternativeText"][0]["description"], "formula image")
        self.assertEqual(visual["relationships"][0]["relationshipId"], "rId9")

    def test_text_box_visible_text_is_explicitly_parsed(self):
        body = f'''<w:p><w:r><w:pict>
<v:shape xmlns:v="{ca.V}"><v:textbox><w:txbxContent><w:p><w:r><w:t>boxed text</w:t></w:r></w:p></w:txbxContent></v:textbox></v:shape>
</w:pict></w:r></w:p>'''
        records, _ = extract({"word/document.xml": document_xml(body)})
        visual = records[0]["visuals"][0]
        self.assertEqual(visual["textBoxes"][0]["text"], "boxed text")
        self.assertTrue(visual["visualArbitrationRequired"])

    def test_alternate_content_preserves_choice_and_fallback_variants(self):
        body = f'''<w:p><mc:AlternateContent>
<mc:Choice Requires="w14"><w:r><w:t>choice</w:t></w:r></mc:Choice>
<mc:Fallback><w:r><w:t>fallback</w:t></w:r></mc:Fallback>
</mc:AlternateContent></w:p>'''
        records, _ = extract({"word/document.xml": document_xml(body)})
        variants = records[0]["alternateContent"][0]["variants"]
        self.assertEqual([(v["branch"], v["text"]) for v in variants], [("Choice", "choice"), ("Fallback", "fallback")])
        self.assertTrue(records[0]["alternateContent"][0]["visualArbitrationRequired"])


class FailureAndDeterminismTests(unittest.TestCase):
    def test_unknown_text_namespace_fails_closed(self):
        body = '<w:p xmlns:x="urn:unknown"><x:semantic>meaning</x:semantic></w:p>'
        with self.assertRaisesRegex(ca.CanonicalError, "Unsupported possibly meaningful"):
            extract({"word/document.xml": document_xml(body)})

    def test_input_hash_mismatch_fails(self):
        data = make_docx({"word/document.xml": document_xml("<w:p/>")})
        with self.assertRaisesRegex(ca.CanonicalError, "SHA-256 mismatch"):
            ca.extract_docx_bytes(data, SOURCE, "0" * 64)

    def test_repeated_extraction_serializes_byte_identically(self):
        parts = {
            "word/document.xml": document_xml('<w:p><w:r><w:t>ä deterministic</w:t></w:r></w:p>'),
            "word/header1.xml": f'<w:hdr xmlns:w="{W}"><w:p/></w:hdr>',
        }
        data = make_docx(parts)
        first_records, first_inventory = ca.extract_docx_bytes(data, SOURCE)
        second_records, second_inventory = ca.extract_docx_bytes(data, SOURCE)
        first = "".join(ca.stable_json(r) + "\n" for r in first_records) + json.dumps(first_inventory, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        second = "".join(ca.stable_json(r) + "\n" for r in second_records) + json.dumps(second_inventory, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
