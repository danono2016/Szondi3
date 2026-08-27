# SZONDI3 — P2A CORPUS INTEGRATION ARCHITECTURE

**Status:** P2A INTEGRATION WORKING CONTRACT  
**Layer:** `DOCTRINE_REPRESENTATION`  
**Purpose:** make independently read Szondi sources converge into one durable, source-faithful, cross-source doctrinal memory without collapsing author, book, chronology or uncertainty.

## 1. Governing idea

P2A is not one book summary and not one chat's memory. It is a corpus-scale doctrinal knowledge base populated independently source by source and later connected transversally.

The durable pipeline is:

`ADMITTED SOURCE -> CANONICAL U###### STREAM -> EXHAUSTIVE SOURCE-ORDER READ -> SOURCE CHECKPOINT -> ATOMIC DOCTRINE -> COVERAGE LEDGER -> CONCEPT INDEX -> CROSS-SOURCE RELATIONS -> RETRIEVAL -> CANONICAL RECONSULTATION`

The atomic doctrine registry remains authoritative for represented doctrine. Full-read checkpoints, indexes and maps are navigation/research aids and may never replace exact source anchors.

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
6. never renumber doctrine IDs already committed or reserved by another branch;
7. never edit another source's entries merely to harmonize terminology;
8. record cross-source parallels as proposed relations or integration notes rather than rewriting either entry;
9. rebase/reconcile against current `main` before merge when another P2A PR has landed;
10. leave enough durable state that a successor can resume without the originating chat.

For split physical volumes that form one work, such as `SZ_IA_1956_A` and `SZ_IA_1956_B`, each sourceId keeps its own stable ID sequence and coverage ledger. A work-level conceptual view may connect them, but provenance is never collapsed.

## 4. Source-level artifacts

Every source should eventually have four durable classes of artifact.

### 4.1 Full-read checkpoint

Recommended path:

`docs/full_reads/<SOURCEID>_FULL_READ_CHECKPOINT.md`

Contains:

- exact reading scope and EOF status;
- canonical witness;
- high-confidence orientation map;
- difficult notation/layout zones;
- unresolved questions;
- explicitly retired exploratory hypotheses;
- next atomic extraction position.

This is an orientation dossier, not doctrinal authority.

### 4.2 Atomic registry

Path:

`doctrine/registry/<SOURCEID>_*.jsonl`

Every entry preserves exact provenance, bounded exact excerpt, faithful Romanian rendering, source-near statement, assertion semantics, sensitive-content flags, relations/ambiguities/contradictions and review state.

### 4.3 Coverage ledger

Path:

`doctrine/coverage/<SOURCEID>_BATCH_*.jsonl`

Coverage must make every reviewed canonical range auditable, including units intentionally producing no entry, visual-arbitration needs and unresolved ambiguities.

### 4.4 Verification records

Path:

`doctrine/verification/<BATCHID>.jsonl`

These record canonical/source verification without overstating PDF inspection.

## 5. Cross-source conceptual layer

Source-order extraction alone is necessary but insufficient for later expert retrieval. After atomic entries exist, a separate transversal index should connect doctrine without changing it.

Recommended future paths:

- `doctrine/index/concepts.jsonl`
- `doctrine/index/terms.jsonl`
- `doctrine/index/source_map.jsonl`
- `doctrine/relations/cross_source.jsonl`
- `doctrine/unresolved/open_questions.jsonl`

These are index/relation artifacts, not replacement doctrine.

### Concept records

A concept record should have a neutral stable identity such as `DC_<NNNNNN>` and contain at minimum:

- preferred project retrieval label;
- Szondian/German terms and variants;
- Romanian access labels;
- aliases/spelling variants;
- linked doctrine IDs;
- linked source IDs;
- chronology notes;
- narrower/broader concept links;
- unresolved terminology notes.

A concept record must not claim that differently worded passages are equivalent merely because they look similar. Equivalence is itself a reviewable relation.

## 6. Initial conceptual families

The index must be open-ended. It should be capable of representing at least:

- `Schicksal`, `Zwangsschicksal`, `Wahlschicksal`, `Schicksalsmöglichkeiten`, `Existenzmöglichkeiten`;
- `familiäres Unbewußtes`, heredity, genes, recessivity, genotropism, ancestral claims and familial repetition;
- drive system: vectors, factors, needs, tendencies, Triebgefahr, Ventil, Wurzelfaktor, Symptomfaktor;
- Ego system: `Ich`, `Ich-Stufen`, `Ich-Funktionen`, Ego defenses, integration/disintegration and the specific Ich-Analyse constructions;
- sexuality, masculinity/femininity, inversion, homosexuality, bisexuality, sadism, masochism and perversion where source-supported;
- paroxysmal/epileptiform/hysteriform and Kain/Abel constructions;
- contact vector and attachment/contact formulations in Szondi's own terminology;
- psychopathology, psychosis, psychopathy, criminality and pathodiagnostic categories;
- test method and interpretation: profile, series, foreground/background, complement, Rand-Mitte, Triebklasse, Triebformel, Trieblinnäus, Dur-Moll, Sozialindex;
- profession, partner choice, friendship, illness, death and other genotropic/fate domains;
- therapeutic doctrine and Schicksalsanalytische Therapie;
- metapsychology, Geist, religion/faith and existential formulations where explicitly present.

This list is a retrieval scaffold, not a closed ontology and not a modernization vocabulary.

## 7. Cross-source relation discipline

Relations between atomic doctrine entries may express:

- restatement;
- qualification;
- narrowing;
- extension;
- alternative formulation;
- contradiction;
- example/dependency;
- diachronic development;
- post-Szondian commentary.

Cross-source relations never merge authorial voices. For Szondi-to-Szondi relations, chronology must remain visible. A later passage may extend or revise an earlier one without silently deleting it.

When relation type is uncertain, record an open question rather than selecting the most convenient harmonization.

## 8. Integration of Ich-Analyse reading

The independent Ich-Analyse reader can contribute without restructuring Lehrbuch work.

Expected handoff:

1. one full-read checkpoint for the work, or one per physical source plus a work-level checkpoint;
2. atomic source-order batches under `SZ_IA_1956_A` and `SZ_IA_1956_B`;
3. coverage and verification for each sourceId;
4. a list of high-value cross-source candidates linking Ich-Analyse to existing `SZ_SA_1948` and `SZ_LEHR_1972` doctrine;
5. explicit unresolved translation/terminology questions;
6. no renumbering or rewriting of Lehrbuch/Schicksalsanalyse entries.

Especially important Ich-Analyse concepts should first be preserved in their own source-near form. Only afterward should the transversal index connect them to Lehrbuch factor/vector descriptions or Schicksalsanalyse fate doctrine.

## 9. Retrieval contract for future chats

A future doctrinal query should not rely on a giant summary. The intended retrieval sequence is:

1. identify concept/term aliases in the transversal index;
2. retrieve all relevant atomic doctrine IDs across sources;
3. preserve source/author/chronology separation;
4. inspect relations, contradictions and unresolved notes;
5. reconsult the exact canonical `U######` context for the entries that matter to the question;
6. consult PDF only where visual/layout/formula evidence affects meaning;
7. only then synthesize an answer or feed later executable-interpretation work.

This prevents both memory loss and decontextualized database quotation.

## 10. Merge and concurrency safety

Parallel P2A work is encouraged only when conflicts remain source-local and reviewable.

- one active writer per source-local doctrine-ID sequence is preferred;
- independent sources may proceed concurrently;
- shared schema, concept-index schema, relation semantics and normative policy are integration-sensitive and should be changed in dedicated PRs;
- a source PR should not casually change shared ontology to fit one book;
- cross-source relation commits should normally occur after the referenced doctrine IDs exist on `main`;
- if a branch discovers a needed shared-schema change, pause that part and raise it explicitly rather than inventing a private extension.

## 11. Quality gates before corpus-scale completion

P2A corpus completion requires more than source EOF claims. At minimum:

- all admitted doctrinal sources have source-order coverage ledgers;
- no unexplained canonical gaps remain;
- every accepted doctrine has exact evidence validation;
- high-risk doctrine has appropriate human review;
- source layers and stable IDs remain mechanically valid;
- cross-source contradictions/qualifications can be represented;
- the transversal index can retrieve doctrine without becoming authority;
- unresolved evidence-loss blockers are explicit;
- no P2B executable logic has leaked into P2A.

## 12. Immediate working plan

1. repair and green the initial Lehrbuch P2A PR;
2. continue `SZ_LEHR_1972` atomically from `BODY U000646` after completed batches `U000584-U000610` and `U000611-U000645`;
3. allow the independent Ich-Analyse reader to populate `SZ_IA_1956_A/B` under this same contract;
4. continue existing `SZ_SA_1948` source-order population independently;
5. introduce the transversal concept/relation index only as a separate, reviewable addition after enough atomic material exists to test it against multiple sources;
6. process Deri and Mélon as separate post-Szondian layers, primarily for clarification/cross-reference, never to manufacture primary doctrine.

## Final invariant

> **Build one corpus memory from many source-faithful voices: source-local first, transversal second, synthesis last. No chat, book, index or ontology is allowed to erase provenance, chronology, contradiction or uncertainty.**
