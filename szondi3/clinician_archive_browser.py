"""Read-only archive browsing extension for the local clinician app.

This shell intercepts only archive navigation. Historical assessments are loaded
through ``SQLiteClinicalArchive.load`` and rendered from the stored snapshot; they
are never promoted into ``_live_runs`` and are never re-executed under the current
P1/P2B/doctrine checkout.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, quote

from .clinical_archive import SQLiteClinicalArchive
from .clinician_app import ClinicianApp, _navigation, _page, make_local_clinician_server
from .clinician_archive_view import (
    build_archived_assessment_view,
    render_archived_assessment_view_fragment,
)
from .clinician_workspace import ClinicianWorkspace


class ArchiveBrowsingClinicianApp(ClinicianApp):
    """Clinician app with immutable historical snapshot navigation."""

    def __init__(
        self,
        workspace: ClinicianWorkspace | None = None,
        *,
        archive: SQLiteClinicalArchive | None = None,
    ) -> None:
        super().__init__(workspace, archive=archive)

    def _archive_index_page(self) -> str:
        if self.archive is None:
            content = (
                '<p class="meta">Arhiva durabilă nu este configurată pentru această sesiune. '
                'Evaluările finalizate rămân numai în memoria procesului.</p>'
            )
        else:
            rows: list[str] = []
            for item in self.archive.list():
                href = "/archive/view?assessment_id=" + quote(item.assessment_id, safe="")
                rows.append(
                    '<article class="card">'
                    f'<h2>{escape(item.assessment_id)}</h2>'
                    f'<p class="meta">Git <code>{escape(item.git_commit_sha)}</code><br>'
                    f'Doctrină <code>{escape(item.doctrine_snapshot_id)}</code><br>'
                    f'P2B <code>{escape(item.p2b_release_id)}</code><br>'
                    f'Payload <code>{escape(item.payload_sha256)}</code></p>'
                    '<p class="meta">Snapshot istoric imuabil; textul manual al clinicianului nu este persistat de acest store necriptat.</p>'
                    f'<p><a href="{escape(href, quote=True)}"><strong>Deschide snapshot-ul</strong></a></p>'
                    '</article>'
                )
            content = "".join(rows) or '<p class="meta">Arhiva este goală.</p>'
        return _page(
            "Szondi3 — arhivă",
            _navigation(self.workspace is not None)
            + '<h1>Arhivă locală pseudonimizată</h1>'
            + '<div class="notice"><strong>Istoric read-only.</strong> Deschiderea unei evaluări arhivate nu o rerulează sub versiunea clinică actuală și nu o introduce automat în comparațiile longitudinale curente.</div>'
            + content,
        )

    def _archive_detail_page(self, query_string: str) -> tuple[str, str]:
        if self.archive is None:
            return (
                "409 Conflict",
                _page(
                    "Szondi3 — arhivă indisponibilă",
                    _navigation(self.workspace is not None)
                    + '<h1>Arhivă indisponibilă</h1><p>Arhiva durabilă nu este configurată.</p>',
                ),
            )
        query = parse_qs(query_string, keep_blank_values=True)
        values = query.get("assessment_id", [])
        if len(values) != 1 or not values[0]:
            return (
                "400 Bad Request",
                _page(
                    "Szondi3 — identificator invalid",
                    _navigation(self.workspace is not None)
                    + '<h1>Identificator invalid</h1><p>Este necesar un singur assessment_id pseudonimizat.</p>',
                ),
            )
        assessment_id = values[0]
        try:
            archived = self.archive.load(assessment_id)
            view = build_archived_assessment_view(archived)
            fragment = render_archived_assessment_view_fragment(view)
        except KeyError:
            return (
                "404 Not Found",
                _page(
                    "Szondi3 — snapshot inexistent",
                    _navigation(self.workspace is not None)
                    + f'<h1>Snapshot inexistent</h1><p>{escape(assessment_id)}</p>',
                ),
            )
        except (RuntimeError, TypeError, ValueError) as exc:
            return (
                "409 Conflict",
                _page(
                    "Szondi3 — snapshot invalid",
                    _navigation(self.workspace is not None)
                    + '<h1>Snapshot invalid</h1>'
                    + f'<div class="notice error">{escape(str(exc))}</div>'
                    + '<p>Înregistrarea nu este rerulată sau reparată automat.</p>',
                ),
            )
        return (
            "200 OK",
            _page(
                f"Szondi3 — arhivă {assessment_id}",
                _navigation(self.workspace is not None)
                + '<p><a href="/archive">← Înapoi la arhivă</a></p>'
                + fragment,
            ),
        )

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        if path == "/archive":
            return "200 OK", self._archive_index_page()
        if path == "/archive/view":
            return self._archive_detail_page(query_string)
        return super()._resolve(path, query_string)


def main(argv: list[str] | None = None) -> int:
    """Launch the clinician shell with immutable archive browsing enabled."""
    parser = argparse.ArgumentParser(description="Szondi3 local clinician application with archive browser")
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
    app = ArchiveBrowsingClinicianApp(None, archive=archive)
    server = make_local_clinician_server(app, host="127.0.0.1", port=args.port)
    print(f"Szondi3 clinician app + archive browser: http://127.0.0.1:{server.server_port}/")
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
