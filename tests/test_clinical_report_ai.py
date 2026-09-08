import json
import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinical_report_ai import (
    build_clinical_report_ai_payload,
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
        "clinical_formulation": "Clinic, această direcție poate fi examinată fără a o transforma într-o trăsătură globală.",
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

    def test_payload_contains_only_case_specific_non_limitation_findings(self):
        payload = build_clinical_report_ai_payload(self.packet)
        self.assertTrue(payload["active_case_findings"])
        self.assertTrue(
            all(item["assertion_mode"] != "LIMITATION" for item in payload["active_case_findings"])
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

    def test_valid_block_passes_existing_support_envelope(self):
        finding = next(
            item for item in self.packet.report.findings
            if item.assertion_mode != "LIMITATION"
        )
        result = parse_openai_clinical_report_response(
            self.packet,
            _response([_raw_block(finding)]),
        )
        self.assertEqual(len(result.blocks), 1)
        self.assertEqual(result.blocks[0].support_claim_ids, (finding.claim_id,))

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
            if item.assertion_mode != "LIMITATION"
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
            if item.assertion_mode != "LIMITATION"
        )
        block = _raw_block(finding, title="APPROVED finding")
        with self.assertRaisesRegex(ValueError, "technical/audit vocabulary"):
            parse_openai_clinical_report_response(self.packet, _response([block]))


if __name__ == "__main__":
    unittest.main()
