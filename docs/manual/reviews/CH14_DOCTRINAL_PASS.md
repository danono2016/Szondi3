# Capitolul 14 — Doctrinal pass

**Capitol:** Încărcare cantitativă, Quantumspannung și profilul simbolic  
**Verdict:** PASS AFTER DIRECT PRIMARY-SOURCE RECHECK  
**Statut:** DRAFT v1 / AUTHOR READER PASS PENDING

## Verificare independentă a feedback-ului

Feedback-ul tehnic primit pentru cap. 13–14 a fost reverificat direct în corpusul canonic, cu prioritate pentru `Lehrbuch der experimentellen Triebdiagnostik`, Tabelle 3 și secțiunile metodologice despre `Durchschnittsreaktionen`, `Vollreaktionen`, `Quantumspannung`, `Tendenzrichtung` și `Zwangs-Nullreaktion`.

Software-ul din `main` este folosit numai ca verificare secundară de consistență.

## Control direct pe `Lehrbuch`, Tabelle 3

Confirmat:

- reacțiile pozitive medii: `2/0`, `2/1`, `3/0`, `3/1 → +`;
- `4/0`, `4/1 → +!`;
- `5/0`, `5/1 → +!!`;
- `6/0 → +!!!`;
- seria negativă este simetrică;
- `4/2`, `2/4 → ±!`;
- `2/2`, `3/2`, `2/3`, `3/3 → ±` fără `!`.

Tabelle 3 confirmă astfel cele 28 de distribuții și separarea dintre `Tendenzrichtung` și marcajul de supraîncărcare.

## Nuanță cantitativă verificată

Textul lui Szondi despre `Vollreaktionen` confirmă că:

- `Vollreaktion` și `Quantumspannung` NU sunt sinonime;
- există **ambivalente Vollreaktionen** în care 4, 5 sau 6 fotografii ale factorului sunt împărțite între cele două direcții;
- `2/2`, `3/2`, `2/3`, `3/3` sunt ambivalente Vollreaktionen fără `!`;
- `4/2` și `2/4` sunt ambivalente Vollreaktionen cu `Quantumspannung`, notate `±!`;
- `3/3 → ±` este controlul decisiv că simplul total de șase alegeri nu produce automat Quantumspannung.

Prin urmare formularea din DRAFT — **`Vollreaktion ≠ Quantumspannung`** — este doctrinar justificată.

## Ce înseamnă formal `Quantumspannung`

În protocolul matur:

- 4 alegeri într-o singură direcție → `!`;
- 5 → `!!`;
- 6 → `!!!`.

La ambivalență, datorită limitei materiale de șase fotografii, singura supraîncărcare posibilă este `4/2` sau `2/4 → ±!`.

Marcajul exprimă `Überdruck` / `Quantumspannung` al unei tendințe, nu severitate clinică automată.

## Quantumspannung vs TspG

Reverificarea directă a aparatului de serie din `Lehrbuch` confirmă diferența cerută de feedback:

### Quantumspannung

- unitate: o reacție factorială într-un profil singular;
- bază: acumularea alegerilor într-o direcție;
- protocol: `! / !! / !!!`.

### Tendenzspannungsgrad (TspG)

- unitate: un factor urmărit într-o serie de profiluri;
- Szondi justifică măsurarea gradului de Tendenzspannung prin suma reacțiilor ambivalente și postambivalente/nule;
- formulă de lucru matură: `TspG = Σ± + Σ0`;
- folosit ulterior pentru ordonarea factorilor și aparatul de serie.

Cele două noțiuni nu sunt sinonime și nu trebuie predate ca două variante ale aceleiași „tensiuni”. DRAFT-ul cap. 14 le separă corect și nu calculează TspG.

## `0` liber vs `ø`

`Lehrbuch` confirmă explicit că EKP poate conține `Zwangs-Nullreaktionen` atunci când VGP a consumat 5 sau 6 fotografii ale factorului. Aceste reacții sunt marcate prin zero barat pentru a fi deosebite de reacțiile nule libere și Szondi spune că nu trebuie interpretate ca acestea.

Precizare importantă: sursa verificată susține explicit **diferența de statut și neinterpretabilitatea ca 0 liber**. Nu am găsit în pasajele controlate o formulare textuală care să spună direct „ø se exclude din calculul TspG”. Implementarea din `series.py` face această excludere ca protecție formală; manualul va revalida regula la capitolul de serie înainte de a o prezenta drept regulă szondiană explicită.

## Exemplul de profil complet

Exemplul sintetic din DRAFT este formal valid:

- `h 4/0 → +!`;
- `s 1/3 → −`;
- `e 2/2 → ±`;
- `hy 1/0 → 0`;
- `k 2/4 → ±!`;
- `p 3/1 → +`;
- `d 0/5 → −!!`;
- `m 1/1 → 0`.

Capitolul nu interpretează factorii și nu transformă profilul formal într-un diagnostic.

## Prag pedagogic

După cap. 14, cititorul poate reconstrui:

**card → alegere → factor → frecvență → reacție → încărcare → profil simbolic complet.**

Aceasta corespunde pragului arhitectural al Părții III.

## Verdict

**PASS. Conținutul formal al cap. 14 este confirmat direct de sursele canonice.** Reader pass-ul autorului rămâne singurul pas înainte de STABLE DRAFT.