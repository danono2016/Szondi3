# Ich-Analyse P2A — CONTINUATION CHECKPOINT

**Purpose:** durable handoff if the active chat ends. Repository state, not chat history, is authoritative.

**Branch:** `work/p2a-ich-analyse-full-read-001`  
**PR:** #52, draft, open, mergeable  
**Scope:** exclusively `SZ_IA_1956_A` and `SZ_IA_1956_B`  
**Do not modify:** `SZ_LEHR_1972`, `SZ_SA_1948`, their doctrine IDs, coverage, verification, checkpoints, or any other source-local writer artifacts.

## Governing curation rule

`read everything -> account for everything -> store only critical doctrine`

Canonical TXT is complete textual memory. Coverage is exhaustive. Registry is a compact retrieval index, not a reproduction of the books. Before promoting a doctrine ask: **If this entry is omitted, do we lose information critical for calculation, interpretation, or faithful reconstruction of doctrine?**

Do not promote ordinary examples, repetitions, historical exposition, secondary enumerations, transitions, or details recoverable from canonical context. Preserve hereditary/genetic/genotropic, sexual, pathological, criminological and historical terminology at exact source strength when doctrinally critical. Preserve epistemic qualifiers (`Hypothese`, `Arbeitshypothese`, `Annahme`, `scheint`, `u. E.`, tendencies/probabilities) without upgrading them.

## Book-level reading

- `SZ_IA_1956_A`: full source-order PDF reading complete, EOF reached.
- `SZ_IA_1956_B`: full source-order PDF reading complete, EOF reached.

Book-level full reading does not substitute for canonical U-by-U P2A coverage.

## SZ_IA_1956_A status

**Canonical BODY extent:** `U000001-U003200`.

**P2A canonical coverage:** COMPLETE THROUGH EOF (`U003200`).

Final batch:
- `P2A-IA-A-018`
- interval `BODY U003150-U003200`
- retained doctrine IDs: `DR_SZ_IA_1956_A_000050`, `DR_SZ_IA_1956_A_000051`
- batch coverage explicitly states that this closes source-local canonical BODY coverage for `SZ_IA_1956_A` at `U003200 / EOF`.

Final critical objects include:
- ordered Ego-development stages: Partizipation -> Inflation -> Introjektion -> Negation;
- warning that any `Unifunktion` can be dangerous;
- ideal integration of all four elementary Ego functions;
- PDF-arbitrated `integriertes Ich = Sch ± ±` and `Desintegration = Sch 0 0`.

Earlier core A doctrine includes the four elementary functions/signs (`-p`, `+p`, `+k`, `-k`), Egodiastole/Egosystole, Partizipation/Projection, familial Projection/Genotropismus, Integration vs Wahl, Negation as Hauptbegriff with Verdrängung as Unterform, and other compact project-critical Sch/Ego rules.

**Administrative note:** the older `SZ_IA_1956_A_FULL_READ_CHECKPOINT.md` may still show a stale intermediate P2A position. Do not use that stale line to resume A. The authoritative coverage record is Batch 018 plus this continuation checkpoint. A requires no further source-order P2A extraction unless a later audit identifies a specific defect.

## SZ_IA_1956_B status

**Canonical BODY extent:** `U000001-U003722`.

**Book-level read:** EOF reached.

**Canonical P2A extraction:** NOT YET STARTED.

**Next exact source-order position:** `SZ_IA_1956_B:BODY U000001`.

No `DR_SZ_IA_1956_B_*` doctrine objects existed at checkpoint creation. Begin B IDs at `DR_SZ_IA_1956_B_000001` unless repository state at resumption shows another writer has legitimately created B objects; always re-check before writing.

Priority themes for B remain project-relevant only: p/k/Sch; Egodiastole/Egosystole; within-factor dialectic; Vorder-/Hinter-Ich and complementary profiles; `Ich-Bild` vs `Ich-Mechanismus`; defense mechanisms; Integration/Desintegration; character/fate where it changes test interpretation; methodological limits; critical hereditary/genetic/genotropic claims; dream/Wahn/Glaube only when they introduce a compact doctrine needed for faithful reconstruction or test interpretation.

## Verification state at checkpoint

PR head before this checkpoint write: `a69abfc7b7d7b7410550d73fbb7596b872acde56` (`Verify IA A batch 018 EOF`). On that head all four checks completed successfully:
- P2A doctrine registry — success
- Foundation verification — success
- P0 canonical access — success
- P0 source inspection — success

The checkpoint write itself creates a newer head. On resumption, verify current PR head and CI before the next important write.

## Resume protocol

1. Read this file first.
2. Check PR #52, branch head, changed files and all current CI checks.
3. Confirm no concurrent `DR_SZ_IA_1956_B_*` writer activity.
4. Do not touch source-local artifacts outside IA.
5. Begin `SZ_IA_1956_B` at `BODY U000001`.
6. Work source-order in bounded batches: canonical read -> selective atomic doctrine -> coverage -> verification -> PDF arbitration only when needed.
7. Keep registry minimal. Cases remain anchors/examples unless they add a genuinely distinct critical rule.
8. At each batch report: source | U interval | doctrine IDs created | units without doctrine | ambiguities | PDF arbitration | next U.

> **Continuation invariant:** A is P2A-covered to EOF. Resume only with B at `U000001`, after repository/PR/CI revalidation.