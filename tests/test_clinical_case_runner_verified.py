import unittest

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_case_runner import run_clinical_case_from_verified_checkout
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.stimuli import SERIES, presentation_rows


def _record():
    choices = []
    for series in SERIES:
        cards = [card.card_id for row in presentation_rows(series) for card in row]
        choices.append(record_foreground(series, cards[:2], cards[2:4]))
    return AdministeredTestRecord(complete_foreground(choices))


class VerifiedCheckoutClinicalCaseRunnerTests(unittest.TestCase):
    def test_product_runner_uses_verified_checkout_without_caller_supplied_sha(self):
        run = run_clinical_case_from_verified_checkout(
            (_record(),),
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )
        self.assertEqual(
            run.release.manifest.git_commit_sha,
            clinical_release._verified_checkout_sha(),
        )
        self.assertEqual(run.report.header.profile_count, 1)
        self.assertTrue(run.report.header.production_mode)


if __name__ == "__main__":
    unittest.main()
