"""Source-derived core of Szondi's abbreviated Triebformel.

Primary basis: Lipot Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 269-271 and printed examples in the same
Trieblinnaeus chapter.

Szondi defines the abbreviated Triebformel as a simple fraction with a
symptomatic factor in the numerator and a root (Wurzel-) factor in the
denominator. Unique maximal/minimal factorial TspG extrema therefore provide a
source-safe simple abbreviation (for example Fall 11 m/s and the first Fall 18
fraction k/s).

The admitted examples do not support a universal rule for ties. Fall 16 prints
both e/d and e/m for tied minimal extrema, while another printed case with tied
minimal TspG values selects only one denominator. Therefore tied extrema are
preserved as candidates, but software must not declare all combinations to be
the authoritative abbreviated formula without an additional source-authorized
selection rule.

This module also does not formalize Fall 18's additional printed ``kp/hs``
variant. No psychological meaning is assigned here.
"""

from dataclasses import dataclass

from .formula import FormulaFactorTension, formula_factor_tensions
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


def abbreviated_fraction_candidates_from_tensions(
    tensions: tuple[FormulaFactorTension, ...],
) -> tuple[AbbreviatedFormulaFraction, ...]:
    """Return extrema-based candidates without claiming a tie-selection rule."""
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
    """Return source-compatible extrema candidates for one profile series."""
    return abbreviated_fraction_candidates_from_tensions(formula_factor_tensions(series))


def unique_abbreviated_formula_fraction(series: ProfileSeries) -> AbbreviatedFormulaFraction:
    """Return a simple abbreviation only when the source-safe extrema are unique.

    Ties fail closed because the admitted primary examples demonstrate that equal
    extrema are not governed by a universal 'emit every combination' rule.
    """
    candidates = abbreviated_formula_candidates(series)
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError(
        "Abbreviated Triebformel is unresolved: tied extrema require an additional source-authorized rule"
    )
