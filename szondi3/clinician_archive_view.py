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
_VECTOR_GROUPS = (
    ("S", ("h", "s")),
    ("P", ("e", "hy")),
    ("Sch", ("k", "p")),
    ("C", ("d", "m")),
)


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
    return json.loads(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )


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
    _require_list(formal.get("calculations"), "report.formal.calculations")
    findings = _require_list(report.get("findings"), "report.findings")
    _require_list(report.get("limits_and_anti_inferences"), "report.limits_and_anti_inferences")
    _require_dict(report.get("status"), "report.status")
    _require_dict(report.get("experimental_complement"), "report.experimental_complement")
    _require_list(report.get("longitudinal"), "report.longitudinal")
    _require_list(report.get("provenance"), "report.provenance")
    release = _require_dict(report.get("release"), "report.release")
    _require_dict(report.get("technical_audit"), "report.technical_audit")

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
        raise ValueError(
            "Snapshot arhivat conține context clinic manual interzis în store-ul necriptat"
        )
    if not isinstance(synthesis, dict) or synthesis.get("text") is not None:
        raise ValueError(
            "Snapshot arhivat conține sinteză clinică manuală interzisă în store-ul necriptat"
        )

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

    complement_count = sum(
        1 for item in archived.protocol_payload if item.get("complement") is not None
    )
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
        value = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(", ", ": "),
        )
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


def _finding_block(finding: Any) -> str:
    if not isinstance(finding, dict):
        raise ValueError("Snapshot arhivat invalid: constatare non-obiect")
    scope = finding.get("scope")
    profile = finding.get("profile_number")
    location = str(scope) if profile is None else f"{scope} {profile}"
    anti = finding.get("anti_inferences") or []
    if not isinstance(anti, list):
        raise ValueError("Snapshot arhivat invalid: anti_inferences non-listă")
    anti_html = ""
    if anti:
        anti_html = (
            '<div class="boundary"><strong>Limite / anti-inferențe</strong><ul>'
            + "".join(f"<li>{_text(item)}</li>" for item in anti)
            + "</ul></div>"
        )
    return (
        '<article class="finding">'
        f'<p class="meta">{_text(location)} · {_text(finding.get("assertion_mode"))} · {_text(finding.get("source_strength_note"))}</p>'
        f'<p>{_text(finding.get("statement"))}</p>{anti_html}'
        f'<details><summary>Identitate tehnică</summary><code>{_text(finding.get("claim_id"))}</code></details>'
        '</article>'
    )


def _render_findings(view: ArchivedAssessmentView) -> str:
    blocks = [_finding_block(item) for item in view.report_payload["findings"]]
    return "".join(blocks) or '<p class="empty">Snapshot-ul nu conține constatări active.</p>'


def _render_calculations(view: ArchivedAssessmentView) -> str:
    calculations = view.report_payload["formal"]["calculations"]
    rows: list[str] = []
    for item in calculations:
        if not isinstance(item, dict):
            raise ValueError("Snapshot arhivat invalid: calcul non-obiect")
        rows.append(
            '<tr>'
            f'<th>{_text(item.get("name"))}</th>'
            f'<td>{_text(item.get("state"))}</td>'
            f'<td>{_text(item.get("value"))}</td>'
            f'<td>{_text(item.get("note"))}</td>'
            '</tr>'
        )
    if not rows:
        return '<p class="empty">Snapshot-ul nu conține calcule de serie.</p>'
    return (
        '<table><thead><tr><th>Calcul</th><th>Stare</th><th>Valoare</th><th>Notă</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )


def _render_boundaries(view: ArchivedAssessmentView) -> str:
    boundaries = view.report_payload["limits_and_anti_inferences"]
    blocks: list[str] = []
    for item in boundaries:
        if not isinstance(item, dict):
            raise ValueError("Snapshot arhivat invalid: limită non-obiect")
        anti = item.get("anti_inferences") or []
        blocks.append(
            '<details class="boundary-record"><summary>'
            f'{_text(item.get("scope"))} · {_text(item.get("claim_id"))}</summary>'
            f'<p>{_text(item.get("statement"))}</p>'
            + ("<ul>" + "".join(f"<li>{_text(value)}</li>" for value in anti) + "</ul>" if anti else "")
            + '</details>'
        )
    return "".join(blocks) or '<p class="empty">Nicio limită suplimentară în snapshot.</p>'


def _uncertainty_block(item: Any) -> str:
    if not isinstance(item, dict):
        raise ValueError("Snapshot arhivat invalid: incertitudine non-obiect")
    profile = item.get("profile_number")
    scope = item.get("scope")
    location = str(scope) if profile is None else f"{scope} {profile}"
    return (
        '<article class="uncertainty">'
        f'<p class="meta">{_text(location)} · {_text(item.get("kind"))} · {_text(item.get("claim_id"))}</p>'
        f'<p>{_text(item.get("message"))}</p>'
        '</article>'
    )


def _render_status(view: ArchivedAssessmentView) -> str:
    status = view.report_payload["status"]
    unresolved = _require_list(status.get("unresolved"), "report.status.unresolved")
    blocked = _require_list(status.get("blocked"), "report.status.blocked")
    suppressed = _require_list(status.get("suppressed"), "report.status.suppressed")
    unresolved_html = "".join(_uncertainty_block(item) for item in unresolved)
    blocked_html = "".join(_uncertainty_block(item) for item in blocked)
    suppressed_rows: list[str] = []
    for item in suppressed:
        if not isinstance(item, dict):
            raise ValueError("Snapshot arhivat invalid: claim neactivat non-obiect")
        profile = item.get("profile_number")
        scope = item.get("scope")
        location = str(scope) if profile is None else f"{scope} {profile}"
        suppressed_rows.append(
            '<tr>'
            f'<td>{_text(location)}</td><td><code>{_text(item.get("claim_id"))}</code></td>'
            f'<td>{_text(item.get("activation_status"))}</td>'
            f'<td>{_text(item.get("missing_facts"))}</td><td>{_text(item.get("missing_context"))}</td>'
            '</tr>'
        )
    suppressed_html = (
        '<details><summary>Claim-uri neactivate păstrate în snapshot '
        f'({len(suppressed)})</summary><table><thead><tr><th>Scop</th><th>Claim</th><th>Stare</th><th>Fapte lipsă</th><th>Context lipsă</th></tr></thead>'
        f'<tbody>{"".join(suppressed_rows)}</tbody></table></details>'
        if suppressed_rows
        else '<p class="empty">Niciun claim neactivat în snapshot.</p>'
    )
    return (
        '<h3>Nerezolvat</h3>'
        + (unresolved_html or '<p class="empty">Nicio stare nerezolvată.</p>')
        + '<h3>Blocat</h3>'
        + (blocked_html or '<p class="empty">Nicio stare blocată.</p>')
        + '<h3>Audit de activare</h3>'
        + suppressed_html
    )


def _render_complement(view: ArchivedAssessmentView) -> str:
    complement = view.report_payload["experimental_complement"]
    findings = _require_list(complement.get("findings"), "report.experimental_complement.findings")
    uncertainties = _require_list(
        complement.get("uncertainties"),
        "report.experimental_complement.uncertainties",
    )
    evidence = _require_list(complement.get("evidence"), "report.experimental_complement.evidence")
    finding_html = "".join(_finding_block(item) for item in findings)
    uncertainty_html = "".join(_uncertainty_block(item) for item in uncertainties)
    evidence_html = ""
    if evidence:
        evidence_html = '<details><summary>Dovezi E.K.P. salvate</summary><pre>' + escape(
            json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2)
        ) + '</pre></details>'
    if not finding_html and not uncertainty_html and not evidence_html:
        return '<p class="empty">Snapshot-ul nu conține material E.K.P.</p>'
    return (
        '<h3>Constatări E.K.P.</h3>'
        + (finding_html or '<p class="empty">Nicio constatare E.K.P. activă.</p>')
        + '<h3>Stări E.K.P.</h3>'
        + (uncertainty_html or '<p class="empty">Nicio stare E.K.P. nerezolvată/blocată.</p>')
        + evidence_html
    )


def _render_longitudinal(view: ArchivedAssessmentView) -> str:
    comparisons = view.report_payload["longitudinal"]
    if not comparisons:
        return '<p class="empty">Snapshot-ul nu conține comparații longitudinale.</p>'
    blocks: list[str] = []
    for item in comparisons:
        if not isinstance(item, dict):
            raise ValueError("Snapshot arhivat invalid: comparație longitudinală non-obiect")
        issues = item.get("comparability_issues") or []
        issue_html = "".join(
            f'<li><strong>{_text(issue.get("code"))}</strong>: {_text(issue.get("detail"))}</li>'
            for issue in issues
            if isinstance(issue, dict)
        )
        raw = json.dumps(item, ensure_ascii=False, sort_keys=True, indent=2)
        blocks.append(
            '<article class="longitudinal">'
            f'<h3>{_text(item.get("case_id_a"))} → {_text(item.get("case_id_b"))}</h3>'
            '<p class="boundary">Comparație structurală salvată; viewer-ul arhivei nu atribuie sens clinic schimbării.</p>'
            + (f'<ul>{issue_html}</ul>' if issue_html else '')
            + f'<details><summary>Toate diferențele structurale salvate</summary><pre>{escape(raw)}</pre></details>'
            + '</article>'
        )
    return "".join(blocks)


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
    provenance = view.report_payload["provenance"]
    blocks: list[str] = []
    for item in provenance:
        if not isinstance(item, dict):
            raise ValueError("Snapshot arhivat invalid: provenance item non-obiect")
        anchors = item.get("source_anchors") or []
        if not isinstance(anchors, list):
            raise ValueError("Snapshot arhivat invalid: source_anchors non-listă")
        anchor_html = "".join(
            '<li>'
            f'{_text(anchor.get("stream"))} · {_text(anchor.get("unit_start"))}–{_text(anchor.get("unit_end"))} · pagina tipărită {_text(anchor.get("printed_page"))}'
            + (f' · {_text(anchor.get("pdf_path"))}' if anchor.get("pdf_path") else '')
            + (f'<br><em>{_text(anchor.get("visual_arbitration_note"))}</em>' if anchor.get("visual_arbitration_note") else '')
            + '</li>'
            for anchor in anchors
            if isinstance(anchor, dict)
        )
        scope_notes = item.get("scope_notes") or []
        blocks.append(
            '<details class="provenance"><summary>'
            f'{_text(item.get("doctrine_id"))} · {_text(item.get("source_id"))} · {_text(item.get("review_status"))}'
            '</summary>'
            f'<p><strong>Forță:</strong> {_text(item.get("assertion_strength"))}</p>'
            f'<p><strong>Doctrină:</strong> {_text(item.get("doctrinal_statement"))}</p>'
            f'<p><strong>Redare română:</strong> {_text(item.get("romanian_rendering"))}</p>'
            f'<blockquote>{_text(item.get("source_excerpt"))}</blockquote>'
            + (f'<ul>{anchor_html}</ul>' if anchor_html else '')
            + (
                '<p><strong>Note de scop:</strong></p><ul>'
                + "".join(f'<li>{_text(note)}</li>' for note in scope_notes)
                + '</ul>'
                if scope_notes
                else ''
            )
            + '</details>'
        )
    return "".join(blocks) or '<p class="empty">Snapshot-ul nu conține proveniență doctrinară.</p>'


def _render_key_value_table(payload: dict[str, Any]) -> str:
    return '<table class="kv"><tbody>' + "".join(
        f'<tr><th>{_text(key)}</th><td>{_text(value)}</td></tr>'
        for key, value in payload.items()
    ) + '</tbody></table>'


def _render_release_and_audit(view: ArchivedAssessmentView) -> str:
    release = view.report_payload["release"]
    audit = view.report_payload["technical_audit"]
    return (
        '<h3>Manifest de release salvat</h3>'
        + _render_key_value_table(release)
        + '<h3>Audit structural salvat</h3>'
        + _render_key_value_table(audit)
        + '<h3>Identitatea arhivei</h3><table class="kv"><tbody>'
        f'<tr><th>payload_sha256</th><td><code>{_text(view.payload_sha256)}</code></td></tr>'
        f'<tr><th>archive_schema_version</th><td>{view.schema_version}</td></tr>'
        '</tbody></table>'
    )


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
<section><h2>Calcule deterministe salvate</h2>{_render_calculations(view)}</section>
<section><h2>Constatări salvate</h2>{_render_findings(view)}</section>
<section><h2>Limite salvate</h2><p class="meta">Aceste limite provin din raportul istoric; nu sunt regenerate de viewer.</p>{_render_boundaries(view)}</section>
<section><h2>Stări nerezolvate, blocate și neactivate</h2>{_render_status(view)}</section>
<section><h2>Complement experimental (E.K.P.) salvat</h2>{_render_complement(view)}</section>
<section><h2>Comparații longitudinale salvate</h2>{_render_longitudinal(view)}</section>
<section><h2>Protocol administrat</h2><p class="meta">Alegerile de cartele sunt păstrate ca fapte de administrare; deschiderea arhivei nu le transformă într-un caz clinic curent.</p>{_render_protocol(view)}</section>
<section><h2>Surse / proveniență din snapshot</h2>{_render_provenance(view)}</section>
<section><h2>Trasabilitate tehnică istorică</h2>{_render_release_and_audit(view)}</section>
<section><h2>Integrare manuală</h2><p class="boundary"><strong>Redactată intenționat.</strong> Contextul și sinteza manuală a clinicianului nu sunt persistate în arhiva SQLite necriptată.</p></section>
<section><h2>Audit snapshot</h2><details><summary>Raportul JSON salvat</summary><pre>{escape(raw_report)}</pre></details><details><summary>Protocolul JSON salvat</summary><pre>{escape(raw_protocol)}</pre></details></section>
</section>
<style>
.archive-snapshot section{{margin:1.6rem 0}} .summary-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0}}
.summary-grid>div{{border:1px solid #d0d7de;border-radius:.5rem;padding:.7rem}} .table-wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;margin:.6rem 0}} th,td{{border:1px solid #d0d7de;padding:.45rem;text-align:left;vertical-align:top}}
.matrix th,.matrix td{{text-align:center;white-space:nowrap}} .matrix .reaction{{font-size:1.08rem;font-weight:700}} .finding,.provenance,.uncertainty,.longitudinal{{border:1px solid #d0d7de;border-radius:.5rem;padding:.8rem 1rem;margin:.7rem 0}}
.boundary,.boundary-record{{background:#f6f8fa;padding:.5rem .8rem}} blockquote{{margin:.7rem 0;padding:.6rem .8rem;border-left:3px solid #d0d7de;background:#f6f8fa}} pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f8fa;padding:.8rem}} code{{overflow-wrap:anywhere}} .kv th{{width:28%}}
@media(max-width:760px){{.summary-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
</style>
"""
