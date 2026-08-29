import json
import unittest

from szondi3.clinical_ai_preview import (
    inspect_openai_preview_response,
    parse_openai_preview_response,
)
from szondi3.clinical_evidence_packet import build_clinical_evidence_packet
from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.clinical_synthesis import SynthesisProposition
from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}


def _reaction(factor: str, symbol: str) -> FactorReaction:
    base = "±" if symbol.startswith("±") else symbol[0]
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=_KIND[base],
        symbol=symbol,
        quantum_level=symbol.count("!"),
        forced_null=False,
    )


def _packet():
    profile = build_profile(
        _reaction(factor, symbol)
        for factor, symbol in zip(
            _FACTORS,
            ("+", "0", "-", "-", "+", "±", "+", "-"),
        )
    )
    return build_clinical_evidence_packet(
        evaluate_clinical_protocol(ProfileSeries((profile,)), production=True)
    )


def _proposition_from_finding(finding, *, proposition_id: str, profile_number: int):
    return SynthesisProposition(
        proposition_id=proposition_id,
        scope=finding.scope,
        profile_number=profile_number,
        text=finding.statement,
        support_claim_ids=(finding.claim_id,),
        support_fact_ids=finding.support_fact_ids,
        support_doctrine_ids=finding.doctrine_ids,
        anti_inference_ids_applied=finding.anti_inference_ids,
    )


def _response(*propositions: SynthesisProposition):
    payload = {
        "propositions": [
            {
                "proposition_id": proposition.proposition_id,
                "scope": proposition.scope,
                "profile_number": proposition.profile_number,
                "text": proposition.text,
                "support_claim_ids": list(proposition.support_claim_ids),
                "support_fact_ids": list(proposition.support_fact_ids),
                "support_doctrine_ids": list(proposition.support_doctrine_ids),
                "anti_inference_ids_applied": list(
                    proposition.anti_inference_ids_applied
                ),
            }
            for proposition in propositions
        ]
    }
    return {
        "id": "resp_o4_test",
        "model": "gpt-preview-test",
        "status": "completed",
        "output": [
            {
                "type": "message",
                "status": "completed",
                "content": [
                    {
                        "type": "output_text",
                        "text": json.dumps(payload, ensure_ascii=False),
                    }
                ],
            }
        ],
    }


class ClinicalAiPreviewInspectionTests(unittest.TestCase):
    def test_o4_inspection_separates_accepted_and_rejected_without_weakening_gate(self):
        packet = _packet()
        finding = next(
            item
            for item in packet.report.findings
            if item.claim_id == "IC_SZONDI_PRIMARY_000009"
        )
        accepted = _proposition_from_finding(
            finding,
            proposition_id="PROP_ACCEPTED",
            profile_number=1,
        )
        rejected = _proposition_from_finding(
            finding,
            proposition_id="PROP_REJECTED",
            profile_number=2,
        )
        response = _response(accepted, rejected)

        inspection = inspect_openai_preview_response(packet, response)

        self.assertEqual(inspection.response_id, "resp_o4_test")
        self.assertEqual(inspection.model, "gpt-preview-test")
        self.assertEqual(inspection.raw_proposition_count, 2)
        self.assertEqual(inspection.accepted_propositions, (accepted,))
        self.assertEqual(len(inspection.rejected_propositions), 1)
        self.assertEqual(inspection.rejected_propositions[0].position, 2)
        self.assertEqual(
            inspection.rejected_propositions[0].proposition_id,
            "PROP_REJECTED",
        )
        self.assertIn(
            "Claim is not active",
            inspection.rejected_propositions[0].reason,
        )

        with self.assertRaisesRegex(ValueError, "Claim is not active"):
            parse_openai_preview_response(packet, response)


if __name__ == "__main__":
    unittest.main()
