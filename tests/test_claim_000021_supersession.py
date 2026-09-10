import unittest

from szondi3 import interpretation_catalogue_base as historical_base
from szondi3 import interpretation_catalogue_fate_modifiability as current_catalogue
from szondi3.interpretation import (
    ActivationStatus,
    Fact,
    LifecycleStatus,
    evaluate_catalogue,
)


CLAIM_021 = "IC_SZONDI_PRIMARY_000021"
CLAIM_081 = "IC_SZONDI_PRIMARY_000081"


def _facts(*, k_quantum=0, p_quantum=0):
    return (
        Fact("profile.vector.Sch.base_symbols", ("+", "±")),
        Fact("profile.factor.k.quantum_level", k_quantum),
        Fact("profile.factor.p.quantum_level", p_quantum),
    )


class Claim000021SupersessionTests(unittest.TestCase):
    def test_historical_claim_021_remains_approved(self):
        historical = next(
            claim for claim in historical_base.INITIAL_CLAIMS if claim.claim_id == CLAIM_021
        )
        self.assertIs(historical.status, LifecycleStatus.APPROVED)

    def test_current_frontier_projects_claim_021_as_superseded_without_advancing_frontier(self):
        self.assertIs(
            current_catalogue.CLAIMS_BY_ID[CLAIM_021].status,
            LifecycleStatus.SUPERSEDED,
        )
        self.assertEqual(
            current_catalogue.CATALOGUE_FRONTIER,
            "IC_SZONDI_PRIMARY_000087",
        )
        self.assertEqual(
            current_catalogue.INITIAL_CLAIMS[-1].claim_id,
            "IC_SZONDI_PRIMARY_000087",
        )

    def test_ordinary_sch_plus_ambivalent_executes_only_precise_claim_081(self):
        records = evaluate_catalogue(
            current_catalogue.INITIAL_CLAIMS,
            _facts(),
            production=True,
        )
        by_id = {record.claim_id: record for record in records}

        self.assertNotIn(CLAIM_021, by_id)
        self.assertIn(CLAIM_081, by_id)
        self.assertIs(by_id[CLAIM_081].activation_status, ActivationStatus.ACTIVE)

    def test_overpressure_executes_neither_claim_021_nor_claim_081(self):
        for k_quantum, p_quantum in ((1, 0), (0, 1)):
            with self.subTest(k_quantum=k_quantum, p_quantum=p_quantum):
                records = evaluate_catalogue(
                    current_catalogue.INITIAL_CLAIMS,
                    _facts(k_quantum=k_quantum, p_quantum=p_quantum),
                    production=True,
                )
                by_id = {record.claim_id: record for record in records}

                self.assertNotIn(CLAIM_021, by_id)
                self.assertIn(CLAIM_081, by_id)
                self.assertIs(
                    by_id[CLAIM_081].activation_status,
                    ActivationStatus.INACTIVE,
                )


if __name__ == "__main__":
    unittest.main()
