# P2A Batch 002 — Schicksalsanalyse: transition and Begriff des Schicksals

**Batch:** `P2A-SA-002`  
**Source:** `SZ_SA_1948` — `SZONDI_PRIMARY`  
**Canonical range:** `BODY U000178-U000229`  
**Registry entries:** 35 (`DR_SZ_SA_1948_000040`–`DR_SZ_SA_1948_000074`)  
**Review state:** `SOURCE_VERIFIED`; clinician review remains required for high-risk entries before P2A gate closure.

## Scope

This source-order batch closes the end of the 1948 preface/introduction and then covers Chapter I, *Begriff des Schicksals*, through the transition immediately before Chapter II (*Physiologie der latenten rezessiven Gene*).

The batch preserves, without modernization or sanitization:

- the hereditary hypothesis concerning `Notausgänge` / `Verlegenheitsmotivierungen`;
- the triebpsychological definition of depression as loss of a `Liebesobjekt` / `Schutzobjekt`;
- Szondi's statement that Schicksalsanalyse is autonomous as a specific method but belongs to the unity of `Tiefenpsychologie`;
- the proposed three-dimensional training in psychoanalysis, complex psychology and Schicksalsanalyse;
- the explicitly biological and biopsychological program of the work;
- `Lebensplan`, `Objektwahl`, `Erbforschung`, `latente Gene`, `latent-rezessive Gene`, `dominante Gene`, `familiäres Erbgut` and `Ahnenansprüche`;
- the explicit definition `Schicksal ist der Wahl-Zwang der verborgenen Ahnen in Liebe, Freundschaft, Beruf, Krankheit und Tod`;
- the claim that hidden ancestral demands constrain concrete choices in love, friendship, profession, illness and death;
- the distinction among `Triebschicksal`, `Mental-Schicksal`, `Sozial-Schicksal` and `Gesamtschicksal`;
- Szondi's explicit epistemic limitation that Schicksalsanalyse is not yet able to represent the complete `Lebensplan`;
- the metascientific claim that Schicksal is a resultant of irrational forces and the attempt to bridge Natur- and Geisteswissenschaften.

No P2B trigger, protocol-match rule, anti-inference rule or runtime behavior is introduced.

## Assertion-strength discipline

Source qualifiers are preserved literally rather than inflated:

- `wie mir scheint` at U000179 is represented below categorical certainty;
- `Ich glaube` at U000210 is represented as a theoretical claim rather than established fact;
- `Sie nimmt an` across U000213-U000214 remains an explicit assumption;
- `Wir vermuten` at U000221 remains conjectural;
- the modal `sollten` in the training proposal at U000188 is preserved as a proposal and is not converted into an executable rule.

## Source-order recovery

The batch deliberately starts at U000178 rather than jumping directly to the chapter heading. A continuity sweep recovered doctrinally relevant material from the end of the preface, including hereditary, pathodiagnostic and methodological statements. Units that are headings, acknowledgements, attributed Freud/Knebel/Schopenhauer material, transitions or historical/programmatic context are explicitly accounted for in the coverage ledger rather than silently skipped.

## Original-PDF verification and visual arbitration

The original scan was directly inspected for printed pp. 26–35 (scan pp. 30–39) for the entries whose text appears on those pages. Two metascientific entries on printed p. 36 (`DR_SZ_SA_1948_000072` and `000073`) are currently canonical-verified but are explicitly marked as not visually checked in this batch; this limitation is preserved in `doctrine/verification/P2A-SA-002.jsonl` rather than disguised.

Four canonical-access anomalies required explicit arbitration:

1. U000188 contains a stray apostrophe before `andere`; the original scan reads `die eine oder die andere Methode`.
2. U000214 begins with a carried page-header artifact inside a sentence; the original scan establishes continuity from U000213.
3. U000220 corrupts the Greek word `ἀνάγκη`; the original scan is the visual authority.
4. U000221 repeats the corrupted Greek typography; the original again resolves `ἀνάγκη`.

The canonical derivative remains the deterministic address witness. The original scan governs typography and meaning where the two diverge.

## Evidence witness

Canonical extraction/review uses the independently green post-Batch-001 `main` witness:

- workflow run: `32997133589`;
- artifact: `9617057695` (`p0-canonical-access`);
- artifact digest: `sha256:a310b6c571fb2be9fe0e9c0f0f03513dc1356d4716589d7b7afd637d770a299d`;
- source HEAD: `1be223f865066334c2e142a5006a7133965483f3`.

## Unresolved / pending review

No source-access ambiguity is left unresolved for the registered doctrines in U000178-U000225. The two p. 36 entries remain explicitly not visually checked, but their canonical anchors are deterministic and do not depend on typography or layout.

High-risk hereditary/genetic and pathodiagnostic assertions remain `SOURCE_VERIFIED`; clinician/steward acceptance is not fabricated. No statement in this batch declares `P2A_PRIMARY_DOCTRINE_PASS`.

## Batch boundary

The next source-order unit is U000230, `KAPITEL II`, followed by U000231, `Physiologie der latenten rezessiven Gene`. Batch 003 must begin there unless a later audit reopens an earlier unit.
