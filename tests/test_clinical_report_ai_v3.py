import json
import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinical_report_ai_v3 import (
    CLINICAL_REPORT_AI_CONTRACT_VERSION,
    build_clinical_report_ai_payload_v3,
    build_openai_clinical_report_request_v3,
    parse_openai_clinical_report_response_v3,
)
from szondi3.clinical_report_plan import build_clinical_report_plan
from szondi3.clinical_report_voice import build_clinical_report_voice_directives
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


def _response(blocks):
    return {
        "status": "completed",
        "id": "resp_v3_test",
        "model": DEFAULT_PREVIEW_MODEL,
        "output_text": json.dumps({"blocks": blocks}, ensure_ascii=False),
    }


def _valid_blocks(packet):
    plan = build_clinical_report_plan(packet)
    directives = {
        item.unit_id: item
        for item in build_clinical_report_voice_directives(packet, plan)
    }
    blocks = []
    for unit in plan.units:
        directive = directives[unit.unit_id]
        hard_terms = ", ".join(item.term_ro for item in directive.hard_terms)
        reading = "Lectura Szondiană autorizată este redată direct în română."
        if hard_terms:
            reading += " Termenii duri păstrați sunt: " + hard_terms + "."
        blocks.append(
            {
                "block_id": unit.unit_id,
                "scope": unit.scope,
                "profile_number": unit.profile_number,
                "title": "Mișcarea clinică autorizată",
                "szondi_reading": reading,
                "clinical_formulation": (
                    "Mecanismul este formulat prin verbe și mișcări, fără a deveni "
                    "o afirmație globală despre persoană."
                ),
                "illustrative_examples": [
                    "Exemplu explicativ: într-o situație imaginară, aceeași mișcare poate fi observată fără a o atribui cazului."
                ],
                "exploration_questions": [
                    "Povestiți-mi despre o situație concretă în care această mișcare ar putea fi verificată."
                ],
                "relevant_limit": None,
                "support_claim_ids": list(unit.support_claim_ids),
                "support_fact_ids": list(unit.support_fact_ids),
                "support_doctrine_ids": list(unit.support_doctrine_ids),
                "anti_inference_ids_applied": list(unit.anti_inference_ids),
            }
        )
    return blocks


class ClinicalReportAIV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = _packet()
        cls.plan = build_clinical_report_plan(cls.packet)

    def test_payload_contains_binding_plan_and_voice_directives(self):
        payload = build_clinical_report_ai_payload_v3(self.packet)
        self.assertEqual(payload["ai_contract_version"], CLINICAL_REPORT_AI_CONTRACT_VERSION)
        self.assertEqual(payload["report_plan"], self.plan.to_dict())
        self.assertEqual(
            [item["unit_id"] for item in payload["voice_directives"]["units"]],
            [item.unit_id for item in self.plan.units],
        )
        self.assertEqual(len(payload["active_case_findings"]), sum(
            len(unit.support_claim_ids) for unit in self.plan.units
        ))

    def test_request_makes_plan_voice_examples_and_hard_terms_binding(self):
        request = build_openai_clinical_report_request_v3(self.packet)
        instructions = request["instructions"]
        self.assertIn("report_plan.units is mandatory and exhaustive", instructions)
        self.assertIn("DO NOT SOFTEN THE TERM; CONTROL THE PREDICATION", instructions)
        self.assertIn("Exemplu explicativ:", instructions)
        self.assertIn("Contrast discriminativ:", instructions)
        self.assertIn("Bifurcație ilustrativă:", instructions)
        self.assertIn("E.K.P. is outside this writer contract", instructions)
        examples = request["text"]["format"]["schema"]["properties"]["blocks"]["items"]["properties"]["illustrative_examples"]
        self.assertEqual(examples["maxItems"], 4)

    def test_complete_plan_bound_response_passes_all_local_gates(self):
        blocks = _valid_blocks(self.packet)
        result = parse_openai_clinical_report_response_v3(
            self.packet,
            _response(blocks),
        )
        self.assertEqual(result.contract_version, CLINICAL_REPORT_AI_CONTRACT_VERSION)
        self.assertEqual(
            [item.block_id for item in result.blocks],
            [item.unit_id for item in self.plan.units],
        )

    def test_missing_plan_unit_is_rejected(self):
        blocks = _valid_blocks(self.packet)
        self.assertGreater(len(blocks), 1)
        with self.assertRaisesRegex(ValueError, "exactly one block for every report-plan unit"):
            parse_openai_clinical_report_response_v3(
                self.packet,
                _response(blocks[:-1]),
            )

    def test_writer_cannot_rename_or_reorder_plan_units(self):
        blocks = _valid_blocks(self.packet)
        blocks[0]["block_id"] = "invented-unit"
        with self.assertRaisesRegex(ValueError, "must use planned unit id"):
            parse_openai_clinical_report_response_v3(
                self.packet,
                _response(blocks),
            )

    def test_writer_cannot_change_plan_support_envelope(self):
        blocks = _valid_blocks(self.packet)
        blocks[0]["support_fact_ids"] = blocks[0]["support_fact_ids"] + ["F_INVENTED"]
        with self.assertRaisesRegex(ValueError, "changed its deterministic support envelope"):
            parse_openai_clinical_report_response_v3(
                self.packet,
                _response(blocks),
            )

    def test_normal_plan_unit_cannot_drop_all_examples(self):
        blocks = _valid_blocks(self.packet)
        directives = build_clinical_report_voice_directives(self.packet, self.plan)
        normal_index = next(
            index
            for index, directive in enumerate(directives)
            if directive.example_policy == "AT_LEAST_ONE_HYPOTHETICAL"
        )
        blocks[normal_index]["illustrative_examples"] = []
        with self.assertRaisesRegex(ValueError, "requires at least one concrete hypothetical example"):
            parse_openai_clinical_report_response_v3(
                self.packet,
                _response(blocks),
            )

    def test_new_example_markers_and_four_examples_are_accepted(self):
        blocks = _valid_blocks(self.packet)
        blocks[0]["illustrative_examples"] = [
            "Exemplu explicativ: o scenă ipotetică face mișcarea vizibilă.",
            "Contrast discriminativ: simpla asemănare nu este încă același mecanism.",
            "Bifurcație ilustrativă: limita poate fi acceptată sau poate rămâne dificil de tolerat, fără a decide cazul.",
            "Exemplu pur ilustrativ: o a doua scenă rămâne ipotetică.",
        ]
        result = parse_openai_clinical_report_response_v3(
            self.packet,
            _response(blocks),
        )
        self.assertEqual(len(result.blocks[0].illustrative_examples), 4)

    def test_unmarked_example_is_rejected_before_semantic_validation(self):
        blocks = _valid_blocks(self.packet)
        blocks[0]["illustrative_examples"] = ["Persoana face întotdeauna acest lucru."]
        with self.assertRaisesRegex(ValueError, "authorized hypothetical/contrast marker"):
            parse_openai_clinical_report_response_v3(
                self.packet,
                _response(blocks),
            )


if __name__ == "__main__":
    unittest.main()
