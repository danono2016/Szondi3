"""Compact clinician-facing current-case projection.

This module turns the already-built ``ClinicianWorkspace`` into the primary visual
Szondi reading surface: one compact matrix of foreground profile reactions. It does
not calculate, normalize, interpret, or collapse reaction details. Full reaction
symbols, quantum level, raw sympathetic/unsympathetic counts, and forced-null state
remain separate fields so the compact UI can reveal details without changing P1.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape

from .clinician_workspace import ClinicianWorkspace
from .profile import VECTOR_FACTORS
from .stimuli import FACTORS


@dataclass(frozen=True, slots=True)
class CurrentCaseReactionCell:
    factor: str
    symbol: str
    sympathetic: int
    unsympathetic: int
    quantum_level: int
    forced_null: bool


@dataclass(frozen=True, slots=True)
class CurrentCaseProfileRow:
    profile_number: int
    reactions: tuple[CurrentCaseReactionCell, ...]

    def reaction(self, factor: str) -> CurrentCaseReactionCell:
        matches = tuple(item for item in self.reactions if item.factor == factor)
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate factor in current-case row: {factor}")
        return matches[0]


@dataclass(frozen=True, slots=True)
class CurrentCaseVectorGroup:
    vector: str
    factors: tuple[str, str]


@dataclass(frozen=True, slots=True)
class CurrentCaseView:
    case_id: str
    assessment_ids: tuple[str, ...]
    factor_order: tuple[str, ...]
    vector_groups: tuple[CurrentCaseVectorGroup, ...]
    profiles: tuple[CurrentCaseProfileRow, ...]
    active_finding_count: int
    unresolved_count: int
    blocked_count: int
    interpretation_release_state: str

    def profile(self, profile_number: int) -> CurrentCaseProfileRow:
        if not isinstance(profile_number, int) or isinstance(profile_number, bool):
            raise TypeError("profile_number must be an integer")
        matches = tuple(item for item in self.profiles if item.profile_number == profile_number)
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate current-case profile: {profile_number}")
        return matches[0]


def build_current_case_view(workspace: ClinicianWorkspace) -> CurrentCaseView:
    """Build the compact current-case view without changing report semantics."""
    if not isinstance(workspace, ClinicianWorkspace):
        raise TypeError("Current case view requires a ClinicianWorkspace")

    report = workspace.report
    rows: list[CurrentCaseProfileRow] = []
    for observation in report.formal.observations:
        by_factor = {item.factor: item for item in observation.factors}
        if len(by_factor) != len(observation.factors) or set(by_factor) != set(FACTORS):
            raise ValueError("Current case observation does not contain exactly eight factors")
        rows.append(
            CurrentCaseProfileRow(
                profile_number=observation.profile_number,
                reactions=tuple(
                    CurrentCaseReactionCell(
                        factor=factor,
                        symbol=by_factor[factor].symbol,
                        sympathetic=by_factor[factor].sympathetic,
                        unsympathetic=by_factor[factor].unsympathetic,
                        quantum_level=by_factor[factor].quantum_level,
                        forced_null=by_factor[factor].forced_null,
                    )
                    for factor in FACTORS
                ),
            )
        )

    if tuple(row.profile_number for row in rows) != tuple(range(1, len(rows) + 1)):
        raise ValueError("Current case profile numbering is not contiguous")

    return CurrentCaseView(
        case_id=workspace.current.case_id,
        assessment_ids=workspace.assessment_ids,
        factor_order=tuple(FACTORS),
        vector_groups=tuple(
            CurrentCaseVectorGroup(vector=name, factors=factors)
            for name, factors in VECTOR_FACTORS
        ),
        profiles=tuple(rows),
        active_finding_count=report.summary.finding_count,
        unresolved_count=report.summary.unresolved_count,
        blocked_count=report.summary.blocked_count,
        interpretation_release_state=report.summary.interpretation_release_state,
    )


def _text(value: object) -> str:
    return escape(str(value), quote=True)


def render_current_case_view_html(view: CurrentCaseView) -> str:
    """Render the compact matrix as a standalone clinician-facing HTML surface."""
    if not isinstance(view, CurrentCaseView):
        raise TypeError("Current case renderer requires a CurrentCaseView")

    vector_header = "".join(
        f'<th colspan="2" class="vector">{_text(group.vector)}</th>'
        for group in view.vector_groups
    )
    factor_header = "".join(f"<th>{_text(factor)}</th>" for factor in view.factor_order)

    matrix_rows: list[str] = []
    detail_blocks: list[str] = []
    for row in view.profiles:
        cells = []
        detail_rows = []
        for reaction in row.reactions:
            forced = (
                '<span class="forced-null" title="zero forțat / E.K.P. distinct de zero real">F</span>'
                if reaction.forced_null
                else ""
            )
            cells.append(
                f'<td class="reaction"><span class="symbol">{_text(reaction.symbol)}</span>{forced}</td>'
            )
            detail_rows.append(
                "<tr>"
                f"<td>{_text(reaction.factor)}</td><td>{_text(reaction.symbol)}</td>"
                f"<td>{reaction.sympathetic}</td><td>{reaction.unsympathetic}</td>"
                f"<td>{reaction.quantum_level}</td><td>{_text(reaction.forced_null)}</td>"
                "</tr>"
            )
        matrix_rows.append(
            f'<tr><th class="profile">{row.profile_number}</th>{"".join(cells)}</tr>'
        )
        detail_blocks.append(
            f"<details><summary>Detalii profil {row.profile_number}</summary>"
            '<table class="detail"><thead><tr><th>Factor</th><th>Reacție</th><th>+</th><th>-</th>'
            '<th>Quantum</th><th>Null forțat</th></tr></thead>'
            f'<tbody>{"".join(detail_rows)}</tbody></table></details>'
        )

    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Szondi3 — caz curent — {_text(view.case_id)}</title>
<style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem; color: #1f2328; }}
header {{ margin-bottom: 1rem; }}
.meta {{ color: #57606a; font-size: .9rem; }}
.status {{ display: flex; gap: 1rem; flex-wrap: wrap; margin: .75rem 0 1.25rem; }}
.status span {{ border: 1px solid #d0d7de; border-radius: 999px; padding: .25rem .6rem; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #d0d7de; text-align: center; padding: .45rem .55rem; }}
th {{ background: #f6f8fa; }}
.vector {{ font-weight: 700; }}
.profile {{ width: 4rem; }}
.reaction {{ min-width: 4.2rem; position: relative; }}
.symbol {{ font-size: 1.18rem; font-weight: 650; }}
.forced-null {{ margin-left: .3rem; font-size: .68rem; border: 1px solid #57606a; border-radius: 50%; padding: .05rem .25rem; vertical-align: top; }}
details {{ margin: .7rem 0; }}
summary {{ cursor: pointer; font-weight: 650; }}
.detail {{ margin-top: .5rem; font-size: .9rem; }}
@media (max-width: 760px) {{ body {{ padding: .75rem; }} .matrix-wrap {{ overflow-x: auto; }} }}
</style>
</head>
<body>
<header>
<h1>Profil Szondi — caz curent</h1>
<p><strong>{_text(view.case_id)}</strong></p>
<p class="meta">Evaluări: {_text(" → ".join(view.assessment_ids))}</p>
<div class="status">
<span>Constatări active: {view.active_finding_count}</span>
<span>Nerezolvate: {view.unresolved_count}</span>
<span>Blocate: {view.blocked_count}</span>
<span>{_text(view.interpretation_release_state)}</span>
</div>
</header>
<div class="matrix-wrap">
<table class="matrix">
<thead><tr><th rowspan="2">Profil</th>{vector_header}</tr><tr>{factor_header}</tr></thead>
<tbody>{"".join(matrix_rows)}</tbody>
</table>
</div>
<section>
<h2>Detalii de reacție</h2>
<p class="meta">Matricea păstrează simbolul complet. Numerele brute, quantum-ul și zero-ul forțat rămân separat inspectabile.</p>
{"".join(detail_blocks)}
</section>
</body>
</html>
"""
