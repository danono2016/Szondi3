# Manualul Szondi — Starea curentă

**Ramură:** `manual`  
**Statut general:** PART I — STABLE DRAFT / PART II CHAPTERS 5–9 — STABLE DRAFT / PART III CHAPTERS 10–14 — STABLE DRAFT / PART IV CHAPTERS 15–26 — STABLE DRAFT / PART V CHAPTERS 27–31 — STABLE DRAFT / PART VI CHAPTERS 32–37 — STABLE DRAFT / PART VII CHAPTERS 38–43 — STABLE DRAFT / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE / CH43-ABBR-01 SOURCE/PROCEDURE HOLD ACTIVE / CH43-SHORT-01 SOURCE CONFLICT HOLD ACTIVE / CHAPTER 44 — OUTLINE COMPLETE / DRAFT NEXT / CH44-AUDIT-01 ACTIVE / CH44-AUDIT-02 ACTIVE / CH44-ROUND-01 SOURCE/PROCEDURE HOLD ACTIVE  
**Arhitectură:** 11 părți, 63 de capitole + anexe candidat

## Bootstrap

1. `CURRENT_STATE.md`
2. `MANUAL_FOUNDATION.md`
3. `BOOK_ARCHITECTURE.md`
4. numai documentele active indicate mai jos.

Repository-ul este memoria operațională.

---

## Ce este stabil

- Corpusul canonic: 8 volume Szondi + Deri + Mélon.
- Arhitectura este fixată în `BOOK_ARCHITECTURE.md`.
- Partea I, cap. 1–4 — `STABLE DRAFT`.
- Partea II, cap. 5–9 — `STABLE DRAFT`.
- Partea III, cap. 10–14 — `STABLE DRAFT`.
- Partea IV, cap. 15–26 — `STABLE DRAFT`.
- Partea V, cap. 27–31 — `STABLE DRAFT`.
- Partea VI, cap. 32–37 — `STABLE DRAFT`.
- Cap. 1–34 au trecut auditul canonic transversal A–G; raportul este `reviews/TRANSVERSAL_CANONICAL_AUDIT_01_34.md`.
- Cap. 35 este închis doctrinar și stilistic după audit, reverificare și reader pass.
- Cap. 36 este închis doctrinar după trei treceri științifice externe, inclusiv control final semn-cu-semn, și închis stilistic după reader pass conservator.
- Cap. 37 este închis doctrinar după trei treceri științifice externe, inclusiv control final semn-cu-semn și statut-cu-stat, și închis stilistic după reader pass conservator.
- Cap. 38 este închis doctrinar după patru treceri științifice externe și închis stilistic după reader pass conservator `PASS WITH LIGHT REVISION`.
- Cap. 39 este închis doctrinar după auditul științific final și închis stilistic după reader pass `PASS WITH MODERATE REVISION`, integrat conservator cu prioritate doctrinară.
- Cap. 40 este închis doctrinar după audit și trei recheck-uri succesive, inclusiv verificarea numerică celulă cu celulă a `Tabelle 13`, și închis stilistic după reader pass `PASS WITH LIGHT REVISION` integrat conservator.
- Cap. 41 este închis doctrinar după audit și recheck extern al DRAFT v2 și închis stilistic după `PASS WITH MODERATE REVISION`, integrarea DRAFT v3 și recheck-ul extern final `STYLE PASS — READY FOR STABLE DRAFT`; `CH41-SHORT-01` rămâne SOURCE CONFLICT HOLD activ ca limită documentată a sursei.
- Cap. 42 este închis doctrinar prin verdict extern `DOCTRINAL PASS — SCIENTIFIC AUDIT CLOSED` și închis stilistic după `PASS WITH MODERATE REVISION`, integrarea DRAFT v4 și recheck-ul extern final `STYLE PASS — READY FOR STABLE DRAFT`; `CH41-SHORT-01` rămâne upstream constraint activ și nu este rezolvat prin stabilizarea cap. 42.
- Cap. 43 este închis doctrinar prin recheck-ul extern integral al DRAFT v2: **DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED**. Reader pass-ul extern pe DRAFT v2 a dat **PASS WITH MODERATE REVISION — REVISION REQUIRED BEFORE STABLE**; revizia a fost integrată în DRAFT v3, iar recheck-ul stilistic extern final a acordat **STYLE PASS — READY FOR STABLE DRAFT**. Capitolul este stabil. `CH43-AUDIT-01` și `CH43-NOTATION-01` sunt CONFIRMED/CLOSED; `CH43-ABBR-01` și `CH43-SHORT-01` rămân HOLD-uri active ca limite documentate ale sursei și nu sunt rezolvate prin stabilizare.
- `LEXICON.md`, `ANTI_INFERENCE_MAP.md` și `CONCEPT_RECURRENCE_MAP.md` sunt instrumente vii, nu gate-uri.

Cap. 1–43 nu se redeschid fără o problemă concretă nouă. `CH41-SHORT-01`, `CH43-ABBR-01` și `CH43-SHORT-01` rămân HOLD-uri documentate și nu constituie, prin ele însele, motiv de redeschidere a capitolelor stabile.

---

# Reguli active după auditul transversal canonic 1–34

## Doctrină

- **doctrina se verifică înainte de stil**;
- verificăm atât corectitudinea afirmațiilor existente, cât și completitudinea doctrinară relevantă;
- Szondi are prioritate; Deri/Mélon sunt tradiție ulterioară explicit atribuită;
- factor, reacție factorială, `Vektorbild`, mecanism, funcție a Eului, sindrom experimental și diagnostic clinic rămân niveluri distincte;
- profilul/seria precizează sensul testologic; relevanța clinică cere anamneză, observație și date clinice;
- `0`, `±` și încărcările nu se reduc la dicționare;
- cronologia doctrinară se spune când conceptele se dezvoltă;
- la capitolele de sinteză/transversale verificăm explicit tezele primare omise;
- cei patru vectori S/P/Sch/C sunt arhitectura formală fixă a testului, dar nu sunt reificați ca unități biologice originare: la Szondi `Trieb` este deja `Verschränkung` / sinteză de trebuințe, iar teoria mai largă admite și alte `Bedürfnisverschränkungen` în dezvoltare/patologie.

> **Nu simplificăm Szondi reducând numărul distincțiilor lui. Îl facem accesibil făcând distincțiile lui mai clare.**

## Stil

Direcția este **română firească, atmosferă szondiană**.

- clarificăm fără să domesticim; traducem fără să contemporaneizăm doctrina;
- termenii pregnanți și germana rămân vizibile când poartă diferențe reale;
- reducem ticurile metapedagogice și anti-inferențele preventive;
- metaforele proprii nu devin pseudo-concepte;
- recapitularea rămâne numai dacă reorganizează sensul.

Ordinea de lucru:

> **1. întâi Szondi; 2. apoi claritate; 3. apoi eleganță.**

## Flux de feedback dublu

Pentru fiecare capitol nou:

1. feedback științific/doctrinar;
2. feedback stilistic/reader pass.

Un capitol nu devine `STABLE DRAFT` până când ambele sunt închise. **În orice conflict, auditul doctrinar prevalează asupra auditului stilistic.**

### Regulă operațională de sincronizare a statutului

După închiderea oricărui gate extern, **înainte de orice handoff către alt chat/auditor**, se sincronizează obligatoriu în aceeași etapă:

1. `CURRENT_STATE.md`;
2. frontmatter-ul capitolului activ;
3. review-ul activ al acelui gate.

Niciun document activ nu trebuie să păstreze `RECHECK REQUIRED`, `AUDIT NEXT` sau alt statut vechi după ce gate-ul a fost închis. `CURRENT_STATE.md` are prioritate operațională, dar cele trei locuri trebuie să fie coerente între ele.

---

## HOLD-uri active

- `genotrop / genotropisch / genotropistisch` — anomalie tipărită târzie;
- sensurile tehnice ale `Schicksalsmöglichkeit` când devin active;
- diferențierile fine `Ich-Schicksal / Wahlschicksal / Freiheitsschicksal` pentru părțile dedicate Eului și terapiei;
- `Strebung -> năzuință` rămâne soluție lexicală de lucru;
- **CH39-BOSZ-01 — `± ↔ 0` temporal în `Inkonstanzmethode`**: ponderea nu este confirmată în materialul controlat; recovery v4 confirmă că este singurul HOLD real al matricei tehnice reconstruite; nu se completează prin simetrie, Deri sau Mélon și nu se confundă cu complementarea cap. 37;
- **CH41-SHORT-01 — ordinea conversiei pentru seriile 3–9**: `Lehrbuch` cere `Umrechnung` în instrucțiunile Schafir–Szondi, dar Fall 18 calculează `Latenzgrade` pentru șase profile direct din `TspG` brute. Nici `TspG brut -> Tabelle 13 -> TspD`, nici `TspD brut -> Tabelle 13` nu este autorizat ca regulă canonică universală până la o rezolvare primară explicită;
- **CH43-ABBR-01 — formula abreviată / selecția exactă a `Leitbuchstaben`**: sursa definește funcțional numărătorul prin `Symptomfaktoren` și numitorul prin `Wurzelfaktoren`, dar Fall 11/12/16/18 nu autorizează o regulă universală simplă „maxim/maxime -> sus; minim/minime -> jos”. Manualul nu inventează algoritmul lipsă;
- **CH43-SHORT-01 — `Triebformel` în seriile 3–9**: `Tabelle 13` este intitulată explicit `Zur Umrechnung der Zahlen der Latenzproportion und der Triebformel` și instrucțiunea generală cere `Umrechnung`, dar Fall 18 construiește formula unei serii de șase profile cu indicii TspG bruți `5,4,3,3,2,2,1,0`. Manualul nu alege o ordine universală de conversie pentru formula seriei scurte.
- **CH44-ROUND-01 — precizia numerică și rotunjirea:** corpusul controlat nu declară o regulă universală de rotunjire sau un număr fix de zecimale; exemplele canonice se reproduc ca tipărite, iar orice convenție nouă de afișare rămâne explicit editorială.

Distincția veche `0` liber / nul forțat nu mai este HOLD: controlul vizual canonic din cap. 37 confirmă **`Ø = Zwangsnullreaktion`** în EKP; `Ø` nu se interpretează și rămâne distinct de `0` liber. În EKP, un `0` liber are rang specific și poate primi în doctrina lui Szondi sens de `Entladungsbereitschaft` a tendinței din fundal.

---

# Partea a V-a — STABLE DRAFT

Cap. 27–31 sunt închise științific și stilistic; auditul transversal 1–34 nu a identificat contradicții reziduale în această parte.

---

# Partea a VI-a — STABLE DRAFT

## Capitolul 32 — STABLE DRAFT

**Titlu:** Regula de bază: niciun semn nu se citește singur

Research, auditul științific, auditul transversal și reader pass-ul stilistic sunt închise. Cap. 32 nu se redeschide fără o problemă concretă nouă.

## Capitolul 33 — STABLE DRAFT

**Titlu:** Lectura reacției factoriale: sens, încărcare și context

Research 10/10 + bounded deep corpus pass, auditul științific, auditul transversal și reader pass-ul stilistic sunt închise.

### Achiziții doctrinare protejate

- `Quantität` și `Tendenzrichtung` sunt coordonate distincte;
- `Leer-/Nullreaktion`, `Durchschnittsreaktion`, `Vollreaktion` rămân clase cantitative;
- `Tendenzspannung` și `Quantumspannung` sunt distincte și pot coexista;
- `0` indică mai întâi absența actuală a trebuinței din prim-plan, nu absența ei din persoană;
- `Quantumspannung` / `!` nu înseamnă severitate clinică;
- schema `Quantumspannung -> Ambivalenz -> Entladung / Nullreaktion` cere seria pentru observare;
- factorul partener este pragul către lectura vectorială.

Cap. 33 nu se redeschide fără o problemă concretă nouă.

## Capitolul 34 — STABLE DRAFT

**Titlu:** Metoda lecturii vectoriale: de la două reacții la `Vektorbild`

Research 10/10 + bounded deep corpus pass, SCIENTIFIC PASS prin auditul transversal canonic și reader pass-ul stilistic sunt închise.

Documente de control:

- `research/CH34_RESEARCH.md` — RESEARCH COMPLETE / corpus pass 10/10 + bounded deep corpus pass;
- `research/CH34_OUTLINE.md` — OUTLINE COMPLETE;
- `chapters/34_Metoda_lecturii_vectoriale_de_la_doua_reactii_la_Vektorbild_DRAFT.md` — STABLE DRAFT;
- `reviews/CH34_DOCTRINAL_PASS.md` — SCIENTIFIC PASS / AUDIT CLOSED;
- `reviews/CH34_READER_PASS.md` — STYLISTIC PASS / INTEGRATED;
- `reviews/TRANSVERSAL_CANONICAL_AUDIT_01_34.md` — external/transversal scientific PASS pentru baza 1–34.

### Achiziții doctrinare protejate

- `Vektorbild` este imaginea vizibilă a unui `Trieb` în profil, alcătuită din reacțiile celor doi factori constitutivi;
- fiecare vector are 16 variații formale;
- pentru numărarea tendințelor din prim-plan: `+ / − = 1`, `± = 2`, `0 = 0`;
- `!` modifică `Quantumspannung`, nu clasa structurală `Nulli-/Uni-/Bi-/Tri-/Quadritendenz`;
- `±` factorial nu este sinonim cu `Bitendenz` vectorială;
- `Bitendenz` vectorială cuprinde `++`, `−−`, `±0`, `0±`, `+−`, `−+`;
- formele bitendenței sunt: orizontală `Legierung`, verticală `Isolierung`, diagonală `Spaltung / Zerspaltung`;
- la `Tritendenz`, tendința a patra absentă din prim-plan poate avea rang interpretativ decisiv;
- `±±` este canonic `Integration/Reintegration`, fără echivalare cu sănătatea;
- `00` este `Nullitendenz / Desintegration` a întregului pulsional din prim-plan, fără diagnostic clinic global;
- aceeași geometrie structurală are conținut diferit în S, P, Sch și C;
- `Vektorbild ≠ profil ≠ diagnostic`.

### Decizia editorială

Reader pass-ul a fost integrat conservator după SCIENTIFIC PASS. Au fost reduse balustradele, anticiparea `Triebgefahr` și câteva formule editoriale, fără modificarea geometriei canonice sau a limitelor epistemice.

**Control de interferență:** nu a fost identificat niciun conflict material între auditul stilistic și cel doctrinar. La condensarea `±± / 00` a fost păstrată explicit forma doctrinară mai precisă, astfel încât stilul să nu slăbească statutul `Nullitendenz / Desintegration`.

Cap. 34 nu se redeschide fără o problemă concretă nouă.

## Capitolul 35 — STABLE DRAFT

**Titlu:** Relațiile dintre vectori: arhitectura profilului

Research 10/10 + bounded deep corpus pass, DOCTRINAL PASS după audit și reverificare și reader pass-ul stilistic sunt închise.

Documente de control:

- `research/CH35_RESEARCH.md` — RESEARCH COMPLETE / corpus pass 10/10 + bounded deep corpus pass; evaluarea preliminară privind relevanța *Therapie II* este suprascrisă de auditul extern direct în corpus;
- `research/CH35_OUTLINE.md` — OUTLINE COMPLETE;
- `chapters/35_Relatiile_dintre_vectori_arhitectura_profilului_DRAFT.md` — STABLE DRAFT;
- `reviews/CH35_DOCTRINAL_PASS.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / RECHECK CLOSED;
- `reviews/CH35_READER_PASS.md` — STYLISTIC PASS / INTEGRATED.

### Achiziții doctrinare protejate

- `Mosaikspiel` este explicit respins de Szondi ca metodă de interpretare;
- `korrelative Deutung` este regula centrală a trecerii de la `Vektorbild` la profil;
- corelarea operează atât `interfaktoriell`, cât și `intervektoriell`;
- S/P/Sch/C delimitează domenii distincte, dar formează în lectura profilului o `unzertrennliche Ganzheit`;
- sensul general/abstract al unui factor sau `Vektorbild` nu este identic cu sensul testologic individualizat în profil;
- corelația profilului nu epuizează forma concretă: `Erscheinungskreise / Erscheinungsebenen` și funcție ≠ conținut rămân distincte;
- reciprocitatea S↔Sch/P/C rămâne; niciun vector, inclusiv Sch, nu rezumă singur profilul;
- corelațiile relevante pot traversa vectorii la nivel factorial; exemple primare: h↔p și s↔k;
- `Konkordanzregel` S↔Sch este exemplu primar de relație între două `Vektorbilder` întregi și nu autorizează cauzalitate S→Sch sau Sch→S;
- exemplele de corelație nu formează un catalog exhaustiv și nu autorizează o matrice universală a celor șase perechi vectoriale;
- confirmare / limitare / contradicție este schemă pedagogică a manualului, nu taxonomie tehnică Szondi;
- fiecare profil trebuie interpretat `in seiner Ganzheit`, dar un profil singular reprezintă numai o `Schicksalsmöglichkeit`;
- formula de control este `întregimea profilului ≠ totalitatea persoanei`;
- `Vektorbild ≠ profil ≠ diagnostic` rămâne intact.

### Decizia editorială

Reader pass-ul a redus metadiscursul, metaforele redundante și recapitulările administrative, fără a modifica vreo achiziție doctrinară. Au rămas explicit, deși adaugă densitate, `Erscheinungsebenen`, funcție ≠ conținut, statutul pedagogic al triadei și lipsa cauzalizării în `Konkordanzregel`.

**Control de interferență doctrină–stil:** PASS. Auditul doctrinar a prevalat integral.

Cap. 35 nu se redeschide fără o problemă concretă nouă.

## Capitolul 36 — STABLE DRAFT

**Titlu:** Rand și Mitte: `Triebgefahr` la margine și apărarea din centru

Research 10/10 + bounded deep corpus pass, trei treceri științifice externe și reader pass-ul stilistic sunt închise.

Documente de control:

- `research/CH36_RESEARCH.md` — RESEARCH COMPLETE / corpus pass 10/10 + bounded deep corpus pass; evaluarea internă privind relevanța *Ich-Analyse II* este superseded de auditul extern direct în corpus în privința rangului `Abwehrort`;
- `research/CH36_OUTLINE.md` — OUTLINE COMPLETE / EXTERNAL AUDIT QUALIFICATIONS INTEGRATED;
- `chapters/36_Rand_si_Mitte_Triebgefahr_la_margine_si_apararea_din_centru_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / STYLISTIC PASS INTEGRATED;
- `reviews/CH36_DOCTRINAL_PASS.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / RECHECK CLOSED;
- `reviews/CH36_READER_PASS.md` — STYLISTIC PASS / INTEGRATED / CHAPTER STABLE.

### Întrebarea cognitivă

Cum organizează metoda `Rand / Mitte` un profil deja citit corelativ, astfel încât `Triebgefahr`, apărarea și centrul să nu fie confundate cu simpla topografie, cu o metodă cantitativă sau cu diagnosticul clinic?

### Achiziții doctrinare protejate

- `Rand = S + C`; `Mitte = P + Sch`;
- denumirea are sens topografic și funcțional, iar funcția are rang interpretativ mai mare;
- metoda este `qualitativ / dialektisch` și urmărește `Wie`, nu `Wieviel`;
- apariția `Quantumspannung` nu schimbă rangul metodologic al `Rand / Mitte`;
- `Triebgefahr` este categorie doctrinar-testologică, nu sinonim pentru risc clinic contemporan;
- cele șapte forme sunt: `Unitendenz`, `Tritendenz` prin căderea unei tendințe vitale, `Isolierung`, `Spaltung / Zerspaltung`, `Desintegration`, `Integration` excesivă și `Quantumspannung / Triebüberdruck`;
- în analiza `Triebgefahr`, `Integration` poate figura ca pericol prin tensiunea completă și excesivă a contrariilor; aceasta nu înseamnă `Integration = patologie` și nu contrazice cap. 31/34;
- `Mitte` este `Zensursystem / stellungnehmendes System` în cadrul metodei, dar nu este sinonim cu Sch și nici cu Eul conștient;
- factorii centrului sunt e/hy/k/p, iar direcțiile socialpozitive de cenzură sunt exact `+e / −hy / −k / +p`;
- schema istorică `sozialnegative Mitte` = `−e +hy +k −p`;
- aceste etichete sunt parte din vocabularul evaluativ istoric al lui Szondi, nu verdict moral contemporan;
- și Mitte poate purta `Affektgefahr` în P și `Ichgefahr` în Sch; centrul nu este apărare sănătoasă automată;
- teoria generală a apărării nu limitează `Abwehrort` la Mitte; toate cele patru domenii pulsionale pot fi folosite defensiv de Eu;
- variațiile / tabelele Mitte sunt exemple, nu legi diagnostice;
- **Mitte nu se interpretează autonom** și nu se folosește diagnostic fără analiza Rand;
- un profil singular semnalează pericole și apărări actuale / episodice; seria este necesară pentru stabilitate temporală;
- `Rand / Mitte` organizează `korrelative Deutung`, nu o înlocuiește;
- `Vektorbild / Triebgefahr / profil / diagnostic` rămân niveluri distincte.

### Decizia editorială

Reader pass-ul a fost integrat exclusiv prin compresie, aerisire și reducerea dublărilor. Au fost păstrate integral toate distincțiile validate științific, inclusiv pasajele dense despre `Wie/Wieviel`, semnele cenzurilor, `Abwehrort`, `Mitte` fără Rand și limita clinică.

**Control de interferență doctrină–stil:** PASS. Auditul doctrinar a prevalat integral.

Cap. 36 nu se redeschide fără o problemă concretă nouă.

## Capitolul 37 — STABLE DRAFT

**Titlu:** Vordergänger și Hintergänger: complementul teoretic, complementul experimental și dialectica Eului

Research 10/10 + bounded deep corpus pass + control vizual canonic al notației, trei treceri științifice externe și reader pass-ul stilistic sunt închise.

Documente de control:

- `research/CH37_RESEARCH.md` — RESEARCH COMPLETE / corpus pass 10/10 + bounded deep corpus pass + canonical visual notation check; auditul extern direct în sursele primare prevalează asupra oricărei omisiuni de rang din research;
- `research/CH37_OUTLINE.md` — OUTLINE COMPLETE / SECOND EXTERNAL RECHECK QUALIFICATIONS INTEGRATED;
- `chapters/37_Vorderganger_si_Hinterganger_complementul_teoretic_complementul_experimental_si_dialectica_Eului_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / STYLISTIC PASS INTEGRATED;
- `reviews/CH37_DOCTRINAL_PASS.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED;
- `reviews/CH37_READER_PASS.md` — STYLISTIC PASS / INTEGRATED / CHAPTER STABLE.

### Întrebarea cognitivă

Cum trecem de la profilul din prim-plan la ceea ce Szondi numește `Hintergänger`, fără să confundăm un complement construit teoretic, o a doua alegere experimentală și ideea unei „personalități adevărate” ascunse?

### Teza validată

`Komplementmethode` adaugă profilului o a doua axă dialectică. VGP este prim-planul experimental; ThKP este complementul teoretic construit față de `Ganzprofil` și este identificat doctrinar de Szondi cu `wirklicher Hintergänger`; EKP este complementul experimental obținut prin `Nachwahl`, poate fi numit `experimenteller Hintergänger`, dar în metoda complementară se citește în primul rând prin `Konkordanzanalyse`, nu ca profil autonom de același rang. În Sch, polaritatea complementară apare ca `Vorder-Ich / Hinter-Ich`. Forma matură a metodei se desfășoară serial pe 8–10 VGP cu profilele complementare corespunzătoare; cap. 37 fixează mecanica și rangul, iar dinamica seriei rămâne pentru cap. 38–39.

### Achiziții doctrinare protejate

- `Komplementmethode` este metodă `qualitativ / dialektisch`, în continuitate cu cap. 36;
- forma matură este serială, cu 8–10 VGP și profile complementare corespunzătoare; demonstrația pe un moment nu este protocolul complet;
- VGP / ThKP / EKP au statute epistemice diferite;
- VGP este prim-plan testologic, nu conștientul și nu o mască falsă;
- `Vordergrund` nu este sinonim cu `Bewusstsein`; `Hintergrund` nu este sinonim cu inconștientul ca întreg; ambele aparțin în mare parte dialecticii inconștiente;
- ThKP este construcție formală, nu a doua măsurare;
- regula direcțională VGP → ThKP este `+ -> −`, `− -> +`, `± -> 0`, `0 -> ±`;
- tabelul direcțional nu șterge automat `Quantumspannung` în complementarea concretă;
- `0 -> ±` păstrează două posibilități doctrinare: `Bitendenz im Hintergrund` / `Reintegration nach der vordergründigen Befriedigung`;
- `±` ThKP nu este o a doua alegere ambivalentă; `0` ThKP are rang formal specific complementului;
- `VGP + ThKP -> Ganzprofil` este operație formală; `ThKP = wirklicher Hintergänger` este teza doctrinară a lui Szondi;
- VGP și ThKP sunt concepute ca simultan active (`Wirkungssimultaneität`) și trebuie citite sinoptic;
- `Ganzprofil` testologic ≠ totalitatea persoanei;
- `Vorder-/Hintergänger` ≠ `Vorder-/Hinter-Ich`;
- Vorder-/Hinter-Ich sunt polaritatea complementară în Sch; complementaritate ≠ integrare / Pontifex;
- EKP este obținut empiric prin `Nachwahl`, dar nu este ThKP și nu este al treilea profil autonom de același rang în `Komplementmethode`;
- EKP poate fi numit `experimenteller Hintergänger`, distinct de `wirklicher Hintergänger` pentru ThKP;
- EKP se evaluează prin `Konkordanzanalyse`: concordanță cu VGP, concordanță cu ThKP sau `Neuorientierung`;
- înainte de interpretarea EKP se verifică `Wahlzwang`;
- **`0 ≠ Ø`**; canonic, `Ø = Zwangsnullreaktion`, iar `Ø` nu se interpretează;
- un `0` EKP liber poate primi în doctrina lui Szondi sens de `Entladungsbereitschaft` a tendinței din fundal;
- unele `Quantumspannungen` EKP pot fi numeric constrânse și nu se citesc automat ca încărcările VGP;
- Hintergänger nu este sine adevărat fix și nu este sinonim cu Jung `Schatten`;
- `Hintergrund` nu este automat mecanismul specific de `Verdrängung`;
- afirmațiile prognostice tari despre mobilizarea Hintergänger-ului rămân doctrina istorică a lui Szondi, nu predicție clinică modernă validată.

### Decizia editorială

Reader pass-ul a redus stratul protector după instalarea distincțiilor tehnice: metadiscurs, repetiții despre „persoana ascunsă”, balustradele din jurul EKP și trimiterile administrative au fost comprimate. Au fost păstrate integral toate diferențele validate științific, inclusiv `0/Ø`, `0 -> ±`, `Wirkungssimultaneität`, VGP/ThKP/EKP, `Wahlzwang`, `Konkordanzanalyse` și limita prognostică.

**Control de interferență doctrină–stil:** PASS. Auditul doctrinar a prevalat integral.

Cap. 37 nu se redeschide fără o problemă concretă nouă. Partea VI este închisă ca bloc stabil.

---

# Partea a VII-a — activă

## Capitolul 38 — STABLE DRAFT

**Titlu:** De la profil la serie: de ce un singur profil nu este suficient

Research 10/10 + bounded deep corpus pass, patru treceri științifice externe și reader pass-ul stilistic sunt închise.

Documente de control:

- `research/CH38_RESEARCH.md` — RESEARCH COMPLETE / THIRD EXTERNAL CHECK INTEGRATED;
- `research/CH38_OUTLINE.md` — OUTLINE COMPLETE / THIRD EXTERNAL CHECK INTEGRATED;
- `chapters/38_De_la_profil_la_serie_de_ce_un_singur_profil_nu_este_suficient_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / STYLISTIC PASS INTEGRATED;
- `reviews/CH38_DOCTRINAL_PASS.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / RECHECK CLOSED;
- `reviews/CH38_READER_PASS.md` — STYLISTIC PASS / INTEGRATED / CHAPTER STABLE.

### Întrebarea cognitivă

De ce cere Szondi o serie de profile dacă fiecare profil trebuie deja interpretat în întregimea lui?

### Teza validată

Un profil singular face vizibilă o `Schicksalsmöglichkeit` și trebuie citit separat `in seiner Ganzheit`; seria leagă mai multe profile prin timp și introduce `Nacheinander`. Ea nu caută un „profil adevărat” care să anuleze profilele anterioare, ci permite să observăm recurența, succesiunea și posibilitatea transformării.

### Achiziții doctrinare protejate

- un profil singular este o `Schicksalsmöglichkeit`, nu totalitatea persoanei și nici o versiune defectă a seriei;
- fiecare profil din serie se interpretează separat, `in seiner Ganzheit`;
- `in seiner Ganzheit` ≠ exhaustivitate;
- formularea generală verificată este `acht bis zehn Triebprofile`;
- pentru `Trieblinnäus`, cerința inițială este `minimal 8–10 Triebprofilaufnahmen`;
- 8–10 nu este prag universal pentru toate operațiile seriale;
- `Trieblinnäus`: scara de constanță este **3–8**; la opt profile apare `Konstanz des gesamten Trieblinnäus`;
- **9 nu este prag nou de constanță**;
- `Tabelle 13` convertește separat seriile de **3–9** profile la baza de zece;
- **10** este baza de referință / normalizare;
- profilul singular are rang actual / episodic; seria permite observarea formelor recurente / preferate;
- seria introduce `Nacheinander` și face vizibile `Wandlungsmöglichkeiten und -richtungen` în doctrina lui Szondi;
- variabilitatea dintre profile nu este automat eroare în sistemul lui Szondi, fără ca aceasta să devină validare psihometrică modernă;
- seria nu este media profilelor și nu funcționează prin majoritate;
- o apariție rară poate rămâne interpretativ relevantă în practica canonică, fără atribuirea unei maxime primare neidentificate;
- schema orizontal / vertical este explicația manualului, nu taxonomie Szondi;
- tipologia constanței, schimbării și fazei rămâne pentru cap. 39;
- pragurile și operațiile seriei scurte / `Tabelle 13` rămân pentru cap. 40;
- calculele TspG/TspD/Latenzproportionen și celelalte mărimi rămân pentru cap. 41–45;
- Deri și Mélon sunt tradiție ulterioară explicit atribuită și nu sunt fuzionați într-un protocol primar Szondi.

### Decizia editorială

Reader pass-ul extern a dat **PASS WITH LIGHT REVISION**. Revizia a fost integrată conservator: a redus dublările despre profil singular versus serie, a făcut mai exactă formularea despre repetarea examinării, a scurtat metadiscursul, a comprimat secțiunile despre media profilelor și tradiția ulterioară și a reorganizat vizual secțiunea numerică. Nicio cifră, formulă germană, frontieră de capitol sau distincție doctrinară validată nu a fost modificată.

**Control de interferență doctrină–stil:** PASS. Secțiunea numerică păstrează integral rangurile `8–10 / 3–8 / 9 / 3–9 / 10`.

Cap. 38 nu se redeschide fără o problemă concretă nouă.

## Capitolul 39 — STABLE DRAFT

**Titlu:** Constanță, schimbare și fază în serie

Research 10/10 + bounded deep corpus pass + dosarul tehnic Böszörményi/Janssen, auditul științific extern și reader pass-ul stilistic sunt închise.

Verdict științific final:

**CAP. 39 — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED.**

Verdict stilistic extern:

**PASS WITH MODERATE REVISION — INTEGRATED.**

Documente de control:

- `research/CH39_RESEARCH.md` — RESEARCH COMPLETE / HOLD ACTIVE;
- `research/CH39_OUTLINE.md` — OUTLINE COMPLETE;
- `chapters/39_Constanta_schimbare_si_faza_in_serie_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / STYLISTIC PASS INTEGRATED / SOURCE HOLD ACTIVE;
- `reviews/CH39_DOCTRINAL_PASS.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / SOURCE HOLD ACTIVE;
- `reviews/CH39_READER_PASS.md` — STYLISTIC PASS / INTEGRATED / CHAPTER STABLE / SOURCE HOLD ACTIVE.

### Achiziții doctrinare protejate

- Szondi cere interpolarea fazelor lipsă în modelul `Quantumspannung -> Ambivalenz -> Entladung`; faza observată și faza interpolată rămân epistemic distincte;
- `Ich-Analyse II` și `Triebpathologie II` susțin rangul configurațional/pluriprofil al fazei;
- `Clasificatorul Böszörményi/Janssen ≠ clasificarea factorială matură Szondi din Tabelle 3`;
- proveniența tehnică este explicită: Janssen 1955, p. 6 și III.D, pp. 53–57; articolul primar Böszörményi 1953 nu este declarat controlat direct;
- Janssen descrie operația brută, dar simbolul `Q` este notația manualului;
- nucleul recuperat sigur este **pairwise**: diferența dintre două profile; formula nu este demonstrată ca limitată la profile succesive;
- pentru lectura temporală, manualul privilegiază perechile adiacente: din `N` profile rezultă `N−1`; la 10 profile există 9 perechi adiacente și 45 de perechi distincte posibile;
- clasificatorul reconstruit pentru distribuția `P/N` este: `0` dacă `P≤1,N≤1`; `±` dacă `P=N≥2`; `+` dacă `P>N,P≥2`; `−` dacă `N>P,N≥2`;
- reconstrucția Böszörményi/Janssen partitionează cele 28 de distribuții `0=4`, `+=11`, `−=11`, `±=2`; scoringul matur Szondi le partitionează `0=4`, `+=9`, `−=9`, `±=6`;
- diferențele exacte sunt `3/2`, `4/2`, `2/3`, `2/4`, ambivalente la Szondi matur și direcționate în clasificatorul Böszörményi/Janssen;
- recovery-ul mecanic al celor 784 de perechi ordonate dă `i=28`, `qu=234`, `t=264`, `c=242`, `HOLD=16`; toate HOLD-urile sunt `±↔0`;
- Janssen tipărește ponderile `qu=1`, `t=1,5`, `c=2`, dar nu un `M_i=0`; la `i`, contribuția este zero deoarece `Q=0`; `M_i=0` este cel mult convenție de implementare;
- exemplul Janssen `4/0 -> 1/1` este `+ -> 0`, clasa `t`, scor `6`;
- pretențiile psihodiagnostice istorice tari ale `Inkonstanzmethode` sunt redate, dar nu devin criterii contemporane validate;
- eșantionul contraprobei Janssen este precizat: 80 elevi-infirmieri, 40 femei/40 bărbați, aprox. 18–30 ani, în formare într-o instituție psihiatrică; Janssen însuși nu îl considera reprezentativ pentru populația normală;
- contraproba Janssen rămâne `14,5` la repetare imediată versus `16,3` după o zi, aproximativ 12%; Janssen o folosește pentru a critica interpretarea simplă a variabilității drept efect al unor procese psihologice profunde;
- contraproba este poziția lui Janssen, nu a lui Szondi/Böszörményi, și nu anulează automat doctrina fazelor;
- vocabularul `constanță locală`, `constanță configurațională`, `recurență`, `alternanță`, `microfază`, `macrofază` este etichetat ca organizare a manualului.

### HOLD protejat

**CH39-BOSZ-01 — `± ↔ 0` temporal** rămâne nerezolvat și este singurul HOLD real al matricei tehnice reconstruite. Formula se predă până la frontiera sursei; ponderea nu este dedusă, importată sau cosmetizată. HOLD-ul este o limită documentată a sursei și nu împiedică DOCTRINAL PASS-ul sau stabilitatea editorială a capitolului.

### Decizia editorială

Reader pass-ul `PASS WITH MODERATE REVISION` a fost integrat prin compresia repetițiilor, reducerea metadiscursului și aerisirea părții tehnice. Nu au fost tăiate formulele, clasificatorul, controlul mecanic, proveniența, distincția `observat ≠ interpolat`, diferența pairwise/adiacență sau HOLD-ul.

**Control de interferență doctrină–stil:** PASS. Nu a existat conflict material care să oblige respingerea reader pass-ului. În punctele unde economia stilistică putea slăbi o frontieră epistemică — fază observată/interpolată, proveniența tehnicii, pairwise/adiacență și HOLD `± ↔ 0` — auditul doctrinar a prevalat și formulările de protecție au fost păstrate explicit.

Cap. 39 nu se redeschide fără o problemă concretă nouă.

## Capitolul 40 — STABLE DRAFT

**Titlu:** Seria scurtă și `Tabelle 13`: normalizarea la baza de zece

Research 10/10 + bounded deep corpus pass, control vizual canonic al `Tabelle 13`, auditul doctrinar și reader pass-ul stilistic sunt închise.

Verdict științific final:

**CAP. 40 — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED.**

Verdict stilistic extern:

**PASS WITH LIGHT REVISION — INTEGRATED.**

Documente de control:

- `research/CH40_RESEARCH.md` — RESEARCH COMPLETE / corpus pass 10/10 + bounded deep corpus pass + canonical visual table check;
- `research/CH40_OUTLINE.md` — OUTLINE COMPLETE;
- `chapters/40_Seria_scurta_si_Tabelle_13_normalizarea_la_baza_de_zece_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / STYLISTIC PASS INTEGRATED;
- `reviews/CH40_DOCTRINAL_PASS.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / READER PASS CLOSED / CHAPTER STABLE;
- `reviews/CH40_READER_PASS.md` — STYLISTIC PASS / PASS WITH LIGHT REVISION — INTEGRATED / CHAPTER STABLE.

### Achiziții doctrinare protejate

- Schafir: 120 Zehnerserien; Szondi precizează `Die Arbeit ist derzeit noch nicht publiziert.`;
- indicațiile pentru practicianul fără `Zehnerserie` completă, inclusiv scara 3–8, sunt formulate de Schafir și reproduse/prezentate de Szondi;
- la 3 profile, condițiile de repetare sunt formulate de Schafir și reproduse de Szondi;
- la 4 profile, continuitatea `ununterbrochen` aparține indicațiilor lui Schafir reproduse de Szondi;
- la 5 profile: `Wurzelfaktoren` + prima clasă constante, cu diferențiere bolnavi/normali pentru `Symptomfaktoren` și formula abreviată;
- la 6 profile: cele patru criterii indicate sunt constante;
- la 7 profile: a doua `Triebklasse` + `Äqualität`; pragul minim de șapte profile pentru toate criteriile `Trieblinnäus`-ului este concluzia lui Schafir reprodusă de Szondi;
- la 8 profile: `Konstanz des gesamten Trieblinnäus`;
- 9 nu este prag nou de constanță;
- 10 este `Zehnerserie` / baza de referință;
- `Tabelle 13` convertește seriile 3–9 și operează pe mărimi agregate bazate pe numărări, nu pe profile;
- `normalizare la 10 ≠ zece observații`;
- `normalizare ≠ completarea profilelor lipsă`;
- `normalizare ≠ interpolare de fază`;
- `Tabelle 13` nu reconstruiește `Nacheinander`;
- tabelul tipărit este regula operațională; nu inventăm o convenție generală de rotunjire;
- în reproducerea manualului, `—` marchează editorial celulele lăsate goale în original pentru combinațiile imposibile;
- titlul canonic leagă `Tabelle 13` de `Latenzproportion` și `Triebformel`; regula nu este generalizată automat la orice indice;
- Deri și Mélon rămân tradiție ulterioară și nu suprascriu mecanica primară Schafir/Szondi;
- TspG/TspD/Latenzproportionen rămân pentru cap. 41.

### Decizia editorială

Reader pass-ul `PASS WITH LIGHT REVISION` a fost integrat prin compresia repetițiilor, reducerea metadiscursului și scurtarea anti-inferențelor după exemple. Au fost păstrate integral proveniența Schafir/Szondi, scara 3–8, toate valorile `Tabelle 13`, `angenommene Zehnerserie`, convenția editorială `—`, limita de rotunjire și frontierele epistemice validate.

**Control de interferență doctrină–stil:** PASS. Auditul doctrinar a prevalat integral; nicio condensare nu a modificat o atribuire, o valoare numerică sau domeniul operației.

Cap. 40 nu se redeschide fără o problemă concretă nouă.

## Capitolul 41 — STABLE DRAFT / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE

**Titlu:** `TspG`, `TspD` și `Latenzproportionen`: de la factor la tensiunea vectorială

Research 10/10 + bounded deep corpus pass, control vizual canonic direct al formulelor și exemplelor primare, auditul doctrinar extern, reader pass-ul extern cu revizie moderată și recheck-ul stilistic extern final sunt închise. Verdictul final stilistic este **STYLE PASS — READY FOR STABLE DRAFT**. `CH41-SHORT-01` rămâne activ ca limită documentată a sursei și nu este un defect al manuscrisului.

Documente de control:

- `research/CH41_RESEARCH.md` — RESEARCH COMPLETE / corpus pass 10/10 + bounded deep corpus pass + canonical visual formula check; evaluarea privind seria scurtă este superseded de conflictul canonic identificat la audit;
- `research/CH41_OUTLINE.md` — OUTLINE COMPLETE; secvența propusă pentru seria scurtă este superseded de SOURCE CONFLICT HOLD;
- `chapters/41_TspG_TspD_si_Latenzproportionen_de_la_factor_la_tensiunea_vectoriala_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE;
- `reviews/CH41_DOCTRINAL_PASS.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CHAPTER STABLE / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE;
- `reviews/CH41_READER_PASS.md` — STYLE PASS / READER PASS CLOSED / CHAPTER STABLE / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE.

### Achiziții doctrinare și stilistice protejate

- `TspG = Σ(0 + ±)` pentru fiecare factor de-a lungul seriei;
- `TspG ≠ Quantumspannung`; `!` nu intră în această sumă;
- `Tages-TspG` este eticheta canonică pentru suma orizontală pe profil; `faktorieller TspG` este agregatul vertical pe factor și baza pentru `TspD`;
- în `Triebpathologie II`, `TspG` este `Maßstab für die Entladungsbereitschaft eines Bedürfnisses`;
- interpretarea reacției `±` ca `Vorphase der Entladung` este calificată explicit prin `abgesehen von den Zwangsneurotikern`; formula `TspG = Σ0 + Σ±` rămâne neschimbată;
- valoarea brută `TspG` depinde de lungimea seriei; într-o serie mai lungă de zece poate depăși 10;
- `TspD = TspG mai mare − TspG mai mic` în interiorul aceluiași vector;
- în `Triebpathologie II`, `TspD` exprimă diferența gradelor de `Entladungsbereitschaft` dintre cei doi factori și măsoară cantitativ tensiunea / `Triebgefahr` intravectorială în doctrina lui Szondi;
- indexul vectorului este factorul cu `TspG` mai mic, nu factorul cu valoarea mai mare;
- există patru `TspD`, câte unul pentru S, P, Sch și C;
- `TspD` este intravectorial, nu temporal și nu se confundă cu `Inkonstanzmethode`;
- `TspD = 0` nu identifică un singur `Vektorbild`; aceeași valoare poate proveni din configurații calitativ diferite;
- formula **`Calculul nu șterge geometria vectorului`** rămâne protejată;
- sursele folosesc `Latenzgrad` / `Latenzgröße` pentru mărimea diferenței localizate în vector; terminologia nu este rigidizată artificial;
- `Latenzproportionen` exprimă relația/ordinea celor patru grade de latență; egalitățile rămân egalități și nu inventăm tie-break;
- `Triebklasse/Unterklasse` rămân cap. 42; `Triebformel` cap. 43; `TspQu` cap. 44;
- **CH41-SHORT-01 — SOURCE CONFLICT HOLD ACTIVE:** instrucțiunile Schafir–Szondi cer `Umrechnung` pentru seria scurtă, dar Fall 18 calculează, într-o serie de șase profile, `S=1, P=0, Sch=1, C=0` direct din `TspG` brute `h=1, s=0, e=2, hy=2, k=5, p=4, d=3, m=3`. Aplicarea prealabilă a `Tabelle 13` ar da `S=2, P=0, Sch=1, C=0`, iar conversia directă a `TspD` brute ar da `S=2, Sch=2`. Manualul nu alege un algoritm în locul sursei;
- **`Ambiguitatea documentată este preferabilă certitudinii inventate.`**

Formula de control:

**calculul ordonează o serie; nu transformă seria într-un diagnostic.**

## Capitolul 42 — STABLE DRAFT / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CH42-AUDIT-01 CLOSED / CH42-AUDIT-02 CLOSED / CH41-SHORT-01 UPSTREAM CONSTRAINT ACTIVE

**Titlu:** `Triebklasse` și `Unterklasse`: `Wurzelfaktor`, `Triebgefahr` și `Ventil`

Auditul doctrinar extern este închis prin **DOCTRINAL PASS — SCIENTIFIC AUDIT CLOSED**. Reader pass-ul extern asupra DRAFT v3 a dat **PASS WITH MODERATE REVISION — REVISION REQUIRED BEFORE STABLE**; revizia a fost integrată în DRAFT v4, apoi recheck-ul stilistic extern a acordat **STYLE PASS — READY FOR STABLE DRAFT**. Capitolul este stabil. `CH41-SHORT-01` rămâne upstream constraint activ și nu este rezolvat prin această stabilizare.

Documente de control:

- `research/CH42_RESEARCH.md` — RESEARCH COMPLETE / OUTLINE COMPLETE / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED;
- `research/CH42_OUTLINE.md` — OUTLINE COMPLETE / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED;
- `chapters/42_Triebklasse_si_Unterklasse_Wurzelfaktor_Triebgefahr_si_Ventil_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED;
- `reviews/CH42_DOCTRINAL_REVIEW.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CHAPTER STABLE;
- `reviews/CH42_READER_PASS.md` — STYLE PASS / READER PASS CLOSED / CHAPTER STABLE.

### Achiziții doctrinare și stilistice protejate

- cele 8 `Haupttriebklassen` și cele 16 `Unterklassen` rămân intacte;
- factorul din numele clasei este factorul cu `TspG` mai mic, tratat doctrinar de Szondi ca `Wurzelfaktor`;
- semnul `+ / −` al `Wurzelfaktor`-ului produce `Unterklasse`; nu este semnul lui `TspD`, al vectorului întreg sau evaluare morală;
- **nivel relativ-dinamic:** maximul/maximele `Latenzgrade` localizează cea mai puternică / amenințătoare `Triebgefahr`;
- **nivel absolut-formal al `Zehnerserie`:** `5–10 -> Gefahr-/Wurzelklasse`, `0–4 -> Ventil-/Symptomklasse`;
- **pericol relativ-dinamic ≠ simpla apartenență formală la `Gefahrklasse`**;
- `Ventil` înseamnă `Notausgang` / canal de descărcare și poate fi simptomatic; nu este sinonim cu sănătate, resursă sau coping;
- pot exista una, două, trei sau patru `Gefahren`; numărul lor se păstrează;
- pentru **exact două `Gefahren`**, persoana este determinată în ambele clase, iar ambele `Existenzformen` sunt `Schicksalsmöglichkeiten` în doctrina lui Szondi;
- pentru trei sau patru `Gefahren`, regula specială pentru două nu se extrapolează; Fall 17, p. 327, oferă contraproba prin localizarea unui caz cu trei pericole în `Gefahrklasse Cd+`, rubrica „drei Gefahren”;
- `Triventilklasse` corespunde unei amplitudini max–min de `3–4`, iar `Quadriventilklasse` unei amplitudini `<3`; `Biventilklasse` nu mai este evidențiată separat în simplificarea târzie;
- vechile denumiri de clasă `inäqual / bi-/tri-/quadriäqual` ale primei ediții sunt declarate `hinfällig`; `Äqualität` rămâne proprietate descriptivă reală;
- la maxime egale se păstrează toate clasele co-conducătoare; nu se inventează tie-break;
- Deri 144 variante aparține stratului vechi; Mélon rămâne confirmare ulterioară, nu arbitru;
- `Triebklasse` este `aktuell`, mobilă și `relativ umweltlabil`;
- doctrina Szondi admite dinamica `Gefahr ↔ Ventil` prin acumulare/descărcare;
- toate cele patru `Latenzgrade` rămân relevante;
- `Triebklasse` localizează `Wurzelfaktoren` și `Triebgefahr`, dar nu spune încă natura/calitatea concretă a `Notausgänge`;
- individualizarea `Symptomfaktoren` și ventilelor aparține `Triebformel`, cap. 43;
- `Triebklasse ≠ diagnostic ≠ tip fix de personalitate`.

### Audit status

- **CH42-AUDIT-01 — CONFIRMED / CLOSED:** pragul `5–10 = Gefahr / 0–4 = Ventil` este predat strict în domeniul direct documentat al `Zehnerserie`; nu se universalizează la orice lungime de serie;
- **CH42-AUDIT-02 — CONFIRMED / CLOSED:** la maxime egale se păstrează toate maximele și toate clasele co-conducătoare; nu se inventează tie-break;
- **CH41-SHORT-01 — UPSTREAM CONSTRAINT ACTIVE:** pentru seriile 3–9, cap. 42 nu autorizează un algoritm universal de clasă/pericol/ventil cât timp ordinea conversiei valorii de intrare rămâne canonic ambiguă.

### Reader/style status

- verdict extern pe DRAFT v3: **PASS WITH MODERATE REVISION — REVISION REQUIRED BEFORE STABLE**;
- revizia a fost integrată în DRAFT v4;
- recheck extern final pe DRAFT v4: **STYLE PASS — READY FOR STABLE DRAFT**;
- **READER PASS CLOSED / CHAPTER STABLE**.

Formula de control:

**clasa organizează formal latențele unei serii; nu stabilește singură un diagnostic și nu fixează persoana într-un tip imuabil.**

## Capitolul 43 — STABLE DRAFT / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CH43-AUDIT-01 CONFIRMED/CLOSED / CH43-NOTATION-01 CONFIRMED/CLOSED / CH43-ABBR-01 SOURCE/PROCEDURE HOLD ACTIVE / CH43-SHORT-01 SOURCE CONFLICT HOLD ACTIVE

**Titlu:** `Triebformel`: formula abreviată, formula completă și limitele calculului

Research-ul 10/10, bounded deep corpus pass, controlul vizual canonic și outline-ul sunt închise. DRAFT v2 a primit verdictul doctrinar extern final **CAP. 43 — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED**. Reader pass-ul extern pe DRAFT v2 a dat **PASS WITH MODERATE REVISION — REVISION REQUIRED BEFORE STABLE**; revizia a fost integrată în DRAFT v3, iar recheck-ul stilistic extern final a acordat **STYLE PASS — READY FOR STABLE DRAFT**. Capitolul este stabil.

Documente de control:

- `research/CH43_RESEARCH.md` — RESEARCH COMPLETE / OUTLINE COMPLETE / DRAFT v2 CREATED;
- `research/CH43_OUTLINE.md` — OUTLINE COMPLETE / DRAFT v2 CREATED;
- `chapters/43_Triebformel_formula_abreviata_formula_completa_si_limitele_calculului_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED;
- `reviews/CH43_DOCTRINAL_REVIEW.md` — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / CH43-ABBR-01 + CH43-SHORT-01 ACTIVE;
- `reviews/CH43_READER_PASS.md` — STYLE PASS / READER PASS CLOSED / CHAPTER STABLE / CH43-ABBR-01 + CH43-SHORT-01 ACTIVE.

### Achiziții doctrinare și stilistice protejate

- `Triebformel` se construiește din rangul celor opt `TspG` factoriale;
- `Symptomfaktoren` se află la polul reacțiilor `0 / ±` și al `TspG` ridicat; `Wurzelfaktoren` la polul reacțiilor persistente `+ / −` și al `TspG` scăzut;
- `−` nu este automat numai `Verdrängung`; `Verzicht` și `Anpassung` rămân posibile, iar `+` poate de asemenea exprima un necesar nesatisfăcut în doctrina lui Szondi;
- `Wurzelfaktor` vector-local din cap. 42 nu este automat denominatorul global al `Triebformel`; formula ordonează global cei opt factori;
- formula abreviată este `Bruchformel` `nur zur raschen Orientierung`; numărătorul poartă `Leitbuchstaben` ale `Symptomfaktoren`, numitorul pe cele ale `Wurzelfaktoren`;
- **CH43-ABBR-01 — SOURCE/PROCEDURE HOLD ACTIVE:** Fall 11/12/16/18 nu autorizează o regulă universală simplă de selecție numai din extremele `TspG`; manualul nu inventează algoritmul lipsă;
- formula completă este `mehrfache Bruchformel` cu trei niveluri: simptomatic / submanifest-sublatent / rădăcină;
- regula textuală primară spune că factorii de pe aceeași linie au diferența TspG nu mai mare de 2, fără clustering matematic universal inventat;
- **CH43-AUDIT-01 — CONFIRMED/CLOSED**;
- Fall 11 rămâne exemplul canonic principal pentru rang și cele trei niveluri; formula tipărită are `m=8` sus, `d=5, k=5, p=4, e=4` la mijloc și `hy=2, h2, s=1` jos;
- **CH43-NOTATION-01 — CONFIRMED/CLOSED** prin control vizual extern;
- `Triebklasse = genus proximum`; `Triebformel = differentiae specificae`;
- formula individualizează `Notausgänge / Triebventile` în doctrina lui Szondi, fără echivalarea lor cu resurse sănătoase;
- rangul psihodiagnostic și characterologic revendicat istoric de Szondi este consemnat explicit: `Triebformel` și `Trieblinnäus` sunt folosite în doctrina lui pentru `Triebnatur`, `Charakter` și `Krankheitsform`, fără transformarea acestei revendicări în validare clinică contemporană sau diagnostic mecanic;
- contraexemplul intern din `Triebpathologie II` — `Die experimentelle Triebdiagnose war demnach falsch.` — protejează limita infailibilității;
- aceeași `Triebklasse` poate avea formule diferite și configurații Uni-/Tritendenz diferite;
- `Triebformel` este actuală, se poate schimba și are numai relativă `Umweltstabilität`;
- factorii mediani `submanifest / sublatent` aparțin formulei complete chiar dacă tabelele `Trieblinnäus` îi omit;
- pentru coloana de șase profile a `Tabelle 13`, sunt tipărite `1->2, 2->3, 3->5, 4->7, 5->8, 6->10`; **`0->0` nu este celulă tipărită**;
- **CH43-SHORT-01 — SOURCE CONFLICT HOLD ACTIVE:** `Tabelle 13` cere `Umrechnung` și include `Triebformel` în titlu, dar Fall 18 tipărește formula cu indicii TspG bruți `5,4,3,3,2,2,1,0`; manualul nu alege un algoritm universal pentru seriile 3–9;
- controlul mecanic extern reconfirmă Fall 11 `8,5,5,4,4,2,2,1`, Fall 18 brut `5,4,3,3,2,2,1,0` și conversia valorilor nenule la `8,7,5,5,3,3,2,0`; incompatibilitatea numerică este reală;
- `CH43-ABBR-01` și `CH43-SHORT-01` rămân active, dar nu blochează capitolul deoarece manualul documentează limitele sursei fără inferență;
- Deri rămâne pedagogie timpurie; Mélon tradiție ulterioară; niciunul nu suprascrie `Lehrbuch` și nici nu rezolvă `CH43-ABBR-01`;
- `TspQu` și `% Sy-Re` rămân pentru cap. 44;
- `Triebformel ≠ diagnostic autonom ≠ etiologie demonstrată ≠ tip fix`.

### Statutul focus-urilor după stabilizare

- **CH43-AUDIT-01 — CONFIRMED/CLOSED:** structura în trei niveluri și regula `TspG <=2` sunt confirmate; refuzul clusteringului exhaustiv rămâne protejat;
- **CH43-NOTATION-01 — CONFIRMED/CLOSED:** Fall 11 a fost verificat vizual extern și redarea este confirmată;
- **CH43-ABBR-01 — SOURCE/PROCEDURE HOLD ACTIVE:** limita selecției universale a formulei abreviate rămâne documentată și nu este rezolvată prin stabilizare;
- **CH43-SHORT-01 — SOURCE CONFLICT HOLD ACTIVE:** conflictul `Tabelle 13 / Umrechnung` versus Fall 18 rămâne documentat; `0->0` nu este atribuit ca celulă tipărită și HOLD-ul nu este rezolvat prin stabilizare.

### Reader/style status

- verdict extern pe DRAFT v2: **PASS WITH MODERATE REVISION — REVISION REQUIRED BEFORE STABLE**;
- revizia a fost integrată în DRAFT v3 prin eliminarea infrastructurii de audit din vocea cărții, reducerea dublărilor de protecție și compactarea secțiunilor indicate;
- recheck extern final pe DRAFT v3: **STYLE PASS — READY FOR STABLE DRAFT**;
- **READER PASS CLOSED / CHAPTER STABLE**.

Formula de control:

**Calculul comprimă distribuția serială a factorilor; nu produce singur etiologie, diagnostic sau prognostic clinic.**

Cap. 43 nu se redeschide fără o problemă concretă nouă. `CH43-ABBR-01` și `CH43-SHORT-01` rămân limite active ale sursei.

## Capitolul 44 — OUTLINE COMPLETE / DRAFT NEXT / CH44-AUDIT-01 ACTIVE / CH44-AUDIT-02 ACTIVE / CH44-ROUND-01 SOURCE/PROCEDURE HOLD ACTIVE

**Titlu:** `TspQu` și `% Sy-Re`: indicii seriei

Research-ul 10/10, bounded deep corpus pass, controlul vizual canonic al formulelor și exemplelor și outline-ul sunt închise. Nu există încă DRAFT, audit doctrinar sau reader pass pentru cap. 44.

Documente active:

- `research/CH44_RESEARCH.md` — RESEARCH COMPLETE / OUTLINE COMPLETE / DRAFT NEXT / CH44-AUDIT-01 ACTIVE / CH44-AUDIT-02 ACTIVE / CH44-ROUND-01 SOURCE/PROCEDURE HOLD ACTIVE;
- `research/CH44_OUTLINE.md` — OUTLINE COMPLETE / RESEARCH CLOSED / DRAFT NEXT / CH44-AUDIT-01 ACTIVE / CH44-AUDIT-02 ACTIVE / CH44-ROUND-01 SOURCE/PROCEDURE HOLD ACTIVE.

### Achiziții protejate pentru DRAFT v1

- `TspQu = Σ0 / Σ±`;
- `% Sy-Re = ((Σ0 + Σ±) × 100) / (8 × N)`;
- `TspQu` este raportul intern `0/±`, iar `% Sy-Re` este ponderea totală `0+±` în toate reacțiile factoriale ale seriei;
- `TspQu ≠ TspG ≠ TspD ≠ Quantumspannung`;
- `Σ_f TspG(f) = Σ0 + Σ±` este o echivalență aritmetică derivată: permite recuperarea numeratorului `% Sy-Re` din cei opt `TspG`, dar nu permite recuperarea `TspQu` fără separarea globală `Σ0 / Σ±`;
- pentru `Σ±=0` și `Σ0>0`, sursa tipărește canonic `∞`; cazul `0/0` nu este tratat și nu primește sens psihologic inventat;
- reperele `TspQu <1`, `1–3`, `>5` sunt istorice și neexhaustive; `Lehrbuch` avertizează că comportamentul nu se deduce numai din mărimea quotientului;
- `% Sy-Re` folosește denominatorul real `8×N`: la 8 profile =64, la 7=56 etc.; această normalizare procentuală nu este `Umrechnung` prin `Tabelle 13`;
- banda `20–30%` este reper empiric istoric formulat `vorderhand`, nu normă psihometrică contemporană;
- `% Sy-Re` trebuie citit împreună cu `TspQu`; un quotient mic poate coexista cu procent mare;
- `TspQu` este indice al unei serii; o curbă `TspQu` între serii este o succesiune de indici de serie și nu se confundă cu `Inkonstanzmethode`;
- Deri și Mélon rămân tradiție ulterioară atribuită; `Lehrbuch` rămâne sursa tehnică primară;
- `Dur–Moll` și `Sozialindex` rămân pentru cap. 45.

### Focus-uri active

- **CH44-AUDIT-01 — ACTIVE:** pragurile `TspQu` rămân repere istorice neexhaustive și nu devin clasificator clinic modern;
- **CH44-AUDIT-02 — ACTIVE:** `% Sy-Re = 20–30%` rămâne reper istoric/provizoriu; denominatorul `8×N` se păstrează și `Tabelle 13` nu este importată fără bază canonică;
- **CH44-ROUND-01 — SOURCE/PROCEDURE HOLD ACTIVE:** sursa nu declară o regulă universală de rotunjire sau precizie; manualul nu inventează una ca regulă Szondi.

Formula de control:

**`TspQu` descrie compoziția reacțiilor simptomatice; `% Sy-Re` descrie cât spațiu ocupă ele în întreaga serie. Niciunul nu suspendă lectura calitativă a profilelor.**

## Următorul pas autorizat

**CH44 — DRAFT v1.**
