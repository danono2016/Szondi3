import unittest

from szondi3 import interpretation_catalogue_base as historical_base
from szondi3 import interpretation_catalogue_fate_modifiability as current_catalogue
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import (
    ActivationStatus,
    Fact,
    LifecycleStatus,
    evaluate_catalogue,
)
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


CLAIM_021 = "IC_SZONDI_PRIMARY_000021"
CLAIM_081 = "IC_SZONDI_PRIMARY_000081"


def _facts(*, k_quantum=0, p_quantum=0):
    return (
        Fact("profile.vector.Sch.base_symbols", ("+", "±")),
        Fact("profile.factor.k.quantum_level", k_quantum),
        Fact("profile.factor.p.quantum_level", p_quantum),
    )


def _reaction(factor, symbol="0", quantum=0):
    kind = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}[symbol]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=symbol + ("!" * quantum),
        quantum_level=quantum,
    )


def _profile(*, k_quantum=0, p_quantum=0):
    symbols = {"k": "+", "p": "±"}
    quantums = {"k": k_quantum, "p": p_quantum}
    return build_profile(
        _reaction(factor, symbols.get(factor, "0"), quantums.get(factor, 0))
        for factor in FACTORS
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

    def test_clinical_protocol_ordinary_profile_surfaces_081_but_not_superseded_021(self):
        result = evaluate_clinical_protocol(
            ProfileSeries((_profile(),)),
            production=True,
        )
        finding_ids = {
            finding.claim_id for finding in result.profiles[0].interpretation.findings
        }

        self.assertNotIn(CLAIM_021, finding_ids)
        self.assertIn(CLAIM_081, finding_ids)

    def test_clinical_protocol_overpressure_surfaces_neither_021_nor_081(self):
        for k_quantum, p_quantum in ((1, 0), (0, 1)):
            with self.subTest(k_quantum=k_quantum, p_quantum=p_quantum):
                result = evaluate_clinical_protocol(
                    ProfileSeries((
                        _profile(k_quantum=k_quantum, p_quantum=p_quantum),
                    )),
                    production=True,
                )
                finding_ids = {
                    finding.claim_id
                    for finding in result.profiles[0].interpretation.findings
                }

                self.assertNotIn(CLAIM_021, finding_ids)
                self.assertNotIn(CLAIM_081, finding_ids)


if __name__ == "__main__":
    unittest.main()
