import unittest

from szondi3 import clinical_release
from szondi3.administration import (
    complete_complement,
    complete_foreground,
    record_complement,
    record_foreground,
)
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_pipeline import AdministeredTestRecord, evaluate_administered_tests
from szondi3.clinical_release import (
    build_administered_clinical_evidence_packet,
    build_audited_clinical_release,
)
from szondi3.clinical_synthesis import SynthesisProposition, validate_synthesis_propositions
from szondi3.interpretation_catalogue_affect_anxiety_comparison import (
    INITIAL_CLAIMS as EXECUTABLE_INITIAL_CLAIMS,
)
from szondi3.stimuli import SERIES, presentation_rows


_COMMIT = "0123456789abcdef0123456789abcdef01234567"


def _ids(series):
    rows = presentation_rows(series)
    return [card.card_id for row in rows for card in row]


def _foreground(offset=0):
    choices = []
    for series in SERIES:
        cards = _ids(series)
        rotated = cards[offset:] + cards[:offset]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def _complement(foreground):
    choices = []
    for choice in foreground.series_choices:
        choices.append(
            record_complement(
                choice,
                selected=choice.remaining[:2],
                selected_as="unsympathetic",
            )
        )
    return complete_complement(foreground, choices)


class ClinicalReleaseTests(unittest.TestCase):
    def _packet(self):
        foreground = _foreground(0)
        administered = evaluate_administered_tests(
            (AdministeredTestRecord(foreground, _complement(foreground)),),
            production=True,
        )
        return build_administered_clinical_evidence_packet(administered)

    def test_release_hashes_the_same_p2b_catalogue_used_by_runtime(self):
        self.assertEqual(clinical_release.INITIAL_CLAIMS, EXECUTABLE_INITIAL_CLAIMS)
        self.assertEqual(
            clinical_release.INITIAL_CLAIMS[-1].claim_id,
            "IC_SZONDI_PRIMARY_000081",
        )

    def test_ekp_reaches_packet_without_becoming_foreground_series(self):
        packet = self._packet()

        self.assertEqual(packet.schema_version, 3)
        self.assertEqual(packet.report.header.profile_count, 1)
        self.assertEqual(len(packet.experimental_complements), 1)
        complement = packet.experimental_complements[0]
        self.assertEqual(complement.test_number, 1)
        self.assertEqual(len(complement.factor_symbols), 8)
        self.assertTrue(
            any(
                fact.key == "protocol.experimental_complement.sch_theoretical_relation"
                for fact in complement.facts
            )
        )

        findings = tuple(
            item
            for item in packet.report.findings
            if item.scope == "EXPERIMENTAL_COMPLEMENT"
        )
        self.assertEqual(
            tuple(item.claim_id for item in findings),
            ("IC_SZONDI_PRIMARY_000046", "IC_SZONDI_PRIMARY_000048"),
        )
        doctrine_ids = {
            doctrine_id
            for finding in findings
            for doctrine_id in finding.doctrine_ids
        }
        self.assertTrue(
            doctrine_ids.issubset(
                {item.doctrine_id for item in packet.canonical_evidence}
            )
        )

        payload = packet.to_dict()
        self.assertEqual(payload["profile_count"], 1)
        self.assertEqual(len(payload["experimental_complements"]), 1)
        self.assertTrue(
            any(
                item["scope"] == "EXPERIMENTAL_COMPLEMENT"
                for item in payload["findings"]
            )
        )

    def test_complement_proposition_requires_exact_complement_scope_bundle(self):
        packet = self._packet()
        finding = next(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000046"
            and item.scope == "EXPERIMENTAL_COMPLEMENT"
        )
        proposition = SynthesisProposition(
            proposition_id="PROP_EKP_001",
            scope="EXPERIMENTAL_COMPLEMENT",
            profile_number=1,
            text=finding.statement,
            support_claim_ids=(finding.claim_id,),
            support_fact_ids=finding.support_fact_ids,
            support_doctrine_ids=finding.doctrine_ids,
            anti_inference_ids_applied=finding.anti_inference_ids,
        )
        self.assertEqual(
            validate_synthesis_propositions(packet, (proposition,)),
            (proposition,),
        )

        wrong_scope = SynthesisProposition(
            proposition_id="PROP_EKP_002",
            scope="PROFILE",
            profile_number=1,
            text=finding.statement,
            support_claim_ids=(finding.claim_id,),
            support_fact_ids=finding.support_fact_ids,
            support_doctrine_ids=finding.doctrine_ids,
            anti_inference_ids_applied=finding.anti_inference_ids,
        )
        with self.assertRaisesRegex(ValueError, "Claim is not active"):
            validate_synthesis_propositions(packet, (wrong_scope,))

    def test_release_manifest_is_deterministic_complete_and_preview_only(self):
        packet = self._packet()
        first = build_audited_clinical_release(
            packet,
            git_commit_sha=_COMMIT,
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )
        second = build_audited_clinical_release(
            packet,
            git_commit_sha=_COMMIT,
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )

        self.assertEqual(first.manifest, second.manifest)
        manifest = first.manifest
        self.assertEqual(manifest.git_commit_sha, _COMMIT)
        self.assertTrue(manifest.doctrine_snapshot_id.startswith("DS_"))
        self.assertEqual(len(manifest.doctrine_registry_sha256), 64)
        self.assertTrue(manifest.p2b_release_id.startswith("P2B_"))
        self.assertEqual(len(manifest.p2b_catalogue_sha256), 64)
        self.assertEqual(len(manifest.evidence_packet_sha256), 64)
        self.assertEqual(manifest.synthesis_contract_version, PREVIEW_CONTRACT_VERSION)
        self.assertEqual(manifest.synthesis_model, DEFAULT_PREVIEW_MODEL)
        self.assertEqual(
            manifest.synthesis_release_policy,
            "PREVIEW_ONLY_MANUAL_CLINICIAN_RELEASE",
        )
        self.assertFalse(manifest.autonomous_ai_release)

        exported = first.to_dict()
        self.assertIn("manifest", exported)
        self.assertIn("evidence_packet", exported)
        self.assertEqual(
            exported["manifest"]["evidence_packet_sha256"],
            manifest.evidence_packet_sha256,
        )

    def test_release_rejects_noncanonical_commit_identity(self):
        with self.assertRaisesRegex(ValueError, "40-hex"):
            build_audited_clinical_release(
                self._packet(),
                git_commit_sha="abc123",
                synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
                synthesis_model=DEFAULT_PREVIEW_MODEL,
            )


if __name__ == "__main__":
    unittest.main()
