"""Source-derived Trieblinnäus classifications for repeated profile series.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), especially the definition of Haupttriebklassen from
the greatest intravectorial Tendenzspannungsdifferenz and the explicit treatment
of co-leading relative latency magnitudes.

This module remains in the deterministic P1 layer. It assigns formal class
structure only; it does not attach clinical meaning.
"""

from dataclasses import dataclass

from .series import ProfileSeries, VectorLatencyStatus, latency_statuses


@dataclass(frozen=True, slots=True)
class LeadingDriveClass:
    """One source-authorized co-leading Haupttriebklasse candidate."""

    designation: str
    status: VectorLatencyStatus



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
