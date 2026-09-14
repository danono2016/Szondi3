import unittest
from types import SimpleNamespace

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinical_report_plan import (
    ClinicalReportPlan,
    ClinicalReportPlanUnit,
    build_clinical_report_plan,
)
from szondi3.clinical_report_voice import (
    CLINICAL_REPORT_VOICE_SPEC_VERSION,
    build_clinical_report_voice_directives,
    hard_terms_for_unit,
    validate_clinical_report_voice,
    voice_directives_payload,
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


def _unit(statement, *, unit_id="RPU-P1-001", anti_inferences=()):
    return ClinicalReportPlanUnit(
        unit_id=unit_id,
        scope="PROFILE",
        profile_number=1,
        composition_mode="ATOMIC",
        support_claim_ids=("IC_TEST",),
        support_fact_ids=("F_TEST",),
        support_doctrine_ids=("DR_TEST",),
        anti_inference_ids=tuple(f"AI-{index}" for index, _ in enumerate(anti_inferences, start=1)),
        authorized_statements=(statement,),
        anti_inferences=tuple(anti_inferences),
        source_strength_notes=(),
        sensitive_domains=(),
    )


def _block(unit, *, text, examples=("Exemplu explicativ: o scenă strict ipotetică.",)):
    return SimpleNamespace(
        block_id=unit.unit_id,
        title="Titlu clinic",
        szondi_reading=text,
        clinical_formulation="Mișcarea este explicată în română directă.",
        illustrative_examples=examples,
        exploration_questions=("Povestiți-mi despre o situație concretă relevantă.",),
        relevant_limit=None,
    )


class ClinicalReportVoiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = _packet()

    def test_live_plan_receives_one_voice_directive_per_unit(self):
        plan = build_clinical_report_plan(self.packet)
        directives = build_clinical_report_voice_directives(self.packet, plan)
        self.assertEqual(
            [item.unit_id for item in directives],
            [item.unit_id for item in plan.units],
        )
        payload = voice_directives_payload(self.packet, plan)
        self.assertEqual(payload["version"], CLINICAL_REPORT_VOICE_SPEC_VERSION)
        self.assertEqual(len(payload["units"]), len(plan.units))

    def test_hard_term_compiler_preserves_direct_szondian_vocabulary(self):
        unit = _unit(
            "Szondi numește aceste forme narzißtische Formen des Ich-Schutzes; "
            "contextul poate fi inzestuös, bisexuell, invertiert sau pervers."
        )
        terms = {item.term_ro: item for item in hard_terms_for_unit(unit)}
        self.assertEqual(
            set(terms),
            {"narcisic", "incestuos", "bisexualitate", "inversiune", "perversiune"},
        )
        self.assertEqual(terms["narcisic"].predication_scope, "MECHANISM")
        self.assertEqual(terms["perversiune"].predication_scope, "DOCTRINE_ONLY")
        self.assertTrue(terms["perversiune"].historical_context)

    def test_hard_terms_are_never_activated_only_by_anti_inference_text(self):
        unit = _unit(
            "Szondi descrie identificarea prin introiecție.",
            anti_inferences=(
                "Constatarea nu dovedește narcisism modern, perversiune sau criminalitate.",
            ),
        )
        self.assertEqual(hard_terms_for_unit(unit), ())

    def test_risk_sensitive_terms_make_hypothetical_scene_optional(self):
        unit = _unit("Sursa discută Suizid și Mord ca termeni doctrinari.")
        plan = ClinicalReportPlan(version="TEST", units=(unit,))
        directive = build_clinical_report_voice_directives(self.packet, plan)[0]
        self.assertEqual(directive.example_policy, "OPTIONAL_CANONICAL_PREFERRED")
        terms = {item.term_ro for item in directive.hard_terms}
        self.assertEqual(terms, {"sinucidere", "omor"})

    def test_ordinary_unit_requires_a_concrete_hypothetical_example(self):
        unit = _unit("Szondi descrie Introjektion ca însușire.")
        plan = ClinicalReportPlan(version="TEST", units=(unit,))
        block = _block(unit, text="Introiecția ia ceva în sine.", examples=())
        with self.assertRaisesRegex(ValueError, "requires at least one"):
            validate_clinical_report_voice(self.packet, plan, (block,))

    def test_mandatory_hard_term_cannot_be_euphemized_away(self):
        unit = _unit("Szondi numește forma narzißtisch.")
        plan = ClinicalReportPlan(version="TEST", units=(unit,))
        euphemized = _block(unit, text="Este o formă de autoprotecție a Eului.")
        with self.assertRaisesRegex(ValueError, "mandatory hard term: narcisic"):
            validate_clinical_report_voice(self.packet, plan, (euphemized,))

        direct = _block(
            unit,
            text="Szondi o numește o formă narcisică de protecție a Eului.",
        )
        validate_clinical_report_voice(self.packet, plan, (direct,))

    def test_untranslated_germanism_is_rejected_from_clinician_prose(self):
        unit = _unit("Szondi descrie introiecția ca însușire.")
        plan = ClinicalReportPlan(version="TEST", units=(unit,))
        block = _block(unit, text="Introjektion înseamnă însușire.")
        with self.assertRaisesRegex(ValueError, "untranslated Germanism"):
            validate_clinical_report_voice(self.packet, plan, (block,))

    def test_software_jargon_is_rejected_from_clinician_prose(self):
        unit = _unit("Szondi descrie introiecția ca însușire.")
        plan = ClinicalReportPlan(version="TEST", units=(unit,))
        block = _block(unit, text="Finding-ul descrie însușirea.")
        with self.assertRaisesRegex(ValueError, "software/audit vocabulary"):
            validate_clinical_report_voice(self.packet, plan, (block,))

    def test_wrong_input_types_fail_closed(self):
        plan = build_clinical_report_plan(self.packet)
        with self.assertRaises(TypeError):
            build_clinical_report_voice_directives(object(), plan)
        with self.assertRaises(TypeError):
            build_clinical_report_voice_directives(self.packet, object())
        with self.assertRaises(TypeError):
            validate_clinical_report_voice(self.packet, plan, [])


if __name__ == "__main__":
    unittest.main()
