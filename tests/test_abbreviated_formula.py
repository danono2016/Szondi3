import unittest

from szondi3.abbreviated_formula import abbreviated_structure_from_partition
from szondi3.formula import (
    FactorTensionLevel,
    FormulaFactorTension,
    formula_partition_candidates_from_levels,
)


def level(decision_degree, *factor_specs):
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


class AbbreviatedFormulaTests(unittest.TestCase):
    def test_fall_11_structure_is_m_over_root_line(self):
        levels = (
            level(8, "m"),
            level(5, "d", "k"),
            level(4, "p", "e"),
            level(2, "hy", "h"),
            level(1, "s"),
        )
        partition = formula_partition_candidates_from_levels(levels)[0]

        structure = abbreviated_structure_from_partition(partition)

        self.assertEqual(structure.numerator_factors, ("m",))
        self.assertEqual(structure.denominator_factors, ("hy", "h", "s"))

    def test_fall_18_structure_omits_submanifest_line(self):
        levels = (
            level(8, ("k", 5)),
            level(7, ("p", 4)),
            level(5, ("m", 3), ("d", 3)),
            level(3, ("hy", 2), ("e", 2)),
            level(2, ("h", 1)),
            level(0, ("s", 0)),
        )
        partition = formula_partition_candidates_from_levels(levels)[0]

        structure = abbreviated_structure_from_partition(partition)

        self.assertEqual(structure.numerator_factors, ("k", "p"))
        self.assertEqual(structure.denominator_factors, ("h", "s"))
        self.assertEqual(
            tuple(item.display_degree for item in structure.symptomatic),
            (5, 4),
        )
        self.assertEqual(
            tuple(item.display_degree for item in structure.root),
            (1, 0),
        )

    def test_fall_16_root_equality_is_preserved_structurally(self):
        # Ten-profile Fall 16 prints abbreviated e/d and e/m separately.
        # The source definition guarantees one symptomatic factor e and two root
        # factors d,m; exact multi-fraction typography is intentionally not inferred.
        levels = (
            level(7, "e"),
            level(3, "hy"),
            level(1, "h", "s", "p", "k"),
            level(0, "d", "m"),
        )
        partition = formula_partition_candidates_from_levels(levels)[0]

        structure = abbreviated_structure_from_partition(partition)

        self.assertEqual(structure.numerator_factors, ("e",))
        self.assertEqual(structure.denominator_factors, ("d", "m"))


if __name__ == "__main__":
    unittest.main()
