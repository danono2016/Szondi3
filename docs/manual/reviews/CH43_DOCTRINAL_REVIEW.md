# CH43 — Doctrinal Review

**Capitol:** 43 — `Triebformel`: formula abreviată, formula completă și limitele calculului  
**DRAFT auditat:** v1, blob SHA `f90d5b6ca449a5b9d0ca8bd9769d57c11132a1dd`  
**Proveniență verdict:** audit doctrinar extern furnizat de utilizator după reconstrucție independentă și control vizual direct în *Lehrbuch*, inclusiv Fall 11, 12, 16 și 18  
**Verdict extern:** **PASS WITH ONE MATERIAL FIX + ONE MATERIAL ADDITION + ONE PRECISION FIX. NU ÎNCĂ DOCTRINAL PASS.**  
**Statut după integrare:** DRAFT v2 — RECHECK DOCTRINAR EXTERN INTEGRAL REQUIRED  
**Reader gate:** NOT OPEN  

---

## Verdictul extern integrat

Auditul a confirmat nucleul DRAFT v1, dar a identificat trei intervenții obligatorii înainte de orice `DOCTRINAL PASS`.

### 1. MATERIAL FIX — formula abreviată

DRAFT v1 prezenta prea algoritmic formula abreviată, sugerând că factorii conducători pot fi selectați universal prin extremele `TspG`.

Sursa garantează sigur numai principiul:

- numărător: `Leitbuchstaben` ale `Symptomfaktoren`;
- numitor: `Leitbuchstaben` ale `Wurzelfaktoren`;
- funcție: `nur zur raschen Orientierung`.

Exemplele controlate extern împiedică regula universală simplă „maxim/maxime ↔ minim/minime”:

- Fall 11: `m₈/s₁`;
- Fall 12: `s/h`, deși `p` și `h` sunt ambele la `TspG = 0`;
- Fall 16: `e/d` și `e/m`;
- Fall 18: `k/s` și `kp/hs`.

**Decizie integrată:** `CH43-ABBR-01 — SOURCE/PROCEDURE HOLD ACTIVE`. Manualul predă principiul funcțional și cazurile canonice, dar nu inventează un algoritm universal de selecție a formulei abreviate.

### 2. MATERIAL ADDITION — rangul psihodiagnostic istoric

DRAFT v1 proteja corect limita contemporană, dar subreprezenta rangul pe care Szondi îl revendică pentru metodă.

În `Lehrbuch`, analiza `Triebformel` este folosită pentru caracterul unei `Triebnatur` sănătoase/bolnave, raportul dintre simptom și satisfacția pulsională ratată și, împreună cu `Triebklasse` / `Trieblinnäus`, pentru determinarea `Triebnatur`, `Charakter` și `Krankheitsform`. Fall 12 arată un traseu de la formula abreviată la formula completă și apoi la diagnoză.

În același timp, auditul a indicat contraexemplul intern din `Triebpathologie II`, unde Szondi admite explicit: `Die experimentelle Triebdiagnose war demnach falsch.`

**Decizie integrată:** DRAFT v2 consemnează explicit rangul psihodiagnostic/characterologic revendicat istoric de Szondi, fără a-l transforma în validare clinică contemporană, infailibilitate sau permisiune de diagnostic mecanic din formulă.

### 3. PRECISION FIX — `Tabelle 13`

DRAFT v1 atribuia coloanei pentru șase profile conversia `0->0`.

Auditul vizual a confirmat că tabelul tipărește numai:

`1->2, 2->3, 3->5, 4->7, 5->8, 6->10`.

Rândul `0` nu este tipărit.

**Decizie integrată:** DRAFT v2 nu mai atribuie tabelului o celulă `0->0`. Dacă valoarea nulă este păstrată într-o comparație operațională, acest lucru este marcat explicit ca operație de lucru, nu ca intrare tipărită.

---

## Focus-uri închise prin verdict extern

### CH43-AUDIT-01 — CONFIRMED/CLOSED

Structura în trei niveluri a formulei complete și regula `diferență TspG <=2` sunt confirmate direct. Refuzul unui algoritm exhaustiv de clustering inventat rămâne protejat.

### CH43-NOTATION-01 — CONFIRMED/CLOSED

Fall 11 a fost controlat vizual extern semn-cu-semn, indice-cu-indice și linie-cu-linie. Redarea din DRAFT v1 a fost confirmată corectă și a fost păstrată în DRAFT v2.

---

## HOLD-uri active după integrare

### CH43-ABBR-01 — SOURCE/PROCEDURE HOLD ACTIVE

Nu există încă o procedură universală canonică autorizată pentru selecția exactă a `Leitbuchstaben` din formula abreviată pentru orice serie.

### CH43-SHORT-01 — SOURCE CONFLICT HOLD ACTIVE

`Tabelle 13` cere `Umrechnung` și include `Triebformel` în titlu, dar Fall 18 tipărește formula unei serii de șase profile cu valorile brute. Manualul nu alege între cele două brațe ale conflictului.

`CH41-SHORT-01` rămâne separat și nu este redeschis.

---

## Stare după integrare

DRAFT v2 a integrat toate cele trei intervenții materiale/precizie cerute de audit. Acest document **nu acordă `DOCTRINAL PASS`** și nu transformă integrarea corecturilor într-un verdict de închidere.

### Următorul pas autorizat

**RECHECK DOCTRINAR EXTERN INTEGRAL AL DRAFT v2, de la zero.**

Reader/style pass-ul și cap. 44 rămân închise până la un verdict extern explicit de `DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED`.
