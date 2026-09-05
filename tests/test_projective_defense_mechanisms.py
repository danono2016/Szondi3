import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.stimuli import FACTORS


def _reaction(factor, kind="null", quantum=0):
    base = {"null": "0", "positive": "+", "negative": "-", "ambivalent": "±"}[kind]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=kind,
        symbol=base + ("!" * quantum),
        quantum_level=quantum,
    )


def _profile(overrides=None):
    overrides = overrides or {}
    return build_profile(
        _reaction(factor, *overrides.get(factor, ("null", 0)))
        for factor in FACTORS
    )


def _findings(overrides):
    result = evaluate_clinical_protocol(ProfileSeries((_profile(overrides),)), production=True)
    return {item.claim_id: item for item in result.profiles[0].interpretation.findings}


class ProjectiveDefenseMechanismTests(unittest.TestCase):
    def test_table_10_exact_projective_family_routes_without_collapse(self):
        cases = (
            ({"p": ("negative", 0)}, "IC_SZONDI_PRIMARY_000066", "totale Projektion"),
            ({"p": ("ambivalent", 0)}, "IC_SZONDI_PRIMARY_000067", "inflative Projektion"),
            ({"k": ("positive", 0), "p": ("negative", 0)}, "IC_SZONDI_PRIMARY_000068", "Introprojektion"),
            ({"k": ("ambivalent", 0), "p": ("negative", 0)}, "IC_SZONDI_PRIMARY_000069", "Fugue / Flucht"),
            ({"k": ("negative", 0), "p": ("ambivalent", 0)}, "IC_SZONDI_PRIMARY_000024", "Entfremdung"),
        )
        exact_ids = {
            "IC_SZONDI_PRIMARY_000066",
            "IC_SZONDI_PRIMARY_000067",
            "IC_SZONDI_PRIMARY_000068",
            "IC_SZONDI_PRIMARY_000069",
            "IC_SZONDI_PRIMARY_000024",
        }
        for overrides, expected_id, term in cases:
            with self.subTest(overrides=overrides):
                findings = _findings(overrides)
                self.assertIn(expected_id, findings)
                self.assertIn(term, findings[expected_id].statement)
                self.assertEqual(exact_ids.intersection(findings), {expected_id})

    def test_new_table_10_relations_are_bound_to_ia_b_projective_taxonomy(self):
        for overrides, claim_id in (
            ({"p": ("negative", 0)}, "IC_SZONDI_PRIMARY_000066"),
            ({"p": ("ambivalent", 0)}, "IC_SZONDI_PRIMARY_000067"),
            ({"k": ("positive", 0), "p": ("negative", 0)}, "IC_SZONDI_PRIMARY_000068"),
            ({"k": ("ambivalent", 0), "p": ("negative", 0)}, "IC_SZONDI_PRIMARY_000069"),
        ):
            finding = _findings(overrides)[claim_id]
            self.assertEqual(finding.doctrine_ids, ("DR_SZ_IA_1956_B_000017",))
            self.assertEqual(finding.source_ids, ("SZ_IA_1956_B",))

    def test_quantum_overpressure_is_not_auto_extended(self):
        for overrides in (
            {"p": ("negative", 1)},
            {"p": ("ambivalent", 1)},
            {"k": ("positive", 1), "p": ("negative", 0)},
            {"k": ("ambivalent", 0), "p": ("negative", 1)},
        ):
            with self.subTest(overrides=overrides):
                findings = _findings(overrides)
                for claim_id in (
                    "IC_SZONDI_PRIMARY_000066",
                    "IC_SZONDI_PRIMARY_000067",
                    "IC_SZONDI_PRIMARY_000068",
                    "IC_SZONDI_PRIMARY_000069",
                ):
                    self.assertNotIn(claim_id, findings)


if __name__ == "__main__":
    unittest.main()
