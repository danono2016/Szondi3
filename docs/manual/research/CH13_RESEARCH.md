# Manualul Szondi — Capitolul 13 — Cercetare 10/10

**Capitol:** 13. Reacțiile factoriale: `+`, `−`, `±`, `0`  
**Statut:** RESEARCH COMPLETE / CORRECTED AFTER TABELLE 3 CROSS-CHECK  
**Ramură:** `manual`

## Întrebarea capitolului

**Cum transformă Szondi distribuția brută a alegerilor simpatice și antipatice dintr-un factor în cele patru forme factoriale de bază — pozitivă, negativă, ambivalentă și nulă — și ce exprimă formal fiecare fără a confunda direcția reacției cu încărcarea cantitativă?**

Cap. 12 s-a oprit deliberat la frecvențe. Cap. 13 face operația următoare: clasifică distribuția factorială după forma ei de bază, păstrând separat problema cantității și a `Quantumspannung`, care intră sistematic în cap. 14.

---

## 1. Corecția doctrinară decisivă: Tabelle 3 are prioritate

Controlul direct pe `Lehrbuch`, Tabelle 3, corectează o simplificare introdusă inițial prin regula pedagogică a lui Deri.

În metodologia matură a lui Szondi:

- reacția **pozitivă** cere cel puțin două alegeri simpatice și **cel mult una antipatică**;
- reacția **negativă** cere cel puțin două alegeri antipatice și **cel mult una simpatică**;
- reacția **ambivalentă** cere cel puțin două alegeri în fiecare direcție.

Prin urmare:

- `4/2` NU este `+`; este **`±!`**;
- `2/4` NU este `−`; este **`±!`**.

Acesta este punctul unde regula pedagogică Deri de tip „minimum 2:1” nu poate fi folosită ca regulă exhaustivă. Raportul `4:2` este 2:1, dar Tabelle 3 îl clasifică ambivalent, deoarece ambele direcții ating pragul de minimum două alegeri.

**Prioritate editorială:** pentru clasificarea formală exactă, Szondi matur / Tabelle 3 are prioritate asupra simplificării pedagogice Deri.

---

## 2. Două axe formale, nu patru „direcții”

`Lehrbuch` separă explicit:

1. **cantitatea reacției** — `Nullreaktion`, `Durchschnittsreaktion`, `Vollreaktion`;
2. **direcția / tendința reacției** — pozitivă, negativă, ambivalentă.

De aici rezultă o corecție de vocabular pentru manual:

- `+`, `−`, `±` sunt clasificări ale **direcției/tendinței**;
- `0` este **Nullreaktion**, nu o a patra direcție.

Pentru ansamblu folosim formularea sigură:

**cele patru forme / reacții factoriale de bază: `+`, `−`, `±`, `0`.**

Această separare pregătește cap. 14, unde cantitatea va fi tratată explicit prin `Vollreaktion`, `Überdruck`, `!`, `!!`, `!!!` și `Quantumspannung`.

---

## 3. Tabelle 3 — cele 28 de distribuții, corect clasificate

Notăm:

- `S` = alegeri simpatice;
- `A` = alegeri antipatice.

### Nullreaktionen — 4

`0/0, 1/0, 0/1, 1/1` → `0`.

### Reacții pozitive — 9

Forma de bază pozitivă cere `S >= 2` și `A <= 1`:

`2/0, 2/1, 3/0, 3/1, 4/0, 4/1, 5/0, 5/1, 6/0`.

Marcajele cantitative mature sunt:

- `2/0`, `2/1`, `3/0`, `3/1` → `+`;
- `4/0`, `4/1` → `+!`;
- `5/0`, `5/1` → `+!!`;
- `6/0` → `+!!!`.

### Reacții negative — 9

Simetric, `A >= 2` și `S <= 1`:

`0/2, 1/2, 0/3, 1/3, 0/4, 1/4, 0/5, 1/5, 0/6`.

Marcajele mature:

- `0/2`, `1/2`, `0/3`, `1/3` → `−`;
- `0/4`, `1/4` → `−!`;
- `0/5`, `1/5` → `−!!`;
- `0/6` → `−!!!`.

### Reacții ambivalente — 6

Ambele direcții ating minimum două alegeri:

`2/2, 3/2, 2/3, 3/3, 4/2, 2/4`.

Marcajele mature:

- `2/2`, `3/2`, `2/3`, `3/3` → `±`;
- `4/2`, `2/4` → `±!`.

Bilanțul explicit al lui Szondi este:

**4 null + 9 pozitive + 9 negative + 6 ambivalente = 28 variații.**

Acest bilanț coincide cu implementarea formală din `main/szondi3/scoring.py` și cu testul exhaustiv `tests/test_scoring.py`, care verifică toate cele 28 de distribuții după Tabelle 3.

---

## 4. Ce rămâne valid din Deri și ce trebuie corectat

Deri rămâne foarte utilă pedagogic pentru:

- explicația reacțiilor pozitive/negative ca dominanțe, nu ca acceptare/reprimare simplistă;
- avertismentul împotriva interpretării morale a semnelor;
- clarificarea reacției nule ca `open reaction` în vocabularul ei;
- prezentarea accesibilă a trecerii de la numărătoare la simbol.

Dar regula ei rezumativă de tip „cel puțin dublu” nu este suficientă ca algoritm exhaustiv pentru Tabelle 3.

**Contradicția relevantă există exact la `4/2` și `2/4`.**

Prin urmare, afirmația anterioară că „nu există contradicție relevantă Szondi–Deri” este retrasă. Pentru pragurile exacte, manualul urmează Szondi matur.

---

## 5. `+` și `−`: dominanță, nu puritate

Rămâne doctrinar și pedagogic valoroasă ideea:

**`+` și `−` exprimă dominanțe, nu puritate.**

`2/1` poate fi `+`, iar `1/2` poate fi `−`.

`Lehrbuch` numește persistența alegerii în direcția opusă **`Remanenz der Opposition`**.

Aceasta leagă direct cap. 13 de psihologia contrariilor din cap. 8:

**direcția dominantă nu șterge contrariul.**

Dar remanența nu trebuie convertită într-o regulă de raport. Când ambele direcții ating cel puțin două alegeri, reacția devine ambivalentă; de aceea `4/2` și `2/4` aparțin familiei `±`.

---

## 6. `±`: ambivalență și supraîncărcare

Reacția ambivalentă este dublu-direcționată: ambele tendințe sunt suficient de reprezentate.

Important pentru cap. 13:

- `±` nu înseamnă indecizie banală;
- nu înseamnă automat patologie;
- `4/2` și `2/4` arată că o reacție poate fi simultan **ambivalentă ca direcție** și **supraîncărcată cantitativ** (`±!`).

Acest caz este puntea cea mai bună spre cap. 14: direcția și cantitatea sunt axe distincte care se pot combina în același simbol.

---

## 7. `0`: Nullreaktion, nu factor absent

Distribuțiile nule sunt:

`0/0, 1/0, 0/1, 1/1`.

Anti-inferența rămâne obligatorie:

**`0` nu înseamnă că factorul nu există în persoană.**

În `Lehrbuch`, Szondi explică explicit că Nullreaktion nu înseamnă absența tendinței din constituția ereditară; în teoria sa, poate indica o descărcare temporară, satisfacere directă sau indirectă și, mai rar, slăbiciune constituțională.

Pentru cap. 13 se păstrează numai definiția formală și anti-inferența; sensurile dinamice ample rămân contextuale.

---

## 8. Puntea exactă spre cap. 14

Tabelle 3 arată că aceeași direcție de bază poate avea cantități diferite:

`2/0 → +`  
`4/0 → +!`  
`5/0 → +!!`  
`6/0 → +!!!`.

Și arată că supraîncărcarea nu este rezervată reacțiilor unidirecționale:

`4/2 → ±!`  
`2/4 → ±!`.

Așadar cap. 14 trebuie să răspundă:

**ce anume măsoară această încărcare cantitativă într-un singur profil și cum se codifică prin `!`?**

---

## 9. Distincția critică pentru cap. 14: Quantumspannung ≠ TspG

Această diferență trebuie fixată înainte de redactarea cap. 14.

### Quantumspannung

- privește **încărcarea cantitativă a unei reacții factoriale într-un profil**;
- în Tabelle 3 apare când una dintre direcții ajunge la 4, 5 sau 6 alegeri;
- este protocoalată prin `!`, `!!`, `!!!`;
- poate apărea și într-o reacție ambivalentă (`4/2`, `2/4` → `±!`).

### Tendenzspannungsgrad — TspG

- este o **măsură de serie**, nu a unei reacții singulare;
- se calculează după examinări repetate;
- pentru fiecare factor, Szondi însumează frecvențele reacțiilor `0` și `±` din serie;
- `TspG = Σ(Nullreaktionen) + Σ(ambivalente Reaktionen)` pentru factorul respectiv;
- este folosit ulterior în aparatul `Triebformel`, `Wurzelfaktor`, `TspD`, `Latenzproportionen` etc.

Implementarea din `main/szondi3/series.py` păstrează exact această separare: `factor_tension_degrees()` calculează TspG din numărul reacțiilor nule și ambivalente într-o serie, în timp ce `scoring.py` păstrează `quantum_level` la nivelul reacției dintr-un profil.

**Regulă editorială pentru cap. 14:** nu folosi `TspG` ca sinonim, explicație sau măsură alternativă pentru `Quantumspannung`. TspG aparține capitolelor despre serie (arhitectural cap. 41+).

---

## 10. Forward hold: `0` liber vs `ø` — Zwangs-Nullreaktion

Controlul cu implementarea formală din `main` confirmă o distincție care trebuie păstrată pentru capitolele despre complement și serie.

În EKP, dacă VGP a consumat deja **5 sau 6** dintre cele șase fotografii ale unui factor, pentru `Nachwahl` mai rămâne cel mult una sau niciuna. O reacție nulă poate apărea atunci din **constrângere numerică**, nu dintr-o alegere liberă.

Szondi marchează această reacție cu zero barat: **`ø` — Zwangs-Nullreaktion**.

`scoring.py` o marchează explicit prin `forced_null=True`, iar `series.py` refuză ca un astfel de `ø` să intre tacit în calculele de serie rezervate reacțiilor libere.

Această distincție trebuie reactivată la cap. 37 și/sau în partea de serie:

- `0` liber ≠ `ø` forțat;
- `ø` nu trebuie interpretat ca Nullreaktion liberă;
- `ø` nu intră fără regulă primară explicită în TspG/TspQu/%Sy-Re;
- distincția demonstrează concret teza cap. 11: **EKP este condiționat numeric de VGP.**

Nu este nevoie ca acest aparat să fie predat integral în cap. 13 sau 14.

---

## 11. Matrice 10/10 a corpusului canonic

| Sursă | Relevanță pentru cap. 13–14 | Funcție |
|---|---|---|
| `SCHICKSALSANALYSE` | control istoric | geneza reacțiilor; nu sursa finală pentru Tabelle 3 |
| `TRIEBPATHOLOGIE I` | relevantă | stabilizează vocabularul reacțiilor, Quantumspannung și dinamica încărcare–descărcare |
| `TRIEBPATHOLOGIE II` | control clinic | folosește frecvent `Quantumspannung` în sindromatică; nu redefinește tabelul formal |
| `ICH-ANALYSE I` | control doctrinar | utilizează `Quantumspannung` în teoria funcțiilor Eului |
| `ICH-ANALYSE II` | control doctrinar | idem; exemple de reacții cu supraîncărcare |
| `THERAPIE I` | periferic | profilele apar în context terapeutic; fără redefinirea formală centrală |
| `THERAPIE II` | periferic | control de continuitate |
| `LEHRBUCH` | **CENTRALĂ** | Tabelle 3; separarea cantitate/tendință; Null-/Durchschnitts-/Vollreaktion; `Quantumspannung`; ulterior definiția TspG de serie |
| `DERI` | tradiție pedagogică | explicații utile, dar regula 2:1 nu prevalează asupra Tabelle 3 la `4/2`, `2/4` |
| `MÉLON` | tradiție ulterioară / control | păstrează tensiunile factoriale și ulterior TspG; trebuie atribuit, nu folosit pentru a rescrie Szondi |

---

## 12. Anti-inferențe obligatorii

- `+` ≠ „bun”;
- `−` ≠ „rău”;
- `0` ≠ absența factorului;
- `±` ≠ automat patologie sau indecizie;
- semnul ≠ reacție la o singură fotografie;
- `4/2` ≠ `+`; `2/4` ≠ `−`;
- regula pedagogică 2:1 ≠ Tabelle 3 completă;
- `0` nu este o „direcție” în același sens cu `+ / − / ±`;
- direcția/tendința ≠ încărcarea cantitativă;
- `Quantumspannung` ≠ TspG;
- `0` liber ≠ `ø` forțat în EKP.

## Verdict de cercetare

**RESEARCH COMPLETE — CORRECTED.** Tabelle 3 din `Lehrbuch` este sursa normativă pentru clasificarea formală. Corecția `4/2, 2/4 → ±!` este obligatorie și a fost propagată în DRAFT și în controlul doctrinar.