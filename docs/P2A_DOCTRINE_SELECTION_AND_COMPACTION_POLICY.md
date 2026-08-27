# SZONDI3 — P2A DOCTRINE SELECTION AND COMPACTION POLICY

**Status:** WORKING CORPUS POLICY — applies before further source-order population  
**Layer:** `DOCTRINE_REPRESENTATION`  
**Purpose:** keep the doctrinal corpus critical, compact and retrievable without reproducing the admitted books.

## 1. Core distinction

P2A has three different completeness obligations and they MUST NOT be confused:

1. **Reading completeness:** every admitted canonical unit is actually reviewed in source order.
2. **Coverage completeness:** every reviewed range is accounted for in the coverage ledger, including units producing no doctrine.
3. **Registry selectivity:** only doctrinally critical, distinct, future-retrieval-worthy information becomes a doctrine object.

Therefore:

> **100% coverage does not imply one doctrine per passage, paragraph, example or formulation.**

The canonical TXT/PDF is the complete textual memory. The registry is a compact semantic/provenance map back into that memory.

## 2. Admission test for a doctrine object

Create or retain a separate doctrine entry only when omission would cause loss of at least one materially distinct item needed for later faithful reconstruction:

- a core definition or specifically Szondian concept;
- a major theoretical proposition or causal/hereditary/genotropic claim;
- an interpretive rule that materially changes how a test reaction/vector/profile is understood;
- an explicit condition, exception, limit or anti-overinterpretation rule;
- a method rule necessary to understand how Szondi obtains or construes a result;
- a diagnostically/pathodiagnostically important association stated with meaningful force;
- an epistemically important qualification (`Hypothese`, `Annahme`, `scheint`, explicit uncertainty, failure/limit);
- a contradiction, revision or diachronic development that must remain separately addressable;
- a rare but consequential claim likely to disappear from retrieval if represented only by broad topic tags.

If none of these is true, coverage is normally sufficient.

## 3. Material that normally should NOT become a separate doctrine

Unless it changes doctrine materially, do not create separate entries for:

- chapter/section headings;
- bibliographic or historical background;
- repeated restatements of an already represented claim;
- rhetorical explanation or pedagogical elaboration;
- lists of examples that merely instantiate a represented rule;
- worked cases whose only function is to demonstrate an already represented method;
- repeated factor/vector descriptions differing only in illustrative wording;
- enumerations that can be preserved as conditions/examples inside one core doctrine;
- transition sentences;
- source cross-references;
- quantitative tables whose doctrinal meaning is already stated in prose;
- every individual phenotype/profession/character example when a broader source-stated category already preserves the critical association;
- low-consequence details that are easily recoverable by canonical context once the governing doctrine is retrieved.

## 4. Granularity rule

The registry should be **semantically atomic, not sentence-atomic**.

One object may contain a tightly coupled assertion set when separating it would create artificial fragments that future retrieval would always need to reassemble. Conditions and exceptions belong with the doctrine they constrain.

Conversely, do not create giant chapter summaries that collapse independent claims or hide contradiction/epistemic differences.

Practical question:

> **Would a future expert normally need this object independently of its neighboring object?**

If no, merge or omit it.

## 5. Retrieval-value test

Before creating a new entry, ask:

1. What future question would retrieve this entry?
2. Is that question materially different from the question answered by an existing entry?
3. Could the same information be recovered safely by reconsulting the canonical context of an existing doctrine anchor?
4. Does a separate object preserve a condition, exception, contradiction or epistemic distinction that would otherwise be lost?

If answers 1–2 are weak and 3 is yes, do not create the entry.

## 6. Examples and cases

Cases are not automatically doctrine.

Create a case-derived doctrine object only when Szondi uses the case to establish, qualify or exemplify a rule that is not adequately represented elsewhere, or when the case has exceptional doctrinal importance for a named method/concept.

Otherwise record the range in coverage and, where useful, attach the case as an `EXAMPLE_OF` relation or source anchor to the governing doctrine rather than creating many case-specific doctrine objects.

## 7. Tables and visual material

Visual arbitration remains fail-closed where layout affects meaning. But visual complexity does not itself justify more registry entries.

After arbitration, extract only the critical doctrinal structure. Do not serialize an entire table into doctrine objects when the canonical/PDF source remains directly addressable.

## 8. Compaction of existing registry

Existing P2A entries are subject to a **lossless doctrinal compaction audit**.

Classify each current entry as:

- `KEEP_CORE` — distinct critical doctrine;
- `MERGE_INTO_CORE` — useful content, but not independently retrieval-worthy;
- `ANCHOR_OR_EXAMPLE_ONLY` — preserve provenance/example relation without a standalone doctrine;
- `OMIT_NONCRITICAL` — coverage is sufficient;
- `KEEP_SEPARATE_EPISTEMIC` — apparently similar content whose different assertion strength/condition/contradiction requires separation;
- `UNRESOLVED` — cannot compact safely without source reconsultation.

Compaction MUST NOT:

- lose exact source anchors;
- erase hereditary/genetic/genotropic, sexual, pathodiagnostic or criminological content merely because it is uncomfortable or repetitive;
- collapse categorical and hypothetical statements into one strength;
- erase conditions/exceptions;
- harmonize contradictions;
- recycle retired doctrine IDs.

Retired IDs remain historically reserved and should be mapped to the retained core object when a merge occurs.

## 9. Size is not a success metric

Neither number of doctrine entries nor registry byte size is a completion metric.

Preferred outcome is the **smallest registry that still permits faithful reconstruction of all critical doctrine through source anchors and canonical reconsultation**.

The final corpus may be much smaller than the books because it is an index of critical doctrine, while the books themselves remain the full evidence store.

## 10. Relationship to cross-source indexing

Do not compensate for an overgrown source-local registry by building an even larger transversal ontology.

Cross-source concepts should link a compact set of high-value doctrine objects. Synonyms, aliases and terminology variants belong primarily in term/concept indexes, not as duplicate doctrines.

## 11. Working rule for further Lehrbuch extraction

Until the existing Lehrbuch registry has been audited, new extraction should use a deliberately higher admission threshold:

- prioritize definitions, governing rules, interpretive constraints, exceptions, epistemic limits and major theory;
- represent repeated examples through anchors/coverage where possible;
- prefer one well-formed doctrine with multiple source anchors over several near-duplicates when authorial meaning and assertion strength are the same;
- stop and reconsult source context before merging anything that may contain a genuine distinction.

## Final invariant

> **Read everything. Account for everything. Store only what is doctrinally critical. Retrieve the rest from the canonical source when needed.**
