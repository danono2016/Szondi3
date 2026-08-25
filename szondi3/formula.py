"""Source-derived deterministic primitives for the Szondian Triebformel.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 267-286. The source defines factorial TspG as
Sigma(null) + Sigma(ambivalent), orders the eight factors by that degree, and for
series shorter than ten profiles requires Tabelle 13 conversion before using the
numbers of the Triebformel.

For the complete Triebformel Szondi states that factors written on the same line
must differ in TspG by no more than 2, and presents three semantic lines:
symptomatic, submanifest/sublatent, and root factors. That condition is necessary
but is not, by itself, a universal tie-break for every possible ranking. This module
therefore enumerates source-compatible three-line partitions and resolves one only
when the admitted quantitative rule makes the partition unique.

This P1 module remains formal test calculation only; it does not attach clinical
meaning or invent a missing grouping convention.
"""

from dataclasses import dataclass
from typing import Literal

from .series import ProfileSeries, factor_tension_degrees, ten_base_count


@dataclass(frozen=True, slots=True)
class FormulaFactorTension:
    """One factor's raw and ten-series-normalized TspG for formula use."""

    factor: str
    raw_degree: int
    ten_base_degree: int


@dataclass(frozen=True, slots=True)
class FactorTensionLevel:
    """One equality-preserving level in descending formula TspG order."""

    degree: int
    factors: tuple[FormulaFactorTension, ...]


FormulaLineRole = Literal["symptomatic", "submanifest", "root"]


@dataclass(frozen=True, slots=True)
class FormulaLine:
    """One source-compatible line of the complete Triebformel."""

    role: FormulaLineRole
    levels: tuple[FactorTensionLevel, ...]

    @property
    def factors(self) -> tuple[FormulaFactorTension, ...]:
        return tuple(factor for level in self.levels for factor in level.factors)

    @property
    def maximum_degree(self) -> int:
        return self.levels[0].degree

    @property
    def minimum_degree(self) -> int:
        return self.levels[-1].degree

    @property
    def spread(self) -> int:
        return self.maximum_degree - self.minimum_degree


@dataclass(frozen=True, slots=True)
class FormulaLinePartition:
    """One admissible symptomatic / submanifest / root three-line partition."""

    symptomatic: FormulaLine
    submanifest: FormulaLine
    root: FormulaLine

    @property
    def lines(self) -> tuple[FormulaLine, FormulaLine, FormulaLine]:
        return (self.symptomatic, self.submanifest, self.root)


def formula_factor_tensions(series: ProfileSeries) -> tuple[FormulaFactorTension, ...]:
    """Return formula TspG values on Szondi's common ten-profile basis.

    Lehrbuch requires at least three profiles for Trieblinnäus use and states that
    the shorter-series Triebformel numbers must be converted through Tabelle 13.
    Raw values are retained alongside the normalized values for provenance.
    """
    if not series.supports_linnaeus_evaluation:
        raise ValueError("Triebformel evaluation requires at least three profiles")

    return tuple(
        FormulaFactorTension(
            factor=item.factor,
            raw_degree=item.degree,
            ten_base_degree=ten_base_count(series.profile_count, item.degree),
        )
        for item in factor_tension_degrees(series)
    )


def factor_tension_levels(series: ProfileSeries) -> tuple[FactorTensionLevel, ...]:
    """Order the eight normalized TspG values from greatest to smallest.

    Equal degrees remain one genuine equality level. Stable source factor order is
    retained inside a tie only for deterministic identity; it is not treated as a
    priority between equal factors.
    """
    tensions = formula_factor_tensions(series)
    degrees = sorted({item.ten_base_degree for item in tensions}, reverse=True)
    return tuple(
        FactorTensionLevel(
            degree=degree,
            factors=tuple(item for item in tensions if item.ten_base_degree == degree),
        )
        for degree in degrees
    )


def _line(role: FormulaLineRole, levels: tuple[FactorTensionLevel, ...]) -> FormulaLine:
    if not levels:
        raise ValueError("A complete Triebformel line cannot be empty")
    line = FormulaLine(role=role, levels=levels)
    if line.spread > 2:
        raise ValueError("Factors on one Triebformel line cannot differ in TspG by more than 2")
    return line


def formula_partition_candidates_from_levels(
    levels: tuple[FactorTensionLevel, ...],
) -> tuple[FormulaLinePartition, ...]:
    """Enumerate three-line partitions allowed by Szondi's explicit TspG rule.

    Equality levels are indivisible. The ranking is partitioned into three nonempty
    contiguous lines, and every line must have max(TspG)-min(TspG) <= 2. This is a
    deliberately conservative representation of the explicit quantitative rule.

    It does not assume that local neighbour differences are transitive: for example
    TspG values 5, 3, 1 cannot all occupy one line merely because 5-3 and 3-1 are
    each 2. Nor does it invent a tie-break when more than one three-line partition
    satisfies the stated rule.
    """
    if len(levels) < 3:
        return ()
    if any(levels[index].degree <= levels[index + 1].degree for index in range(len(levels) - 1)):
        raise ValueError("Formula tension levels must be strictly descending")

    result = []
    for first_cut in range(1, len(levels) - 1):
        for second_cut in range(first_cut + 1, len(levels)):
            groups = (
                levels[:first_cut],
                levels[first_cut:second_cut],
                levels[second_cut:],
            )
            if any(group[0].degree - group[-1].degree > 2 for group in groups):
                continue
            result.append(
                FormulaLinePartition(
                    symptomatic=_line("symptomatic", groups[0]),
                    submanifest=_line("submanifest", groups[1]),
                    root=_line("root", groups[2]),
                )
            )
    return tuple(result)


def formula_partition_candidates(series: ProfileSeries) -> tuple[FormulaLinePartition, ...]:
    """Return every complete-formula partition supported by the explicit rule."""
    return formula_partition_candidates_from_levels(factor_tension_levels(series))


def unique_formula_partition(series: ProfileSeries) -> FormulaLinePartition:
    """Return the complete formula partition only when the quantitative rule is unique.

    A zero-candidate result means that the three-line structure cannot be formed
    from the explicit rule. More than one candidate means that an additional
    source-authorized grouping rule is required. Both cases fail closed rather than
    selecting a convenient partition.
    """
    candidates = formula_partition_candidates(series)
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ValueError("Complete Triebformel partition is unresolved: no source-compatible partition")
    raise ValueError(
        "Complete Triebformel partition is unresolved: explicit TspG rule permits multiple partitions"
    )
