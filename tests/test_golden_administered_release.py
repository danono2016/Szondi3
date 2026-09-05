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
from szondi3.stimuli import SERIES, presentation_rows


def _commit():
    return clinical_release._verified_checkout_sha()


def _card_ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def _foreground(offset):
    choices = []
    for series in SERIES:
        cards = _card_ids(series)
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


class GoldenAdministeredReleaseTests(unittest.TestCase):
    def test_eight_real_administrations_survive_the_full_release_boundary(self):
        foregrounds = tuple(_foreground(offset) for offset in range(8))
        records = tuple(
            AdministeredTestRecord(
                foreground,
                _complement(foreground) if index == 3 else None,
            )
            for index, foreground in enumerate(foregrounds, start=1)
        )

        administered = evaluate_administered_tests(records, production=True)
        report = administered.build_report()
        packet = build_administered_clinical_evidence_packet(administered)
        release = build_audited_clinical_release(
            packet,
            git_commit_sha=_commit(),
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )

        self.assertEqual(administered.test_count, 8)
        self.assertEqual(administered.clinical_evaluation.profile_count, 8)
        self.assertEqual(len(administered.foreground_profiles), 8)
        self.assertEqual(len(administered.complement_profiles), 1)
        self.assertEqual(administered.complement_profiles[0].test_number, 3)

        self.assertEqual(report.header.profile_count, 8)
        self.assertTrue(report.header.production_mode)
        self.assertEqual(
            report.header.interpretation_release_state,
            "PRODUCTION_APPROVED_CLAIMS_ONLY",
        )
        self.assertEqual(len(report.observations), 8)
        self.assertTrue(report.findings)
        self.assertTrue(
            all(finding.lifecycle_status == "APPROVED" for finding in report.findings)
        )
        self.assertTrue(
            any(
                finding.scope == "EXPERIMENTAL_COMPLEMENT"
                and finding.profile_number == 3
                for finding in report.findings
            )
        )

        self.assertEqual(packet.schema_version, 3)
        self.assertEqual(packet.report, report)
        self.assertEqual(len(packet.factor_series), 8)
        self.assertEqual(len(packet.vector_series), 4)
        self.assertEqual(len(packet.experimental_complements), 1)
        self.assertEqual(packet.experimental_complements[0].test_number, 3)
        self.assertTrue(packet.canonical_evidence)

        payload = release.to_dict()
        self.assertEqual(payload["evidence_packet"]["profile_count"], 8)
        self.assertEqual(
            len(payload["evidence_packet"]["experimental_complements"]),
            1,
        )
        self.assertEqual(
            payload["evidence_packet"]["experimental_complements"][0]["test_number"],
            3,
        )
        self.assertEqual(
            payload["manifest"]["synthesis_release_policy"],
            "PREVIEW_ONLY_MANUAL_CLINICIAN_RELEASE",
        )
        self.assertFalse(payload["manifest"]["autonomous_ai_release"])
        self.assertEqual(len(payload["manifest"]["p2b_catalogue_sha256"]), 64)
        self.assertEqual(len(payload["manifest"]["evidence_packet_sha256"]), 64)

    def test_golden_release_is_deterministic_for_identical_recorded_choices(self):
        foregrounds = tuple(_foreground(offset) for offset in range(8))
        records = tuple(AdministeredTestRecord(item) for item in foregrounds)

        first_packet = build_administered_clinical_evidence_packet(
            evaluate_administered_tests(records, production=True)
        )
        second_packet = build_administered_clinical_evidence_packet(
            evaluate_administered_tests(records, production=True)
        )
        commit = _commit()
        first = build_audited_clinical_release(
            first_packet,
            git_commit_sha=commit,
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )
        second = build_audited_clinical_release(
            second_packet,
            git_commit_sha=commit,
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )

        self.assertEqual(first.manifest, second.manifest)
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
