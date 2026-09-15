from copy import deepcopy
import json
import unittest

from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_report_ai_v4_replay import replay_v4_provider_response
from szondi3.clinical_report_plan import build_clinical_report_plan
from szondi3.legacy_profile_import import (
    profile_series_from_legacy_text,
    run_legacy_profile_case_from_verified_checkout,
)


REFERENCE_PROFILE = "h- s+ e+ hy0 k+ p+ d- m-"


def _run():
    series = profile_series_from_legacy_text(REFERENCE_PROFILE)
    return run_legacy_profile_case_from_verified_checkout(
        series,
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


def _role_units(packet):
    plan = build_clinical_report_plan(packet)
    units = plan.units
    return {
        "inflation": next(
            u
            for u in units
            if len(u.support_claim_ids) == 1
            and any("+p" in s and "Inflation" in s for s in u.authorized_statements)
        ),
        "introjection": next(
            u
            for u in units
            if len(u.support_claim_ids) == 1
            and any("+k" in s and "Introjektion" in s for s in u.authorized_statements)
        ),
        "identification": next(
            u for u in units if any("−m" in s and "+k" in s for s in u.authorized_statements)
        ),
        "sch": next(u for u in units if len(u.support_claim_ids) == 2),
        "contact": next(
            u for u in units if any("Kontaktsperre" in s for s in u.authorized_statements)
        ),
    }


def _valid_decoded(packet):
    u = _role_units(packet)
    return {
        "summary": [
            {
                "item_id": "S1",
                "unit_id": u["sch"].unit_id,
                "kind": "SYNTHESIS",
                "text": (
                    "Centrul de greutate al materialului disponibil se află în introinflație: "
                    "însușirea și expansiunea funcționează împreună, iar problema clinică "
                    "devine limita impusă de realitate."
                ),
            },
            {
                "item_id": "S2",
                "unit_id": u["contact"].unit_id,
                "kind": "SYNTHESIS",
                "text": (
                    "În același profil, blocarea contactului este legată doctrinar de o formă "
                    "narcisică de protecție a Eului; formula nu stabilește ce primejdie "
                    "pulsională concretă ar exista."
                ),
            },
        ],
        "sections": [
            {
                "section_id": "SEC1",
                "title": "A face propriu și a duce mai departe",
                "lead_unit_id": u["sch"].unit_id,
                "passages": [
                    {
                        "item_id": "P1",
                        "unit_id": u["introjection"].unit_id,
                        "kind": "EXPLANATION",
                        "text": (
                            "Introiecția descrie mișcarea prin care ceva valoros este "
                            "încorporat, luat în posesie și făcut propriu."
                        ),
                    },
                    {
                        "item_id": "P2",
                        "unit_id": u["inflation"].unit_id,
                        "kind": "EXPLANATION",
                        "text": (
                            "Inflația descrie mișcarea către dublare, perfecțiune și "
                            "totalitate: forma parțială tinde să fie împinsă către mai mult."
                        ),
                    },
                    {
                        "item_id": "P3",
                        "unit_id": u["sch"].unit_id,
                        "kind": "BIFURCATION",
                        "text": (
                            "Două evoluții rămân posibile: Eul poate limita realist pretenția "
                            "de a fi totul sau poate rămâne prins în ea; configurația singură "
                            "nu decide între aceste ramuri."
                        ),
                    },
                ],
            },
            {
                "section_id": "SEC2",
                "title": "Identificarea prin preluare",
                "lead_unit_id": u["identification"].unit_id,
                "passages": [
                    {
                        "item_id": "P4",
                        "unit_id": u["identification"].unit_id,
                        "kind": "CONTRAST",
                        "text": (
                            "Un contrast util: a admira o calitate nu este încă același lucru "
                            "cu a o prelua și a o transforma într-o parte a propriului mod de "
                            "a proceda; identificarea nu este identitatea globală."
                        ),
                    }
                ],
            },
            {
                "section_id": "SEC3",
                "title": "Când contactul se blochează",
                "lead_unit_id": u["contact"].unit_id,
                "passages": [
                    {
                        "item_id": "P5",
                        "unit_id": u["contact"].unit_id,
                        "kind": "EXPLANATION",
                        "text": (
                            "Szondi numește această asociere o formă narcisică de protecție a "
                            "Eului. În vocabularul doctrinar, primejdia pulsională poate fi "
                            "numită incestuoasă sau poate apărea sub termenii bisexualitate, "
                            "inversiune ori perversiune, fără ca formula să atribuie persoanei "
                            "una dintre aceste forme."
                        ),
                    },
                    {
                        "item_id": "P6",
                        "unit_id": u["contact"].unit_id,
                        "kind": "EXAMPLE",
                        "text": (
                            "De pildă, într-un moment dificil contactul ar putea fi întrerupt, "
                            "iar persoana s-ar putea retrage din schimbul cu celălalt către "
                            "propria organizare; scena este doar explicativă și nu precizează "
                            "natura primejdiei pulsionale."
                        ),
                    },
                ],
            },
        ],
        "global_questions": [
            {
                "question_id": "Q1",
                "unit_id": u["sch"].unit_id,
                "text": (
                    "Povestiți despre o situație în care ceva important a crescut mult și "
                    "a trebuit să decideți unde să vă opriți."
                ),
            },
            {
                "question_id": "Q2",
                "unit_id": u["identification"].unit_id,
                "text": (
                    "Există un mod de a proceda pe care l-ați preluat de la cineva și "
                    "l-ați făcut al dumneavoastră?"
                ),
            },
            {
                "question_id": "Q3",
                "unit_id": u["contact"].unit_id,
                "text": "Ce se întâmplă concret înainte de momentele în care contactul cu ceilalți se închide?",
            },
        ],
        "closing_limits": [
            {
                "item_id": "L1",
                "unit_id": u["contact"].unit_id,
                "kind": "LIMIT",
                "text": (
                    "Terminologia sexuală de mai sus este doctrinară și nu stabilește "
                    "orientarea, conduita sau diagnosticul persoanei."
                ),
            }
        ],
        "appendix_only_unit_ids": [],
    }


def _direct_response(packet, decoded=None):
    payload = _valid_decoded(packet) if decoded is None else decoded
    return {
        "id": "resp_v4_replay",
        "model": "gpt-5.6-sol",
        "status": "completed",
        "output_text": json.dumps(payload, ensure_ascii=False),
    }


def _nested_response(packet, decoded=None):
    payload = _valid_decoded(packet) if decoded is None else decoded
    return {
        "id": "resp_v4_nested",
        "model": "gpt-5.6-sol",
        "status": "completed",
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": json.dumps(payload, ensure_ascii=False),
                    }
                ],
            }
        ],
    }


class _ReplayFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case_run = _run()
        cls.packet = cls.case_run.evidence_packet
        cls.plan = build_clinical_report_plan(cls.packet)
        cls.units = _role_units(cls.packet)


class ClinicalReportV4ReplayGateATests(_ReplayFixture):
    """Gate A: provider extraction, JSON structure and protocol/schema behavior."""

    def test_direct_output_text_replays_through_full_post_provider_pipeline(self):
        result = replay_v4_provider_response(self.packet, _direct_response(self.packet))
        self.assertEqual(result.response_id, "resp_v4_replay")
        self.assertEqual(result.model, "gpt-5.6-sol")
        self.assertEqual(len(result.blocks), len(self.plan.units))

    def test_nested_responses_api_output_replays_identically(self):
        result = replay_v4_provider_response(self.packet, _nested_response(self.packet))
        self.assertEqual(result.response_id, "resp_v4_nested")
        self.assertEqual(len(result.blocks), len(self.plan.units))

    def test_non_completed_response_is_rejected_before_parse(self):
        response = _direct_response(self.packet)
        response["status"] = "incomplete"
        response["incomplete_details"] = {"reason": "max_output_tokens"}
        with self.assertRaisesRegex(ValueError, "response is not completed"):
            replay_v4_provider_response(self.packet, response)

    def test_refusal_is_rejected_before_parse(self):
        response = {
            "id": "resp_refusal",
            "model": "gpt-5.6-sol",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "refusal", "refusal": "cannot comply"}],
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "model refused"):
            replay_v4_provider_response(self.packet, response)

    def test_multiple_nested_output_text_parts_are_rejected(self):
        payload = json.dumps(_valid_decoded(self.packet), ensure_ascii=False)
        response = {
            "id": "resp_multi",
            "model": "gpt-5.6-sol",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "content": [
                        {"type": "output_text", "text": payload},
                        {"type": "output_text", "text": payload},
                    ],
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "exactly one output_text"):
            replay_v4_provider_response(self.packet, response)

    def test_invalid_json_is_rejected(self):
        response = _direct_response(self.packet)
        response["output_text"] = "{not-json"
        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            replay_v4_provider_response(self.packet, response)

    def test_missing_or_extra_top_level_fields_are_rejected(self):
        missing = _valid_decoded(self.packet)
        del missing["closing_limits"]
        with self.assertRaisesRegex(ValueError, "missing or unexpected top-level"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, missing))

        extra = _valid_decoded(self.packet)
        extra["unexpected"] = []
        with self.assertRaisesRegex(ValueError, "missing or unexpected top-level"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, extra))

    def test_known_misplaced_summary_kind_is_rejected_not_repaired(self):
        decoded = _valid_decoded(self.packet)
        decoded["summary"][0]["kind"] = "LIMIT"
        with self.assertRaisesRegex(ValueError, "kind is not allowed here: LIMIT"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_known_misplaced_body_kind_is_rejected_not_repaired(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][0]["passages"][0]["kind"] = "SYNTHESIS"
        with self.assertRaisesRegex(ValueError, "kind is not allowed here: SYNTHESIS"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_unknown_kind_is_rejected(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][0]["passages"][0]["kind"] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "kind is not allowed here: UNKNOWN"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_missing_response_identity_or_model_is_rejected(self):
        missing_id = _direct_response(self.packet)
        del missing_id["id"]
        with self.assertRaisesRegex(ValueError, "lacks response id"):
            replay_v4_provider_response(self.packet, missing_id)

        missing_model = _direct_response(self.packet)
        del missing_model["model"]
        with self.assertRaisesRegex(ValueError, "lacks model identifier"):
            replay_v4_provider_response(self.packet, missing_model)

    def test_known_source_terms_are_normalized_before_germanism_gate(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][0]["passages"][0]["text"] = (
            "Introjektion descrie Einverleibung și Inbesitznahme fără a inventa biografie."
        )
        result = replay_v4_provider_response(
            self.packet,
            _nested_response(self.packet, decoded),
        )
        text = result.sections[0].passages[0].text
        self.assertIn("introiecție", text)
        self.assertIn("încorporare", text)
        self.assertIn("luare în posesie", text)
        self.assertNotIn("Introjektion", text)


class ClinicalReportV4ReplayGateBTests(_ReplayFixture):
    """Gate B: closed-world identifiers, support coverage and semantic safeguards."""

    def test_unknown_unit_id_is_rejected(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][0]["passages"][0]["unit_id"] = "RPU-DOES-NOT-EXIST"
        with self.assertRaisesRegex(ValueError, "unknown report-plan unit"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_duplicate_item_section_and_question_ids_are_rejected(self):
        duplicate_item = _valid_decoded(self.packet)
        duplicate_item["sections"][0]["passages"][0]["item_id"] = "S1"
        with self.assertRaisesRegex(ValueError, "Duplicate clinical report V4 item id"):
            replay_v4_provider_response(
                self.packet,
                _direct_response(self.packet, duplicate_item),
            )

        duplicate_section = _valid_decoded(self.packet)
        duplicate_section["sections"][1]["section_id"] = "SEC1"
        with self.assertRaisesRegex(ValueError, "Duplicate clinical report V4 section id"):
            replay_v4_provider_response(
                self.packet,
                _direct_response(self.packet, duplicate_section),
            )

        duplicate_question = _valid_decoded(self.packet)
        duplicate_question["global_questions"][1]["question_id"] = "Q1"
        with self.assertRaisesRegex(ValueError, "Duplicate clinical report V4 question id"):
            replay_v4_provider_response(
                self.packet,
                _direct_response(self.packet, duplicate_question),
            )

    def test_appendix_duplicates_and_visible_overlap_are_rejected(self):
        duplicate = _valid_decoded(self.packet)
        intro = self.units["introjection"].unit_id
        duplicate["sections"][0]["passages"] = [
            item
            for item in duplicate["sections"][0]["passages"]
            if item["unit_id"] != intro
        ]
        duplicate["appendix_only_unit_ids"] = [intro, intro]
        with self.assertRaisesRegex(ValueError, "contains duplicates"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, duplicate))

        overlap = _valid_decoded(self.packet)
        overlap["appendix_only_unit_ids"] = [self.units["inflation"].unit_id]
        with self.assertRaisesRegex(ValueError, "both visible and appendix-only"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, overlap))

    def test_missing_narrative_coverage_is_rejected(self):
        decoded = _valid_decoded(self.packet)
        intro = self.units["introjection"].unit_id
        decoded["sections"][0]["passages"] = [
            item
            for item in decoded["sections"][0]["passages"]
            if item["unit_id"] != intro
        ]
        with self.assertRaisesRegex(ValueError, "account for every report-plan unit"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_hard_term_unit_cannot_be_hidden_in_appendix(self):
        decoded = _valid_decoded(self.packet)
        contact = self.units["contact"].unit_id
        decoded["summary"] = [item for item in decoded["summary"] if item["unit_id"] != contact]
        decoded["sections"] = [
            section for section in decoded["sections"] if section["lead_unit_id"] != contact
        ]
        decoded["global_questions"] = [
            item for item in decoded["global_questions"] if item["unit_id"] != contact
        ]
        decoded["closing_limits"] = [
            item for item in decoded["closing_limits"] if item["unit_id"] != contact
        ]
        decoded["appendix_only_unit_ids"] = [contact]
        with self.assertRaisesRegex(ValueError, "mandatory hard vocabulary"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_visible_software_jargon_is_rejected(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][0]["passages"][0]["text"] = (
            "Acest unit_id are support_claim_ids suficiente pentru formulare."
        )
        with self.assertRaisesRegex(ValueError, "software/audit vocabulary"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_example_without_visible_hypothetical_marker_is_rejected(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][2]["passages"][1]["text"] = (
            "Persoana întrerupe contactul și se retrage către propria organizare."
        )
        with self.assertRaisesRegex(ValueError, "visibly remain hypothetical"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_malformed_mandatory_hard_term_is_rejected(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][2]["passages"][0]["text"] = decoded["sections"][2]["passages"][0]["text"].replace(
            "perversiune",
            "perversăiune",
        )
        with self.assertRaisesRegex(ValueError, "perversiune"):
            replay_v4_provider_response(self.packet, _direct_response(self.packet, decoded))

    def test_valid_replay_rebuilds_exact_local_support_envelopes(self):
        result = replay_v4_provider_response(self.packet, _direct_response(self.packet))
        self.assertEqual(
            {block.support_claim_ids for block in result.blocks},
            {unit.support_claim_ids for unit in self.plan.units},
        )
        by_claims = {unit.support_claim_ids: unit for unit in self.plan.units}
        for block in result.blocks:
            unit = by_claims[block.support_claim_ids]
            self.assertEqual(block.support_fact_ids, unit.support_fact_ids)
            self.assertEqual(block.support_doctrine_ids, unit.support_doctrine_ids)
            self.assertEqual(block.anti_inference_ids_applied, unit.anti_inference_ids)


if __name__ == "__main__":
    unittest.main()
