"""Current Alpha launcher wired to the plan-bound clinical report writer V3.

The clinician application surface itself remains ``AlphaClinicianApp``. This thin
launcher changes only the configured AI writer, preserving administration, archive,
legacy import, report rendering and ephemeral AI-result behavior.
"""

from __future__ import annotations

import argparse
from functools import partial
import os
from pathlib import Path

from .clinical_archive import SQLiteClinicalArchive
from .clinical_report_ai_v3 import run_openai_clinical_report
from .clinician_alpha_app import AlphaClinicianApp, ClinicalReportAIRunner
from .clinician_app import make_local_clinician_server


def _configured_ai_runner() -> ClinicalReportAIRunner | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    return partial(run_openai_clinical_report, api_key=api_key)


def main(argv: list[str] | None = None) -> int:
    """Launch the current Alpha product with deterministic report planning + V3 writer."""
    parser = argparse.ArgumentParser(description="Szondi3 Alpha clinician application")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--archive",
        default=str(Path.home() / ".szondi3" / "clinical_archive.sqlite3"),
        help="SQLite archive path outside the repository",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Run without durable local assessment persistence",
    )
    args = parser.parse_args(argv)

    archive = None if args.no_archive else SQLiteClinicalArchive(args.archive)
    ai_runner = _configured_ai_runner()
    app = AlphaClinicianApp(None, archive=archive, ai_report_runner=ai_runner)
    server = make_local_clinician_server(app, host="127.0.0.1", port=args.port)
    ai_state = "AI clinic configurat" if ai_runner is not None else "AI clinic neconfigurat"
    print(
        f"Szondi3 Alpha: http://127.0.0.1:{server.server_port}/ "
        f"({ai_state})"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if archive is not None:
            archive.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
