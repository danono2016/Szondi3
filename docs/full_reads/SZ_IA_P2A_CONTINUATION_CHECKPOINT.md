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

Final batch `P2A-IA-A-018` closes `BODY U003150-U003200`. A requires no further source-order P2A extraction unless a later audit identifies a specific defect.

## SZ_IA_1956_B status

**Canonical BODY extent:** `U000001-U003722`.  
**Book-level read:** EOF reached.  
**Canonical P2A extraction:** COMPLETE THROUGH **`BODY U000679`**.

Completed:
- `P2A-IA-B-000` — `U000001-U000181` — `DR_SZ_IA_1956_B_000001` through `000005`.
- `P2A-IA-B-001` — `U000182-U000289` — `DR_SZ_IA_1956_B_000006` through `000010`.
- `P2A-IA-B-002` — `U000290-U000679` — `DR_SZ_IA_1956_B_000011` through `000014`.

B-002 critical core:
- complement-profile diagnostic rule preventing foreground-only Fehldiagnosen;
- `+k` / introjektives Hab-Ich interpretation with `unserer Erfahrung nach` preserved;
- prodromal `Sch = ± ±` -> `Sch = 0 0` sequence with source's `zumeist` qualifier;
- explicit `vorläufig offen` limit on exhaustiveness of the eight complementary Ego-fates.

Batch 002 canonical witness:
- workflow `33110371265`
- artifact `9662281026`
- digest `sha256:861c679719dfd3686a711ab8bfc6d2743aaa1b5124e7e1c441f687c250fd3c60`
- witness head `2fee089fd1d01cac88452ca6d592698acc285be4`.

**Next exact source-order position:** `SZ_IA_1956_B:BODY U000680` — `Kapitel XIX` in `ABSCHNITT IV — ÄUSSERE ICH-DIALEKTIK`.

Priority themes remain project-relevant only: p/k/Sch; Egodiastole/Egosystole; Vorder-/Hinter-Ich; `Ich-Bild` vs `Ich-Mechanismus`; external defense mechanisms; Integration/Desintegration; character/fate where it changes test interpretation; methodological limits; critical hereditary/genetic/genotropic claims; dream/Wahn/Glaube only when they add compact doctrine needed for faithful reconstruction or test interpretation.

## Verification state before B-002 write

PR head `2fee089fd1d01cac88452ca6d592698acc285be4` was draft/open/mergeable and all four checks were green: P2A doctrine registry, Foundation verification, P0 canonical access, P0 source inspection.

B-002 and this checkpoint update create a newer head. On resumption, verify the current PR head and CI before the next important write.

## Resume protocol

1. Read this file first.
2. Check PR #52, branch head, changed files and all current CI checks.
3. Confirm no concurrent `DR_SZ_IA_1956_B_*` writer activity beyond the legitimate objects recorded here.
4. Do not touch source-local artifacts outside IA.
5. Resume `SZ_IA_1956_B` at `BODY U000680`.
6. Work source-order in bounded batches: canonical read -> selective atomic doctrine -> coverage -> verification -> PDF arbitration only when needed.
7. Keep registry minimal. Cases remain anchors/examples unless they add a genuinely distinct critical rule.
8. At each batch report: source | U interval | doctrine IDs created | units without doctrine | ambiguities | PDF arbitration | next U.

> **Continuation invariant:** A is P2A-covered to EOF. B is covered through `U000679`; resume B at `U000680` after repository/PR/CI revalidation.
