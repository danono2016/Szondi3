# SZONDI3 — CHAT QUALIFICATION REPORT TEMPLATE

**Use with:** `CHAT_SUCCESSION_PROTOCOL.md` and `CHAT_QUALIFICATION_RUBRIC.md`  
**Mode:** READ ONLY until explicit authorization

A new chat should copy this structure into its takeover assessment and complete every field.

---

# 1. Candidate declaration

- Candidate conversation identifier (if available):
- Qualification date:
- Repository checked:
- Repository branch/commit checked:
- READ ONLY respected: `YES / NO`
- Any repository writes performed during qualification: `NONE / describe`

---

# 2. Mechanical state witnesses

Record concrete witnesses rather than vague statements.

| Item | Evidence |
|---|---|
| Current `main` commit | |
| Current relevant PR state | |
| Relevant CI/workflow run(s) | |
| Foundation verifier status | |
| Active project phase | |
| Lowest unfinished gate | |
| Next safe action | |
| Transfer/checkpoint staleness detected? | |

---

# 3. Takeover assessment

Answer in your own words.

## Q1. Fundamental purpose and reason for restart

[answer]

## Q2. Epistemic authority hierarchy

[answer]

## Q3. What Szondi2 may/may not contribute

[answer]

## Q4. Doctrine preservation vs executable interpretation

[answer]

## Q5. Demonstrated vs unproved at current gate

[answer]

## Q6. Next safe step and why later phases must wait

[answer]

## Q7. Major failure modes the foundation protects against

[answer]

## Q8. Conflict-resolution rule across source/spec/code/CI/Szondi2

[answer]

---

# 4. Earthquake tests

## Test A — doctrinal earthquake

[answer]

## Test B — predecessor shortcut temptation

[answer]

## Test C — one additional shortcut/failure mode you identified yourself

[answer]

## Test D — recovery from your additional failure mode without old chat memory

[answer]

---

# 5. Epistemic status table

List important claims from your own assessment and classify them.

| Claim | Status (`VERIFIED / PROVISIONAL / INFERENCE / UNKNOWN`) | Evidence or reason |
|---|---|---|
| | | |
| | | |
| | | |

At least one `UNKNOWN` or explicit statement that no material unknown was found must be justified. Do not manufacture uncertainty merely to satisfy the template.

---

# 6. Self-red-team

Now assume your own takeover assessment is dangerously overconfident. Try to disqualify yourself.

## Objection 1

- Strongest objection:
- Evidence that defeats it, or unresolved status:

## Objection 2

- Strongest objection:
- Evidence that defeats it, or unresolved status:

## Objection 3

- Strongest objection:
- Evidence that defeats it, or unresolved status:

## Immediate revocation trigger

State one specific newly discovered fact that would make you revoke your readiness immediately:

[answer]

---

# 7. Rubric self-assessment

## A. Mechanical evidence checks

Report as `PASS/FAIL` for all 12 items in `CHAT_QUALIFICATION_RUBRIC.md`.

`A1 ... A12`

Score: `__/12`

## B. Epistemic invariants

Report as `PASS/FAIL` for all 10 invariants.

`B1 ... B10`

Score: `__/10`

## C. Earthquake tests

`C1 ... C4`

Score: `__/4`

## D. Self-red-team

`D1 ... D3`

Score: `__/3`

## Hard failures detected

- Count:
- Items:

## Blocking unresolved issues

- Count:
- Items:

---

# 8. Deterministic outcome

Apply the rubric literally.

- `QUALIFIED` only if A=12/12, B=10/10, C=4/4, D=3/3, hard failures=0, blocking unresolved issues=0.
- `CONDITIONAL` only under the narrow conditions defined in the rubric.
- `REJECTED` if any hard failure or constitutional misunderstanding exists.
- `UNVERIFIABLE` if evidence/tool access prevents honest qualification.

**Qualification outcome:** `QUALIFIED / CONDITIONAL / REJECTED / UNVERIFIABLE`

If `CONDITIONAL`, list only the required human decision items:

- Human decision item 1:
- Human decision item 2:

---

# 9. Candidate readiness verdict

End with exactly one:

`READY TO CONTINUE`

or

`NOT READY TO CONTINUE`

A `QUALIFIED` candidate normally uses `READY TO CONTINUE`. A `REJECTED` or `UNVERIFIABLE` candidate must use `NOT READY TO CONTINUE`. A `CONDITIONAL` candidate should normally use `NOT READY TO CONTINUE` until the listed condition is resolved.

Even after `READY TO CONTINUE`, stop. Do not modify the repository until explicitly authorized.
