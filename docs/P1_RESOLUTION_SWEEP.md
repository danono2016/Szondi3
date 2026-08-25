# P1 Resolution Sweep

**Status:** ACTIVE P1 CLOSURE RECORD

## Purpose

This document tracks every P1 item that is still partial, source-underdetermined, deferred, or potentially out of scope before `P1_DETERMINISTIC_ENGINE_PASS` can be considered.

The governing evidence order is:

`SZONDI_PRIMARY -> POST-SZONDI SECONDARY (Deri -> Melon) -> external research only if internal admitted evidence is insufficient`

Secondary sources may clarify where to look or how later tradition understood a rule, but they do not override a clear Szondi-primary statement.

## Closure statuses

- `RESOLVED_IMPLEMENTED` — source-authorized deterministic rule implemented and tested.
- `RESOLVED_FAIL_CLOSED` — source does not determine a unique executable rule; software preserves the ambiguity explicitly.
- `RESOLVED_OUTSIDE_P1` — material belongs to doctrine, executable interpretation, clinical integration, or another later layer rather than deterministic scoring.
- `BLOCKED_MISSING_EVIDENCE` — a specific source needed to resolve the item is not yet admitted/available.
- `ACTIVE_RESEARCH` — internal corpus sweep still in progress.

## Active items

### 1. Abbreviated Triebformel: relation between simple extreme fraction and broader symptom/root fraction

**Current status:** `ACTIVE_RESEARCH`

Primary findings so far:

- Lehrbuch Fall 11 prints a simple abbreviation `m/s` although the complete formula contains a broader symptomatic/root structure.
- Lehrbuch Fall 16 prints `e/d` and `e/m` in a tied-root case.
- Lehrbuch Fall 18 prints both `k/s` and `kp/hs`.
- Lehrbuch separately uses the concepts `leitender Symptomfaktor` and `dynamischster Wurzelfaktor`, showing that a leading factor can be distinguished from the larger set of symptomatic/root factors.
- Lehrbuch short-series guidance treats the `abgekuerzte Triebformel` as requiring at least one sufficiently established Symptomfaktor and at least one sufficiently established Wurzelfaktor, with Tabelle 13 conversion required before short-series results are used.
- Schicksalsanalyse defines the Triebformel as a fraction whose numerator contains Symptomfaktoren and whose denominator contains Wurzelfaktoren, and contains multi-factor formula examples.

Secondary corroboration:

- Deri describes the formula as the relationship between the most symptomatic factor(s) and the least symptomatic/root factor(s), with middle factors placed on the middle row; she explicitly notes that the number of factors assigned to the three rows has no exact universal count rule and is based on relative TspG values.

**Current executable rule:** after PR #36, unique extreme factors can produce a unique simple fraction; ties remain candidates and fail closed when a unique formula would require an unproved tie rule.

**Research question:** determine whether `k/s` and `kp/hs` are two explicitly distinct Szondian representation levels (leading/extreme pair versus broader abbreviated symptom/root structure), and derive the exact source-authorized selection rule for each.

### 2. Abbreviated Triebformel ties

**Current status:** `ACTIVE_RESEARCH`, executable behavior currently fail-closed.

Fall 16 demonstrates that more than one tied root can be printed, but another Lehrbuch example with equal minimal TspG does not automatically print every tied denominator. Therefore `emit all max/min combinations` is disproved as a universal rule.

**Required closure:** corpus-wide comparison of formula examples for evidence of an additional selector such as Leitfaktor status, root-direction constancy, Triebklasse relation, or another explicitly stated criterion.

### 3. Unterklasse sign for mixed Wurzelfaktor direction

**Current status:** `ACTIVE_RESEARCH`, executable behavior currently fail-closed.

The primary Lehrbuch defines positive/negative Unterklassen through the Wahlrichtung of the unsatisfied Wurzelfaktor. Current P1 code assigns a sign only where the observed root direction is one-sided and refuses to invent a majority threshold for mixed `+` and `-` series.

**Required closure:** search all Szondi-primary volumes for an explicit rule or examples defining how `constant`, `almost constant`, `dominant`, or mixed root directions determine the Unterklasse sign. Deri and Melon are secondary corroboration only after the Szondi sweep.

### 4. Complete Triebformel partition when the explicit TspG line rule admits multiple partitions

**Current status:** `ACTIVE_RESEARCH`, executable behavior currently fail-closed.

The engine uses the explicit same-line rule and Tabelle 13 normalization. Fall 11 and Fall 18 are uniquely reproduced. Hypothetical rankings can still admit multiple mathematically valid three-line partitions.

**Required closure:** determine whether Szondi supplies an additional selection rule elsewhere in the primary corpus. If not, close as `RESOLVED_FAIL_CLOSED` rather than inventing a general tie-break.

### 5. Quantenverrechnung

**Current status:** candidate `RESOLVED_FAIL_CLOSED / NOT EXECUTABLE FROM ADMITTED DESCRIPTION`.

Lehrbuch states that the method had not yet reached completion and omits the exact technique pending fuller publication. Unless another admitted Szondi-primary source supplies the completed method, it must not become a guessed P1 algorithm.

### 6. Inkonstanzmethode

**Current status:** `ACTIVE_RESEARCH`.

Lehrbuch refers the calculation technique to Boeszoermenyi in *Szondiana I* rather than providing the complete procedure itself.

**Required closure:** first determine whether the cited method is already contained in admitted internal material. If not, classify the exact missing evidence before considering any external search/admission.

### 7. Trieblinnaeus constancy criteria for short series

**Current status:** `ACTIVE_RESEARCH / boundary classification`.

Lehrbuch gives empirical constancy/use criteria for 3-8 profiles, including context-dependent distinctions for some profile counts. These must not be silently converted into deterministic scoring if they are reliability/validity conditions rather than computation rules.

**Required closure:** classify each statement as deterministic precondition, empirical validity statement, or later interpretive condition.

### 8. Rand-Mitte and verbal/association methods

**Current status:** candidate `RESOLVED_OUTSIDE_P1`.

These methods require qualitative/psychodynamic interpretation beyond the deterministic test engine. They should be explicitly routed to later doctrine/executable-interpretation work rather than retained as vague P1 debt.

### 9. Dur-Moll and Sozialindex interpretation

**Current status:** numeric procedures `RESOLVED_IMPLEMENTED`; interpretation candidate `RESOLVED_OUTSIDE_P1`.

P1 contains the source-defined matrices and arithmetic. Sexual, social, forensic, diagnostic, hereditary, and clinical meanings remain downstream doctrine/interpretation and must not be smuggled into the arithmetic layer.

## Corpus sweep order

For each active item, search in this order:

1. `SZ_LEHR_1972` — Lehrbuch der experimentellen Triebdiagnostik.
2. `SCHICKSALSANALYSE`.
3. `SZ_ICH_1` and `SZ_ICH_2`.
4. `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`.
5. Other admitted Szondi-primary works where the concept is used or reformulated.
6. Deri as the first secondary witness.
7. Melon as the next secondary witness.
8. External research only for a specifically identified missing source or unresolved historical publication.

## Gate rule

`P1_DETERMINISTIC_ENGINE_PASS` must not be declared while an item is merely postponed because the internal corpus has not been searched sufficiently.

The gate does **not** require pretending that every historical/clinical question has a unique algorithm. It requires every P1-relevant uncertainty to have a durable, justified status: implemented, explicitly fail-closed because the source is underdetermined, outside P1, or blocked by a named missing evidence object.
