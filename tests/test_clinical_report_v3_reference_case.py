import unittest

from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_report_ai_v3 import build_clinical_report_ai_payload_v3
from szondi3.clinical_report_plan import build_clinical_report_plan
from szondi3.clinical_report_voice import build_clinical_report_voice_directives
from szondi3.legacy_profile_import import (
    profile_series_from_legacy_text,
    run_legacy_profile_case_from_verified_checkout,
)


REFERENCE_PROFILE = "h- s+ e+ hy0 k+ p+ d- m-"


def _packet():
    series = profile_series_from_legacy_text(REFERENCE_PROFILE)
    run = run_legacy_profile_case_from_verified_checkout(
        series,
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )
    return run.evidence_packet


class ClinicalReportV3ReferenceCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = _packet()
        cls.plan = build_clinical_report_plan(cls.packet)
        cls.directives = build_clinical_report_voice_directives(cls.packet, cls.plan)

    def test_reference_case_six_findings_become_five_legal_narrative_units(self):
        findings = tuple(
            finding
            for finding in self.packet.report.findings
            if finding.assertion_mode != "LIMITATION"
            and finding.scope in {"PROFILE", "SERIES"}
        )
        self.assertEqual(len(findings), 6)
        self.assertEqual(len(self.plan.units), 5)
        composed = tuple(
            unit for unit in self.plan.units if unit.composition_mode == "SAME_FACT_BUNDLE"
        )
        self.assertEqual(len(composed), 1)
        self.assertEqual(len(composed[0].support_claim_ids), 2)
        self.assertTrue(
            all("Sch ++" in statement for statement in composed[0].authorized_statements)
        )

    def test_reference_case_keeps_introjection_and_inflation_atomic_outside_sch_bridge(self):
        atomic_statements = [
            statement
            for unit in self.plan.units
            if unit.composition_mode == "ATOMIC"
            for statement in unit.authorized_statements
        ]
        self.assertTrue(any("+p" in statement and "Inflation" in statement for statement in atomic_statements))
        self.assertTrue(any("+k" in statement and "Introjektion" in statement for statement in atomic_statements))
        self.assertTrue(any("−m" in statement and "+k" in statement for statement in atomic_statements))

    def test_contact_introinflation_unit_requires_uncosmetized_hard_vocabulary(self):
        directives_by_id = {item.unit_id: item for item in self.directives}
        target = next(
            unit
            for unit in self.plan.units
            if any("Kontaktsperre" in statement for statement in unit.authorized_statements)
        )
        terms = {item.term_ro for item in directives_by_id[target.unit_id].hard_terms}
        self.assertIn("narcisic", terms)
        self.assertIn("incestuos", terms)
        self.assertIn("bisexualitate", terms)
        self.assertIn("inversiune", terms)
        self.assertIn("perversiune", terms)

    def test_v3_payload_exposes_reference_plan_without_ekp_promotion(self):
        payload = build_clinical_report_ai_payload_v3(self.packet)
        self.assertEqual(len(payload["report_plan"]["units"]), 5)
        self.assertNotIn("experimental_complements", payload["report_plan"])
        self.assertEqual(
            [unit["unit_id"] for unit in payload["report_plan"]["units"]],
            [unit["unit_id"] for unit in payload["voice_directives"]["units"]],
        )


if __name__ == "__main__":
    unittest.main()
