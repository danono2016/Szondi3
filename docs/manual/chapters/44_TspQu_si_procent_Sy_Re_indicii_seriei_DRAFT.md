# Capitolul 44 — `TspQu` și `% Sy-Re`: indicii seriei

**Statut:** STABLE DRAFT — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CH44-AUDIT-01 CONFIRMED/CLOSED / CH44-AUDIT-02 CONFIRMED/CLOSED / CH44-ROUND-01 SOURCE/PROCEDURE HOLD ACTIVE  
**Notă editorială:** recheck-ul stilistic extern integral al DRAFT v3 a acordat `STYLE PASS — READY FOR STABLE DRAFT.` Capitolul este stabil doctrinar și stilistic. `CH44-AUDIT-01` și `CH44-AUDIT-02` sunt confirmate/închise. `CH44-ROUND-01` rămâne SOURCE/PROCEDURE HOLD ACTIVE ca limită documentată a sursei și nu este rezolvat prin stabilizare.

---

După `Triebformel`, seria poate fi comprimată încă în două mărimi globale. Ambele pornesc de la aceleași reacții — `0` și `±` — dar răspund la întrebări diferite.

`TspQu` întreabă cum se împart între ele reacțiile `0` și `±`.

`% Sy-Re` întreabă cât reprezintă împreună aceste reacții din totalul reacțiilor factoriale ale seriei.

Cele două formule se citesc împreună, fără a fi confundate:

`TspQu = Σ0 / Σ±`

`% Sy-Re = ((Σ0 + Σ±) × 100) / (8 × N)`

unde `N` este numărul de profile din serie.

În vocabularul lui Szondi, reacțiile `0` și `±` sunt numite `Symptomreaktionen`. Termenul are aici rang formal-testologic: nu înseamnă că fiecare reacție nulă sau ambivalentă este, prin ea însăși, un simptom clinic observabil.

> **`TspQu` descrie compoziția reacțiilor simptomatice; `% Sy-Re` descrie cât spațiu ocupă ele în întreaga serie. Niciunul nu suspendă lectura calitativă a profilelor.**

## Materia de intrare: `Σ0`, `Σ±` și lungimea seriei

Pentru cei doi indici avem nevoie de trei date:

- `Σ0` — numărul total al reacțiilor factoriale `0` din serie;
- `Σ±` — numărul total al reacțiilor factoriale `±` din serie;
- `N` — numărul de profile ale seriei.

Fiecare profil conține opt reacții factoriale — câte una pentru `h, s, e, hy, k, p, d, m`. O serie de `N` profile conține deci `8 × N` reacții factoriale. În `Zehnerserie` avem `10 × 8 = 80`.

Aceste numărări privesc reacțiile factoriale. Nu sunt numărări ale portretelor alese și nu însumează încărcările `!`.

## `TspQu`: raportul `0 / ±`

Denumirea completă este `Tendenzspannungsquotient`.

Formula canonică este:

`TspQu = Σ0 / Σ±`.

Numărătorul spune câte reacții nule apar în serie. Numitorul spune câte reacții ambivalente apar. Quotientul compară aceste două frecvențe între ele; nu le raportează la totalul de 80 sau la `8 × N`.

`TspQu` este un quotient global al seriei; nu este procent și nu se confundă cu `TspG`, `TspD` sau `Quantumspannung`.

Apropierea terminologică dintre `Tendenzspannungsquotient`, `Tendenzspannung` și `Quantumspannung` nu autorizează contopirea operațiilor.

## Ce păstrează și ce pierde `TspG`

Capitolul 41 a definit, pentru fiecare factor:

`TspG(f) = Σ0_f + Σ±_f`.

Dacă însumăm cei opt `TspG` factoriali, obținem:

`Σ_f TspG(f) = Σ0 + Σ±`.

Aceasta este o echivalență aritmetică derivată din definiții, nu o formulă suplimentară atribuită textual lui Szondi.

Suma celor opt `TspG` păstrează **cantitatea totală** de reacții `0 + ±`, deci poate furniza numărătorul lui `% Sy-Re`. Dar ea nu mai păstrează **separarea** dintre `0` și `±`.

Prin urmare, din cei opt `TspG` nu putem reconstrui `TspQu` dacă nu mai avem separat `Σ0` și `Σ±`.

Un exemplu simplu arată de ce. Două serii pot avea același total `Σ0 + Σ± = 40`, dar una poate avea `30/10`, iar alta `20/20`. Procentul total al reacțiilor simptomatice ar fi același dacă lungimea seriilor este aceeași; `TspQu` ar fi însă diferit.

> **Cantitatea `0+±` nu conține automat informația despre raportul `0/±`.**

## Când `Σ± = 0`

`Triebpathologie II` oferă un caz în care nu apare nicio reacție ambivalentă. Szondi tipărește explicit:

`Σ0 / Σ± = 31 / 0 = ∞`.

Așadar, pentru `Σ± = 0` și `Σ0 > 0`, simbolul `∞` nu este o convenție adăugată de manual; apare în sursa canonică.

Cazul formal în care `Σ0 = 0` și `Σ± = 0` este diferit. Raportul `0/0` este matematic nedefinit, iar în corpusul controlat nu a fost identificată o interpretare psihologică szondiană pentru această situație. Manualul nu completează această absență prin inferență.

## Ce spune Szondi despre mărimea `TspQu`

În `Lehrbuch`, Szondi leagă quotientul de raportul dintre reacțiile nule, pe care le numește istoric simptome „exterioare”, și reacțiile ambivalente, numite simptome „interioare”. Pe această bază propune câteva repere pentru `Verhalten / Behaviour`:

- la `TspQu < 1`, conduite descrise ca `gehemmt`, `zwangsartig`, adesea `gebremst`;
- la valori `1, 2, 3`, comportamentul poate fi relativ nefrapant, chiar dacă persoana poate fi psihic bolnavă;
- la `TspQu > 5`, uneori chiar peste 10, Szondi descrie conduite excitate, nefrânate, `agiert`.

Aceste repere nu alcătuiesc un clasificator exhaustiv. Sursa nu furnizează un tabel continuu în care fiecare interval numeric primește un sens stabil.

Corpusul primar păstrează și trei repere numerice apropiate, dar aparținând unor contexte diferite:

- `1–3` — `Schwankungsbreite` atribuită de Szondi persoanelor numite `Triebgesunde`;
- `1,6–2,5` — observația colectivă/de dezvoltare legată de `Tabelle 15`, pentru intervalul de vârstă 3–90 de ani;
- `1,5–2,5` — formularea `normal: 1,5–2,5` întâlnită într-un caz din `Triebpathologie II`.

Cele trei repere provin din contexte diferite și nu autorizează construirea unei norme unice.

Mai important, `Lehrbuch` cere ca mărimea quotientului să fie readusă în configurația calitativă a profilului. Inhibiția poate proveni din mecanisme diferite, iar reacții precum `−hy`, `−k` sau `±k` pot modifica sensul comportamental al unui quotient mai mare. Invers, un quotient mic nu garantează prin el însuși o conduită liniștită.

> **Comportamentul nu se deduce numai din mărimea `TspQu`.**

## `% Sy-Re`: procentul reacțiilor simptomatice și lungimea seriei

Al doilea indice nu mai compară `0` cu `±`, ci întreabă cât reprezintă împreună aceste două clase în totalul reacțiilor factoriale.

Formula canonică este:

`% Sy-Re = ((Σ0 + Σ±) × 100) / (8 × N)`.

Într-o `Zehnerserie`, denominatorul este 80. Exemplul didactic din `Lehrbuch` pornește de la 33 de reacții simptomatice:

`33 / 80 × 100 = 41,25%`.

Sursa tipărește:

`% Sy-Re = 41%`.

Dacă seria are altă lungime, denominatorul urmărește numărul real de profile. La opt profile sunt `8 × 8 = 64` reacții factoriale; la șapte, `7 × 8 = 56`. Procentul se calculează din totalul real disponibil.

Această operație este diferită de `Tabelle 13`. Tabelul transforma anumite numărări ale seriilor de 3–9 profile într-o `angenommene Zehnerserie` pentru domeniile indicate de titlul său. Pentru `% Sy-Re`, Szondi prescrie direct denominatorul corespunzător numărului efectiv de profile.

> **Normalizarea procentuală la `8 × N` nu este `Umrechnung` prin `Tabelle 13`.**

Titlul canonic al `Tabelle 13` menționează `Latenzproportion` și `Triebformel`, nu `TspQu` sau `% Sy-Re`. Pentru `TspQu`, corpusul controlat nu oferă o instrucțiune de conversie prin acel tabel înaintea calculării raportului `Σ0/Σ±`.

Problemele de `Umrechnung` întâlnite la `TspD` și `Triebformel` nu se transferă automat asupra acestor doi indici.

## Reperul istoric `20–30%`

Pentru `% Sy-Re`, `Lehrbuch` oferă reperul:

`20–30%`.

Formularea germană este importantă: `Empirisch wurde die Normalgröße der prozentualen Symptomreaktion vorderhand zwischen 20% und 30% gefunden.`

`Vorderhand` păstrează caracterul provizoriu al afirmației. În alte straturi ale corpusului, formularea poate deveni mai categorică; `Triebpathologie II`, de pildă, poate vorbi despre `Norm` în aceeași bandă. Diferența de ton trebuie păstrată.

`20–30%` rămâne astfel un **reper empiric istoric al lui Szondi**, nu o normă psihometrică contemporană. Chiar `Lehrbuch` avertizează că acești indici nu sunt suficienți singuri pentru stabilirea unei diagnoze clinice; pot funcționa cel mult ca `Wegweiser` într-o interpretare mai largă.

## De ce `TspQu` și `% Sy-Re` trebuie citite împreună

Szondi cere explicit ca `% Sy-Re` să fie evaluat ținând seama de `Tendenzspannungsquotient`.

Motivul se vede direct în formule:

- `TspQu` spune **cum se împart** reacțiile simptomatice între `0` și `±`;
- `% Sy-Re` spune **cât de multe** reacții `0+±` există în raport cu întreaga serie.

Cele două dimensiuni nu se determină reciproc.

Un exemplu canonic din `Triebpathologie II`, într-un caz de nevroză obsesională, face diferența clară:

`Σ0 = 26`

`Σ± = 28`

`TspQu = 26/28 ≈ 0,9` — valoarea tipărită în sursă.

Masa totală a reacțiilor simptomatice este însă `26 + 28 = 54`, iar într-o serie de zece profile:

`54/80 × 100 = 67,5%`.

Așadar, un quotient mic poate coexista cu un procent foarte mare de reacții simptomatice.

`Lehrbuch` oferă și contraponderea istorică: în tulburările circulare, raritatea reacțiilor `±` poate ridica `TspQu`, în timp ce procentul total al reacțiilor simptomatice rămâne relativ mic.

> **Raportul `0/±` și cantitatea totală `0+±` sunt două întrebări diferite.**

## Fall 62: cei doi indici în aceeași serie

Fall 62 din `Lehrbuch` permite controlul simultan al ambelor formule. În foaia canonică sunt tipărite:

`Σ0 = 23`

`Σ± = 12`

Prin urmare:

`23/12 = 1,91666...`

Sursa tipărește:

`TspQu = 1,9`.

Totalul reacțiilor simptomatice este `23 + 12 = 35`, iar pentru 80 de reacții factoriale:

`35/80 × 100 = 43,75%`.

Sursa tipărește:

`% Sy-Re = 43,7%`.

Exemplul arată și că precizia zecimală nu este uniformă în corpus.

## Precizia numerică: formula este clară, regula de afișare nu

Mai multe exemple canonice produc un tablou neuniform:

- `33/80 × 100 = 41,25%`, tipărit `41%`;
- `35/80 × 100 = 43,75%`, tipărit `43,7%`;
- `23/12 = 1,916...`, tipărit `1,9`;
- în Fall 1 din `Triebpathologie I`, `25/14 = 1,785714...`, tipărit `1,78`;
- `26/28 = 0,92857...`, tipărit `0,9`.

Aceste cazuri pot sugera în mai multe locuri o tăiere a zecimalelor, dar corpusul controlat nu enunță o regulă universală de rotunjire și nici un număr fix de zecimale.

Manualul separă formula de problema afișării:

- formula se calculează exact;
- când reproduce un caz canonic, păstrează valoarea tipărită în sursă;
- dacă realizează un calcul nou și afișează o valoare zecimală, precizia folosită este o convenție editorială declarată, nu o regulă atribuită lui Szondi.

> **Limită de procedură.** Sursa nu oferă o convenție universală de rotunjire care să poată fi predată ca regulă canonică.

## `TspQu` al unei serii și curba `TspQu` între serii

În `Lehrbuch`, Szondi urmărește `TspQu` și prin serii repetate, construind ceea ce numește o `Jahreskurve`. Nu mai avem atunci un singur quotient, ci o succesiune de quotiente calculate separat din mai multe serii.

Trebuie păstrate trei niveluri distincte:

`TspQu al unei serii ≠ curba TspQu între serii ≠ Inkonstanzmethode`.

`Inkonstanzmethode` compară schimbări între profile. Curba `TspQu` urmărește, în schimb, un indice deja agregat la nivelul fiecărei serii.

Szondi atribuie istoric acestor curbe rang psihodiagnostic: descrie o relativă `Umweltstabilität` a valorilor `1–3` la persoane considerate `Triebgesunde`, acordă importanță rigidității persistent scăzute și oscilațiilor foarte mari și corelează uneori variațiile quotientului cu faze clinice. Aceste afirmații aparțin doctrinei istorice a metodei și nu sunt transformate aici în validare prognostică sau psihometrică contemporană.

## Rangul psihodiagnostic revendicat de Szondi

Szondi folosește `TspQu` și `% Sy-Re` ca orientări asupra `Verhalten / Behaviour` și îi integrează în `Syndromanalyse`; diferențele dintre predominanța reacțiilor `0`, predominanța reacțiilor `±` și masa lor totală primesc în textele sale sens psihodiagnostic.

În același timp, `Lehrbuch` spune explicit că `TspQu` nu permite singur deducerea comportamentului și că acești indici nu sunt suficienți, luați singuri, pentru stabilirea unei diagnoze clinice. Manualul păstrează împreună rangul psihodiagnostic revendicat istoric și limita interpretării izolate.

## Deri și Mélon

Susan Deri descrie același `Tendenzspannungsquotient`, ca raport între suma reacțiilor deschise și suma reacțiilor `plus-minus`, adică `Σ0/Σ±`. Lectura ei este pedagogică și insistă asupra raportului dintre descărcare și control, dar avertizează împotriva interpretării rigide a valorilor numerice. Pragurile ei nu sunt folosite pentru a rescrie mecanica matură din `Lehrbuch`.

Jacques Mélon reia ulterior `TspQu`, `% Sy` și reperul `20–30`, insistând la rândul lui asupra valorii relative a indicilor numerici. Nici această tradiție ulterioară nu completează intervalele lipsă, nu furnizează o regulă canonică de rotunjire și nu autorizează introducerea `Tabelle 13` în calculul celor doi indici.

## Protocolul sigur de calcul

Pentru o serie de `N` profile, calculul poate fi ordonat astfel:

1. se numără toate reacțiile factoriale `0` și se obține `Σ0`;
2. se numără toate reacțiile factoriale `±` și se obține `Σ±`;
3. se calculează `TspQu = Σ0 / Σ±`;
4. dacă `Σ± = 0` și `Σ0 > 0`, se păstrează convenția canonică `∞`;
5. se calculează totalul simptomatic `Σ0 + Σ±`;
6. se calculează numărul total de reacții factoriale, `8 × N`;
7. se calculează `% Sy-Re = ((Σ0 + Σ±) × 100) / (8 × N)`;
8. cei doi indici sunt citiți împreună și apoi readuși în configurația calitativă a seriei.

Protocolul nu folosește `Tabelle 13` pentru acești indici. Pentru `0/0`, raportul rămâne nedefinit. Acolo unde se afișează zecimale noi, precizia este o convenție editorială, nu o regulă canonică dedusă din exemple.

În sistemul lui Szondi, cei doi indici intră în `Syndromanalyse`; ca operație, ei comprimă însă numai frecvențe ale seriei.

> **Calculul comprimă frecvențe ale seriei; nu înlocuiește geometria și contextul clinic.**

## Spre `Dur–Moll` și `Sozialindex`

Cu `TspQu` și `% Sy-Re`, am folosit reacțiile `0` și `±` pentru două descrieri globale:

`Σ0 / Σ± -> TspQu`

și

`(Σ0 + Σ±) / toate reacțiile factoriale -> % Sy-Re`.

Capitolul următor schimbă întrebarea. Nu va mai privi doar cât și în ce raport apar reacțiile simptomatice, ci alte moduri în care seria este ponderată și calificată global.

Acolo intră `Dur–Moll` și `Sozialindex`.