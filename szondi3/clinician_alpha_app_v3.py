"""Current Alpha launcher wired to the plan-bound clinical report writer V3.

The underlying clinician application remains ``AlphaClinicianApp``. This layer
selects the V3 writer and adds immediate browser feedback while a synchronous AI
request is running; administration, archive, legacy import and report semantics
remain unchanged.
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


_AI_SUBMIT_FEEDBACK = """<script>
document.addEventListener('submit', function (event) {
  var form = event.target;
  if (!form || !form.matches('form[action="/report/ai"]')) return;
  var button = form.querySelector('button[type="submit"]');
  if (button) {
    button.disabled = true;
    button.textContent = 'Se generează… vă rugăm așteptați';
  }
  if (!form.querySelector('[data-ai-wait-note]')) {
    var note = document.createElement('span');
    note.setAttribute('data-ai-wait-note', 'true');
    note.className = 'quiet';
    note.textContent = ' Cererea poate dura până la aproximativ 90 de secunde.';
    form.appendChild(note);
  }
});
</script>"""


def _inject_ai_submit_feedback(html: str) -> str:
    """Add a one-shot loading state without changing report or request semantics."""
    if not isinstance(html, str):
        raise TypeError("AI submit feedback requires HTML text")
    if _AI_SUBMIT_FEEDBACK in html or '</body>' not in html:
        return html
    return html.replace('</body>', _AI_SUBMIT_FEEDBACK + '</body>', 1)


class AlphaClinicianAppV3(AlphaClinicianApp):
    """Alpha shell with the V3 writer and visible synchronous-submit feedback."""

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        status, html = super()._resolve(path, query_string)
        if path == '/report' and self.ai_available and status == '200 OK':
            html = _inject_ai_submit_feedback(html)
        return status, html


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
    app = AlphaClinicianAppV3(None, archive=archive, ai_report_runner=ai_runner)
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
