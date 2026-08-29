import unittest

from szondi3.clinical_facts import profile_facts
from szondi3.clinical_interpretation import interpret_facts
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import ActivationStatus, LifecycleStatus, evaluate_claim
from szondi3.interpretation_catalogue import (
    CLAIMS_BY_ID,
    EXECUTABLE_CLAIMS,
    FALL40_CANDIDATE_CLAIMS,
    INITIAL_CLAIMS,
)
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def reaction(factor, kind="null", quantum=0):
    base = {"null": "0", "positive": "+", "negative": "-", "ambivalent": "±"}[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=base + ("!" * quantum),
        quantum_level=quantum,
    )


def profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


class Fall40CatalogueLifecycleTests(unittest.TestCase):
    def test_original_nucleus_stays_approved_and_candidate_tranche_stays_review_only(self):
        self.assertEqual(len(INITIAL_CLAIMS), 12)
        self.assertTrue(all(item.status is LifecycleStatus.APPROVED for item in INITIAL_CLAIMS))
        self.assertEqual(len(FALL40_CANDIDATE_CLAIMS), 10)
        self.assertTrue(
            all(
                item.status is LifecycleStatus.FORMALIZATION_REVIEWED
                for item in FALL40_CANDIDATE_CLAIMS
            )
        )
        self.assertEqual(len(EXECUTABLE_CLAIMS), 22)
        self.assertEqual(len(CLAIMS_BY_ID), 22)

    def test_production_mode_excludes_candidate_meanings_without_clinician_approval(self):
        facts = profile_facts(
            profile(
                {
                    "h": ("positive", 1),
                    "e": ("negative", 1),
                    "hy": ("negative", 0),
                    "d": ("positive", 0),
                    "m": ("negative", 0),
                }
            )
        )
        preview = interpret_facts(facts)
        production = interpret_facts(facts, production=True)

        preview_ids = {item.claim_id for item in preview.findings}
        production_ids = {item.claim_id for item in production.findings}
        self.assertTrue(
            {
                "IC_SZONDI_PRIMARY_000013",
                "IC_SZONDI_PRIMARY_000014",
                "IC_SZONDI_PRIMARY_000015",
                "IC_SZONDI_PRIMARY_000016",
                "IC_SZONDI_PRIMARY_000017",
                "IC_SZONDI_PRIMARY_000018",
                "IC_SZONDI_PRIMARY_000019",
                "IC_SZONDI_PRIMARY_000020",
                "IC_SZONDI_PRIMARY_000021",
            }.issubset(preview_ids)
        )
        self.assertTrue(
            all(int(item.rsplit("_", 1)[1]) <= 12 for item in production_ids)
        )


class Fall40PrimitiveSemanticsTests(unittest.TestCase):
    def evaluate(self, claim_id, overrides):
        return evaluate_claim(CLAIMS_BY_ID[claim_id], profile_facts(profile(overrides)))

    def test_partner_factor_guard_is_active_for_every_complete_profile(self):
        result = self.evaluate("IC_SZONDI_PRIMARY_000013", {})
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertTrue(result.anti_inferences)

    def test_quantum_guard_activates_only_when_a_quantum_mark_is_present(self):
        active = self.evaluate("IC_SZONDI_PRIMARY_000014", {"h": ("positive", 1)})
        inactive = self.evaluate("IC_SZONDI_PRIMARY_000014", {"h": ("positive", 0)})
        self.assertEqual(active.activation_status, ActivationStatus.ACTIVE)
        self.assertEqual(inactive.activation_status, ActivationStatus.INACTIVE)

    def test_positive_h_keeps_eros_and_hypertonia_semantics_separate(self):
        ordinary_facts = profile_facts(profile({"h": ("positive", 0)}))
        hypertonic_facts = profile_facts(profile({"h": ("positive", 2)}))

        base_claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000015"]
        hyper_claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000016"]
        self.assertEqual(
            evaluate_claim(base_claim, ordinary_facts).activation_status,
            ActivationStatus.ACTIVE,
        )
        self.assertEqual(
            evaluate_claim(hyper_claim, ordinary_facts).activation_status,
            ActivationStatus.INACTIVE,
        )
        self.assertEqual(
            evaluate_claim(hyper_claim, hypertonic_facts).activation_status,
            ActivationStatus.ACTIVE,
        )
        self.assertIn("Eroshypertonie", hyper_claim.claim)

    def test_negative_e_keeps_kain_semantics_without_criminal_or_epilepsy_verdict(self):
        result = self.evaluate("IC_SZONDI_PRIMARY_000017", {"e": ("negative", 0)})
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertIn("Kain", CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000017"].claim)
        prohibited = " ".join(item.prohibited_conclusion for item in result.anti_inferences)
        self.assertIn("epilepsie", prohibited)
        self.assertIn("criminalitate", prohibited)

    def test_hypertonic_negative_e_adds_affect_accumulation_but_not_violence_prediction(self):
        ordinary = self.evaluate("IC_SZONDI_PRIMARY_000018", {"e": ("negative", 0)})
        hyper = self.evaluate("IC_SZONDI_PRIMARY_000018", {"e": ("negative", 1)})
        self.assertEqual(ordinary.activation_status, ActivationStatus.INACTIVE)
        self.assertEqual(hyper.activation_status, ActivationStatus.ACTIVE)
        self.assertTrue(hyper.anti_inferences)

    def test_negative_hy_is_verbergung_not_generic_emotional_inhibition(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000019"]
        result = self.evaluate(claim.claim_id, {"hy": ("negative", 0)})
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertIn("Verbergungsdrang", claim.claim)

    def test_positive_d_is_search_and_change(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000020"]
        result = self.evaluate(claim.claim_id, {"d": ("positive", 0)})
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertIn("Auf-Suche-Gehen", claim.claim)

    def test_negative_m_is_detachment_and_must_not_be_semantically_reversed(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000021"]
        result = self.evaluate(claim.claim_id, {"m": ("negative", 0)})
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertIn("Abtrennung", claim.claim)
        self.assertIn("Freiheit", claim.claim)
        prohibited = " ".join(item.prohibited_conclusion for item in result.anti_inferences)
        self.assertIn("incapacitate de desprindere", prohibited)

    def test_zero_s_is_relative_and_partner_bound(self):
        claim = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000022"]
        result = self.evaluate(claim.claim_id, {"s": ("null", 0)})
        self.assertEqual(result.activation_status, ActivationStatus.ACTIVE)
        self.assertIn("Partnerfaktor", claim.claim)
        self.assertTrue(result.anti_inferences)


class Fall40ClinicalRoutingTests(unittest.TestCase):
    def test_preview_protocol_routes_candidate_meanings_but_production_does_not(self):
        series = ProfileSeries(
            (
                profile(
                    {
                        "h": ("positive", 1),
                        "e": ("negative", 0),
                        "hy": ("negative", 0),
                        "d": ("positive", 0),
                        "m": ("negative", 0),
                    }
                ),
            )
        )
        preview = evaluate_clinical_protocol(series)
        production = evaluate_clinical_protocol(series, production=True)

        preview_ids = {item.claim_id for item in preview.profiles[0].interpretation.findings}
        production_ids = {item.claim_id for item in production.profiles[0].interpretation.findings}
        self.assertTrue(
            {
                "IC_SZONDI_PRIMARY_000013",
                "IC_SZONDI_PRIMARY_000014",
                "IC_SZONDI_PRIMARY_000015",
                "IC_SZONDI_PRIMARY_000016",
                "IC_SZONDI_PRIMARY_000017",
                "IC_SZONDI_PRIMARY_000019",
                "IC_SZONDI_PRIMARY_000020",
                "IC_SZONDI_PRIMARY_000021",
            }.issubset(preview_ids)
        )
        self.assertFalse(any(int(item.rsplit("_", 1)[1]) >= 13 for item in production_ids))
        self.assertEqual(preview.profiles[0].interpretation.unresolved, ())


if __name__ == "__main__":
    unittest.main()
