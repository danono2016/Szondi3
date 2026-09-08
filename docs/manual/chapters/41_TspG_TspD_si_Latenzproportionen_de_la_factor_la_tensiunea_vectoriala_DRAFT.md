# Capitolul 41 — `TspG`, `TspD` și `Latenzproportionen`: de la factor la tensiunea vectorială

**Statut:** STABLE DRAFT — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE  
**Notă editorială:** reader pass-ul extern a cerut revizie moderată înainte de stabilizare; DRAFT v3 a integrat conservator compresia, segmentarea și reducerea metadiscursului, iar recheck-ul stilistic extern a dat **STYLE PASS — READY FOR STABLE DRAFT**. `CH41-SHORT-01` rămâne SOURCE CONFLICT HOLD ACTIVE ca limită documentată a sursei.

---

O serie poate fi numărată fără ca sensul ei să fie redus la număr.

După ce profilele au fost citite ca succesiune, începe o altă operație. Nu mai întrebăm ce profil a urmat după altul, ci ce se acumulează, de-a lungul seriei, în fiecare factor și cum se raportează apoi cei doi factori ai aceluiași vector.

Mișcarea este precisă:

`reacții factoriale în serie -> TspG factorial -> TspD intravectorial -> Latenzgrad / Latenzgröße -> Latenzproportionen`.

Mai întâi agregăm în interiorul factorului. Apoi comparăm cei doi factori ai vectorului. La sfârșit comparăm între ele cele patru diferențe vectoriale.

## Primul nivel: `TspG`

În `Lehrbuch`, Szondi numește `Grad der Tendenzspannung` suma reacțiilor nule și ambivalente ale unui factor de-a lungul seriei. Abrevierea este `TspG`.

**`TspG(factor) = numărul reacțiilor 0 + numărul reacțiilor ± din seria considerată`.**

Reacțiile `+` și `−` nu intră în sumă. Nici semnele de `Quantumspannung` — `!`, `!!`, `!!!` — nu adaugă unități la `TspG`.

Dacă factorul `h` apare într-o serie de zece profile astfel:

`+ , 0 , ± , + , 0 , − , ± , 0 , + , −`

avem trei reacții `0` și două reacții `±`:

`TspG h = 3 + 2 = 5`.

## De ce apar împreună `0` și `±`

Suma aparține concepției lui Szondi despre `Tendenzspannung`. Reacția `±` face vizibilă coexistarea celor două direcții ale tendinței, iar reacția `0` este tratată ca reacție de descărcare și, în această construcție, ca `postambivalente Reaktion`. De aceea `TspG` numără împreună aparițiile `±` și `0`.

`Triebpathologie II` precizează rangul mărimii: `TspG` este un **`Maßstab für die Entladungsbereitschaft eines Bedürfnisses`**.

Tot acolo, reacțiile ambivalente sunt tratate empiric ca **`Vorphase der Entladung`**, cu calificarea explicită **`abgesehen von den Zwangsneurotikern`**. Formula `TspG = Σ0 + Σ±` rămâne neschimbată; calificarea privește justificarea doctrinară a ambivalenței ca prefază a descărcării.

În același context, Szondi opune factorii simptomatici, cu `TspG` mai mare, `Wurzelfaktoren`-ilor, care au `TspG` mai mic. De aceea un `TspG` mic nu înseamnă pur și simplu un factor „slab”: în calculul latenței, tocmai factorul cu `TspG` mai mic primește rangul dinamic decisiv.

## `TspG` nu este `Quantumspannung`

`Quantumspannung` aparține reacției factoriale și este exprimată prin `!`, `!!`, `!!!` etc. `TspG` este o mărime serială: numără cât de des factorul apare ca `0` sau `±`.

Astfel, `+!!!` nu contribuie la `TspG`, în timp ce o reacție `±` contribuie cu o unitate.

**`TspG ≠ Quantumspannung`.**

## `Tages-TspG` și `faktorieller TspG`

În `Tendenzspannungstabelle`, cele două direcții de numărare trebuie văzute imediat separat:

- **orizontal, pe profil:** `Σ0 + Σ± -> Tages-TspG`;
- **vertical, pe factor de-a lungul seriei:** `Σ0 + Σ± -> faktorieller TspG`.

Pentru `TspD` folosim **`faktorieller TspG`**.

`Tages-TspG ≠ faktorieller TspG`.

## Lungimea seriei schimbă domeniul numeric

Dacă seria are `N` profile, un factor poate avea un `TspG` brut între `0` și `N`. Într-o `Zehnerserie`, maximul este `10`; într-o serie mai lungă poate fi mai mare. `Lehrbuch` oferă și o serie de 15 profile în care apare un `TspG` de `13`.

**Baza zece este un standard de serie, nu limita matematică absolută a `TspG`.**

## Al doilea nivel: `TspD`

După ce avem `TspG` factorial pentru toți cei opt factori, calculul trece de la factor la vector:

- S: `h / s`;
- P: `e / hy`;
- Sch: `k / p`;
- C: `d / m`.

Pentru fiecare pereche scădem valoarea `TspG` mai mică din cea mai mare. Rezultatul este `Tendenzspannungsdifferenz`, abreviat `TspD`.

**`TspD = TspG mai mare − TspG mai mic`.**

Există patru `TspD`, câte unul pentru S, P, Sch și C.

În `Triebpathologie II`, `TspD` exprimă diferența gradelor de `Entladungsbereitschaft` dintre cei doi factori ai aceluiași vector și măsoară cantitativ tensiunea — respectiv `Triebgefahr`, în vocabularul doctrinar al lui Szondi — intravectorial.

## Diferența și factorul indexat

Exemplul canonic arată de ce cifra singură nu este suficientă:

`TspG h = 9`  
`TspG s = 2`

Diferența este:

`9 − 2 = 7`.

Szondi indexează vectorul cu factorul care are **`TspG` mai mic**. Aici acesta este `s`, deci forma de latență este:

**`Ss / 7`.**

Dacă inversăm valorile:

`TspG h = 2`  
`TspG s = 9`,

diferența rămâne `7`, dar factorul cu `TspG` mai mic este acum `h`:

**`Sh / 7`.**

Cifra rămâne aceeași; indexul și sensul factorial al diferenței se schimbă.

**Indexul aparține factorului cu `TspG` mai mic, nu factorului cu valoarea mai mare.**

În doctrina lui Szondi, factorul cu gradul simptomatic mai mic primește rangul latent și dinamica mai puternică. De aceea `TspG` nu trebuie transformat într-un scor modern de „forță”.

## `TspD` nu este o diferență în timp

În `Inkonstanzmethode`, diferența aparține comparației dintre două profile și succesiunii temporale. În `TspD`, comparăm **cei doi factori ai aceluiași vector**, după ce fiecare a fost agregat de-a lungul seriei prin `TspG`.

**Diferență temporală între profile ≠ `TspD` intravectorial.**

## Ce nu spune un `TspD = 0`

O diferență zero nu descrie o singură formă vectorială. Szondi discută situații calitativ diferite — `++`, `−−`, `00`, `±±` — care pot conduce la aceeași diferență numerică; în nota sa apare și `+− / −+`, pentru care vorbește despre `Triebentmischung`, nu despre `Trieblegierung`.

**Aceeași valoare `TspD = 0` nu identifică singură același `Vektorbild`.**

**Calculul nu șterge geometria vectorului.**

## `TspD`, `Latenzgrad` și `Latenzgröße`

Terminologia lui Szondi nu este perfect rigidă între volume. `Lehrbuch` lucrează cu `Tendenzspannungsdifferenz`, `Latenzgrad` și `Latenzgröße`, iar `Triebpathologie II` formulează explicit `Latenzgrad oder Latenzgröße`.

Operația rămâne clară: din cele două `TspG` factoriale obținem `TspD`; valoarea diferenței localizată în vector este tratată de Szondi ca `Latenzgrad` sau `Latenzgröße`.

**`TspD` este diferența; valoarea ei localizată în vector este `Latenzgrad` / `Latenzgröße`.**

## Al treilea nivel: `Latenzproportionen`

Lanțul complet este:

`8 TspG -> 4 TspD -> 4 Latenzgrade -> Latenzproportionen`.

`Lehrbuch` oferă, într-un exemplu cu 15 profile:

`Sh / 13 : Schp / 4 : Cm / 4 : P / 0`.

Exemplul arată simultan că o valoare poate depăși `10`, că două grade pot fi egale (`4 : 4`) și că la diferența zero poate apărea `P / 0` fără un factor unic indexat prin simpla diferență numerică.

În `Triebpathologie II`, aceeași logică apare într-o formulare matură:

`Schp− / 10 : Phy− / 6 : Sh+ / 6 : Cd+ / 3`.

Semnele `+` și `−` atașate factorului latent vor conta pentru `Unterklasse`; regula clasificatorie aparține capitolului 42.

## Egalitățile rămân egalități

Când două grade sunt egale, nu inventăm o ordine suplimentară. În exemplul canonic:

`4 : 4` rămâne `4 : 4`.

Consecințele pentru clase și `Äqualität` aparțin pasului următor al aparatului.

---

## `CH41-SHORT-01` — SOURCE CONFLICT HOLD

**Aici sursa nu oferă o regulă operațională neechivocă. HOLD-ul trebuie citit ca limită a sursei, nu ca încă o regulă tehnică.**

Pentru seriile de trei până la nouă profile, instrucțiunile Schafir–Szondi de la pp. 285–286 spun că rezultatele pot fi folosite numai după `Umrechnung`, iar `Tabelle 13` convertește sumele reacțiilor în raport cu o `angenommene Zehnerserie`.

În același `Lehrbuch`, **Fall 18** lucrează însă cu numai șase profile și tipărește direct:

`h=1, s=0, e=2, hy=2, k=5, p=4, d=3, m=3`.

Din aceste `TspG` brute calculează fără conversie prealabilă:

`h−s = 1−0 = 1`  
`e−hy = 2−2 = 0`  
`k−p = 5−4 = 1`  
`d−m = 3−3 = 0`.

Rezultatul tipărit este:

`S=1, P=0, Sch=1, C=0`.

Dacă am normaliza mai întâi `TspG` prin `Tabelle 13`, pentru șase profile:

`1→2`, `0→0`, `2→3`, `5→8`, `4→7`, `3→5`,

ar rezulta:

`S=2, P=0, Sch=1, C=0`.

Dacă am converti direct `TspD` brute, ambele diferențe `1` ar deveni `2`, deci ar rezulta:

`S=2, Sch=2`.

Niciuna dintre cele două ordine nu reproduce Fall 18.

Avem astfel o **inconsistență operațională internă în aceeași ediție a `Lehrbuch`-ului**. Manualul nu o rezolvă alegând un algoritm în locul lui Szondi.

> **Ambiguitatea documentată este preferabilă certitudinii inventate.**

**Pentru seriile de 3–9 profile, manualul nu autorizează nici `TspG brut -> Tabelle 13 -> TspD`, nici `TspD brut -> Tabelle 13` ca regulă canonică universală.**

HOLD-ul privește numai ordinea operațională a conversiei în seria scurtă. El nu anulează mecanica direct documentată a `TspG`, `TspD` și `Latenzproportionen` acolo unde sursa le calculează fără această ambiguitate.

---

## Deri și Mélon

Deri și Mélon rămân tradiție ulterioară, nu arbitri ai conflictului `CH41-SHORT-01`.

Susan Deri explică pedagogic succesiunea `open + plus-minus -> T.sp.G. -> diferență -> Latenzgrösse -> Latenzproportionen` și confirmă indexarea prin factorul cu indice simptomatic mai mic, dar nu adoptă întreaga justificare genetică a lui Szondi.

Mélon descrie mecanica generală și folosește pentru diferență abrevierea `TspGD`. Manualul păstrează notația primară Szondi:

**`TspD`.**

## Limita calculului

`TspG`, `TspD`, `Latenzgrad` și `Latenzproportionen` ordonează formal seria; ele nu devin prin aceasta măsuri autonome de forță psihică, severitate clinică ori probabilitate diagnostică și nici instrumente psihometrice moderne.

**Calculul ordonează o serie; nu transformă seria într-un diagnostic.**

## Spre `Triebklasse`

Acum avem opt `TspG`, patru diferențe vectoriale și ordinea celor patru grade de latență. Următoarea problemă este statutul pe care îl primesc vectorii în această ordine: `Triebklasse`, `Unterklasse`, `Wurzelfaktor`, `Triebgefahr` și `Ventil`.

Regulile lor aparțin capitolului 42.