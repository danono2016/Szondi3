# CH41 — Outline

**Capitol:** 41 — `TspG`, `TspD` și `Latenzproportionen`: de la factor la tensiunea vectorială  
**Statut:** OUTLINE COMPLETE / DRAFT NEXT  
**Bază:** `CH41_RESEARCH.md` — corpus pass 10/10 + bounded deep corpus pass + control vizual canonic al formulelor și exemplelor primare

---

## Întrebarea cognitivă

**Cum transformăm seria de reacții factoriale în opt `TspG`, apoi în patru diferențe intravectoriale și, în final, într-o ordine a celor patru grade de latență, fără să confundăm calculul cu profilul, cu `Quantumspannung` sau cu diagnosticul?**

## Teza capitolului

> **`TspG` agregă reacții în interiorul unui factor; `TspD` compară cei doi factori ai aceluiași vector; `Latenzproportionen` compară apoi cele patru diferențe vectoriale.**

Lanțul trebuie să rămână vizibil pe tot parcursul capitolului:

`reacții factoriale în serie -> TspG factorial -> TspD intravectorial -> Latenzgrad / Latenzgröße -> Latenzproportionen`

Formula epistemică de control:

> **calculul ordonează o serie; nu transformă seria într-un diagnostic.**

---

# Mișcarea capitolului

## 1. Deschidere — de la serie la mărime formală

Deschidere scurtă, fără recapitularea cap. 38–40.

Propunere de frază de intrare:

> **O serie poate fi numărată fără ca sensul ei să fie redus la număr.**

Cap. 40 a pus, când era nevoie, sumele unei serii scurte pe baza zece. Acum întrebarea este alta: **ce anume numărăm în fiecare factor și cum trecem de la opt factori la patru raporturi vectoriale?**

Nu intrăm încă în `Triebklasse`, `Unterklasse`, `Triebformel` sau `TspQu`.

## 2. Primul nivel: `TspG` factorial

Definiția trebuie introdusă direct din `Lehrbuch`:

- pentru fiecare factor, de-a lungul seriei, numărăm reacțiile `0`;
- numărăm reacțiile `±`;
- le adunăm;
- suma este `Grad der Tendenzspannung` — `TspG`.

Formula didactică:

> **`TspG(factor) = numărul reacțiilor 0 + numărul reacțiilor ± din seria considerată`.**

Clarificare imediată:

- `+` și `−` nu intră în această sumă;
- `!`, `!!`, `!!!` nu adaugă nimic la `TspG`;
- numărăm **tipuri de reacții factoriale**, nu alegeri sau „cantitatea” semnului.

## 3. De ce `0` și `±` apar împreună

Scurtă justificare doctrinară, fără a transforma teoria istorică în validare modernă:

- `±` face vizibilă ambivalența / dublarea tendințelor;
- `0` este tratat de Szondi ca reacție de descărcare și `postambivalente Reaktion`;
- de aici suma `± + 0`.

Păstrăm observația canonică:

- factorii simptomatici au `TspG` mai mare;
- `Wurzelfaktoren` au `TspG` mai mic.

Formula contraintuitivă care trebuie pregătită aici:

> **un `TspG` mic nu înseamnă automat factor „slab”; în doctrina lui Szondi, factorul cu `TspG` mai mic primește rang dinamic mai mare în calculul latenței.**

Nu anticipăm încă sistemul de clase din cap. 42.

## 4. `TspG ≠ Quantumspannung`

Secțiune scurtă, obligatorie pentru continuitatea cu cap. 33.

Separăm:

- `Quantumspannung` = încărcarea cantitativă a unei reacții, vizibilă prin `!`;
- `TspG` = frecvența serială a reacțiilor `0` și `±` ale unui factor.

Formula de control:

> **`TspG ≠ Quantumspannung`.**

Nu revenim la toată teoria `Quantumspannung`; o singură delimitare clară este suficientă.

## 5. `täglicher TspG` versus `faktorieller TspG`

Aici trebuie arătată arhitectura `Tendenzspannungstabelle` fără a reproduce încă întregul protocol de lucru din cap. 61:

- pe orizontală, pentru fiecare profil, pot fi calculate `Σ0`, `Σ±` și `täglicher TspG`;
- pe verticală, pentru fiecare factor, se calculează `Σ0`, `Σ±` și `faktorieller TspG`.

Pentru cap. 41 și pentru `TspD`, baza este:

> **`faktorieller TspG`.**

Protecție:

`sumă pe profil ≠ sumă pe factor de-a lungul seriei`.

## 6. Lungimea seriei și domeniul numeric

Scurtă secțiune menită să împiedice o extrapolare greșită din cap. 40:

- într-o serie de `N` profile, `TspG` brut poate varia între `0` și `N`;
- în `Zehnerserie`, maximul este 10;
- 10 nu este însă un plafon universal al `TspG`;
- exemplul canonic cu 15 profile arată o valoare de 13.

Concluzie:

> **baza zece este un standard de serie, nu limita matematică absolută a `TspG`.**

## 7. Al doilea nivel: `TspD`

Definiția trebuie predată mecanic, înaintea interpretării:

Pentru fiecare vector:

1. luăm cele două `TspG` factoriale;
2. scădem valoarea mai mică din cea mai mare;
3. rezultatul este `Tendenzspannungsdifferenz` — `TspD`.

Formula:

> **`TspD = TspG mai mare − TspG mai mic`.**

Există patru astfel de diferențe:

- S: h / s;
- P: e / hy;
- Sch: k / p;
- C: d / m.

## 8. Exemplul canonic și regula indexului

Exemplul principal:

- `TspG h = 9`;
- `TspG s = 2`;
- `TspD = 7`;
- factorul cu `TspG` mai mic este `s`;
- notația devine **`Ss / 7`**.

Apoi inversarea controlată:

- `h = 2`, `s = 9`;
- `TspD` rămâne `7`;
- notația devine **`Sh / 7`**.

Concluzia trebuie formulată puternic:

> **mărimea diferenței poate rămâne aceeași, dar factorul indexat se schimbă.**

și:

> **indexul aparține factorului cu `TspG` mai mic, nu celui cu valoarea mai mare.**

Aceasta este una dintre regulile pe care cititorul trebuie să le poată aplica fără ezitare după capitol.

## 9. `TspD` nu este o diferență temporală

Legătură strictă cu cap. 39:

- `Inkonstanzmethode` compară două profile / două momente;
- `TspD` compară doi factori parteneri ai aceluiași vector după agregarea întregii serii.

Formula de control:

> **diferență temporală între profile ≠ `TspD` intravectorial.**

Fără reluarea tehnicii Böszörményi/Janssen.

## 10. Ce nu spune un `TspD = 0`

Aceasta trebuie să fie secțiunea-limită a metricii.

Păstrăm exemplele canonice de configurații diferite care pot conduce la aceeași diferență zero:

- `++` / `−−`;
- `00`;
- `±±`;
- nota de subsol pentru `+−` / `−+`, unde Szondi vorbește despre `Triebentmischung`, nu `Trieblegierung`.

Concluzie:

> **aceeași valoare numerică nu identifică singură același `Vektorbild`.**

Aceasta protejează regula generală a manualului:

`calcul ≠ formă calitativă ≠ diagnostic`.

## 11. De la `TspD` la `Latenzgrad / Latenzgröße`

Terminologia trebuie păstrată flexibil, după sursă:

- `Tendenzspannungsdifferenz` = operația / diferența;
- valoarea localizată în vector apare ca `Latenzgrad` sau `Latenzgröße`;
- `Triebpathologie II` spune explicit `Latenzgrad oder Latenzgröße`.

Formula editorială:

> **`TspD` este diferența; valoarea ei localizată în vector este tratată de Szondi ca `Latenzgrad` / `Latenzgröße`.**

Nu construim o taxonomie terminologică mai rigidă decât corpusul.

## 12. Al treilea nivel: `Latenzproportionen`

După cele opt `TspG` și cele patru `TspD`, ordonăm cele patru grade de latență după mărime.

Flux vizual:

`8 TspG -> 4 TspD -> 4 Latenzgrade -> Latenzproportionen`

Exemplul canonic din `Lehrbuch`:

`Sh / 13 : Schp / 4 : Cm / 4 : P / 0`.

Acest exemplu trebuie folosit pentru trei lucruri simultan:

- valorile pot depăși 10;
- două grade pot fi egale;
- la diferență zero nu există obligatoriu un factor unic indexabil.

Apoi, ca reformulare matură, poate fi menționat scurt exemplul din `Triebpathologie II`:

`Schp− / 10 : Phy− / 6 : Sh+ / 6 : Cd+ / 3`.

Semnele `+ / −` ale factorului latent sunt doar anunțate; utilizarea lor clasificatorie aparține cap. 42.

## 13. Egalitățile rămân egalități

Regulă simplă:

- ordonăm după mărime;
- dacă două valori sunt egale, le păstrăm egale;
- nu inventăm un tie-break editorial;
- `Äqualität` și efectele asupra `Triebklasse / Unterklasse` rămân pentru cap. 42.

Această secțiune trebuie să fie scurtă, dar explicită.

## 14. Seria scurtă și `Tabelle 13` — audit focus protejat

Aceasta este singura secțiune care trebuie scrisă în draft cu statut epistemic vizibil.

### Ce avem direct

Din cap. 40:

- `Tabelle 13` convertește sumele reacțiilor din 3–9 profile la baza unei `angenommene Zehnerserie`;
- titlul tabelului leagă conversia de `Latenzproportion` și `Triebformel`.

Din ordinea `Trieblinnäus`:

- `faktorieller TspG` precede calculul `TspD`.

### Sinteza procedurală cea mai bine susținută

Pentru seria scurtă:

`sume factoriale 0 + ± -> Tabelle 13 -> TspG factorial convertit -> TspD -> Latenzproportionen`

Dar aceasta trebuie etichetată în draft ca **sinteză procedurală din două pasaje canonice**, nu ca propoziție citată textual din Szondi.

Protecție absolută:

> **nu convertim direct un `TspD` brut prin `Tabelle 13` fără control doctrinar extern.**

Motivul trebuie spus scurt: lookup-ul tabelului nu este liniar, deci ordinea operațiilor poate schimba numeric rezultatul.

**AUDIT FOCUS: CH41-SHORT-01.**

## 15. Tradiția ulterioară — numai cât ajută mecanica

Deri:

- explică foarte clar pedagogic `open + plus-minus -> T.sp.G. -> diferență -> Latenzgrösse -> Latenzproportionen`;
- confirmă indexarea prin factorul cu indice simptomatic mai mic;
- dar nu adoptă integral justificarea genetică a lui Szondi.

Mélon:

- confirmă aceeași mecanică;
- folosește `TspGD`, nu `TspD`.

Manualul păstrează notația primară Szondi:

> **`TspD`.**

Deri și Mélon rămân tradiție ulterioară explicit atribuită, nu sursă pentru rescrierea doctrinei primare.

## 16. Ce poate și ce nu poate face calculul

Poate:

- agrega reacțiile simptomatice ale fiecărui factor;
- compara factorii parteneri în interiorul vectorului;
- ordona cele patru grade de latență.

Nu poate, singur:

- înlocui `Vektorbild`;
- transforma `TspG` mic în „forță psihică obiectiv măsurată”;
- transforma `TspD` mare în severitate clinică;
- transforma `Latenzgrad` în probabilitate diagnostică;
- transforma `Latenzproportionen` într-un test psihometric modern autonom.

Formula finală de control revine o singură dată:

> **calculul ordonează o serie; nu transformă seria într-un diagnostic.**

## 17. Închidere spre cap. 42

Finalul trebuie să lase deschisă exact întrebarea următoare:

> **Dacă cele patru grade de latență sunt acum ordonate, ce statut primește vectorul cu cea mai mare latență și cum apar `Triebklasse`, `Unterklasse`, `Wurzelfaktor` și `Ventil`?**

Nu răspundem încă.

---

# Protecții obligatorii în draft

- `TspG = numărul reacțiilor 0 + numărul reacțiilor ±` pe factor, în serie;
- `TspG ≠ Quantumspannung`;
- `!` nu intră în calculul `TspG`;
- `faktorieller TspG`, nu `täglicher TspG`, intră în `TspD`;
- `TspG` brut depinde de lungimea seriei și poate depăși 10;
- `TspD = TspG mare − TspG mic` în interiorul aceluiași vector;
- indexul vectorului aparține factorului cu `TspG` mai mic;
- există patru `TspD`, câte unul pentru S/P/Sch/C;
- `TspD` intravectorial ≠ diferență temporală;
- `TspD = 0` nu definește singur un `Vektorbild`;
- `Latenzgrad / Latenzgröße` rămân termenii sursei, fără rigidizare artificială;
- `Latenzproportionen` ordonează cele patru grade de latență;
- egalitățile rămân egalități; fără tie-break inventat;
- notația primară a manualului este `TspD`, nu `TspGD`;
- Deri/Mélon sunt tradiție ulterioară;
- `Triebklasse / Unterklasse` rămân pentru cap. 42;
- `Triebformel` rămâne pentru cap. 43;
- `TspQu` rămâne pentru cap. 44;
- **CH41-SHORT-01** rămâne audit focus explicit: `sume factoriale -> Tabelle 13 -> TspD` este sinteza procedurală cea mai bine susținută, dar nu trebuie prezentată ca propoziție canonică unică și nu se autorizează conversia directă a unui `TspD` brut fără recheck extern.

---

# Ritm stilistic

Capitolul trebuie să fie tehnic, dar să avanseze în trei trepte clare:

`factor -> vector -> relația dintre vectori`.

Ideal, fiecare treaptă introduce:

1. operația;
2. un exemplu;
3. limita acelei operații.

Mișcare recomandată:

`TspG -> exemplu -> TspD -> index -> TspD=0 -> Latenzgrad -> Latenzproportionen -> seria scurtă -> limite -> punte spre clase`.

Evitat:

- recapitularea excesivă a cap. 39–40;
- explicarea prematură a `Triebklasse`;
- transformarea fiecărei delimitări într-o secțiune defensivă lungă;
- limbajul de „scor clinic” sau „severitate”.

---

## Următorul pas

**DRAFT v1 — NEXT.**
