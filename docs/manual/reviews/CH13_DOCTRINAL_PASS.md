# Capitolul 13 — Doctrinal pass

**Capitol:** Reacțiile factoriale: `+`, `−`, `±`, `0`  
**Verdict:** PASS AFTER TARGETED REMEDIATION  
**Statut:** STABLE DRAFT

## Motivul redeschiderii punctuale

Cross-check-ul DRAFT-ului și al research-ului cu `Lehrbuch`, Tabelle 3, plus implementarea formală din `main/szondi3/scoring.py` și `tests/test_scoring.py`, a identificat o eroare locală: regula pedagogică Deri de tip 2:1 fusese tratată prea larg și clasifica greșit `4/2` și `2/4`.

Nu a fost necesară o rescriere structurală.

## Verificări refăcute direct pe Tabelle 3

- `0`: exact 4 distribuții — `0/0`, `1/0`, `0/1`, `1/1`;
- pozitive: exact 9 distribuții, cu condiția matură `sympathetic >= 2` și `unsympathetic <= 1`;
- negative: exact 9 distribuții, simetric;
- ambivalente: exact 6 distribuții — `2/2`, `3/2`, `2/3`, `3/3`, `4/2`, `2/4`;
- `4/2 → ±!` și `2/4 → ±!` sunt acum corect clasificate;
- bilanțul total este `4 + 9 + 9 + 6 = 28` distribuții;
- tabelul corespunde implementării exhaustive din `tests/test_scoring.py`.

## Corecții conceptuale

- nu toate cele patru forme sunt numite „direcții”;
- `+`, `−`, `±` sunt clasificări după direcția/tendința reacției;
- `0` este `Nullreaktion`, adică formă pe axa cantitativă;
- formula de ansamblu folosită de manual este „cele patru forme/reacții factoriale de bază”.

## Elemente protejate

- **„`+` și `−` exprimă dominanțe, nu puritate.”**
- `Remanenz der Opposition` explică de ce `2/1` poate rămâne `+` și `1/2` poate rămâne `−`;
- remanența NU este transformată într-o regulă 2:1: când ambele direcții ating minimum două alegeri, reacția este ambivalentă;
- **„`0` nu înseamnă că factorul lipsește din persoană.”**

## Punte spre cap. 14

Controlul matur confirmă că aceeași direcție poate avea încărcări cantitative diferite:

- `2/0 → +`;
- `4/0 → +!`;
- `5/0 → +!!`;
- `6/0 → +!!!`.

De asemenea, `4/2 → ±!` și `2/4 → ±!` demonstrează că **direcția/tendința și încărcarea cantitativă sunt axe distincte**.

## Guardrail pentru cercetarea cap. 14

- `Quantumspannung` = încărcare cantitativă a unei reacții factoriale într-un profil, marcată prin `! / !! / !!!`;
- `Tendenzspannungsgrad (TspG)` = măsură de serie, calculată ulterior din `Σ0 + Σ±` pentru fiecare factor;
- cele două nu sunt sinonime și nu trebuie apropiate terminologic ca și cum ar măsura același lucru.

## Forward hold

`0` liber și `ø` (`Zwangs-Nullreaktion`) rămân distincte. În EKP, un `ø` poate fi impus numeric dacă VGP a consumat deja 5 sau 6 fotografii ale factorului. Distincția trebuie reactivată în capitolele despre complement și/sau serie și nu trebuie lăsată să intre tacit în calculele de serie.

## Verdict final

**PASS. Capitolul 13 poate fi închis ca STABLE DRAFT.**