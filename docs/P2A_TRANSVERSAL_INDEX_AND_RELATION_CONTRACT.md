# SZONDI3 — P2A TRANSVERSAL INDEX AND RELATION CONTRACT

**Status:** PRE-INTEGRATION WORKING CONTRACT  
**Layer:** `DOCTRINE_REPRESENTATION`  
**Scope:** corpus-level retrieval and cross-source relations after source-local doctrine is stable on `main`  
**Not a gate:** this document creates no cross-source relation, no concept instance and no P2B executable rule.

## 1. Purpose

Once independently curated Szondi sources coexist on `main`, P2A needs a small transversal layer that makes them jointly retrievable without merging authorial voices or rewriting source-local doctrine.

The intended flow is:

`SOURCE-LOCAL DOCTRINE -> TRANSVERSAL CONCEPT RETRIEVAL -> CROSS-SOURCE RELATIONS -> CANONICAL RECONSULTATION -> LATER P2B REVIEW`

The transversal layer is an address and relation system, not a new synthetic textbook.

## 2. Preconditions for committed integration records

Actual concept links and cross-source relations SHOULD be committed only when all referenced doctrine IDs are stable on `main`.

For the first Lehrbuch/Ich-Analyse integration pass this means, at minimum:

1. `SZ_LEHR_1972` source-local P2A artifacts are merged to `main`;
2. `SZ_IA_1956_A` and `SZ_IA_1956_B` source-local P2A artifacts are merged to `main`;
3. all referenced doctrine IDs pass registry validation on the same `main` snapshot;
4. canonical evidence for both sides remains addressable;
5. no source-local object is edited merely to make terminology line up.

Before those conditions are met, only schema/runbook preparation and read-only candidate notes are allowed.

## 3. Storage roles

Recommended committed paths after integration begins:

- `doctrine/integration/snapshots/` — deterministic identity manifests for the exact doctrine snapshot used by an integration pass;
- `doctrine/index/concepts.jsonl` — curated neutral retrieval concepts;
- `doctrine/index/terms.jsonl` — lexical/terminological access index, preferably generated or mechanically validated;
- `doctrine/index/source_map.jsonl` — source/doctrine-to-concept lookup, preferably generated;
- `doctrine/relations/cross_source.jsonl` — reviewed cross-source relation records;
- `doctrine/unresolved/open_questions.jsonl` — unresolved cross-source questions.

The concept and relation layers MUST NOT replace canonical evidence or source-local doctrine.

### 3.1 Integration snapshot identity

Before the first transversal record is authored against a merged corpus, freeze the exact doctrine identity surface with:

`scripts/freeze_doctrine_snapshot.py`

The generator is deterministic and emits no timestamp. Given the same full Git commit SHA, selected source IDs and doctrine JSON content, it produces the same snapshot identity and registry digest.

A snapshot manifest records at least:

- the full `integrationCommit`;
- selected source IDs;
- doctrine count and per-source counts;
- the complete sorted doctrine-ID set;
- a deterministic digest for every selected source;
- one deterministic aggregate `registryDigest`;
- input-file SHA-256 identities;
- a derived `DS_*` snapshot identity.

The snapshot proves which doctrine objects were under review. It is **not** doctrinal authority and does not prove semantic correctness of any later relation.

For the first Lehrbuch/Ich-Analyse integration, select exactly:

- `SZ_LEHR_1972`
- `SZ_IA_1956_A`
- `SZ_IA_1956_B`

Example post-merge invocation:

```bash
python scripts/freeze_doctrine_snapshot.py \
  --commit-sha "$(git rev-parse HEAD)" \
  --source-id SZ_LEHR_1972 \
  --source-id SZ_IA_1956_A \
  --source-id SZ_IA_1956_B \
  --output doctrine/integration/snapshots/lehr_ia.json
```

The committed filename may later adopt the generated `DS_*` identity, but the manifest contents — not a hand-written filename — define the frozen snapshot.

## 4. Concept-record contract

A concept is a retrieval address, not a normalized psychological definition.

Stable identity:

`DC_<NNNNNN>`

Minimum conceptual fields:

```text
schemaVersion
conceptId
preferredLabel
retrievalLabels[]
germanTerms[]
romanianLabels[]
aliases[]
linkedDoctrineIds[]
sourceIds[]
broaderConceptIds[]
narrowerConceptIds[]
chronologyNotes[]
terminologyNotes[]
unresolvedNotes[]
reviewStatus
```

### 4.1 Forbidden concept behavior

A concept record MUST NOT:

- silently define a modern equivalent for a Szondian term;
- collapse `SZONDI_PRIMARY` and post-Szondian formulations into one voice;
- choose a winner between conflicting primary doctrines;
- strengthen a possibility/generalization into a fact;
- serve as a hidden P2B trigger;
- reproduce long doctrine statements already present in the registry.

`preferredLabel` is only an access label. It is not doctrinal authority.

## 5. Cross-source relation-record contract

Stable identity:

`XR_<NNNNNN>`

Minimum relation fields:

```text
schemaVersion
relationId
relationType
fromDoctrineId
toDoctrineId
direction
relationScope[]
rationale
epistemicStatus
chronologyNotes[]
evidenceReview
reviewStatus
notes[]
```

### 5.1 Allowed relation types

Use the relation vocabulary already authorized by the Primary Doctrine specification:

- `QUALIFIES`
- `NARROWS`
- `EXTENDS`
- `RESTATES`
- `CONTRADICTS`
- `ALTERNATIVE_FORMULATION`
- `EXAMPLE_OF`
- `DEPENDENT_ON`
- `POST_SZONDI_COMMENTARY_ON`

Do not invent a new relation type merely because two passages feel related. Use an open question when the correct relation cannot be established safely.

### 5.2 Direction

`direction` is normally `DIRECTED` because qualification, extension and dependency are directional.

A relation that is genuinely symmetric may use `SYMMETRIC`, but symmetry must not be inferred merely from thematic similarity.

### 5.3 Relation scope

`relationScope[]` names the narrow aspect actually being related, for example:

- `definition`
- `method_rule`
- `factor_sign_meaning`
- `ego_model_scope`
- `diagnostic_limit`
- `epistemic_strength`
- `historical_revision`

This prevents an accurate relation on one aspect from being misread as equivalence of the entire doctrine objects.

### 5.4 Epistemic status

Allowed integration statuses:

- `SOURCE_EXPLICIT` — the source itself explicitly refers to/revises/qualifies the other doctrine or work;
- `INTEGRATION_INFERRED` — relation is a curator/reviewer inference constrained by both source passages;
- `UNRESOLVED` — evidence supports relevance but not a safe relation type/direction.

`INTEGRATION_INFERRED` must never be presented downstream as a quotation or explicit authorial cross-reference.

### 5.5 Evidence review

`evidenceReview` records the evidence actually reconsulted for the relation:

```text
fromCanonicalReconsulted
toCanonicalReconsulted
fromPdfReconsulted
toPdfReconsulted
visualArbitrationRequired
reviewNotes[]
```

A cross-source relation is not accepted merely because two registry paraphrases look compatible. At acceptance, both canonical contexts must have been reconsulted. PDF reconsultation is required only where visual/layout/sign evidence affects the relation.

### 5.6 Review status

Recommended relation-review states:

- `PROPOSED`
- `SOURCE_RECHECKED`
- `CLINICIAN_REVIEWED`
- `ACCEPTED`
- `UNRESOLVED`
- `REOPENED`

High-consequence relations involving Sch/Ego interpretation, heredity/genotropism, sexuality, pathodiagnosis or criminality require clinician/steward review before `ACCEPTED`.

Semantic/clinician review is intentionally not inferred by the structural validator. The validator can prove that provenance prerequisites are present; it cannot decide that a clinical or doctrinal synthesis is correct.

## 6. Source-local immutability during integration

Cross-source integration MUST NOT rewrite a source-local registry entry to harmonize it with another book.

In particular:

- a later Szondi formulation does not erase the earlier entry;
- a later self-correction is represented by a relation plus chronology, not by silently rewriting the earlier doctrine;
- different uses of `Sch`, `Ich-Bild`, `Ich-Mechanismus`, `Integration`, `Negation`, `Verdrängung`, `Wurzelfaktor` or similar terms remain source-attributed;
- post-Szondian Deri/Mélon material remains separately attributed even where it systematizes Szondi.

If a source-local object itself is defective, repair that source-local layer separately with its own evidence and verification trail before creating the relation.

## 7. Chronology discipline

Chronology is metadata, not an automatic precedence rule.

For every relation involving materially different formulations, record enough chronology to distinguish:

- restatement;
- later elaboration;
- narrowing;
- expansion;
- explicit self-correction;
- genuine contradiction;
- terminological shift without doctrinal contradiction.

A later passage wins only when an explicit project decision or source statement establishes supersession. Otherwise both remain retrievable.

## 8. Open-question contract

When relation typing would require guessing, create an unresolved record instead.

Stable identity:

`UQ_<NNNNNN>`

Minimum fields:

```text
schemaVersion
questionId
topic
implicatedDoctrineIds[]
issue
evidenceNeeded[]
currentEvidence[]
status
notes[]
```

Recommended statuses:

- `OPEN`
- `WAITING_SOURCE`
- `WAITING_REVIEW`
- `RESOLVED`
- `RETIRED`

Open questions are preferable to false harmonization.

## 9. Generated indexes versus authored doctrine

`terms.jsonl` and `source_map.jsonl` should be generated or mechanically derivable wherever possible.

They may contain:

- normalized search keys;
- exact German terms from `terms[]`;
- Romanian access variants;
- source IDs;
- doctrine IDs;
- linked concept IDs.

They MUST NOT contain new doctrinal claims.

This keeps search infrastructure cheap to rebuild and prevents index text from becoming an unreviewed third doctrinal layer.

## 10. First post-merge integration runbook: Lehrbuch + Ich-Analyse

After both PRs are on `main`:

1. **Freeze one integration snapshot** — run `scripts/freeze_doctrine_snapshot.py` on the exact `main` commit containing `SZ_LEHR_1972`, `SZ_IA_1956_A`, and `SZ_IA_1956_B`; commit the deterministic manifest before authoring accepted relations.
2. **Validate identities** — enumerate all selected doctrine IDs and confirm no orphan/duplicate IDs; the snapshot generator and registry validator must agree on the selected surface.
3. **Seed a minimal concept set** from high-value retrieval families only; do not index every term.
4. **Start with explicit/high-value overlaps**, not broad thematic matching.
5. **Reconsult both canonical contexts** for every proposed relation.
6. **Classify chronology and relation type**; if uncertain, create `UQ_*` rather than forcing a relation.
7. **Keep relations sparse** — one relation should answer a concrete retrieval/interpretation need.
8. **Run mechanical validation** for concept IDs, relation IDs and doctrine targets.
9. **Clinician/steward review** high-consequence relations.
10. **Only after the transversal layer is stable**, revisit P2B candidate rules that depend on integrated doctrine.

## 11. Priority concept families for the first integration pass

The initial Lehrbuch/Ich-Analyse pass should prioritize only concepts that materially affect interpretation or prevent error:

- `Sch` as Ego vector / Ego image / Ego mechanism;
- `Egodiastole` / `Egosystole` and p/k functional polarity;
- `Projektion`, `Inflation`, `Introjektion`, `Negation`;
- `Negation` versus `Verdrängung`;
- `Integration` / `Desintegration`;
- `Vorder-Ich` / `Hinter-Ich` / complement profile;
- symptom analysis requiring foreground/background Ego dialectic;
- Triebformel root/symptom meaning where Ego doctrine qualifies interpretation;
- methodological limits that prevent one-factor or one-profile diagnostic inference.

Do not begin with encyclopedic concept coverage.

## 12. P2B handoff rule

A P2B rule depending only on stable Lehrbuch doctrine may proceed independently if its prerequisites are complete and it does not touch Sch/Ego interpretation held by later primary doctrine.

A P2B Sch/Ego rule MUST wait until the relevant Lehrbuch and Ich-Analyse doctrines have been integrated or explicitly reviewed as non-conflicting.

P2B consumes accepted doctrine plus deterministic P1 facts. It must not use the transversal index as a substitute for canonical provenance.

## 13. Validation invariants

Future validators for the transversal layer should enforce at least:

- unique `DC_*`, `XR_*`, `UQ_*` identities;
- every linked doctrine ID exists on the frozen integration snapshot;
- every relation type is allowed by the P2A doctrine spec;
- `fromDoctrineId != toDoctrineId` for cross-source relations;
- source-local doctrine is never generated/rewritten by the index builder;
- accepted relations have canonical reconsultation recorded for both sides;
- generated indexes contain no executable trigger fields;
- post-Szondian relations never masquerade as `SZONDI_PRIMARY`;
- deterministic serialization and stable ordering;
- the committed snapshot manifest remains reproducible from its recorded commit and selected sources.

## Final invariant

> **Freeze the doctrine surface, connect doctrine without collapsing it, index for retrieval, relate only after reconsultation, and leave uncertainty explicit.**
