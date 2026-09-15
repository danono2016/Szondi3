"""Experimental Alpha launcher wired to the global clinical report writer V4."""

from __future__ import annotations

import argparse
from functools import partial
import os
from pathlib import Path

from .clinical_archive import SQLiteClinicalArchive
from .clinical_report_ai import _response_output_text
from .clinical_report_ai_v4 import (
    DEFAULT_V4_TIMEOUT_SECONDS,
    ClinicalReportAIV4Result,
    parse_openai_clinical_report_response_v4,
)
from .clinical_report_ai_v4_transport import (
    request_openai_clinical_report_response_v4_strict,
)
from .clinician_alpha_app import ClinicalReportAIRunner
from .clinician_alpha_app_v3 import (
    AlphaClinicianAppV3,
    _inject_ai_submit_feedback,
    _normalize_clinician_report_language,
)
from .clinician_alpha_report_renderer_v4 import render_clinician_alpha_report_v4_html
from .clinician_app import make_local_clinician_server


_AI_REQUEST_TIMEOUT_SECONDS = DEFAULT_V4_TIMEOUT_SECONDS


def _normalize_provider_response_language(response: dict) -> dict:
    """Translate known source vocabulary before the strict V4 parser runs.

    Structural metadata is deliberately not repaired here.  The provider-side JSON
    schema now matches the parser slot contract, so a replayed/malformed ``kind``
    remains malformed and is rejected instead of being silently canonicalized.
    """
    if not isinstance(response, dict):
        raise TypeError("Clinical report provider response must be a dictionary")

    output_text = _normalize_clinician_report_language(_response_output_text(response))
    normalized = dict(response)
    normalized["output_text"] = output_text
    return normalized


def _run_configured_ai(packet, *, api_key: str):
    response = request_openai_clinical_report_response_v4_strict(
        packet,
        api_key=api_key,
        timeout_seconds=_AI_REQUEST_TIMEOUT_SECONDS,
    )
    return parse_openai_clinical_report_response_v4(
        packet,
        _normalize_provider_response_language(response),
    )


def _configured_ai_runner() -> ClinicalReportAIRunner | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    return partial(_run_configured_ai, api_key=api_key)


class AlphaClinicianAppV4(AlphaClinicianAppV3):
    """Experimental shell rendering V4 output as one global report."""

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        if path == "/report":
            try:
                workspace = self._workspace_required()
            except LookupError:
                return super()._resolve(path, query_string)
            result = self._current_ai_result(workspace)
            if isinstance(result, ClinicalReportAIV4Result):
                html = render_clinician_alpha_report_v4_html(
                    workspace,
                    ai_result=result,
                    ai_available=self.ai_available,
                    csrf_token=self.csrf_token if self.ai_available else None,
                    ai_error=self._ai_error,
                )
                html = self._legacy_notice(html, workspace.current.case_id)
                html = _normalize_clinician_report_language(html)
                if self.ai_available:
                    html = _inject_ai_submit_feedback(html)
                return "200 OK", html
        return super()._resolve(path, query_string)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Szondi3 experimental V4 clinician application"
    )
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
    app = AlphaClinicianAppV4(None, archive=archive, ai_report_runner=ai_runner)
    server = make_local_clinician_server(app, host="127.0.0.1", port=args.port)
    ai_state = "AI clinic configurat" if ai_runner is not None else "AI clinic neconfigurat"
    print(
        "Szondi3 Alpha V4 experimental: "
        f"http://127.0.0.1:{server.server_port}/ ({ai_state})"
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
