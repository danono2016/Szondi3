"""Default Szondi3 Alpha product launcher.

``python -m szondi3`` opens the archive-enabled local clinician application with
the concise Alpha clinical report. Administration, deterministic calculation,
interpretation, archive and provenance remain in their existing authoritative
layers; the Alpha shell only changes the clinician-facing report surface and adds
explicit preview-only AI wording when configured.
"""

from __future__ import annotations

from .clinician_alpha_app import main as alpha_clinician_main


def main(argv: list[str] | None = None) -> int:
    """Launch the current local clinician Alpha surface."""
    return alpha_clinician_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
