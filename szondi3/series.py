"""Repeated profile series and source-defined formal series measures.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 267-287, including factorial TspG,
vectorial TspD, Latenzproportionen, Gefahr/Ventil thresholds, Tabelle 13,
Tendenzspannungsquotient and prozentuale Symptomreaktionen.

The module records ordered repeated profiles without imposing a timing interval.
Source-defined arithmetic is preserved exactly. Decimal or integer presentation is
not treated as part of the mathematical rule where the source does not specify a
general rounding convention.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from .profile import DriveProfile, VECTOR_FACTORS
from .stimuli import FACTORS


_TABLE_13 = {
    3: {1: 3, 2: 7, 3: 10},
    4: {1: 2, 2: 5, 3: 7, 4: 10},
    5: {1: 2, 2: 4, 3: 6, 4: 8, 5: 10},
    6: {1: 2, 2: 3, 3: 5, 4: 7, 5: 8, 6: 10},
    7: {1: 1, 2: 3, 3: 4, 4: 6, 5: 7, 6: 9, 7: 10},
    8: {1: 1, 2: 2, 3: 4, 4: 5, 5: 6, 6: 7, 7: 9, 8: 10},
    9: {1: 1, 2: 2, 3: 3, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10},
}

LatencyStatus = Literal["danger", "ventil"]


@dataclass(frozen=True, slots=True)
class ProfileSeries:
    """Ordered repeated profiles, with the source-defined ten-profile ceiling."""

    profiles: tuple[DriveProfile, ...]

    def __post_init__(self) -> None:
        if not 1 <= len(self.profiles) <= 10:
            raise ValueError("A recorded profile series must contain between one and ten profiles")
        if any(not isinstance(profile, DriveProfile) for profile in self.profiles):
            raise TypeError("A profile series can contain only DriveProfile objects")

    @property
    def profile_count(self) -> int:
        return len(self.profiles)

    @property
    def is_ten_series(self) -> bool:
        return self.profile_count == 10

    @property
    def supports_linnaeus_evaluation(self) -> bool:
        """Szondi states that Trieblinnäus evaluation requires at least three profiles."""
        return self.profile_count >= 3


@dataclass(frozen=True, slots=True)
class SeriesIndices:
    """Source-defined raw series counts and exact arithmetic measures."""

    null_reactions: int
    ambivalent_reactions: int
    total_factor_reactions: int
    tendenzspannungsquotient: Fraction | None
    symptom_percentage: Fraction

    @property
    def symptom_reactions(self) -> int:
        return self.null_reactions + self.ambivalent_reactions


@dataclass(frozen=True, slots=True)
class FactorTensionDegree:
    """Raw factorial Tendenzspannungsgrad (TspG) for one drive factor."""

    factor: str
    null_reactions: int
    ambivalent_reactions: int
    degree: int


@dataclass(frozen=True, slots=True)
class VectorTensionDifference:
    """Intravektorielle Tendenzspannungsdifferenz (TspD) for one vector.

    Szondi defines the magnitude as larger TspG minus smaller TspG. When the
    degrees differ, the factor with the smaller TspG is retained as the vector
    index because the source treats that factor as dynamically stronger. Equal
    TspGs have no unique smaller factor, so no index/designation is invented.
    """

    vector: str
    factors: tuple[str, str]
    degrees: tuple[int, int]
    magnitude: int
    lower_tension_factor: str | None
    designation: str | None


@dataclass(frozen=True, slots=True)
class LatencyLevel:
    """One equal-magnitude level in the descending Latenzproportionen."""

    magnitude: int
    differences: tuple[VectorTensionDifference, ...]


@dataclass(frozen=True, slots=True)
class VectorLatencyStatus:
    """One vector's source-normalized Gefahr/Ventil latency status."""

    vector: str
    difference: VectorTensionDifference
    raw_magnitude: int
    ten_base_magnitude: int
    status: LatencyStatus


def ten_base_count(profile_count: int, observed_count: int) -> int:
    """Convert an observed frequency to the Zehnerserie basis using Tabelle 13.

    Tabelle 13 supplies the non-zero mappings for series of three through nine
    profiles. Zero remains zero, and an actual ten-profile series is already on
    the source's reference basis.
    """
    if not isinstance(profile_count, int) or not isinstance(observed_count, int):
        raise ValueError("Profile and observed counts must be integers")
    if not 3 <= profile_count <= 10:
        raise ValueError("Tabelle 13 conversion applies only from three through ten profiles")
    if not 0 <= observed_count <= profile_count:
        raise ValueError("Observed count must fall within the recorded profile count")
    if observed_count == 0 or profile_count == 10:
        return observed_count
    return _TABLE_13[profile_count][observed_count]


def _free_reactions(series: ProfileSeries):
    reactions = tuple(
        reaction
        for profile in series.profiles
        for reaction in profile.factors
    )
    if any(reaction.forced_null for reaction in reactions):
        raise ValueError("Zwangs-Nullreaktion cannot silently enter free-reaction series measures")
    return reactions


def series_indices(series: ProfileSeries) -> SeriesIndices:
    """Calculate TspQu and % Sy-Re without adding clinical interpretation.

    TspQu is Sigma(null) / Sigma(ambivalent). The admitted primary source does not
    specify a value for a zero ambivalent denominator, so that case is represented
    explicitly as ``None`` rather than silently inventing infinity or another value.

    % Sy-Re is (Sigma(null) + Sigma(ambivalent)) * 100 divided by the number of
    factorial reactions. The exact Fraction is retained because source examples
    display rounded values without stating a general rounding convention.

    A source-defined forced null (ø) is intentionally rejected here: Szondi says
    that such a Zwangs-Nullreaktion must not be interpreted as a freely produced
    null reaction. Until a primary rule authorizes its use in these series measures,
    it cannot silently enter them.
    """
    reactions = _free_reactions(series)
    null_reactions = sum(reaction.kind == "null" for reaction in reactions)
    ambivalent_reactions = sum(reaction.kind == "ambivalent" for reaction in reactions)
    total = len(reactions)

    tendenzspannungsquotient = (
        Fraction(null_reactions, ambivalent_reactions)
        if ambivalent_reactions
        else None
    )
    symptom_percentage = Fraction(
        (null_reactions + ambivalent_reactions) * 100,
        total,
    )

    return SeriesIndices(
        null_reactions=null_reactions,
        ambivalent_reactions=ambivalent_reactions,
        total_factor_reactions=total,
        tendenzspannungsquotient=tendenzspannungsquotient,
        symptom_percentage=symptom_percentage,
    )


def factor_tension_degrees(series: ProfileSeries) -> tuple[FactorTensionDegree, ...]:
    """Return each factor's raw TspG = Sigma(null) + Sigma(ambivalent).

    This is the source-defined factorial count only. No ranking, Triebformel line,
    symptom/root classification or clinical meaning is assigned here. Short series
    remain raw observed counts; any later source-authorized ten-series conversion
    must be applied explicitly by the procedure that requires it.
    """
    reactions = _free_reactions(series)
    result = []
    for factor in FACTORS:
        factor_reactions = tuple(reaction for reaction in reactions if reaction.factor == factor)
        null_reactions = sum(reaction.kind == "null" for reaction in factor_reactions)
        ambivalent_reactions = sum(reaction.kind == "ambivalent" for reaction in factor_reactions)
        result.append(
            FactorTensionDegree(
                factor=factor,
                null_reactions=null_reactions,
                ambivalent_reactions=ambivalent_reactions,
                degree=null_reactions + ambivalent_reactions,
            )
        )
    return tuple(result)


def vector_tension_differences(series: ProfileSeries) -> tuple[VectorTensionDifference, ...]:
    """Calculate the four raw intravectorial TspD values.

    The magnitude is always the larger factorial TspG minus the smaller. If one
    factor has the smaller degree, its letter is appended to the vector name exactly
    as in Szondi's notation (for example ``Ss`` or ``Schp``). Equal degrees are
    retained as an explicit tie: there is no uniquely source-authorized index.

    This function does not rank vectors or assign a Triebklasse.
    """
    by_factor = {item.factor: item for item in factor_tension_degrees(series)}
    result = []
    for vector, factors in VECTOR_FACTORS:
        first, second = factors
        first_degree = by_factor[first].degree
        second_degree = by_factor[second].degree
        magnitude = abs(first_degree - second_degree)

        if first_degree < second_degree:
            lower_tension_factor = first
        elif second_degree < first_degree:
            lower_tension_factor = second
        else:
            lower_tension_factor = None

        designation = (
            f"{vector}{lower_tension_factor}"
            if lower_tension_factor is not None
            else None
        )
        result.append(
            VectorTensionDifference(
                vector=vector,
                factors=factors,
                degrees=(first_degree, second_degree),
                magnitude=magnitude,
                lower_tension_factor=lower_tension_factor,
                designation=designation,
            )
        )
    return tuple(result)


def latency_proportions(series: ProfileSeries) -> tuple[LatencyLevel, ...]:
    """Return the descending raw Reihe der Latenzgrade without tie-breaking.

    Szondi orders the four intravectorial TspD values from greatest to smallest.
    Equal differences are genuine equal proportions; they are grouped into one
    level instead of being assigned an artificial rank. The original vector order
    S, P, Sch, C is retained inside each equality group solely as stable identity,
    not as a clinical priority.

    This is ordering only. It does not classify danger/ventil status or assign a
    Haupttriebklasse.
    """
    differences = vector_tension_differences(series)
    magnitudes = sorted({item.magnitude for item in differences}, reverse=True)
    return tuple(
        LatencyLevel(
            magnitude=magnitude,
            differences=tuple(item for item in differences if item.magnitude == magnitude),
        )
        for magnitude in magnitudes
    )


def latency_statuses(series: ProfileSeries) -> tuple[VectorLatencyStatus, ...]:
    """Classify normalized vector latencies as Triebgefahr or Triebventil.

    Szondi's rule is stated on the Zehnerserie basis: latency magnitudes 5 through
    10 are Triebgefahren; magnitudes below 5 (0 through 4) are Triebventile.
    For three through nine recorded profiles, Tabelle 13 is applied first because
    the source explicitly requires conversion of Latenzproportion numbers to the
    assumed ten-profile basis before those results are used.

    This is the quantitative status only. It does not assign Triventilklasse,
    Quadriventilklasse, Haupttriebklasse, subclass, or clinical meaning.
    """
    if not series.supports_linnaeus_evaluation:
        raise ValueError("Gefahr/Ventil classification requires at least three profiles")

    result = []
    for difference in vector_tension_differences(series):
        normalized = ten_base_count(series.profile_count, difference.magnitude)
        status: LatencyStatus = "danger" if normalized >= 5 else "ventil"
        result.append(
            VectorLatencyStatus(
                vector=difference.vector,
                difference=difference,
                raw_magnitude=difference.magnitude,
                ten_base_magnitude=normalized,
                status=status,
            )
        )
    return tuple(result)
