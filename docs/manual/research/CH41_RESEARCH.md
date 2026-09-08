# CH41 — Research

**Capitol:** 41 — `TspG`, `TspD` și `Latenzproportionen`: de la factor la tensiunea vectorială  
**Statut:** RESEARCH COMPLETE — corpus pass 10/10 + bounded deep corpus pass + control vizual canonic al formulelor / OUTLINE NEXT  
**Ramură:** `manual`

---

## Întrebarea cognitivă

Capitolul 40 a stabilit cum pot fi aduse anumite sume din seriile scurte la baza unei `Zehnerserie`, fără a inventa profile. Capitolul 41 trebuie să răspundă acum la întrebarea următoare:

**cum se trece de la reacțiile seriale ale fiecărui factor la o mărime factorială (`TspG`), apoi la o diferență intravectorială (`TspD`) și, în final, la relația dintre cele patru grade de latență (`Latenzproportionen`)?**

Teza de lucru este:

> **`TspG` agregă reacții în interiorul unui factor; `TspD` compară cei doi factori ai aceluiași vector; `Latenzproportionen` compară apoi cele patru diferențe vectoriale.**

Această succesiune trebuie păstrată strict. Niciuna dintre aceste mărimi nu este un profil, un `Vektorbild`, o măsură a `Quantumspannung` sau o diferență temporală între două profile.

---

# I. Sursa primară directă — `Lehrbuch`

## 1. `TspG`: `Grad der Tendenzspannung`

Sursa primară directă este `Lehrbuch der experimentellen Triebdiagnostik`, în special pp. tipărite **268–269**, controlate textual și vizual.

Szondi formulează explicit:

- pentru fiecare factor se determină suma reacțiilor **ambivalente (`±`) și nule (`0`)** din serie;
- această sumă dă `Grad der Tendenzspannung` al factorului;
- abrevierea canonică este **`TspG`**.

Formula operațională a manualului poate fi exprimată fără a inventa notație nouă astfel:

**`TspG(factor) = numărul reacțiilor 0 + numărul reacțiilor ± ale factorului în seria considerată`.**

Important: este vorba despre **numărul de reacții factoriale de tip `0` sau `±`**, nu despre numărul de alegeri, pătrățele sau semne `!` din reacție.

### Sens doctrinar în `Lehrbuch`

Szondi numește `Tendenzspannung` tensiunea produsă de cele două tendințe genetic dublu orientate ale aceluiași `Bedürfnis`. În această construcție:

- reacția `±` face vizibilă dublarea/ambivalența;
- reacția `0` este tratată ca reacție de descărcare și, doctrinar, ca `postambivalente Reaktion`;
- tocmai de aceea `TspG` nu este calculat numai din `±`, ci din **`± + 0`**.

Szondi spune tot aici că factorii simptomatici au `TspG` mare, iar `Wurzelfaktoren` au `TspG` mic.

Această inversiune este esențială pentru capitol: **un `TspG` mic nu înseamnă factor „slab” în doctrina lui Szondi; dimpotrivă, factorul cu `TspG` mai mic este tratat ca mai latent și mai puternic dinamic.**

---

## 2. `TspG` nu este `Quantumspannung`

Această distincție trebuie protejată din cap. 33.

`Quantumspannung` descrie încărcarea cantitativă a unei reacții factoriale și este marcată prin `!`, `!!`, `!!!` etc.

`TspG`, în schimb, este o **mărime serială de frecvență categorială**:

- `0` contribuie cu o apariție;
- `±` contribuie cu o apariție;
- `+` și `−` nu intră în această sumă;
- încărcarea cu `!` nu transformă o reacție `+` sau `−` într-o reacție simptomatică pentru calculul `TspG`.

Deri subliniază ulterior exact această diferență: calculul `TspG` nu se bazează pe numărul absolut de alegeri/„squares”, ci pe frecvența reacțiilor `open` și `plus-minus`.

Formula de control pentru manual:

> **`TspG ≠ Quantumspannung`.**

---

## 3. `täglicher TspG` și `faktorieller TspG`

`Lehrbuch`, p. tipărită **297**, controlată vizual, dă ordinea tehnică a `Trieblinnäus`-ului.

În `Tendenzspannungstabelle`, Szondi calculează:

- pentru fiecare profil, pe orizontală, `Σ0`, `Σ±` și `täglicher TspG`;
- pentru fiecare factor, pe verticală, `Σ0`, `Σ±` și `faktorieller TspG`.

Pentru cap. 41, mărimea care intră în calculul `TspD` este **`faktorieller TspG`**, adică agregatul pe serie al fiecărui factor.

Nu confundăm:

- suma simptomatică a unui profil întreg;
- cu suma simptomatică a unui factor de-a lungul seriei.

---

# II. Domeniul numeric al `TspG`

`TspG` este o numărare pe seria efectiv utilizată.

Dacă seria are `N` profile, valoarea brută a unui `TspG` este între `0` și `N`.

Consecințe:

- într-o `Zehnerserie`, `TspG` este între `0` și `10`;
- într-o serie mai lungă poate depăși `10`;
- `10` nu este un maxim universal al `TspG`, ci maximul unei serii de zece.

`Lehrbuch` folosește chiar un caz cu **15 profile** în care un `TspG` ajunge la **13**.

`Triebpathologie II` spune de asemenea că rezultatele a „10 sau mai multe profile” pot fi prezentate sumar în aparatul formal.

Această precizare protejează cap. 41 de o extrapolare greșită din cap. 40: baza zece este standardul de referință pentru `Zehnerserie` și pentru conversia seriilor scurte, nu limita matematică absolută a mărimilor seriale.

---

# III. `TspD`: diferența intravectorială a gradelor de tensiune

## 1. Definiția canonică

`Lehrbuch`, pp. tipărite **276–277**, controlate vizual, definește `Tendenzspannungsdifferenz`.

Pentru fiecare vector se iau cele două `TspG` factoriale ale factorilor constitutivi și:

> **se scade valoarea mai mică din valoarea mai mare.**

Rezultatul este `TspD`.

Exemplul canonic:

- `TspG h = 9`;
- `TspG s = 2`;
- `TspD` în vectorul S = `9 − 2 = 7`.

Dacă raportul este inversat:

- `TspG h = 2`;
- `TspG s = 9`;
- mărimea rămâne `7`, dar sensul factorial al diferenței se schimbă.

Prin urmare, `TspD` are două componente care nu trebuie confundate:

1. **mărimea numerică a diferenței**;
2. **factorul în favoarea căruia este citită diferența**.

---

## 2. Indexul aparține factorului cu `TspG` mai mic

Szondi adaugă la litera vectorului litera factorului care are **gradul de tensiune mai mic** și care este, în doctrina lui, **dinamic mai puternic**.

Astfel, cele opt variații principale sunt:

`Sh`, `Ss`, `Pe`, `Phy`, `Schk`, `Schp`, `Cd`, `Cm`.

Exemplu:

- `TspG h = 9`, `TspG s = 2`;
- diferența este `7`;
- factorul cu TspG mai mic este `s`;
- forma este **`Ss / 7`** la nivelul notației de latență.

Dacă `h = 2` și `s = 9`, forma devine **`Sh / 7`**.

Această regulă este contraintuitivă și trebuie predată explicit:

> **indexul nu indică factorul cu TspG mai mare, ci factorul cu TspG mai mic.**

---

## 3. `TspD` este o diferență intravectorială, nu temporală

Aceasta trebuie delimitată explicit de cap. 39.

În `Inkonstanzmethode`, diferența este calculată între două profile pentru a descrie schimbarea în timp.

În `TspD`:

- nu comparăm profilul I cu profilul II;
- nu comparăm două momente;
- comparăm **cei doi factori ai aceluiași vector**, după ce fiecare a fost agregat pe întreaga serie prin `TspG`.

Formula de control:

> **diferență temporală între profile ≠ `TspD` intravectorial.**

---

# IV. `TspD = 0` nu înseamnă un singur `Vektorbild`

`Lehrbuch`, p. tipărită **279**, este important tocmai pentru limita metricii.

Szondi arată că `TspD = 0` sau foarte mic poate apărea când cei doi factori ai vectorului au grade egale sau aproape egale.

El distinge mai multe situații calitativ diferite care pot produce diferența zero:

- autoreglarea reciprocă a factorilor prin configurații de tip `++` sau `−−`;
- descărcarea simultană `00`;
- ambivalența simultană `±±`;
- în nota de subsol, și `+−` / `−+` pot avea `TspD = 0`, dar Szondi vorbește acolo despre `Triebentmischung`, nu despre `Trieblegierung`.

Consecința metodologică este decisivă:

> **aceeași valoare numerică `TspD = 0` poate proveni din configurații vectoriale diferite.**

Prin urmare:

- `TspD` nu înlocuiește `Vektorbild`;
- egalitatea numerică nu șterge forma calitativă a reacțiilor;
- calculul seriei rămâne dependent de lectura profilelor.

Această achiziție trebuie protejată la audit și reader pass.

---

# V. `Latenzgrad`, `Latenzgröße` și `TspD`

Terminologia nu este perfect rigidă în toate volumele și nu trebuie rigidizată editorial peste sursă.

## În `Lehrbuch`

Szondi vorbește despre:

- `Tendenzspannungsdifferenz` (`TspD`);
- `Latenzgrad`;
- `Latenzgröße`.

Mărimea numerică a diferenței intravectoriale devine, în lanțul `Trieblinnäus`, gradul/mărimea latenței vectorului.

## În `Triebpathologie II`, pp. tipărite 245–246

Controlul vizual confirmă o reformulare foarte clară:

- `Tendenzspannungsgrad` = suma reacțiilor nule și ambivalente;
- `Tendenzspannungsdifferenz` = diferența dintre gradele de descărcare ale celor doi factori ai vectorului;
- aceeași situație poate fi exprimată în forma unui `Latenzgrad`;
- Szondi spune explicit: **`Latenzgrad oder Latenzgröße`**.

În această prezentare, formula de latență notează:

- vectorul;
- factorul considerat critic/latent și direcția lui;
- în numitor, mărimea diferenței.

Pentru cap. 41 este suficient să stabilim:

> **`TspD` este operația/diferența; valoarea ei localizată în vector este tratată de Szondi ca `Latenzgrad` / `Latenzgröße`.**

Nu transformăm această formulare într-o taxonomie modernă mai rigidă decât textul.

---

# VI. `Latenzproportionen`

## 1. Definiția primară

`Lehrbuch`, p. tipărită **278**, spune că proporțiile relative ale celor patru diferențe de tensiune dau imaginea `Proportionen der Latenz`, adică a raporturilor dinamice dintre cei patru vectori.

Fluxul este:

1. calculăm cei opt `TspG` factoriali;
2. calculăm cele patru `TspD`;
3. ordonăm cele patru diferențe după mărime;
4. obținem seria proporțională a `Latenzgrade` / `Latenzgrößen`.

Aceasta este `Latenzproportion` / `Latenzproportionen`.

Exemplul canonic din `Lehrbuch`, pe 15 profile, este:

`Sh / 13 : Schp / 4 : Cm / 4 : P / 0`.

Acest exemplu arată simultan că:

- valorile pot depăși 10 în serii mai lungi;
- egalitățile sunt posibile (`4` și `4`);
- la diferență zero nu există obligatoriu un factor unic care să dea indexul.

## 2. `Triebpathologie II`: formularea matură

Szondi spune că seria de raporturi a `Latenzgrade` se numește **`Latenzproportionen`** și că ea pune în relație cele patru domenii pulsionale.

Exemplul controlat vizual este:

`Schp− / 10 : Phy− / 6 : Sh+ / 6 : Cd+ / 3`.

Semnele `+ / −` ale factorului latent devin importante pentru `Unterklasse`; aceasta este însă materia cap. 42.

---

## 3. Nu inventăm tie-break la egalitate

Sursele folosesc explicit egalități ale valorilor de latență și doctrina ulterioară lucrează cu `Äqualität`.

Cap. 41 trebuie să prezinte ordonarea după mărime, dar:

- valori egale rămân egale;
- nu inventăm o regulă arbitrară pentru a decide care dintre două diferențe egale „vine prima”;
- efectele clasificatorii ale egalității aparțin cap. 42.

---

# VII. Relația cu seria scurtă și `Tabelle 13`

Aici există un punct operațional care trebuie marcat pentru audit deoarece ordinea calculului contează numeric.

## Ce spune direct sursa

`Lehrbuch` fixează, pentru metoda standard, ordinea:

`Tendenzspannungstabelle -> faktorieller TspG -> cele patru TspD -> Rangreihe der Latenzgrade`.

În cap. 40, `Tabelle 13` spune că pentru seriile de 3–9 profile trebuie convertite **sumele reacțiilor** în raport cu o `angenommene Zehnerserie`, iar titlul tabelului leagă conversia de `Latenzproportion` și `Triebformel`.

## Sinteza operațională cea mai bine susținută

Pentru o serie scurtă, lanțul cel mai fidel celor două instrucțiuni este:

1. se numără, pentru fiecare factor, reacțiile `0` și `±`;
2. aceste sume factoriale sunt convertite prin `Tabelle 13` la baza zece;
3. valorile factoriale convertite sunt apoi comparate în perechi pentru obținerea `TspD`;
4. cele patru diferențe formează `Latenzproportionen`.

Această ordine respectă faptul că p. 287 definește intrarea în `Tabelle 13` drept **„Summe der jeweils erhaltenen Reaktionen”**, iar p. 297 definește `TspD` abia după `faktorieller TspG`.

### Audit focus CH41-SHORT-01

Sursa nu tipărește însă într-o singură propoziție formula „convertim TspG și apoi scădem”. Aceasta este o sinteză procedurală din două pasaje adiacente.

Punctul este material deoarece `Tabelle 13` nu este o transformare liniară perfectă: din cauza valorilor de lookup, **diferența dintre două valori convertite nu coincide întotdeauna cu convertirea directă a diferenței brute**.

Prin urmare:

> **nu vom preda conversia directă a unui `TspD` brut prin `Tabelle 13` fără control doctrinar extern.**

Pentru draft, procedura `sume factoriale -> Tabelle 13 -> TspD` poate fi folosită numai etichetată ca lectură operațională rezultată din secvența canonică, iar auditorul trebuie să controleze explicit acest punct.

Acesta este principalul audit focus al cap. 41.

---

# VIII. Delimitări față de capitolele vecine

## Față de cap. 39

- `Inkonstanz` = diferență temporală / pairwise între profile;
- `TspD` = diferență structurală între factorii parteneri ai aceluiași vector, după agregare serială.

Nu sunt aceeași operație.

## Față de cap. 40

- `Tabelle 13` schimbă baza numerică a sumelor;
- `TspG` și `TspD` sunt operațiile care construiesc apoi aparatul tensiunii factoriale/vectoriale.

## Față de cap. 42

Cap. 41 poate arăta că cea mai mare `TspD` deschide drumul spre `Triebklasse`, dar nu trebuie să predea încă:

- `Haupttriebklasse` ca sistem complet;
- `Unterklasse`;
- semnul `+ / −` al `Wurzelfaktor` ca regulă clasificatorie;
- `Gefahrklasse` / `Ventilklasse`;
- pragurile `5–10` versus `0–4`;
- `Äqualität` ca sistem de clase.

Acestea aparțin cap. 42.

## Față de cap. 43

`Lehrbuch` spune că `Triebformel` se construiește din cei opt `TspG`, dar formula abreviată/completă și regulile ei rămân cap. 43.

## Față de cap. 44

`TspQu` este o altă mărime. Ea compară totalul reacțiilor `0` cu totalul reacțiilor `±` și nu trebuie confundată nici cu `TspG`, nici cu `TspD`.

---

# IX. Tradiția ulterioară: Deri și Mélon

## Susan Deri, pp. 50–55

Deri oferă una dintre cele mai clare explicații pedagogice ulterioare ale mecanicii:

- adună `open` + `plus-minus` pentru fiecare factor;
- numește rezultatul `T.sp.G.`;
- scade indicele mai mic din cel mai mare în fiecare vector;
- numește rândul rezultat `Latenzgrösse`;
- indexează vectorul cu factorul care a avut indicele simptomatic mai mic;
- ordonează cele patru valori pentru `Latenzproportionen`.

Deri insistă și că formalizarea nu înlocuiește analiza profilelor originale.

Ea modifică însă justificarea teoretică: declară că nu adoptă în cartea sa întreaga teorie genetică a lui Szondi și folosește `TspG` mai ales ca sumă a reacțiilor simptomatice. Această diferență de fundamentare trebuie păstrată ca **tradiție ulterioară**, nu retroproiectată în Szondi.

## Jacques Mélon, pp. 165–166

Mélon rezumă aceeași mecanică:

- `TspG` = suma reacțiilor simptomatice ale factorului;
- diferența dintre TspG-urile factorilor parteneri dă diferența intravectorială;
- folosește abrevierea **`TspGD`**, nu `TspD`;
- o numește și `Latenzgrösse`;
- factorul cu `TspG` mai mic dă numele clasei;
- compararea celor patru diferențe dă proporția gradelor de latență.

Manualul păstrează **notația primară Szondi `TspD`**. `TspGD` rămâne variantă a tradiției Mélon, nu devine notație canonică a manualului.

---

# X. Pass 10/10 — relevanța fiecărei surse canonice

## 1. `SCHICKSALSANALYSE- Szondi`

Relevanță secundară. Confirmă că pe baza unei `Zehnerserie` se stabilesc `Triebklasse` și `Triebformel` și că apartenența la clasă este legată de cel mai puternic `Latenzgrad`. Nu adaugă mecanică peste `Lehrbuch`.

## 2. `Susan Deri - Szondi Introduction`

Relevanță tehnică ulterioară ridicată. Explică `TspG`, `Latenzgrösse`, indexarea factorului mai puțin simptomatic și `Latenzproportionen`. Este utilă pedagogic, dar justificarea ei dinamică nu este identică cu fundamentarea genetică Szondi.

## 3. `Szondi Ich-Analyse 1. Teil`

Relevanță doctrinară ridicată pentru sensul proporțional. `Latenzproportionen` sunt tratate ca raporturi de forță relative, individuale și actuale; Szondi spune explicit că metoda experimentală pentru stabilirea lor este descrisă în `Experimentelle Triebdiagnostik`.

## 4. `Szondi Ich-Analyse 2. Teil`

Relevanță de confirmare prin cazuri și formule de latență. Nu introduce o mecanică alternativă pentru `TspG/TspD`.

## 5. `Szondi Lehrbuch der experimentellen Triebdiagnostik`

Sursa primară directă și principală pentru cap. 41. Pasajele controlate vizual: pp. tipărite 268–269 (`TspG`), 276–279 (`TspD` și `Latenzproportionen`), 285–287 (`Tabelle 13`) și 297 (ordinea operațională a `Trieblinnäus`).

## 6. `Szondi Schicksalsanalytische Therapie 1. Teil`

Nu s-a găsit material operațional nou relevant pentru calculul `TspG/TspD/Latenzproportionen` în bounded pass.

## 7. `Szondi Schicksalsanalytische Therapie 2. Teil`

Relevanță doctrinară periferică: menționează că `Latenzproportionen` se pot modifica în timp în anumite condiții. Nu adaugă reguli de calcul.

## 8. `Szondi Triebpathologie 1. Teil`

Relevanță de aplicare și exemplificare. Confirmă utilizarea `Latenzproportionen` în cazuri și faptul că proporțiile latenței pot suferi deplasări. Nu modifică algoritmul primar.

## 9. `Szondi Triebpathologie 2. Teil`

Relevanță primară foarte ridicată ca reformulare matură și compactă. Pp. tipărite 245–246, controlate vizual, definesc din nou `TspG`, `TspD`, `Latenzgrad/Latenzgröße` și `Latenzproportionen` și confirmă că acestea sunt rezultate de serie.

## 10. `The_orie_et_pratique_du_Szondi_J_Me_lon`

Relevanță tehnică ulterioară ridicată. Confirmă mecanica generală, dar folosește notația `TspGD`. Rămâne tradiție ulterioară explicit atribuită.

---

# XI. Achiziții care trebuie protejate în outline și draft

1. **`TspG = Σ(0 + ±)` pe factor, în serie.**
2. **`TspG ≠ Quantumspannung`** și nu este sumă de `!` sau de alegeri.
3. `faktorieller TspG`, nu `täglicher TspG`, este baza pentru `TspD`.
4. Valoarea brută `TspG` depinde de lungimea seriei; într-o serie de 15 poate depăși 10.
5. **`TspD = TspG mai mare − TspG mai mic`** în interiorul aceluiași vector.
6. Indexul vectorului este factorul cu **TspG mai mic**, nu cel cu TspG mai mare.
7. Există patru `TspD`, câte unul pentru S, P, Sch și C.
8. `TspD` este intravectorial, nu temporal; nu se confundă cu `Inkonstanzmethode`.
9. `TspD = 0` nu identifică un singur `Vektorbild`; aceeași diferență poate proveni din forme calitativ diferite.
10. `TspD` / valoarea localizată este numită în surse `Latenzgrad` / `Latenzgröße`; nu rigidizăm artificial termenii.
11. `Latenzproportionen` = relația/ordinea celor patru grade de latență.
12. Egalitățile rămân egalități; nu inventăm tie-break înainte de `Äqualität` din cap. 42.
13. `TspG/TspD/Latenzproportionen` nu suspendă lectura profilelor sau a `Vektorbilder`.
14. `TspQu` este altă operație și rămâne cap. 44.
15. `Triebklasse/Unterklasse` rămân cap. 42; `Triebformel` rămâne cap. 43.
16. **CH41-SHORT-01:** pentru seria scurtă, ordinea `sume factoriale -> Tabelle 13 -> TspD` este sinteza procedurală cel mai bine susținută, dar trebuie controlată explicit de auditor deoarece sursa nu o tipărește într-o singură propoziție și lookup-ul nu este liniar.

---

# XII. Frontiere epistemice pentru redactare

Capitolul trebuie să descrie întâi **operația**, apoi sensul istoric pe care Szondi i-l atribuie.

Nu transformăm automat:

- TspG mic în „forță psihică obiectiv măsurată”;
- TspD mare în severitate clinică;
- `Latenzgrad` în probabilitate diagnostică;
- cea mai mare diferență într-un diagnostic contemporan;
- proporțiile de latență într-o măsură psihometrică validată modern.

Afirmațiile lui Szondi despre `Triebgefahr`, viitorul destinului, `Konduktornatur` și direcții de boală sunt doctrină istorică și vor fi tratate în cap. 42 și în partea clinică, cu frontierele deja fixate ale manualului.

Formula de control a cap. 41:

> **calculul ordonează o serie; nu transformă seria într-un diagnostic.**

---

# XIII. Concluzie de research

Nucleul cap. 41 este canonic stabil:

`reacții factoriale în serie -> Σ(0 + ±) = TspG factorial -> diferența dintre factorii parteneri = TspD -> patru Latenzgrade/Latenzgrößen -> Latenzproportionen`.

Sursa primară directă este suficient de explicită pentru `TspG`, `TspD`, indexare și `Latenzproportionen`, iar `Triebpathologie II` confirmă terminologia într-o formulare matură.

Singurul punct care merită control extern special este **CH41-SHORT-01**, ordinea exactă a aplicării `Tabelle 13` înainte de `TspD` în seriile 3–9, deoarece efectul valorilor de lookup face ca ordinea operațiilor să fie materială.

**Următorul pas: CH41 OUTLINE.**