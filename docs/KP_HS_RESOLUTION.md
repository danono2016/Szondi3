# `kp/hs` — Final resolution

**Status:** `RESOLVED`  
**Decision date:** 2026-08-27  
**Primary source:** `SZ_LEHR_1972`  
**Scope:** abbreviated Triebformel semantics and deterministic representation

## Final definition

The **abbreviated Triebformel** is the polar representation of the Triebformel structure in which the symptomatic zone is confronted with the root zone and the median submanifest/sublatent factors are omitted.

The **simple abbreviated form** represents the leading symptomatic factor over the leading/deepest root factor, for example:

`k/s`

The **extended abbreviated form** preserves the complete factorial groups that constitute the symptomatic and root lines:

`kp/hs`

Operationally:

`extended abbreviated formula = symptomatic line / root line`

The submanifest/sublatent middle line is omitted.

For Fall 18, the already source-constrained complete Triebformel partition is:

`kp / mdhye / hs`

and the extended abbreviated projection is therefore:

`kp/hs`

The slash `/` separates **symptom from root**. It does not denote vectors or arbitrary halves of the profile.

## Critical algorithmic clarification

`p` and `h` are **not added later** to `k/s` by a special expansion rule. They appear in `kp/hs` because, under the rules that constitute the complete Triebformel, `p` belongs to the symptomatic line with `k`, while `h` belongs to the root line with `s`.

Consequently there is no separate universal `kp/hs` neighbour/threshold selector to discover or implement.

The number of factors in either outer line is not fixed artificially. The extended abbreviation contains however many factors legitimately belong to the symptomatic and root lines. It is therefore not constrained to a `2/2` shape.

## Epistemic classification

### SOURCE-ESTABLISHED

- `SZ_LEHR_1972` `U003718-U003720`: high TspG identifies Symptomfaktoren; low TspG identifies Wurzelfaktoren.
- `U003734-U003739`: Triebformel is a symptom/root fraction; the complete form has symptomatic, submanifest/sublatent and root lines; factors whose TspG difference is not greater than 2 may occupy the same line.
- `U004527-U004530`: Fall 18 prints both `k/s` and `kp/hs` under `Abgekürzte Triebformel`, before the separate `Vollständige Triebformel` heading.
- Fall 18's complete-formula partition, after Tabelle 13 normalization, is reproduced deterministically as `kp / mdhye / hs` by the existing complete-formula implementation.

### IMPLEMENTATION-INFERRED, STRONGLY SOURCE-CONSTRAINED

The universal executable representation of the **extended** abbreviated formula is the projection of an already constituted complete Triebformel onto its symptomatic and root lines, with the median line omitted.

This is deliberately classified as implementation-inferred rather than as a verbatim universal Szondi rule because no sentence has been located in which Szondi explicitly formulates this projection as a general algorithm. The inference adds no new factor-selection threshold: all membership decisions are delegated to the complete-formula constitution already constrained by primary evidence.

### LOCAL FAIL-CLOSED BOUNDARIES

The conceptual `kp/hs` problem is closed. Only particular ambiguous inputs remain fail-closed:

- if the complete-formula partition is non-unique under admitted source rules, the extended abbreviation is also non-unique and must fail closed;
- if the **simple** abbreviation has tied extrema, the existing tie policy remains separate and fail-closed where no source-authorized selector exists.

These local ambiguity boundaries do **not** reopen the conceptual status of `kp/hs`.

## Relationship to earlier project records

This decision supersedes the earlier `RESOLVED_FAIL_CLOSED` status for a separate universal broader-abbreviation selector in:

- `docs/P1_RESOLUTION_SWEEP.md`, item 1;
- `docs/PROJECT_CHECKPOINT.md`, the `kp/hs` residual-limitations bullet;
- `docs/LEHRBUCH_FULL_READ_CHECKPOINT.md`, the passages stating that a universal broader selector remains open.

Those records remain historically useful: they correctly rejected the false claim that `kp/hs` is itself the **complete formula**, and they correctly prohibited an invented top/bottom neighbour threshold. The present resolution does not reverse either safeguard. It distinguishes the authentic abbreviated formula from the complete formula while deriving the extended abbreviation structurally from the latter's already-established outer-line membership.

## Implementation

`szondi3/abbreviated_formula.py` now provides an extended abbreviated formula by projecting `unique_formula_partition(series)` onto its symptomatic and root lines. No separate expansion selector is used.

Regression coverage includes:

- Fall 18 -> `kp/hs`;
- a variable-cardinality witness showing that the outer groups are not forced to contain two factors each;
- preservation of the existing fail-closed policy for simple-form extrema ties.

## Final project rule

> **`kp/hs` is RESOLVED.**
>
> `extended abbreviated formula = symptomatic line / root line, with the submanifest middle line omitted`
>
> Ambiguity in the underlying complete-formula partition remains local and fail-closed; it does not reopen the conceptual definition.
