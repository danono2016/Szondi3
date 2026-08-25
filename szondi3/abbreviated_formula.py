"""Source-derived core of Szondi's abbreviated Triebformel.

Primary basis: Lipot Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 269-271 and the printed examples Fall 11,
Fall 16 and Fall 18.

Szondi defines the abbreviated Triebformel as a simple fraction with a
symptomatic factor in the numerator and a root (Wurzel-) factor in the
denominator. The printed examples demonstrate the source-safe core used here:
the factor(s) at maximal factorial TspG stand against the factor(s) at minimal
factorial TspG. Equal extrema are preserved as alternative simple fractions.

This module deliberately does not formalize Fall 18's additional printed
``kp/hs`` variant, whose relation to the simple ``k/s`` abbreviation is not yet
stated explicitly enough in the admitted source for a universal software rule.
No psychological meaning is assigned here.
"""

from dataclasses import dataclass

from .formula import FormulaFactorTension, formula_factor_tensions
from .series import ProfileSeries


@dataclass(frozen=True, slots=True)
class AbbreviatedFormulaFraction:
    """One source-safe simple symptom/root fraction."""

    symptomatic: FormulaFactorTension
    root: FormulaFactorTension

    @property
    def numerator_factor(self) -> str:
        return self.symptomatic.factor

    @property
    def denominator_factor(self) -> str:
        return self.root.factor


def abbreviated_fractions_from_tensions(
    tensions: tuple[FormulaFactorTension, ...],
) -> tuple[AbbreviatedFormulaFraction, ...]:
    """Pair every maximal-TspG factor with every minimal-TspG factor.

    Equal extrema are genuine source ties and are not collapsed or arbitrarily
    ordered. The function expects at least one factor tension.
    """
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


def abbreviated_formula_fractions(series: ProfileSeries) -> tuple[AbbreviatedFormulaFraction, ...]:
    """Return every simple extreme-TspG abbreviation without breaking ties.

    Factorial TspG is monotone under Tabelle-13 conversion, so maximal/minimal
    factor identity and ties are the same on observed and ten-series bases. The
    observed factor objects are retained for provenance/display.

    Fall 11 yields ``m/s``. Fall 16 has one maximal factor ``e`` and the tied
    minimal factors ``d`` and ``m``, yielding ``e/d`` and ``e/m`` exactly as
    printed. Fall 18 yields the source's first printed simple fraction ``k/s``.
    The additional ``kp/hs`` variant is intentionally outside this primitive.
    """
    return abbreviated_fractions_from_tensions(formula_factor_tensions(series))
