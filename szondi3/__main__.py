"""Default Szondi3 Alpha product launcher.

``python -m szondi3`` opens the stable local clinician Alpha surface.  The global
V4 clinical writer remains an explicit experimental opt-in via
``python -m szondi3.clinician_alpha_app_v4`` and is not part of the default path
while its composition and acceptance contracts are still under development.

Administration, deterministic calculation, interpretation, archive and provenance
remain in their existing authoritative layers.  The default launcher choice is a
stability boundary, not a claim that the older writer is clinically final.
"""

from __future__ import annotations

from .clinician_alpha_app_v3 import main as alpha_clinician_main


def main(argv: list[str] | None = None) -> int:
    """Launch the stable local clinician Alpha surface."""
    return alpha_clinician_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
