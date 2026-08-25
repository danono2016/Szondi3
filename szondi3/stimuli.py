"""Source-derived stimulus identity and presentation facts.

Primary basis: Lipót Szondi, Lehrbuch der experimentellen Triebdiagnostik,
3rd expanded edition (1972), pp. 45-48 and p. 357, Tabelle 19.

This module contains deterministic administration facts only. It contains no
clinical interpretation and no historical metadata about photographed persons.
"""

from dataclasses import dataclass
from pathlib import Path

SERIES = ("I", "II", "III", "IV", "V", "VI")
FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")

_FACTOR_BY_POSITION = {
    "I": ("k", "s", "p", "d", "h", "e", "m", "hy"),
    "II": ("hy", "m", "e", "h", "d", "p", "s", "k"),
    "III": ("h", "e", "s", "m", "k", "d", "hy", "p"),
    "IV": ("p", "hy", "d", "k", "m", "s", "e", "h"),
    "V": ("e", "d", "hy", "p", "s", "k", "h", "m"),
    "VI": ("m", "h", "k", "s", "p", "hy", "d", "e"),
}


@dataclass(frozen=True, slots=True)
class Stimulus:
    card_id: str
    series: str
    position: int
    factor: str
    image_path: str


def catalog() -> tuple[Stimulus, ...]:
    """Return all 48 cards in series order and source-defined position order."""
    return tuple(
        Stimulus(
            card_id=f"{series}-{position:02d}",
            series=series,
            position=position,
            factor=factor,
            image_path=f"assets/stimuli/{series}-{position:02d}-{factor}.webp",
        )
        for series in SERIES
        for position, factor in enumerate(_FACTOR_BY_POSITION[series], start=1)
    )


def presentation_rows(series: str) -> tuple[tuple[Stimulus, ...], tuple[Stimulus, ...]]:
    """Return one series as two simultaneous rows: positions 1-4 and 5-8."""
    if series not in SERIES:
        raise ValueError(f"Unknown stimulus series: {series}")
    group = tuple(card for card in catalog() if card.series == series)
    return group[:4], group[4:]


def validate_assets(asset_dir: Path) -> None:
    """Fail if the repository stimulus filenames differ from the source mapping."""
    expected = {Path(card.image_path).name for card in catalog()}
    actual = {path.name for path in asset_dir.glob("*.webp")}
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"Stimulus asset mismatch; missing={missing}; extra={extra}")
