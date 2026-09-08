"""Read-only browser projection of one durable archived assessment.

The archive view consumes only the checksum-verified snapshot returned by
``SQLiteClinicalArchive.load``. It deliberately does not rebuild a historical
``ClinicalCaseRun`` and never re-runs P1/P2B under the current checkout. The stored
report/protocol remain the historical authority for this surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
import json
from typing import Any

from .clinical_archive import ArchivedAssessment


_ARCHIVE_VIEW_SCHEMA_VERSION = 1
_FACTOR_ORDER = ("h", "s", "e", "hy", "k", "p", "d", "m")
_VECTOR_GROUPS = (("S", ("h", "s")), ("P", ("e", "hy")), ("Sch", ("k", "p")), ("C", ("d", "m")))


@dataclass(frozen=True, slots=True)
class ArchivedAssessmentView:
    assessment_id: str
    schema_version: int
    payload_sha256: str
    git_commit_sha: str
    doctrine_snapshot_id: str
    p2b_release_id: str
    profile_count: int
    finding_count: int
    protocol_profile_count: int
    complement_profile_count: int
    report_payload: dict[str, Any]
    protocol_payload: tuple[dict[str, Any], ...]


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"Snapshot arhivat invalid: {label} trebuie să fie obiect")
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"Snapshot arhivat invalid: {label} trebuie să fie listă")
    return value


def _canonical_copy(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def build_archived_assessment_view(archived: ArchivedAssessment) -> ArchivedAssessmentView:
    """Validate and project one stored snapshot without historical re-execution."""
    if not isinstance(archived, ArchivedAssessment):
        raise TypeError("Archive view requires an ArchivedAssessment")
    summary = archived.summary
    if summary.schema_version != _ARCHIVE_VIEW_SCHEMA_VERSION:
        raise ValueError(
            f"Versiune de arhivă nesuportată de acest viewer: {summary.schema_version}"
        )

    report = _require_dict(archived.report_payload, "report_payload")
    report_summary = _require_dict(report.get("summary"), "report.summary")
    formal = _require_dict(report.get("formal"), "report.formal")
    _require_list(formal.get("observations"), "report.formal.observations")
    findings = _require_list(report.get("findings"), "report.findings")
    release = _require_dict(report.get("release"), "report.release")

    if report_summary.get("current_case_id") != summary.assessment_id:
        raise ValueError("Snapshot arhivat invalid: identitatea raportului nu corespunde arhivei")
    if release.get("git_commit_sha") != summary.git_commit_sha:
        raise ValueError("Snapshot arhivat invalid: Git SHA diferă de metadatele arhivei")
    if release.get("doctrine_snapshot_id") != summary.doctrine_snapshot_id:
        raise ValueError("Snapshot arhivat invalid: doctrina diferă de metadatele arhivei")
    if release.get("p2b_release_id") != summary.p2b_release_id:
        raise ValueError("Snapshot arhivat invalid: P2B release diferă de metadatele arhivei")

    context = report.get("clinician_context")
    synthesis = report.get("clinician_synthesis")
    if context != []:
        raise ValueError("Snapshot arhivat conține context clinic manual interzis în store-ul necriptat")
    if not isinstance(synthesis, dict) or synthesis.get("text") is not None:
        raise ValueError("Snapshot arhivat conține sinteză clinică manuală interzisă în store-ul necriptat")

    try:
        profile_count = int(report_summary["profile_count"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Snapshot arhivat invalid: profile_count lipsește sau este invalid") from exc
    if profile_count != len(archived.protocol_payload):
        raise ValueError("Snapshot arhivat invalid: numărul de protocoale diferă de raport")
    try:
        stored_finding_count = int(report_summary["finding_count"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Snapshot arhivat invalid: finding_count lipsește sau este invalid") from exc
    if stored_finding_count != len(findings):
        raise ValueError("Snapshot arhivat invalid: finding_count diferă de lista de constatări")

    complement_count = sum(1 for item in archived.protocol_payload if item.get("complement") is not None)
    return ArchivedAssessmentView(
        assessment_id=summary.assessment_id,
        schema_version=summary.schema_version,
        payload_sha256=summary.payload_sha256,
        git_commit_sha=summary.git_commit_sha,
        doctrine_snapshot_id=summary.doctrine_snapshot_id,
        p2b_release_id=summary.p2b_release_id,
        profile_count=profile_count,
        finding_count=stored_finding_count,
        protocol_profile_count=len(archived.protocol_payload),
        complement_profile_count=complement_count,
        report_payload=_canonical_copy(report),
        protocol_payload=tuple(_canonical_copy(item) for item in archived.protocol_payload),
    )


def _text(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(", ", ": "))
    return escape(str(value), quote=True)


def _render_profile_matrix(view: ArchivedAssessmentView) -> str:
    observations = view.report_payload["formal"]["observations"]
    rows: list[str] = []
    for profile in observations:
        if not isinstance(profile, dict):
            raise ValueError("Snapshot arhivat invalid: observație formală non-obiect")
        factors = profile.get("factors")
        if not isinstance(factors, list):
            raise ValueError("Snapshot arhivat invalid: factorii profilului lipsesc")
        by_factor = {
            item.get("factor"): item
            for item in factors
            if isinstance(item, dict) and isinstance(item.get("factor"), str)
        }
        if set(by_factor) != set(_FACTOR_ORDER):
            raise ValueError("Snapshot arhivat invalid: profilul nu conține exact cei opt factori")
        cells = "".join(
            '<td class="reaction" title="+ {plus} / - {minus} · quantum {quantum} · null forțat {forced}">{symbol}</td>'.format(
                plus=_text(by_factor[factor].get("sympathetic")),
                minus=_text(by_factor[factor].get("unsympathetic")),
                quantum=_text(by_factor[factor].get("quantum_level")),
                forced=_text(by_factor[factor].get("forced_null")),
                symbol=_text(by_factor[factor].get("symbol")),
            )
            for factor in _FACTOR_ORDER
        )
        rows.append(f'<tr><th>{_text(profile.get("profile_number"))}</th>{cells}</tr>')

    group_headers = "".join(
        f'<th colspan="2">{escape(vector)}</th>' for vector, _ in _VECTOR_GROUPS
    )
    factor_headers = "".join(f"<th>{factor}</th>" for factor in _FACTOR_ORDER)
    return (
        '<div class="table-wrap"><table class="matrix"><thead>'
        f'<tr><th rowspan="2">Profil</th>{group_headers}</tr><tr>{factor_headers}</tr>'
        f'</thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def _render_findings(view: ArchivedAssessmentView) -> str:
    blocks: list[str] = []
    for finding in view.report_payload["findings"]:
        if not isinstance(finding, dict):
            raise ValueError("Snapshot arhivat invalid: constatare non-obiect")
        scope = finding.get("scope")
        profile = finding.get("profile_number")
        location = str(scope) if profile is None else f"{scope} {profile}"
        anti = finding.get("anti_inferences") or []
        anti_html = ""
        if anti:
            anti_html = '<div class="boundary"><strong>Limite / anti-inferențe</strong><ul>' + "".join(
                f"<li>{_text(item)}</li>" for item in anti
            ) + "</ul></div>"
        blocks.append(
            '<article class="finding">'
            f'<p class="meta">{_text(location)} · {_text(finding.get("assertion_mode"))} · {_text(finding.get("source_strength_note"))}</p>'
            f'<p>{_text(finding.get("statement"))}</p>{anti_html}'
            f'<details><summary>Identitate tehnică</summary><code>{_text(finding.get("claim_id"))}</code></details>'
            '</article>'
        )
    return "".join(blocks) or '<p class="empty">Snapshot-ul nu conține constatări active.</p>'


def _render_protocol(view: ArchivedAssessmentView) -> str:
    tests: list[str] = []
    for test_number, item in enumerate(view.protocol_payload, start=1):
        foreground = item.get("foreground")
        if not isinstance(foreground, list):
            raise ValueError("Snapshot arhivat invalid: protocol foreground lipsă")
        rows = "".join(
            '<tr>'
            f'<th>{_text(entry.get("series"))}</th>'
            f'<td>{_text(entry.get("sympathetic"))}</td>'
            f'<td>{_text(entry.get("unsympathetic"))}</td>'
            '</tr>'
            for entry in foreground
            if isinstance(entry, dict)
        )
        complement = item.get("complement")
        complement_html = ""
        if complement is not None:
            if not isinstance(complement, list):
                raise ValueError("Snapshot arhivat invalid: complement non-listă")
            complement_rows = "".join(
                '<tr>'
                f'<th>{_text(entry.get("series"))}</th>'
                f'<td>{_text(entry.get("relative_sympathetic"))}</td>'
                f'<td>{_text(entry.get("relative_unsympathetic"))}</td>'
                '</tr>'
                for entry in complement
                if isinstance(entry, dict)
            )
            complement_html = (
                '<h4>E.K.P. administrat</h4><table><thead><tr><th>Seria</th><th>Relativ simpatice</th><th>Relativ antipatice</th></tr></thead>'
                f'<tbody>{complement_rows}</tbody></table>'
            )
        tests.append(
            f'<details><summary>Protocol profil {test_number}</summary>'
            '<table><thead><tr><th>Seria</th><th>Simpatice</th><th>Antipatice</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>{complement_html}</details>'
        )
    return "".join(tests)


def _render_provenance(view: ArchivedAssessmentView) -> str:
    provenance = view.report_payload.get("provenance") or []
    if not isinstance(provenance, list):
        raise ValueError("Snapshot arhivat invalid: provenance non-listă")
    blocks: list[str] = []
    for item in provenance:
        if not isinstance(item, dict):
            raise ValueError("Snapshot arhivat invalid: provenance item non-obiect")
        anchors = item.get("anchors") or item.get("source_anchors") or []
        excerpt = item.get("source_excerpt")
        blocks.append(
            '<article class="provenance">'
            f'<p class="meta">{_text(item.get("doctrine_id"))} · {_text(item.get("source_id"))} · {_text(item.get("source_strength"))}</p>'
            f'<p>{_text(item.get("statement"))}</p>'
            f'<blockquote>{_text(excerpt)}</blockquote>'
            f'<p class="meta">Ancore: {_text(anchors)}</p>'
            '</article>'
        )
    return "".join(blocks) or '<p class="empty">Snapshot-ul nu conține proveniență doctrinară.</p>'


def render_archived_assessment_view_fragment(view: ArchivedAssessmentView) -> str:
    """Render a historical snapshot as read-only HTML; no current-runtime operations."""
    if not isinstance(view, ArchivedAssessmentView):
        raise TypeError("Archive renderer requires an ArchivedAssessmentView")
    report_summary = view.report_payload["summary"]
    raw_report = json.dumps(view.report_payload, ensure_ascii=False, sort_keys=True, indent=2)
    raw_protocol = json.dumps(view.protocol_payload, ensure_ascii=False, sort_keys=True, indent=2)
    return f"""
<section class="archive-snapshot">
<h1>Evaluare arhivată — {_text(view.assessment_id)}</h1>
<div class="notice"><strong>Snapshot istoric read-only.</strong> Această pagină nu rerulează protocolul, nu recalculează P1 și nu reactivează P2B sub versiunea curentă a aplicației. Afișează exclusiv protocolul și raportul salvate la momentul evaluării.</div>
<div class="summary-grid">
<div><strong>Profile</strong><br>{view.profile_count}</div><div><strong>Constatări</strong><br>{view.finding_count}</div><div><strong>E.K.P.</strong><br>{view.complement_profile_count}/{view.protocol_profile_count}</div><div><strong>Stare release</strong><br>{_text(report_summary.get("interpretation_release_state"))}</div>
</div>
<section><h2>Profil Szondi salvat</h2><p class="meta">Reacțiile sunt cele din snapshot-ul raportului. Detaliile numerice sunt disponibile prin tooltip; nu sunt recalculate.</p>{_render_profile_matrix(view)}</section>
<section><h2>Constatări salvate</h2>{_render_findings(view)}</section>
<section><h2>Protocol administrat</h2><p class="meta">Alegerile de cartele sunt păstrate ca fapte de administrare; deschiderea arhivei nu le transformă într-un caz clinic curent.</p>{_render_protocol(view)}</section>
<section><h2>Identitatea release-ului istoric</h2>
<table><tbody><tr><th>Git commit</th><td><code>{_text(view.git_commit_sha)}</code></td></tr><tr><th>Doctrine snapshot</th><td><code>{_text(view.doctrine_snapshot_id)}</code></td></tr><tr><th>P2B release</th><td><code>{_text(view.p2b_release_id)}</code></td></tr><tr><th>Payload SHA-256</th><td><code>{_text(view.payload_sha256)}</code></td></tr><tr><th>Schema arhivă</th><td>{view.schema_version}</td></tr></tbody></table>
</section>
<section><h2>Surse / proveniență din snapshot</h2>{_render_provenance(view)}</section>
<section><h2>Audit snapshot</h2><details><summary>Raportul JSON salvat</summary><pre>{escape(raw_report)}</pre></details><details><summary>Protocolul JSON salvat</summary><pre>{escape(raw_protocol)}</pre></details></section>
</section>
<style>
.archive-snapshot section{{margin:1.6rem 0}} .summary-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0}}
.summary-grid>div{{border:1px solid #d0d7de;border-radius:.5rem;padding:.7rem}} .table-wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;margin:.6rem 0}} th,td{{border:1px solid #d0d7de;padding:.45rem;text-align:left;vertical-align:top}}
.matrix th,.matrix td{{text-align:center;white-space:nowrap}} .matrix .reaction{{font-size:1.08rem;font-weight:700}} .finding,.provenance{{border:1px solid #d0d7de;border-radius:.5rem;padding:.8rem 1rem;margin:.7rem 0}}
.boundary{{background:#f6f8fa;padding:.5rem .8rem}} blockquote{{margin:.7rem 0;padding:.6rem .8rem;border-left:3px solid #d0d7de;background:#f6f8fa}} pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f8fa;padding:.8rem}} code{{overflow-wrap:anywhere}}
@media(max-width:760px){{.summary-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
</style>
"""
