import unittest

from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from szondi3.clinical_pipeline import AdministeredTestRecord, evaluate_administered_tests
from szondi3.interpretation import EpistemicClass
from szondi3.interpretation_catalogue import CLAIMS_BY_ID
from szondi3.stimuli import SERIES, presentation_rows


def ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def make_foreground(offset):
    choices = []
    for series in SERIES:
        cards = ids(series)
        rotated = cards[offset:] + cards[:offset]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def make_complement(foreground):
    choices = []
    for choice in foreground.series_choices:
        choices.append(
            record_complement(
                choice,
                selected=choice.remaining[:2],
                selected_as="unsympathetic",
            )
        )
    return complete_complement(foreground, choices)


def fact_value(formal, key):
    matches = tuple(item for item in formal.facts if item.key == key)
    if len(matches) != 1:
        raise AssertionError(f"Expected exactly one fact for {key}")
    return matches[0].value


class SuccessiveContrastSchTests(unittest.TestCase):
    def test_exact_complement_that_later_reappears_in_foreground_supports_possible_successive_contrast(self):
        first_foreground = make_foreground(2)  # ordinary Sch ±±
        first_complement = make_complement(first_foreground)  # ordinary E.K.P. Sch 00
        later_foreground = make_foreground(6)  # ordinary foreground Sch 00

        result = evaluate_administered_tests(
            (
                AdministeredTestRecord(first_foreground, first_complement),
                AdministeredTestRecord(later_foreground),
            ),
            production=True,
        )
        formal = result.complement_profiles[0]

        self.assertEqual(
            fact_value(
                formal,
                "protocol.experimental_complement.sch_theoretical_relation",
            ),
            "MATCH",
        )
        self.assertEqual(
            fact_value(
                formal,
                "protocol.experimental_complement.sch_later_foreground_matches",
            ),
            (2,),
        )
        self.assertEqual(
            tuple(item.claim_id for item in formal.interpretation.findings),
            (
                "IC_SZONDI_PRIMARY_000046",
                "IC_SZONDI_PRIMARY_000047",
                "IC_SZONDI_PRIMARY_000049",
            ),
        )

        successive = formal.interpretation.findings[-1]
        self.assertEqual(
            successive.doctrine_ids,
            (
                "DR_SZ_IA_1956_B_000006",
                "DR_SZ_IA_1956_B_000008",
                "DR_SZ_IA_1956_B_000009",
            ),
        )
        self.assertIn("sukzessive Kontrastwirkung", successive.statement)
        self.assertIn("nu dovedește", successive.statement)
        self.assertIn("schimbări globale", successive.anti_inferences[0])
        self.assertIn("Nu presupune cauzalitate", successive.anti_inferences[0])

        definition = CLAIMS_BY_ID["IC_SZONDI_PRIMARY_000049"]
        self.assertEqual(
            definition.epistemic_class,
            EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER,
        )
        self.assertIsNotNone(definition.inference_rationale)
        self.assertIsNotNone(definition.reversal_condition)

        report = result.build_report()
        report_match = tuple(
            item
            for item in report.findings
            if item.scope == "EXPERIMENTAL_COMPLEMENT"
            and item.claim_id == "IC_SZONDI_PRIMARY_000049"
        )
        self.assertEqual(len(report_match), 1)
        self.assertEqual(report_match[0].profile_number, 1)
        self.assertEqual(report.header.profile_count, 2)

    def test_theoretical_match_without_later_same_foreground_sch_does_not_activate_successive_contrast(self):
        first_foreground = make_foreground(2)
        first_complement = make_complement(first_foreground)
        later_foreground = make_foreground(0)  # Sch --, not the E.K.P. 00

        result = evaluate_administered_tests(
            (
                AdministeredTestRecord(first_foreground, first_complement),
                AdministeredTestRecord(later_foreground),
            ),
            production=True,
        )
        formal = result.complement_profiles[0]

        self.assertEqual(
            fact_value(
                formal,
                "protocol.experimental_complement.sch_later_foreground_matches",
            ),
            (),
        )
        self.assertEqual(
            tuple(item.claim_id for item in formal.interpretation.findings),
            ("IC_SZONDI_PRIMARY_000046", "IC_SZONDI_PRIMARY_000047"),
        )

    def test_later_recurrence_of_an_ekp_that_mismatched_thkp_is_not_called_successive_contrast(self):
        first_foreground = make_foreground(0)  # Sch --
        first_complement = make_complement(first_foreground)  # E.K.P. --, Th.K.P. ++
        later_foreground = make_foreground(0)  # repeats observed E.K.P. --

        result = evaluate_administered_tests(
            (
                AdministeredTestRecord(first_foreground, first_complement),
                AdministeredTestRecord(later_foreground),
            ),
            production=True,
        )
        formal = result.complement_profiles[0]

        self.assertEqual(
            fact_value(
                formal,
                "protocol.experimental_complement.sch_theoretical_relation",
            ),
            "MISMATCH",
        )
        self.assertEqual(
            fact_value(
                formal,
                "protocol.experimental_complement.sch_later_foreground_matches",
            ),
            (),
        )
        self.assertEqual(
            tuple(item.claim_id for item in formal.interpretation.findings),
            ("IC_SZONDI_PRIMARY_000046", "IC_SZONDI_PRIMARY_000048"),
        )
        self.assertFalse(
            any(
                item.claim_id == "IC_SZONDI_PRIMARY_000049"
                for item in result.build_report().findings
            )
        )


if __name__ == "__main__":
    unittest.main()
