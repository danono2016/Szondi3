import unittest

from szondi3 import clinical_interpretation, clinical_release
from szondi3 import interpretation_catalogue as historical_catalogue
from szondi3 import interpretation_catalogue_fate_modifiability as current_catalogue


class CatalogueFrontierTests(unittest.TestCase):
    def test_single_public_current_catalogue_frontier_is_000087(self):
        self.assertFalse(historical_catalogue.CURRENT_CATALOGUE)
        self.assertEqual(
            historical_catalogue.CATALOGUE_ROLE,
            "HISTORICAL_BASE_SEGMENT_THROUGH_000070",
        )
        self.assertEqual(
            historical_catalogue.CURRENT_CATALOGUE_MODULE,
            "szondi3.interpretation_catalogue_fate_modifiability",
        )
        self.assertTrue(current_catalogue.CURRENT_CATALOGUE)
        self.assertEqual(
            current_catalogue.CATALOGUE_ROLE,
            "CURRENT_EXECUTABLE_PUBLIC_CATALOGUE",
        )
        self.assertEqual(
            current_catalogue.CATALOGUE_FRONTIER,
            "IC_SZONDI_PRIMARY_000087",
        )
        self.assertEqual(
            current_catalogue.INITIAL_CLAIMS[-1].claim_id,
            "IC_SZONDI_PRIMARY_000087",
        )

        self.assertIs(clinical_interpretation.INITIAL_CLAIMS, current_catalogue.INITIAL_CLAIMS)
        self.assertIs(clinical_interpretation.CLAIMS_BY_ID, current_catalogue.CLAIMS_BY_ID)
        self.assertIs(clinical_release.INITIAL_CLAIMS, current_catalogue.INITIAL_CLAIMS)


if __name__ == "__main__":
    unittest.main()
