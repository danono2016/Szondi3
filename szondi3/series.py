"""Repeated profile series and Szondi's ten-series conversion table.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 285-286, Tabelle 13.

The module records ordered repeated profiles without imposing a timing interval.
Szondi treats repetition as obligatory and the Zehnerserie as the formal basis,
while allowing defined evaluation from at least three profiles. Counts observed
in series of three to nine profiles are converted to the ten-profile basis by the
explicit source table below rather than by an inferred rounding formula.
"""

from dataclasses import dataclass

from .profile import DriveProfile


_TABLE_13 = {
    3: {1: 3, 2: 7, 3: 10},
    4: {1: 2, 2: 5, 3: 7, 4: 10},
    5: {1: 2, 2: 4, 3: 6, 4: 8, 5: 10},
    6: {1: 2, 2: 3, 3: 5, 4: 7, 5: 8, 6: 10},
    7: {1: 1, 2: 3, 3: 4, 4: 6, 5: 7, 6: 9, 7: 10},
    8: {1: 1, 2: 2, 3: 4, 4: 5, 5: 6, 6: 7, 7: 9, 8: 10},
    9: {1: 1, 2: 2, 3: 3, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10},
}


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
