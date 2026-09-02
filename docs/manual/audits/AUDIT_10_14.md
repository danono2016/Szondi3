# Manualul Szondi — Audit de arhitectură

## TRANȘA 2 — CAPITOLELE 10–14

**Statut:** WORKING / DRAFT  
**Ramură:** `manual`  
**Scop:** audit structural al nucleului operațional: material -> administrare -> protocol factorial -> reacții -> încărcare/Quantumspannung/profil.

> Acest document continuă `docs/manual/ARCHITECTURE_AUDIT.md`. Este audit structural, nu cercetarea 10/10 de finalizare a capitolelor.

## Matrice de relevanță

| Cap. | SA | LEHR | IA-A | IA-B | THER-A | THER-B | TRIEB-1 | TRIEB-2 | DERI | MELON |
|---|---|---|---|---|---|---|---|---|---|---|
| 10. Materialul testului | CONTROL | CENTRALĂ | CONTROL | CONTROL | FĂRĂ CONTRIBUȚIE IDENTIFICATĂ | FĂRĂ CONTRIBUȚIE IDENTIFICATĂ | CONTROL | CONTROL | CONTRIBUTIVĂ | CONTRIBUTIVĂ |
| 11. Administrarea | CONTROL | CENTRALĂ | CONTROL | CONTROL | FĂRĂ CONTRIBUȚIE IDENTIFICATĂ | FĂRĂ CONTRIBUȚIE IDENTIFICATĂ | CONTROL | FĂRĂ CONTRIBUȚIE IDENTIFICATĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ |
| 12. De la alegeri la protocolul factorial | CONTROL | CENTRALĂ | CONTROL | CONTROL | FĂRĂ CONTRIBUȚIE IDENTIFICATĂ | FĂRĂ CONTRIBUȚIE IDENTIFICATĂ | CONTROL | CONTROL | CONTRIBUTIVĂ | CONTRIBUTIVĂ |
| 13. Reacțiile factoriale: `+`, `−`, `±`, `0` | CONTROL | CENTRALĂ | CONTROL | CONTROL | CONTROL | CONTROL | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ |
| 14. Încărcare cantitativă, Quantumspannung și profilul simbolic | CONTROL | CENTRALĂ | CONTROL | CONTROL | CONTROL | CONTROL | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ | CONTRIBUTIVĂ |

Abrevieri: SA=`SZ_SA_1948`; LEHR=`SZ_LEHR_1972`; IA-A/B=`SZ_IA_1956_A/B`; THER-A/B=`SZ_THER_1963_A/B`; TRIEB-1/2=`SZ_TRIEBPATH_1/2`.

---

## 10. Materialul testului

### Verdict
**PĂSTRĂM. Este primul capitol propriu-zis de tehnică și trebuie să fie foarte concret.**

### Nucleu canonic
`Lehrbuch` descrie aparatul ca o cutie cu șase compartimente, fiecare cu câte opt imagini: 48 de fotografii în total. Acesta este punctul operațional de plecare. Deri confirmă aceeași structură de 48 de fotografii împărțite în șase seturi de câte opt. Mélon o folosește în expunerea sa practică.

### Ajustare recomandată
Capitolul nu trebuie să fie doar inventar. Trebuie să răspundă la trei întrebări distincte:

1. **Ce vede examinatul?** — șase serii de câte opt chipuri.
2. **Ce știe examinatorul și examinatul nu trebuie să folosească?** — identitatea formală a fiecărei cărți, poziția în serie și factorul.
3. **Ce NU trebuie confundat cu sensul unei alegeri?** — diagnosticul istoric al persoanei fotografiate nu este un dicționar clinic al subiectului care alege.

### Frontiera cu software-ul
Mapping-ul digital al celor 48 de stimuli poate servi drept control practic al identității serie/poziție/factor, dar nu furnizează doctrina capitolului.

### Control vizual obligatoriu
Pentru ediția manualului vor trebui controlate direct în PDF/Test-Band ordinea, poziția, literele și eventualele diferențe între reproducerea istorică și setul digital. Orice tabel reprodus în carte va fi verificat vizual, nu reconstruit din OCR.

### Interdicție pedagogică
Nu explicăm încă semnificația psihologică a celor opt factori și nu cerem cititorului să memoreze „diagnosticul” fiecărui chip.

---

## 11. Administrarea

### Verdict
**PĂSTRĂM, dar trebuie să devină mai precis decât titlul actual și să distingă procedura primară de variantele ulterioare.**

### Nucleu canonic
În `Lehrbuch`, cele opt fotografii ale unei serii sunt expuse simultan în două rânduri de câte patru. Szondi cere alegeri relative de simpatie și antipatie, insistă asupra alegerii fără deliberare prelungită și descrie trecerea prin toate cele șase serii. După prima alegere sunt obținute cele 24 de alegeri ale prim-planului; cele 24 de imagini rămase intră în a doua alegere pentru profilul complementar experimental (EKP).

### Descoperire importantă de audit
**Sursele ulterioare nu trebuie amestecate mecanic cu procedura din `Lehrbuch`.**

Deri (1949) descrie, după cele șase serii și constituirea celor 12 imagini plăcute + 12 neplăcute, o alegere finală suplimentară a celor patru cele mai plăcute și patru cele mai neplăcute. `Lehrbuch` 1972 organizează explicit al doilea act de alegere în jurul celor 24 de imagini rămase și al EKP. Mélon prezintă la rândul său VGP -> alegerea celor 24 rămase -> EKP.

Aceste proceduri au straturi istorice diferite. Manualul nu va produce o procedură hibridă. În cercetarea dedicată capitolului trebuie stabilit exact:

- ce procedură este normativă în ediția târzie a lui Szondi;
- ce rol are pasul suplimentar descris de Deri;
- dacă există diferențe de ordine a alegerilor simpatic/antipatic între autori;
- ce trebuie prezentat ca istorie a tehnicii și ce trebuie recomandat practic.

### Titlu posibil
**Administrarea: de la prima serie la VGP și EKP**

Dacă EKP este considerat prea devreme pedagogic, titlul rămâne simplu, iar a doua alegere este prezentată numai procedural, fără interpretarea fundalului.

### Interdicție pedagogică
Nu explicăm încă sensul clinic al VGP/EKP și nu echivalăm automat EKP cu întreaga doctrină `Vorder-Ich/Hinter-Ich`.

---

## 12. De la alegeri la protocolul factorial

### Verdict
**PĂSTRĂM, dar schimbăm titlul.** Formula veche „De la alegeri la reacții factoriale” invadează capitolul 13.

### Titlu recomandat
**De la alegeri la protocolul factorial**

### Întrebarea exactă
> Cum sunt transformate cele 24 de alegeri concrete ale unui profil în opt perechi de numărări factoriale, înainte de atribuirea semnelor `+`, `−`, `±`, `0`?

### De ce
`Lehrbuch` separă metodologic construcția profilului de clasificarea cantitativă și calitativă a reacțiilor. Deri descrie foarte clar grila: opt coloane factoriale, alegerile simpatice deasupra liniei zero, cele antipatice dedesubt; profilul de prim-plan însumează 12 alegeri simpatice și 12 antipatice. Mélon descrie aceeași trecere de la 24 de alegeri la grila celor opt trebuințe.

### Decizie pedagogică
În acest capitol nu folosim încă sensuri psihologice. Cititorul trebuie să poată lua un protocol brut și să răspundă doar:

- câte alegeri simpatice are fiecare factor;
- câte alegeri antipatice are fiecare factor;
- dacă totalurile sunt intern consistente;
- cum se așază aceste valori în grilă.

### Frontiera cu capitolul 14
Capitolul 12 produce **matricea numerică**. Capitolul 13 o transformă în **modul reacției**. Capitolul 14 adaugă **încărcarea cantitativă/Quantumspannung și notația finală**.

### Interdicție pedagogică
Nu interpretăm încă un număr mare de alegeri ca „intensitate clinică” și nu folosim semnul de exclamare înainte de a explica regula sursei.

---

## 13. Reacțiile factoriale: `+`, `−`, `±`, `0`

### Verdict
**PĂSTRĂM, dar capitolul trebuie să distingă două axe pe care prezentarea simplificată le poate confunda: direcția reacției și încărcarea cantitativă.**

### Suport canonic
Cuprinsul `Lehrbuch` separă explicit:

- repartizarea **cantitativă**: reacții nule, medii (`Durchschnittsreaktionen`), pline (`Vollreaktionen`);
- repartizarea **calitativă după tendință**: pozitivă, negativă, ambivalentă.

În plus, figura dedicată celor patru reacții de alegere prezintă pozitivă, negativă, ambivalentă și goală/nulă. Deci notația pedagogică `+ / − / ± / 0` este legitimă, dar nu trebuie să facă invizibilă axa cantitativă.

### Ajustare recomandată
Capitolul trebuie să răspundă în această ordine:

1. Ce face o reacție **pozitivă**?
2. Ce face o reacție **negativă**?
3. Ce face o reacție **ambivalentă**?
4. Ce face o reacție **nulă / goală**?
5. Cum se separă această direcție de cantitatea alegerilor?

### Descoperire importantă: `0` nu este unic
`Lehrbuch` avertizează că în alegerea complementară poate apărea o reacție nulă **din constrângerea materialului**, atunci când pentru factor nu mai există suficiente fotografii disponibile. Mélon păstrează explicit o notație distinctă pentru această nulitate forțată/barată în EKP.

Prin urmare manualul trebuie să distingă:

- `0` rezultat al alegerii / al descărcării în sensul metodei;
- `0` forțat de disponibilitatea imaginilor în EKP.

Sensul clinic al complementului poate fi amânat, dar **distincția formală nu poate fi amânată**, altfel cititorul va învăța greșit notația.

### Interdicție pedagogică
Nu transformăm `+` în „bun”, `−` în „rău”, `±` în „indecizie” și `0` în „absența pulsiunii”. Aceste traduceri sunt doctrinar false sau grav simplificatoare.

---

## 14. Încărcare cantitativă, Quantumspannung și profilul simbolic

### Verdict
**PĂSTRĂM, dar schimbăm titlul din „Intensitate, Quantumspannung și construirea profilului”.**

### Titlu recomandat
**Încărcare cantitativă, Quantumspannung și profilul simbolic**

### De ce schimbarea este necesară
Termenul românesc „intensitate” riscă să sugereze o mărime psihologică generală. În sursă este vorba mai precis despre distribuția cantitativă a alegerilor, `Vollreaktion`, `Überdruck` și `Quantumspannung`, marcate prin semne de exclamare.

`Lehrbuch` definește reacțiile medii ca alegeri de două sau trei imagini în aceeași direcție și reacțiile pline când sunt alese mai mult de trei imagini ale aceluiași factor în aceeași direcție. Pentru reacțiile pozitive cu `Quantumspannung`, notația crește odată cu numărul de imagini alese; aceeași logică trebuie verificată vizual pentru variantele negative și ambivalente.

### Control vizual efectuat la audit
Paginile metodologice din `Lehrbuch` au fost renderizate și inspectate direct. Se confirmă că această zonă este puternic dependentă de layout: grilele de profil, exemplele de încărcare, cele zece profile schematice și Tabelul 3 nu pot fi preluate sigur numai din OCR.

### Funcția capitolului
La finalul capitolului, cititorul trebuie să poată trece de la matricea numerică la profilul simbolic complet:

`h s | e hy | k p | d m`

cu semnele direcției și marcajele de încărcare corect plasate.

### Regula de interpretare pe care o prefigurăm, dar nu o dezvoltăm încă
`Lehrbuch` precizează chiar în secțiunea metodologică faptul că interpretarea unui factor depinde de constelația factorului partener. Aceasta este o justificare canonică timpurie pentru regula noastră ulterioară: **niciun semn nu se citește singur**.

Totuși, în capitolul 14 o menționăm doar ca avertisment. Interpretarea propriu-zisă rămâne pentru Partea a VI-a.

### Interdicție pedagogică
Nu transformăm `!`, `!!`, `!!!` într-o scară clinică universală și nu atribuim diagnostice din `Quantumspannung` izolată.

---

# Concluzii după tranșa 10–14

1. **Nucleul 10–14 este foarte bine susținut de corpus și nu necesită eliminarea niciunui capitol.**
2. **Capitolul 12 trebuie redenumit** `De la alegeri la protocolul factorial`, pentru a separa numărarea de clasificarea reacției.
3. **Capitolul 14 trebuie redenumit** `Încărcare cantitativă, Quantumspannung și profilul simbolic`.
4. **Capitolul 13 trebuie să introducă formal nulitatea forțată din EKP**, fără a anticipa interpretarea complementului.
5. **Administrarea are o problemă istorică reală de sursă:** Deri, Szondi târziu și Mélon nu trebuie fuzionați într-o procedură unică fără control dedicat. Manualul va privilegia procedura primară Szondi și va atribui explicit variantele ulterioare.
6. După aceste ajustări, progresia operațională devine mult mai curată:

`material -> administrare -> protocol numeric -> mod de reacție -> încărcare/Quantumspannung -> profil simbolic`

7. **Pragul pedagogic al capitolului 14 se confirmă.** Abia aici cititorul trebuie să poată produce singur un profil formal complet. Până aici cartea nu îi cere să interpreteze psihologic profilul.
8. Pentru redactarea finală a acestor capitole, controlul vizual al `Lehrbuch` este obligatoriu pentru grile, Tabelul 3, reacțiile pline, semnele de exclamare și notația nulității forțate.

---

## Următoarea tranșă

Capitolele **15–26: cei opt factori și cele patru lecturi vectoriale S, P, Sch și C**.

Aici auditul va trebui să verifice nu doar dacă fiecare factor are material suficient, ci și dacă arhitectura actuală riscă să repete conținutul între capitolul factorului și capitolul vectorului și unde trebuie separate clar Szondi, Deri și Mélon.