# Szondi3 — pachet curent de transfer

**Status:** MANDATORY SUCCESSOR ENTRY POINT  
**Repository:** `danono2016/Szondi3`  
**Linie clinică autoritativă:** `work/ai-clinical-provenance-strategy-001`  
**Data actualizării:** 2026-09-02  
**Audit forensic baseline:** `92befe8cc3a47af5f5c30d0ce56dc2d9b778b949`  
**P0 10/10 recovery checkpoint:** `061c172afb67b848d58295851ea22165ccbc1df5`  
**Rand–Mitte `s+!! / e0` verification checkpoint:** `90b5bcc54ee1cec2ccc25271ab22bc621e9db63a`  
**Technical finishing checkpoint:** `3637f1c56c90fd36a6378d8e20e40d317a5a932c`  
**Governance closure checkpoint:** `8f9166f987eb21bec14aa8b4a50ef4159f24e851`  
**PR umbrella:** #65 — OPEN / DRAFT / NOT MERGED

> Important: forensic findings below are preserved as historical audit context. Their former P0/CI/release defects have been remediated where this document explicitly says CLOSED. Always verify the live HEAD, CI and rulesets before writing.

---

## 0. Protocol obligatoriu pentru următorul chat

Nu reconstrui proiectul din memoria modelului sau din conversații vechi. Începe din repository.

Ordinea minimă:

1. citește integral acest document;
2. verifică live HEAD-ul `work/ai-clinical-provenance-strategy-001`, `main`, PR #65, CI și rulesets;
3. citește `docs/PROJECT_STATE.md`;
4. citește `docs/SOURCE_AUTHORITY_POLICY.md` și tratează PDF-ul original ca arbitru suprem la conflict OCR;
5. verifică `szondi3/interpretation_catalogue.py` și `doctrine/registry/`; nu presupune numărul sau sensul claim-urilor din memorie;
6. nu relua auditul general dacă nu apare o contradicție concretă;
7. nu deschide o relație clinică nouă fără reluarea explicită a dezvoltării clinice;
8. cere clinicianului decizia numai pentru o ambiguitate doctrinară/clinică reală care schimbă sensul.

---

## 1. Misiunea și regula de autoritate

Szondi3 separă strict:

```text
PRIMARY EVIDENCE
    -> DOCTRINE
    -> EXECUTABLE P2B
    -> SOFTWARE FINDINGS
    -> AI SYNTHESIS / WORDING
```

Nicio etapă downstream nu poate rescrie upstream-ul.

> **Correct-but-incomplete beats rich-but-invented.**

Nu se acceptă:
- diagnostic modern dedus automat din termeni istorici;
- biografie, comportament, periculozitate, crimă, pronostic sau motive inventate;
- transformarea unui profil în descrierea întregii persoane;
- transformarea complementului E.K.P. într-un predictor;
- RAG general, vector DB, ontology/graph DB, al doilea LLM-validator;
- scor Rand–Mitte inventat;
- scoring P1 alternativ;
- Fall 40 hard-coded ca doctrină.

---

## 2. Autoritatea documentară PDF/DOCX

`docs/SOURCE_AUTHORITY_POLICY.md` este politica curentă.

- PDF autentic/original = `PRIMARY_DOCUMENTARY_EVIDENCE`;
- DOCX creat atent cu ABBYY FineReader = `PRIMARY_DOCUMENTARY_EVIDENCE`;
- când concordă, au același rang documentar;
- la conflict, **PDF-ul original prevalează**;
- PDF-ul decide semnele `+ - ± 0`, `! / !! / !!!`, formulele, tabelele, layout-ul, tipografia și corupțiile OCR;
- DOCX rămâne canalul normal de full-text search, canonical extraction și provenance automatizată;
- canonical derivative nu poate corecta originalul.

Ierarhia autorilor rămâne separată:
- Szondi = `SZONDI_PRIMARY`;
- Deri / Mélon = `POST_SZONDI_TRADITION`.

---

## 3. P0 reproducibility boundary — CLOSED 10/10

Auditul din `92befe8c...` găsise o contradicție reală: 10 PDF-uri autorizate, dar numai 8 repository-locked. Aceasta este **închisă**.

Ambele originale Triebpathologie sunt acum în repository și identity-locked:

- `sources/originals/Szondi Triebpathologie 1. Teil.pdf` — Git blob `de905f28eb96b9da40bd4f6ce7e1cc852c94fe88`;
- `sources/originals/Szondi Triebpathologie 2. Teil.pdf` — Git blob `0ed487efd94788c13651032479b2278eabde49f5`.

Starea curentă a frontierei P0:
- 10 DOCX surse;
- 10 PDF originale/admitted;
- 48 stimuli WebP;
- `config/source_catalog.json` are `pdfPath` pentru ambele Triebpathologie;
- `config/evidence_lock.json` blochează identitatea tuturor celor 10 PDF-uri;
- P0 canonical cere exact 10 PDF paths unice.

Nu modifica retroactiv OCR/canonical text pentru a-l face să „semene” cu PDF-ul. Orice arbitraj vizual se consemnează separat.

---

## 4. CI și Git governance — CLOSED

P0 source inspection și P0 canonical access rulează direct pe:
- `main`;
- `work/ai-clinical-provenance-strategy-001`.

P2A rulează de asemenea pe linia clinică.

Repository governance este acum impus prin două rulesets GitHub active:

### `Szondi3 main protection` — ruleset `22055760`

Țintește numai `main` și:
- blochează ștergerea ramurii;
- blochează force-push;
- cere integrare prin pull request;
- cere `0` aprobări umane obligatorii;
- cere branch up-to-date înainte de merge;
- cere exact aceste 5 checks GitHub Actions:
  - `verify-foundation`;
  - `unittest`;
  - `inspect-docx`;
  - `canonical-access`;
  - `doctrine-registry`;
- bypass list este goală.

### `Szondi3 clinical branch protection` — ruleset `22056039`

Țintește numai `work/ai-clinical-provenance-strategy-001` și:
- blochează ștergerea;
- blochează force-push;
- permite direct fast-forward updates, pentru ca fluxul clinic existent să poată continua și CI să ruleze după push;
- nu cere PR pentru fiecare update;
- bypass list este goală.

La governance checkpoint `8f9166f...`, toate cele cinci workflow-uri au trecut:
- Foundation verification — run `33574954344` — `success`;
- Runtime tests — run `33574954334` — `success`;
- P0 source inspection — run `33574954139` — `success`;
- P2A doctrine registry — run `33574954207` — `success`;
- P0 canonical access — run `33574954146` — `success`.

---

## 5. P1 — verdict curent

Nu rescrie P1.

Auditul nu a găsit defect sistemic actual în:
- 48 stimuli mapping;
- foreground administration;
- E.K.P. scoring formal;
- factor scoring și quantum marks;
- forced null `ø`;
- profile/vector construction;
- ProfileSeries;
- exact Fraction arithmetic;
- TspQu, %Sy-Re, TspG, TspD;
- Tabelle 13 normalization;
- latency structure / danger / ventil;
- Haupttriebklasse;
- root-direction evidence / strict subclasses;
- complete/abbreviated Triebformel;
- Dur–Moll;
- Sozialindex.

Fostul risc `_capture()` este **închis**:
- `P1UnresolvedError` marchează fail-closed ambiguity legitimă;
- `_capture()` prinde numai această excepție tipizată;
- un `ValueError` generic de programare nu mai este mascat ca `UNRESOLVED` clinic.

---

## 6. P2B — verdict curent

Hardening-ul live rămâne valid:
- claim source IDs trebuie să fie exact sursele doctrinelor legate;
- doctrine review status admis: `SOURCE_VERIFIED`, `CLINICIAN_REVIEWED`, `ACCEPTED`;
- claim-urile noi cer lifecycle status explicit;
- epistemic ceiling este verificat pentru modurile epistemice;
- `CONDITIONAL` este formă logică, nu nivel de certitudine;
- `LIMITATION` / `WARNING` nu sunt forțate într-o scară artificială.

`AssertionMode` încă amestecă epistemic force cu functional/logical form. Nu refactoriza fără un caz concret care o cere.

`ActivationRecord` poate conține metadata mai bogată decât `ClinicianFinding/ReportFinding`. Nu face o migrare largă preventivă; extinde numai când un claim concret are nevoie de acele câmpuri downstream.

---

## 7. Clinical report / evidence packet / AI — technical finishing CLOSED

### Audited release manifest

`szondi3/clinical_release.py` oferă un release envelope determinist pentru un evidence packet deja construit și înregistrează:
- Git commit SHA;
- doctrine snapshot identity;
- doctrine-registry SHA-256;
- P2B release identity;
- P2B catalogue SHA-256;
- evidence-packet SHA-256;
- synthesis contract version;
- model identity.

Release policy este explicit:

`PREVIEW_ONLY_MANUAL_CLINICIAN_RELEASE`

cu `autonomous_ai_release = false`.

### E.K.P. evidence transport

Fostul gap este **închis**.

`AdministeredClinicalEvidencePacket` poate transporta complementul experimental cu:
- complement findings;
- doctrine exacte;
- factor symbols;
- facts;
- scope `EXPERIMENTAL_COMPLEMENT`;
- administered test number.

E.K.P. nu este introdus în seria foreground.

Validatorul determinist poate valida o propoziție complement-scoped numai față de bundle-ul exact activ claim/fact/doctrine/anti-inference.

### AI semantic boundary

Aceasta **nu este un bug rămas de reparat**. Este o limită deliberată:
- validatorul determinist dovedește support envelope-ul exact;
- nu pretinde că poate demonstra semantic fidelitatea oricărui text generat;
- de aceea AI rămâne preview-only și nu produce autonom output clinic final.

Nu introduce un al doilea LLM validator pentru a simula această garanție.

---

## 8. Frontiera clinică curentă — HOLD AT `000056`

Catalogul executabil ajunge la:

`IC_SZONDI_PRIMARY_000056`

Nu există claim clinic ulterior introdus în incrementul de finisare tehnică.

### `IC_SZONDI_PRIMARY_000055`

Configurație exactă:

`s+!!` împreună cu `e+` obișnuit.

Sursa primară descrie latura `e+` prin `Gutmachung` / `Gewissensschutz` în relația Rand–Mitte cu tensiunea la `s`.

Nu autorizează afirmații că persoana este violentă, agresivă, periculoasă, morală, sigură sau neapărat bine controlată.

### `IC_SZONDI_PRIMARY_000056`

Configurație exactă:

`s+!!` împreună cu `e0`.

În primul dintre cele două exemple din pasajul primar, Szondi folosește vocabularul istoric/testologic `Aggressionsgefahr` fără `ethischen Schutz`.

Reguli de siguranță:
- `e0` nu este generalizat în „lipsa conștiinței” sau „lipsa moralității”;
- `Aggressionsgefahr` nu devine afirmație factuală despre agresiune, violență, periculozitate sau criminalitate;
- nu se extinde la semne/quantum levels vecine prin analogie.

Supporting doctrine: `DR_SZ_TRIEBPATH_1_000004`.

**Nu deschide alt Rand–Mitte sau altă relație clinică până când dezvoltarea clinică nu este reluată explicit.**

---

## 9. Fall 40

Fall 40 rămâne **regression specimen**, nu runtime doctrine și nu centru de design.

Nu deriva reguli din caz doar pentru că explică bine cazul.

---

## 10. PR și branch history relevant

### PR #65

PR #65 este:
- OPEN;
- DRAFT;
- NOT MERGED;
- base `main`;
- head `work/ai-clinical-provenance-strategy-001`.

Rolul lui este explicit **clinical integration umbrella**, nu release gate.

A acumulat un diff foarte mare; nu-l merge automat doar pentru că CI este verde. Orice integrare finală în `main` trebuie să fie o decizie conștientă de release/integration boundary.

### PR #50

Rămâne research witness pentru Schicksalsanalyse. Nu este autoritate și nu trebuie merge-uit automat. Orice recuperare viitoare cere revalidare față de sursa curentă.

### `tmp-do-not-use`

Este branch vechi/superseded. Nu porni lucru de acolo.

### `work/p2b-multiple-triebgefahren-001`

Conține muncă structurală de păstrat ca witness, nu de merge-uit automat. Claim ID `000054` este deja ocupat în live.

---

## 11. Corpus coverage

Coverage-ul doctrinar este bogat pentru Lehrbuch și Ich-Analyse, parțial pentru Schicksalsanalyse și încă redus raportat la volum pentru Triebpathologie, Therapie, Deri și Mélon.

Aceasta este **muncă clinică viitoare**, nu defect tehnic și nu contradicție de sursă.

Nu completa coverage-ul mecanic și nu construi o matrice de reacții prin analogie.

---

## 12. Problemele auditului din 2026-09-02 — status actualizat

| Problemă identificată la baseline | Status curent |
|---|---|
| 10 PDF autorizate / 8 repository-locked | **CLOSED — 10/10** |
| Triebpathologie I/II lipsă din Git lock | **CLOSED** |
| P0 workflows fără direct clinical trigger | **CLOSED** |
| main/clinical fără protection | **CLOSED** |
| required checks neimpuse pe main | **CLOSED** |
| report fără audited build manifest | **CLOSED** |
| E.K.P. omis din evidence packet | **CLOSED** |
| `_capture()` masca generic `ValueError` | **CLOSED** |
| AI semantic fidelity pentru autonomous output | **DELIBERATE BOUNDARY — autonomous release disabled** |
| PR #65 foarte mare | **KNOWN GOVERNANCE FACT — not a code defect** |
| P2A/corpus coverage incomplet | **FUTURE CLINICAL WORK — not a defect** |
| branch-uri istorice / research witnesses | **PRESERVE / DO NOT AUTO-MERGE** |

Nu relua reparațiile marcate CLOSED fără o contradicție live nouă.

---

## 13. Fișiere minime la takeover

1. `docs/CHAT_TRANSFER_PACKAGE.md` — acest document;
2. `docs/PROJECT_STATE.md`;
3. `docs/SOURCE_AUTHORITY_POLICY.md`;
4. `docs/PROJECT_CONSTITUTION.md`;
5. `docs/VALIDATION_AND_RECOVERY.md`;
6. `config/source_catalog.json`;
7. `config/evidence_lock.json`;
8. workflow-ul relevant task-ului concret;
9. `szondi3/interpretation_catalogue.py`;
10. `szondi3/clinical_protocol.py`;
11. `szondi3/clinical_pipeline.py`;
12. `szondi3/clinical_evidence_packet.py`;
13. `szondi3/clinical_release.py`;
14. `doctrine/registry/` numai pentru task-ul concret.

Nu încărca istoricul larg dacă nu este necesar.

---

## 14. Immediate next action

**Nu există o reparație tehnică deschisă cunoscută la acest checkpoint.**

Frontiera clinică rămâne intenționat:

`HOLD AT IC_SZONDI_PRIMARY_000056`

Dacă dezvoltarea este reluată ulterior:
1. verifică live HEAD, PR #65, rulesets și CI;
2. nu redeschide auditul general;
3. alege următoarea relație numai din suport primar explicit;
4. urmează `primary source -> doctrine -> executable P2B -> exact trigger/guards -> focused tests -> verification`;
5. oprește-te pentru clinician numai la ambiguitate doctrinară/clinică reală.

---

## 15. Stil de lucru

Lucrează autonom pe programare, tests, routing, CI și provenance mechanics.

Nu cere clinicianului să valideze:
- branch mechanics;
- test wiring;
- schema trivială;
- refactor tehnic verificabil independent.

Nu se dorește:
- audit repetat al auditului;
- infrastructură stufoasă;
- micro-iterații fără valoare;
- re-arhitectare fără defect demonstrat.

Preferă modificări mici, generalizabile, source-grounded, grupate logic și verificabile.

---

## 16. Final handoff invariant

Prima întrebare a unui succesor este:

> **Este live HEAD-ul coerent cu acest checkpoint și sunt CI + rulesets încă verzi/active?**

Dacă DA:
- nu repara din nou P0, EKP, manifestul, `_capture()` sau branch protection;
- păstrează frontiera clinică `000056` până la reluare explicită.

Dacă NU:
- investighează contradicția concretă, nu reface auditul general.

> **Preserve Szondi first. Formalize second. Integrate third. Communicate last.**
