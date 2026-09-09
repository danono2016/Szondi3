# CH42 — External doctrinal review

**Capitol:** 42 — `Triebklasse` și `Unterklasse`: `Wurzelfaktor`, `Triebgefahr` și `Ventil`  
**Verdict extern curent:** RECHECK HOLD — ONE MATERIAL OVERGENERALIZATION / NU ESTE ÎNCĂ DOCTRINAL PASS  
**Stare după integrare:** DRAFT v3 / PUNCTUAL DOCTRINAL RECHECK REQUIRED  
**Reader pass:** NOT OPEN  
**CH42-AUDIT-01:** CONFIRMED  
**CH42-AUDIT-02:** CONFIRMED  
**CH41-SHORT-01:** UPSTREAM CONSTRAINT ACTIVE

---

## Proveniența verdictelor

Primul verdict extern asupra DRAFT v1 a fost **REVIZIE DOCTRINARĂ OBLIGATORIE / NU ESTE ÎNCĂ DOCTRINAL PASS**.

După integrarea acelor corecții în DRAFT v2, auditorul a refăcut **recheck-ul doctrinar de la zero**, cu control direct al *Lehrbuch* și recalcularea exemplelor. Verdictul a fost:

**RECHECK HOLD — ONE MATERIAL OVERGENERALIZATION.**

Acest document consemnează verdictul extern; nu îl generează și nu îl transformă în `DOCTRINAL PASS`.

## Ce a trecut recheck-ul DRAFT v2

Auditorul a confirmat că au fost integrate corect:

- separarea celor două niveluri ale `Triebgefahr`;
- regula specială pentru două `Gefahren`;
- `CH42-AUDIT-02` privind maximele egale și clasele co-conducătoare;
- dinamica `Gefahr ↔ Ventil`;
- caracterul `aktuell / relativ umweltlabil` al `Triebklasse`;
- frontiera exactă `Triebklasse -> Triebformel`;
- `CH42-AUDIT-01`: pragul `5/4` strict în domeniul `Zehnerserie`;
- `CH41-SHORT-01` ca upstream constraint activ.

Controlul mecanic a fost confirmat:

- `10 : 9 : 2 : 1` -> două `Gefahren`;
- `4 : 3 : 2 : 1`, amplitudine `3` -> `Triventilklasse`;
- `4 : 3 : 3 : 2`, amplitudine `2` -> `Quadriventilklasse`.

## Unica problemă materială identificată la recheck

În algoritmul final al DRAFT v2 apărea formularea:

> dacă sunt două sau mai multe `Gefahren`, păstrează toate clasele de pericol relevante și consideră `Existenzformen` corespunzătoare drept `Schicksalsmöglichkeiten`.

Aceasta extrapola neautorizat regula documentată explicit pentru **exact două** `Triebgefahren`.

În *Lehrbuch*, regula este formulată sub titlul **`Bestimmung der Person in der Triebklasse mit zwei Gefahren`**: pentru două pericole, persoana se determină în ambele clase, iar ambele `Existenzformen` sunt tratate ca `Schicksalsmöglichkeiten`.

Controlul extern al **Fall 17**, p. tipărită 327, arată o structură cu **trei `Triebgefahren`** în care Szondi nu extinde regula „în toate clasele”; persoana este introdusă în `Gefahrklasse Cd+`, în rubrica „drei Gefahren”.

Prin urmare, regula specială pentru două pericole nu poate fi universalizată la „două sau mai multe”.

## Fix punctual integrat în DRAFT v3

Punctul 7 al algoritmului spune acum:

> dacă sunt **exact două `Gefahren`**, determină persoana în ambele clase și, în doctrina lui Szondi, consideră ambele `Existenzformen` drept `Schicksalsmöglichkeiten`; pentru structurile cu trei sau patru `Gefahren`, nu extrapola această regulă din cazul cu două — păstrează numărul pericolelor și regulile de localizare documentate de sursă.

Nu a fost făcută nicio altă modificare doctrinară în corpul capitolului.

## Achiziții doctrinare protejate

### Două niveluri ale lui `Triebgefahr`

- **nivel relativ-dinamic:** maximul / maximele `Latenzgrade` localizează cea mai puternică / amenințătoare `Triebgefahr`;
- **nivel absolut-formal al `Zehnerserie`:** `5–10 = Gefahr-/Wurzelklasse`, `0–4 = Ventil-/Symptomklasse`.

Formula protejată:

**pericol relativ-dinamic ≠ simpla apartenență formală la `Gefahrklasse`.**

### Exact două `Gefahren`

Pentru **exact două** `Triebgefahren`, persoana este determinată în ambele clase de pericol, iar ambele `Existenzformen` trebuie considerate, în doctrina lui Szondi, `Schicksalsmöglichkeiten`.

Această regulă nu se extinde editorial la structurile cu trei sau patru `Gefahren`.

### `CH42-AUDIT-02` — CONFIRMED

La maxime egale nu se inventează tie-break. Sursa oferă caz în care două maxime egale sunt păstrate amândouă pentru localizare.

Regula protejată:

**identifică maximul / maximele relative; la egalitate păstrează toate clasele co-conducătoare.**

### Dinamica `Gefahr ↔ Ventil`

Aceeași persoană poate trece, în doctrina lui Szondi, din `Gefahrklasse` în `Ventil-/Symptomklasse` și invers, în funcție de acumulare / descărcare.

Afirmația rămâne doctrină istorică Szondi, nu validare psihometrică sau genetică modernă.

### Frontiera `Triebklasse -> Triebformel`

- `Triebklasse` localizează `Wurzelfaktoren` și domeniul / domeniile de `Triebgefahr`;
- nu spune încă natura și calitatea concretă a `Notausgänge`;
- individualizarea `Symptomfaktoren` și a ventilelor aparține `Triebformel`, cap. 43.

### `CH42-AUDIT-01` — CONFIRMED

Pragul `5–10 = Gefahr / 0–4 = Ventil` rămâne predat strict în domeniul direct documentat:

**`Zehnerserie`.**

Nu se universalizează pentru orice lungime de serie.

`CH41-SHORT-01` rămâne upstream constraint activ și nu este rezolvat în cap. 42.

## Statutul gate-ului

**NU ESTE ÎNCĂ DOCTRINAL PASS.**

Unica suprageneralizare identificată de recheck-ul DRAFT v2 a fost corectată în DRAFT v3.

Următorul pas autorizat este exclusiv:

**recheck doctrinar punctual al propoziției / punctului 7 din algoritmul CH42 DRAFT v3.**

Dacă auditorul extern confirmă fixul fără altă modificare, numai verdictul său explicit poate acorda `DOCTRINAL PASS` și închide auditul științific.

Reader pass-ul stilistic rămâne închis până atunci.
