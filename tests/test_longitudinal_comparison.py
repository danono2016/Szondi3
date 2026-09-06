import unittest
from dataclasses import replace

from szondi3 import clinical_release
from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.longitudinal_comparison import (
    LongitudinalCaseRef,
    compare_clinical_case_sequence,
    compare_clinical_cases,
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


def _complement(foreground):
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


def _run(profile_count=8, start_offset=0, complement_at=None):
    foregrounds = tuple(
        _foreground(start_offset + index) for index in range(profile_count)
    )
    records = tuple(
        AdministeredTestRecord(
            foreground,
            _complement(foreground) if number == complement_at else None,
        )
        for number, foreground in enumerate(foregrounds, start=1)
    )
    return run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


def _ref(case_id, run):
    return LongitudinalCaseRef(case_id=case_id, run=run)


def _with_manifest(run, **changes):
    manifest = replace(run.release.manifest, **changes)
    return replace(run, release=replace(run.release, manifest=manifest))


class LongitudinalComparisonTests(unittest.TestCase):
    def test_identical_run_is_structurally_identical_without_new_meaning(self):
        run = _run()
        result = compare_clinical_cases(_ref("A", run), _ref("B", run))

        self.assertEqual(result.comparability_issues, ())
        self.assertTrue(all(item.is_identical for item in result.header_diffs))
        self.assertTrue(all(item.sequences_identical for item in result.factor_comparisons))
        self.assertTrue(all(item.base_sequences_identical for item in result.factor_comparisons))
        self.assertTrue(all(item.quantum_total_diff.is_identical for item in result.factor_comparisons))
        self.assertTrue(all(item.is_identical for item in result.vector_comparisons))
        self.assertTrue(all(item.is_identical for item in result.series_calculation_diffs))
        self.assertTrue(all(not item.state_changed for item in result.claim_comparisons))
        self.assertEqual(result.unresolved_or_blocked_a, result.unresolved_or_blocked_b)

    def test_ordered_series_difference_is_exposed_without_synthetic_change_score(self):
        run_a = _run(start_offset=0)
        run_b = _run(start_offset=1)
        result = compare_clinical_cases(_ref("A", run_a), _ref("B", run_b))

        self.assertEqual(result.comparability_issues, ())
        self.assertTrue(
            any(not item.sequences_identical for item in result.factor_comparisons)
            or any(not item.is_identical for item in result.vector_comparisons)
        )
        self.assertFalse(hasattr(result, "change_score"))
        self.assertFalse(hasattr(result, "clinical_meaning"))

    def test_claim_occurrences_are_not_collapsed_by_claim_id(self):
        run = _run()
        result = compare_clinical_cases(_ref("A", run), _ref("B", run))

        evaluation = run.evaluation.clinical_evaluation
        expected = len(run.report.findings)
        expected += sum(len(profile.interpretation.suppressed) for profile in evaluation.profiles)
        expected += len(evaluation.series_result.interpretation.suppressed)
        expected += sum(
            len(item.interpretation.suppressed)
            for item in run.evaluation.complement_profiles
        )
        self.assertEqual(len(result.claim_comparisons), expected)
        keys = tuple(item.key for item in result.claim_comparisons)
        self.assertEqual(len(keys), len(set(keys)))

    def test_profile_count_mismatch_is_reported_but_comparison_continues(self):
        result = compare_clinical_cases(
            _ref("A", _run(profile_count=8)),
            _ref("B", _run(profile_count=10)),
        )

        self.assertIn(
            "PROFILE_COUNT_MISMATCH",
            {item.code for item in result.comparability_issues},
        )
        self.assertTrue(result.factor_comparisons)
        self.assertTrue(result.vector_comparisons)
        self.assertTrue(result.series_calculation_diffs)

    def test_experimental_complement_asymmetry_is_explicit_and_stays_separate(self):
        result = compare_clinical_cases(
            _ref("A", _run(complement_at=3)),
            _ref("B", _run()),
        )

        self.assertTrue(result.experimental_complement_present_a)
        self.assertFalse(result.experimental_complement_present_b)
        self.assertIn(
            "EXPERIMENTAL_COMPLEMENT_ASYMMETRY",
            {item.code for item in result.comparability_issues},
        )
        self.assertTrue(
            any(
                item.key.scope == "EXPERIMENTAL_COMPLEMENT"
                for item in result.claim_comparisons
            )
        )

    def test_doctrine_provenance_mismatch_is_visible_without_blocking_diff(self):
        run_a = _run(start_offset=0)
        run_b = _run(start_offset=1)
        changed = _with_manifest(
            run_b,
            doctrine_snapshot_id="different-doctrine-snapshot",
            doctrine_registry_sha256="f" * 64,
        )

        result = compare_clinical_cases(_ref("A", run_a), _ref("B", changed))
        issues = {item.code: item.detail for item in result.comparability_issues}

        self.assertIn("DOCTRINE_SNAPSHOT_MISMATCH", issues)
        self.assertIn("doctrine_snapshot_id", issues["DOCTRINE_SNAPSHOT_MISMATCH"])
        self.assertIn("doctrine_registry_sha256", issues["DOCTRINE_SNAPSHOT_MISMATCH"])
        self.assertTrue(result.factor_comparisons)
        self.assertTrue(result.vector_comparisons)
        self.assertTrue(result.series_calculation_diffs)

    def test_runtime_and_p2b_provenance_mismatches_are_separate_codes(self):
        run = _run()
        changed = _with_manifest(
            run,
            git_commit_sha="0" * 40,
            p2b_release_id="different-p2b-release",
            p2b_catalogue_sha256="e" * 64,
        )

        result = compare_clinical_cases(_ref("A", run), _ref("B", changed))
        codes = {item.code for item in result.comparability_issues}

        self.assertIn("RUNTIME_VERSION_MISMATCH", codes)
        self.assertIn("P2B_RELEASE_MISMATCH", codes)

    def test_missing_release_manifest_is_visible_without_blocking_diff(self):
        run = _run()
        missing_manifest = replace(
            run,
            release=replace(run.release, manifest=None),
        )

        result = compare_clinical_cases(_ref("A", run), _ref("B", missing_manifest))

        self.assertIn(
            "RELEASE_MANIFEST_MISSING",
            {item.code for item in result.comparability_issues},
        )
        self.assertTrue(result.factor_comparisons)
        self.assertTrue(result.claim_comparisons)

    def test_tampered_case_run_fails_closed_at_existing_integrity_boundary(self):
        run = _run()
        tampered_report = replace(run.report, findings=())
        tampered_packet = replace(run.evidence_packet, report=tampered_report)
        tampered_run = replace(run, evidence_packet=tampered_packet)

        with self.assertRaises(ValueError):
            compare_clinical_cases(_ref("A", tampered_run), _ref("B", run))

    def test_sequence_compares_only_adjacent_supplied_cases(self):
        a = _ref("A", _run(start_offset=0))
        b = _ref("B", _run(start_offset=1))
        c = _ref("C", _run(start_offset=2))

        result = compare_clinical_case_sequence((a, b, c))
        self.assertEqual(len(result), 2)
        self.assertEqual((result[0].case_id_a, result[0].case_id_b), ("A", "B"))
        self.assertEqual((result[1].case_id_a, result[1].case_id_b), ("B", "C"))

        with self.assertRaises(ValueError):
            compare_clinical_case_sequence((a,))

    def test_external_case_identity_is_required_without_mutating_clinical_case_run(self):
        run = _run()
        with self.assertRaises(ValueError):
            LongitudinalCaseRef(case_id="", run=run)
        with self.assertRaises(TypeError):
            LongitudinalCaseRef(case_id="A", run=object())


if __name__ == "__main__":
    unittest.main()
