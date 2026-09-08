# CH41 — Doctrinal review

**Capitol:** 41 — `TspG`, `TspD` și `Latenzproportionen`: de la factor la tensiunea vectorială  
**Status:** DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CHAPTER STABLE / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE

## Baza de audit

- `research/CH41_RESEARCH.md` — RESEARCH COMPLETE / corpus pass 10/10 + bounded deep corpus pass + canonical visual formula check;
- `research/CH41_OUTLINE.md` — OUTLINE COMPLETE;
- `chapters/41_TspG_TspD_si_Latenzproportionen_de_la_factor_la_tensiunea_vectoriala_DRAFT.md` — STABLE DRAFT / DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED / STYLE PASS / READER PASS CLOSED / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE;
- `reviews/CH41_READER_PASS.md` — STYLE PASS / READER PASS CLOSED / CHAPTER STABLE / CH41-SHORT-01 SOURCE CONFLICT HOLD ACTIVE.

## Cronologia auditului extern

Auditul DRAFT v1 a dat:

**SCIENTIFIC HOLD — ONE MATERIAL CANONICAL CONFLICT + ONE CONCEPTUAL ADDITION + ONE TERMINOLOGY FIX.**

Au fost cerute și integrate în DRAFT v2:

1. transformarea `CH41-SHORT-01` din audit focus în **SOURCE CONFLICT HOLD**;
2. introducerea tezei primare din `Triebpathologie II` despre `Entladungsbereitschaft`, inclusiv calificarea `abgesehen von den Zwangsneurotikern`;
3. fix terminologic `täglicher TspG` -> **`Tages-TspG`**.

Recheck-ul extern al DRAFT v2 a verificat din nou de la zero punctele sensibile în `Lehrbuch` și `Triebpathologie II` și a dat verdictul final:

**CAP.41 — DOCTRINAL PASS / SCIENTIFIC AUDIT CLOSED.**

`CH41-SHORT-01` rămâne activ ca **SOURCE CONFLICT HOLD**, dar nu mai constituie un defect al capitolului.

Reader pass-ul extern ulterior a dat:

**PASS WITH MODERATE REVISION — REVISION REQUIRED BEFORE STABLE.**

Revizia stilistică cerută a fost integrată în DRAFT v3. Recheck-ul stilistic extern al DRAFT v3 a dat apoi verdictul final:

**STYLE PASS — READY FOR STABLE DRAFT.**

Reader pass-ul este astfel închis. Auditul doctrinar rămâne închis; recheck-ul stilistic a confirmat că integrarea nu a produs regresie doctrinară.

## Nucleul confirmat

- `TspG = Σ(0 + ±)` pe factor, în serie;
- `TspG ≠ Quantumspannung` și `!` nu intră în sumă;
- `Tages-TspG` este eticheta canonică pentru agregarea orizontală pe profil;
- `faktorieller TspG` este agregatul vertical pe factor și baza pentru `TspD`;
- în `Triebpathologie II`, `TspG` este `Maßstab für die Entladungsbereitschaft eines Bedürfnisses`;
- explicația reacției `±` ca `Vorphase der Entladung` este calificată prin `abgesehen von den Zwangsneurotikern`; formula `TspG = Σ0 + Σ±` rămâne neschimbată;
- `TspD = TspG mai mare − TspG mai mic` intravectorial;
- `TspD` exprimă diferența gradelor de `Entladungsbereitschaft` dintre factorii parteneri și măsoară cantitativ tensiunea / `Triebgefahr` intravectorială în doctrina lui Szondi;
- indexul vectorului aparține factorului cu `TspG` mai mic, tratat de Szondi ca dinamic mai puternic;
- `TspD = 0` nu identifică un singur `Vektorbild`;
- `Latenzgrad / Latenzgröße` și `Latenzproportionen` sunt păstrate în rangul și terminologia sursei;
- exemplul `13 : 4 : 4 : 0` este canonic, iar egalitatea `4:4` rămâne egalitate, fără tie-break inventat;
- Deri și Mélon rămân tradiție ulterioară;
- `TspQu` nu este omisiune: rămâne în cap. 44 conform arhitecturii;
- `Triebklasse/Unterklasse` rămân cap. 42, `Triebformel` cap. 43.

## CH41-SHORT-01 — SOURCE CONFLICT HOLD ACTIVE

Problema este o contradicție operațională internă în aceeași ediție a `Lehrbuch`-ului.

### Pasajul Schafir–Szondi

La pp. 285–286, instrucțiunile pentru seria scurtă spun:

`Diese Angaben können nur nach Umrechnung der Ergebnisse folgender Tabelle verwendet werden`

și introduc imediat `Tabelle 13`, care convertește sumele reacțiilor în raport cu o `angenommene Zehnerserie`.

### Contraexemplul canonic — Fall 18

În Fall 18, Szondi lucrează cu numai **6 profile** și tipărește:

`h=1, s=0, e=2, hy=2, k=5, p=4, d=3, m=3`.

Apoi calculează direct din aceste `TspG` brute:

`h−s = 1−0 = 1`  
`e−hy = 2−2 = 0`  
`k−p = 5−4 = 1`  
`d−m = 3−3 = 0`.

Rezultatul tipărit este:

`S=1, P=0, Sch=1, C=0`.

Dacă `TspG` ar fi convertite mai întâi prin `Tabelle 13`, pentru șase profile:

`1→2`, `0→0`, `2→3`, `5→8`, `4→7`, `3→5`,

ar rezulta:

`S=2, P=0, Sch=1, C=0`.

Dacă am converti direct `TspD` brute, ambele diferențe `1` ar deveni `2`, deci ar rezulta:

`S=2, Sch=2`.

Niciuna dintre variante nu reproduce Fall 18.

### Concluzia HOLD-ului

Sursa primară nu permite stabilirea neechivocă a unei reguli universale pentru seriile de 3–9 profile.

Manualul nu autorizează:

- nici `TspG brut -> Tabelle 13 -> TspD`;
- nici `TspD brut -> Tabelle 13`;

ca regulă canonică universală.

**Ambiguitatea documentată este preferabilă certitudinii inventate.**

HOLD-ul privește ordinea operațională a conversiei pentru seria scurtă. El nu invalidează mecanica direct documentată a `TspG`, `TspD` și `Latenzproportionen` și nu împiedică stabilitatea capitolului.

## Gate

**Auditul doctrinar și reader pass-ul sunt închise. Capitolul 41 este STABLE DRAFT.**

`CH41-SHORT-01` rămâne SOURCE CONFLICT HOLD ACTIVE și nu se „rezolvă” editorial fără o sursă canonică nouă și explicită.

Următorul pas autorizat este **research-ul pentru capitolul 42**.