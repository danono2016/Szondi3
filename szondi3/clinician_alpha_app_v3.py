"""Current Alpha launcher wired to the plan-bound clinical report writer V3.

The underlying clinician application remains ``AlphaClinicianApp``. This layer
selects the V3 writer through its low-latency provider profile, keeps the ordinary
report surface in direct Romanian, and adds immediate browser feedback while the
synchronous AI request is running; administration, archive, legacy import and report
semantics remain unchanged.
"""

from __future__ import annotations

import argparse
from functools import partial
import os
from pathlib import Path

from .clinical_archive import SQLiteClinicalArchive
from .clinical_report_ai_fast import (
    DEFAULT_FAST_TIMEOUT_SECONDS,
    run_openai_clinical_report_fast,
)
from .clinician_alpha_app import AlphaClinicianApp, ClinicalReportAIRunner
from .clinician_app import make_local_clinician_server


_AI_REQUEST_TIMEOUT_SECONDS = DEFAULT_FAST_TIMEOUT_SECONDS

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
    note.textContent = ' Generarea este optimizată pentru latență; limita de siguranță rămâne aproximativ 3 minute.';
    form.appendChild(note);
  }
});
</script>"""


_REPORT_LANGUAGE_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    # Clinician-surface framing: keep provenance available without sounding like an audit log.
    ("Semnificații Szondiene autorizate", "Baza interpretativă"),
    (
        "Aceste afirmații există independent de AI și reprezintă stratul interpretativ executabil al cazului.",
        "Aceste sensuri sunt stabilite înaintea redactării AI și constituie baza interpretării de mai jos.",
    ),
    (
        "Textul de mai jos face expansiune semantică numai asupra semnificațiilor deja autorizate.",
        "Textul de mai jos dezvoltă numai sensurile deja stabilite pentru acest profil.",
    ),
    (
        "P2B și raportul folosesc numai morfologia formală furnizată.",
        "Interpretarea și raportul folosesc numai morfologia formală furnizată.",
    ),
    ("În termenii lui Szondi", "Sensul szondian"),
    ("Limită relevantă", "Ce nu rezultă de aici"),
    # Phrase-level translations precede token-level replacements so Romanian grammar survives.
    ("Abwehr-ul unei Triebgefahr", "apărarea față de o primejdie pulsională"),
    # Romanian renderings of recurring source-language terms in deterministic statements.
    ("narzißtische Formen des Ich-Schutzes", "forme narcisice de protecție a Eului"),
    ("kollektive Introinflation", "introinflație colectivă"),
    ("introjektive Identifizierung", "identificare introiectivă"),
    ("stellungnehmendes Ich", "Eul care ia poziție"),
    ("Verdoppelung", "dublare"),
    ("Vollkommenheit", "perfecțiune"),
    ("Einverleibung", "încorporare"),
    ("Inbesitznahme", "luare în posesie"),
    ("Personabildung", "formarea Personei"),
    ("a doua cale a formarea Personei", "a doua cale de formare a Personei"),
    ("Kontaktsperre", "blocarea contactului"),
    ("Introinflation", "introinflație"),
    ("Introjektion", "introiecție"),
    ("Identifizierung", "identificare"),
    ("Identität", "identitate"),
    ("Alleshaben", "a avea totul"),
    ("Allessein", "a fi totul"),
    ("Überdruck", "suprapresiune"),
    ("Deflation", "deflație/limitare"),
    ("Ich-Bild-ul", "imaginea Eului"),
    ("Triebgefahr", "primejdie pulsională"),
    ("Abwehr-ul", "apărarea"),
    ("Stellung", "poziție"),
    ("Inflation", "inflație"),
    ("am häufigsten", "cel mai frecvent"),
    ("inzestuös", "incestuoasă"),
    ("bisexuell", "bisexuală"),
    ("invertiert", "inversată"),
    ("pervers", "perversă"),
)


def _normalize_clinician_report_language(html: str) -> str:
    """Translate presentation-only legacy terminology without changing P2B storage."""
    if not isinstance(html, str):
        raise TypeError("Clinical report language normalization requires HTML text")
    rendered = html
    for source, target in _REPORT_LANGUAGE_REPLACEMENTS:
        rendered = rendered.replace(source, target)
    return rendered


def _inject_ai_submit_feedback(html: str) -> str:
    """Add a one-shot loading state without changing report or request semantics."""
    if not isinstance(html, str):
        raise TypeError("AI submit feedback requires HTML text")
    if _AI_SUBMIT_FEEDBACK in html or '</body>' not in html:
        return html
    return html.replace('</body>', _AI_SUBMIT_FEEDBACK + '</body>', 1)


def _run_configured_ai(packet, *, api_key: str):
    """Run V3 through the latency-tuned Responses API profile."""
    return run_openai_clinical_report_fast(
        packet,
        api_key=api_key,
        timeout_seconds=_AI_REQUEST_TIMEOUT_SECONDS,
    )


class AlphaClinicianAppV3(AlphaClinicianApp):
    """Alpha shell with V3 writing, Romanian report surface and submit feedback."""

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        status, html = super()._resolve(path, query_string)
        if path == '/report' and status == '200 OK':
            html = _normalize_clinician_report_language(html)
            if self.ai_available:
                html = _inject_ai_submit_feedback(html)
        return status, html


def _configured_ai_runner() -> ClinicalReportAIRunner | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    return partial(_run_configured_ai, api_key=api_key)


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
