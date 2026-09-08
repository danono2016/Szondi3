"""Default Szondi3 product launcher.

``python -m szondi3`` opens the archive-enabled local clinician application. The
entrypoint delegates to the existing archive-browser shell and adds no clinical
calculation or interpretation semantics of its own.
"""

from __future__ import annotations

from .clinician_archive_browser import main as archive_browser_main


def main(argv: list[str] | None = None) -> int:
    """Launch the current local clinician product surface."""
    return archive_browser_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
