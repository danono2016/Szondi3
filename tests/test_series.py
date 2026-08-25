import unittest
from fractions import Fraction

from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import (
    ProfileSeries,
    factor_tension_degrees,
    latency_proportions,
    series_indices,
    ten_base_count,
    vector_tension_differences,
)
from szondi3.stimuli import FACTORS


TABLE_13 = {
    3: {1: 3, 2: 7, 3: 10},
    4: {1: 2, 2: 5, 3: 7, 4: 10},
    5: {1: 2, 2: 4, 3: 6, 4: 8, 5: 10},
    6: {1: 2, 2: 3, 3: 5, 4: 7, 5: 8, 6: 10},
    7: {1: 1, 2: 3, 3: 4, 4: 6, 5: 7, 6: 9, 7: 10},
    8: {1: 1, 2: 2, 3: 4, 4: 5, 5: 6, 6: 7, 7: 9, 8: 10},
    9: {1: 1, 2: 2, 3: 3, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10},
}


REACTION_FIXTURES = {
    "null": (0, 0, "0"),
    "positive": (2, 0, "+"),
    "negative": (0, 2, "-"),
    "ambivalent": (2, 2, "±"),
}


def profile_with_kinds(kinds):
    if len(kinds) != len(FACTORS):
        raise ValueError("A test profile needs eight reaction kinds")
    reactions = []
    for factor, kind in zip(FACTORS, kinds):
        sympathetic, unsympathetic, symbol = REACTION_FIXTURES[kind]
        reactions.append(
            FactorReaction(
                factor=factor,
                sympathetic=sympathetic,
                unsympathetic=unsympathetic,
                kind=kind,
                symbol=symbol,
                quantum_level=0,
            )
        )
    return build_profile(reactions)


def null_profile():
    return profile_with_kinds(["null"] * 8)


def series_from_factor_counts(null_counts, ambivalent_counts, profile_count=10):
    profiles = []
    for profile_index in range(profile_count):
        kinds = []
        for factor_index in range(len(FACTORS)):
            if profile_index < null_counts[factor_index]:
                kinds.append("null")
            elif profile_index < null_counts[factor_index] + ambivalent_counts[factor_index]:
                kinds.append("ambivalent")
            else:
                kinds.append("positive")
        profiles.append(profile_with_kinds(kinds))
    return ProfileSeries(tuple(profiles))


class ProfileSeriesTests(unittest.TestCase):
    def test_series_preserves_order_and_accepts_one_to_ten_profiles(self):
        profile = null_profile()
        for count in range(1, 11):
            with self.subTest(count=count):
                series = ProfileSeries(tuple(profile for _ in range(count)))
                self.assertEqual(len(series.profiles), count)
                self.assertEqual(series.profile_count, count)
                self.assertEqual(series.is_ten_series, count == 10)
                self.assertEqual(series.supports_linnaeus_evaluation, count >= 3)

    def test_series_rejects_empty_or_more_than_ten_profiles(self):
        profile = null_profile()
        with self.assertRaises(ValueError):
            ProfileSeries(())
        with self.assertRaises(ValueError):
            ProfileSeries(tuple(profile for _ in range(11)))

    def test_table_13_all_source_entries(self):
        for profile_count, row in TABLE_13.items():
            for observed_count, expected in row.items():
                with self.subTest(profile_count=profile_count, observed_count=observed_count):
                    self.assertEqual(ten_base_count(profile_count, observed_count), expected)

    def test_zero_and_full_ten_series_are_identity_cases(self):
        for profile_count in range(3, 11):
            self.assertEqual(ten_base_count(profile_count, 0), 0)
        for observed_count in range(0, 11):
            self.assertEqual(ten_base_count(10, observed_count), observed_count)

    def test_ten_base_conversion_fails_outside_source_domain(self):
        invalid = [(2, 1), (11, 1), (3, -1), (3, 4), (10, 11)]
        for profile_count, observed_count in invalid:
            with self.subTest(profile_count=profile_count, observed_count=observed_count):
                with self.assertRaises(ValueError):
                    ten_base_count(profile_count, observed_count)

    def test_tspqu_preserves_exact_source_ratio(self):
        # Lehrbuch case: Sigma 0 = 11, Sigma ± = 3; source prints TspQu = 3.6.
        # The engine preserves 11/3 exactly and leaves decimal presentation downstream.
        kinds = ["null"] * 11 + ["ambivalent"] * 3 + ["positive"] * 66
        profiles = tuple(profile_with_kinds(kinds[i:i + 8]) for i in range(0, 80, 8))
        measures = series_indices(ProfileSeries(profiles))

        self.assertEqual(measures.null_reactions, 11)
        self.assertEqual(measures.ambivalent_reactions, 3)
        self.assertEqual(measures.total_factor_reactions, 80)
        self.assertEqual(measures.tendenzspannungsquotient, Fraction(11, 3))
        self.assertEqual(measures.symptom_percentage, Fraction(35, 2))

    def test_source_symptom_percentage_formula_is_exact(self):
        # Lehrbuch example: 33 symptom reactions of 80 are displayed as 41%.
        # The exact formal value is 41.25%, preserved here without inventing a rounding rule.
        kinds = ["null"] * 20 + ["ambivalent"] * 13 + ["positive"] * 47
        profiles = tuple(profile_with_kinds(kinds[i:i + 8]) for i in range(0, 80, 8))
        measures = series_indices(ProfileSeries(profiles))
        self.assertEqual(measures.symptom_reactions, 33)
        self.assertEqual(measures.symptom_percentage, Fraction(165, 4))

    def test_tspqu_is_explicitly_undefined_when_no_ambivalent_reaction_exists(self):
        profile = profile_with_kinds(["positive"] * 8)
        measures = series_indices(ProfileSeries((profile, profile, profile)))
        self.assertEqual(measures.null_reactions, 0)
        self.assertEqual(measures.ambivalent_reactions, 0)
        self.assertIsNone(measures.tendenzspannungsquotient)
        self.assertEqual(measures.symptom_percentage, Fraction(0, 1))

    def test_forced_null_does_not_silently_enter_series_indices(self):
        reactions = []
        for index, factor in enumerate(FACTORS):
            reactions.append(
                FactorReaction(
                    factor=factor,
                    sympathetic=0,
                    unsympathetic=0,
                    kind="null",
                    symbol="ø" if index == 0 else "0",
                    quantum_level=0,
                    forced_null=index == 0,
                )
            )
        profile = build_profile(reactions)
        with self.assertRaises(ValueError):
            series_indices(ProfileSeries((profile,)))

    def test_factorial_tspg_matches_lehrbuch_case_11(self):
        # Fall 11: Sigma0 = [0,0,4,1,5,0,5,4]
        #          Sigma± = [2,1,0,1,0,4,0,4]
        #          TspG   = [2,1,4,2,5,4,5,8]
        series = series_from_factor_counts(
            null_counts=(0, 0, 4, 1, 5, 0, 5, 4),
            ambivalent_counts=(2, 1, 0, 1, 0, 4, 0, 4),
        )
        degrees = factor_tension_degrees(series)

        self.assertEqual(tuple(item.factor for item in degrees), FACTORS)
        self.assertEqual(tuple(item.null_reactions for item in degrees), (0, 0, 4, 1, 5, 0, 5, 4))
        self.assertEqual(tuple(item.ambivalent_reactions for item in degrees), (2, 1, 0, 1, 0, 4, 0, 4))
        self.assertEqual(tuple(item.degree for item in degrees), (2, 1, 4, 2, 5, 4, 5, 8))

    def test_factorial_tspg_rejects_forced_null(self):
        reactions = []
        for index, factor in enumerate(FACTORS):
            reactions.append(
                FactorReaction(
                    factor=factor,
                    sympathetic=0,
                    unsympathetic=0,
                    kind="null",
                    symbol="ø" if index == 0 else "0",
                    quantum_level=0,
                    forced_null=index == 0,
                )
            )
        with self.assertRaises(ValueError):
            factor_tension_degrees(ProfileSeries((build_profile(reactions),)))

    def test_vector_tspd_uses_smaller_tspg_factor_as_index(self):
        series = series_from_factor_counts(
            null_counts=(9, 2, 5, 5, 4, 1, 0, 0),
            ambivalent_counts=(0, 0, 0, 0, 0, 0, 0, 0),
        )
        differences = {item.vector: item for item in vector_tension_differences(series)}

        self.assertEqual(differences["S"].magnitude, 7)
        self.assertEqual(differences["S"].lower_tension_factor, "s")
        self.assertEqual(differences["S"].designation, "Ss")
        self.assertEqual(differences["Sch"].magnitude, 3)
        self.assertEqual(differences["Sch"].designation, "Schp")

        self.assertEqual(differences["P"].magnitude, 0)
        self.assertIsNone(differences["P"].lower_tension_factor)
        self.assertIsNone(differences["P"].designation)
        self.assertEqual(differences["C"].magnitude, 0)
        self.assertIsNone(differences["C"].lower_tension_factor)

    def test_vector_tspd_direction_reverses_with_factor_degrees(self):
        series = series_from_factor_counts(
            null_counts=(2, 9, 0, 0, 0, 0, 0, 0),
            ambivalent_counts=(0, 0, 0, 0, 0, 0, 0, 0),
        )
        s_difference = vector_tension_differences(series)[0]
        self.assertEqual(s_difference.magnitude, 7)
        self.assertEqual(s_difference.lower_tension_factor, "h")
        self.assertEqual(s_difference.designation, "Sh")

    def test_vector_tspd_matches_lehrbuch_fall_18_raw_degrees(self):
        # Fall 18 raw factorial TspG: h=1,s=0,e=2,hy=2,k=5,p=4,d=3,m=3.
        series = series_from_factor_counts(
            null_counts=(0, 0, 2, 1, 3, 2, 3, 1),
            ambivalent_counts=(1, 0, 0, 1, 2, 2, 0, 2),
            profile_count=6,
        )
        differences = vector_tension_differences(series)

        self.assertEqual(tuple(item.vector for item in differences), ("S", "P", "Sch", "C"))
        self.assertEqual(tuple(item.magnitude for item in differences), (1, 0, 1, 0))
        self.assertEqual(tuple(item.designation for item in differences), ("Ss", None, "Schp", None))
        self.assertEqual(differences[1].degrees, (2, 2))
        self.assertEqual(differences[3].degrees, (3, 3))

    def test_latency_proportions_preserve_fall_18_ties(self):
        series = series_from_factor_counts(
            null_counts=(0, 0, 2, 1, 3, 2, 3, 1),
            ambivalent_counts=(1, 0, 0, 1, 2, 2, 0, 2),
            profile_count=6,
        )
        levels = latency_proportions(series)

        self.assertEqual(tuple(level.magnitude for level in levels), (1, 0))
        self.assertEqual(tuple(item.vector for item in levels[0].differences), ("S", "Sch"))
        self.assertEqual(tuple(item.designation for item in levels[0].differences), ("Ss", "Schp"))
        self.assertEqual(tuple(item.vector for item in levels[1].differences), ("P", "C"))
        self.assertEqual(tuple(item.designation for item in levels[1].differences), (None, None))

    def test_latency_proportions_sort_without_breaking_equalities(self):
        series = series_from_factor_counts(
            null_counts=(9, 2, 5, 5, 4, 1, 8, 6),
            ambivalent_counts=(0, 0, 0, 0, 0, 0, 0, 0),
        )
        levels = latency_proportions(series)
        self.assertEqual(tuple(level.magnitude for level in levels), (7, 3, 2, 0))
        self.assertEqual(tuple(level.differences[0].vector for level in levels), ("S", "Sch", "C", "P"))


if __name__ == "__main__":
    unittest.main()
