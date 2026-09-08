# Capitolul 41 — `TspG`, `TspD` și `Latenzproportionen`: de la factor la tensiunea vectorială

**Statut:** DRAFT v2 — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE / READER PASS NEXT  
**Notă editorială:** nucleul `TspG -> TspD -> Latenzgrad/Latenzgröße -> Latenzproportionen` este documentat direct și a primit DOCTRINAL PASS după recheck extern. Pentru seriile de 3–9 profile, `Lehrbuch` conține însă un conflict operațional intern: instrucțiunile Schafir–Szondi cer `Umrechnung` prin `Tabelle 13`, în timp ce Fall 18 calculează `Latenzgrade` pentru o serie de șase profile direct din `TspG` brute. `CH41-SHORT-01` rămâne SOURCE CONFLICT HOLD ACTIVE: manualul nu autorizează nici `TspG brut -> Tabelle 13 -> TspD`, nici `TspD brut -> Tabelle 13` ca regulă canonică universală. HOLD-ul documentează o contradicție a sursei și nu mai constituie un defect al capitolului.

---

O serie poate fi numărată fără ca sensul ei să fie redus la număr.

După ce profilele au fost citite ca succesiune, începe o altă operație. Nu mai întrebăm ce profil a urmat după altul, ci ce se acumulează, de-a lungul seriei, în fiecare factor și cum se raportează apoi cei doi factori ai aceluiași vector.

Mișcarea este precisă:

`reacții factoriale în serie -> TspG factorial -> TspD intravectorial -> Latenzgrad / Latenzgröße -> Latenzproportionen`.

Fiecare treaptă schimbă nivelul calculului. Mai întâi agregăm în interiorul factorului. Apoi comparăm cei doi factori ai vectorului. La sfârșit comparăm între ele cele patru diferențe vectoriale.

## Primul nivel: `TspG`

În `Lehrbuch`, Szondi numește `Grad der Tendenzspannung` suma reacțiilor nule și ambivalente ale unui factor de-a lungul seriei. Abrevierea este `TspG`.

Pentru fiecare factor numărăm:

- de câte ori apare reacția `0`;
- de câte ori apare reacția `±`;
- apoi adunăm cele două frecvențe.

Formula de lucru este:

**`TspG(factor) = numărul reacțiilor 0 + numărul reacțiilor ± din seria considerată`.**

Reacțiile `+` și `−` nu intră în această sumă. Nici semnele de `Quantumspannung` — `!`, `!!`, `!!!` — nu adaugă unități la `TspG`.

Să luăm un exemplu didactic simplu. Dacă factorul `h` apare într-o serie de zece profile astfel:

`+ , 0 , ± , + , 0 , − , ± , 0 , + , −`

avem trei reacții `0` și două reacții `±`. Prin urmare:

`TspG h = 3 + 2 = 5`.

Nu am numărat intensitatea alegerilor și nu am numărat semnele grafice din reacții. Am numărat cinci **reacții factoriale** aparținând celor două categorii care intră în calcul.

## De ce apar împreună `0` și `±`

Suma nu este o simplă convenție aritmetică. Ea aparține concepției lui Szondi despre `Tendenzspannung`.

Reacția `±` face vizibilă coexistarea celor două direcții ale tendinței. Reacția `0` este tratată de Szondi ca reacție de descărcare și, în această construcție, ca `postambivalente Reaktion`. Din acest motiv, gradul tensiunii de tendință nu este calculat numai din aparițiile `±`, ci din frecvența comună a reacțiilor `±` și `0`.

`Triebpathologie II` precizează rangul conceptual al acestei mărimi: `TspG` este pentru Szondi un **`Maßstab für die Entladungsbereitschaft eines Bedürfnisses`**, adică o măsură a disponibilității de descărcare a trebuinței în cadrul doctrinei sale. Tot acolo, reacțiile ambivalente sunt numărate între reacțiile simptomatice/de descărcare deoarece sunt tratate empiric ca `Vorphase der Entladung`, dar Szondi formulează explicit calificarea **`abgesehen von den Zwangsneurotikern`**. Formula `TspG = Σ0 + Σ±` nu se schimbă; ceea ce nu trebuie universalizat fără rest este justificarea doctrinară a ambivalenței ca prefază a descărcării.

În același context, Szondi opune factorii simptomatici, cu `TspG` mai mare, `Wurzelfaktoren`-ilor, care au `TspG` mai mic. Această relație produce una dintre inversiunile importante ale aparatului formal: un `TspG` mic nu înseamnă pur și simplu un factor „slab”. În calculul latenței, tocmai factorul cu `TspG` mai mic primește rangul dinamic decisiv.

Sistemul de clase construit din această relație va fi materia capitolului următor. Aici avem nevoie numai de mecanica pe care el se sprijină.

## `TspG` nu este `Quantumspannung`

Cele două noțiuni folosesc cuvântul „tensiune”, dar nu măsoară același lucru.

`Quantumspannung` aparține reacției factoriale și exprimă încărcarea ei cantitativă prin `!`, `!!`, `!!!` etc. `TspG` este o mărime serială: numără cât de des factorul apare ca `0` sau `±` în seria considerată.

De aceea o reacție `+!!!` rămâne, pentru calculul `TspG`, o reacție `+` și nu contribuie la sumă. O reacție `±` contribuie cu o unitate, indiferent că problema ei doctrinară este cu totul alta decât aceea a unei reacții `0`.

**`TspG ≠ Quantumspannung`.**

## Două direcții de numărare în `Tendenzspannungstabelle`

În prezentarea tehnică a `Trieblinnäus`-ului, Szondi distinge două feluri de agregare.

Pe orizontală, pentru fiecare profil, pot fi însumate reacțiile `0`, reacțiile `±` și poate fi calculat un **`Tages-TspG`**. Acesta descrie încărcarea simptomatică a profilului respectiv.

Pe verticală, pentru fiecare factor, sunt însumate aparițiile `0` și `±` de-a lungul întregii serii. Rezultatul este `faktorieller TspG`.

Pentru calculul care urmează în acest capitol, baza este **`faktorieller TspG`**.

Cele două direcții nu trebuie confundate:

`sumă pe profil ≠ sumă pe factor de-a lungul seriei`.

## Lungimea seriei schimbă domeniul numeric

`TspG` brut depinde de numărul profilelor pe care îl agregăm. Dacă seria are `N` profile, un factor poate avea un `TspG` cuprins între `0` și `N`.

Într-o `Zehnerserie`, maximul este deci `10`. Dar acesta nu este un plafon universal al mărimii. `Lehrbuch` folosește și o serie de 15 profile în care apare un `TspG` de `13`.

Capitolul precedent a folosit baza zece ca reper pentru seria scurtă. De aici nu trebuie dedus că orice mărime serială a lui Szondi ar fi prin definiție limitată la zece.

**Baza zece este un standard de serie, nu limita matematică absolută a `TspG`.**

## Al doilea nivel: `TspD`

După ce avem `TspG` factorial pentru toți cei opt factori, calculul se mută de la factor la vector.

Fiecare vector conține doi factori:

- S: `h / s`;
- P: `e / hy`;
- Sch: `k / p`;
- C: `d / m`.

Pentru fiecare pereche luăm cele două valori `TspG` și scădem valoarea mai mică din valoarea mai mare. Rezultatul este `Tendenzspannungsdifferenz`, abreviat `TspD`.

**`TspD = TspG mai mare − TspG mai mic`.**

Există astfel patru `TspD`: unul pentru S, unul pentru P, unul pentru Sch și unul pentru C.

În `Triebpathologie II`, Szondi formulează și sensul acestei diferențe: `TspD` exprimă diferența gradelor de `Entladungsbereitschaft` dintre cei doi factori ai aceluiași vector și este mărimea prin care tensiunea — respectiv `Triebgefahr`, în vocabularul său doctrinar — este măsurată cantitativ intravectorial. Aceasta fixează rangul conceptual al operației fără a transforma `TspD` într-un scor clinic contemporan de severitate.

## Diferența și factorul indexat

Exemplul canonic este foarte instructiv:

`TspG h = 9`  
`TspG s = 2`

Diferența este:

`9 − 2 = 7`.

Dar notația nu reține numai cifra `7`. Szondi indexează vectorul cu factorul care are **`TspG` mai mic**. În exemplul nostru, acesta este `s`, deci forma de latență este:

**`Ss / 7`.**

Dacă inversăm valorile:

`TspG h = 2`  
`TspG s = 9`,

diferența rămâne `7`, dar factorul cu gradul de tensiune mai mic este acum `h`. Notația devine:

**`Sh / 7`.**

Mărimea numerică a diferenței este aceeași. Sensul factorial al diferenței nu mai este același.

**Indexul aparține factorului cu `TspG` mai mic, nu factorului cu valoarea mai mare.**

Această regulă pare contraintuitivă numai dacă tratăm `TspG` ca pe un scor de „forță”. În doctrina lui Szondi, factorul cu gradul simptomatic mai mic este tocmai cel căruia îi atribuie rangul latent și dinamica mai puternică. Calculul trebuie învățat în termenii acestui sistem, fără a-l transforma într-o măsură psihologică modernă pe care sursa nu o oferă.

## `TspD` nu este o diferență în timp

Cuvântul „diferență” poate induce o confuzie cu metoda schimbării dintre profile.

În `Inkonstanzmethode`, două profile sunt comparate între ele și diferența aparține succesiunii temporale. În `TspD`, nu comparăm profilul I cu profilul II și nu comparăm două momente experimentale.

Comparăm **cei doi factori ai aceluiași vector**, după ce fiecare a fost agregat de-a lungul seriei prin `TspG`.

**Diferență temporală între profile ≠ `TspD` intravectorial.**

## Ce nu spune un `TspD = 0`

O diferență zero pare, la prima vedere, să descrie o situație unică: cei doi factori ar fi „egali”. Numeric, da. Calitativ, nu.

Szondi arată că aceeași diferență nulă sau foarte mică poate apărea în contexte vectoriale diferite. El discută situații de autoreglare reciprocă prin forme precum `++` sau `−−`, descărcarea simultană `00` și ambivalența simultană `±±`. În nota sa apare și cazul `+− / −+`, pentru care vorbește despre `Triebentmischung`, nu despre `Trieblegierung`.

Aceste forme nu devin echivalente pentru că produc aceeași diferență numerică.

**Aceeași valoare `TspD = 0` nu identifică singură același `Vektorbild`.**

Calculul nu șterge geometria vectorului. Pentru a ști *cum* este organizată egalitatea, trebuie să revenim la profile și la `Vektorbilder`.

## `TspD`, `Latenzgrad` și `Latenzgröße`

Terminologia lui Szondi nu este perfect rigidă între toate volumele. `Lehrbuch` lucrează cu `Tendenzspannungsdifferenz`, `Latenzgrad` și `Latenzgröße`, iar `Triebpathologie II` formulează explicit `Latenzgrad oder Latenzgröße`.

Nu este necesar să transformăm aceste variante într-o taxonomie editorială mai strictă decât sursa.

Operația este clară: din cele două `TspG` factoriale obținem diferența `TspD`. Atunci când această diferență este localizată în vector și intră în seria raporturilor de latență, valoarea ei este tratată de Szondi ca `Latenzgrad` sau `Latenzgröße`.

Pe scurt:

**`TspD` este diferența; valoarea ei localizată în vector este `Latenzgrad` / `Latenzgröße`.**

## Al treilea nivel: `Latenzproportionen`

După cele opt `TspG` și cele patru `TspD`, avem patru mărimi vectoriale. Ele sunt puse în relație după mărimea lor.

Lanțul poate fi văzut acum în forma sa completă:

`8 TspG -> 4 TspD -> 4 Latenzgrade -> Latenzproportionen`.

`Lehrbuch` oferă, într-un exemplu cu 15 profile, următoarea serie:

`Sh / 13 : Schp / 4 : Cm / 4 : P / 0`.

Exemplul este util din trei motive. Mai întâi, arată din nou că o valoare poate depăși `10` într-o serie mai lungă. Apoi arată că două grade pot fi egale: aici `Schp / 4` și `Cm / 4`. În sfârșit, la diferența zero apare `P / 0`, fără ca un factor unic să poată fi indexat prin simpla diferență numerică.

În `Triebpathologie II`, aceeași logică apare într-o formulare matură de tipul:

`Schp− / 10 : Phy− / 6 : Sh+ / 6 : Cd+ / 3`.

Semnele `+` și `−` atașate factorului latent vor conta pentru `Unterklasse`. Aici le observăm numai ca parte a notației; regula clasificatorie aparține capitolului 42.

## Egalitățile rămân egalități

Când cele patru grade sunt ordonate, o valoare mai mare precedă o valoare mai mică. Dacă două valori sunt egale, nu avem dreptul să inventăm o ordine suplimentară numai pentru a obține un clasament fără egalități.

În exemplul de mai sus, `4 : 4` rămâne `4 : 4`.

Efectele pe care egalitatea le va avea asupra claselor, inclusiv problema `Äqualität`, aparțin pasului următor al aparatului. Capitolul acesta nu introduce un tie-break pe care sursa nu îl dă.

## Seria scurtă și `Tabelle 13`: conflictul sursei

Pentru seriile de trei până la nouă profile, sursa primară nu permite stabilirea neechivocă a ordinii conversiei.

Pe de o parte, instrucțiunile Schafir–Szondi de la pp. 285–286 spun că rezultatele pentru seria scurtă pot fi folosite numai după `Umrechnung`, iar `Tabelle 13` convertește sumele reacțiilor în raport cu o `angenommene Zehnerserie`.

Pe de altă parte, același `Lehrbuch`, în **Fall 18**, lucrează cu numai șase profile și tipărește direct următoarele `TspG`:

`h=1, s=0, e=2, hy=2, k=5, p=4, d=3, m=3`.

Din ele calculează fără conversie prealabilă:

`h−s = 1−0 = 1`  
`e−hy = 2−2 = 0`  
`k−p = 5−4 = 1`  
`d−m = 3−3 = 0`.

Așadar, `Latenzgrade` sunt obținute aici direct din `TspG` brute ale seriei de șase profile.

Dacă am aplica mai întâi `Tabelle 13`, valorile relevante ar deveni:

`1→2`, `0→0`, `2→3`, `5→8`, `4→7`, `3→5`,

iar diferențele ar fi:

`S=2, P=0, Sch=1, C=0`,

nu `S=1, P=0, Sch=1, C=0`, cum tipărește Fall 18.

Nici conversia directă a diferențelor brute prin `Tabelle 13` nu rezolvă conflictul: ambele diferențe brute `1` ar deveni `2`, deci ar rezulta `S=2, Sch=2`.

Avem astfel o **inconsistență operațională internă în aceeași ediție a `Lehrbuch`-ului**. Manualul nu o rezolvă alegând un algoritm în locul lui Szondi.

Prin urmare:

**Pentru seriile de 3–9 profile, manualul nu autorizează în acest moment nici `TspG brut -> Tabelle 13 -> TspD`, nici `TspD brut -> Tabelle 13` ca regulă canonică universală.**

Acest punct este documentat ca:

**`CH41-SHORT-01 — SOURCE CONFLICT HOLD`.**

HOLD-ul privește ordinea operațională a conversiei în seria scurtă. Nu anulează mecanica direct documentată a `TspG`, `TspD` și `Latenzproportionen` în seriile pentru care sursa le calculează fără această ambiguitate.

## Deri și Mélon

Tradiția ulterioară face mecanica mai ușor de urmărit, dar nu înlocuiește fundamentarea primară.

Susan Deri explică limpede succesiunea `open + plus-minus -> T.sp.G. -> diferență -> Latenzgrösse -> Latenzproportionen` și confirmă indexarea vectorului prin factorul cu indice simptomatic mai mic. În același timp, ea spune că nu adoptă în lucrarea ei întreaga justificare genetică a lui Szondi. Claritatea ei pedagogică nu trebuie retroproiectată ca și cum ar fi chiar argumentația primară a lui Szondi.

Mélon descrie aceeași mecanică generală, dar folosește pentru diferență abrevierea `TspGD`.

Manualul păstrează notația primară:

**`TspD`.**

## Ce poate afirma calculul

Prin aceste operații putem:

- agrega frecvența reacțiilor `0` și `±` pentru fiecare factor;
- compara factorii parteneri ai fiecărui vector;
- obține patru grade sau mărimi de latență;
- pune aceste patru valori într-o relație proporțională.

Dar numărul nu dobândește, prin calcul, drepturi interpretative nelimitate. Un `TspG` mic nu este o „forță psihică” măsurată obiectiv. Un `TspD` mare nu este un scor de severitate clinică. Un `Latenzgrad` nu este o probabilitate diagnostică, iar `Latenzproportionen` nu devine prin sine un instrument psihometric modern autonom.

Mai ales, calculul nu înlocuiește forma calitativă a profilelor. Cazul `TspD = 0` a arătat deja de ce: aceeași cifră poate acoperi configurații vectoriale diferite.

**Calculul ordonează o serie; nu transformă seria într-un diagnostic.**

## Spre `Triebklasse`

Acum avem opt `TspG`, patru diferențe vectoriale și o ordine a celor patru grade de latență.

Următoarea întrebare nu mai este cum se calculează diferența, ci ce statut primește vectorul care ocupă anumite poziții în această ordine. Acolo apar `Triebklasse`, `Unterklasse`, `Wurzelfaktor`, `Triebgefahr` și `Ventil`.

Acesta este pasul următor al aparatului formal.