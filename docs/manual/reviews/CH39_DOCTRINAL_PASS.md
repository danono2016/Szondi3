# CH39 — Doctrinal review

**Capitol:** 39 — Constanță, schimbare și fază în serie  
**Status:** PASS WITH ONE MATERIAL ADDITION + ONE TECHNICAL SOURCE-CORRECTION — INTEGRATED / FINAL SCIENTIFIC RECHECK REQUIRED / SOURCE HOLD ACTIVE

## Verdict extern — prima trecere

**SCIENTIFIC HOLD — MAJOR REVISION REQUIRED. Nu DOCTRINAL PASS.**

Auditorul a precizat că gravitatea este epistemică, nu arhitecturală: structura capitolului poate rămâne, dar este necesară o revizie materială țintită.

## Corecțiile materiale din prima trecere — integrate și confirmate ulterior

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

## Verdict extern — al doilea recheck

Auditorul a refăcut controlul direct în sursele relevante și a reconstruit toate cele **28 de distribuții posibile** `(+,−)`, comparând clasificarea matură Szondi cu clasificatorul istoric Böszörményi/Janssen.

Verdict:

**PASS WITH ONE MATERIAL FIX. Nu încă DOCTRINAL PASS.**

Ultima corecție materială a fost explicitarea exhaustivă a clasificatorului Böszörményi/Janssen:

- `0` dacă `P ≤ 1` și `N ≤ 1`;
- `±` dacă `P = N ≥ 2`;
- `+` dacă `P > N` și `P ≥ 2`;
- `−` dacă `N > P` și `N ≥ 2`.

Reconstrucția partitionează cele 28 de distribuții `0=4`, `+=11`, `−=11`, `±=2`; scoringul matur Szondi le partitionează `0=4`, `+=9`, `−=9`, `±=6`. Diferențele exacte sunt `3/2`, `4/2`, `2/3`, `2/4`.

## Verdict extern — recovery v4 / al treilea recheck

Auditorul a refăcut recovery-ul de la zero pe Janssen, cu control direct pe **p. 6 și pp. 53–57**, a verificat toate cele **28 de distribuții** și toate cele **784 de tranziții**, apoi a recitit DRAFT v3.

Verdictul recovery-ului:

**RECOVERY v4 — MECHANICAL PASS / SOURCE PASS, cu un singur HOLD real: `± ↔ 0`.**

Distribuția mecanică a celor 784 tranziții:

- `i = 28`;
- `qu = 234`;
- `t = 264`;
- `c = 242`;
- `HOLD = 16`.

Toate cele 16 HOLD-uri sunt și numai `± ↔ 0`.

Verdictul pentru capitol:

**CAP. 39 DRAFT v3 — PASS WITH ONE MATERIAL ADDITION + ONE TECHNICAL SOURCE-CORRECTION. Nu încă DOCTRINAL PASS.**

## Corecția tehnică de sursă — `i`

Janssen tipărește ponderile:

- `qu = 1`;
- `t = 1,5`;
- `c = 2`.

El **nu tipărește un multiplicator `M_i=0`**. `i-Reaktionen` sunt reacții neschimbate, iar contribuția lor este zero deoarece `Q=0`.

**Corecție integrată în DRAFT v4, research și outline:** tabelul nu mai prezintă `0` drept „multiplicator recuperat” pentru `i`. Formula este acum `—; contribuție 0 deoarece Q=0`, cu precizarea că `M_i=0`, dacă este folosit într-o implementare, este numai convenție de implementare.

## Adăugarea materială — contraproba empirică Janssen

Recovery v4 a identificat o omisiune materială: Janssen nu folosește `Inkonstanzmethode` doar pentru descrierea tehnicii, ci și pentru a critica interpretarea dinamică a variabilității.

Pe **80 de subiecți**, Janssen raportează:

- repetare imediată: **14,5**;
- repetare după o zi: **16,3**;
- diferență: aproximativ **12%**.

Pe p. 57, Janssen concluzionează că diferențele dintre profilele aceluiași szondigram nu trebuie considerate pur și simplu efectul unor procese psihologice profunde și îl critică direct pe Deri în acest punct.

**Integrare obligatorie realizată:** DRAFT v4 are o secțiune proprie pentru această contraproba. Este etichetată explicit ca **poziție empirică a lui Janssen**, nu ca teză Böszörményi sau Szondi. Nu anulează doctrina Szondi a fazelor, dar limitează dreptul de a lua variabilitatea măsurată drept dovadă automată a unei dinamici psihice profunde.

Formula de control introdusă:

> **Măsurarea variabilității nu dovedește prin ea însăși cauza sau profunzimea psihologică a variabilității.**

## HOLD protejat

**HOLD CH39-BOSZ-01 — `± ↔ 0` temporal** rămâne activ.

Recovery v4 confirmă că acesta este singurul HOLD real al matricei tehnice reconstruite. Ponderea nu se deduce prin simetrie, nu se importă din Deri/Mélon și nu se confundă cu complementarea `± -> 0 / 0 -> ±` din cap. 37.

## Fișiere revizuite

- `research/CH39_RESEARCH.md` — recovery v4, corecția `i` și contraproba Janssen integrate;
- `research/CH39_OUTLINE.md` — cele două intervenții integrate fără schimbarea arhitecturii;
- `chapters/39_Constanta_schimbare_si_faza_in_serie_DRAFT.md` — DRAFT v4;
- `reviews/CH39_DOCTRINAL_PASS.md` — prezentul status;
- `CURRENT_STATE.md` — sincronizat cu verdictul curent.

## Următorul gate

**FINAL SCIENTIFIC RECHECK REQUIRED.**

Nu se acordă DOCTRINAL PASS înainte de verdictul explicit al recheck-ului final asupra DRAFT v4. Reader pass-ul stilistic și cap. 40 rămân închise.