"""Source-constrained Szondian abbreviated Triebformel primitives.

Primary basis: Lipot Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 269-271 and printed examples in the same
Trieblinnaeus chapter.

SOURCE-ESTABLISHED:
- the abbreviated Triebformel is a symptom/root fraction;
- symptomatic factors occupy the numerator and root (Wurzel-) factors the
  denominator;
- Fall 11 prints the simple fraction m/s;
- Fall 18 prints both k/s and kp/hs under ``Abgekürzte Triebformel``;
- the complete Triebformel has symptomatic, submanifest/sublatent, and root
  lines, with same-line membership constrained by the source TspG rule.

PROJECT RESOLUTION / IMPLEMENTATION-INFERRED, strongly source-constrained:
The extended abbreviated formula is the projection of an already constituted
complete Triebformel onto its two outer lines:

    symptomatic line / root line

The middle submanifest/sublatent line is omitted. Thus Fall 18's complete
partition k,p / m,d,hy,e / h,s projects to kp/hs. Factors such as p and h are
not added later by a special neighbour/threshold rule; they are present because
they already belong to the symptomatic and root lines respectively.

This removes the need for a separate universal ``broader selector``. If the
complete formula partition is not uniquely source-authorized, only that local
case remains fail-closed.

The simple abbreviation remains the leading symptomatic factor over the deepest
root factor. Unique maximal/minimal factorial TspG extrema therefore provide a
source-safe simple abbreviation (for example Fall 11 m/s and Fall 18 k/s).
Tied extrema remain candidates only; software does not invent a tie selector.
"""

from dataclasses import dataclass

from .formula import (
    FormulaFactorTension,
    FormulaLinePartition,
    formula_factor_tensions,
    unique_formula_partition,
)
from .series import ProfileSeries


@dataclass(frozen=True, slots=True)
class AbbreviatedFormulaFraction:
    """One simple symptom/root fraction candidate."""

    symptomatic: FormulaFactorTension
    root: FormulaFactorTension

    @property
    def numerator_factor(self) -> str:
        return self.symptomatic.factor

    @property
    def denominator_factor(self) -> str:
        return self.root.factor


@dataclass(frozen=True, slots=True)
class ExtendedAbbreviatedFormula:
    """Outer-line projection of a complete Triebformel partition."""

    symptomatic: tuple[FormulaFactorTension, ...]
    root: tuple[FormulaFactorTension, ...]

    @property
    def numerator_factors(self) -> tuple[str, ...]:
        return tuple(item.factor for item in self.symptomatic)

    @property
    def denominator_factors(self) -> tuple[str, ...]:
        return tuple(item.factor for item in self.root)

    @property
    def notation(self) -> str:
        """Return compact factor notation such as ``kp/hs``."""
        return f"{''.join(self.numerator_factors)}/{''.join(self.denominator_factors)}"


def abbreviated_fraction_candidates_from_tensions(
    tensions: tuple[FormulaFactorTension, ...],
) -> tuple[AbbreviatedFormulaFraction, ...]:
    """Return extrema-based simple candidates without claiming a tie-selection rule."""
    if not tensions:
        raise ValueError("Abbreviated Triebformel requires at least one factor tension")
    maximum = max(item.ten_base_degree for item in tensions)
    minimum = min(item.ten_base_degree for item in tensions)
    symptomatic = tuple(item for item in tensions if item.ten_base_degree == maximum)
    roots = tuple(item for item in tensions if item.ten_base_degree == minimum)
    return tuple(
        AbbreviatedFormulaFraction(symptomatic=top, root=bottom)
        for top in symptomatic
        for bottom in roots
    )


def abbreviated_formula_candidates(series: ProfileSeries) -> tuple[AbbreviatedFormulaFraction, ...]:
    """Return source-compatible simple extrema candidates for one profile series."""
    return abbreviated_fraction_candidates_from_tensions(formula_factor_tensions(series))


def unique_abbreviated_formula_fraction(series: ProfileSeries) -> AbbreviatedFormulaFraction:
    """Return a simple abbreviation only when the source-safe extrema are unique.

    Ties fail closed because admitted primary examples demonstrate that equal
    extrema are not governed by a universal 'emit every combination' rule.
    """
    candidates = abbreviated_formula_candidates(series)
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError(
        "Abbreviated Triebformel is unresolved: tied extrema require an additional source-authorized rule"
    )


def extended_abbreviated_formula_from_partition(
    partition: FormulaLinePartition,
) -> ExtendedAbbreviatedFormula:
    """Project a complete formula onto symptomatic/root lines, omitting the middle."""
    return ExtendedAbbreviatedFormula(
        symptomatic=partition.symptomatic.factors,
        root=partition.root.factors,
    )


def extended_abbreviated_formula(series: ProfileSeries) -> ExtendedAbbreviatedFormula:
    """Return the extended abbreviation when the complete partition is unique.

    Ambiguity is inherited from complete-formula constitution: this function adds
    no new factor selector and therefore fails closed exactly when
    ``unique_formula_partition`` fails closed.
    """
    return extended_abbreviated_formula_from_partition(unique_formula_partition(series))
