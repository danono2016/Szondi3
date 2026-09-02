# Manualul Szondi — Audit de arhitectură

## TRANȘA 6 — CAPITOLELE 38–44

**Statut:** WORKING / DRAFT  
**Ramură:** `manual`  
**Scop:** audit structural al trecerii de la profilul singular la serie și de la observația serială la aparatul cantitativ: constanță/schimbare, normalizarea seriilor scurte, TspG/TspD, Latenzproportionen, Triebklasse/Unterklasse, Triebformel și indicii/proporțiile formale.

> Acest document continuă `docs/manual/ARCHITECTURE_AUDIT.md` și auditurile 10–14, 15–26, 27–31 și 32–37. Este audit structural 10/10, nu cercetarea de finalizare a capitolelor.

## Matrice de relevanță

| Cap. | SA | LEHR | IA-A | IA-B | THER-A | THER-B | TRIEB-1 | TRIEB-2 | DERI | MELON |
|---|---|---|---|---|---|---|---|---|---|---|
| 38. De la profil la serie | CONTRIBUTIVĂ | CENTRALĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTROL | CONTRIBUTIVĂ | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ |
| 39. Constanță, schimbare și fază | CONTROL | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ | CONTROL | CONTRIBUTIVĂ | CENTRALĂ | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ |
| 40. Seria scurtă și Tabelle 13 | CONTROL | CENTRALĂ | CONTROL | CONTROL | CONTROL | CONTROL | CONTROL | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTROL |
| 41. TspG, TspD și Latenzproportionen | CONTRIBUTIVĂ | CENTRALĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTROL | CONTRIBUTIVĂ | CENTRALĂ | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ |
| 42. Triebklasse și Unterklasse | CONTRIBUTIVĂ | CENTRALĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTROL | CONTROL | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ |
| 43. Triebformel | CONTRIBUTIVĂ | CENTRALĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTROL | CONTROL | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ |
| 44. Indicii seriei / metode proporționale | CONTROL | CENTRALĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTROL | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ |

Abrevieri: SA=`SZ_SA_1948`; LEHR=`SZ_LEHR_1972`; IA-A/B=`SZ_IA_1956_A/B`; THER-A/B=`SZ_THER_1963_A/B`; TRIEB-1/2=`SZ_TRIEBPATH_1/2`.

---

# Verdict structural major

**PĂSTRĂM nucleul întregii tranșe, dar facem trei corecții importante de arhitectură.**

1. Capitolul 38 trebuie să pornească explicit de la ideea târzie a lui Szondi că un profil singular face vizibilă **o posibilitate de existență**, nu „persoana întreagă”; seria este necesară tocmai pentru pluralitatea posibilităților și a fazelor.
2. Capitolul 40 trebuie îngustat drastic: nu este despre „organizarea seriei” în general, ci despre **seria scurtă și normalizarea prin Tabelle 13 la baza convențională de zece**.
3. Capitolul 44, în forma actuală „Indicii și proporțiile formale”, este prea larg. `Lehrbuch` separă clar indicii din cadrul `Linnäusmethode` (`TspQu`, `% Sy-Re`) de metodele proporționale ulterioare (`Dur–Moll/Sexualindex`, `Sozialindex`). Recomandăm **scindarea internă în 44A și 44B**, iar renumerotarea definitivă se amână până la închiderea auditului întregii cărți.

Această tranșă trebuie să fie cea mai disciplinată formal din manual. Cititorul trebuie să vadă permanent diferența dintre:

**date brute ale seriei → operație de calcul → categorie formală → sens doctrinar → inferență clinică.**

Aici o eroare de un prag, o egalitate tratată arbitrar sau o formulă extinsă fără regulă sursă poate schimba întregul rezultat. De aceea, toate tabelele, formulele și exemplele vor fi verificate vizual în PDF-ul canonic înainte de FINAL.

---

## 38. De ce un singur profil nu este suficient

### Verdict
**PĂSTRĂM, dar mutăm centrul de greutate de la ideea vagă de „fiabilitate prin repetare” la doctrina pluralității posibilităților de existență.**

### Titlu recomandat
**De la profil la serie: de ce un singur profil nu este suficient**

### Nucleu canonic
În ediția târzie a `Lehrbuch`, Szondi formulează direct principiul care trebuie să conducă acest capitol: omul nu are un singur destin, ci mai multe `Schicksalsmöglichkeiten`, adesea orientate în direcții opuse. Un singur `Triebprofil` face vizibilă numai una dintre aceste posibilități; de aceea el cere, pentru persoană, **opt până la zece profile**. Fiecare profil trebuie interpretat mai întâi ca un întreg și ca o posibilitate de existență în sine, înainte de sinteza serială.

Această formulare este mai matură și mai bună pedagogic decât simplul „un test nu ajunge”. Repetarea nu este doar un artificiu statistic. Ea face vizibilă **pluralitatea și transformarea**.

### Cronologia trebuie păstrată
Corpusul nu spune peste tot exact același lucru despre numărul necesar de profile:

- în `Schicksalsanalyse` și în lucrările timpurii apare frecvent `Zehnerserie` ca bază pentru Triebklasse și Triebformel;
- `Triebpathologie` formulează adesea calculele pe zece sau mai multe profile;
- Deri lucrează pedagogic cu seria de zece, dar în prefață spune și că metoda trebuie administrată cel puțin de șase ori;
- `Lehrbuch` 1972 formulează explicit **8–10 profile** și oferă `Tabelle 13` pentru seriile mai scurte.

Manualul nu va transforma aceste formulări istorice într-o singură propoziție atemporală. Pentru mecanica formală vom lua ediția târzie a `Lehrbuch` drept reper principal și vom marca diferențele de etapă.

### Ce trebuie să învețe cititorul
Capitolul separă trei niveluri:

- **profilul singular** — o configurație actuală, interpretabilă în întregimea ei;
- **succesiunea de profile** — schimbare, constanță, alternanță, fază;
- **seria ca bază de calcul** — datele din care pot fi derivate TspG, TspD, Latenzproportionen, clase și formule.

### Interdicții
- Nu spunem că seria „dezvăluie adevărata personalitate” iar profilul singular ar fi fals.
- Nu reducem repetarea la control de consistență.
- Nu folosim un singur profil pentru a produce categorii seriale care presupun explicit o serie.
- Nu confundăm utilizarea unuia/două profile în cercetări de grup cu interpretarea individuală completă.

---

## 39. Constanță, schimbare și oscilație

### Verdict
**PĂSTRĂM, dar înlocuim „oscilație” cu termenul mai precis de „fază”.**

### Titlu recomandat
**Constanță, schimbare și fază în serie**

### De ce „fază”
`Lehrbuch`, `Ich-Analyse` și materialul clinic descriu nu numai alternanțe mecanice, ci treceri de fază în care același factor poate deveni simptomatic, submanifest sau Wurzelfaktor și apoi poate reveni. În materialul longitudinal, Szondi vorbește despre o **stabilitate relativă**, nu absolută: Triebklasse și Triebformel se pot modifica în timp, în timp ce direcția și calitatea transformării pot rămâne relativ caracteristice.

Acesta este un punct doctrinar important: **stabilitatea nu înseamnă imobilitate**.

### Axele de lectură ale seriei
Capitolul trebuie să învețe cititorul să urmărească:

1. constanța unei direcții factoriale;
2. frecvența reacțiilor `0` și `±`;
3. trecerile `+ ↔ −` și schimbările de încărcare;
4. apariția/dispariția `Quantumspannung`;
5. trecerea unui factor între poziție simptomatică, submanifestă și radicală;
6. transformările vectoriale repetate;
7. raportul dintre schimbarea testologică și faza temporală/clinică.

Deri este pedagogic foarte utilă aici: recomandă așezarea profilelor simbolizate unul sub altul pentru a vedea rapid tendințele de constanță și schimbare, dar avertizează că înregistrarea abreviată nu poate înlocui profilele grafice originale, unde se văd intensitatea și detaliile cantitative.

### Distincție epistemică
Vom separa explicit:

- **constanță observată** în N profile;
- **categorie formală** obținută din frecvențe;
- **interpretarea szondiană** a constanței/schimbării;
- **corelația clinică** dintr-un caz sau dintr-o tradiție ulterioară.

O repetare a unei reacții nu devine automat trăsătură de caracter; o schimbare nu devine automat patologie.

### Interdicții
- Nu transformăm `stabil` în „constituțional” fără condițiile sursei.
- Nu transformăm orice alternanță `+ ↔ −` în diagnostic.
- Afirmațiile lui Deri despre reversări factoriale/vectoriale vor fi prezentate ca Deri, nu retroproiectate automat ca reguli universale ale lui Szondi.

---

## 40. Tabelle 13 și organizarea seriei

### Verdict
**PĂSTRĂM, dar REDEFINIM COMPLET funcția capitolului.**

### Titlu recomandat
**Seria scurtă și Tabelle 13: normalizarea la baza de zece**

### Nucleu canonic
În `Lehrbuch`, după discuția privind numărul de profile necesare, Szondi oferă `Tabelle 13` ca tabel de conversie pentru seriile sub zece. Datele obținute la 3–9 profile sunt raportate la o **bază convențională de zece**, astfel încât proporțiile de latență și formula să poată fi comparate în același cadru de calcul.

Aici trebuie să fim foarte stricți: `Tabelle 13` este o **regulă internă a metodei**, nu dovada modernă că trei sau patru profile ar avea aceeași valoare informațională ca zece.

### Ce trebuie prezentat formal
Capitolul va distinge vizual:

**N observat → frecvență brută → conversie Tabelle 13 → valoare normalizată la baza de zece → calcul ulterior.**

Pentru fiecare exemplu trebuie afișate atât datele brute, cât și rezultatul conversiei; nu vom lăsa cititorul să creadă că numărul convertit a fost efectiv observat.

### Afirmațiile istorice despre „constanță”
`Lehrbuch` oferă și afirmații despre momentul la care anumite elemente ale `Trieblinnäus` ar deveni constante pe măsură ce crește numărul de profile. Acestea vor fi prezentate exact ca **afirmații metodologice ale lui Szondi**, nu ca validare statistică contemporană.

### Interdicții
- Nu extrapolăm liniar în afara tabelului.
- Nu inventăm rotunjiri, egalități sau interpolări care nu apar în sursă.
- Nu aplicăm calcule de Zehnerserie la serii scurte fără conversia cerută de metodă.
- Dacă un caz formal produce ambiguitate după conversie, manualul o va declara, nu o va rezolva prin convenție proprie.

---

## 41. Tensiunea factorială și proporțiile de latență

### Verdict
**PĂSTRĂM, dar titlul trebuie să numească exact operatorii formali.**

### Titlu recomandat
**TspG, TspD și Latenzproportionen: de la factor la tensiunea vectorială**

### Ordinea formală
Aici cititorul trebuie să poată reproduce mecanic calculele:

1. pentru fiecare factor se numără reacțiile `0` și `±` din serie;
2. suma lor constituie `Tendenzspannungsgrad` (`TspG`);
3. în fiecare vector se compară TspG-urile celor doi factori;
4. diferența intravectorială constituie `Tendenzspannungsdifferenz` (`TspD`, respectiv `Latenzgröße/Latenzgrad` în terminologia sursei);
5. cele patru diferențe formează `Latenzproportionen`.

`Triebpathologie` explică explicit TspG ca sumă a reacțiilor nule și ambivalente și TspD ca diferență a gradelor de disponibilitate pentru descărcare dintre cei doi factori ai vectorului. `Lehrbuch` rafinează ulterior această mecanică și o folosește pentru Haupttriebklasse, Gefahr/Ventil și Trieblinnäus.

### Atenție terminologică
Nu vom traduce `TspG` printr-un vag „nivel de tensiune al factorului”. În sistem, TspG este un **indice serial calculat din frecvența reacțiilor simptomatice (`0` + `±`)**. Sensul său doctrinar poate fi discutat după ce operația este clară.

La fel, `Latenzgröße` nu este „cantitatea de inconștient”. Este diferența formală dintre TspG-urile celor doi factori ai unui vector, căreia Szondi îi atribuie un sens dinamic.

### Interdicții
- Nu confundăm TspG cu `Quantumspannung` dintr-un profil singular.
- Nu confundăm TspD cu diferența brută dintre numărul de alegeri simpatice/antipatice.
- Nu numim automat valoarea mare „patologie”.
- Nu sărim direct de la număr la diagnostic înainte de capitolele 42–44 și de întoarcerea la lectura calitativă.

---

## 42. Triebklasse, Unterklasse și Wurzelfaktor

### Verdict
**PĂSTRĂM, dar aducem aici formal distincția Gefahr/Ventil amânată deliberat în capitolul 36.**

### Titlu recomandat
**Triebklasse și Unterklasse: Wurzelfaktor, Triebgefahr și Ventil**

### Arhitectura canonică
În `Lehrbuch`:

- cele opt `Haupttriebklassen` sunt determinate din diferențele intravectoriale;
- direcția `Unterklasse` este dată de polaritatea Wahlrichtung a trebuinței nesatisfăcute, adică a `Wurzelfaktor`-ului;
- într-o Zehnerserie, `Latenzgröße` **5–10** este plasată în zona `Triebgefahr`, iar **0–4** în zona `Triebventil`;
- vectorul cu diferența cea mai mare indică locul celei mai puternice Triebgefahr actuale în logica metodei.

Acesta este momentul potrivit să legăm formal ceea ce capitolul 36 a prezentat calitativ drept pericol și răspuns/ieșire.

### Wurzelfaktor: două corecții obligatorii
Manualul trebuie să insiste asupra a două afirmații explicite ale lui Szondi:

1. o reacție Wurzel negativă nu înseamnă automat refulare; poate exprima și renunțare/adaptare;
2. și o reacție Wurzel pozitivă poate reprezenta o trebuință rămasă nesatisfăcută.

Aceste două corecții sunt indispensabile pentru a împiedica apariția unui dicționar simplist `+ = acceptat`, `− = reprimat`.

### Despre mono-/bi-/tri-/quadrigefahr și Ventil
Clasificările ulterioare ale numărului de pericole/ventile pot fi prezentate numai după verificarea exactă a regulilor în sursa primară. Mélon este util pentru claritate și pentru terminologia triventil/quadriventil, dar selectorii lui trebuie atribuiți ca tradiție ulterioară dacă nu sunt regăsiți textual la Szondi.

### Interdicții
- `Sh+`, `Pe−`, `Schk+`, etc. nu sunt diagnostice.
- Clasa nu este un „tip de personalitate” imuabil.
- `Gefahr` nu înseamnă automat comportament periculos social.
- `Ventil` nu înseamnă automat mecanism sănătos ori patologic; el trebuie citit în configurația și faza cazului.
- Nu importăm denumirile nosologice din tabelele de clase ca verdict asupra unei persoane fără restul dovezilor cerute de metodă.

---

## 43. Triebformel

### Verdict
**PĂSTRĂM și îl transformăm într-un capitol formal cu limite explicite.**

### Titlu recomandat
**Triebformel: formula abreviată, formula completă și limitele calculului**

### Nucleu istoric și dezvoltare
În `Schicksalsanalyse`, formula este prezentată timpuriu ca fracție: factorii simptomatici la numărător, `Wurzelfaktoren` la numitor. În lucrările ulterioare, mai ales `Lehrbuch`, apar diferențierea dintre `abgekürzte Triebformel` și `vollständige Triebformel`, precum și nivelul factorilor submanifest/sub-latenți.

Pentru manual, acest lucru trebuie prezentat ca **dezvoltare a metodei**, nu ca și cum toate edițiile ar fi conținut aceeași regulă finală.

### Formula completă
În `Lehrbuch`, ordonarea factorilor se bazează pe rangul TspG, iar pentru formula completă apare regula conform căreia factori a căror diferență TspG nu este mai mare de 2 pot fi plasați pe aceeași linie. Orice exemplu va fi verificat vizual în PDF, deoarece formulele sunt deosebit de vulnerabile la OCR și la pierderea poziționării verticale.

### Formula abreviată: prudență maximă
Corpusul oferă exemple clare de formule abreviate și forme abreviate mai largi. Totuși, **nu vom deduce dintr-un exemplu particular un selector universal pentru toate egalitățile sau extinderile multifactoriale** dacă sursa nu îl formulează textual.

În special, forme de tip `k/s` și `kp/hs` trebuie tratate la finalizare ca problemă de arbitraj vizual și doctrinar. Dacă două reguli posibile produc două formule plauzibile, manualul va declara ambiguitatea și va rămâne fail-closed.

### Deri ca avertisment metodologic
Deri este importantă tocmai pentru limită: recomandă completarea tuturor categoriilor de scoring, dar avertizează să nu se bazeze interpretarea pe `drive-classes` și `formulas` fără analiza calitativă atentă a profilelor însele.

### Interdicții
- Formula nu este „rezumatul personalității”.
- Numărătorul și numitorul nu sunt o ierarhie morală bine/rău.
- Wurzelfaktor-ul din numitor nu este automat „reprimatul”.
- Nicio formulă nu va fi interpretată fără întoarcerea la factori, vectori, serie și context clinic.

---

## 44. Indicii și proporțiile formale

### Verdict
**NU PĂSTRĂM capitolul în forma nediferențiată actuală. RECOMANDĂM SCINDARE INTERNĂ.**

`Lehrbuch` separă două familii care au funcții și riscuri interpretative diferite. Dacă le punem sub o singură etichetă, cititorul poate crede că toate sunt doar „niște indici” calculați pe aceeași logică.

### 44A recomandat
**TspQu și % Sy-Re: indicii seriei**

#### TspQu
`Tendenzspannungsquotient` exprimă raportul cantitativ dintre reacțiile nule și cele ambivalente și este folosit de Szondi pentru a discuta raportul dintre simptome exterioare și interioare / modalitatea comportamentală. Dar sursa formulează chiar aici o interdicție esențială: **nu este permisă deducerea comportamentului din valoarea TspQu singură**. Configurația factorială poate modifica sensul aceleiași valori.

Această frază trebuie să fie în manual lângă orice prag numeric.

#### % Sy-Re
`prozentuale Symptomreaktionen` exprimă proporția totalului reacțiilor `0 + ±` față de toate reacțiile factoriale disponibile. Numitorul depinde de numărul de profile: într-o serie de zece sunt 80 de reacții factoriale, într-una de opt sunt 64 etc. Este un bun exemplu pentru diferența dintre **calcul exact** și **interpretare contextuală**.

#### Coda: Trieblinnäus
La finalul 44A trebuie introdusă o pagină de sinteză care arată cum TspG, Latenzproportionen, Triebklasse, Triebformel, TspQu și % Sy-Re se așază împreună în aparatul `Trieblinnäus`. Manualul actual are toate piesele, dar fără această sinteză cititorul riscă să nu vadă ansamblul formal.

### 44B recomandat
**Dur–Moll și Sozialindex: metode proporționale și limite**

Acest subcapitol trebuie separat deoarece intrăm într-o zonă istorică și terminologică sensibilă: sexualitate, masculin/feminin, social pozitiv/social negativ, grupuri clinice și criminologice.

#### Dur–Moll / Sexualindex
`Lehrbuch` însuși avertizează că materialul prezentat nu permite încă afirmații definitive despre anumite grupuri profesionale sau de boală și formulează explicit regula că `Dur–Moll-Index` **nu trebuie folosit niciodată singur pentru evaluarea socială**; el trebuie citit sinoptic cu `Sozialindex`.

Manualul va păstra terminologia istorică acolo unde este necesară pentru a explica metoda, dar nu o va converti în afirmații moderne despre sex, gen, orientare sau valoare socială.

#### Sozialindex
Aici trebuie separată complet:

- operația formală de calcul;
- terminologia istorică a lui Szondi;
- exemplele sale clinice/criminologice;
- ceea ce manualul are dreptul să infereze astăzi.

Pragurile numerice nu vor fi folosite pentru a deduce fapte criminale, periculozitate individuală sau o scară generală de sănătate. Orice afirmație de acest tip trebuie fie susținută exact de sursă și limitată istoric, fie exclusă din inferența clinică a manualului.

### De ce scindarea este necesară
TspQu și % Sy-Re sunt extensii naturale ale analizei seriei și ale `Linnäusmethode`. Dur–Moll și Sozialindex sunt `Proporzmethoden` distincte în arhitectura `Lehrbuch`, cu altă istorie conceptuală și cu un risc mult mai mare de anacronism și suprainterpretare.

**Decizie de audit:** păstrăm deocamdată numerotarea `44A / 44B`; renumerotarea tuturor capitolelor ulterioare se va decide numai după auditul complet, pentru a evita mișcări locale care produc haos global.

---

# Secvența formală care trebuie să rămână vizibilă

Pentru această parte a cărții, cititorul trebuie să poată urmări o singură linie de construcție:

**profil singular → succesiune → serie → conversie Tabelle 13 dacă seria este scurtă → TspG pe factor → TspD/Latenzgröße pe vector → Latenzproportionen → Triebklasse/Unterklasse + Gefahr/Ventil → Triebformel → TspQu și % Sy-Re → abia apoi metodele proporționale Dur–Moll / Sozialindex → revenire la analiza calitativă a profilurilor și la contextul clinic.**

Ordinea manualului este pedagogică, nu copiază ordinea capitolelor lui Szondi. În special, faptul că prezentăm clasa înaintea formulei este o alegere editorială pentru a face întâi vizibilă structura celor patru diferențe de latență; nu vom pretinde că aceasta este o prioritate doctrinară universală.

---

# Riscuri care trebuie blocate înainte de redactare

1. **Confuzia profil = persoană.** Profilul singular este o configurație actuală / posibilitate, nu totalitatea individului.
2. **Confuzia TspG = Quantumspannung.** Sunt construcții diferite, la niveluri diferite.
3. **Confuzia Latenzgröße = cantitate de inconștient.** Este o diferență formală intravectorială căreia Szondi îi atribuie sens dinamic.
4. **Confuzia Wurzelfaktor negativ = refulare.** Sursa o exclude explicit ca regulă universală.
5. **Confuzia Wurzelfaktor pozitiv = nevoie satisfăcută.** Sursa admite explicit contrariul.
6. **Confuzia Triebklasse = diagnostic.** Clasa este o categorie a metodei; diagnosticul cere alte niveluri de dovadă.
7. **Confuzia Triebformel = rezumat definitiv al personalității.** Deri avertizează împotriva folosirii claselor/formulelor fără analiza calitativă.
8. **Confuzia prag numeric = verdict clinic.** TspQu, Dur–Moll și Sozialindex au toate nevoie de context; unele au interdicții explicite de folosire izolată.
9. **Generalizarea unui exemplu într-un algoritm.** Egalitățile, formulele abreviate extinse și partiționările complete trebuie să aibă regulă textuală sau să rămână neautomatizate.
10. **Modernizarea cosmetică a termenilor.** Terminologia istorică sensibilă va fi explicată și delimitată, nu rescrisă ca și cum ar fi psihometrie contemporană.

---

# Ce trebuie să poată face cititorul după această tranșă

La capătul 38–44, cititorul ar trebui să poată:

- explica de ce seria schimbă statutul interpretării;
- distinge configurația singulară de constanță și fază;
- normaliza corect o serie scurtă prin Tabelle 13, fără a confunda observatul cu convertitul;
- calcula TspG, TspD și cele patru Latenzproportionen;
- determina formal Haupttriebklasse/Unterklasse și să înțeleagă sensul metodologic al Gefahr/Ventil;
- construi și citi prudent o Triebformel, distingând formula abreviată de cea completă;
- calcula TspQu și % Sy-Re și să știe de ce niciunul nu se interpretează izolat;
- înțelege Dur–Moll și Sozialindex ca metode proporționale istorice distincte și să cunoască limitele inferenței;
- reveni, după toate calculele, la profilurile concrete și la întrebarea clinică.

Acesta este al patrulea prag major al cărții: **cititorul nu mai are doar vocabularul și metoda de lectură, ci poate construi aparatul formal al unei serii fără să confunde calculul cu adevărul clinic.**

Următoarea tranșă trebuie să verifice ce se întâmplă după formalizare: cum sunt folosite constelațiile, sindroamele, formele de existență și/sau aplicațiile clinice fără a transforma metoda într-un catalog diagnostic.