# Capitolul 43 — `Triebformel`: formula abreviată, formula completă și limitele calculului

**Statut:** DRAFT v2 — EXTERNAL DOCTRINAL REVISION INTEGRATED / RECHECK REQUIRED / CH43-AUDIT-01 CONFIRMED/CLOSED / CH43-NOTATION-01 CONFIRMED/CLOSED / CH43-ABBR-01 SOURCE/PROCEDURE HOLD ACTIVE / CH43-SHORT-01 SOURCE CONFLICT HOLD ACTIVE  
**Notă editorială:** revizie punctuală integrată după auditul doctrinar extern al DRAFT v1. Formula abreviată nu mai este prezentată ca deducție mecanică din extreme; rangul psihodiagnostic revendicat istoric de Szondi este restituit explicit; redarea `Tabelle 13` nu mai atribuie tabelului o celulă `0->0` netipărită. Nu există încă `DOCTRINAL PASS`, `SCIENTIFIC AUDIT CLOSED`, reader pass sau `STABLE DRAFT`.

---

O `Triebklasse` nu este încă o `Triebformel`.

Clasa ne-a spus unde se concentrează rădăcina și `Triebgefahr`; formula încearcă să individualizeze mai fin cum se distribuie, în seria actuală, factorii simptomatici, factorii intermediari și factorii-rădăcină.

Szondi exprimă această diferență printr-o pereche foarte precisă:

`Triebklasse = genus proximum`  
`Triebformel = differentiae specificae`.

Cu alte cuvinte, clasa apropie cazul de un gen formal; formula introduce diferențele specifice din interiorul acelui gen.

## Materia formulei: cei opt `TspG` factoriali

Punctul de plecare îl constituie cei opt `TspG` factoriali ai seriei:

`h, s, e, hy, k, p, d, m`.

Capitolul 41 a fixat operația:

`TspG = Σ0 + Σ±`.

Aici nu reluăm sensul `TspG`; folosim rezultatul. Cei opt factori sunt puși într-o **ordine globală** după mărimea `TspG`-ului lor.

Lanțul este:

`8 TspG factoriale -> rang global -> pol simptomatic / nivel intermediar / pol de rădăcină -> Triebformel`.

Această ordonare globală trebuie separată de calculul vectorial din capitolul anterior. În `Triebklasse`, factorul cu `TspG` mai mic dintr-o pereche vectorială poate da `Wurzelfaktor`-ul clasei. În `Triebformel`, însă, **toți cei opt factori sunt comparați între ei**.

**`Wurzelfaktor` vector-local nu devine automat denominatorul global al `Triebformel`.**

## Polul simptomatic: `Symptomfaktoren`

În mecanica formulei, la polul valorilor mari de `TspG` apar `Symptomfaktoren`.

Aceștia sunt factorii în care, de-a lungul seriei, apar constant sau aproape constant reacții `0` și `±`. Tocmai aceste reacții intră în suma `TspG`, astfel încât acumularea lor împinge factorul spre partea superioară a rangului.

Szondi distinge istoric reacțiile `±` ca simptome mai curând „interioare” sau „subiective” și reacțiile `0` ca simptome mai curând „exterioare” sau „obiective”. Această distincție aparține limbajului său teoretic; ea nu transformă `0` sau `±` într-un diagnostic de sine stătător.

`Symptomfaktor` este, aici, o poziție în organizarea serială a factorilor. Nu este echivalent cu un diagnostic clinic.

## Polul de rădăcină: `Wurzelfaktoren`

La celălalt pol se află factorii cu `TspG` mic, adică factorii în care predomină reacțiile persistente `+` sau `−`. În vocabularul lui Szondi, aceștia sunt `Wurzelfaktoren` sau `Konduktorfaktoren` ai formulei.

Sensul lor doctrinar este legat de trebuințe care rămân nesatisfăcute. Dar semnul nu trebuie redus la o singură cauză psihologică.

O reacție `−` nu înseamnă automat numai `Verdrängung`; Szondi admite și `Verzicht` sau `Anpassung`. Invers, nici `+` nu garantează satisfacerea trebuinței: o direcție afirmativă poate persista tocmai acolo unde satisfacerea nu se realizează.

Termenul `Wurzelfaktor` păstrează aici sensul istoric al doctrinei lui Szondi. Formula nu demonstrează prin ea însăși o etiologie genetică modernă.

## Două operații înrudite sub numele de `Wurzelfaktor`

Este util să fixăm diferența înainte de a construi formula.

În capitolul 42, operația era **vector-locală**: în fiecare pereche, factorul cu `TspG` mai mic indexa `TspD`; în clasa conducătoare, acest factor putea deveni rădăcina clasei.

În `Triebformel`, operația este **globală**: cei opt factori sunt puși într-un singur rang, iar stratul inferior al acelui rang formează `Wurzelfaktoren` formulei.

De aceea denominatorul formulei nu se obține prin simpla copiere a celor patru indici vectoriali.

Fall 11 face vizibilă această diferență.

## Formula abreviată: `Bruchformel`

Forma abreviată este o fracție de orientare. În definiția sigură a sursei, la numărător apar `Leitbuchstaben` ale `Symptomfaktoren`, iar la numitor `Leitbuchstaben` ale `Wurzelfaktoren`.

Szondi precizează că această formă servește **`nur zur raschen Orientierung`** — numai pentru orientare rapidă.

În Fall 11, ordinea celor opt `TspG` este:

`m=8, d=5, k=5, p=4, e=4, hy=2, h=2, s=1`.

Formula abreviată tipărită este:

```text
m₈
──
s₁
```

Fall 11 arată limpede relația dintre polul simptomatic și polul de rădăcină, dar nu autorizează singur o regulă universală de tip „ia maximul/maximele și minimul/minimele”. Alte cazuri canonice împiedică această simplificare: Fall 12 tipărește `s/h`, deși `p` și `h` sunt ambele la `TspG = 0`; Fall 16 dă două fracții, `e/d` și `e/m`; Fall 18 tipărește două forme, `k/s` și `kp/hs`.

Prin urmare, formula abreviată poate fi definită sigur prin funcția factorilor selectați, nu printr-un algoritm universal de selecție dedus editorial din extreme.

> **CH43-ABBR-01 — SOURCE/PROCEDURE HOLD ACTIVE**  
> `Triebformel` abreviată selectează `Symptomfaktoren` și `Wurzelfaktoren` pentru orientare rapidă, dar materialul canonic controlat nu autorizează un algoritm universal simplu care să deducă pentru orice serie selecția exactă numai din maximul/maximele și minimul/minimele `TspG`.

## Formula completă: `mehrfache Bruchformel`

Forma completă introduce un al treilea nivel și devine o **`mehrfache Bruchformel`**.

Ea ordonează factorii pe trei linii funcționale:

1. sus — `Symptomfaktoren`;
2. la mijloc — factorii `submanifest / sublatent`;
3. jos — `Wurzelfaktoren`.

Linia mediană nu este un rest aritmetic. Szondi îi atribuie un rang propriu și spune că factorii de aici pot condiționa frecvent „tema interesului”. În anumite tabele `Trieblinnäus`, factorii mediani sunt omişi pentru simplificare, dar aceasta nu îi scoate din formula completă construită din serie.

### Fall 11: cele trei niveluri

Pentru rangul:

`m=8, d=5, k=5, p=4, e=4, hy=2, h=2, s=1`,

formula tipărită separă:

- sus: `m₈`;
- mijloc: `d₅, k₅, p₄, e₄`;
- jos: `hy₂, h₂, s₁`.

Păstrând semnele și indicii controlați vizual în PDF, structura poate fi redată schematic astfel:

```text
                  ± 0
                   m₈
        ─────────────────────
 + 0        + 0        + ±        − 0
 d₅         k₅         p₄         e₄
        ─────────────────────
 +           −!          −!!
 hy₂         h₂          s₁
```

Aici se vede imediat ceea ce forma abreviată ascunde: între factorul simptomatic conducător și rădăcina extremă există o zonă intermediară reală, iar polul de rădăcină însuși poate conține mai mulți factori.

## Regula diferenței `TspG <= 2`

`Lehrbuch` adaugă o regulă explicită: factorii puși pe aceeași linie a `Triebformel` au între `TspG`-urile lor o diferență care nu depășește 2.

Regula trebuie păstrată. Dar ea nu trebuie transformată într-un algoritm matematic mai rigid decât sursa.

Fall 11 arată de ce. Valorile `5, 5, 4, 4` formează linia mediană, iar `2, 2, 1` linia inferioară. În același timp, textul metodologic descrie linia superioară prin factorii simptomatici cu cele mai mari valori, iar exemplul tipărit are aici un singur factor conducător, `m₈`.

Manualul păstrează deci împreună:

- rangul global al celor opt valori;
- cele trei funcții — simptomatică, intermediară, de rădăcină;
- regula textuală `diferență TspG <= 2` pentru factorii aflați pe aceeași linie;
- exemplul canonic așa cum este tipărit.

Nu deducem de aici un procedeu universal de clustering pentru orice șir numeric posibil.

## Ce păstrează notația formulei

`Triebformel` nu este doar o listă de litere.

În notația canonică pot apărea:

- litera factorului;
- tipul sau direcția reacției caracteristice: `0`, `±`, `+`, `−`;
- încărcările `!`, atunci când sunt prezente;
- indicele numeric relevant al seriei;
- poziția factorului pe unul dintre cele trei niveluri.

În `Triebpathologie II`, Szondi explică suplimentar că pentru `Symptomfaktoren` se notează reacția simptomatică și frecvența ei, iar pentru `Wurzelfaktoren` direcția reacției și frecvența descărcării.

Din acest motiv, notația nu trebuie reconstruită aproximativ din text layer. **Semnele, indicii, încărcările și liniile fracției se controlează vizual în PDF-ul canonic.**

## Ce adaugă formula față de clasă

Putem reveni acum la distincția de la început:

`Triebklasse = genus proximum`  
`Triebformel = differentiae specificae`.

Clasa localizează domeniul principal al rădăcinii și al `Triebgefahr`. Formula păstrează rădăcina, dar adaugă:

- `Symptomfaktoren`;
- factorii `submanifest / sublatent`;
- distribuția globală a celor opt factori;
- configurația `Notausgänge / Triebventile` în vocabularul lui Szondi.

Numărătorul formulei arată tocmai factorii prin care tensiunea își găsește căi simptomatice de ieșire. Aceasta nu înseamnă că `Notausgang` este o „resursă sănătoasă”; canalul de descărcare poate fi simptomatic.

**`Triebklasse` spune unde este rădăcina dominantă; `Triebformel` arată prin ce configurație de factori simptomatici și intermediari se individualizează ieșirea din acea tensiune.**

## Rangul psihodiagnostic revendicat de Szondi

Limita contemporană a manualului nu trebuie să șteargă rangul pe care Szondi însuși îl atribuie metodei.

În `Lehrbuch`, analiza `Triebformel` este folosită pentru stabilirea caracterului unei `Triebnatur` sănătoase sau bolnave și pentru raportul dintre simptom și satisfacția pulsională ratată. Împreună cu `Triebklasse`, în cadrul `Trieblinnäus`, Szondi o folosește pentru determinarea `Triebnatur`, a `Charakter`-ului și a `Krankheitsform`. Fall 12 arată chiar succesiunea practică: formula abreviată, apoi formula completă căutată în tabel, urmate de formularea unei diagnoze.

Acesta este **rangul psihodiagnostic revendicat istoric de Szondi pentru metodă**. Manualul îl consemnează ca atare; nu îl transformă în validare clinică contemporană și nici într-o permisiune de a diagnostica mecanic din fracție.

Sursa însăși oferă și limita internă a unei asemenea pretenții. În `Triebpathologie II`, Szondi poate admite explicit, despre un caz: **`Die experimentelle Triebdiagnose war demnach falsch.`** Faptul că metoda primește la Szondi o funcție diagnostică istorică nu înseamnă că rezultatul experimental este infailibil și cu atât mai puțin că manualul îl poate trata drept diagnostic clinic autonom.

## Aceeași clasă, formule diferite

`Triebformel` nu repetă pur și simplu clasa.

`Triebpathologie II` arată că, în interiorul aceleiași `Triebklasse`, formula poate diferenția configurații în care pericolul apare prin `Unitendenz` de configurații în care apare prin `Tritendenz`.

Prin urmare:

**Aceeași `Triebklasse` nu implică aceeași `Triebformel` și nici aceeași geometrie vectorială.**

Formula adaugă specificitate, dar nu suspendă lectura `Vektorbilder`, a profilelor individuale și a succesiunii lor în serie.

## Formula este actuală și mobilă

La fel ca `Triebklasse`, `Triebformel` are caracter actual.

Szondi descrie treceri precum:

`Symptomfaktor -> Wurzelfaktor`  
`Wurzelfaktor -> Symptomfaktor`  
`Symptomfaktor <-> submanifest`.

În această dinamică vorbește despre o relativă `Umweltstabilität` a direcțiilor și a calității schimbării. „Relativă” este termenul important: formula nu este tratată ca o structură imuabilă.

**`Triebformel` descrie o configurație serială actuală, nu un tip fix de personalitate.**

## Seria scurtă: conflictul pe care calculul nu îl poate decide

Pentru o `Zehnerserie`, mecanica de mai sus poate fi predată fără ambiguitate majoră. Pentru seriile de 3–9 profile apare însă aceeași tensiune de sursă întâlnită, sub altă formă, în capitolul 41.

Instrucțiunile Schafir–Szondi spun că anumite rezultate pot fi utilizate înainte de profilul 10 numai după `Umrechnung`. Mai mult, titlul tabelului este explicit:

**`Tabelle 13. Zur Umrechnung der Zahlen der Latenzproportion und der Triebformel`.**

Pentru șase profile, coloana tipărită a tabelului dă:

`1->2, 2->3, 3->5, 4->7, 5->8, 6->10`.

Rândul `0` nu este tipărit în `Tabelle 13`; prin urmare manualul nu atribuie tabelului o celulă `0->0`.

Dar Fall 18 are tot șase profile și tipărește următoarele `TspG` brute:

`h=1, s=0, e=2, hy=2, k=5, p=4, d=3, m=3`.

Rangul folosit pentru `Triebformel` este tipărit direct cu aceste valori:

`k=5, p=4, m=3, d=3, hy=2, e=2, h=1, s=0`.

Dacă s-ar aplica valorilor nenule conversiile tipărite din `Tabelle 13`, iar valoarea nulă ar fi păstrată doar ca o consecință operațională de lucru — nu ca o celulă tipărită a tabelului — setul comparativ ar deveni:

`h=2, s=0, e=3, hy=3, k=8, p=7, d=5, m=5`.

Indicii formulei ar fi deci alții decât cei tipăriți în Fall 18.

> **CH43-SHORT-01 — SOURCE CONFLICT HOLD ACTIVE**  
> Pentru seriile 3–9, manualul nu autorizează universal nici `TspG brut -> Tabelle 13 -> Triebformel`, nici `TspG brut -> Triebformel fără Umrechnung`.

Acest conflict este înrudit cu `CH41-SHORT-01`, dar obiectul lui imediat este aici construcția și notația `Triebformel`. Nu există motiv să redeschidem capitolul 41 și nici dreptul de a alege o regulă pe care sursa nu o stabilește neechivoc.

## Formula abreviată înainte de profilul 10

În aceeași secțiune, Schafir formulează concluzii despre momentul în care formula abreviată poate deveni utilizabilă sau constantă.

În rezumat:

- la 3–4 profile sunt cerute condiții explicite de repetare și continuitate;
- la 5 profile apare o diferențiere între cazurile bolnave și cele normale în concluziile lui Schafir;
- la 6–7 profile `abgekürzte Triebformel` este declarată constantă;
- la 8 profile este afirmată constanța întregului `Trieblinnäus`.

Acestea sunt concluziile lui Schafir reproduse de Szondi. Ele nu rezolvă însă conflictul numeric de `Umrechnung`: una este afirmația de stabilitate a unei forme, alta este întrebarea ce valori trebuie înscrise efectiv în formulă.

## Deri și Mélon: două straturi ulterioare

Deri explică foarte clar distribuția relativă între factorii simptomatici, intermediari și de rădăcină. În prezentarea ei, însă, spune că nu dispune de o regulă exactă pentru numărul factorilor de pe fiecare rând și nici de un prag absolut care să decidă trecerea dintre rânduri.

`Lehrbuch` ulterior are prioritate pentru mecanica tehnică matură: formula abreviată și completă, cele trei linii și regula diferenței `TspG <= 2`.

Mélon propune mai târziu o simplificare pedagogică prin praguri absolute, cu factor simptomatic la valori `>5` și factor-rădăcină la valori `<3`. Manualul nu transformă aceste praguri într-un algoritm canonic primar, deoarece acesta nu este modul în care `Lehrbuch` definește formula completă.

## Un protocol sigur pentru `Zehnerserie`

Pentru domeniul neambiguu al seriei de zece, traseul de lucru poate fi rezumat astfel:

1. preia cei opt `TspG` factoriali;
2. ordonează-i global, păstrând egalitățile;
3. identifică polul simptomatic și polul de rădăcină în termenii sursei;
4. pentru formula abreviată, păstrează principiul `Symptomfaktoren / Wurzelfaktoren` și folosește selecția efectiv documentată de sursă; nu deduce universal combinația exactă numai din extremele `TspG`;
5. pentru formula completă, păstrează cele trei niveluri — simptomatic / `submanifest-sublatent` / rădăcină — și regula textuală `diferență TspG <= 2` pentru factorii de pe aceeași linie, fără să inventezi un clustering exhaustiv;
6. adaugă reacția caracteristică, încărcările și indicii după notația canonică controlată vizual;
7. păstrează rangul real al liniei mediane chiar dacă unele tabele ulterioare o omit;
8. oprește-te înainte de `TspQu / % Sy-Re`.

Acest protocol nu rezolvă `CH43-ABBR-01`. Pentru seriile 3–9, el se oprește suplimentar la `CH43-SHORT-01`.

## Limitele calculului

`Triebformel` poate comprima distribuția serială a celor opt factori, poate separa polul simptomatic de nivelul intermediar și de rădăcină și poate individualiza, în doctrina lui Szondi, raportul dintre `Wurzelfaktoren` și `Notausgänge`.

În doctrina istorică a lui Szondi, formula primește și o funcție psihodiagnostică și caracterologică în cadrul `Trieblinnäus`. Această revendicare trebuie păstrată în istoria internă a metodei.

Dar această comprimare nu transformă formula, pentru manualul clinic contemporan, într-un diagnostic autonom. `Symptomfaktor` nu devine prin nume o entitate nosologică, `Wurzelfaktor` nu devine dovadă genetică, iar `Notausgang` nu devine automat resursă sănătoasă. Formula nu înlocuiește `Vektorbild`, profilul sau seria și nu rezolvă contradicțiile sursei prin simplul fapt că produce o notație ordonată.

**Calculul comprimă distribuția serială a factorilor; nu produce singur etiologie, diagnostic sau prognostic clinic.**

## Spre indicii globali ai seriei

Cu `Triebformel`, am trecut de la opt valori factoriale la o structură care le distribuie între simptom, nivel intermediar și rădăcină.

Dar această formulă nu este ultimul calcul al seriei.

Pasul următor nu mai întreabă cum sunt ordonați factorii în fracție, ci ce informație adaugă indicii globali ai seriei. Aici începe capitolul 44: `TspQu` și `% Sy-Re`.
