import unittest

from szondi3.formula import (
    FactorTensionLevel,
    FormulaFactorTension,
    formula_partition_candidates_from_levels,
)


def level(degree, *factors):
    return FactorTensionLevel(
        degree=degree,
        factors=tuple(
            FormulaFactorTension(factor=factor, raw_degree=degree, ten_base_degree=degree)
            for factor in factors
        ),
    )


def factor_names(line):
    return tuple(item.factor for item in line.factors)


class FormulaPartitionTests(unittest.TestCase):
    def test_fall_11_quantitative_rule_yields_unique_three_line_partition(self):
        # Lehrbuch Fall 11: m8 / d5 k5 p4 e4 / hy2 h2 s1.
        levels = (
            level(8, "m"),
            level(5, "d", "k"),
            level(4, "p", "e"),
            level(2, "hy", "h"),
            level(1, "s"),
        )

        candidates = formula_partition_candidates_from_levels(levels)

        self.assertEqual(len(candidates), 1)
        partition = candidates[0]
        self.assertEqual(factor_names(partition.symptomatic), ("m",))
        self.assertEqual(factor_names(partition.submanifest), ("d", "k", "p", "e"))
        self.assertEqual(factor_names(partition.root), ("hy", "h", "s"))
        self.assertEqual(tuple(line.spread for line in partition.lines), (0, 1, 1))

    def test_fall_18_explicit_tspg_rule_does_not_uniquely_determine_printed_partition(self):
        # Lehrbuch Fall 18 prints k,p / m,d,hy,e / h,s for 5,4,3,3,2,2,1,0.
        # The stated <=2 same-line condition alone admits other cuts, so the
        # implementation must preserve that ambiguity instead of inventing a rule.
        levels = (
            level(5, "k"),
            level(4, "p"),
            level(3, "m", "d"),
            level(2, "hy", "e"),
            level(1, "h"),
            level(0, "s"),
        )

        candidates = formula_partition_candidates_from_levels(levels)

        self.assertGreater(len(candidates), 1)
        printed = (
            ("k", "p"),
            ("m", "d", "hy", "e"),
            ("h", "s"),
        )
        rendered = tuple(
            (
                factor_names(candidate.symptomatic),
                factor_names(candidate.submanifest),
                factor_names(candidate.root),
            )
            for candidate in candidates
        )
        self.assertIn(printed, rendered)

    def test_same_line_rule_is_not_applied_transitively(self):
        # 5-3 and 3-1 are each 2, but 5-1 is 4. No generated line may contain
        # all three values through a transitive neighbour-chain shortcut.
        levels = (level(5, "k"), level(3, "m"), level(1, "h"))

        candidates = formula_partition_candidates_from_levels(levels)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(tuple(line.spread for line in candidates[0].lines), (0, 0, 0))

    def test_equal_tspg_factors_are_not_split_between_formula_lines(self):
        levels = (
            level(8, "m"),
            level(5, "d", "k"),
            level(4, "p", "e"),
            level(2, "hy", "h"),
            level(1, "s"),
        )

        partition = formula_partition_candidates_from_levels(levels)[0]

        self.assertEqual(factor_names(partition.submanifest)[:2], ("d", "k"))
        self.assertEqual(factor_names(partition.root)[:2], ("hy", "h"))

    def test_levels_must_be_strictly_descending(self):
        with self.assertRaisesRegex(ValueError, "strictly descending"):
            formula_partition_candidates_from_levels((level(5, "k"), level(5, "p"), level(2, "h")))


if __name__ == "__main__":
    unittest.main()
