# SZONDI3 — BINARY ASSET ADMISSION RECORD

**Status:** COMPLETED / VERIFIED  
**Original purpose:** one-time whitelist-only transfer of documentary binaries into Szondi3  
**Admission commit:** `cddacb3ecfa86e44ae58b900115548593ad5c8df`

## Actual admitted paths

The completed transfer admitted exactly:

- 10 DOCX files at `sources/text/*.docx`;
- 8 PDF files at `sources/originals/*.pdf`;
- 48 WebP stimulus files at `assets/stimuli/*.webp`.

The local legacy container `Szondi_Carduri_Final/` was deliberately not committed.

## Excluded from the transfer

No source code, tests, canonical TXT, CSV, workflow, predecessor script, `project-state.json`, legacy ledger or photographed-person metadata was transferred with the binary admission commit.

## Verification

`docs/ASSET_ADMISSION_VERIFICATION.md` records the post-push verification:

- the 48-image Szondi3 Git tree is identical to the predecessor image tree;
- every admitted DOCX has the same Git blob identity and byte size as its predecessor source;
- every admitted PDF has the same Git blob identity and byte size as its predecessor source;
- the admission commit contains exactly 66 binary files.

Result: `BINARY_SOURCE_ADMISSION_PASS`.

## Historical note

Earlier versions of this document proposed temporary destination directories `sources/docx/` and `sources/pdf/`. The actual local source tree already used the stable paths `sources/text/` and `sources/originals/`, so no unnecessary duplication was performed. Those actual paths are now authoritative through `docs/SOURCE_ASSET_MANIFEST.md` and `config/source_catalog.json`.

This one-time transfer procedure is closed. Future source admission must be explicit, independently identity-verified and documented as a new provenance event.
