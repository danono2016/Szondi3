import unittest

from szondi3.clinical_facts import complete_formula_facts
from szondi3.formula import (
    FactorTensionLevel,
    FormulaFactorTension,
    FormulaLine,
    FormulaLinePartition,
)
from szondi3.interpretation import ActivationStatus, Fact, evaluate_claim
from szondi3.interpretation_catalogue import CLAIMS_BY_ID


def _factor(name: str, degree: int) -> FormulaFactorTension:
    return FormulaFactorTension(name, degree, degree)


def _line(role: str, *items: tuple[str, int]) -> FormulaLine:
    levels = tuple(
        FactorTensionLevel(degree=degree, factors=(_factor(name, degree),))
        for name, degree in items
    )
    return FormulaLine(role=role, levels=levels)


def _resolved_formula() -> FormulaLinePartition:
    return FormulaLinePartition(
        symptomatic=_line("symptomatic", ("m", 6)),
        submanifest=_line("submanifest", ("d", 4), ("hy", 3)),
        root=_line("root", ("h", 1), ("s", 0)),
    )


class FormulaP2BSemanticsTests(unittest.TestCase):
    def test_adapter_exposes_only_resolved_formula_roles(self):
        facts = {item.key: item for item in complete_formula_facts(_resolved_formula())}
        self.assertTrue(facts["formula.complete.available"].value)
        self.assertEqual(facts["formula.symptomatic_factors"].value, ("m",))
        self.assertEqual(facts["formula.submanifest_factors"].value, ("d", "hy"))
        self.assertEqual(facts["formula.root_factors"].value, ("h", "s"))

    def test_symptom_and_root_semantics_activate_from_resolved_formula(self):
        facts = complete_formula_facts(_resolved_formula())
        for claim_id in ("IC_SZONDI_PRIMARY_000025", "IC_SZONDI_PRIMARY_000026"):
            with self.subTest(claim_id=claim_id):
                result = evaluate_claim(CLAIMS_BY_ID[claim_id], facts)
                self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
                self.assertTrue(result.anti_inferences)

    def test_root_semantics_preserve_historical_genetic_boundary(self):
        facts = complete_formula_facts(_resolved_formula())
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000026"]
        active = evaluate_claim(claim, facts)

        self.assertEqual(active.activation_status, ActivationStatus.ACTIVE)
        self.assertIn("DR_SZ_LEHR_1972_000347", active.provenance_trace)
        self.assertIn("DR_SZ_LEHR_1972_000348", active.provenance_trace)
        self.assertIn("genetică modernă", claim.claim)
        self.assertTrue(
            any(
                "moșteniri genetice contemporane" in guard.prohibited_conclusion
                for guard in active.anti_inferences
            )
        )

    def test_formula_semantics_fail_closed_without_resolved_formula_facts(self):
        for claim_id in ("IC_SZONDI_PRIMARY_000025", "IC_SZONDI_PRIMARY_000026"):
            with self.subTest(claim_id=claim_id):
                result = evaluate_claim(CLAIMS_BY_ID[claim_id], ())
                self.assertEqual(
                    result.activation_status,
                    ActivationStatus.UNRESOLVED_INPUT,
                )

    def test_triebklasse_and_formula_relation_requires_both_outputs(self):
        formula_facts = complete_formula_facts(_resolved_formula())
        leader_fact = Fact(
            key="linnaeus.leading_drive_classes",
            value=("Sh",),
            scope="profile_series",
            fact_id="profile_series:leading_drive_classes",
        )
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000027"]

        active = evaluate_claim(claim, formula_facts + (leader_fact,))
        self.assertEqual(active.activation_status, ActivationStatus.ACTIVE)
        self.assertTrue(active.anti_inferences)
        self.assertIn("se pot transforma", claim.claim)
        self.assertTrue(
            any(
                "permanentă" in guard.prohibited_conclusion
                for guard in active.anti_inferences
            )
        )

        without_class = evaluate_claim(claim, formula_facts)
        self.assertEqual(
            without_class.activation_status,
            ActivationStatus.UNRESOLVED_INPUT,
        )

    def test_formula_relates_symptom_side_to_unsatisfied_drive_side(self):
        facts = complete_formula_facts(_resolved_formula())
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000028"]

        active = evaluate_claim(claim, facts)
        self.assertEqual(active.activation_status, ActivationStatus.ACTIVE)
        self.assertEqual(
            active.provenance_trace[:2],
            ("DR_SZ_LEHR_1972_000316", "DR_SZ_LEHR_1972_000318"),
        )
        self.assertIn("SZ_LEHR_1972", active.provenance_trace)
        self.assertTrue(active.anti_inferences)

        without_root = tuple(
            fact for fact in facts if fact.key != "formula.root_factors"
        )
        unresolved = evaluate_claim(claim, without_root)
        self.assertEqual(
            unresolved.activation_status,
            ActivationStatus.UNRESOLVED_INPUT,
        )


if __name__ == "__main__":
    unittest.main()
