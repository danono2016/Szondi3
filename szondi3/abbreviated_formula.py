"""Source-constrained core of Szondi's abbreviated Triebformel.

Primary basis: Lipot Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 269-271 and the published Trieblinnaeus
examples.

SOURCE-ESTABLISHED:
- the abbreviated Triebformel is a symptom/root fraction;
- symptomatic factors occupy the numerator and root (Wurzel-) factors the
  denominator;
- Fall 11 prints m/s and explicitly describes m alone as the symptomatic factor
  and s alone as the root factor in the abbreviated formula;
- Fall 18 prints both k/s and kp/hs under ``Abgekürzte Triebformel`` before the
  separate ``Vollständige Triebformel``;
- the complete Triebformel has symptomatic, submanifest/sublatent, and root
  lines, with same-line membership constrained by the source TspG rule;
- in the Trieblinnaeus tables, formulas are represented without the middle
  submanifest/sublatent factors.

SOURCE LIMIT / FAIL-CLOSED BOUNDARY:
The admitted evidence does not establish a universal selector that determines
when or how the simple abbreviated fraction is broadened to a multi-factor form
such as kp/hs. In particular, the complete-formula outer lines cannot simply be
relabelled as a universal extended abbreviation: in Fall 11 the complete root
line contains hy, h, and s, while Szondi explicitly prints/describes s alone in
the abbreviated formula. Likewise, Fall 12 has tied minimal TspG factors but
prints only one of them in its abbreviated formula, so ties do not authorize an
``emit every combination`` convention.

The statement that Trieblinnaeus table formulas omit middle factors is retained
as a separate table-representation fact. It does not by itself prove that every
outer-line projection is an ``extended abbreviated formula``.

Accordingly this module implements only the source-safe simple-extrema core and
preserves tied extrema as candidates. It does not manufacture the unresolved
multi-factor broadening selector.
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
    extrema are not governed by a universal ``emit every combination`` rule.
    """
    candidates = abbreviated_formula_candidates(series)
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError(
        "Abbreviated Triebformel is unresolved: tied extrema require an additional source-authorized rule"
    )
