import json
import unittest

from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_report_ai_v4 import (
    CLINICAL_REPORT_AI_V4_CONTRACT_VERSION,
    ClinicalReportAIV4Result,
    build_openai_clinical_report_request_v4,
    parse_openai_clinical_report_response_v4,
)
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
        "inflation": next(u for u in units if len(u.support_claim_ids) == 1 and any("+p" in s and "Inflation" in s for s in u.authorized_statements)),
        "introjection": next(u for u in units if len(u.support_claim_ids) == 1 and any("+k" in s and "Introjektion" in s for s in u.authorized_statements)),
        "identification": next(u for u in units if any("−m" in s and "+k" in s for s in u.authorized_statements)),
        "sch": next(u for u in units if len(u.support_claim_ids) == 2),
        "contact": next(u for u in units if any("Kontaktsperre" in s for s in u.authorized_statements)),
    }


def _valid_decoded(packet):
    u = _role_units(packet)
    return {
        "summary": [
            {
                "item_id": "S1",
                "unit_id": u["sch"].unit_id,
                "kind": "SYNTHESIS",
                "text": "Centrul de greutate al materialului disponibil se află în introinflație: însușirea și expansiunea funcționează împreună, iar problema clinică devine limita impusă de realitate.",
            },
            {
                "item_id": "S2",
                "unit_id": u["contact"].unit_id,
                "kind": "SYNTHESIS",
                "text": "În același profil, blocarea contactului este legată doctrinar de o formă narcisică de protecție a Eului; formula nu stabilește ce primejdie pulsională concretă ar exista.",
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
                        "text": "Introiecția descrie mișcarea prin care ceva valoros este încorporat, luat în posesie și făcut propriu.",
                    },
                    {
                        "item_id": "P2",
                        "unit_id": u["inflation"].unit_id,
                        "kind": "EXPLANATION",
                        "text": "Inflația descrie mișcarea către dublare, perfecțiune și totalitate: forma parțială tinde să fie împinsă către mai mult.",
                    },
                    {
                        "item_id": "P3",
                        "unit_id": u["sch"].unit_id,
                        "kind": "BIFURCATION",
                        "text": "Două evoluții rămân posibile: Eul poate limita realist pretenția de a fi totul sau poate rămâne prins în ea; configurația singură nu decide între aceste ramuri.",
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
                        "text": "Un contrast util: a admira o calitate nu este încă același lucru cu a o prelua și a o transforma într-o parte a propriului mod de a proceda; identificarea nu este identitatea globală.",
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
                        "text": "Szondi numește această asociere o formă narcisică de protecție a Eului. În vocabularul doctrinar, primejdia pulsională poate fi numită incestuoasă sau poate apărea sub termenii bisexualitate, inversiune ori perversiune, fără ca formula să atribuie persoanei una dintre aceste forme.",
                    },
                    {
                        "item_id": "P6",
                        "unit_id": u["contact"].unit_id,
                        "kind": "EXAMPLE",
                        "text": "De pildă, într-un moment dificil contactul ar putea fi întrerupt, iar persoana s-ar putea retrage din schimbul cu celălalt către propria organizare; scena este doar explicativă și nu precizează natura primejdiei pulsionale.",
                    },
                ],
            },
        ],
        "global_questions": [
            {"question_id": "Q1", "unit_id": u["sch"].unit_id, "text": "Povestiți despre o situație în care ceva important a crescut mult și a trebuit să decideți unde să vă opriți."},
            {"question_id": "Q2", "unit_id": u["identification"].unit_id, "text": "Există un mod de a proceda pe care l-ați preluat de la cineva și l-ați făcut al dumneavoastră?"},
            {"question_id": "Q3", "unit_id": u["contact"].unit_id, "text": "Ce se întâmplă concret înainte de momentele în care contactul cu ceilalți se închide?"},
        ],
        "closing_limits": [
            {"item_id": "L1", "unit_id": u["contact"].unit_id, "kind": "LIMIT", "text": "Terminologia sexuală de mai sus este doctrinară și nu stabilește orientarea, conduita sau diagnosticul persoanei."}
        ],
        "appendix_only_unit_ids": [],
    }


def _response(packet, decoded=None):
    return {
        "id": "resp_v4_test",
        "model": "gpt-5.6-sol",
        "status": "completed",
        "output_text": json.dumps(decoded or _valid_decoded(packet), ensure_ascii=False),
    }


class ClinicalReportAIV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case_run = _run()
        cls.packet = cls.case_run.evidence_packet
        cls.plan = build_clinical_report_plan(cls.packet)

    def test_request_is_global_writer_not_one_block_per_unit(self):
        request = build_openai_clinical_report_request_v4(self.packet)
        self.assertEqual(request["reasoning"], {"effort": "none"})
        self.assertEqual(request["text"]["verbosity"], "medium")
        self.assertEqual(request["text"]["format"]["name"], "szondi3_clinical_report_global_v4")
        instructions = request["instructions"]
        self.assertIn("GLOBAL-WRITER PRINCIPLE", instructions)
        self.assertIn("Do NOT produce one visible mini-report per plan unit", instructions)
        self.assertIn("Every visible text atom", instructions)
        schema = request["text"]["format"]["schema"]
        self.assertIn("summary", schema["properties"])
        self.assertIn("sections", schema["properties"])
        self.assertNotIn("blocks", schema["properties"])

    def test_reference_case_parses_as_one_global_report_and_retains_unit_support(self):
        result = parse_openai_clinical_report_response_v4(self.packet, _response(self.packet))
        self.assertIsInstance(result, ClinicalReportAIV4Result)
        self.assertEqual(result.contract_version, CLINICAL_REPORT_AI_V4_CONTRACT_VERSION)
        self.assertEqual(len(result.sections), 3)
        self.assertEqual(len(result.blocks), len(self.plan.units))
        self.assertEqual(
            {block.support_claim_ids for block in result.blocks},
            {unit.support_claim_ids for unit in self.plan.units},
        )

    def test_every_plan_unit_must_be_narrated_or_explicitly_left_to_appendix(self):
        decoded = _valid_decoded(self.packet)
        intro = _role_units(self.packet)["introjection"].unit_id
        decoded["sections"][0]["passages"] = [
            item for item in decoded["sections"][0]["passages"] if item["unit_id"] != intro
        ]
        with self.assertRaisesRegex(ValueError, "account for every report-plan unit"):
            parse_openai_clinical_report_response_v4(self.packet, _response(self.packet, decoded))

    def test_text_atom_cannot_cite_foreign_or_multiple_units(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][0]["passages"][0]["unit_id"] = "RPU-DOES-NOT-EXIST"
        with self.assertRaisesRegex(ValueError, "unknown report-plan unit"):
            parse_openai_clinical_report_response_v4(self.packet, _response(self.packet, decoded))

    def test_report_level_examples_replace_per_unit_example_quota(self):
        result = parse_openai_clinical_report_response_v4(self.packet, _response(self.packet))
        intro = _role_units(self.packet)["introjection"].unit_id
        intro_examples = [
            p for section in result.sections for p in section.passages
            if p.unit_id == intro and p.kind == "EXAMPLE"
        ]
        self.assertEqual(intro_examples, [])
        self.assertTrue(any(p.kind == "EXAMPLE" for s in result.sections for p in s.passages))

    def test_mandatory_hard_term_cannot_be_misspelled_or_softened(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][2]["passages"][0]["text"] = decoded["sections"][2]["passages"][0]["text"].replace("perversiune", "perversăiune")
        with self.assertRaisesRegex(ValueError, "perversiune"):
            parse_openai_clinical_report_response_v4(self.packet, _response(self.packet, decoded))

    def test_example_must_remain_visibly_hypothetical(self):
        decoded = _valid_decoded(self.packet)
        decoded["sections"][2]["passages"][1]["text"] = "Persoana întrerupe contactul și se retrage către propria organizare."
        with self.assertRaisesRegex(ValueError, "visibly remain hypothetical"):
            parse_openai_clinical_report_response_v4(self.packet, _response(self.packet, decoded))


if __name__ == "__main__":
    unittest.main()
