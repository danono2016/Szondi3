# Manualul Szondi — Starea curentă

**Ramură:** `manual`  
**Statut general:** PRE-WRITING / GOVERNANCE SETUP  
**Ultima etapă închisă:** audit structural global al arhitecturii  
**Arhitectură curentă:** 11 părți, 63 de capitole + anexe candidat  

## Ce este stabil acum

- Corpusul canonic 10/10 este definit.
- Auditul structural al arhitecturii inițiale a fost încheiat.
- Cele patru scindări necesare au fost consolidate.
- `BOOK_ARCHITECTURE.md` este arhitectura de bază de lucru.
- `GLOBAL_COVERAGE_AUDIT.md` confirmă că nu există în prezent un gol major care să ceară alt capitol autonom.
- Nu există încă niciun capitol redactat care să fie considerat model de continuitate.

## Ce NU este încă făcut

- Nu a început cercetarea 10/10 dedicată capitolului 1.
- Nu există draft de capitol.
- Nu există capitol FINAL.
- Nu sunt înghețate definitiv toate anexele.
- Problemele formale/cazurile-limită enumerate în audit rămân de verificat în cercetarea capitolelor relevante.

## Documente de guvernanță

Acest director trebuie să conțină și să respecte:

- `BOOK_ARCHITECTURE.md`
- `GLOBAL_COVERAGE_AUDIT.md`
- `WRITER_CONTRACT.md`
- `CHAPTER_COMPLETION_GATE.md`
- `READER_EXPERIENCE_STANDARD.md`
- `CURRENT_STATE.md`

Auditurile locale rămân în `docs/manual/audits/` ca istoric de decizie și material de control.

## Următorul pas autorizat

După fixarea documentelor de guvernanță, următorul pas este:

**Capitolul 1 — cercetare 10/10, matrice de relevanță, note conceptuale și control de independență înainte de orice draft.**

Nu se începe proza capitolului 1 înainte ca cercetarea lui să fie suficientă pentru a construi o arhitectură proprie a capitolului.

## Regula de stare

- primul text complet al unui capitol este întotdeauna `DRAFT`;
- un capitol rămâne `DRAFT` dacă există îndoieli doctrinare, formale, vizuale, de independență sau de experiență a cititorului;
- `FINAL` este permis numai după trecerea integrală a `CHAPTER_COMPLETION_GATE.md`.