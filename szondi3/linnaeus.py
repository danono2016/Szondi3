"""Source-derived Trieblinnäus classifications for repeated profile series.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), especially the definition of Haupttriebklassen from
the greatest intravectorial Tendenzspannungsdifferenz and the distinction of
positive/negative Unterklassen by the Wahlrichtung of the unsatisfied root factor.

This module remains in the deterministic P1 layer. It preserves formal evidence
and class structure only; it does not attach clinical meaning or invent a subclass
sign when the admitted source does not supply a general decision rule.
"""

from dataclasses import dataclass
from typing import Literal

from .series import ProfileSeries, VectorLatencyStatus, latency_statuses

SubclassSign = Literal["+", "-"]


@dataclass(frozen=True, slots=True)
class LeadingDriveClass:
    """One source-authorized co-leading Haupttriebklasse candidate."""

    designation: str
    status: VectorLatencyStatus


@dataclass(frozen=True, slots=True)
class RootDirectionEvidence:
    """Observed Wahlrichtung evidence for one leading class's Wurzelfaktor.

    Szondi defines positive/negative Unterklassen from the positive or negative
    Wahlrichtung of the unsatisfied root factor. The source also describes roots
    as constantly or almost constantly directional, but does not state a universal
    numeric majority threshold for every mixed series. Counts are therefore
    preserved without converting an arbitrary majority into a subclass sign.
    """

    designation: str
    root_factor: str
    positive_reactions: int
    negative_reactions: int
    null_reactions: int
    ambivalent_reactions: int

    @property
    def directional_reactions(self) -> int:
        return self.positive_reactions + self.negative_reactions


@dataclass(frozen=True, slots=True)
class StrictDriveSubclass:
    """A positive/negative Unterklasse established without a mixed-direction rule."""

    designation: str
    sign: SubclassSign
    root_factor: str
    evidence: RootDirectionEvidence

    @property
    def label(self) -> str:
        return f"{self.designation}{self.sign}"



def leading_drive_classes(series: ProfileSeries) -> tuple[LeadingDriveClass, ...]:
    """Return all Haupttriebklassen tied at the greatest normalized latency.

    Szondi defines the current Haupttriebklasse from the greatest vectorial TspD.
    His later all-Ventil examples explicitly preserve more than one table/class
    when multiple vectors share the relatively highest latency. Therefore ties are
    returned together rather than broken by vector order.

    Three through nine recorded profiles are first normalized to the ten-series
    basis by ``latency_statuses``. If all four vectorial differences are zero,
    none of the eight directional Haupttriebklassen can be constructed because no
    vector has a source-defined lower-tension factor; the function fails closed.
    """
    statuses = latency_statuses(series)
    highest = max(item.ten_base_magnitude for item in statuses)
    leaders = tuple(item for item in statuses if item.ten_base_magnitude == highest)

    if highest == 0:
        raise ValueError(
            "Haupttriebklasse is unresolved when all four vectorial TspD values are zero"
        )

    result = []
    for item in leaders:
        designation = item.difference.designation
        if designation is None:
            raise ValueError(
                "Haupttriebklasse requires a source-defined directional vector designation"
            )
        result.append(LeadingDriveClass(designation=designation, status=item))
    return tuple(result)



def leading_root_direction_evidence(
    series: ProfileSeries,
) -> tuple[RootDirectionEvidence, ...]:
    """Count +, -, 0 and ± reactions for each leading Wurzelfaktor.

    Lehrbuch pp. 281 ff. defines Unterklassen by the positivity or negativity of
    the Wahlrichtung of the unsatisfied need/root factor. This function records
    exactly the series evidence needed for that later classification. It does not
    infer a subclass sign from a mixed + / - history because no general numeric
    majority threshold has yet been established from the admitted primary source.

    A forced null belongs to the complement procedure and cannot silently enter
    foreground Trieblinnäus evidence.
    """
    result = []
    for leader in leading_drive_classes(series):
        root_factor = leader.status.difference.lower_tension_factor
        if root_factor is None:
            raise ValueError("Leading class has no source-defined Wurzelfaktor")

        reactions = []
        for profile in series.profiles:
            reaction = next(item for item in profile.factors if item.factor == root_factor)
            if reaction.forced_null:
                raise ValueError(
                    "Zwangs-Nullreaktion cannot silently enter Wurzelfaktor direction evidence"
                )
            reactions.append(reaction)

        result.append(
            RootDirectionEvidence(
                designation=leader.designation,
                root_factor=root_factor,
                positive_reactions=sum(item.kind == "positive" for item in reactions),
                negative_reactions=sum(item.kind == "negative" for item in reactions),
                null_reactions=sum(item.kind == "null" for item in reactions),
                ambivalent_reactions=sum(item.kind == "ambivalent" for item in reactions),
            )
        )
    return tuple(result)



def strict_leading_subclasses(series: ProfileSeries) -> tuple[StrictDriveSubclass, ...]:
    """Assign Unterklasse signs only when observed root direction is unambiguous.

    Lehrbuch defines the two Unterklassen by positive versus negative Wahlrichtung
    of the Wurzelfaktor. A series containing directional reactions on only one side
    therefore supports that sign directly. If both positive and negative root
    reactions occur, the admitted source has not yet yielded a universal numeric
    decision threshold, so this deterministic layer fails closed instead of using
    an invented majority rule. A root with no directional reaction also cannot be
    signed.
    """
    result = []
    for evidence in leading_root_direction_evidence(series):
        positive = evidence.positive_reactions
        negative = evidence.negative_reactions
        if positive and not negative:
            sign: SubclassSign = "+"
        elif negative and not positive:
            sign = "-"
        elif positive and negative:
            raise ValueError(
                f"Unterklasse sign unresolved for mixed Wurzelfaktor direction: {evidence.root_factor}"
            )
        else:
            raise ValueError(
                f"Unterklasse sign unresolved without directional Wurzelfaktor reactions: {evidence.root_factor}"
            )
        result.append(
            StrictDriveSubclass(
                designation=evidence.designation,
                sign=sign,
                root_factor=evidence.root_factor,
                evidence=evidence,
            )
        )
    return tuple(result)
