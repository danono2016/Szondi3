import io
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import canonical_access as core
import canonical_access_stream as stream

SOURCE = {
    "sourceId": "TEST_STREAM_SOURCE",
    "layer": "SZONDI_PRIMARY",
    "docxPath": "sources/text/test-stream.docx",
}


def document_xml(body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{core.W}" xmlns:r="{core.R}" xmlns:mc="{core.MC}" xmlns:a="{core.A}" xmlns:wp="{core.WP}">
  <w:body>{body}<w:sectPr/></w:body>
</w:document>'''


def make_docx(parts: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "<Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'/>")
        for name, content in parts.items():
            zf.writestr(name, content.encode("utf-8"))
    return buf.getvalue()


class StreamFieldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stream.install_stream_parser()

    def test_field_can_span_paragraph_boundaries(self):
        body = r'''<w:p><w:r><w:fldChar w:fldCharType="begin"/><w:instrText> TOC \o "1-3" </w:instrText><w:fldChar w:fldCharType="separate"/></w:r></w:p>
<w:p><w:r><w:t>Entry one</w:t></w:r></w:p>
<w:p><w:r><w:t>Entry two</w:t><w:fldChar w:fldCharType="end"/></w:r></w:p>'''
        records, _ = core.extract_docx_bytes(
            make_docx({"word/document.xml": document_xml(body)}), SOURCE
        )
        self.assertEqual(records[1]["segments"][0]["fieldId"], "F000001")
        self.assertEqual(records[2]["fields"][0]["fieldCode"], "TOC")
        self.assertEqual(records[2]["fields"][0]["displayedResult"], "Entry oneEntry two")
        self.assertEqual(records[0]["fieldEvents"][-1]["event"], "SEPARATE")
        self.assertEqual(records[2]["fieldEvents"][-1]["event"], "END")

    def test_table_property_exceptions_are_preserved_as_structural_metadata(self):
        body = r'''<w:tbl><w:tr><w:tblPrEx><w:tblW w:w="5000" w:type="dxa"/></w:tblPrEx><w:tc><w:p><w:r><w:t>x</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'''
        records, _ = core.extract_docx_bytes(
            make_docx({"word/document.xml": document_xml(body)}), SOURCE
        )
        row = records[0]["rows"][0]
        meta = row["structuralProperties"][0]
        self.assertEqual(meta["tag"], core.qn(core.W, "tblPrEx"))
        self.assertEqual(meta["children"][0]["tag"], core.qn(core.W, "tblW"))
        self.assertEqual(meta["children"][0]["attributes"][core.qn(core.W, "w")], "5000")


if __name__ == "__main__":
    unittest.main()
