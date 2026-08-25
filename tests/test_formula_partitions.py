import unittest

from szondi3.formula import (
    FactorTensionLevel,
    FormulaFactorTension,
    formula_partition_candidates_from_levels,
)


def level(decision_degree, *factor_specs):
    """Build one converted decision level.

    Each factor spec is either a factor name (raw == converted for ten-series
    witnesses) or ``(factor, raw_degree)`` for a short-series source witness.
    """
    factors = []
    for spec in factor_specs:
        if isinstance(spec, tuple):
            factor, raw_degree = spec
        else:
            factor, raw_degree = spec, decision_degree
        factors.append(
            FormulaFactorTension(
                factor=factor,
                raw_degree=raw_degree,
                ten_base_degree=decision_degree,
            )
        )
    return FactorTensionLevel(degree=decision_degree, factors=tuple(factors))


def factor_names(line):
    return tuple(item.factor for item in line.factors)


class FormulaPartitionTests(unittest.TestCase):
    def test_fall_11_quantitative_rule_yields_unique_three_line_partition(self):
        # Lehrbuch Fall 11 is a Zehnerserie: m8 / d5 k5 p4 e4 / hy2 h2 s1.
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

    def test_fall_18_table_13_conversion_uniquely_yields_printed_partition(self):
        # Lehrbuch Fall 18 has six observed profiles and raw TspG
        # k5,p4,m3,d3,hy2,e2,h1,s0. Tabelle 13 converts these to the common
        # ten-series decision basis 8,7,5,5,3,3,2,0 before Trieblinnäus use.
        # The printed complete formula groups k,p / m,d,hy,e / h,s while its
        # factor subscripts retain the observed raw values.
        levels = (
            level(8, ("k", 5)),
            level(7, ("p", 4)),
            level(5, ("m", 3), ("d", 3)),
            level(3, ("hy", 2), ("e", 2)),
            level(2, ("h", 1)),
            level(0, ("s", 0)),
        )

        candidates = formula_partition_candidates_from_levels(levels)

        self.assertEqual(len(candidates), 1)
        partition = candidates[0]
        self.assertEqual(factor_names(partition.symptomatic), ("k", "p"))
        self.assertEqual(factor_names(partition.submanifest), ("m", "d", "hy", "e"))
        self.assertEqual(factor_names(partition.root), ("h", "s"))
        self.assertEqual(tuple(line.spread for line in partition.lines), (1, 2, 2))
        self.assertEqual(
            tuple((item.factor, item.display_degree) for item in partition.symptomatic.factors),
            (("k", 5), ("p", 4)),
        )
        self.assertEqual(
            tuple((item.factor, item.display_degree) for item in partition.root.factors),
            (("h", 1), ("s", 0)),
        )

    def test_same_line_rule_is_not_applied_transitively(self):
        # 5-3 and 3-1 are each 2, but 5-1 is 4. No generated line may contain
        # all three values through a transitive neighbour-chain shortcut.
        levels = (level(5, "k"), level(3, "m"), level(1, "h"))

        candidates = formula_partition_candidates_from_levels(levels)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(tuple(line.spread for line in candidates[0].lines), (0, 0, 0))

    def test_equal_converted_tspg_factors_are_not_split_between_formula_lines(self):
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
