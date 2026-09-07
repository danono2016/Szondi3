# Capitolul 12 — De la alegeri la protocolul factorial

**Statut:** STABLE DRAFT  
**Notă editorială:** redactat după cercetarea locală 10/10, outline selectiv, control doctrinar și reader pass; continuitatea procedurală cu `Instruktion Nr. II` din cap. 11 a fost reverificată. Capitolul explică explicit construcția factorială pe VGP; EKP se transcrie separat după aceeași regulă de transfer, din alegerile relative ale `Nachwahl`. Reacțiile `+ / − / ± / 0` apar abia în cap. 13.

---

Capitolul precedent s-a încheiat după două momente distincte de alegere: prima trecere, care produce datele pentru VGP, și `Nachwahl`, care produce separat datele pentru EKP.

Pentru a vedea fără confuzie cum se transformă o alegere în protocol factorial, vom urmări mai întâi **VGP-ul**. Aici avem cele douăsprezece fotografii alese ca simpatice și cele douăsprezece alese ca antipatice în prima trecere. EKP se transcrie separat prin aceeași operație de identificare factorială și numărare, folosind cele douăsprezece poziții relativ simpatice și cele douăsprezece relativ antipatice rezultate din `Nachwahl`. Cele două profiluri nu se amestecă într-o singură numărătoare.

Pentru persoană, experimentul a fost până acum foarte concret: șase serii de chipuri, preferințe și respingeri. Pentru examinator, însă, fiecare dintre aceste chipuri are și o identitate în aparat. Pe verso există informația pe care persoana examinată nu a folosit-o când a ales: seria, poziția și factorul fotografiei.

Acum cardurile se întorc.

Nu pentru a reinterpreta retrospectiv ceea ce a simțit persoana în fața unui chip, ci pentru a răspunde la o întrebare mai modestă și mai exactă:

**ce factori au fost aleși și de câte ori, separat în direcția simpatiei și a antipatiei?**

Aici actul de alegere începe să devină protocol.

În limbajul manualului putem formula pragul astfel:

**în momentul în care întoarcem cardul, alegerea rămâne aceeași, dar descrierea ei se schimbă: din chip ales devine alegere atribuită unui factor.**

## Mai întâi păstrăm urma alegerii

Există o tentație firească de a sări direct la un profil desenat. Avem douăsprezece fotografii preferate, douăsprezece respinse, opt factori — le numărăm și gata.

Dar între fotografie și profil există un nivel care merită păstrat.

Pentru fiecare alegere putem nota trei lucruri simple:

- din ce serie provine fotografia;
- în ce direcție a fost aleasă — simpatică sau antipatică;
- ce inițială factorială poartă pe verso.

Aceasta este forma cea mai apropiată de datele brute ale administrării.

Deri o face foarte vizibilă în fișa pe care o descrie: seriile I–VI au propriile rânduri, iar alegerile simpatice și antipatice sunt notate prin inițialele factorilor fotografiilor alese. Abia după aceea se construiește profilul grafic.

Distincția este metodologic sănătoasă și pentru noi:

**protocolul nu inventează o reacție; păstrează urma alegerii și o face numărabilă.**

Dacă mai târziu un total pare suspect, trebuie să putem coborî din nou până la cardurile concrete care l-au produs.

## De la cele șase serii la cele opt litere

Ordinea factorilor o cunoaștem deja:

`h, s, e, hy, k, p, d, m`.

Ei formează, în aceeași ordine, cei patru vectori:

`S(h,s) — P(e,hy) — Sch(k,p) — C(d,m)`.

Persoana examinată nu a ales însă „factorul h” sau „factorul p”. A ales fotografii. Factorii apar în protocol numai după ce examinatorul identifică litera de pe verso și transferă alegerea în coloana corespunzătoare.

Să luăm o singură serie.

Dacă în seria I cele două fotografii preferate poartă pe verso `h` și `p`, iar cele două respinse `e` și `m`, protocolul brut pentru acea serie poate fi scris astfel:

**Seria I — simpatie: `h, p`; antipatie: `e, m`.**

Nu am spus încă nimic despre sensul psihologic al acestor alegeri.

Am făcut doar o transcriere verificabilă.

## Un exemplu complet, fără interpretare

Ca să vedem întreaga operație, putem construi un exemplu didactic. Nu este cazul unei persoane reale și nu demonstrează nicio regulă psihologică. Este doar un protocol sintetic pentru a face vizibil mecanismul.

Să presupunem că după cele șase serii avem următoarele alegeri VGP:

| Seria | Simpatice | Antipatice |
|---|---|---|
| I | `h, p` | `e, m` |
| II | `s, h` | `hy, d` |
| III | `k, m` | `p, e` |
| IV | `d, s` | `h, hy` |
| V | `p, k` | `m, d` |
| VI | `e, hy` | `s, k` |

Citit astfel, protocolul încă seamănă cu administrarea: șase momente succesive de alegere.

Acum schimbăm perspectiva. Nu ne mai interesează în ce serie a apărut fiecare literă, ci **de câte ori apare fiecare factor între cele douăsprezece preferințe și între cele douăsprezece respingeri**.

Numărătoarea dă:

| Factor | `h` | `s` | `e` | `hy` | `k` | `p` | `d` | `m` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| alegeri simpatice | 2 | 2 | 1 | 1 | 2 | 2 | 1 | 1 |
| alegeri antipatice | 1 | 1 | 2 | 2 | 1 | 1 | 2 | 2 |

Acesta este momentul în care cele șase serii au fost reorganizate în cele opt coloane ale sistemului.

Observă însă ce NU am făcut.

Nu am numit niciuna dintre aceste distribuții pozitivă, negativă, ambivalentă sau nulă. Nu am pus niciun semn lângă `h`, `s` sau ceilalți factori. Avem încă doar **frecvențe de alegere**.

Între fotografie și semn există deci un nivel pe care nu avem voie să-l sărim:

**numărătoarea factorială.**

## Două totaluri care trebuie să iasă întotdeauna

Protocolul oferă și cele mai simple controale ale propriei corectitudini.

În VGP, persoana a selectat din fiecare dintre cele șase serii două fotografii simpatice și două antipatice. Prin urmare, la capătul transferului factorial trebuie să avem exact:

**12 alegeri simpatice**  
și  
**12 alegeri antipatice**.

În exemplul nostru:

`2 + 2 + 1 + 1 + 2 + 2 + 1 + 1 = 12`

și

`1 + 1 + 2 + 2 + 1 + 1 + 2 + 2 = 12`.

Dacă unul dintre aceste totaluri este 11 sau 13, nu avem o subtilitate psihologică. Avem o eroare de înregistrare sau de numărare.

Pentru EKP există același control aritmetic, dar aplicat separat: totalurile trebuie să fie **12 relativ simpatice** și **12 relativ antipatice**, provenite numai din `Nachwahl`.

Mai există un control elementar. Fiecare factor este reprezentat în întregul material prin șase fotografii. Într-un profil, pentru un factor dat, suma fotografiilor lui înregistrate în cele două direcții nu poate depăși șase.

Și aceasta este o limită materială, nu o interpretare.

Astfel de verificări pot părea banale. Tocmai banalitatea lor este utilă. Ele separă eroarea tehnică de problema psihologică înainte ca interpretarea să înceapă.

## Profilul grafic al lui Szondi

Szondi nu păstrează rezultatul numai ca două rânduri de numere.

În *Lehrbuch*, profilul este reprezentat pe o fișă cu opt coloane, câte una pentru fiecare factor. Pentru fiecare coloană există șase pătrate deasupra liniei zero și șase dedesubt.

Pătratele de deasupra corespund alegerilor simpatice; cele de dedesubt alegerilor antipatice.

În convenția grafică istorică descrisă de Szondi, alegerile simpatice sunt marcate cu roșu, iar cele antipatice cu albastru. Dacă `h` a fost ales de două ori simpatic și o dată antipatic, în coloana `h` se marchează două poziții deasupra liniei și una dedesubt.

Culoarea ajută ochiul. Dar nu ea poartă logica operației.

Am putea reprezenta aceleași date prin hașuri, puncte, cifre sau într-o interfață digitală. Ceea ce trebuie păstrat este triada:

**factor — direcția alegerii — frecvența.**

Roșul și albastrul sunt o convenție istorică de reprezentare, nu proprietăți ale factorilor.

## De ce Szondi recomandă să desenăm profilul imediat

În descrierea matură a procedurii, Szondi recomandă ca reprezentarea grafică să fie făcută imediat după încheierea experimentului.

Motivul este foarte concret: fotografiile alese sunt încă la îndemână și transferul poate fi controlat încă o dată.

Cele douăsprezece imagini simpatice pot fi ordonate după factor, numărate și confruntate cu profilul. La fel cele douăsprezece antipatice.

Aici vedem din nou că profilul nu este conceput ca o impresie globală asupra testului. El este rezultatul unei operații care trebuie să poată fi verificată.

Pentru un manual care vrea să păstreze trasabilitatea, principiul merită generalizat:

**un total bun trebuie să poată fi desfăcut înapoi până la cardurile care l-au produs.**

Dacă în coloana `p` avem două alegeri simpatice, ar trebui să putem spune din ce două serii au provenit fotografiile respective. Dacă nu putem, am păstrat rezultatul, dar am pierdut traseul lui.

## De ce datele brute sunt mai bogate decât desenul

Deri insistă tocmai asupra acestui punct. Ea recomandă să nu ne bazăm numai pe reprezentarea grafică, ci să notăm și inițialele fotografiilor alese pentru fiecare serie.

Motivul imediat este controlul. Dar există și un motiv mai larg: odată ce agregăm, pierdem informație despre succesiunea concretă a alegerilor.

Să presupunem că două protocoale produc același total factorial pentru `h`. Într-unul, alegerile `h` au apărut în seriile I și II; în celălalt, în V și VI. La nivelul numărătorii finale, rezultatul este același. La nivelul datelor brute, traseul nu este identic.

Nu avem nevoie acum să interpretăm această diferență și nici să-i atribuim automat o semnificație. Este suficient să înțelegem de ce păstrarea protocolului brut este mai sigură decât păstrarea numai a rezultatului agregat.

**Agregarea simplifică. Protocolul păstrează posibilitatea verificării.**

## Protocolul factorial nu este încă reacția factorială

Ajungem aici la granița cea mai importantă a capitolului.

În fața noastră există acum, pentru fiecare factor, două numere: de câte ori fotografiile lui au fost înregistrate într-o direcție și de câte ori în cealaltă.

De exemplu, în protocolul nostru sintetic VGP:

`h: 2 simpatice / 1 antipatică`  
`e: 1 simpatică / 2 antipatice`.

Acestea sunt distribuții de alegeri.

În vocabularul complet al testului, Szondi va transforma asemenea distribuții în **reacții factoriale**. Acolo vor apărea cele patru forme simbolice pe care le-am amânat deliberat până acum.

Dar clasificarea nu este același lucru cu numărarea.

Mai întâi avem:

**carduri → poziție simpatică/antipatică → inițială factorială → frecvențe factoriale.**

Abia după aceea putem avea:

**frecvențe → reacție factorială simbolică.**

Același lanț formal este folosit separat pentru VGP și EKP; ceea ce diferă este proveniența datelor de alegere și, ulterior, regulile de interpretare ale profilurilor.

Capitolul acesta se oprește la primul lanț.

## Ce avem acum în față

Am pornit Partea a III-a cu o cutie de fotografii.

În cap. 10 am văzut cum este construit materialul. În cap. 11 persoana a intrat în relație cu el prin prima alegere și prin `Nachwahl`. Acum, în cap. 12, aceste alegeri pot fi traduse, fără a le amesteca, într-o formă pe care sistemul o poate prelucra.

Pentru prima dată putem vedea simultan cele două fețe ale aceluiași eveniment:

pentru persoană: **„am ales acest chip”**;

pentru protocol: **„această poziție de alegere aparține factorului `h`, `p`, `e`...”**.

Încă nu știm ce înseamnă configurația numerică a unui factor.

Știm doar s-o construim corect.

Și tocmai această modestie tehnică ne permite următoarea întrebare fără să sărim nicio treaptă:

**când o distribuție de alegeri devine pozitivă, negativă, ambivalentă sau nulă — și de ce există exact aceste patru reacții?**