# Lehrbuch P2A compaction audit — DR 000027–000047

**Source:** `SZ_LEHR_1972`  
**Policy:** `docs/P2A_DOCTRINE_SELECTION_AND_COMPACTION_POLICY.md`

## Result

Original standalone objects: **21**  
Retained standalone objects in this segment: **4**  
Reduction: **17 objects / 81%**

Several retired objects are not lost; they are redundant restatements of retained core objects `000017`, `000019`, `000021` from the preceding compacted segment.

## Retained cores

- `000028` — **Gentheorie basic work hypothesis:** genes as sources of drives / specific Triebgene, with hereditary transmission and the family/ancestral-past tendency concept absorbed as context while keeping hypothesis status.
- `000034` — **Triebgegensatzpaare versus Freud's Triebdualismus:** allelic hereditary basis of opposed drive tendencies/needs.
- `000040` — **two polarities:** faktorielle/Strebungspolarität and vektorielle/Bedürfnispolarität.
- `000047` — **drive synthesis:** needs are the genobiological units, drives are syntheses; Verschränkung follows genetically prescribed laws but its process/timing also depends on internal/external factors including the Ego.

## Retirement map

| IDs | Decision |
|---|---|
| 000027, 000029–000033 | `MERGE_INTO_CORE -> 000028` |
| 000035–000036 | `MERGE_INTO_CORE -> 000017` (smallest genetic tendency unit already retained) |
| 000037 | `MERGE_INTO_CORE -> 000019` (factor = paired tendencies already retained) |
| 000038 | `MERGE_INTO_CORE -> 000021` (vector = combination of factors already retained) |
| 000039 | `MERGE_INTO_CORE -> 000047` |
| 000041 | `MERGE_INTO_CORE -> 000034/000040` |
| 000042 | `OMIT_NONCRITICAL` — animal/human instinct-link background, readily recoverable from context |
| 000043–000044 | `ANCHOR_OR_EXAMPLE_ONLY` — infant oral-sadistic Probemischung example, not a governing doctrine needed independently |
| 000045–000046 | `MERGE_INTO_CORE -> 000047` |

## Fidelity safeguards

- Gentheorie remains explicitly a hypothesis where Szondi labels it `Arbeitshypothese`/`Annahme`; compaction does not convert it to contemporary fact.
- Hereditary/genobiological content is retained rather than replaced by metaphorical family-pattern language.
- The distinction between *factorial* and *vectorial* polarity remains separately retrievable because it can matter to factor/vector interpretation.
- The Ego's role in Verschränkung remains preserved in `000047`.
- The oral-sadistic infant example remains reachable through canonical coverage; it is not promoted to corpus-level critical doctrine.
- Stable retired IDs remain reserved through this audit and Git history.
