# CH43 — Reader / Style Review

**Capitol:** 43 — `Triebformel`: formula abreviată, formula completă și limitele calculului  
**DRAFT evaluat inițial:** v2, blob SHA `72c8701fa687c415462aa76950ab3c72695ecc12`  
**DRAFT reverificat integral:** v3, blob SHA `fc4d25e65dfba149a309cf92cb7775759c62c2bb`  
**Proveniență verdict:** reader/style pass extern furnizat de utilizator după verificarea gate-ului doctrinar, lectura integrală a DRAFT v2 și recheck stilistic integral al DRAFT v3  
**Verdict inițial extern:** **PASS WITH MODERATE REVISION — REVISION REQUIRED BEFORE STABLE.**  
**Verdict final extern:** **STYLE PASS — READY FOR STABLE DRAFT.**  
**Statut:** STYLE PASS / READER PASS CLOSED / CHAPTER STABLE  
**Doctrinal gate:** DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED  
**HOLD-uri doctrinare păstrate:** CH43-ABBR-01 SOURCE/PROCEDURE HOLD ACTIVE; CH43-SHORT-01 SOURCE CONFLICT HOLD ACTIVE  

---

## Primul reader/style pass — DRAFT v2

Reader pass-ul a considerat capitolul solid stilistic și didactic, dar a cerut o revizie moderată înainte de stabilizare. Problema principală nu era doctrina sau arhitectura, ci vizibilitatea infrastructurii de audit în vocea cărții și repetarea unor limite deja instalate.

Direcția de revizie formulată extern a fost:

> **arată cititorului exact unde sursa știe și exact unde nu știe; scoate însă codurile prin care proiectul nostru a ajuns să știe această diferență.**

## Intervenții integrate în DRAFT v3

### 1. Infrastructura de audit scoasă din vocea cărții

Au fost eliminate din corpul manuscrisului codurile administrative `CH43-ABBR-01` și `CH43-SHORT-01`, precum și formulele `SOURCE/PROCEDURE HOLD ACTIVE` / `SOURCE CONFLICT HOLD ACTIVE`.

Limitele doctrinare rămân intacte, dar sunt formulate pentru cititor:

- **Limită de procedură** pentru selecția exactă a `Leitbuchstaben` în formula abreviată;
- **Limită de sursă pentru seriile scurte** pentru conflictul `Tabelle 13 / Fall 18`.

Codurile și statutele lor rămân documentate în acest review, în review-ul doctrinar și în `CURRENT_STATE.md`.

### 2. Dublările de protecție reduse

Au fost condensate fără pierdere doctrinară:

- explicația inițială a diferenței vector-local / global, păstrând secțiunea dedicată ca loc principal al distincției;
- dubla formulare `Symptomfaktor ≠ diagnostic`;
- repetarea perechii `genus proximum / differentiae specificae` în secțiunea despre ce adaugă formula față de clasă;
- balustradele repetate în jurul rangului psihodiagnostic istoric;
- recapitularea finală a limitelor deja instalate.

### 3. Formulări naturalizate

Formula protejată despre rădăcina locală a fost naturalizată astfel:

**`Wurzelfaktor`-ul vector-local nu devine automat numitorul global al `Triebformel`.**

Secțiunea despre regula `TspG <= 2` a fost compactată la relația esențială dintre rangul global, cele trei funcții ale liniilor, regula `ΔTspG <= 2` și configurația canonică tipărită, fără algoritm universal de clustering.

### 4. Conflictul seriei scurte păstrat integral

Au rămas neschimbate în substanță:

- titlul explicit al `Tabelle 13`;
- conversiile tipărite pentru șase profile;
- faptul că `0->0` nu este o celulă tipărită;
- valorile brute din Fall 18;
- valorile rezultate prin conversia celor nenule;
- incompatibilitatea indicilor.

A fost eliminată numai propoziția de management de proiect despre redeschiderea cap. 41.

### 5. Deri/Mélon și protocolul final compactate

Deri și Mélon au fost reunite într-un singur paragraf, păstrând prioritatea `Lehrbuch` și statutul lor de tradiție/pedagogie ulterioară.

Protocolul pentru `Zehnerserie` păstrează cei opt pași, dar referințele administrative la HOLD-uri au fost înlocuite prin formularea directă a limitelor de sursă.

### 6. Limitele calculului strânse la două idei

Finalul păstrează:

- rangul psihodiagnostic/characterologic revendicat istoric de Szondi;
- limita contemporană a manualului.

Formula finală protejată rămâne:

**Calculul comprimă distribuția serială a factorilor; nu produce singur etiologie, diagnostic sau prognostic clinic.**

---

## Recheck stilistic extern integral — DRAFT v3

Recheck-ul extern a fost făcut integral pe DRAFT v3, nu doar asupra modificărilor. Auditorul stilistic a confruntat textul cu reader pass-ul precedent și cu achizițiile doctrinare protejate și nu a identificat regresii doctrinare sau motive stilistice pentru o nouă rundă obligatorie.

Verdictul final extern este:

**CH43 DRAFT v3 — STYLE PASS / READER PASS CLOSED / READY FOR STABLE DRAFT.**

Recheck-ul confirmă în particular că:

- deschiderea și axa `Triebklasse = genus proximum / Triebformel = differentiae specificae` rămân intacte;
- distincția vector-local / global este plasată și formulată corect;
- secțiunile `Symptomfaktoren` și `Wurzelfaktoren` sunt compacte fără pierderea distincțiilor doctrinare;
- formula abreviată păstrează Fall 11/12/16/18 și limita reală de procedură, fără cod administrativ în manuscris;
- formula completă păstrează cele trei niveluri, schema Fall 11 și regula `ΔTspG <= 2` fără clustering inventat;
- notația și controlul vizual rămân protejate;
- rangul psihodiagnostic istoric și contraexemplul `Die experimentelle Triebdiagnose war demnach falsch.` rămân echilibrate stilistic și doctrinar;
- aceeași clasă ≠ aceeași formulă și caracterul actual/mobil al formulei sunt păstrate;
- conflictul `Tabelle 13 / Fall 18` rămâne integral, inclusiv faptul că `0->0` nu este celulă tipărită;
- Schafir, Deri și Mélon au proporția adecvată;
- protocolul de opt pași reorganizează legitim capitolul;
- finalul păstrează contrastul dintre rangul psihodiagnostic istoric și limita contemporană, precum și frontiera către `TspQu / % Sy-Re`.

Micro-șlefuirile sugerate (`clustering` -> `grupare algoritmică`, `text layer` -> `stratul textual`, eliminarea unei propoziții de anticipare) au fost declarate explicit facultative și neblocante; nu au fost impuse ca revizie suplimentară.

---

## Achiziții protejate intacte

Stabilizarea nu modifică:

- `Triebklasse = genus proximum`; `Triebformel = differentiae specificae`;
- rangul global al celor opt `TspG`;
- `Symptomfaktoren / submanifest-sublatent / Wurzelfaktoren`;
- diferența vector-local / global;
- `nur zur raschen Orientierung`;
- exemplele Fall 11/12/16/18 pentru formula abreviată;
- lipsa unui algoritm universal pentru selecția `Leitbuchstaben`;
- structura în trei linii;
- regula `ΔTspG <= 2` fără clustering inventat;
- notația controlată vizual;
- rangul psihodiagnostic istoric și contraexemplul `Die experimentelle Triebdiagnose war demnach falsch.`;
- aceeași clasă ≠ aceeași formulă;
- caracterul actual/mobil al formulei;
- conflictul `Tabelle 13 / Fall 18` pentru seria scurtă;
- faptul că `0->0` nu este celulă tipărită;
- frontiera către `TspQu / % Sy-Re`.

`CH43-ABBR-01` și `CH43-SHORT-01` rămân HOLD-uri active în memoria operațională. Stabilizarea capitolului nu le închide și nu le rezolvă.

---

## Stare finală

**STYLE PASS / READER PASS CLOSED / CHAPTER STABLE.**

Capitolul 43 poate fi marcat `STABLE DRAFT` pe baza verdictului extern explicit. Gate-ul pentru capitolul 44 poate fi deschis.

### Următorul pas autorizat

**CH44 — RESEARCH.**
