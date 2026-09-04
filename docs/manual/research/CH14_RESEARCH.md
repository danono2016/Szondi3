# Manualul Szondi — Capitolul 14 — Cercetare 10/10

**Capitol:** 14. Încărcare cantitativă, Quantumspannung și profilul simbolic  
**Statut:** RESEARCH COMPLETE / READY FOR OUTLINE  
**Ramură:** `manual`

## Întrebarea capitolului

**După ce cap. 13 a stabilit forma de bază a reacției factoriale, cum păstrează Szondi în protocol încărcarea cantitativă a aceleiași reacții și cum ajung `!`, `!!`, `!!!` și `Quantumspannung` să completeze profilul simbolic fără a fi confundate cu Tendenzspannungsgrad-ul de serie?**

Punctul de pornire este diferența deja deschisă de cap. 13:

`2/0 → +`  
`6/0 → +!!!`.

Direcția de bază este aceeași. Cantitatea nu este.

---

## 1. Sursa normativă: `Lehrbuch`, Tabelle 3 și secțiunea despre cantitatea reacțiilor

În metodologia matură, Szondi clasifică reacțiile factoriale separat după:

1. **cantitate** — `Nullreaktion`, `Durchschnittsreaktion`, `Vollreaktion`;
2. **Tendenzrichtung`** — pozitivă, negativă, ambivalentă.

Cap. 14 trebuie să lucreze numai cu prima axă și cu modul în care ea se combină cu direcția deja învățată.

Tabelle 3 este sursa formală obligatorie. Implementarea din `main/szondi3/scoring.py` și testul exhaustiv din `tests/test_scoring.py` reproduc această tabelă și sunt utile ca verificare operațională, nu ca surse doctrinare autonome.

---

## 2. `Durchschnittsreaktion`: încărcarea obișnuită

Szondi numește reacție medie / `Durchschnittsreaktion` situația în care două sau trei fotografii ale factorului sunt alese în aceeași direcție și nu mai mult.

El include în această zonă și distribuțiile totale de patru alegeri de tip `3/1` sau `1/3`: există o dominanță direcțională, dar încă nu `Überdruck`.

Formele relevante fără semn de exclamare sunt:

### Pozitive

`2/0`, `2/1`, `3/0`, `3/1` → `+`

### Negative

`0/2`, `1/2`, `0/3`, `1/3` → `−`

### Ambivalente fără supraîncărcare

`2/2`, `3/2`, `2/3`, `3/3` → `±`

Aceste reacții pot fi cantitativ diferite între ele, dar nu primesc marcajul de `Quantumspannung`.

---

## 3. `Vollreaktion`: când una dintre direcții trece de trei alegeri

Szondi vorbește despre `Vollreaktion` când, în interiorul aceluiași factor, apar patru, cinci sau șase alegeri într-o direcție.

La reacțiile pozitive și negative, această acumulare este protocoalată prin semne de exclamare:

| Distribuție | Protocol matur |
|---|---|
| `4/0`, `4/1` | `+!` |
| `5/0`, `5/1` | `+!!` |
| `6/0` | `+!!!` |
| `0/4`, `1/4` | `−!` |
| `0/5`, `1/5` | `−!!` |
| `0/6` | `−!!!` |

Prin urmare, fiecare treaptă peste trei alegeri în aceeași direcție adaugă un nivel de supraîncărcare:

- 4 → `!`;
- 5 → `!!`;
- 6 → `!!!`.

Aceasta este exact logica implementată formal în `scoring.py` prin `quantum_level`.

---

## 4. Ambivalența poate avea și ea Quantumspannung

Tabelle 3 corectează o intuiție prea simplă: `Quantumspannung` nu aparține numai reacțiilor pozitive sau negative.

Distribuțiile:

`4/2 → ±!`  
`2/4 → ±!`

sunt reacții **ambivalente cu supraîncărcare**.

Aceste două cazuri sunt pedagogic decisive, deoarece arată că:

**direcția/tendința reacției și încărcarea cantitativă sunt axe distincte care se pot combina.**

`±!` înseamnă simultan:

- ambivalență la nivelul Tendenzrichtung;
- `Überdruck` / `Quantumspannung` într-una dintre direcții.

Cap. 14 trebuie să facă această dublă lectură formală intuitivă înainte de orice sens factor-specific.

---

## 5. Ce măsoară semnul `!`

În vocabularul lui Szondi, `Überdruck` și `Quantumspannung` desemnează acumularea cantitativă accentuată a unei trebuințe într-o anumită direcție de alegere.

Pentru manual, definiția formală minimă este:

> **`!` marchează faptul că una dintre direcțiile de alegere ale factorului a acumulat cel puțin patru dintre cele șase fotografii disponibile.**

Nivelurile sunt:

- `!` — patru alegeri în direcția supraîncărcată;
- `!!` — cinci;
- `!!!` — șase.

Important: `!` nu înseamnă automat severitate clinică, boală, pericol sau „mai multă patologie”. Este mai întâi un marcaj formal al cantității reacției într-un profil.

---

## 6. De ce `3/3` nu primește `!`

Acesta este unul dintre cele mai bune controale conceptuale.

`3/3` folosește toate cele șase fotografii ale factorului și totuși se scrie simplu:

`3/3 → ±`.

În schimb:

`4/2 → ±!`.

Prin urmare, `Quantumspannung` nu este pur și simplu „numărul total de fotografii ale factorului care au fost alese”.

Ea apare când **una dintre direcții depășește pragul de trei și ajunge la patru, cinci sau șase alegeri**.

Această diferență trebuie explicată explicit; altfel cititorul poate confunda cantitatea totală a reacției cu supraîncărcarea unei tendințe.

---

## 7. Quantumspannung NU este Tendenzspannungsgrad (TspG)

Această graniță este obligatorie.

### Quantumspannung

- unitate de analiză: **o reacție factorială într-un profil**;
- date: numărul de alegeri simpatice/antipatice ale factorului în acel profil;
- marcaj: `!`, `!!`, `!!!`;
- apare în Tabelle 3 și în scrierea profilului individual.

### Tendenzspannungsgrad — TspG

- unitate de analiză: **un factor într-o serie de profiluri**;
- date: frecvențele reacțiilor `0` și `±` ale factorului de-a lungul seriei;
- formula matură: `TspG = Σ0 + Σ±`;
- este folosit ulterior pentru ordonarea factorilor, Triebformel, TspD, Latenzproportionen etc.

În `Lehrbuch`, definiția TspG apare în aparatul de serie, mult după metodologia reacției individuale. `main/szondi3/series.py` păstrează exact această separare prin `factor_tension_degrees()`.

**Regulă pentru proza cap. 14:** TspG poate apărea doar într-o frază de delimitare („nu este același lucru”), fără a fi predat sau calculat. Aparatul lui aparține părții de serie.

---

## 8. Legătura cu dinamica încărcare–descărcare

În `Lehrbuch` și deja în `Triebpathologie`, Szondi interpretează `Quantumspannung` într-o dinamică mai largă de acumulare, ambivalență și descărcare.

El descrie schematic succesiuni de tip:

**Quantumspannung → ambivalență → descărcare / Nullreaktion**.

Această doctrină este utilă pentru a arăta de ce `!` nu este un simplu ornament grafic. Dar cap. 14 nu trebuie transformat într-un capitol clinic sau într-o teorie completă a fazelor.

Dozaj recomandat:

- o scurtă explicație a termenului `Spannung` ca încărcare/încordare cantitativă în modelul lui Szondi;
- fără predicții despre evoluția unei persoane dintr-un singur profil;
- fără a deduce că orice `!` „trebuie” să urmeze o descărcare observabilă.

---

## 9. Profilul simbolic complet

După cap. 13 cititorul știe să obțină forma de bază:

`h+`, `s−`, `e±`, `hy0` etc.

Cap. 14 adaugă încărcarea și permite scrierea completă a reacției:

`h+!`, `s−!!`, `e±!`, `hy0` etc.

La sfârșitul capitolului, cititorul trebuie să poată lua numărătorile celor opt factori și să scrie un **profil simbolic complet și verificabil**, organizat pe cei patru vectori:

`S(h,s) — P(e,hy) — Sch(k,p) — C(d,m)`.

Aceasta este pragul pedagogic fixat de arhitectură după cap. 14: **construcția corectă a profilului, încă fără interpretare clinică.**

---

## 10. Control software: ce confirmă `main`

`main/szondi3/scoring.py` implementează Tabelle 3 astfel:

- `quantum_level = 0` pentru reacțiile fără `!`;
- pozitiv/negativ: nivelul crește cu fiecare alegere peste 3 în direcția dominantă;
- ambivalent: `4/2` și `2/4` primesc `quantum_level = 1`;
- simbolul rezultat este exact `+!`, `+!!`, `+!!!`, `−!`, `−!!`, `−!!!`, `±!`.

`tests/test_scoring.py` verifică exhaustiv toate cele 28 de distribuții și include teste explicite pentru nivelurile de Quantumspannung.

Acest control este congruent cu Tabelle 3 și poate fi folosit pentru verificarea exemplelor din manual.

---

## 11. Forward hold: `0` liber vs `ø`

Cap. 14 nu trebuie să transforme orice reacție nulă într-o unitate interschimbabilă.

În EKP există `ø` — `Zwangs-Nullreaktion` — atunci când VGP a consumat deja 5 sau 6 fotografii ale factorului și complementul nu mai are libertatea numerică de a produce alt tip de reacție.

Pentru cap. 14 este suficient un hold editorial:

- nu introduce `ø` în tabelul VGP ca și cum ar fi un al cincilea semn de bază;
- reamintește-l în cap. 37/complement și în partea de serie;
- nu permite ca `ø` să intre tacit în TspG sau alți indici ai reacțiilor libere.

`main/szondi3/scoring.py` și `series.py` implementează deja această protecție.

---

## 12. Matrice corpus 10/10

| Sursă | Relevanță | Funcție pentru cap. 14 |
|---|---|---|
| `SCHICKSALSANALYSE` | control istoric | forme timpurii ale profilului și încărcării; nu sursa matură pentru praguri |
| `TRIEBPATHOLOGIE I` | **importantă** | Quantumspannung și dinamica încărcare–ambivalență–descărcare |
| `TRIEBPATHOLOGIE II` | control clinic | numeroase utilizări ale Quantumspannung în sindromatică; nu definește tabela finală |
| `ICH-ANALYSE I` | control doctrinar | folosește Quantumspannung în analiza funcțiilor Eului |
| `ICH-ANALYSE II` | control doctrinar | exemple de reacții cu supraîncărcare; fără schimbarea pragurilor |
| `THERAPIE I` | periferic | profile în context terapeutic; fără redefinirea formală |
| `THERAPIE II` | periferic | idem |
| `LEHRBUCH` | **CENTRALĂ / normativă** | Null-/Durchschnitts-/Vollreaktion, Tabelle 3, `Überdruck`, `Quantumspannung`, protocol `!` |
| `DERI` | tradiție pedagogică | limbajul `loaded reactions` și explicații de tensiune; se folosește atribuit și nu prevalează asupra Tabelle 3 |
| `MÉLON` | tradiție ulterioară | explică tensiunile factoriale și ulterior TspG; util mai ales pentru control terminologic |

Corpus pass-ul nu arată motiv pentru a modifica pragurile mature din Tabelle 3.

---

## 13. Anti-inferențe obligatorii

- `!` ≠ „mai bolnav”;
- `!!!` ≠ diagnostic sau severitate clinică automată;
- `Quantumspannung` ≠ TspG;
- `Quantumspannung` ≠ simplul total de fotografii alese pentru factor;
- `3/3` are total 6, dar NU are `!`;
- `4/2` și `2/4` sunt `±!`, nu `+`/`−`;
- direcția de bază și încărcarea cantitativă sunt informații distincte;
- `0` liber ≠ `ø` forțat;
- profilul simbolic complet ≠ interpretare clinică.

## Ipoteză de construcție

1. deschidere: `2/0 → +` versus `6/0 → +!!!`;
2. de ce semnul de bază pierde informație cantitativă;
3. Durchschnittsreaktion și Vollreaktion;
4. `! / !! / !!!` ca marcaje ale Quantumspannung;
5. cazul surprinzător `4/2 → ±!` și `2/4 → ±!`;
6. controlul `3/3 → ±` pentru a evita ideea „total mai mare = mai multe !”;
7. delimitare explicită Quantumspannung ≠ TspG;
8. construirea unui exemplu complet de profil simbolic, fără interpretare;
9. închiderea Părții III: cititorul poate construi un profil corect; următoarea parte va începe sensul factorilor.

## Verdict de cercetare

**RESEARCH COMPLETE.** Poate fi redactat outline-ul. TspG rămâne în afara capitolului, cu excepția delimitării negative.