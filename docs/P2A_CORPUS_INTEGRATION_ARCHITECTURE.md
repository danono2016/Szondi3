# SZONDI3 — P2A CORPUS INTEGRATION ARCHITECTURE

**Status:** P2A INTEGRATION WORKING CONTRACT  
**Layer:** `DOCTRINE_REPRESENTATION`  
**Purpose:** make independently read Szondi sources converge into one durable, source-faithful, cross-source doctrinal memory without collapsing author, book, chronology or uncertainty.

## 1. Governing idea

P2A is not one book summary and not one chat's memory. It is a corpus-scale doctrinal knowledge base populated independently source by source and later connected transversally.

The durable pipeline is:

`ADMITTED SOURCE -> CANONICAL U###### STREAM -> EXHAUSTIVE SOURCE-ORDER READ -> SOURCE CHECKPOINT -> SELECTIVE CRITICAL DOCTRINE -> COVERAGE LEDGER -> CONCEPT INDEX -> CROSS-SOURCE RELATIONS -> RETRIEVAL -> CANONICAL RECONSULTATION`

The canonical source is the complete textual memory. The doctrine registry is a compact semantic/provenance map containing only critical, distinct, future-retrieval-worthy doctrine. Coverage proves exhaustive review; it does not require a doctrine object for every passage.

The selection/compaction policy is normative for working population:

`docs/P2A_DOCTRINE_SELECTION_AND_COMPACTION_POLICY.md`

The concrete post-merge transversal-layer contract is:

`docs/P2A_TRANSVERSAL_INDEX_AND_RELATION_CONTRACT.md`

## 2. Corpus partitions

### A. Szondi primary corpus

Each admitted Szondi source owns an independent namespace and extraction sequence:

- `SZ_SA_1948`
- `SZ_LEHR_1972`
- `SZ_IA_1956_A`
- `SZ_IA_1956_B`
- `SZ_THER_1963_A`
- `SZ_THER_1963_B`
- `SZ_TRIEBPATH_1`
- `SZ_TRIEBPATH_2`

No primary source may borrow another source's wording to complete an atomic entry. Relations are added only after both source-local objects exist.

### B. Post-Szondi corpus

- `DERI_1949`
- `MELON_1975`

These remain separate authorial traditions. They may clarify, systematize, extend, criticize or offer alternative formulations, but they do not become `SZONDI_PRIMARY`.

## 3. Parallel-reader contract

Multiple chats may populate P2A in parallel if they obey source ownership and stable identity rules.

A reader working on a source must:

1. verify the current repository/PR state before writing;
2. work on a dedicated branch;
3. preserve the source's `sourceId` and local doctrine-ID sequence;
4. read/extract in source order with bounded batches;
5. maintain source-local coverage and verification records;
6. apply the doctrine-selection policy rather than treating every passage as a registry candidate;
7. never renumber doctrine IDs already committed or reserved by another branch;
8. never edit another source's entries merely to harmonize terminology;
9. record cross-source parallels as proposed relations or integration notes rather than rewriting either entry;
10. leave enough durable state that a successor can resume without the originating chat.

For split physical volumes that form one work, such as `SZ_IA_1956_A` and `SZ_IA_1956_B`, each sourceId keeps its own stable ID sequence and coverage ledger. A work-level conceptual view may connect them, but provenance is never collapsed.

## 4. Source-level artifacts

Every source should eventually have four durable classes of artifact.

### 4.1 Full-read checkpoint

Recommended path:

`docs/full_reads/<SOURCEID>_FULL_READ_CHECKPOINT.md`

Contains exact reading scope/EOF, canonical witness, high-confidence orientation map, difficult notation/layout zones, unresolved questions, retired exploratory hypotheses and next extraction position. This is an orientation dossier, not doctrinal authority.

### 4.2 Selective critical registry

Path:

`doctrine/registry/<SOURCEID>_*.jsonl`

Every retained entry preserves exact provenance, bounded exact excerpt, faithful Romanian rendering, source-near statement, assertion semantics, sensitive-content flags, relations/ambiguities/contradictions and review state.

The registry is deliberately selective. Definitions, governing rules, interpretive constraints, major theory, exceptions, epistemic limits, contradictions and rare consequential claims have priority. Repetitions, pedagogical elaborations and ordinary examples normally remain in canonical context/coverage rather than becoming standalone doctrine.

### 4.3 Coverage ledger

Path:

`doctrine/coverage/<SOURCEID>_BATCH_*.jsonl`

Coverage must make every reviewed canonical range auditable, including units intentionally producing no entry, visual-arbitration needs and unresolved ambiguities. A high number of no-entry units is not a defect when the material is noncritical or redundant.

### 4.4 Verification records

Path:

`doctrine/verification/<BATCHID>.jsonl`

These record canonical/source verification without overstating PDF inspection.

## 5. Cross-source conceptual layer

Source-order extraction alone is necessary but insufficient for later expert retrieval. After compact critical entries exist, a separate transversal index should connect doctrine without changing it.

Recommended future paths:

- `doctrine/index/concepts.jsonl`
- `doctrine/index/terms.jsonl`
- `doctrine/index/source_map.jsonl`
- `doctrine/relations/cross_source.jsonl`
- `doctrine/unresolved/open_questions.jsonl`

These are index/relation artifacts, not replacement doctrine and not a place to re-encode every source detail.

A concept record should use a neutral stable identity such as `DC_<NNNNNN>` and contain retrieval labels, Szondian/German terms and variants, Romanian access labels, aliases, linked doctrine/source IDs, chronology notes, broader/narrower links and unresolved terminology notes.

The exact integration discipline, relation record contract and open-question contract are defined in `docs/P2A_TRANSVERSAL_INDEX_AND_RELATION_CONTRACT.md`.

## 6. Initial conceptual families

The index must be open-ended and retrieval-oriented. It should support at least fate/familial-genetic doctrine; drive vectors/factors; Ego doctrine; sexuality; paroxysmal/Kain-Abel; contact; psychopathology/criminality; test method and interpretation; genotropic fate domains; therapy; metapsychology/Geist/religion/existence where source-supported.

This is a retrieval scaffold, not a closed ontology and not a modernization vocabulary.

## 7. Cross-source relation discipline

Relations may express restatement, qualification, narrowing, extension, alternative formulation, contradiction, example/dependency and post-Szondian commentary. Diachronic development is represented by these relation types together with explicit chronology notes rather than by silently treating the latest text as the winner.

Cross-source relations never merge authorial voices. Chronology remains visible. When relation type is uncertain, record an open question rather than harmonizing.

Actual cross-source relations should normally be committed only after all referenced doctrine IDs exist stably on `main` and both canonical contexts have been reconsulted.

## 8. Integration of Ich-Analyse reading

The independent Ich-Analyse reader contributes without restructuring Lehrbuch work.

Expected handoff:

1. full-read checkpoint(s);
2. **selective critical** source-order batches under `SZ_IA_1956_A` and `SZ_IA_1956_B`;
3. complete coverage and verification for each sourceId;
4. high-value cross-source candidates linking Ich-Analyse to existing primary doctrine;
5. explicit unresolved translation/terminology questions;
6. no renumbering or rewriting of other source-local entries.

The Ich-Analyse reader must follow `P2A_DOCTRINE_SELECTION_AND_COMPACTION_POLICY.md`: read/account for everything, but do not reproduce the book as doctrine objects.

Current integration policy is to wait for normal source-local completion/stabilization of Ich-Analyse rather than building provisional Sch/Ego executable logic from Lehrbuch alone. Read-only candidate inspection is allowed, but committed cross-source relations wait for stable doctrine IDs on `main`.

## 9. Retrieval contract for future chats

A future doctrinal query should:

1. identify concept/term aliases;
2. retrieve the compact relevant doctrine set across sources;
3. preserve source/author/chronology separation;
4. inspect relations/contradictions/unresolved notes;
5. reconsult exact canonical `U######` context;
6. consult PDF only where visual/layout/formula evidence affects meaning;
7. synthesize only afterward.

This is why the registry should remain compact: retrieval is expected to return to the canonical source rather than replace it.

## 10. Merge and concurrency safety

One active writer per source-local doctrine-ID sequence is preferred; independent sources may proceed concurrently. Shared schema/index/relation policy changes are integration-sensitive. A source PR should not casually change shared ontology to fit one book. Cross-source relations should normally be committed only after referenced doctrine IDs exist on `main`.

## 11. Quality gates before corpus-scale completion

P2A corpus completion requires:

- exhaustive source-order coverage ledgers;
- no unexplained canonical gaps;
- exact evidence for every retained doctrine;
- appropriate high-risk review;
- mechanically valid source layers/IDs;
- representable contradictions/qualifications;
- useful transversal retrieval without index inflation;
- explicit unresolved evidence-loss blockers;
- no P2B executable leakage;
- a compaction audit showing that the registry is not functioning as a duplicate book.

## 12. Immediate working plan — current state

The earlier Lehrbuch extraction/compaction plan is complete and is no longer a resume point.

Current sequence:

1. keep `SZ_LEHR_1972` source-local P2A closed unless a specific defect is identified;
2. allow the active `SZ_IA_1956_A/B` writer to finish independently under source ownership;
3. do not create provisional Sch/Ego runtime rules while later primary Ich-Analyse doctrine is still being integrated;
4. merge/review source-local Lehrbuch and Ich-Analyse work through the normal repository process;
5. after both corpora coexist on `main`, freeze one integration snapshot;
6. build only a **minimal** transversal concept set needed for high-value retrieval;
7. add sparse, reviewed cross-source relations only after reconsulting both canonical contexts;
8. represent uncertain harmonization as `UQ_*` open questions rather than forced relations;
9. use the integrated corpus to review the P2B candidate map and executable-claim contract;
10. implement P2B incrementally, beginning with high-confidence structural semantics and anti-inference safeguards rather than a broad diagnostic catalogue.

The concrete mechanics for steps 5–8 are normative working guidance in `docs/P2A_TRANSVERSAL_INDEX_AND_RELATION_CONTRACT.md`.

## Final invariant

> **Read everything. Account for everything. Store only what is doctrinally critical. Retrieve the rest from the canonical source when needed.**
