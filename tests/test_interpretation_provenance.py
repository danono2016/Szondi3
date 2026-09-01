import inspect
import json
import unittest
from pathlib import Path

from szondi3 import interpretation_catalogue
from szondi3.interpretation import AssertionMode
from szondi3.interpretation_catalogue import INITIAL_CLAIMS


_ADMITTED_DOCTRINE_REVIEW_STATUSES = {
    "SOURCE_VERIFIED",
    "CLINICIAN_REVIEWED",
    "ACCEPTED",
}

# P2B AssertionMode currently combines two different dimensions from the data
# contract: epistemic force (CATEGORICAL/PROBABLE/POSSIBLE/HYPOTHESIS) and
# logical or functional form (DEFINITIONAL/CONDITIONAL/WARNING/LIMITATION).
# Only the former can be compared mechanically with P2A assertionStrength.
# Treating CONDITIONAL as a strength would falsely turn an exact structural
# condition into a stronger epistemic assertion.
_EPISTEMIC_P2B_MODES = {
    AssertionMode.HYPOTHESIS,
    AssertionMode.POSSIBLE,
    AssertionMode.PROBABLE,
    AssertionMode.CATEGORICAL,
}

_WEAK_EPISTEMIC_MODES = {
    AssertionMode.HYPOTHESIS,
    AssertionMode.POSSIBLE,
}

_ALLOWED_EPISTEMIC_P2B_MODES_BY_SOURCE_STRENGTH = {
    # HYPOTHESIS/ASSUMPTION are schema-supported legacy strengths. They are
    # retained here until the pre-existing P2A schema/spec vocabulary drift is
    # resolved separately; neither can authorize PROBABLE or CATEGORICAL.
    "HYPOTHESIS": _WEAK_EPISTEMIC_MODES,
    "ASSUMPTION": _WEAK_EPISTEMIC_MODES,
    "POSSIBILITY": _WEAK_EPISTEMIC_MODES,
    "SUSPICION_INDICATION": _WEAK_EPISTEMIC_MODES,
    "TENDENCY": _WEAK_EPISTEMIC_MODES,
    "PROBABILITY": _WEAK_EPISTEMIC_MODES | {AssertionMode.PROBABLE},
    "GENERALIZATION": _WEAK_EPISTEMIC_MODES | {AssertionMode.PROBABLE},
    "ASSERTION": _EPISTEMIC_P2B_MODES,
    "DEFINITIONAL": _EPISTEMIC_P2B_MODES,
    "UNCLEAR_SOURCE_STRENGTH": {AssertionMode.HYPOTHESIS},
}


def _registry_index():
    registry = Path(__file__).resolve().parents[1] / "doctrine" / "registry"
    doctrine = {}
    for path in registry.glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            doctrine_id = item.get("doctrineId")
            if doctrine_id:
                if doctrine_id in doctrine:
                    raise AssertionError(f"Duplicate doctrineId in test index: {doctrine_id}")
                doctrine[doctrine_id] = item
    return doctrine


class InterpretationProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doctrine = _registry_index()

    def test_every_initial_claim_resolves_to_admitted_reviewed_doctrine(self):
        for claim in INITIAL_CLAIMS:
            for doctrine_id in claim.doctrine_ids:
                with self.subTest(claim=claim.claim_id, doctrine=doctrine_id):
                    self.assertIn(doctrine_id, self.doctrine)
                    item = self.doctrine[doctrine_id]
                    self.assertEqual(item["sourceLayer"], claim.source_layer)
                    self.assertIn(
                        item["reviewStatus"],
                        _ADMITTED_DOCTRINE_REVIEW_STATUSES,
                    )
                    self.assertTrue(item.get("sourceAnchors"))

    def test_claim_source_ids_equal_their_linked_doctrine_sources(self):
        for claim in INITIAL_CLAIMS:
            expected_sources = {
                self.doctrine[doctrine_id]["sourceId"]
                for doctrine_id in claim.doctrine_ids
            }
            with self.subTest(claim=claim.claim_id):
                self.assertEqual(len(claim.source_ids), len(set(claim.source_ids)))
                self.assertEqual(set(claim.source_ids), expected_sources)

    def test_epistemic_claim_strength_never_exceeds_all_linked_source_strengths(self):
        for claim in INITIAL_CLAIMS:
            strengths = tuple(
                self.doctrine[doctrine_id]["assertionStrength"]
                for doctrine_id in claim.doctrine_ids
            )
            unknown = tuple(
                strength
                for strength in strengths
                if strength not in _ALLOWED_EPISTEMIC_P2B_MODES_BY_SOURCE_STRENGTH
            )
            with self.subTest(claim=claim.claim_id, strengths=strengths):
                self.assertEqual(unknown, ())
                if claim.assertion_mode not in _EPISTEMIC_P2B_MODES:
                    continue
                self.assertTrue(
                    any(
                        claim.assertion_mode
                        in _ALLOWED_EPISTEMIC_P2B_MODES_BY_SOURCE_STRENGTH[strength]
                        for strength in strengths
                    ),
                    msg=(
                        f"{claim.claim_id} uses epistemic mode "
                        f"{claim.assertion_mode.value}, but linked doctrine strengths "
                        f"{strengths!r} do not authorize that force"
                    ),
                )

    def test_conditional_is_logical_form_not_epistemic_strength(self):
        self.assertNotIn(AssertionMode.CONDITIONAL, _EPISTEMIC_P2B_MODES)

    def test_current_catalogue_helper_requires_explicit_lifecycle_status(self):
        parameter = inspect.signature(interpretation_catalogue._claim).parameters["status"]
        self.assertIs(parameter.default, inspect.Parameter.empty)
        self.assertIs(parameter.kind, inspect.Parameter.KEYWORD_ONLY)


if __name__ == "__main__":
    unittest.main()
