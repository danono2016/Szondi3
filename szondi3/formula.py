"""Source-derived deterministic primitives for the Szondian Triebformel.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), especially pp. 269-271 and 285-286. The source
defines factorial TspG as Sigma(null) + Sigma(ambivalent), orders the eight
factors by that degree, and requires results from shorter series to be converted
through Tabelle 13 to the common ten-profile basis before Trieblinnäus use.

For the complete Triebformel Szondi states that factors written on the same line
must differ in TspG by no more than 2 and presents three semantic lines:
symptomatic, submanifest/sublatent, and root factors. For short series the line
decision is therefore made on the Tabelle-13 ten-series values. The printed
formula may continue to carry the actually observed TspG as factor subscripts;
Fall 18 is the decisive visual witness: observed 5,4,3,3,2,2,1,0 become
8,7,5,5,3,3,2,0 for the grouping decision, yielding exactly the printed
k,p / m,d,hy,e / h,s structure while the printed subscripts remain observed.

The explicit quantitative rule can still be non-unique for some hypothetical
normalized rankings. In that case this module fails closed rather than inventing
a grouping convention. It may expose only factor roles that are invariant across
all source-compatible partitions; this is a logical property of the candidate set,
not a repair or a claim that Szondi defined an additional tie-breaking method.

This P1 module remains formal test calculation only; it does not attach clinical
meaning.
"""

from dataclasses import dataclass
from typing import Literal

from .series import ProfileSeries, factor_tension_degrees, ten_base_count


@dataclass(frozen=True, slots=True)
class FormulaFactorTension:
    """One factor's observed and ten-series TspG for formula use.

    ``raw_degree`` is the actually observed factorial TspG and is the value retained
    for source-faithful formula display. ``ten_base_degree`` is the Tabelle-13 value
    used for ranking/grouping when fewer than ten profiles were recorded.
    """

    factor: str
    raw_degree: int
    ten_base_degree: int

    @property
    def display_degree(self) -> int:
        """Return the source-observed TspG printed as a formula subscript."""
        return self.raw_degree


@dataclass(frozen=True, slots=True)
class FactorTensionLevel:
    """One equality-preserving level in descending ten-series formula TspG order."""

    degree: int
    factors: tuple[FormulaFactorTension, ...]


FormulaLineRole = Literal["symptomatic", "submanifest", "root"]


@dataclass(frozen=True, slots=True)
class FormulaLine:
    """One source-compatible line of the complete Triebformel.

    Line spread is evaluated on the ten-series decision degrees in ``levels``;
    individual factor objects still retain their observed display degrees.
    """

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


@dataclass(frozen=True, slots=True)
class FormulaRoleConsensus:
    """Roles invariant across every source-compatible complete-formula partition.

    This object deliberately does not choose one candidate when the explicit source
    rule admits several. A factor is listed under a role only if it occupies that
    same role in every admissible partition. ``variable_factors`` retain all factors
    whose role changes between candidates.
    """

    candidate_count: int
    symptomatic_factors: tuple[str, ...]
    submanifest_factors: tuple[str, ...]
    root_factors: tuple[str, ...]
    variable_factors: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.candidate_count < 1:
            raise ValueError("Formula role consensus requires at least one candidate")
        groups = (
            self.symptomatic_factors,
            self.submanifest_factors,
            self.root_factors,
            self.variable_factors,
        )
        flattened = tuple(item for group in groups for item in group)
        if len(flattened) != len(set(flattened)):
            raise ValueError("Formula role consensus groups must be disjoint")


def formula_factor_tensions(series: ProfileSeries) -> tuple[FormulaFactorTension, ...]:
    """Return observed and ten-series TspG values for Triebformel use.

    Lehrbuch requires at least three profiles for Trieblinnäus use. For a short
    series Tabelle 13 supplies the common ten-profile decision basis; the observed
    value is retained separately because Szondi's printed short-series formulas
    continue to show the observed TspG as factor subscripts.
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
    """Order factors by the ten-series TspG used for formula decisions.

    Equal converted degrees remain one genuine equality level. Stable source factor
    order is retained inside a tie only for deterministic identity; it is not treated
    as a priority between equal factors.
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

    ``levels`` are decision levels on the common ten-profile basis. Equality levels
    are indivisible. The ranking is partitioned into three nonempty contiguous
    lines, and every line must have max(TspG)-min(TspG) <= 2.

    Local neighbour differences are not treated transitively: values 5, 3, 1 cannot
    all occupy one line merely because 5-3 and 3-1 are each 2. If more than one
    partition satisfies the explicit rule, no tie-break is invented.
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
    """Return every complete-formula partition supported on the ten-series basis."""
    return formula_partition_candidates_from_levels(factor_tension_levels(series))


def formula_role_consensus(series: ProfileSeries) -> FormulaRoleConsensus:
    """Return only factor roles shared by every admissible complete formula.

    When several partitions satisfy Szondi's explicit quantitative rule, choosing a
    single formula would be an unsupported repair. This helper instead intersects
    the candidate roles. It adds no scoring rule and intentionally leaves changing
    roles in ``variable_factors``.
    """
    tensions = formula_factor_tensions(series)
    candidates = formula_partition_candidates(series)
    if not candidates:
        raise ValueError(
            "Formula role consensus is unresolved: no source-compatible partition"
        )

    roles_by_factor: dict[str, set[FormulaLineRole]] = {
        item.factor: set() for item in tensions
    }
    for candidate in candidates:
        for line in candidate.lines:
            for factor in line.factors:
                roles_by_factor[factor.factor].add(line.role)

    factor_order = tuple(item.factor for item in tensions)

    def stable(role: FormulaLineRole) -> tuple[str, ...]:
        return tuple(
            factor for factor in factor_order if roles_by_factor[factor] == {role}
        )

    return FormulaRoleConsensus(
        candidate_count=len(candidates),
        symptomatic_factors=stable("symptomatic"),
        submanifest_factors=stable("submanifest"),
        root_factors=stable("root"),
        variable_factors=tuple(
            factor for factor in factor_order if len(roles_by_factor[factor]) != 1
        ),
    )


def unique_formula_partition(series: ProfileSeries) -> FormulaLinePartition:
    """Return the complete formula partition only when the quantitative rule is unique."""
    candidates = formula_partition_candidates(series)
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ValueError("Complete Triebformel partition is unresolved: no source-compatible partition")
    raise ValueError(
        "Complete Triebformel partition is unresolved: explicit TspG rule permits multiple partitions"
    )
