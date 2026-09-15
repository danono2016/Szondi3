import unittest

from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_report_ai_v4 import _parse_passage
from szondi3.clinical_report_ai_v4_transport import (
    BODY_ITEM_SCHEMA,
    BODY_KINDS,
    LIMIT_ITEM_SCHEMA,
    LIMIT_KINDS,
    STRICT_RESPONSE_SCHEMA_V4,
    SUMMARY_ITEM_SCHEMA,
    SUMMARY_KINDS,
    build_openai_clinical_report_request_v4_strict,
)
from szondi3.legacy_profile_import import (
    profile_series_from_legacy_text,
    run_legacy_profile_case_from_verified_checkout,
)


REFERENCE_PROFILE = "h- s+ e+ hy0 k+ p+ d- m-"
_ALL_PASSAGE_KINDS = frozenset(
    {"SYNTHESIS", "EXPLANATION", "EXAMPLE", "CONTRAST", "BIFURCATION", "LIMIT"}
)


def _packet():
    series = profile_series_from_legacy_text(REFERENCE_PROFILE)
    run = run_legacy_profile_case_from_verified_checkout(
        series,
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )
    return run.evidence_packet


def _raw(kind: str) -> dict[str, str]:
    text = "De pildă, ar putea apărea astfel." if kind == "EXAMPLE" else "Text clinic valid."
    return {"item_id": f"I-{kind}", "unit_id": "U1", "kind": kind, "text": text}


class ClinicalReportAIV4TransportContractTests(unittest.TestCase):
    def test_schema_kind_enums_are_partitioned_by_structural_slot(self):
        self.assertEqual(
            frozenset(SUMMARY_ITEM_SCHEMA["properties"]["kind"]["enum"]),
            SUMMARY_KINDS,
        )
        self.assertEqual(
            frozenset(BODY_ITEM_SCHEMA["properties"]["kind"]["enum"]),
            BODY_KINDS,
        )
        self.assertEqual(
            frozenset(LIMIT_ITEM_SCHEMA["properties"]["kind"]["enum"]),
            LIMIT_KINDS,
        )
        self.assertEqual(SUMMARY_KINDS, frozenset({"SYNTHESIS"}))
        self.assertEqual(
            BODY_KINDS,
            frozenset({"EXPLANATION", "EXAMPLE", "CONTRAST", "BIFURCATION"}),
        )
        self.assertEqual(LIMIT_KINDS, frozenset({"LIMIT"}))
        self.assertEqual(SUMMARY_KINDS | BODY_KINDS | LIMIT_KINDS, _ALL_PASSAGE_KINDS)
        self.assertFalse(SUMMARY_KINDS & BODY_KINDS)
        self.assertFalse(SUMMARY_KINDS & LIMIT_KINDS)
        self.assertFalse(BODY_KINDS & LIMIT_KINDS)

    def test_every_schema_allowed_kind_is_accepted_by_parser_in_same_slot(self):
        for kind in SUMMARY_KINDS:
            with self.subTest(slot="summary", kind=kind):
                self.assertEqual(_parse_passage(_raw(kind), expected_kinds=SUMMARY_KINDS).kind, kind)
        for kind in BODY_KINDS:
            with self.subTest(slot="body", kind=kind):
                self.assertEqual(_parse_passage(_raw(kind), expected_kinds=BODY_KINDS).kind, kind)
        for kind in LIMIT_KINDS:
            with self.subTest(slot="limits", kind=kind):
                self.assertEqual(_parse_passage(_raw(kind), expected_kinds=LIMIT_KINDS).kind, kind)

    def test_every_known_foreign_kind_is_rejected_by_parser_in_each_slot(self):
        for slot, allowed in (
            ("summary", SUMMARY_KINDS),
            ("body", BODY_KINDS),
            ("limits", LIMIT_KINDS),
        ):
            for kind in sorted(_ALL_PASSAGE_KINDS - allowed):
                with self.subTest(slot=slot, kind=kind):
                    with self.assertRaisesRegex(ValueError, "kind is not allowed here"):
                        _parse_passage(_raw(kind), expected_kinds=allowed)

    def test_strict_response_schema_uses_the_slot_specific_item_schemas(self):
        properties = STRICT_RESPONSE_SCHEMA_V4["properties"]
        self.assertEqual(properties["summary"]["items"], SUMMARY_ITEM_SCHEMA)
        self.assertEqual(
            properties["sections"]["items"]["properties"]["passages"]["items"],
            BODY_ITEM_SCHEMA,
        )
        self.assertEqual(properties["closing_limits"]["items"], LIMIT_ITEM_SCHEMA)

    def test_experimental_transport_request_uses_strict_schema(self):
        request = build_openai_clinical_report_request_v4_strict(_packet())
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertEqual(
            request["text"]["format"]["schema"],
            STRICT_RESPONSE_SCHEMA_V4,
        )
        schema = request["text"]["format"]["schema"]["properties"]
        self.assertEqual(schema["summary"]["items"]["properties"]["kind"]["enum"], ["SYNTHESIS"])
        self.assertEqual(schema["closing_limits"]["items"]["properties"]["kind"]["enum"], ["LIMIT"])


if __name__ == "__main__":
    unittest.main()
