# CH43 — Doctrinal Review

**Capitol:** 43 — `Triebformel`: formula abreviată, formula completă și limitele calculului  
**DRAFT auditat inițial:** v1, blob SHA `f90d5b6ca449a5b9d0ca8bd9769d57c11132a1dd`  
**DRAFT reverificat integral:** v2, blob SHA `9a4cdf5ceb6f22469104902c8c1c96f0334b007b`  
**Proveniență verdict:** audit doctrinar extern furnizat de utilizator după reconstrucție independentă, control vizual direct în *Lehrbuch* și recheck integral al DRAFT v2, inclusiv Fall 11, 12, 16 și 18  
**Verdict inițial extern:** **PASS WITH ONE MATERIAL FIX + ONE MATERIAL ADDITION + ONE PRECISION FIX. NU ÎNCĂ DOCTRINAL PASS.**  
**Verdict final extern:** **CAP. 43 — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED.**  
**Statut:** DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / READER PASS NEXT / CH43-AUDIT-01 CONFIRMED/CLOSED / CH43-NOTATION-01 CONFIRMED/CLOSED / CH43-ABBR-01 SOURCE/PROCEDURE HOLD ACTIVE / CH43-SHORT-01 SOURCE CONFLICT HOLD ACTIVE  

---

## Primul audit extern — DRAFT v1

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

## Recheck doctrinar extern integral — DRAFT v2

Recheck-ul extern a fost refăcut integral pe DRAFT v2, nu doar asupra celor trei intervenții. Auditorul a confirmat că nu există regresii doctrinare și a acordat verdictul final:

**CAP. 43 — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED.**

### Confirmarea celor trei intervenții

1. **Formula abreviată — PASS.** Suprageneralizarea a dispărut. DRAFT v2 păstrează definiția canonică prin `Symptomfaktoren / Wurzelfaktoren`, nu deduce mecanic formula prin maxim/maxime ↔ minim/minime și păstrează `CH43-ABBR-01` ca limită de sursă/procedură.
2. **Rangul psihodiagnostic istoric — PASS.** Rolul revendicat de Szondi pentru `Triebformel` în determinarea `Triebnatur`, `Charakter` și `Krankheitsform` este restituit, dar separat explicit de validarea clinică contemporană. Contraexemplul intern `Die experimentelle Triebdiagnose war demnach falsch.` este folosit corect ca limită internă.
3. **`Tabelle 13` — PASS.** Pentru șase profile sunt tipărite `1->2, 2->3, 3->5, 4->7, 5->8, 6->10`; `0->0` nu mai este atribuit tabelului ca celulă tipărită. Conflictul cu Fall 18 rămâne documentat fără arbitraj editorial.

### Control mecanic reconfirmat extern

- Fall 11: rang `8,5,5,4,4,2,2,1`;
- Fall 18 brut: `5,4,3,3,2,2,1,0`;
- aplicarea conversiilor tipărite pentru valorile nenule produce `8,7,5,5,3,3,2,0`;
- incompatibilitatea numerică dintre instrucțiunea generală de `Umrechnung` și formula tipărită în Fall 18 este reală.

---

## Focus-uri închise

### CH43-AUDIT-01 — CONFIRMED/CLOSED

Structura în trei niveluri a formulei complete și regula `diferență TspG <=2` sunt confirmate direct. Refuzul unui algoritm exhaustiv de clustering inventat rămâne protejat.

### CH43-NOTATION-01 — CONFIRMED/CLOSED

Fall 11 a fost controlat vizual extern semn-cu-semn, indice-cu-indice și linie-cu-linie. Redarea din DRAFT v2 este confirmată corectă.

---

## HOLD-uri active după DOCTRINAL PASS

### CH43-ABBR-01 — SOURCE/PROCEDURE HOLD ACTIVE

Nu există în materialul canonic controlat o procedură universală suficient documentată pentru selecția exactă a `Leitbuchstaben` din formula abreviată pentru orice serie. Manualul documentează limita și nu o umple prin inferență.

### CH43-SHORT-01 — SOURCE CONFLICT HOLD ACTIVE

`Tabelle 13` cere `Umrechnung` și include `Triebformel` în titlu, dar Fall 18 tipărește formula unei serii de șase profile cu valorile brute. Manualul păstrează ambele brațe ale conflictului și nu alege o ordine universală de conversie.

`CH41-SHORT-01` rămâne separat și nu este redeschis.

Aceste două HOLD-uri rămân active, dar **nu blochează capitolul**, deoarece limitele sursei sunt documentate fidel și nu sunt completate prin inferență.

---

## Stare după recheck

Gate-ul doctrinar este închis prin verdict extern explicit:

**DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED.**

Nu există încă reader/style pass și capitolul nu este încă `STABLE DRAFT`.

### Următorul pas autorizat

**CH43 — READER / STYLE PASS EXTERN.**

Cap. 44 rămâne închis până la închiderea reader/style gate-ului și stabilizarea explicită a CH43.