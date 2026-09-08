import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.interpretation import EpistemicClass
from szondi3.interpretation_catalogue import CLAIMS_BY_ID
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


_BASE_SYMBOL = {
    "null": "0",
    "positive": "+",
    "negative": "-",
    "ambivalent": "±",
}


def _reaction(factor, kind="null", *, quantum=0, forced_null=False):
    if kind == "positive":
        sympathetic, unsympathetic = 2 + (2 * quantum), 0
    elif kind == "negative":
        sympathetic, unsympathetic = 0, 2 + (2 * quantum)
    elif kind == "ambivalent":
        sympathetic, unsympathetic = 2, 2
    else:
        sympathetic, unsympathetic = 0, 0
    symbol = "ø" if forced_null else _BASE_SYMBOL[kind] + ("!" * quantum)
    return FactorReaction(
        factor=factor,
        sympathetic=sympathetic,
        unsympathetic=unsympathetic,
        kind=kind,
        symbol=symbol,
        quantum_level=quantum,
        forced_null=forced_null,
    )


def _profile(*, k="null", p="null", k_forced=False, p_forced=False):
    return build_profile(
        _reaction(
            factor,
            k if factor == "k" else p if factor == "p" else "null",
            forced_null=k_forced if factor == "k" else p_forced if factor == "p" else False,
        )
        for factor in FACTORS
    )


def _series_fact(evaluation, key):
    matches = tuple(item for item in evaluation.series_result.facts if item.key == key)
    if len(matches) != 1:
        raise AssertionError(f"Expected exactly one fact for {key}")
    return matches[0]


def _series_finding(evaluation, claim_id):
    matches = tuple(
        item
        for item in evaluation.series_result.interpretation.findings
        if item.claim_id == claim_id
    )
    if len(matches) != 1:
        raise AssertionError(f"Expected exactly one finding for {claim_id}")
    return matches[0]


class SchPolaritySeriesTests(unittest.TestCase):
    def test_positive_and_negative_k_activate_same_egosystole_polarity_relation(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries(
                (
                    _profile(k="positive"),
                    _profile(k="negative"),
                )
            ),
            production=True,
        )

        self.assertEqual(
            _series_fact(evaluation, "series.sch.k_positive_profiles").value,
            (1,),
        )
        self.assertEqual(
            _series_fact(evaluation, "series.sch.k_negative_profiles").value,
            (2,),
        )
        self.assertTrue(
            _series_fact(evaluation, "series.sch.k_opposed_signs_present").value
        )

        finding = _series_finding(evaluation, "IC_SZONDI_PRIMARY_000050")
        self.assertEqual(
            finding.doctrine_ids,
            ("DR_SZ_IA_1956_A_000040", "DR_SZ_IA_1956_A_000048"),
        )
        self.assertEqual(finding.source_ids, ("SZ_IA_1956_A",))
        self.assertIn("aceluiași k-Ich/Egosystole", finding.statement)
        self.assertIn("două Euri incompatibile", finding.statement)
        self.assertIn("personalități scindate", finding.anti_inferences[0])
        self.assertIn("reality testing", finding.anti_inferences[0])
        self.assertIn("Verdrängung", finding.anti_inferences[0])
        self.assertEqual(
            CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000050"].epistemic_class,
            EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER,
        )
        self.assertIsNotNone(
            CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000050"].inference_rationale
        )

    def test_single_k_direction_does_not_activate_bipolar_series_relation(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries(
                (
                    _profile(k="positive"),
                    _profile(k="ambivalent"),
                    _profile(k="positive"),
                )
            ),
            production=True,
        )

        self.assertFalse(
            _series_fact(evaluation, "series.sch.k_opposed_signs_present").value
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000050"
                for item in evaluation.series_result.interpretation.findings
            )
        )

    def test_negative_and_positive_p_activate_egodiastole_relation_without_phase_order(self):
        for profiles in (
            (_profile(p="negative"), _profile(p="positive")),
            (_profile(p="positive"), _profile(p="negative")),
        ):
            with self.subTest(order=tuple(profile.vectors[2].symbols for profile in profiles)):
                evaluation = evaluate_clinical_protocol(
                    ProfileSeries(profiles),
                    production=True,
                )
                self.assertTrue(
                    _series_fact(
                        evaluation,
                        "series.sch.p_opposed_signs_present",
                    ).value
                )
                finding = _series_finding(
                    evaluation,
                    "IC_SZONDI_PRIMARY_000051",
                )
                self.assertEqual(
                    finding.doctrine_ids,
                    (
                        "DR_SZ_IA_1956_A_000040",
                        "DR_SZ_IA_1956_A_000043",
                        "DR_SZ_IA_1956_A_000045",
                    ),
                )
                self.assertIn("Egodiastole/Ich-Erweiterung", finding.statement)
                self.assertIn("nu trebuie tratată ca o contradicție", finding.statement)
                self.assertIn("ordinea testelor", finding.anti_inferences[0])
                self.assertIn("nu este întotdeauna stabilibilă", finding.anti_inferences[0])
                self.assertEqual(
                    CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000051"].epistemic_class,
                    EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER,
                )

    def test_forced_null_is_not_misread_as_an_opposed_k_direction(self):
        evaluation = evaluate_clinical_protocol(
            ProfileSeries(
                (
                    _profile(k="null", k_forced=True),
                    _profile(k="positive"),
                )
            ),
            production=True,
        )

        self.assertEqual(
            _series_fact(evaluation, "series.sch.k_negative_profiles").value,
            (),
        )
        self.assertFalse(
            _series_fact(evaluation, "series.sch.k_opposed_signs_present").value
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000050"
                for item in evaluation.series_result.interpretation.findings
            )
        )
        self.assertEqual(
            evaluation.series_result.calculation("series_indices").state.value,
            "UNRESOLVED",
        )


if __name__ == "__main__":
    unittest.main()
