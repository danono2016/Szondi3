# CH39 — Doctrinal review

**Capitol:** 39 — Constanță, schimbare și fază în serie  
**Status:** PASS WITH ONE MATERIAL FIX — FIX INTEGRATED / FINAL SCIENTIFIC RECHECK REQUIRED / SOURCE HOLD ACTIVE

## Verdict extern — prima trecere

**SCIENTIFIC HOLD — MAJOR REVISION REQUIRED. Nu DOCTRINAL PASS.**

Auditorul a precizat că gravitatea este epistemică, nu arhitecturală: structura capitolului poate rămâne, dar este necesară o revizie materială țintită.

## Corecțiile materiale din prima trecere — integrate și confirmate la recheck

### 1. Interpolarea fazelor lipsă

DRAFT v1 și research-ul intern formulaseră regula opusă sursei primare. În `Lehrbuch`, după descrierea succesiunii `Quantumspannung -> Ambivalenz -> Entladung`, Szondi spune explicit:

`Wir müssen aber auf Grund der Empirie die fehlenden Phasen interpolieren.`

**Corecție integrată și confirmată:** Szondi admite și cere interpolarea fazelor lipsă în interiorul modelului său; manualul separă însă strict **faza observată** de **faza interpolată conform modelului Szondi**. Interpolarea nu se introduce în protocol ca observație.

### 2. Exemplul Böszörményi/Janssen

DRAFT v1 clasifica eronat `(+1,−1)` drept `±`.

**Corecție integrată și confirmată:** în clasificatorul istoric Böszörményi/Janssen, `1/1 = 0`. Exemplul:

`(+4,−0) -> (+1,−1)`

este:

`+ -> 0`, clasa `t`, `Q=4`, `M=1,5`, `I=6`.

Rezultatul numeric rămâne 6; categoria tranziției a fost corectată.

### 3. Clasificatorul metodei versus scoringul matur Szondi

A fost introdusă bariera explicită:

> **Clasificatorul Böszörményi pentru `Inkonstanzmethode` ≠ clasificarea factorială matură Szondi din `Tabelle 3`.**

Regulile locale metodei nu sunt generalizate la interpretarea factorială matură Szondi.

### 4. Pretențiile diagnostice istorice

Au fost restabilite pretențiile istorice privind `Präpsychose/Psychose`, natura simptomelor manifeste, tipul tulburării și aplicațiile de grup, urmate de limita contemporană: acestea nu devin criterii diagnostice validate.

### 5. Rangul pluriprofil al fazei

A fost integrat materialul din `Triebpathologie II`, inclusiv secvențe istorice pluriprofil, fără transformarea lor într-o taxonomie universală.

### 6. Proveniența tehnicii Böszörményi

A fost ridicată la standard bibliografic explicit:

**H. J. M. N. Janssen, *De diagnostische waarde van de Szondi-test*, disertație, Nijmegen, 1955, secțiunea III.D, pp. 53–57.**

Se declară separat că articolul primar al lui Böszörményi din *Szondiana I* (1953, pp. 199–210) nu a fost controlat direct și că `Lehrbuch` nu reproduce algoritmul complet.

Nucleul recuperat sigur este tranziție-cu-tranziție. Agregarea originală completă la nivelul întregii serii, rangului factorial și grupului nu este considerată integral recuperată.

## Verdict extern — al doilea recheck

Auditorul a refăcut controlul direct în sursele relevante și a reconstruit toate cele **28 de distribuții posibile** `(+,−)`, comparând clasificarea matură Szondi cu clasificatorul istoric Böszörményi/Janssen.

Verdict:

**PASS WITH ONE MATERIAL FIX. Nu încă DOCTRINAL PASS.**

Cele șase probleme majore din DRAFT v1 sunt confirmate ca reparate. Ultima corecție materială privește caracterul operațional și exhaustiv al clasificatorului Böszörményi/Janssen.

## Ultima corecție materială — clasificatorul exhaustiv

A fost introdus explicit, cu statut de **reconstrucție istorică secundară din Janssen**, nu de tabel primar verificat în articolul Böszörményi, algoritmul:

- `0` dacă `P ≤ 1` și `N ≤ 1`;
- `±` dacă `P = N ≥ 2`;
- `+` dacă `P > N` și `P ≥ 2`;
- `−` dacă `N > P` și `N ≥ 2`.

Acest algoritm partitionează exhaustiv toate cele 28 de distribuții posibile.

### Distribuția claselor

Böszörményi/Janssen reconstruit:

- `0`: 4;
- `+`: 11;
- `−`: 11;
- `±`: 2.

Szondi matur:

- `0`: 4;
- `+`: 9;
- `−`: 9;
- `±`: 6.

### Cele patru diferențe exacte

| Distribuție | Szondi matur | Böszörményi/Janssen reconstruit |
|---|---|---|
| `3/2` | `±` | `+` |
| `4/2` | `±` | `+` |
| `2/3` | `±` | `−` |
| `2/4` | `±` | `−` |

Această corecție face clasificatorul utilizabil fără ambiguitate pentru alegerea multiplicatorului și protejează scoringul matur Szondi de contaminare retroactivă.

### Matricea tranzițiilor după corecție

- aceeași clasă: `i` dacă `Q=0`, altfel `qu`;
- `+ ↔ −`: `c`;
- `+` sau `−` ↔ `±` ori `0`: `t`;
- `± ↔ 0`: **HOLD**.

## HOLD protejat

**HOLD CH39-BOSZ-01 — `± ↔ 0` temporal** rămâne activ.

Multiplicatorul nu este confirmat. Nu se deduce prin simetrie, nu se importă din Deri/Mélon și nu se confundă cu complementarea `± -> 0 / 0 -> ±` din cap. 37.

După explicitarea clasificatorului exhaustiv, `± ↔ 0` rămâne singura muchie categorială a matricei recuperate fără multiplicator confirmat.

## Fișiere revizuite

- `research/CH39_RESEARCH.md` — al doilea recheck și clasificatorul exhaustiv integrate;
- `research/CH39_OUTLINE.md` — clasificatorul exhaustiv integrat fără schimbarea arhitecturii;
- `chapters/39_Constanta_schimbare_si_faza_in_serie_DRAFT.md` — DRAFT v3;
- `reviews/CH39_DOCTRINAL_PASS.md` — prezentul status.

## Următorul gate

**FINAL SCIENTIFIC RECHECK REQUIRED.**

Auditorul a anunțat controlul final pe text și pe matricea completă `28 distribuții × clase de tranziție`, cu HOLD-ul `± ↔ 0` izolat.

Nu se acordă DOCTRINAL PASS înainte de verdictul explicit al acestui recheck final.

Reader pass-ul stilistic și cap. 40 rămân închise.