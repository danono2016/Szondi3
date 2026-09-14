import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinical_report_plan import (
    CLINICAL_REPORT_PLAN_VERSION,
    build_clinical_report_plan,
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


class ClinicalReportPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = _packet()
        cls.plan = build_clinical_report_plan(cls.packet)

    def test_plan_contains_only_active_foreground_or_series_non_limitation_findings(self):
        planned_claim_ids = {
            claim_id
            for unit in self.plan.units
            for claim_id in unit.support_claim_ids
        }
        eligible_claim_ids = {
            finding.claim_id
            for finding in self.packet.report.findings
            if finding.assertion_mode != "LIMITATION"
            and finding.scope in {"PROFILE", "SERIES"}
        }
        self.assertEqual(planned_claim_ids, eligible_claim_ids)
        self.assertEqual(self.plan.version, CLINICAL_REPORT_PLAN_VERSION)
        self.assertTrue(
            all(unit.scope in {"PROFILE", "SERIES"} for unit in self.plan.units)
        )

    def test_each_active_claim_occurs_in_exactly_one_plan_unit(self):
        planned = [
            claim_id
            for unit in self.plan.units
            for claim_id in unit.support_claim_ids
        ]
        self.assertEqual(len(planned), len(set(planned)))

    def test_units_never_mix_distinct_deterministic_fact_bundles(self):
        finding_index = {
            (finding.claim_id, finding.scope, finding.profile_number): finding
            for finding in self.packet.report.findings
        }
        for unit in self.plan.units:
            fact_bundles = {
                frozenset(
                    finding_index[(claim_id, unit.scope, unit.profile_number)].support_fact_ids
                )
                for claim_id in unit.support_claim_ids
            }
            self.assertEqual(len(fact_bundles), 1)
            expected_facts = set().union(*fact_bundles)
            self.assertEqual(set(unit.support_fact_ids), expected_facts)

    def test_same_scope_profile_and_fact_bundle_is_composed_maximally(self):
        eligible = [
            finding
            for finding in self.packet.report.findings
            if finding.assertion_mode != "LIMITATION"
            and finding.scope in {"PROFILE", "SERIES"}
        ]
        expected_groups = {}
        for finding in eligible:
            key = (
                finding.scope,
                finding.profile_number,
                frozenset(finding.support_fact_ids),
            )
            expected_groups.setdefault(key, []).append(finding.claim_id)

        actual_groups = {
            (
                unit.scope,
                unit.profile_number,
                frozenset(unit.support_fact_ids),
            ): list(unit.support_claim_ids)
            for unit in self.plan.units
        }
        self.assertEqual(set(actual_groups), set(expected_groups))
        for key, claim_ids in expected_groups.items():
            self.assertEqual(actual_groups[key], claim_ids)

    def test_composition_mode_exposes_atomic_vs_same_fact_bundle_without_new_semantics(self):
        for unit in self.plan.units:
            expected = "SAME_FACT_BUNDLE" if len(unit.support_claim_ids) > 1 else "ATOMIC"
            self.assertEqual(unit.composition_mode, expected)
            self.assertEqual(len(unit.authorized_statements), len(set(unit.authorized_statements)))

    def test_plan_carries_exact_union_of_doctrine_and_anti_inference_support(self):
        finding_index = {
            (finding.claim_id, finding.scope, finding.profile_number): finding
            for finding in self.packet.report.findings
        }
        for unit in self.plan.units:
            findings = tuple(
                finding_index[(claim_id, unit.scope, unit.profile_number)]
                for claim_id in unit.support_claim_ids
            )
            expected_doctrine = {
                doctrine_id
                for finding in findings
                for doctrine_id in finding.doctrine_ids
            }
            expected_anti = {
                anti_id
                for finding in findings
                for anti_id in finding.anti_inference_ids
            }
            self.assertEqual(set(unit.support_doctrine_ids), expected_doctrine)
            self.assertEqual(set(unit.anti_inference_ids), expected_anti)

    def test_unit_lookup_is_order_insensitive_and_unknown_signature_fails_closed(self):
        unit = next(item for item in self.plan.units if item.support_claim_ids)
        found = self.plan.unit_for_support_claims(tuple(reversed(unit.support_claim_ids)))
        self.assertEqual(found, unit)
        with self.assertRaises(KeyError):
            self.plan.unit_for_support_claims(("IC_DOES_NOT_EXIST",))

    def test_plan_serialization_is_json_ready_and_preserves_support(self):
        payload = self.plan.to_dict()
        self.assertEqual(payload["version"], CLINICAL_REPORT_PLAN_VERSION)
        self.assertEqual(len(payload["units"]), len(self.plan.units))
        first = payload["units"][0]
        self.assertIn("support_claim_ids", first)
        self.assertIn("support_fact_ids", first)
        self.assertIn("authorized_statements", first)
        self.assertIn("anti_inferences", first)

    def test_wrong_packet_type_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "ClinicalEvidencePacket"):
            build_clinical_report_plan(object())


if __name__ == "__main__":
    unittest.main()
