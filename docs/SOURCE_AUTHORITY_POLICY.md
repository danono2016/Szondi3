# SZONDI3 — DOCUMENTARY SOURCE AUTHORITY POLICY

**Status:** AUTHORITATIVE AMENDMENT  
**Clinician admission:** 2026-09-02  
**Scope:** all documentary sources admitted to the Szondi3 project

## Core rule

The authentic/original PDF and the clinician-created ABBYY FineReader DOCX replica are both admitted as **PRIMARY_DOCUMENTARY_EVIDENCE** for the work they reproduce.

The DOCX replicas were created carefully by the clinician from the authentic originals in ABBYY FineReader. They therefore do not constitute a lower doctrinal source layer merely because they are OCR-derived. They are the project's machine-accessible textual replicas used for search, deterministic extraction, addressing and textual provenance.

The original PDF remains the **supreme source representation whenever the PDF and OCR/DOCX differ or when the meaning depends on typography or layout**.

Therefore the project rule is:

> **equal documentary rank when concordant; original PDF prevails on conflict.**

## What the PDF controls

When there is any discrepancy or uncertainty, the original PDF controls at minimum:

- exact wording visible on the original page;
- factor signs and reaction signs;
- `!`, `!!`, `!!!` and other quantum/intensity marks;
- formulas and mathematical/testological notation;
- tables, columns, rows and cell alignment;
- figures, diagrams and graphic labels;
- ordering and spatial relations;
- page layout and typography when they affect meaning;
- any other content that may have been altered, omitted or corrupted by OCR.

No OCR string, canonical derivative or remembered formula may overrule a visually verified original PDF.

## What the DOCX controls operationally

The ABBYY DOCX replica remains the normal input for:

- deterministic canonical text extraction;
- full-text search;
- stable unit addressing;
- machine-readable source excerpts;
- automated provenance verification of textual anchors.

This is an **operational role**, not a higher source-authority rank.

When the DOCX is clear and concordant with the PDF, it may be used directly. When a sign, formula, table, layout or wording is doubtful, the PDF must be consulted and its reading prevails.

Canonical DOCX-derived records are not silently rewritten. A PDF-based correction or arbitration is recorded explicitly in the reviewed doctrine/provenance layer while retaining the original OCR evidence as the machine-addressable witness.

## Doctrinal layer is a different question

Documentary authority must not be confused with author/doctrinal authority.

The authentic PDF of a work is primary documentary evidence for that work, but the existing doctrinal layers remain unchanged:

- Szondi's own works remain `SZONDI_PRIMARY`;
- Deri and Mélon remain `POST_SZONDI_TRADITION` and must be attributed as such.

Thus an original Deri or Mélon PDF is not made into Szondi doctrine by this policy. It is simply the supreme documentary representation of Deri's or Mélon's own text.

## Triebpathologie I and II

The project-uploaded files:

- `Szondi Triebpathologie 1. Teil.pdf`
- `Szondi Triebpathologie 2. Teil.pdf`

are explicitly admitted by the clinician as authentic original PDFs and therefore have `PRIMARY_DOCUMENTARY_EVIDENCE` authority, including supreme arbitration authority over their ABBYY DOCX replicas.

Their current `pdfPath: null` in `config/source_catalog.json` means only that the PDF binaries are not yet locked under `sources/originals/` in the Git repository. It does **not** mean that the PDFs are doctrinally or clinically unadmitted.

Until their binaries are repository-locked, a reviewed record may cite the project PDF by its exact uploaded title and record clinician/visual arbitration explicitly. Once the binaries are placed under `sources/originals/`, `pdfPath` and `config/evidence_lock.json` should be updated without changing their already-admitted documentary authority.

## Conflict rule

If the following disagree:

`original PDF` vs `ABBYY DOCX` vs `canonical extraction`

then the authority order for resolving source content is:

`original PDF` > `ABBYY DOCX` > `canonical derivative`.

The lower representation remains preserved as provenance; it is not erased merely because it contains an OCR error.

## Supersession

This policy supersedes any older project wording that:

- describes admitted PDFs as merely secondary or optional "visual aids";
- implies that an OCR/DOCX extraction can overrule the original PDF;
- treats the absence of a repository `pdfPath` as evidence that an authentic project-uploaded PDF is not admitted;
- states that `SZ_TRIEBPATH_1` or `SZ_TRIEBPATH_2` lacks an admitted PDF source after the clinician's 2026-09-02 admission.

Existing rules about immutable Git identity, deterministic canonical extraction, explicit provenance and separation of Szondi from post-Szondi tradition remain in force.

## Final invariant

> **For documentary truth, read the original. The ABBYY DOCX gives deterministic access to the original; it does not outrank it. When both agree, both carry primary documentary authority. When they disagree, the original PDF decides.**
