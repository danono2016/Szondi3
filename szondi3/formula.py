"""Source-derived deterministic primitives for the Szondian Triebformel.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 267-286. The source defines factorial TspG as
Sigma(null) + Sigma(ambivalent), orders the eight factors by that degree, and for
series shorter than ten profiles requires Tabelle 13 conversion before using the
numbers of the Triebformel.

This P1 module records normalized factor tension and ordering only. It does not yet
construct abbreviated/full formula lines or attach psychological meaning.
"""

from dataclasses import dataclass

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
