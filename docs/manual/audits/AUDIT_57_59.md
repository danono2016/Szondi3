# Manualul Szondi — Audit de arhitectură

## TRANȘA 9 — CAPITOLELE 57–59

**Statut:** WORKING / DRAFT  
**Ramură:** `manual`  
**Scop:** audit structural al închiderii practice a manualului: de la protocolul real la examinarea completă, integrarea în psihoterapie/formularea clinică și un caz didactic capstone complet.

> Acest document continuă `docs/manual/ARCHITECTURE_AUDIT.md` și auditurile 10–14, 15–26, 27–31, 32–37, 38–44, 45–50 și 51–56. Este audit structural 10/10, nu cercetarea de finalizare a capitolelor.

## Observație metodologică specială

Capitolele 57–59 sunt diferite de majoritatea capitolelor anterioare. Corpusul canonic oferă:

- tehnica administrării și calculului;
- metodele de interpretare;
- seria și aparatul formal;
- sindromatica;
- studii și istorii de caz;
- confruntarea cu anamneza, Krankengeschichte, Erbtafel și material clinic;
- utilizări terapeutice și longitudinale în sens larg.

Dar corpusul **nu oferă o singură procedură standardizată, contemporană, de tip „workflow de cabinet” sau un format unic de raport clinic**. Prin urmare, această parte trebuie să combine două niveluri fără să le confunde:

1. **ce este susținut de surse**;
2. **arhitectura practică proprie a manualului**, construită pentru a păstra separate observația, calculul, doctrina, inferența și sinteza clinicianului.

Software-ul Szondi3 poate fi folosit aici numai ca laborator de consistență și ca model de separare a straturilor. El nu este autoritate doctrinară.

---

## Matrice de relevanță

| Cap. | SA | LEHR | IA-A | IA-B | THER-A | THER-B | TRIEB-1 | TRIEB-2 | DERI | MELON |
|---|---|---|---|---|---|---|---|---|---|---|
| 57. Examinarea completă | CONTRIBUTIVĂ | CENTRALĂ | CONTROL | CONTRIBUTIVĂ | CONTROL | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ |
| 58. Integrarea clinică în psihoterapie | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CENTRALĂ | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ |
| 59. Cazul complet | CONTRIBUTIVĂ | CENTRALĂ | CONTRIBUTIVĂ | CENTRALĂ | CONTRIBUTIVĂ | CENTRALĂ | CONTRIBUTIVĂ | CENTRALĂ | CENTRALĂ | CONTRIBUTIVĂ |

Abrevieri: SA=`SZ_SA_1948`; LEHR=`SZ_LEHR_1972`; IA-A/B=`SZ_IA_1956_A/B`; THER-A/B=`SZ_THER_1963_A/B`; TRIEB-1/2=`SZ_TRIEBPATH_1/2`.

**Notă:** la capitolul 59 centralitatea exactă va depinde de cazul ales. Dacă tema clinică a cazului este, de exemplu, predominant de Eu, `Ich-Analyse` va deveni centrală; dacă este predominant de contact sau de paroxism, ponderea surselor se poate schimba. Cercetarea 10/10 trebuie refăcută asupra cazului concret.

---

# Verdict structural major

**PĂSTRĂM toate cele trei capitole, dar le atribuim funcții radical diferite.**

- **57** trebuie să fie capitolul despre **organizarea datelor**: cum ajungem de la alegeri brute la un dosar de examinare complet, controlabil și reproductibil.
- **58** trebuie să fie capitolul despre **integrarea clinică**: cum confruntăm datele Szondi cu anamneza, interviul și procesul terapeutic fără a transforma nici testul, nici clinicianul într-un arbitru infailibil.
- **59** trebuie să fie **demonstrația finală**: un caz complet în care toate nivelurile sunt puse în lucru, inclusiv contradicții, date insuficiente și limite.

Aceste capitole nu mai introduc aproape deloc doctrină nouă. Ele trebuie să arate că întregul manual poate funcționa ca metodă.

---

## 57. De la administrare la examinarea completă

### Verdict

**PĂSTRĂM, dar schimbăm titlul pentru a sublinia că nu este un nou capitol de interpretare.**

### Titlu recomandat

**Examinarea completă: de la protocolul brut la dosarul Szondi**

sau, dacă „dosar” sună prea administrativ:

**Examinarea completă: de la protocolul brut la materialul clinic organizat**

### Întrebarea centrală

> **Ce trebuie să existe, să fie verificat și să rămână separat înainte ca clinicianul să formuleze o concluzie?**

### Suportul din corpus

`Lehrbuch` oferă coloana vertebrală operațională: material, administrare, construire de profil, serie, metode calitative, cantitative și proporționale. `Triebpathologie` și `Ich-Analyse` arată însă că interpretarea clinică reală nu se reduce la profil: apar Erbtafel, Krankengeschichte, analiză dinamică și confruntarea mai multor domenii pulsionale. Într-un caz din `Ich-Analyse`, Szondi spune explicit că analiza dinamică bazată pe tabloul ereditar și istoricul bolii produce un tablou clinic mult mai diferențiat decât eticheta psihiatrică globală de „Psychopathie”.

Deri adaugă o lecție practică foarte importantă: seria simbolizată ajută la observarea rapidă a constanței și schimbării, dar nu trebuie niciodată să înlocuiască profilele grafice originale, deoarece detaliile cantitative și calitative rămân necesare. Ea insistă și că metoda este consumatoare de timp și cere administrări repetate, nu o interpretare instantanee.

### Arhitectura proprie a manualului

Capitolul 57 va propune un **dosar stratificat**, dar va spune explicit că această organizare este a manualului, nu o „fișă oficială Szondi” găsită în surse.

Dosarul trebuie să păstreze separat:

1. **datele de administrare** — data, numărul administrării, eventuale incidente procedurale;
2. **alegerile brute** — simpatic/antipatic și, unde este cazul, complementul;
3. **protocolul factorial numeric**;
4. **profilul simbolic VGP** și încărcările;
5. **EKP/ThKP**, dacă sunt disponibile, etichetate corect și fără echivalări doctrinare automate;
6. **seria de profile**, fără pierderea profilelor individuale;
7. **calculele seriale** — Tabelle 13 dacă este cazul, TspG/TspD, Latenzproportionen, Triebklasse/Unterklasse, Triebformel, indici/proporții;
8. **observațiile interpretative** — separate de calcule;
9. **materialul clinic extern** — anamneză, interviu, evoluție, observații terapeutice, alte instrumente dacă există;
10. **întrebările și incertitudinile rămase deschise**.

### Ordinea are sens epistemic

Cititorul trebuie să poată vedea oricând:

`alegere brută -> numărare -> reacție -> profil -> serie -> calcul -> afirmație doctrinară -> ipoteză clinică`

Dacă o concluzie nu poate fi urmărită înapoi până la datele și regulile care au produs-o, examinarea nu este suficient de transparentă pentru manual.

### Complementul

Capitolul 37 a separat VGP, ThKP, EKP și Vorder-/Hinter-Ich. Aici această separare devine disciplină de dosar. Complementul experimental poate fi calculat și păstrat, dar **nu intră automat în seria de profile libere și nu devine automat Hinter-Ich**.

Această regulă coincide cu soluția practică adoptată în proiectul digital Szondi3: complementul este păstrat ca profil formal separat până când relația clinică este explicit autorizată. Software-ul este folosit doar ca verificare de arhitectură, nu ca sursă doctrinară.

### Interdicții

- Nu reconstruim retrospectiv alegerile brute dintr-un profil dacă nu le avem.
- Nu pierdem datele brute după simbolizare.
- Nu amestecăm valori observate și valori normalizate prin Tabelle 13.
- Nu raportăm un calcul ambiguu ca și cum ar fi determinat.
- Nu facem din EKP o extensie automată a seriei VGP.
- Nu introducem date clinice ca și cum ar fi rezultate ale testului.

---

## 58. Testul în psihoterapie: interpretare, incertitudine și formulare clinică

### Verdict

**PĂSTRĂM, dar titlul trebuie să arate că miza este integrarea, nu „folosirea testului pentru a spune adevărul despre pacient”.**

### Titlu recomandat

**Integrarea clinică în psihoterapie: convergență, contradicție, incertitudine și formulare**

### Întrebarea centrală

> **Cum punem în relație materialul Szondi cu ceea ce știm clinic, fără să confundăm confirmarea, contradicția și lipsa de informație?**

### Ce susțin sursele

Deri formulează una dintre cele mai utile reguli pentru acest capitol: învățarea reală a interpretării trebuie făcută pe cazuri pentru care există **material clinic suplimentar**, iar interpretările trebuie confruntate cu **independent clinical evidence**. Ea recunoaște în același timp lipsa validării cantitative riguroase și avertizează împotriva utilizării testului ca instrument „streamlined” cu rezultat instantaneu.

Tot Deri spune că prezentarea unuia sau a două profile drept reprezentative poate fi făcută didactic numai dacă există dovezi externe că acestea reprezintă într-adevăr patternul stabil al persoanei; în practica obișnuită primele profile pot conduce la erori grosiere dacă sunt tratate drept structura de bază.

`Ich-Analyse` și `Triebpathologie` oferă multiple exemple în care Erbtafel, Krankengeschichte, profiluri și observația clinică se corectează și se completează reciproc. `Schicksalsanalytische Therapie` aduce materialul terapeutic propriu-zis: Lebensgeschichte, Krankengeschichte, vise, asociații, transfer, rezistență și schimbarea formelor de existență.

### Ce NU oferă sursele

Corpusul nu oferă un algoritm unic de tip:

`dacă testul spune X iar interviul spune Y -> concluzia este Z`.

Nu oferă nici o cadență clinică universală de readministrare în psihoterapie și nici un șablon unic de raport. Manualul trebuie să refuze să inventeze asemenea reguli sub numele lui Szondi.

### Propunerea proprie a manualului: integrarea în patru mișcări

Aceasta va fi prezentată explicit drept **procedură editorial-clinică a manualului**, nu doctrină primară:

1. **Descriere independentă a materialului testologic**  
   Ce observăm și calculăm înainte de a încerca să „potrivim” testul cu povestea pacientului?

2. **Confruntare cu materialul clinic**  
   Ce converge? Ce contrazice? Ce nu poate fi verificat? Ce apare în interviu dar nu în test și invers?

3. **Formularea ipotezelor cu statut epistemic**  
   Pentru fiecare afirmație: observație, calcul, doctrină Szondi, autor ulterior, inferență clinică sau explicație proprie a manualului.

4. **Sinteza clinicianului**  
   O formulare care integrează testul cu restul cazului, fără ca testul să primească ultimul cuvânt.

### Contradicția este informație

Un punct central al capitolului trebuie să fie:

> **Testul și clinica nu trebuie forțate să se confirme reciproc.**

O neconcordanță poate însemna:

- variabilitate reală;
- profil/fază momentană;
- material clinic încă incomplet;
- eroare de administrare sau calcul;
- limită a unei reguli interpretative;
- ipoteză doctrinară care nu se confirmă în caz;
- contradicție autentică ce trebuie păstrată.

Nu alegem automat explicația cea mai convenabilă.

### Utilizarea longitudinală

Seria Szondi este prin definiție temporală, iar corpusul clinic și terapeutic oferă numeroase comparații între faze și transformări. Totuși, manualul trebuie să distingă:

- **seria diagnostică/experimentală**;
- **readministrarea la momente clinice diferite**;
- **monitorizarea procesului terapeutic**.

Acestea nu sunt automat aceeași operație. Nu vom inventa un interval fix de readministrare terapeutică dacă sursele canonice nu îl autorizează.

### Formularea clinică recomandată

Structura finală a formulării poate fi:

`observații testologice -> calcule -> configurații/doctrină -> ipoteze -> convergențe clinice -> contradicții -> incertitudini -> sinteză a clinicianului`

Această arhitectură coincide intenționat cu principiul stratificat al proiectului digital Szondi3, unde observațiile, calculele, findings, incertitudinile și sinteza manuală a terapeutului sunt păstrate separat. Dar această coincidență este **design al proiectului**, nu dovadă doctrinară.

### Anti-inferențe obligatorii

- Testul nu „confirma” automat interviul și interviul nu „validează” automat testul.
- Absența unei constelații nu exclude un fenomen clinic.
- Prezența unei constelații nu dovedește diagnosticul.
- O schimbare de profil în cursul terapiei nu dovedește singură progres sau regres.
- Un indice numeric nu are prioritate asupra contradicțiilor clinice.
- O formulare bună poate conține propoziția: **„datele actuale nu permit o concluzie”**.

---

## 59. Un caz complet

### Verdict

**PĂSTRĂM. Este necesar. Dar nu trebuie să fie încă un „caz care demonstrează teoria”.**

### Titlu recomandat

**Cazul complet: de la alegeri brute la sinteza clinicianului**

sau, mai aproape de miza epistemică:

**Cazul complet: traseul verificabil al unei interpretări**

### Întrebarea centrală

> **Poate cititorul să urmărească fiecare pas al metodei și să distingă în orice moment faptul, calculul, doctrina și inferența?**

### De ce este justificat de corpus

Toate ramurile majore ale corpusului folosesc cazuri, genealogii, istorii de boală, serii de profile și exemple clinice. Deri are chiar un capitol separat „Syndromes and Case Illustrations” și revine asupra aceluiași caz după analiza formalizată pentru a arăta cum lectura calitativă a factorilor și vectorilor ajunge la o concluzie comparabilă. Ea insistă însă că adevărata învățare cere cazuri cu material clinic suplimentar și multă experiență.

Prin urmare, un capitol final de caz nu este ornament; este locul în care manualul verifică dacă și-a predat propria metodă.

### Dar cazul manualului trebuie construit altfel decât multe exemple istorice

Nu vrem un caz ales deoarece „iese perfect” și confirmă toate interpretările. Pentru scopul nostru pedagogic, cazul trebuie să conțină deliberat:

- cel puțin o configurație clară;
- cel puțin o ambiguitate formală sau interpretativă;
- o contradicție între test și materialul clinic sau între două niveluri ale testului;
- un element care rămâne necunoscut;
- o ipoteză care trebuie abandonată sau slăbită după confruntarea cu datele clinice.

Altfel cititorul nu învață metoda, ci numai retorica confirmării.

### Datele trebuie să fie suficiente pentru reproducere

Capitolul trebuie să ofere, în ordinea necesară:

1. situația examinării și întrebarea clinică;
2. protocolul brut sau o reprezentare suficientă pentru a reface scorarea;
3. profilele individuale complete;
4. seria și calculele reproducibile;
5. VGP și, dacă sunt folosite, complementele păstrate separat;
6. lectura factorială și vectorială;
7. Rand–Mitte și metodele complementare relevante;
8. aparatul serial și formulele;
9. sindromatica, numai unde criteriile sunt satisfăcute;
10. materialul clinic/anamnestic separat;
11. convergențe și contradicții;
12. formularea clinică finală cu grad de certitudine și anti-inferențe.

### Alegerea tipului de caz

Auditul nu fixează încă sursa cazului. Există trei opțiuni legitime, fiecare cu limite:

- **caz istoric din corpus** — fidel sursei, dar riscă să urmeze arhitectura și exemplele distinctive ale autorului și nu reprezintă cabinetul contemporan;
- **caz real contemporan profund anonimizat** — clinic viu, dar cere control etic și eliminarea oricărei informații identificabile;
- **caz sintetic/compozit creat pentru manual** — reproductibil și sigur editorial, dar trebuie declarat explicit ca didactic și nu poate fi folosit drept „validare clinică”.

### Recomandare provizorie

Pentru ediția de lucru, cea mai sigură opțiune este un **caz didactic sintetic/compozit**, construit astfel încât toate calculele să fie reale și coerente cu metoda, iar materialul clinic să fie explicit fictiv. Dacă ulterior există un caz real publicabil în condiții etice clare, el poate înlocui sau completa cazul sintetic.

### Regula de aur a capitolului 59

**Nu introducem nicio regulă nouă.**

Dacă cititorul întâlnește în cazul final un concept pe care nu l-a învățat deja, arhitectura cărții a eșuat. Capitolul 59 este examenul manualului, nu ultimul loc în care ascundem doctrina rămasă.

### Interdicții

- Nu alegem retrospectiv numai profilele care „se potrivesc”.
- Nu prezentăm materialul clinic în așa fel încât să facă inevitabilă interpretarea testului.
- Nu transformăm o concordanță într-o dovadă de validitate generală.
- Nu ștergem contradicțiile sau rezultatele nerezolvate.
- Nu folosim un caz real identificabil.
- Nu permitem software-ului să scrie sinteza clinicianului.

---

# Relația cu proiectul digital Szondi3

Această parte este locul unde proiectul digital poate fi cel mai util ca **laborator**, fără a deveni autoritate doctrinară.

Arhitectura actuală din `main` separă deja:

`administration -> scoring -> profiles -> series -> calculations -> findings -> uncertainties -> clinician synthesis`

și păstrează complementul experimental ca material formal separat până când relația lui clinică este explicit formalizată. Raportul clinic digital are câmpuri distincte pentru observații, calcule, findings cu surse/anti-inferențe, incertitudini și sinteza terapeutului; codul precizează că raportul nu fabrică diagnosticul și nu scrie sinteza terapeutului.

Manualul poate adopta **această disciplină de separare**, deoarece ea exprimă bine propriile reguli epistemice ale cărții. Dar fiecare sens psihologic și fiecare regulă Szondi trebuie să continue să vină din corpusul canonic, nu din implementare.

---

# Concluzii după tranșa 57–59

1. **Toate cele trei capitole sunt justificate și trebuie păstrate.**
2. Capitolul 57 devine capitolul despre **proveniența și organizarea datelor**, nu despre interpretare clinică.
3. Capitolul 58 devine capitolul despre **integrare clinică și incertitudine**, iar procedura de formulare va fi declarată explicit drept arhitectură a manualului, nu regulă canonică Szondi.
4. Capitolul 59 trebuie să fie un **caz reproducibil și epistemic dificil**, nu un caz demonstrativ care confirmă frumos teoria.
5. Corpusul susține puternic necesitatea materialului clinic suplimentar, a seriilor, a istoriei de caz și a confruntării dinamice; nu susține însă un workflow contemporan unic sau un șablon standardizat de raport. Acestea pot fi construite de manual numai cu etichetare epistemică explicită.
6. Principiul final al părții de cabinet devine:

`date -> calcul -> doctrină -> ipoteză -> confruntare clinică -> incertitudine -> sinteză umană`

și nu:

`test -> verdict`.

---

# Consecință pentru întregul audit

Prin această tranșă, arhitectura funcțională a celor 59 de capitole inițiale a fost parcursă integral. Auditul a produs însă mai multe scindări provizorii (`44A/44B`, `50A/50B`, `52A/52B`, `55A/55B`) și mai multe redenumiri/mutări.

**Următorul pas nu trebuie să fie redactarea capitolului 1 încă.** Mai întâi trebuie făcut un **audit de consolidare globală**:

- aplicarea tuturor deciziilor locale într-un cuprins unic revizuit;
- renumerotarea definitivă;
- verificarea acoperirii celor 10 surse împotriva cuprinsurilor lor integrale;
- detectarea ultimelor goluri și redundanțe;
- stabilirea anexelor care absorb materialul tehnic prea dens pentru corpul cărții;
- abia apoi declararea `BOOK_ARCHITECTURE` ca versiune de lucru pentru redactare.
