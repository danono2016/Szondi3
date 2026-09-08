import json
import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinical_report_ai import (
    build_clinical_report_ai_payload,
    build_openai_clinical_report_request,
    parse_openai_clinical_report_response,
)
from szondi3.stimuli import SERIES, presentation_rows


def _card_ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def _foreground(offset):
    choices = []
    for series in SERIES:
        cards = _card_ids(series)
        shift = offset % len(cards)
        rotated = cards[shift:] + cards[:shift]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def _packet():
    records = tuple(
        AdministeredTestRecord(_foreground(index))
        for index in range(8)
    )
    run = run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )
    return run.evidence_packet


def _raw_block(finding, *, block_id="B1", title="Lectură clinică"):
    return {
        "block_id": block_id,
        "scope": finding.scope,
        "profile_number": finding.profile_number,
        "title": title,
        "szondi_reading": "În termenii lui Szondi, configurația păstrează sensul direct autorizat de sursă.",
        "clinical_formulation": "Clinic, aceeași direcție este explicată fără a o transforma într-o trăsătură globală.",
        "illustrative_examples": [
            "Exemplu pur ilustrativ: o situație imaginară poate face mai ușor de înțeles aceeași mișcare testologică."
        ],
        "exploration_questions": ["Cum se exprimă această tendință în situația actuală?"],
        "relevant_limit": None,
        "support_claim_ids": [finding.claim_id],
        "support_fact_ids": list(finding.support_fact_ids),
        "support_doctrine_ids": list(finding.doctrine_ids),
        "anti_inference_ids_applied": list(finding.anti_inference_ids),
    }


def _response(blocks):
    return {
        "status": "completed",
        "id": "resp_alpha_test",
        "model": DEFAULT_PREVIEW_MODEL,
        "output_text": json.dumps({"blocks": blocks}, ensure_ascii=False),
    }


class ClinicalReportAIContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = _packet()

    def test_payload_contains_only_foreground_case_specific_non_limitation_findings(self):
        payload = build_clinical_report_ai_payload(self.packet)
        self.assertTrue(payload["active_case_findings"])
        self.assertTrue(
            all(
                item["assertion_mode"] != "LIMITATION"
                and item["scope"] in {"PROFILE", "SERIES"}
                for item in payload["active_case_findings"]
            )
        )
        limitation_ids = {
            item.claim_id for item in self.packet.report.findings
            if item.assertion_mode == "LIMITATION"
        }
        self.assertTrue(limitation_ids)
        self.assertTrue(
            limitation_ids.isdisjoint(
                item["claim_id"] for item in payload["active_case_findings"]
            )
        )

    def test_payload_exposes_exact_profile_morphology_to_avoid_generic_factor_wording(self):
        payload = build_clinical_report_ai_payload(self.packet)
        self.assertEqual(
            payload["profile_morphology"],
            self.packet.report.to_dict()["observations"],
        )
        first = payload["profile_morphology"][0]
        self.assertEqual(first["profile_number"], 1)
        self.assertEqual(
            [item["factor"] for item in first["factors"]],
            ["h", "s", "e", "hy", "k", "p", "d", "m"],
        )
        self.assertTrue(all("symbol" in item and "quantum_level" in item for item in first["factors"]))
        self.assertTrue(all("forced_null" in item for item in first["factors"]))

    def test_request_contract_requires_semantic_expansion_without_doctrinal_expansion(self):
        request = build_openai_clinical_report_request(self.packet)
        instructions = request["instructions"]
        self.assertIn("semantic expansion without doctrinal expansion", instructions)
        self.assertIn("profile_morphology", instructions)
        self.assertIn("Exemplu pur ilustrativ:", instructions)
        self.assertIn("Do not generate a block for an experimental complement", instructions)
        scope_schema = request["text"]["format"]["schema"]["properties"]["blocks"]["items"]["properties"]["scope"]
        self.assertEqual(scope_schema["enum"], ["PROFILE", "SERIES"])

    def test_valid_rich_block_passes_existing_support_envelope(self):
        finding = next(
            item for item in self.packet.report.findings
            if item.assertion_mode != "LIMITATION" and item.scope in {"PROFILE", "SERIES"}
        )
        result = parse_openai_clinical_report_response(
            self.packet,
            _response([_raw_block(finding)]),
        )
        self.assertEqual(len(result.blocks), 1)
        self.assertEqual(result.blocks[0].support_claim_ids, (finding.claim_id,))
        self.assertTrue(result.blocks[0].illustrative_examples[0].startswith("Exemplu pur ilustrativ:"))

    def test_unmarked_example_is_rejected(self):
        finding = next(
            item for item in self.packet.report.findings
            if item.assertion_mode != "LIMITATION" and item.scope in {"PROFILE", "SERIES"}
        )
        block = _raw_block(finding)
        block["illustrative_examples"] = ["Persoana face în mod tipic acest lucru."]
        with self.assertRaisesRegex(ValueError, "explicitly marked as hypothetical"):
            parse_openai_clinical_report_response(self.packet, _response([block]))

    def test_experimental_complement_scope_is_rejected_even_if_claim_id_is_real(self):
        finding = next(
            item for item in self.packet.report.findings
            if item.assertion_mode != "LIMITATION" and item.scope in {"PROFILE", "SERIES"}
        )
        block = _raw_block(finding)
        block["scope"] = "EXPERIMENTAL_COMPLEMENT"
        with self.assertRaisesRegex(ValueError, "PROFILE or SERIES"):
            parse_openai_clinical_report_response(self.packet, _response([block]))

    def test_limitation_claim_cannot_be_promoted_to_patient_narrative(self):
        finding = next(
            item for item in self.packet.report.findings
            if item.assertion_mode == "LIMITATION"
        )
        with self.assertRaisesRegex(ValueError, "LIMITATION"):
            parse_openai_clinical_report_response(
                self.packet,
                _response([_raw_block(finding)]),
            )

    def test_distinct_fact_bundles_cannot_be_joined_into_one_block(self):
        candidates = [
            item for item in self.packet.report.findings
            if item.assertion_mode != "LIMITATION" and item.scope in {"PROFILE", "SERIES"}
        ]
        pair = None
        for first in candidates:
            for second in candidates:
                if (
                    first is not second
                    and first.scope == second.scope
                    and first.profile_number == second.profile_number
                    and set(first.support_fact_ids) != set(second.support_fact_ids)
                ):
                    pair = (first, second)
                    break
            if pair:
                break
        self.assertIsNotNone(pair)
        first, second = pair
        block = _raw_block(first)
        block["support_claim_ids"] = [first.claim_id, second.claim_id]
        block["support_fact_ids"] = list(dict.fromkeys(first.support_fact_ids + second.support_fact_ids))
        block["support_doctrine_ids"] = list(dict.fromkeys(first.doctrine_ids + second.doctrine_ids))
        block["anti_inference_ids_applied"] = list(
            dict.fromkeys(first.anti_inference_ids + second.anti_inference_ids)
        )
        with self.assertRaisesRegex(ValueError, "same deterministic fact bundle"):
            parse_openai_clinical_report_response(self.packet, _response([block]))

    def test_visible_technical_vocabulary_is_rejected(self):
        finding = next(
            item for item in self.packet.report.findings
            if item.assertion_mode != "LIMITATION" and item.scope in {"PROFILE", "SERIES"}
        )
        block = _raw_block(finding, title="APPROVED finding")
        with self.assertRaisesRegex(ValueError, "technical/audit vocabulary"):
            parse_openai_clinical_report_response(self.packet, _response([block]))


if __name__ == "__main__":
    unittest.main()
