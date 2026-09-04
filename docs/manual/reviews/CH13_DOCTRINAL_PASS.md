# Capitolul 13 — Doctrinal pass

**Capitol:** Reacțiile factoriale: `+`, `−`, `±`, `0`  
**Verdict:** PASS AFTER TARGETED REMEDIATION + DIRECT PRIMARY-SOURCE RECHECK  
**Statut:** STABLE DRAFT

## Motivul redeschiderii punctuale

Cross-check-ul DRAFT-ului și al research-ului a semnalat o eroare locală: regula pedagogică Deri de tip 2:1 fusese tratată prea larg și clasifica greșit `4/2` și `2/4`.

Feedback-ul a fost reverificat independent în sursele canonice. Autoritatea doctrinară pentru clasificarea matură este `Lehrbuch der experimentellen Triebdiagnostik`, Tabelle 3 și paragrafele metodologice imediat precedente. Implementarea formală din `main/szondi3/scoring.py` și `tests/test_scoring.py` este folosită numai ca verificare operațională secundară.

Nu a fost necesară o rescriere structurală.

## Verificări refăcute direct în `Lehrbuch`

Textul metodologic formulează explicit:

- reacția pozitivă: cel puțin două fotografii simpatice și **nu mai mult de una** antipatică;
- reacția negativă: cel puțin două antipatice și **nu mai mult de una** simpatică;
- reacția ambivalentă: cel puțin două simpatice și simultan cel puțin două antipatice.

Tabelle 3 confirmă exhaustiv:

- `0`: exact 4 distribuții — `0/0`, `1/0`, `0/1`, `1/1`;
- pozitive: exact 9 distribuții — `2/0`, `2/1`, `3/0`, `3/1`, `4/0`, `4/1`, `5/0`, `5/1`, `6/0`;
- negative: exact 9 distribuții, simetric;
- ambivalente: exact 6 distribuții — `2/2`, `3/2`, `2/3`, `3/3`, `4/2`, `2/4`;
- `4/2 → ±!` și `2/4 → ±!`;
- bilanțul total este `4 + 9 + 9 + 6 = 28` distribuții.

Prin urmare corecția cerută de feedback este validă.

## Deri: contradicție reală, nu simplă reformulare

Reverificarea directă în `Susan Deri - Introduction to the Szondi Test` confirmă că Deri formulează regula pozitivă/negativă prin raportul de cel puțin `2:1` și enumeră `4/2` ca pozitiv, respectiv `2/4` ca negativ. Ea enumeră numai `2/2`, `3/2`, `2/3`, `3/3` ca ambivalente.

Aici există deci o **diferență formală reală** între Deri și metodologia matură din `Lehrbuch`. Pentru manual prevalează Szondi matur. Research-ul și DRAFT-ul au fost corectate în consecință.

## Corecții conceptuale

- nu toate cele patru forme sunt numite „direcții”;
- `+`, `−`, `±` sunt clasificări după `Tendenzrichtung`;
- `0` este `Nullreaktion` și aparține clasificării cantitative;
- formula de ansamblu folosită de manual este „cele patru forme/reacții factoriale de bază”.

## Elemente protejate

- **„`+` și `−` exprimă dominanțe, nu puritate.”**
- `Remanenz der Opposition` este confirmată direct de `Lehrbuch`: în reacțiile pozitive apare frecvent cel puțin o alegere negativă și invers;
- remanența NU devine o regulă 2:1: când ambele direcții ating minimum două alegeri, reacția este ambivalentă;
- **„`0` nu înseamnă că factorul lipsește din persoană.”** `Lehrbuch` spune explicit că Nullreaktion nu înseamnă absența tendinței din constituția ereditară, ci o situație dinamică actuală, cu excepții rare.

## Punte spre cap. 14

Tabelle 3 confirmă că aceeași formă direcțională poate avea încărcări cantitative diferite:

- `2/0 → +`;
- `4/0 → +!`;
- `5/0 → +!!`;
- `6/0 → +!!!`.

De asemenea, `4/2 → ±!` și `2/4 → ±!` demonstrează că **Tendenzrichtung și încărcarea cantitativă sunt axe distincte**.

## Guardrail pentru cercetarea cap. 14

Reverificarea directă în `Lehrbuch` confirmă:

- `Quantumspannung` privește supraîncărcarea cantitativă a unei reacții într-un profil și este marcată prin `! / !! / !!!`;
- `Tendenzspannungsgrad (TspG)` apare în aparatul de serie și este măsurat din suma reacțiilor ambivalente și postambivalente/nule ale factorului (`Σ± + Σ0`);
- cele două nu sunt sinonime.

## Forward hold: `0` liber vs `ø`

`Lehrbuch` confirmă explicit `Zwangs-Nullreaktion` în EKP: după o alegere VGP de 5 sau 6 fotografii ale unui factor, în complement mai rămâne una sau niciuna, iar reacția nulă poate fi produsă prin constrângere numerică, nu prin alegere liberă. Szondi cere marcarea ei prin zero barat și spune că asemenea reacții nu trebuie interpretate ca Nullreaktionen libere.

Precizare de statut al sursei: în pasajul verificat, Szondi spune explicit că `ø` nu trebuie interpretat ca o reacție nulă liberă; **nu am găsit în acest control o propoziție care să formuleze textual regula „ø nu intră în TspG”**. Excluderea automată din calculele de serie este de aceea păstrată ca protecție de implementare/editorială până când capitolul de serie va verifica regula în contextul său primar complet.

## Verdict final

**PASS. Remedierea cap. 13 este confirmată direct de corpusul canonic. Capitolul rămâne STABLE DRAFT.**