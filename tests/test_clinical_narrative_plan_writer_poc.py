import json
import unittest

from szondi3.clinical_composition import NULL_SYNTHESIS
from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_narrative_plan import (
    CLOSING,
    EDITORIAL,
    EDITORIAL_REPORT_SCOPE,
    EXPLAIN,
    EXPLANATION,
    NUCLEUS_SCOPE,
    OPENING,
    QUESTION,
    build_clinical_narrative_plan,
)
from szondi3.clinical_nucleus_projection import build_clinical_nucleus_projection
from szondi3.clinical_nucleus_writer_poc import (
    NUCLEUS_WRITER_STYLE_INSTRUCTIONS,
    build_openai_clinical_nucleus_writer_request,
    replay_clinical_nucleus_writer_response,
)
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}


def _reaction(factor: str, symbol: str) -> FactorReaction:
    base = "±" if symbol.startswith("±") else symbol[0]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=_KIND[base],
        symbol=symbol,
        quantum_level=symbol.count("!"),
    )


def _profile(**overrides):
    return build_profile(
        _reaction(factor, overrides.get(factor, "0"))
        for factor in FACTORS
    )


def _case_a():
    # Reference Case A from the clinical-composition handoff:
    # h- s+ | e+ hy0 | k+ p+ | d- m-
    evaluation = evaluate_clinical_protocol(
        ProfileSeries(
            (
                _profile(
                    h="-",
                    s="+",
                    e="+",
                    hy="0",
                    k="+",
                    p="+",
                    d="-",
                    m="-",
                ),
            )
        ),
        production=True,
    )
    packet = build_clinical_evidence_packet(evaluation)
    projection = build_clinical_nucleus_projection(packet)
    plan = build_clinical_narrative_plan(projection, profile_number=1)
    return packet, projection, plan


def _case_a_writer_fixture(projection, plan):
    profile = projection.profile(1)
    n1 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000042")
    n2 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000038")
    n3 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000078")

    s1 = plan.section_for_nucleus(n1.nucleus_id)
    s2 = plan.section_for_nucleus(n2.nucleus_id)
    s3 = plan.section_for_nucleus(n3.nucleus_id)
    opening = next(item for item in plan.sections if item.purpose == OPENING)
    closing = next(item for item in plan.sections if item.purpose == CLOSING)

    output = {
        "items": [
            {
                "item_id": "A-001",
                "section_id": opening.section_id,
                "scope_type": EDITORIAL_REPORT_SCOPE,
                "nucleus_id": None,
                "claim_ids": [],
                "relation_ids": [],
                "speech_act": EDITORIAL,
                "text": (
                    "Materialul se organizează în trei direcții distincte. "
                    "Ele pot fi citite împreună ca hartă de explorare, dar trebuie "
                    "păstrate separate la nivelul relațiilor pe care datele le autorizează."
                ),
            },
            {
                "item_id": "A-002",
                "section_id": s1.section_id,
                "scope_type": NUCLEUS_SCOPE,
                "nucleus_id": n1.nucleus_id,
                "claim_ids": [
                    "IC_SZONDI_PRIMARY_000008",
                    "IC_SZONDI_PRIMARY_000009",
                    "IC_SZONDI_PRIMARY_000042",
                ],
                "relation_ids": ["CCR-P1-042"],
                "speech_act": EXPLANATION,
                "text": (
                    "În primul nucleu, +k și +p intră împreună în configurația Sch ++, "
                    "pe care Szondi o descrie ca Introinflation (introinflație): "
                    "introiecția și aspirația de expansiune a Eului sunt articulate aici "
                    "prin relația autorizată a configurației, nu doar prin simpla lor coexistență."
                ),
            },
            {
                "item_id": "A-003",
                "section_id": s1.section_id,
                "scope_type": NUCLEUS_SCOPE,
                "nucleus_id": n1.nucleus_id,
                "claim_ids": ["IC_SZONDI_PRIMARY_000073"],
                "relation_ids": ["CCR-P1-073"],
                "speech_act": EXPLANATION,
                "text": (
                    "Aceeași configurație deschide și problema Allessein "
                    "(aspirația de a fi totul), a Deflation (reducerea acestei pretenții) "
                    "și a Eului care ia poziție față de realitate. Formula nu stabilește "
                    "dacă această limitare reușește sau eșuează în cazul persoanei."
                ),
            },
            {
                "item_id": "A-004",
                "section_id": s1.section_id,
                "scope_type": NUCLEUS_SCOPE,
                "nucleus_id": n1.nucleus_id,
                "claim_ids": ["IC_SZONDI_PRIMARY_000073"],
                "relation_ids": [],
                "speech_act": QUESTION,
                "text": (
                    "Ce se întâmplă, în situații concrete, când o investiție, un rol "
                    "sau o posibilitate importantă întâlnește o limită impusă de realitate?"
                ),
            },
            {
                "item_id": "A-005",
                "section_id": s2.section_id,
                "scope_type": NUCLEUS_SCOPE,
                "nucleus_id": n2.nucleus_id,
                "claim_ids": ["IC_SZONDI_PRIMARY_000038"],
                "relation_ids": ["CCR-P1-038"],
                "speech_act": EXPLANATION,
                "text": (
                    "Un al doilea nucleu privește identificarea introiectivă: relația "
                    "-m/+k permite discutarea incorporării și însușirii în procesul de "
                    "identificare. Identificarea nu este identitate și nu definește persoana în întregime."
                ),
            },
            {
                "item_id": "A-006",
                "section_id": s2.section_id,
                "scope_type": NUCLEUS_SCOPE,
                "nucleus_id": n2.nucleus_id,
                "claim_ids": ["IC_SZONDI_PRIMARY_000038"],
                "relation_ids": [],
                "speech_act": QUESTION,
                "text": (
                    "Ce calități ale altora sunt doar admirate sau imitate și ce ajunge "
                    "să fie efectiv însușit ori incorporat?"
                ),
            },
            {
                "item_id": "A-007",
                "section_id": s3.section_id,
                "scope_type": NUCLEUS_SCOPE,
                "nucleus_id": n3.nucleus_id,
                "claim_ids": ["IC_SZONDI_PRIMARY_000078"],
                "relation_ids": ["CCR-P1-078"],
                "speech_act": EXPLANATION,
                "text": (
                    "Separat, combinația C -- cu Sch ++ este legată, în vocabularul lui "
                    "Szondi, de Kontaktsperre (blocarea contactului) și de forme narcisice "
                    "de protecție a Eului. Această formulare nu autorizează un diagnostic "
                    "narcisic și nu selectează ca fapt personal ramurile sexuale istorice "
                    "din contextul doctrinei."
                ),
            },
            {
                "item_id": "A-008",
                "section_id": s3.section_id,
                "scope_type": NUCLEUS_SCOPE,
                "nucleus_id": n3.nucleus_id,
                "claim_ids": ["IC_SZONDI_PRIMARY_000078"],
                "relation_ids": [],
                "speech_act": QUESTION,
                "text": (
                    "Ce precede, dacă apare clinic, închiderea contactului și ce se schimbă "
                    "în raport cu interlocutorul?"
                ),
            },
            {
                "item_id": "A-009",
                "section_id": closing.section_id,
                "scope_type": EDITORIAL_REPORT_SCOPE,
                "nucleus_id": None,
                "claim_ids": [],
                "relation_ids": [],
                "speech_act": EDITORIAL,
                "text": (
                    "Cele trei direcții rămân distincte. Materialul disponibil nu "
                    "autorizează o singură dinamică psihodinamică globală care să le explice pe toate."
                ),
            },
        ]
    }
    return {
        "id": "resp_case_a_replay_001",
        "model": "gpt-5.6-sol-poc-fixture",
        "status": "completed",
        "output_text": json.dumps(output, ensure_ascii=False),
    }


class ClinicalNarrativePlanTests(unittest.TestCase):
    def test_case_a_plan_is_minimal_editorial_plus_three_nuclei_plus_closing(self):
        _, projection, plan = _case_a()
        profile = projection.profile(1)

        self.assertEqual(plan.global_synthesis_mode, NULL_SYNTHESIS)
        self.assertEqual(len(plan.nucleus_ids), 3)
        self.assertEqual(len(plan.sections), 5)

        opening, n1_section, n2_section, n3_section, closing = plan.sections
        self.assertEqual((opening.purpose, closing.purpose), (OPENING, CLOSING))
        self.assertEqual(opening.scope_type, EDITORIAL_REPORT_SCOPE)
        self.assertEqual(closing.scope_type, EDITORIAL_REPORT_SCOPE)
        self.assertFalse(opening.semantic_bridge_allowed)
        self.assertFalse(closing.semantic_bridge_allowed)
        self.assertEqual(opening.allowed_claim_ids, ())
        self.assertEqual(opening.allowed_relation_ids, ())
        self.assertEqual(opening.allowed_nucleus_ids, plan.nucleus_ids)
        self.assertEqual(closing.allowed_nucleus_ids, plan.nucleus_ids)

        for section in (n1_section, n2_section, n3_section):
            self.assertEqual(section.scope_type, NUCLEUS_SCOPE)
            self.assertEqual(section.purpose, EXPLAIN)
            self.assertEqual(section.allowed_nucleus_ids, (section.nucleus_id,))

        n1 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000042")
        n2 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000038")
        n3 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000078")
        self.assertEqual(plan.section_for_nucleus(n1.nucleus_id).allowed_claim_ids, n1.support_claim_ids)
        self.assertEqual(plan.section_for_nucleus(n1.nucleus_id).allowed_relation_ids, n1.relation_ids)
        self.assertEqual(plan.section_for_nucleus(n2.nucleus_id).allowed_relation_ids, n2.relation_ids)
        self.assertEqual(plan.section_for_nucleus(n3.nucleus_id).allowed_relation_ids, n3.relation_ids)

        n1_relations = set(n1.relation_ids)
        self.assertTrue(n1_relations)
        self.assertTrue(
            n1_relations.isdisjoint(
                plan.section_for_nucleus(n2.nucleus_id).allowed_relation_ids
            )
        )
        self.assertTrue(
            n1_relations.isdisjoint(
                plan.section_for_nucleus(n3.nucleus_id).allowed_relation_ids
            )
        )

        no_bridge_pairs = {frozenset(pair) for pair in plan.no_bridge_pairs}
        self.assertIn(frozenset((n1.nucleus_id, n2.nucleus_id)), no_bridge_pairs)
        self.assertIn(frozenset((n1.nucleus_id, n3.nucleus_id)), no_bridge_pairs)
        self.assertIn(frozenset((n2.nucleus_id, n3.nucleus_id)), no_bridge_pairs)

    def test_null_synthesis_preserves_editorial_synthesis_but_not_semantic_bridge_authority(self):
        _, _, plan = _case_a()

        self.assertEqual(plan.global_synthesis_mode, NULL_SYNTHESIS)
        editorial = tuple(
            item for item in plan.sections if item.scope_type == EDITORIAL_REPORT_SCOPE
        )
        self.assertEqual(len(editorial), 2)
        for section in editorial:
            self.assertEqual(section.allowed_speech_acts, (EDITORIAL,))
            self.assertFalse(section.semantic_bridge_allowed)
            self.assertEqual(section.allowed_claim_ids, ())
            self.assertEqual(section.allowed_relation_ids, ())

    def test_plan_is_deterministic_and_invalid_inputs_fail_closed(self):
        _, projection, first = _case_a()
        second = build_clinical_narrative_plan(projection, profile_number=1)
        self.assertEqual(first.to_dict(), second.to_dict())

        with self.assertRaisesRegex(TypeError, "ClinicalForegroundNucleusProjection"):
            build_clinical_narrative_plan(object(), profile_number=1)
        with self.assertRaisesRegex(ValueError, "positive integer"):
            build_clinical_narrative_plan(projection, profile_number=0)
        with self.assertRaises(KeyError):
            first.section_for_nucleus("CN-DOES-NOT-EXIST")


class ClinicalNucleusWriterPOCTests(unittest.TestCase):
    def test_case_a_replay_binds_every_item_to_plan_scope_nucleus_claims_and_relations(self):
        _, projection, plan = _case_a()
        response = _case_a_writer_fixture(projection, plan)

        result = replay_clinical_nucleus_writer_response(projection, plan, response)

        self.assertEqual(result.response_id, "resp_case_a_replay_001")
        self.assertEqual(
            {item.section_id for item in result.items},
            {section.section_id for section in plan.sections},
        )

        section_order = {section.section_id: section.order for section in plan.sections}
        self.assertEqual(
            [section_order[item.section_id] for item in result.items],
            sorted(section_order[item.section_id] for item in result.items),
        )

        for item in result.items:
            section = plan.section(item.section_id)
            self.assertEqual(item.scope_type, section.scope_type)
            if item.scope_type == EDITORIAL_REPORT_SCOPE:
                self.assertIsNone(item.nucleus_id)
                self.assertEqual(item.claim_ids, ())
                self.assertEqual(item.relation_ids, ())
                self.assertEqual(item.speech_act, EDITORIAL)
            else:
                self.assertEqual(item.nucleus_id, section.nucleus_id)
                self.assertTrue(set(item.claim_ids).issubset(section.allowed_claim_ids))
                self.assertTrue(set(item.relation_ids).issubset(section.allowed_relation_ids))

        closing_item = result.items[-1]
        self.assertEqual(closing_item.scope_type, EDITORIAL_REPORT_SCOPE)
        self.assertIn("rămân distincte", closing_item.text)
        self.assertIn("nu autorizează", closing_item.text)

    def test_writer_rejects_cross_nucleus_relation_and_editorial_relation_consumption(self):
        _, projection, plan = _case_a()
        profile = projection.profile(1)
        n1 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000042")
        n2 = profile.nucleus_for_claim("IC_SZONDI_PRIMARY_000038")

        response = _case_a_writer_fixture(projection, plan)
        decoded = json.loads(response["output_text"])

        n2_item = next(
            item
            for item in decoded["items"]
            if item["nucleus_id"] == n2.nucleus_id and item["speech_act"] == EXPLANATION
        )
        n2_item["relation_ids"] = [n1.relation_ids[0]]
        bad_cross = dict(response)
        bad_cross["output_text"] = json.dumps(decoded, ensure_ascii=False)
        with self.assertRaisesRegex(ValueError, "relation outside its nucleus"):
            replay_clinical_nucleus_writer_response(projection, plan, bad_cross)

        response = _case_a_writer_fixture(projection, plan)
        decoded = json.loads(response["output_text"])
        decoded["items"][0]["relation_ids"] = [n1.relation_ids[0]]
        bad_editorial = dict(response)
        bad_editorial["output_text"] = json.dumps(decoded, ensure_ascii=False)
        with self.assertRaisesRegex(ValueError, "Editorial writer item cannot consume"):
            replay_clinical_nucleus_writer_response(projection, plan, bad_editorial)

    def test_writer_rejects_nonexistent_nucleus_and_missing_plan_section(self):
        _, projection, plan = _case_a()

        response = _case_a_writer_fixture(projection, plan)
        decoded = json.loads(response["output_text"])
        nucleus_item = next(
            item for item in decoded["items"] if item["scope_type"] == NUCLEUS_SCOPE
        )
        nucleus_item["nucleus_id"] = "CN-DOES-NOT-EXIST"
        bad_nucleus = dict(response)
        bad_nucleus["output_text"] = json.dumps(decoded, ensure_ascii=False)
        with self.assertRaisesRegex(ValueError, "nucleus_id does not match"):
            replay_clinical_nucleus_writer_response(projection, plan, bad_nucleus)

        response = _case_a_writer_fixture(projection, plan)
        decoded = json.loads(response["output_text"])
        closing_id = next(item.section_id for item in plan.sections if item.purpose == CLOSING)
        decoded["items"] = [
            item for item in decoded["items"] if item["section_id"] != closing_id
        ]
        missing_closing = dict(response)
        missing_closing["output_text"] = json.dumps(decoded, ensure_ascii=False)
        with self.assertRaisesRegex(ValueError, "omitted NarrativePlan sections"):
            replay_clinical_nucleus_writer_response(projection, plan, missing_closing)

    def test_request_is_offline_build_only_and_keeps_style_separate_for_future_ablation(self):
        _, projection, plan = _case_a()

        request = build_openai_clinical_nucleus_writer_request(
            projection, plan, model="fixture-model"
        )
        self.assertEqual(request["model"], "fixture-model")
        self.assertFalse(request["store"])
        self.assertEqual(request["tools"], [])
        self.assertIn(NUCLEUS_WRITER_STYLE_INSTRUCTIONS, request["instructions"])
        self.assertIn('"narrative_plan"', request["input"][0]["content"][0]["text"])
        self.assertIn('"profile_projection"', request["input"][0]["content"][0]["text"])

        first = replay_clinical_nucleus_writer_response(
            projection, plan, _case_a_writer_fixture(projection, plan)
        )
        second = replay_clinical_nucleus_writer_response(
            projection, plan, _case_a_writer_fixture(projection, plan)
        )
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
