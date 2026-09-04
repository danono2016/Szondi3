# Manualul Szondi — Capitolul 12 — Cercetare 10/10

**Capitol:** 12. De la alegeri la protocolul factorial  
**Statut:** RESEARCH COMPLETE / READY FOR OUTLINE  
**Ramură:** `manual`

## Întrebarea capitolului

**Cum transformă examinatorul actele concrete de alegere din cele șase serii într-o înregistrare factorială verificabilă, fără să interpreteze încă semnificația reacțiilor?**

Cap. 11 a rămas pe partea persoanei examinate: chipuri, preferințe, respingeri, VGP și EKP. Cap. 12 trebuie să treacă pe partea examinatorului: întoarcerea cardului, identificarea factorului, transferul alegerii și numărarea. Nu trebuie încă să transforme distribuțiile numerice în `+ / − / ± / 0`; aceasta este problema cap. 13.

---

## 1. Sursa centrală matură: `Lehrbuch`, III. Herstellung des Triebprofils

Szondi descrie explicit trecerea de la alegeri la reprezentarea factorială.

Fișa grafică conține câte o coloană pentru fiecare dintre cei opt factori. Pentru fiecare factor există șase poziții deasupra liniei zero pentru alegerile simpatice și șase dedesubt pentru alegerile antipatice. Numărul de poziții marcate corespunde numărului de fotografii ale factorului respectiv care au fost alese în fiecare direcție.

În procedura istorică descrisă de Szondi:

- alegerile simpatice sunt marcate cu roșu;
- alegerile antipatice cu albastru;
- rezultatul este desenat după încheierea administrării;
- Szondi recomandă efectuarea reprezentării imediat, cât fotografiile sunt încă disponibile pentru control;
- cele 12 fotografii simpatice sunt ordonate după factor și numărate; aceeași operație se repetă pentru cele 12 antipatice.

Punct metodologic central:

> profilul grafic nu este produs prin impresie; este produs prin **numărarea alegerilor atribuite fiecărui factor**.

Aceasta este veriga dintre chip și sistem.

---

## 2. Două niveluri de înregistrare

Deri face foarte vizibilă o distincție care este pedagogic utilă:

1. **înregistrarea alegerii concrete** — pentru fiecare serie se notează inițiala factorului de pe verso pentru fiecare fotografie aleasă;
2. **agregarea factorială** — se numără de câte ori apare fiecare factor între cele 12 alegeri simpatice și cele 12 antipatice și se construiește reprezentarea grafică.

Deri insistă că examinatorul nu ar trebui să se bazeze numai pe profilul grafic. Inițialele fotografiilor alese trebuie păstrate ca înregistrare primară și ca mijloc de control.

Această distincție este foarte importantă pentru manual:

**alegerea brută precedă totalul factorial.**

Dacă totalul este greșit, trebuie să putem reveni la cardurile/inițialele concrete care l-au produs.

---

## 3. Ce conține partea de protocol brut

În forma descrisă de Deri, partea inferioară a fișei are:

- câte un rând pentru seriile I–VI;
- o zonă pentru `Sympathie`;
- o zonă pentru `Antipathie`;
- în fiecare căsuță se notează inițiala factorială de pe verso-ul fotografiei alese.

Aceasta păstrează simultan:

- direcția alegerii;
- seria din care provine;
- factorul fotografiei.

Pentru cap. 12 nu este necesar să păstrăm particularitatea procedurii Deri privind `final choice`; aceasta rămâne diferență istorică deja atribuită în cap. 11. Utilitatea lui Deri aici este mai ales transparența formei de înregistrare.

---

## 4. Ordinea factorilor

În fișele și profilele Szondi, factorii sunt organizați în ordinea sistemului:

`h, s, e, hy, k, p, d, m`

sub vectorii:

`S(h,s) — P(e,hy) — Sch(k,p) — C(d,m)`.

Această ordine nu este una dintre alegerile persoanei. Este ordinea aparatului de înregistrare.

Cap. 12 poate folosi deja aceste opt coloane deoarece literele au fost introduse conceptual în cap. 6. Nu trebuie încă să atașeze semne factoriale.

---

## 5. Aritmetica minimă obligatorie

Pentru VGP, administrarea produce exact:

- 12 alegeri simpatice;
- 12 alegeri antipatice.

Prin urmare, după transferul în cele opt coloane trebuie să fie adevărate două controale:

**suma totalurilor simpatice pe cei opt factori = 12**  
**suma totalurilor antipatice pe cei opt factori = 12**.

Fiecare factor are șase fotografii în materialul total, deci pentru fiecare factor:

- numărul alegerilor simpatice poate varia între 0 și 6;
- numărul alegerilor antipatice poate varia între 0 și 6;
- suma alegerilor simpatice și antipatice pentru același factor nu poate depăși 6 în VGP, deoarece există numai șase fotografii ale factorului în întregul material.

Aceasta este încă aritmetică de control, nu interpretare.

---

## 6. Exemplu didactic permis

Cap. 12 are nevoie de un protocol sintetic minimal care să arate transferul fără a preda cap. 13.

Exemplu:

Seria I: simpatice `h, p`; antipatice `e, m`  
Seria II: simpatice `s, h`; antipatice `hy, d`  
...

La final, examinatorul numără aparițiile fiecărei litere separat în cele două direcții.

Rezultatul poate fi arătat ca două rânduri de numere:

| factor | h | s | e | hy | k | p | d | m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| simpatice | ... | ... | ... | ... | ... | ... | ... | ... |
| antipatice | ... | ... | ... | ... | ... | ... | ... | ... |

Regulă: exemplul nu se convertește în `+ / − / ± / 0` în acest capitol.

---

## 7. Graficul istoric și protocolul conceptual al manualului

Szondi folosește un profil grafic cu pătrate deasupra și dedesubtul liniei zero, marcate istoric cu roșu și albastru.

Manualul poate descrie această formă istorică, dar nu trebuie să facă dependența logică a protocolului de culori.

Nucleul invariant este:

- factorul;
- direcția alegerii;
- frecvența alegerii.

Culoarea este convenție grafică a fișei istorice.

Această separare este utilă și pentru implementările digitale ulterioare: o interfață poate arăta diferit, dar dacă păstrează aceste trei informații nu schimbă operația logică de bază.

---

## 8. `Protokollierung` mai largă la Szondi

În `Lehrbuch`, Szondi spune că „protokollierung” nu se încheie cu desenarea profilului: pe o fișă separată sau pe verso pot fi notate date clinice, caracterologice, biografice și familiale.

Acest sens larg NU trebuie importat integral în cap. 12.

Capitolul are o funcție restrânsă: **protocolul factorial al alegerilor**. Dosarul clinic complet va reveni în Partea XI.

Este important doar să nu pretindem că pentru Szondi cuvântul „protocol” se reduce universal la cele opt coloane.

---

## 9. Ce aduce Mélon

Mélon oferă o expunere compactă a modului în care se construiește `protocole szondien` și trece repede de la alegeri la reacțiile factoriale.

Pentru cap. 12 este util ca control de continuitate al tradiției, dar trebuie oprit înainte de clasificarea reacțiilor. Tabelele lui despre `+ / − / ± / 0`, reacții pline și semne de tensiune aparțin cap. 13–14.

Mélon confirmă însă că protocolul este construit din numărul alegerilor simpatice și antipatice atribuite fiecărui factor.

---

## 10. Matrice de relevanță 10/10

| Sursă | Clasificare | Funcție pentru cap. 12 |
|---|---|---|
| `SZ_SA_1948` | CONTROL / GENEZĂ | confirmă experimentul și locul Triebdiagnostik în metodă; nu este sursa principală pentru forma matură a protocolului |
| `SZ_TRIEBPATH_1` | CONTROL APLICAT | folosește profile și fișe în forma deja construită; confirmă continuitatea aparatului, fără a depăși `Lehrbuch` pentru instrucțiunea matură |
| `SZ_TRIEBPATH_2` | PERIFERIC / CLINIC | utilizează profilele în sindromatică; nu adaugă o metodă de transfer necesară cap. 12 |
| `SZ_IA_1956_A` | PERIFERIC | presupune protocolul deja construit; relevant pentru interpretare ulterioară, nu pentru înregistrare |
| `SZ_IA_1956_B` | PERIFERIC | idem |
| `SZ_THER_1963_A` | PERIFERIC / CLINIC | profilul este instrument clinic deja disponibil; nu redefinește operația de transfer |
| `SZ_THER_1963_B` | PERIFERIC / CLINIC | idem |
| `SZ_LEHR_1972` | **CENTRALĂ** | `Herstellung des Triebprofils`: cele opt coloane, cele șase poziții simpatice/antipatice, numărare, culori istorice și control imediat |
| `DERI_1949` | **LATER TRADITION — foarte utilă practic** | separă înregistrarea inițialelor pe serii de agregarea grafică; insistă pe păstrarea datelor brute și controlul profilului |
| `MELON_1975` | LATER TRADITION — CONTROL | arată construcția protocolului și confirmă legătura număr alegeri → reacție; clasificarea reacțiilor este rezervată cap. 13 |

Matricea este închisă pentru funcția cap. 12. Nu există o contradicție relevantă între sursele centrale asupra principiului de transfer.

---

## 11. Anti-inferențe obligatorii

- protocolul factorial ≠ interpretarea profilului;
- frecvența unei litere ≠ încă sensul reacției factoriale;
- culoarea roșu/albastru ≠ proprietate doctrinară a factorului; este convenție grafică istorică;
- totalul factorial ≠ cardul individual; trebuie păstrată trasabilitatea de la card/serie la total;
- `Sympathie / Antipathie` în protocol ≠ „factor bun / factor rău”;
- nu introducem încă `+ / − / ± / 0`;
- nu introducem încă `! / !! / !!!` sau `Quantumspannung`;
- nu interpretăm factorii;
- nu transformăm sensul larg al `Protokollierung` la Szondi într-un capitol despre dosarul clinic complet.

---

## 12. Ipoteză de construcție a capitolului

1. **Pragul:** persoana a terminat de ales; examinatorul întoarce cardurile.
2. **Informația invizibilă până acum:** seria și inițiala factorială de pe verso.
3. **Protocolul brut:** păstrăm direcția, seria și factorul fiecărui card ales.
4. **Din carduri în coloane:** numărăm separat simpaticele și antipaticele pentru `h s e hy k p d m`.
5. **Exemplu complet sintetic:** șase serii → 24 de inițiale → două rânduri de totaluri.
6. **Controlul aritmetic:** 12 + 12; max. 6 per factor per material; trasabilitate.
7. **Profilul grafic istoric:** linia zero, roșu/albastru, fără a transforma încă numerele în semne.
8. **Ce nu știm încă:** aceeași pereche de numere poate trebui clasificată formal; aceasta naște cap. 13.

## Verdict cercetare

**RESEARCH COMPLETE.** Capitolul poate fi redactat fără deschiderea prematură a reacțiilor factoriale.