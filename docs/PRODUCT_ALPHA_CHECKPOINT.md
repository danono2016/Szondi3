# Szondi3 Product Alpha Checkpoint

Date: 2026-09-08

Active clinical line at checkpoint: `work/ai-clinical-provenance-strategy-001`

Checkpoint commit before this document: `049cbf23ce77e0c72191a81589cdc603116dbb91`

## Product decision

Feature expansion is paused. The next goal is not to enlarge the architecture, but to validate whether the current browser product is already useful in real clinical work.

The first alpha is defined as the smallest clinician-usable Szondi3 that can be run locally in a browser, administer a real test, produce deterministic Szondi results, expose traceable authorized interpretation, allow manual clinician integration in-session, and show a working report that can be critically evaluated by the clinician.

## Alpha candidate available now

Launch from an up-to-date checkout of the active clinical branch with:

```bash
python -m szondi3
```

The application serves only on loopback (`127.0.0.1`) and is intended to be opened in a browser on the same clinician-controlled computer.

The current product path is:

`new pseudonymous assessment -> visual administration -> deterministic calculation -> current Szondi profile -> authorized findings -> exact source drill-down -> clinician integration -> working report -> immutable pseudonymous archive snapshot`

## What Alpha-0 must prove

Alpha-0 is successful only if a clinician can complete several real administrations and answer, from direct use rather than architecture review:

1. Is the administration flow natural and reliable enough for a real session?
2. Is the classical Szondi profile readable quickly enough for clinical work?
3. Are the authorized findings clinically useful, appropriately bounded, and understandable?
4. Does “De ce apare?” provide enough traceability to trust or contest a finding?
5. Does the working report help the clinician think and document, rather than merely expose technical data?
6. What is missing from the report that would materially change clinical usefulness?
7. What parts of the interface create friction during an actual session?

No new subsystem should be built until these questions produce concrete evidence of need.

## Current Alpha-0 capabilities

The current browser product already supports:

- pseudonymous assessment creation;
- visual Szondi administration using the admitted card images;
- foreground administration and optional experimental complement kept separate;
- deterministic clinical execution through the verified checkout;
- compact current-case Szondi matrix;
- authorized Szondian findings;
- exact finding -> activating facts -> executable claim -> doctrine -> canonical source evidence drill-down;
- longitudinal structural comparison for assessments that are live in the current process;
- clinician-authored context and manual synthesis in the active session;
- deterministic working-report HTML;
- local immutable pseudonymous SQLite archive snapshots;
- read-only reopening of historical snapshots without rerunning them under the current P1/P2B/doctrine checkout.

## Real-client alpha safety boundary

Alpha-0 is **not** a patient-record system.

For real-client testing:

- use only pseudonymous assessment IDs;
- do not enter names, CNPs, email addresses, phone numbers, or other directly identifying data into assessment IDs;
- keep the application loopback-only; do not expose the current WSGI server to LAN, internet, reverse proxy, or cloud hosting;
- the current SQLite archive is not an encrypted clinical-record store;
- free-text clinician context/synthesis is intentionally not persisted by the unencrypted archive baseline;
- historical snapshots are read-only and must not be treated as automatically reinterpreted under newer software releases.

If testing requires identifiable notes, remote access, multi-user access, or durable sensitive free text, Alpha-0 is not an adequate security boundary and those capabilities must wait for an explicit secure-storage/authentication design.

## Report evaluation target

For the first real runs, the report is the main product under evaluation.

The clinician should judge separately:

- formal Szondi observations and calculations;
- authorized findings and their limits/anti-inferences;
- unresolved or blocked interpretation states;
- experimental complement material;
- longitudinal structural material, when present;
- clinician-authored context and synthesis;
- provenance/release/audit material.

The product question is not whether all available data can be printed. The question is whether the report presents the right clinical hierarchy: profile first, meaningful authorized interpretation second, clinician synthesis clearly separated, and technical provenance available when needed without overwhelming ordinary reading.

## Explicit non-goals for Alpha-0

Do not add merely because they are architecturally possible:

- AI-generated clinical conclusions;
- hidden case-specific rules;
- automatic diagnostic mapping;
- vector search/RAG;
- automated historical reinterpretation;
- remote/cloud deployment;
- multi-user/authentication;
- encrypted patient-record persistence;
- complex historical compatibility machinery;
- additional P2B claims beyond the currently authorized frontier.

These become candidates only if real alpha use demonstrates a concrete product need and the appropriate epistemic/security boundary is designed first.

## Exit condition from Alpha-0

After several real, pseudonymized runs, capture concrete observations about:

- administration friction;
- profile readability;
- useful versus unhelpful findings;
- missing interpretation content;
- report structure and wording;
- source/provenance usefulness;
- any clinical action the clinician wanted to perform but could not.

The next development slice must be selected from those observations. Until then, the product is frozen except for defects that prevent or materially distort Alpha-0 use.
