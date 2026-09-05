"""Audited release boundary for Szondi3 clinical evidence.

This module closes two infrastructure gaps without adding clinical meaning:

- administered experimental-complement (E.K.P.) material can be carried into the
  evidence packet without being folded into the foreground profile series;
- a release bundle receives deterministic identities for Git, doctrine, P2B,
  evidence payload, and the preview synthesis contract/model.

AI remains preview-only. The release manifest records that policy explicitly and
there is no autonomous AI-text release path in this module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

from .clinical_evidence_packet import (
    ClinicalEvidencePacket,
    _factor_series,
    _profile_factor_maps,
    _required_doctrine,
    _vector_series,
    resolve_canonical_evidence,
)
from .clinical_pipeline import AdministeredClinicalEvaluation
from .interpretation import Fact
from .interpretation_catalogue_fate_modifiability import INITIAL_CLAIMS


_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_REPO_ROOT = Path(__file__).resolve().parents[1]
_REGISTRY_ROOT = _REPO_ROOT / "doctrine" / "registry"


@dataclass(frozen=True, slots=True)
class ComplementFactEvidence:
    key: str
    value: Any
    input_state: str
    fact_id: str | None


@dataclass(frozen=True, slots=True)
class ExperimentalComplementEvidence:
    test_number: int
    factor_symbols: tuple[tuple[str, str], ...]
    facts: tuple[ComplementFactEvidence, ...]


@dataclass(frozen=True, slots=True)
class AdministeredClinicalEvidencePacket(ClinicalEvidencePacket):
    """ClinicalEvidencePacket plus formal E.K.P. evidence kept in its own scope."""

    experimental_complements: tuple[ExperimentalComplementEvidence, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = ClinicalEvidencePacket.to_dict(self)
        payload["experimental_complements"] = [
            {
                "test_number": item.test_number,
                "factor_symbols": [list(pair) for pair in item.factor_symbols],
                "facts": [
                    {
                        "key": fact.key,
                        "value": _json_safe(fact.value),
                        "input_state": fact.input_state,
                        "fact_id": fact.fact_id,
                    }
                    for fact in item.facts
                ],
            }
            for item in self.experimental_complements
        ]
        return payload


@dataclass(frozen=True, slots=True)
class ClinicalReleaseManifest:
    schema_version: int
    git_commit_sha: str
    doctrine_snapshot_id: str
    doctrine_registry_sha256: str
    p2b_release_id: str
    p2b_catalogue_sha256: str
    evidence_packet_sha256: str
    synthesis_contract_version: str
    synthesis_model: str
    synthesis_release_policy: str = "PREVIEW_ONLY_MANUAL_CLINICIAN_RELEASE"
    autonomous_ai_release: bool = False


@dataclass(frozen=True, slots=True)
class AuditedClinicalRelease:
    manifest: ClinicalReleaseManifest
    evidence_packet: ClinicalEvidencePacket

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest": _json_safe(self.manifest),
            "evidence_packet": self.evidence_packet.to_dict(),
        }


def _json_safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _json_safe(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        _json_safe(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ("git",) + args,
            cwd=_REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(
            "Audited release requires an accessible local Git checkout"
        ) from exc
    return result.stdout.strip()


def _verified_checkout_sha() -> str:
    """Return the clean checkout HEAD, cross-checked with trusted CI metadata.

    The local checkout is the primary build-identity authority. Tracked changes are
    forbidden because their runtime code/doctrine would no longer correspond to
    HEAD. Untracked doctrine-registry records are also forbidden because they would
    alter the registry digest without belonging to HEAD. In GitHub Actions,
    ``GITHUB_SHA`` is an additional trusted assertion and must equal the checked-out
    HEAD; it never replaces verification of the checkout itself.
    """
    head = _run_git("rev-parse", "--verify", "HEAD")
    if not _COMMIT_RE.fullmatch(head):
        raise ValueError("Verified checkout HEAD is not a full lowercase 40-hex Git SHA")

    tracked_changes = _run_git("status", "--porcelain", "--untracked-files=no")
    if tracked_changes:
        raise ValueError("Audited release requires a clean tracked Git checkout")

    untracked_registry = _run_git(
        "ls-files",
        "--others",
        "--exclude-standard",
        "doctrine/registry",
    )
    if untracked_registry:
        raise ValueError(
            "Audited release refuses untracked doctrine-registry files outside checkout HEAD"
        )

    trusted_ci_sha = os.environ.get("GITHUB_SHA")
    if trusted_ci_sha is not None:
        if not _COMMIT_RE.fullmatch(trusted_ci_sha):
            raise ValueError("GITHUB_SHA must be a full lowercase 40-hex Git commit SHA")
        if trusted_ci_sha != head:
            raise ValueError("GITHUB_SHA does not match the checked-out Git HEAD")

    return head


def _registry_digest() -> str:
    if not _REGISTRY_ROOT.is_dir():
        raise ValueError(f"Doctrine registry is unavailable: {_REGISTRY_ROOT}")
    records = []
    for path in sorted(_REGISTRY_ROOT.glob("*.jsonl")):
        records.append(
            {
                "path": path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    if not records:
        raise ValueError("Doctrine registry contains no JSONL files")
    return _sha256(records)


def _p2b_catalogue_digest() -> str:
    return _sha256(tuple(asdict(claim) for claim in INITIAL_CLAIMS))


def _doctrine_snapshot_id(git_commit_sha: str, registry_digest: str) -> str:
    identity = _sha256(
        {
            "git_commit_sha": git_commit_sha,
            "doctrine_registry_sha256": registry_digest,
        }
    )
    return f"DS_{identity[:16].upper()}"


def _p2b_release_id(catalogue_digest: str) -> str:
    return f"P2B_{catalogue_digest[:16].upper()}"


def _complement_fact(fact: Fact) -> ComplementFactEvidence:
    return ComplementFactEvidence(
        key=fact.key,
        value=fact.value,
        input_state=fact.input_state.value,
        fact_id=fact.fact_id,
    )


def _complement_evidence(
    evaluation: AdministeredClinicalEvaluation,
) -> tuple[ExperimentalComplementEvidence, ...]:
    result = []
    for item in evaluation.complement_profiles:
        result.append(
            ExperimentalComplementEvidence(
                test_number=item.test_number,
                factor_symbols=tuple(
                    (reaction.factor, reaction.symbol)
                    for reaction in item.profile.factors
                ),
                facts=tuple(_complement_fact(fact) for fact in item.facts),
            )
        )
    return tuple(result)


def build_administered_clinical_evidence_packet(
    evaluation: AdministeredClinicalEvaluation,
) -> AdministeredClinicalEvidencePacket:
    """Carry foreground + explicitly authorized E.K.P. material into one packet.

    E.K.P. findings retain ``EXPERIMENTAL_COMPLEMENT`` scope and never enter the
    repeated foreground series. Canonical evidence is resolved from the complete
    administered report, so complement claims cannot arrive without their exact
    doctrine provenance.
    """
    if not isinstance(evaluation, AdministeredClinicalEvaluation):
        raise TypeError(
            "Administered evidence packet requires an AdministeredClinicalEvaluation"
        )

    report = evaluation.build_report()
    doctrine_ids, allowed_sources = _required_doctrine(report)
    canonical_evidence = resolve_canonical_evidence(doctrine_ids)
    for evidence in canonical_evidence:
        if evidence.source_id not in allowed_sources[evidence.doctrine_id]:
            raise ValueError(
                "Canonical doctrine source does not match executable claim provenance: "
                f"{evidence.doctrine_id} -> {evidence.source_id}"
            )

    foreground = evaluation.clinical_evaluation
    factor_maps = _profile_factor_maps(foreground)
    return AdministeredClinicalEvidencePacket(
        schema_version=3,
        report=report,
        factor_series=_factor_series(factor_maps),
        vector_series=_vector_series(factor_maps),
        canonical_evidence=canonical_evidence,
        experimental_complements=_complement_evidence(evaluation),
    )


def build_audited_clinical_release(
    packet: ClinicalEvidencePacket,
    *,
    git_commit_sha: str,
    synthesis_contract_version: str,
    synthesis_model: str,
) -> AuditedClinicalRelease:
    """Freeze deterministic identities around one packet and verified checkout.

    ``git_commit_sha`` is only a caller assertion. The release authority is the
    clean local checkout HEAD, additionally cross-checked against ``GITHUB_SHA`` in
    CI. A syntactically valid but different caller SHA is rejected.
    """
    if not isinstance(packet, ClinicalEvidencePacket):
        raise TypeError("Audited release requires a ClinicalEvidencePacket")
    if not isinstance(git_commit_sha, str) or not _COMMIT_RE.fullmatch(git_commit_sha):
        raise ValueError("git_commit_sha must be a full lowercase 40-hex Git commit SHA")
    if not isinstance(synthesis_contract_version, str) or not synthesis_contract_version.strip():
        raise ValueError("synthesis_contract_version must not be empty")
    if not isinstance(synthesis_model, str) or not synthesis_model.strip():
        raise ValueError("synthesis_model must not be empty")

    verified_sha = _verified_checkout_sha()
    if git_commit_sha != verified_sha:
        raise ValueError("git_commit_sha does not match the verified checkout HEAD")

    doctrine_digest = _registry_digest()
    p2b_digest = _p2b_catalogue_digest()
    evidence_digest = _sha256(packet.to_dict())
    manifest = ClinicalReleaseManifest(
        schema_version=1,
        git_commit_sha=verified_sha,
        doctrine_snapshot_id=_doctrine_snapshot_id(verified_sha, doctrine_digest),
        doctrine_registry_sha256=doctrine_digest,
        p2b_release_id=_p2b_release_id(p2b_digest),
        p2b_catalogue_sha256=p2b_digest,
        evidence_packet_sha256=evidence_digest,
        synthesis_contract_version=synthesis_contract_version,
        synthesis_model=synthesis_model,
    )
    return AuditedClinicalRelease(manifest=manifest, evidence_packet=packet)
