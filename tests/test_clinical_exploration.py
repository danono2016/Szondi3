import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_exploration import explore_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.stimuli import SERIES, presentation_rows


def _card_ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def _foreground(offset):
    choices = []
    for series in SERIES:
        cards = _card_ids(series)
        rotated = cards[offset:] + cards[:offset]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


class ClinicalExplorationTests(unittest.TestCase):
    def _run(self):
        records = tuple(
            AdministeredTestRecord(_foreground(offset)) for offset in range(8)
        )
        return run_clinical_case(
            records,
            git_commit_sha=clinical_release._verified_checkout_sha(),
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )

    def test_profile_exploration_groups_only_existing_profile_outputs(self):
        run = self._run()
        exploration = explore_clinical_case(run)
        profile = exploration.profile(1)

        self.assertEqual(profile.observation, run.report.observations[0])
        self.assertEqual(
            profile.facts,
            run.evaluation.clinical_evaluation.profiles[0].facts,
        )
        self.assertEqual(
            profile.findings,
            tuple(
                item
                for item in run.report.findings
                if item.scope == "PROFILE" and item.profile_number == 1
            ),
        )
        self.assertTrue(profile.suppressed)
        self.assertTrue(all(item.activation_status.value == "INACTIVE" for item in profile.suppressed))

    def test_series_exploration_preserves_calculations_facts_and_unresolved(self):
        run = self._run()
        exploration = explore_clinical_case(run)
        series = exploration.series()

        self.assertEqual(series.calculations, run.report.calculations)
        self.assertEqual(
            series.facts,
            run.evaluation.clinical_evaluation.series_result.facts,
        )
        self.assertEqual(
            series.findings,
            tuple(item for item in run.report.findings if item.scope == "SERIES"),
        )
        self.assertEqual(
            series.uncertainties,
            tuple(item for item in run.report.uncertainties if item.scope == "SERIES"),
        )

    def test_active_finding_traces_exact_facts_and_canonical_doctrine(self):
        run = self._run()
        exploration = explore_clinical_case(run)
        finding = next(
            item
            for item in run.report.findings
            if item.scope == "PROFILE" and item.profile_number == 1
        )

        trace = exploration.trace_finding(
            finding.claim_id,
            scope="PROFILE",
            profile_number=1,
        )
        self.assertEqual(trace.finding, finding)
        self.assertEqual(
            tuple(item.fact_id for item in trace.support_facts),
            finding.support_fact_ids,
        )
        self.assertEqual(
            tuple(item.doctrine_id for item in trace.doctrine_evidence),
            finding.doctrine_ids,
        )
        self.assertEqual(trace.finding.anti_inference_ids, finding.anti_inference_ids)
        self.assertEqual(trace.finding.anti_inferences, finding.anti_inferences)

    def test_trace_fails_closed_on_wrong_scope_or_missing_active_finding(self):
        run = self._run()
        exploration = explore_clinical_case(run)
        profile_finding = next(
            item
            for item in run.report.findings
            if item.scope == "PROFILE" and item.profile_number == 1
        )

        with self.assertRaises(KeyError):
            exploration.trace_finding(profile_finding.claim_id, scope="SERIES")
        with self.assertRaises(ValueError):
            exploration.trace_finding(
                profile_finding.claim_id,
                scope="PROFILE",
                profile_number=None,
            )
        with self.assertRaises(KeyError):
            exploration.profile(0)


if __name__ == "__main__":
    unittest.main()
