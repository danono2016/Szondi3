"""Default Szondi3 Alpha product launcher.

``python -m szondi3`` opens the archive-enabled local clinician application with
the global V4 clinical report writer. Administration, deterministic calculation,
interpretation, archive and provenance remain in their existing authoritative
layers; AI remains an explicit closed-world wording layer.
"""

from __future__ import annotations

from .clinician_alpha_app_v4 import main as alpha_clinician_main


def main(argv: list[str] | None = None) -> int:
    """Launch the current local clinician Alpha surface."""
    return alpha_clinician_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
