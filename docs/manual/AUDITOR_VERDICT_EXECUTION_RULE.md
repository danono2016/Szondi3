# Auditor Verdict Execution Rule

**Status:** OBLIGATORIU / OPERATIONAL HARD RULE  
**Scope:** toate operațiile editoriale GitHub pentru Manualul Szondi după primirea unui verdict extern explicit de auditor.  
**Authority:** operationalizează regula din `MANUAL_FOUNDATION.md` conform căreia scriitorul/integratorul integrează verdictul extern și nu îl rejudecă.

## Regula

După ce un auditor extern a formulat un verdict explicit, scriitorul/integratorul **NU reverifică, NU reevaluează, NU reauditează și NU redeschide fondul verdictului**. Verdictul se aplică imediat, exact și rapid.

Fluxul obligatoriu este:

`verdict explicit -> aplicarea exactă a modificărilor/statutului cerut -> sincronizarea documentelor indicate -> PR -> merge -> gata`

## Interdicții operaționale

După verdict sunt interzise, dacă verdictul sau o eroare tehnică reală nu le cere explicit:

- fetch-uri GitHub redundante;
- căutări/explorări de tool-uri după ce operațiile necesare sunt deja cunoscute;
- verificări doctrinare, științifice sau stilistice suplimentare;
- teste speculative sau apeluri de probă;
- workflow-uri temporare;
- branch-uri suplimentare/de rezervă;
- recheck-uri circulare ale HEAD-ului, diff-ului, gate-ului sau statusului;
- orice operație care nu este necesară direct pentru aplicarea verdictului, sincronizare, PR sau merge.

## Regula de economie GitHub

Se folosesc **minimum de operații GitHub necesare**. Un apel GitHub trebuie să aibă un scop tehnic necesar și direct. Dacă rezultatul necesar este deja disponibil și valid în context, nu se cere din nou.

## Excepția unică

Se oprește aplicarea directă numai dacă apare o **eroare tehnică reală** care împiedică scrierea/merge-ul sau dacă două instrucțiuni externe explicite sunt incompatibile. În acest caz se raportează exact blocajul; nu se transformă blocajul tehnic într-un nou audit de fond.

## Formula de control

> **Auditorul decide. Integratorul aplică. Nu rejudecă verdictul. Nu consumă GitHub pentru reasigurare.**

> **După verdict: modificări cerute -> sincronizare -> PR -> merge -> gata.**
