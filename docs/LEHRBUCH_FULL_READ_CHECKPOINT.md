# SZ_LEHR_1972 — Full-read checkpoint and Triebformel investigation dossier

**Status:** SOURCE-ORDER FULL BOOK READ COMPLETE; atomic P2A extraction remains in progress  
**Source:** `SZ_LEHR_1972` — `SZONDI_PRIMARY`  
**Book:** L. Szondi, *Lehrbuch der experimentellen Triebdiagnostik*, Text-Band, 3., erweiterte Auflage (1972)  
**Full-read scope:** displayed book text from Vorwort through final Sachregister / EOF, in source order  
**Canonical access witness used for durable anchoring:** workflow run `33019653845`, artifact `9625995662` (`p0-canonical-access`), digest `sha256:cb3e8c547fc19ac0a08dea332a551ac798ad519e9fe7e061ce9123fd92668ec0`, source HEAD `2dea792d4a11987cdea03ed75b26fb004465a731`.

> **CURRENT-STATE NOTE — 2026-08-27:** Sections 7 and “What is established versus what is still open” preserve the state of the investigation at the time of the full-read checkpoint. Their claim that the broader `kp/hs` selector remains open is superseded by `docs/KP_HS_RESOLUTION.md` and Decision Log `D-014`. The conceptual `kp/hs` issue must not be reopened from this historical checkpoint. The source observations in sections 4–6 and 8 remain valid.

## Epistemic status

This document is a durable research/checkpoint dossier, **not** a substitute for the Primary Doctrine Registry. It records what the completed source-order reading established, what must be atomized into P2A, and which questions remained unresolved at checkpoint time. Future interpretation must still retrieve the atomic doctrine entries and reconsult the canonical source context.

The full-read claim is book-level/source-order. It does **not** by itself mark all `SZ_LEHR_1972` canonical units, footnotes, headers and footers as atomically audited for P2A coverage. Canonical unit-by-unit extraction and coverage accounting proceed in bounded source-order batches.

## High-confidence methodological findings from the completed read

### 1. The test is subordinate to Schicksalspsychologie

At `BODY U000586-U000587`, Szondi explicitly places `experimentelle Triebdiagnostik` inside `Schicksalspsychologie`, which precedes the test, and states that test interpretation becomes questionable without the specific schicksalspsychological way of thinking. Technical use detached from that framework is criticized.

### 2. A single profile is not the whole person

At `BODY U000591`, Szondi states that a person has multiple `Schicksalsmöglichkeiten`; one `Triebprofil` reveals only one `Existenzmöglichkeit`. He therefore requires 8–10 profiles, each interpreted as a whole. This is a source-level reason not to collapse profile, series and person into one object.

### 3. The declared primary use is existential, not merely psychiatric labeling

At `BODY U000592-U000593`, Szondi says the test should primarily uncover `Existenzmöglichkeiten`, not freeze the person into a psychiatric diagnosis, and assigns the clinician the task of promoting the possibility that offers the greatest chance to the individual and community.

### 4. Triebformel is introduced inside the Linnäusmethode as a symptom/root construction

The defining sequence is `BODY U003705-U003739`.

- `U003711-U003712`: constant/almost-constant ambivalent and null reactions identify `Symptomfaktoren`; ambivalent reactions represent inner/subjective symptoms, null reactions outer/objective manifestations.
- `U003713-U003717`: constant/almost-constant positive and negative reactions identify `Konduktor-` or `Wurzelfaktoren`, representing unsatisfied needs / `Konduktornatur`. Szondi explicitly warns that negative reaction is not always repression and that a positive reaction can also represent an unsatisfied need.
- `U003718-U003720`: `TspG` is obtained from the sum of null and ambivalent reactions; Symptomfaktoren have the highest TspG, Wurzelfaktoren the lowest.
- `U003734-U003736`: the eight TspG are ranked; their order permits construction of the current `Triebformel`; the Triebformel is a fraction with Symptomfaktoren in the numerator and Wurzelfaktoren in the denominator.
- `U003737`: the simple `abgekürzte` form is for rapid orientation.
- `U003738`: the `vollständige Triebformel` is a multiple fraction with two or three strongest symptom factors on the first line, middle-strength `submanifeste`/`sublatente` factors on the middle line, and weakest TspG factors / Wurzelfaktoren on the third line.
- `U003739`: factors whose TspG difference is not greater than 2 are written on the same line.

### 5. Fall 11 is the didactic control case

`BODY U003741-U003796` demonstrates construction and interpretation. `U003748-U003754` explicitly distinguishes abbreviated and complete forms. The abbreviated form has `m` alone as symptom factor and `s` alone as Wurzelfaktor; the complete form retains the intermediate/submanifest structure. `U003796` states that Triebformel analysis exposes the relationship between symptom and omitted/failed drive satisfaction.

### 6. Fall 18: the canonical layout evidence supports two abbreviated fractions

The relevant canonical sequence is `BODY U004515-U004535`.

Crucially:

- `U004525`: `B. Bestimmung der Triebformel`
- `U004526`: ranking heading for Fall 18
- `U004527`: `Abgekürzte Triebformel:`
- `U004528`: `k<TAB>k p`
- `U004529`: `s<TAB>h s`
- `U004530`: only **after those two rows** begins `Vollständige Triebformel`

The canonical extractor also preserves the explicit tab between `k` and `k p`, and between `s` and `h s`. Thus the durable textual evidence supports the P1 closure statement that Fall 18 prints both `k/s` and `kp/hs` under the abbreviated-formula heading. The earlier conversational hypothesis that `kp/hs` might instead be the complete formula with its middle removed is **not supported by this canonical structure and must not be reused as a source-level premise**.

Because the precise visual layout is semantically relevant, the original admitted Lehrbuch PDF remains the final visual arbiter if exact column geometry is later required. The canonical structure is already sufficient to reject the hypothesis that `Vollständige Triebformel` precedes `kp/hs`.

### 7. Historical checkpoint: the broader abbreviated selector was then treated as underdetermined

At the time of this full-read checkpoint, no explicit universal sentence had been located that determined, in every case, when the abbreviated formula should expand from a simple unique-extrema fraction such as `k/s` to a broader multi-factor form such as `kp/hs`.

That historical finding correctly prohibited an invented neighbour/top-cluster threshold. **It no longer defines current project behavior:** D-014 subsequently resolved the executable extended representation as the strongly source-constrained projection `symptomatic line / root line`, while preserving its epistemic classification as implementation-inferred rather than verbatim universal Szondi wording.

### 8. Complete formula and Trieblinnäus representation must remain distinct from abbreviated formula

At `BODY U004176`, Szondi states that in Trieblinnäus tables the complete Triebformeln appear without the middle submanifest/sublatent theme factors. This is a separate representational convention. It must not be retroactively used to claim that `kp/hs` in Fall 18 is itself headed as the complete formula, because Fall 18's own canonical heading places `kp/hs` before `Vollständige Triebformel`.

### 9. Triebklasse and Triebformel are complementary but different procedures

At `BODY U003796-U003801`, Szondi distinguishes them: Triebformel concerns the relationship of symptom to unsatisfied drive satisfaction and primarily uses intrafactorial tendency tension; Triebklasse uses intravectorial TspD. `U003799` states the operational order: first Triebklasse, then Triebformel, together yielding Trieblinnäus placement.

## Corrections to the investigation history

The following earlier exploratory hypotheses are retired as source findings:

- `hs` in `kp/hs` = `homo sacer` — false for this context; `h.s.` is a real genealogical abbreviation elsewhere, but not the Triebformel notation.
- `kp/hs` = a general Sch/S or Ego/Sexual ratio — unsupported.
- `kp/hs` is itself the complete formula — contradicted by the canonical sequence `U004527-U004530`.
- `s TspG=0` = “complete repression” — unsupported simplification.
- universal neighbour-distance / `top-cluster / bottom-cluster` threshold as a separate expansion selector — not established.

The later D-014 project decision does **not** revive those hypotheses. It defines an executable structural projection from already-constituted complete-formula outer lines and explicitly labels that generalization `IMPLEMENTATION-INFERRED, strongly source-constrained`.

## What is established versus current project status

**SOURCE-ESTABLISHED:** nature of Triebformel as symptom/root fraction; TspG basis; definitions of symptom/root reactions; explicit complete-formula three-level architecture; Fall 18 authentic `k/s` and `kp/hs` under the abbreviated heading; separate complete-formula heading; distinct Trieblinnäus convention.

**CURRENT PROJECT RESOLUTION:** `kp/hs` is conceptually closed under D-014 / `docs/KP_HS_RESOLUTION.md`. Extended abbreviation is represented as symptomatic outer line over root outer line with the median line omitted; ambiguity in the underlying complete-formula partition remains local and fail-closed.

## P2A compaction checkpoint

The initial Lehrbuch P2A population became too sentence-granular. A full audit of the original doctrine IDs `DR_SZ_LEHR_1972_000001–000257` has now been completed under `docs/P2A_DOCTRINE_SELECTION_AND_COMPACTION_POLICY.md`.

- covered source range remains `BODY U000584–U001611`;
- original standalone doctrine objects audited: **257**;
- standalone doctrine objects retained after compaction: **72**;
- retired IDs remain historically reserved and are not reusable;
- coverage ledgers remain unchanged and continue to account for reviewed source material;
- final audit manifest: `docs/LEHRBUCH_COMPACTION_AUDIT_FINAL_000001_000257.md`;
- next source-order extraction point: **`BODY U001612`**.

The forward admission threshold is deliberately high: retain definitions, calculation/interpretation rules, major specifically Szondian theory, material conditions/exceptions, epistemic limits and rare consequential claims; leave ordinary examples, repetition and pedagogical elaboration to canonical retrieval.

## P2A continuation rule

The completed book read authorizes **selective critical extraction**, not summary substitution and not book reproduction. `SZ_LEHR_1972` must continue in bounded canonical-unit source-order batches with full coverage accounting, while the Doctrine Registry remains a compact semantic/provenance map back to the canonical source.

> **Read everything. Account for everything. Store only what is doctrinally critical.**
