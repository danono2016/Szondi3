"""Local pseudonymous archive for completed Szondi assessments.

The archive is deliberately narrower than a patient-record system. It stores the
canonical administered card choices plus a read-only working-report snapshot for a
pseudonymous assessment id. Manual clinician context/synthesis is redacted from the
durable snapshot because this first local store has no encryption/key-management
layer.

Disk databases are refused inside the repository so clinical material cannot be
accidentally committed. SQLite is used from the Python standard library and remains
a replaceable technical shell; it is not an epistemic authority.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable

from .administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from .clinical_pipeline import AdministeredTestRecord
from .clinician_workspace import ClinicianWorkspace
from .stimuli import SERIES


_REPO_ROOT = Path(__file__).resolve().parents[1]
_PSEUDONYM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class ArchivedAssessmentSummary:
    assessment_id: str
    git_commit_sha: str
    doctrine_snapshot_id: str
    p2b_release_id: str
    payload_sha256: str
    schema_version: int
    manual_clinician_text_persisted: bool = False


@dataclass(frozen=True, slots=True)
class ArchivedAssessment:
    summary: ArchivedAssessmentSummary
    protocol_payload: tuple[dict[str, Any], ...]
    report_payload: dict[str, Any]

    def administered_records(self) -> tuple[AdministeredTestRecord, ...]:
        """Rebuild only the canonical recorded protocol, not historical interpretation."""
        return administered_records_from_payload(self.protocol_payload)


def _require_pseudonym(value: str) -> str:
    if not isinstance(value, str) or not _PSEUDONYM_RE.fullmatch(value):
        raise ValueError(
            "assessment_id must be a pseudonymous token using only letters, digits, '.', '_' or '-'"
        )
    return value


def _assert_outside_repository(path: Path) -> None:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(_REPO_ROOT.resolve())
    except ValueError:
        return
    raise ValueError("Clinical archive database must be outside the Git repository")


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(protocol_payload: Any, report_payload: Any) -> str:
    envelope = {"protocol": protocol_payload, "report": report_payload}
    return hashlib.sha256(_canonical_json(envelope).encode("utf-8")).hexdigest()


def administered_records_to_payload(
    records: Iterable[AdministeredTestRecord],
) -> tuple[dict[str, Any], ...]:
    """Serialize only source-defined recorded choices, never calculated reactions."""
    supplied = tuple(records)
    if not supplied:
        raise ValueError("At least one administered test record is required")
    if any(not isinstance(item, AdministeredTestRecord) for item in supplied):
        raise TypeError("records must contain only AdministeredTestRecord objects")

    result: list[dict[str, Any]] = []
    for record in supplied:
        foreground = [
            {
                "series": choice.series,
                "sympathetic": list(choice.sympathetic),
                "unsympathetic": list(choice.unsympathetic),
            }
            for choice in record.foreground.series_choices
        ]
        complement = None
        if record.complement is not None:
            complement = [
                {
                    "series": choice.series,
                    "relative_sympathetic": list(choice.relative_sympathetic),
                    "relative_unsympathetic": list(choice.relative_unsympathetic),
                }
                for choice in record.complement.series_choices
            ]
        result.append({"foreground": foreground, "complement": complement})
    return tuple(result)


def administered_records_from_payload(
    payload: Iterable[dict[str, Any]],
) -> tuple[AdministeredTestRecord, ...]:
    """Reconstruct protocols only through canonical administration functions."""
    supplied = tuple(payload)
    if not supplied:
        raise ValueError("Archived protocol payload is empty")
    records: list[AdministeredTestRecord] = []

    for item in supplied:
        if not isinstance(item, dict):
            raise TypeError("Each archived test must be an object")
        foreground_items = item.get("foreground")
        if not isinstance(foreground_items, list):
            raise ValueError("Archived test requires foreground choices")
        by_series = {entry.get("series"): entry for entry in foreground_items if isinstance(entry, dict)}
        if set(by_series) != set(SERIES) or len(foreground_items) != len(SERIES):
            raise ValueError("Archived foreground must contain exactly series I-VI")
        foreground_choices = tuple(
            record_foreground(
                series,
                by_series[series].get("sympathetic", ()),
                by_series[series].get("unsympathetic", ()),
            )
            for series in SERIES
        )
        foreground = complete_foreground(foreground_choices)

        complement_payload = item.get("complement")
        complement = None
        if complement_payload is not None:
            if not isinstance(complement_payload, list):
                raise ValueError("Archived complement must be a list or null")
            complement_by_series = {
                entry.get("series"): entry
                for entry in complement_payload
                if isinstance(entry, dict)
            }
            if set(complement_by_series) != set(SERIES) or len(complement_payload) != len(SERIES):
                raise ValueError("Archived complement must contain exactly series I-VI")
            foreground_by_series = {choice.series: choice for choice in foreground.series_choices}
            complement_choices = []
            for series in SERIES:
                entry = complement_by_series[series]
                canonical = record_complement(
                    foreground_by_series[series],
                    entry.get("relative_unsympathetic", ()),
                    "unsympathetic",
                )
                if list(canonical.relative_sympathetic) != entry.get("relative_sympathetic"):
                    raise ValueError(
                        f"Archived complement series {series} is inconsistent with foreground remainder"
                    )
                complement_choices.append(canonical)
            complement = complete_complement(foreground, complement_choices)

        records.append(AdministeredTestRecord(foreground=foreground, complement=complement))
    return tuple(records)


def _redacted_report_snapshot(workspace: ClinicianWorkspace) -> dict[str, Any]:
    payload = json.loads(_canonical_json(workspace.report.to_dict()))
    payload["clinician_context"] = []
    synthesis = payload.get("clinician_synthesis")
    if isinstance(synthesis, dict):
        synthesis["text"] = None
    return payload


class SQLiteClinicalArchive:
    """Local archive for pseudonymous, non-manual-text assessment snapshots."""

    def __init__(self, database: str | Path) -> None:
        if database == ":memory:":
            self.database = ":memory:"
        else:
            path = Path(database)
            _assert_outside_repository(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.database = str(path.expanduser().resolve())
        self._connection = sqlite3.connect(self.database)
        self._connection.execute("PRAGMA foreign_keys=ON")
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS archived_assessment (
                assessment_id TEXT PRIMARY KEY,
                schema_version INTEGER NOT NULL,
                protocol_json TEXT NOT NULL,
                report_json TEXT NOT NULL,
                git_commit_sha TEXT NOT NULL,
                doctrine_snapshot_id TEXT NOT NULL,
                p2b_release_id TEXT NOT NULL,
                payload_sha256 TEXT NOT NULL,
                manual_clinician_text_persisted INTEGER NOT NULL CHECK (manual_clinician_text_persisted = 0)
            )
            """
        )
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "SQLiteClinicalArchive":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def save(
        self,
        *,
        assessment_id: str,
        records: Iterable[AdministeredTestRecord],
        workspace: ClinicianWorkspace,
    ) -> ArchivedAssessmentSummary:
        """Persist one immutable snapshot; existing assessment ids are not overwritten."""
        assessment_id = _require_pseudonym(assessment_id)
        if not isinstance(workspace, ClinicianWorkspace):
            raise TypeError("workspace must be a ClinicianWorkspace")
        if workspace.current.case_id != assessment_id:
            raise ValueError(
                "Archive assessment_id must equal the current pseudonymous workspace case_id"
            )
        for case_id in workspace.assessment_ids:
            _require_pseudonym(case_id)

        protocol_payload = administered_records_to_payload(records)
        if len(protocol_payload) != workspace.report.summary.profile_count:
            raise ValueError("Archived administered record count must equal report profile_count")
        report_payload = _redacted_report_snapshot(workspace)
        digest = _digest(protocol_payload, report_payload)
        release = workspace.report.release
        summary = ArchivedAssessmentSummary(
            assessment_id=assessment_id,
            git_commit_sha=release.git_commit_sha,
            doctrine_snapshot_id=release.doctrine_snapshot_id,
            p2b_release_id=release.p2b_release_id,
            payload_sha256=digest,
            schema_version=_SCHEMA_VERSION,
        )

        try:
            self._connection.execute(
                """
                INSERT INTO archived_assessment (
                    assessment_id, schema_version, protocol_json, report_json,
                    git_commit_sha, doctrine_snapshot_id, p2b_release_id,
                    payload_sha256, manual_clinician_text_persisted
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    summary.assessment_id,
                    summary.schema_version,
                    _canonical_json(protocol_payload),
                    _canonical_json(report_payload),
                    summary.git_commit_sha,
                    summary.doctrine_snapshot_id,
                    summary.p2b_release_id,
                    summary.payload_sha256,
                ),
            )
            self._connection.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Archived assessment already exists: {assessment_id}") from exc
        return summary

    def load(self, assessment_id: str) -> ArchivedAssessment:
        assessment_id = _require_pseudonym(assessment_id)
        row = self._connection.execute(
            """
            SELECT schema_version, protocol_json, report_json, git_commit_sha,
                   doctrine_snapshot_id, p2b_release_id, payload_sha256,
                   manual_clinician_text_persisted
            FROM archived_assessment WHERE assessment_id = ?
            """,
            (assessment_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"Unknown archived assessment: {assessment_id}")
        schema_version, protocol_json, report_json, git_sha, doctrine_id, p2b_id, digest, manual = row
        if manual != 0:
            raise ValueError("Archive contains forbidden durable manual clinician text marker")
        protocol = tuple(json.loads(protocol_json))
        report = json.loads(report_json)
        expected = _digest(protocol, report)
        if expected != digest:
            raise ValueError("Archived assessment payload checksum mismatch")
        # Revalidate recorded card choices before exposing the archive record.
        administered_records_from_payload(protocol)
        return ArchivedAssessment(
            summary=ArchivedAssessmentSummary(
                assessment_id=assessment_id,
                git_commit_sha=git_sha,
                doctrine_snapshot_id=doctrine_id,
                p2b_release_id=p2b_id,
                payload_sha256=digest,
                schema_version=schema_version,
            ),
            protocol_payload=protocol,
            report_payload=report,
        )

    def list(self) -> tuple[ArchivedAssessmentSummary, ...]:
        rows = self._connection.execute(
            """
            SELECT assessment_id, git_commit_sha, doctrine_snapshot_id,
                   p2b_release_id, payload_sha256, schema_version
            FROM archived_assessment ORDER BY assessment_id
            """
        ).fetchall()
        return tuple(
            ArchivedAssessmentSummary(
                assessment_id=row[0],
                git_commit_sha=row[1],
                doctrine_snapshot_id=row[2],
                p2b_release_id=row[3],
                payload_sha256=row[4],
                schema_version=row[5],
            )
            for row in rows
        )
