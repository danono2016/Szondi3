"""Source-derived structural primitive for Szondi's abbreviated Triebformel.

Primary basis: Lipot Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 269-271. Szondi defines the abbreviated
Triebformel as a simple fraction whose numerator contains the letters of the
symptomatic factors and whose denominator contains the letters of the root
(Wurzel-) factors. The middle submanifest/sublatent line belongs only to the
complete formula.

This module models that factor-set structure only. It deliberately does not
invent a universal typography for cases where the book prints more than one
simple fraction (for example Fall 16), and it assigns no psychological meaning.
"""

from dataclasses import dataclass

from .formula import FormulaFactorTension, FormulaLinePartition, unique_formula_partition
from .series import ProfileSeries


@dataclass(frozen=True, slots=True)
class AbbreviatedFormulaStructure:
    """Source-defined numerator/root factor sets of the abbreviated formula."""

    symptomatic: tuple[FormulaFactorTension, ...]
    root: tuple[FormulaFactorTension, ...]

    @property
    def numerator_factors(self) -> tuple[str, ...]:
        return tuple(item.factor for item in self.symptomatic)

    @property
    def denominator_factors(self) -> tuple[str, ...]:
        return tuple(item.factor for item in self.root)


def abbreviated_structure_from_partition(
    partition: FormulaLinePartition,
) -> AbbreviatedFormulaStructure:
    """Drop the complete formula's middle line and preserve top/root factors."""
    return AbbreviatedFormulaStructure(
        symptomatic=partition.symptomatic.factors,
        root=partition.root.factors,
    )


def abbreviated_formula_structure(series: ProfileSeries) -> AbbreviatedFormulaStructure:
    """Return the abbreviated formula's source-defined factor sets.

    The complete-formula partition is resolved first on the same source-authorized
    ten-series decision basis. Its symptomatic line becomes the numerator and its
    root line becomes the denominator; the submanifest line is omitted exactly as
    Szondi defines the abbreviated Bruchformel.

    If the complete partition is not uniquely determined by the explicit source
    rules, this function inherits the fail-closed behavior of
    ``unique_formula_partition`` rather than inventing an abbreviated result.
    """
    return abbreviated_structure_from_partition(unique_formula_partition(series))
