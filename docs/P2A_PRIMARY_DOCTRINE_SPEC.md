# SZONDI3 — P2A PRIMARY DOCTRINE REGISTRY SPECIFICATION

**Status:** P2A NORMATIVE CANDIDATE  
**Gate:** `P2A_PRIMARY_DOCTRINE_PASS`  
**Layer:** `DOCTRINE_REPRESENTATION`  
**Scope:** source-near preservation of doctrine before executable interpretation

## 1. Purpose

P2A records what the admitted authors state before asking what software may infer from protocol evidence.

The registry is a durable source-near doctrinal layer between deterministic test facts and executable interpretation:

`PRIMARY EVIDENCE -> CANONICAL ACCESS -> DETERMINISTIC TEST FACTS -> PRIMARY DOCTRINE REGISTRY -> EXECUTABLE INTERPRETATION`

P2A does **not** create executable triggers, clinical synthesis, contemporary correction, client-friendly reformulation or report prose.

The governing invariant is:

> **Preserve doctrine first. Do not weaken, complete, sanitize or operationalize it merely because software prefers a simpler rule.**

## 2. Authority and source-layer separation

Every registry entry belongs to exactly one admitted source layer and authorial provenance.

### `SZONDI_PRIMARY`

Only the eight admitted `SZ_*` sources may produce `SZONDI_PRIMARY` doctrine entries.

Primary doctrine preserves Szondi's own conceptual force, including hereditary/genetic/genotropic/familial/transgenerational formulations, sexual terminology, pathodiagnostic language, criminological language and historically dated terminology when source-supported.

### `POST_SZONDI_TRADITION`

`DERI_1949` and `MELON_1975` remain separate later-author layers. They may clarify, extend, systematize or disagree with Szondi, but their statements never become `SZONDI_PRIMARY` through paraphrase, agreement or convenience.

Deri and Mélon must remain distinguishable from one another at entry level.

### Contemporary context

Contemporary scientific or clinical evaluation is outside P2A. If introduced in a later phase, it must be a separate labeled layer and may not rewrite a P2A entry.

## 3. Evidence rule

Every doctrinal assertion must have an exact evidence path into the admitted source boundary.

Minimum source anchor:

- `sourceId`;
- canonical stream;
- one or more canonical `unitId` values;
- structural context where needed;
- PDF/page or visual-arbitration reference when typography, table position, symbol, formula or layout affects meaning.

Canonical units are access/provenance derivatives. The original admitted DOCX/PDF remains superior evidence if the derivative is ambiguous or appears wrong.

A registry entry without an exact admitted-source anchor is invalid.

## 4. Atomicity rule

A doctrine entry should represent one reviewable doctrinal assertion or one tightly coupled assertion set whose meaning would be distorted by separation.

Do not create giant chapter-summary entries that collapse multiple conditions, exceptions or competing claims.

Conversely, do not fragment a single conditional statement so aggressively that its condition, exception, causal direction or assertion strength is lost.

Atomicity is judged by whether a reviewer can answer:

- what exactly is being claimed;
- by whom;
- under which conditions;
- with what degree of force;
- from which exact evidence;
- whether another source passage qualifies or contradicts it.

## 5. Stable identity

Every accepted entry receives a stable identifier that is never recycled.

Format:

`DR_<SOURCEID>_<NNNNNN>`

Examples:

- `DR_SZ_LEHR_1972_000001`
- `DR_SZ_SA_1948_000001`
- `DR_DERI_1949_000001`

The numeric sequence is source-local and zero-padded. A later wording correction does not create a new identity if the represented doctrinal object is demonstrably the same; a materially different doctrinal object receives a new identifier.

Deleted/retracted identifiers remain reserved in history.

## 6. Required registry fields

The durable machine-readable representation must contain at least the following fields.

### Identity and provenance

- `schemaVersion`
- `doctrineId`
- `sourceId`
- `sourceLayer`
- `authorTradition`
- `sourceAnchors[]`

Each `sourceAnchor` contains at minimum:

- `stream`
- `unitStart`
- `unitEnd`
- optional `structuralPath`
- optional `pdfPath`
- optional `printedPage`
- optional `visualArbitrationNote`

### Source-near content

- `sourceLanguage`
- `sourceExcerpt`
- `romanianRendering`
- `doctrinalStatement`

`sourceExcerpt` is a bounded exact excerpt sufficient for review, not an uncontrolled reproduction of a chapter. The full canonical source remains addressable through the anchor.

`romanianRendering` is a faithful rendering for comprehension. It may retain German terms in parentheses where doctrinal precision requires them.

`doctrinalStatement` is the registry's source-near normalized statement. It must not introduce modern psychological equivalence or executable conditions absent from the source.

### Assertion semantics

- `assertionMode`
- `assertionStrength`
- `conditions[]`
- `exceptions[]`
- `scopeNotes[]`

Allowed `assertionMode` values:

- `DEFINITION`
- `DESCRIPTIVE_CLAIM`
- `CAUSAL_CLAIM`
- `HEREDITARY_GENETIC_CLAIM`
- `GENOTROPIC_CLAIM`
- `DIAGNOSTIC_PATHODIAGNOSTIC_CLAIM`
- `PROGNOSTIC_CLAIM`
- `METHOD_RULE`
- `TYPOLOGY_CLASSIFICATION`
- `INTERPRETIVE_ASSOCIATION`
- `EMPIRICAL_GENERALIZATION`
- `NORMATIVE_THERAPEUTIC_CLAIM`
- `OTHER_EXPLICIT`

More than one mode may be represented only when the source assertion genuinely combines them and review would be harmed by artificial separation.

Allowed `assertionStrength` values:

- `POSSIBILITY`
- `SUSPICION_INDICATION`
- `TENDENCY`
- `PROBABILITY`
- `GENERALIZATION`
- `ASSERTION`
- `DEFINITIONAL`
- `UNCLEAR_SOURCE_STRENGTH`

The registry must preserve the source's epistemic force. It may not upgrade a possibility to a fact or downgrade a categorical Szondian assertion because contemporary knowledge disputes it.

### Doctrinal vocabulary

- `terms[]`
- `historicallySensitiveTerms[]`
- `hereditaryGeneticContent`
- `sexualContent`
- `pathodiagnosticContent`
- `criminologicalContent`

The four content flags are descriptive metadata for review/search. They do not censor or replace the underlying wording.

`terms[]` should retain specifically Szondian German terminology where relevant, for example `Genotropismus`, `Schicksal`, `Triebgefahr`, `Wurzelfaktor`, `Vordergänger`, `Hintergänger`, `Kain`, `Abel`, `Ich-Stufen`.

### Relations and uncertainty

- `relations[]`
- `ambiguities[]`
- `contradictions[]`
- `reviewStatus`
- `reviewNotes[]`

Allowed relation types include:

- `QUALIFIES`
- `NARROWS`
- `EXTENDS`
- `RESTATES`
- `CONTRADICTS`
- `ALTERNATIVE_FORMULATION`
- `EXAMPLE_OF`
- `DEPENDENT_ON`
- `POST_SZONDI_COMMENTARY_ON`

A relation never merges two entries into one authorial voice.

Allowed `reviewStatus` values:

- `DRAFT_EXTRACTED`
- `SOURCE_VERIFIED`
- `CLINICIAN_REVIEWED`
- `ACCEPTED`
- `UNRESOLVED`
- `REOPENED`

`UNRESOLVED` is a valid durable state. Ambiguity is data, not a defect to be hidden.

## 7. Doctrinal fidelity rules

For `SZONDI_PRIMARY`, the registry MUST preserve source-supported content concerning, among other things:

- heredity, genes, hereditary disposition and genetic determination;
- genotropism and genotropic attraction;
- familial and ancestral transmission;
- latent/recessive familial tendencies;
- ancestry, family tree and hereditary fate;
- partner choice, friendship, profession, illness and death where related by Szondi to hereditary/familial fate;
- transgenerational or intergenerational repetition in Szondi's own sense;
- sexuality, inversion, homosexuality, bisexuality, masculinity/femininity, sadism, masochism and perversion;
- criminality, psychopathy, psychosis, epilepsy, hysteria and other pathodiagnostic categories;
- Eros/Thanatos, Kain/Abel, Ich-Stufen, Schicksal and other specifically Szondian constructions.

It is forbidden to silently replace literal hereditary/genetic/genotropic content with concepts such as family narrative, attachment, learned family pattern, symbolic inheritance, transmitted beliefs or psychological legacy unless the cited source itself establishes that equivalence.

Historically difficult wording may be annotated, translated or contextualized later; it may not be removed from the source-near doctrine object.

## 8. Translation rule

Romanian rendering exists for faithful access, not modernization.

It must preserve:

1. object of the claim;
2. direction of the claim;
3. causal/hereditary language;
4. assertion strength;
5. explicit conditions;
6. explicit exceptions;
7. diagnostic/sexual terminology;
8. specifically Szondian terminology where translation alone would blur meaning.

If more than one Romanian rendering is defensible and the difference could affect doctrine, record the ambiguity instead of silently selecting the smoother version.

## 9. Contradiction and diachronic-development rule

P2A does not harmonize Szondi across books or editions by narrative convenience.

When two admitted primary passages differ materially:

- preserve both entries;
- record the relation/contradiction explicitly;
- preserve source chronology;
- distinguish a genuine contradiction from later qualification, narrower scope, changed terminology or development of the theory;
- do not choose a winner unless the source itself or an accepted project rule supplies a discriminator.

A later Szondi statement does not automatically erase an earlier one merely because it is later.

Deri or Mélon cannot resolve a primary contradiction by overwriting either primary entry.

## 10. Doctrine versus executability boundary

P2A records doctrine regardless of whether it can currently be operationalized safely.

P2A MUST NOT contain:

- executable trigger expressions;
- protocol match logic;
- software confidence scores derived from runtime evidence;
- anti-inference rules;
- report-generation templates;
- narrative integration rules;
- client-facing softening;
- invented numeric thresholds used to make a doctrine executable.

P2A MAY record a non-authoritative boundary note such as `executionStatus: NOT_ASSESSED` or `NOT_EXECUTABLE_YET` only to prevent accidental downstream assumptions. Such a note is not an executable rule and cannot alter `doctrinalStatement`.

The P2B layer, not P2A, will later decide which accepted doctrine can be activated and under what evidence conditions.

## 11. Deterministic P1 material entering P2A

P1 formal procedures remain deterministic test facts. P2A may cite them as context only where a doctrinal passage explicitly interprets, qualifies or assigns meaning to those facts.

A P1 result does not become doctrine merely because it has a name or test.

Likewise, a clinical/qualitative statement excluded from P1 is not discarded. If source-supported, it belongs in P2A even when it is not deterministic.

This explicitly preserves the P1 residual boundaries for later doctrinal representation, including qualitative short-series constancy, Rand-Mitte, association/verbal methods and clinical meanings of Dur-Moll/Sozialindex.

## 12. Source-order workflow

P2A population proceeds source-first rather than topic-first to reduce cherry-picking and hidden author mixing.

For the `SZONDI_PRIMARY` layer, work should proceed through the admitted eight Szondi sources with stable coverage accounting. Cross-source thematic consolidation occurs only after each candidate statement retains its original source identity.

Post-Szondian sources are processed separately after or alongside primary coverage but never inside the same primary entries.

For a disputed or difficult point, the research priority remains:

`SZONDI_PRIMARY -> Deri -> Mélon -> external research only when the admitted corpus is insufficient and a specific missing source/object has been identified`

External research cannot manufacture a primary Szondi statement.

## 13. Coverage ledger

P2A must maintain a durable coverage ledger so completion is not based on impressionistic reading.

For every admitted doctrinal-candidate source, the ledger records at minimum:

- sourceId;
- canonical unit range reviewed;
- review batch identifier;
- candidate doctrine entries created;
- units intentionally producing no entry;
- units requiring visual arbitration;
- unresolved ambiguities;
- review status.

The ledger is an audit/progress artifact, not doctrinal authority.

A unit may legitimately produce no doctrine entry, but unexplained corpus gaps are not acceptable at gate closure.

## 14. Batch discipline

P2A should be reviewed in bounded batches rather than one giant registry commit.

Each batch must state:

- source and canonical range;
- entries added/changed;
- fidelity-sensitive terminology encountered;
- contradictions/ambiguities discovered;
- whether visual arbitration was required;
- whether any item remains unresolved;
- whether any post-Szondian evidence was consulted and why.

A batch may be accepted with explicit `UNRESOLVED` items when source ambiguity itself is faithfully preserved and the ambiguity does not indicate unreviewed evidence loss.

## 15. Validation requirements

P2A validation must test structure and epistemic boundaries, not doctrinal truth by software assertion.

Machine validation should enforce at least:

- unique stable doctrine IDs;
- valid admitted `sourceId` values;
- source-layer consistency with `config/source_catalog.json`;
- valid canonical anchors;
- non-empty source-near statement;
- required assertion-strength field;
- allowed enums;
- explicit author separation;
- no executable trigger fields;
- no orphan relation targets;
- deterministic serialization;
- schema version presence.

Machine validation cannot prove that a doctrinal paraphrase is semantically faithful. Source/clinician review remains required for acceptance.

## 16. Clinician review boundary

Because P2A can affect later clinical interpretation, doctrine acceptance requires human review proportional to doctrinal consequence.

High-risk entries include especially:

- hereditary/genetic/genotropic claims;
- sexuality and sexual inversion/perversion terminology;
- criminality/psychopathy/psychosis/pathodiagnostic claims;
- causal statements;
- claims whose mistranslation would change assertion strength;
- entries involved in source contradictions;
- entries requiring PDF visual arbitration.

A machine-valid registry is not automatically an accepted doctrine registry.

## 17. Storage contract

The authoritative registry representation should be versioned structured data under a clearly doctrinal path, separate from generated canonical access and executable logic.

Recommended initial paths:

- `doctrine/schema/primary_doctrine.schema.json`
- `doctrine/registry/*.jsonl`
- `doctrine/coverage/*.jsonl`

Serialization for committed JSONL must be deterministic:

- UTF-8;
- LF newlines;
- one JSON object per line;
- stable field ordering determined by the writer/validator;
- no timestamps inside hashed semantic records;
- deterministic record ordering by `doctrineId` within each source file.

The exact schema and validator are implementation work under this specification and must not weaken any rule above.

## 18. Gate acceptance criteria

`P2A_PRIMARY_DOCTRINE_PASS` requires all of the following:

1. a versioned registry schema is accepted;
2. source-layer separation is mechanically enforced;
3. all accepted entries have exact admitted-source provenance;
4. Szondi-primary wording/conceptual force is preserved without modernization or sanitization;
5. hereditary/genetic/genotropic/transgenerational content is preserved literally where the source is literal;
6. sexual/pathodiagnostic/criminological terminology is not silently suppressed;
7. assertion strength, conditions and exceptions are explicitly represented;
8. contradictions and ambiguity can be represented without forced reconciliation;
9. no executable trigger logic is embedded in P2A;
10. a durable coverage ledger accounts for the admitted doctrinal corpus;
11. machine structural/provenance validation passes;
12. required source/clinician review is recorded;
13. post-Szondian material remains authorially distinct;
14. no unresolved evidence-loss or provenance blocker remains hidden;
15. current limitations and reopenable items are recorded in the final gate record.

P2A does not pass merely because a large number of doctrine entries exist.

## 19. Fail-closed conditions

P2A pauses at the affected boundary when:

- source identity or canonical provenance cannot be established;
- a source passage appears mistranscribed or semantically suspicious and original evidence cannot resolve it;
- visual form may alter meaning but no available visual arbiter resolves it;
- authorial layer cannot be determined;
- paraphrase would require choosing among materially different meanings;
- assertion strength cannot be determined safely;
- a contradiction is being smoothed rather than represented;
- a proposed entry depends on Deri/Mélon to create primary Szondi content;
- a reviewer proposes modern terminology as replacement rather than separate context;
- executable logic is required to make the doctrine entry coherent.

The correct state is `UNRESOLVED`, not plausible completion.

## 20. Non-goals for P2A

P2A does not attempt to:

- prove Szondi scientifically correct by contemporary standards;
- reconcile Szondi with modern genetics;
- sanitize historically dated concepts;
- decide which doctrines are clinically advisable today;
- create the final interpretation engine;
- create the Clinical Evidence Graph;
- integrate competing claims into a patient narrative;
- produce clinician or client reports;
- complete source procedures that Szondi himself leaves incomplete.

## 21. Reopening rule

An accepted doctrine entry may be reopened when stronger admitted evidence, corrected source access, visual arbitration or source review shows that its representation is materially wrong or incomplete.

Reopening preserves history and stable identity where possible, identifies downstream dependents, and does not mutate the original evidence.

## Final invariant

> **P2A is a fidelity registry, not an interpretation shortcut: preserve exactly who says what, where, with what force, under what conditions and with what uncertainty before software is allowed to decide what any of it means for a protocol.**
