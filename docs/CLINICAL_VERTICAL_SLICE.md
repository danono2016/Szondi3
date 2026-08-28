# SZONDI3 — Clinical vertical slice

**Status:** ACTIVE IMPLEMENTATION PATH  
**Purpose:** move from a verified deterministic engine to a usable, source-grounded clinical instrument without making corpus exhaustiveness a prerequisite for every useful increment.

## Product goal

The project is building a versatile Szondi instrument for real clinical use. Canonical TXT/PDF sources remain the primary evidential basis. Git, doctrine registries, tests and governance artifacts exist to make the instrument safer, reproducible and traceable; they are infrastructure, not the product goal.

## Vertical path

The working path is now:

`administration -> P1 deterministic facts -> P2B executable interpretation -> clinical integration -> clinician report`

Each layer must preserve the distinction between:

1. observed/administered data;
2. deterministic calculations;
3. source-grounded Szondian interpretation;
4. limitations, alternatives and unresolved input;
5. later clinical synthesis by the therapist.

No layer may silently convert a test configuration into a diagnosis or person-level verdict beyond the admitted source evidence.

## First implemented P2B tranche

The first executable tranche intentionally starts with high-confidence structural semantics and safeguards:

- Wurzelfaktor direction safeguards, including negative root != automatic Verdrängung;
- TspQu and %Sy-Re method-scope safeguards;
- Dur-Moll not sufficient alone for social valuation;
- Sozialindex < 40% does not license inference of a criminal act;
- elementary Ego-function semantics for `-p`, `+p`, `+k`, `-k` from Ich-Analyse;
- `-k` / Negation is broader than Verdrängung;
- `Sch ±±` and `Sch 00` may receive source-faithful testological labels while explicit anti-overreach prevents conversion into unsupported global person-level conclusions.

These claims are initially `FORMALIZATION_REVIEWED`. They are deliberately **not** `CLINICIAN_REVIEWED` or `APPROVED`. Preview/review evaluation is executable now; production mode admits only later explicitly approved claims.

## Runtime boundary

P2B consumes facts exported from existing P1 objects. It does not rescore selections, recompute P1 with different rules, resolve P1 ambiguity, or invent a majority/tie-break convention.

Missing or ambiguous prerequisite facts fail closed locally. Other independent claims may still evaluate.

## Clinical review path

The next clinically meaningful review is not another corpus audit. It is review of the initial executable claims as they appear on representative complete protocols. For each claim the reviewer should be able to see:

- the P1 fact that activated it;
- the exact claim wording and assertion mode;
- linked doctrine IDs and source IDs;
- anti-inferences that constrain its use;
- sensitive-domain flags;
- unresolved or blocked prerequisites.

After that review, selected claims can be promoted individually to `CLINICIAN_REVIEWED` and then `APPROVED` for production use.

## Next implementation increments

Priority is driven by clinical usefulness, not by the next unprocessed canonical unit:

1. build a complete protocol/session object that assembles P1 outputs and P2B facts in one place;
2. add Vorder-Ich/Hinter-Ich and complement-aware facts and guards;
3. add longitudinal comparison across repeated profiles/series;
4. add structured report sections that keep calculations, Szondian interpretation, uncertainty and therapist synthesis separate;
5. validate on synthetic/de-identified complete protocols with manual cross-checks;
6. expand doctrine/P2B from Schicksalsanalyse, Therapie and Triebpathologie when a concrete clinical capability requires it.

The unfinished primary corpus remains valuable, but it is no longer treated as a blanket blocker on clinically useful, well-supported P2B work.
