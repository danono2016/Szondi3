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

A requires no further source-order P2A extraction unless a later audit identifies a specific defect.

## SZ_IA_1956_B status

**Canonical BODY extent:** `U000001-U003722`.

**Book-level read:** EOF reached.

**Canonical P2A extraction:** COMPLETE THROUGH `BODY U000181`.

Completed batch:
- `P2A-IA-B-000`
- interval `BODY U000001-U000181`
- retained doctrine IDs `DR_SZ_IA_1956_B_000001` through `DR_SZ_IA_1956_B_000005`
- critical core: three forms of innere Ich-Dialektik; p:k Egodiastole/Egosystole inner defense; intrafactorial `−p/+p` and `+k/−k` with `±p/±k`; Zwang as Intronegation / `Sch = ± 0`; historical Moll-Ich Sch interpretation grid.

Batch 000 canonical witness:
- workflow `33105644492`
- artifact `9660348836`
- digest `sha256:cf40c0eb335eb3ffcc3b718730d07be500385ff717c256c484aa0861ef5a50dc`
- witness head `9cd059411318cb41e745cea04579e3962e4b7b4e`.

**Next exact source-order position:** `SZ_IA_1956_B:BODY U000182` (`Kapitel XVIII — Die Dialektik zwischen dem Vorder-Ich und dem Hinter-Ich`).

Priority themes for B remain project-relevant only: p/k/Sch; Egodiastole/Egosystole; within-factor dialectic; Vorder-/Hinter-Ich and complementary profiles; `Ich-Bild` vs `Ich-Mechanismus`; defense mechanisms; Integration/Desintegration; character/fate where it changes test interpretation; methodological limits; critical hereditary/genetic/genotropic claims; dream/Wahn/Glaube only when they introduce a compact doctrine needed for faithful reconstruction or test interpretation.

## Verification state

Before B Batch 000, PR head `9cd059411318cb41e745cea04579e3962e4b7b4e` had all four checks green: P2A doctrine registry, Foundation verification, P0 canonical access, P0 source inspection. Batch 000 and these checkpoint updates create newer heads. On resumption, verify the current PR head and CI before the next important write.

## Resume protocol

1. Read this file first.
2. Check PR #52, branch head, changed files and all current CI checks.
3. Confirm no concurrent `DR_SZ_IA_1956_B_*` writer activity beyond the legitimate objects recorded here.
4. Do not touch source-local artifacts outside IA.
5. Resume `SZ_IA_1956_B` at `BODY U000182`.
6. Work source-order in bounded batches: canonical read -> selective atomic doctrine -> coverage -> verification -> PDF arbitration only when needed.
7. Keep registry minimal. Cases remain anchors/examples unless they add a genuinely distinct critical rule.
8. At each batch report: source | U interval | doctrine IDs created | units without doctrine | ambiguities | PDF arbitration | next U.

> **Continuation invariant:** A is P2A-covered to EOF. B is covered through `U000181`; resume B at `U000182` after repository/PR/CI revalidation.