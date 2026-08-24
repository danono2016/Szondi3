# SZONDI3 — ASSET ADMISSION VERIFICATION

**Status:** VERIFIED  
**Admission commit:** `cddacb3ecfa86e44ae58b900115548593ad5c8df`  
**Classification:** `SOURCE_ASSET_TRANSFER`

## Verified admission set

The admission commit contains exactly 66 binary files and no predecessor implementation:

- 10 DOCX source files in `sources/text/`;
- 8 PDF visual-arbitration files in `sources/originals/`;
- 48 WebP stimulus files in `assets/stimuli/`.

No Java source, tests, scripts, workflow, generated canonical TXT, `project-state.json`, runtime CSV or photograph-person metadata was admitted in this transfer.

## Identity verification

### Stimulus images

The Git tree for `assets/stimuli/` in Szondi3 is:

`bdb6a6006e8f988efc6a0023ddc04bbbc339f251`

This is identical to the immutable predecessor tree at:

`danono2016/szondi-:main/app/baseline-v2.0.0/resources/assets/images`

Therefore all 48 filenames and binary contents are byte-identical to the admitted predecessor stimulus set.

### DOCX sources

Every file in `Szondi3:sources/text/` has the same Git blob identity and byte size as the corresponding file in `danono2016/Szondi2`, branch `work/szondi-engine-master`, `sources/text/`.

This establishes byte-for-byte transfer identity for all 10 admitted DOCX files.

### PDF sources

Every file in `Szondi3:sources/originals/` has the same Git blob identity and byte size as the corresponding file in `danono2016/Szondi2`, branch `work/szondi-engine-master`, `sources/originals/`.

This establishes byte-for-byte transfer identity for all 8 admitted PDF files.

## What this verification proves

It proves transfer integrity and set identity. It does not prove that OCR text is error-free, that every historical edition is optimal, or that the predecessor stimulus factor mapping is doctrinally correct. Those are separate source-validation questions.

In particular, the 48 image binaries are now admitted as immutable assets, while series/position/factor mapping remains evidence pending independent primary-source revalidation before runtime administration is implemented.

## Canonical derivatives

No canonical TXT derivative from Szondi2 was admitted. Szondi3 must generate its own canonical access layer from the admitted DOCX sources under `docs/CANONICAL_ACCESS_SPEC.md` and compare predecessor canonical hashes only after independent generation.

## Result

`BINARY_SOURCE_ADMISSION_PASS`
