# Lehrbuch P2A compaction audit — DR 000001–000026

**Source:** `SZ_LEHR_1972`  
**Policy:** `docs/P2A_DOCTRINE_SELECTION_AND_COMPACTION_POLICY.md`  
**Goal:** preserve critical doctrine for calculation/interpretation/retrieval while removing duplication, introductions, ordinary examples and over-fragmentation.

## Result

Original standalone doctrine objects: **26**  
Retained core objects after audit: **10**  
Reduction in this segment: **16 objects / 61.5%**

No canonical coverage is removed. Retired IDs remain historically reserved through this audit map and Git history.

## Decisions

| Doctrine ID | Decision | Retained in / reason |
|---|---|---|
| 000001 | MERGE_INTO_CORE | `000002` — test belongs to Schicksalspsychologie and requires its conceptual framework; independent object not needed. |
| 000002 | KEEP_CORE | Governing interpretation rule: technical use without Schicksalspsychologie is insufficient. |
| 000003 | MERGE_INTO_CORE | `000004` — hereditary oppositions at birth belong to the broader fate-formation model. |
| 000004 | KEEP_CORE | Core hereditary/multifactorial fate model, including possible overcoming or repetition of Zwangsschicksal. |
| 000005 | KEEP_CORE | Core method: plural Existenzmöglichkeiten; one profile is not the whole person; serial profiles required. |
| 000006 | MERGE_INTO_CORE | `000005` — primary purpose is discovery of Existenzmöglichkeiten rather than psychiatric fixation. |
| 000007 | MERGE_INTO_CORE | `000005` — therapeutic/testological consequence of the same existence-possibility doctrine. |
| 000008 | OMIT_NONCRITICAL | Introductory justification/roadmap; later factor/vector doctrines carry the substantive content. |
| 000009 | KEEP_CORE | Important anti-overinterpretation rule: findings should be checked through multiple interpretive methods. |
| 000010 | KEEP_CORE | Core definition of Trieb as radical; absorbs general radical properties and the two general drive traits. |
| 000011 | MERGE_INTO_CORE | `000010` — elaboration of Triebradikal properties. |
| 000012 | MERGE_INTO_CORE | `000021` — eight-factor/four-vector system belongs to the vector architecture object. |
| 000013 | OMIT_NONCRITICAL | Instinkthandlung background distinction; recoverable from canonical context, not critical to test interpretation. |
| 000014 | OMIT_NONCRITICAL | Triebhandlung-vs-instinct elaboration; same reason as 000013. |
| 000015 | KEEP_CORE | Critical interpretive thesis: human drive life is interaction of Triebbedürfnisse with Ich-Triebe. |
| 000016 | KEEP_CORE | Rand–Mitte is a named interpretive method central to the project. |
| 000017 | KEEP_CORE | Core genetic definition: Triebtendenz/Triebstrebung as smallest genetic drive unit. |
| 000018 | MERGE_INTO_CORE | `000019` — paired allelic tendency structure belongs to the Triebbedürfnis/Triebfaktor definition. |
| 000019 | KEEP_CORE | Core definition of factor/need as paired allelic tendencies. |
| 000020 | ANCHOR_OR_EXAMPLE_ONLY | `000019` — Männlichkeit polarity is an example of the paired-tendency model, not a separate governing doctrine. |
| 000021 | KEEP_CORE | Core vector architecture; absorbs the four named vector definitions. |
| 000022 | MERGE_INTO_CORE | `000021` — Sexualtrieb is one member of the four-vector taxonomy. |
| 000023 | MERGE_INTO_CORE | `000021` — Kontakttrieb is one member of the four-vector taxonomy. |
| 000024 | MERGE_INTO_CORE | `000021` — Ich-Trieb/Egodiastole–Egosystole remains explicitly preserved inside the core vector object. |
| 000025 | MERGE_INTO_CORE | `000021` — Paroxysmaltrieb is one member of the four-vector taxonomy; its later detailed doctrine will remain separately retrievable. |
| 000026 | MERGE_INTO_CORE | `000010` — general traits of all drives belong to the governing Trieb definition. |

## Fidelity safeguards

- `000004` retains hereditary/ancestral/Zwangsschicksal content without modernization.
- `000005` retains the 8–10 profile rule and the anti-diagnostic priority of Existenzmöglichkeiten.
- `000017` and `000019` remain separate because the smallest genetic unit and the paired-factor construction answer materially different future questions.
- `000020` is not erased from the source: its canonical range remains in coverage and is explicitly mapped as an example of `000019`.
- The four vectors are compacted into one taxonomy object, but their German names and defining paired needs remain represented in the retained statement/terms.
- No retired stable ID is recycled.

## Working implication

This segment demonstrates the intended scale: source-order reading remains exhaustive, while the registry contracts toward high-value retrieval objects. Subsequent Lehrbuch audits should use the same threshold before forward extraction resumes.
