# SZONDI3 — BINARY ASSET ADMISSION INSTRUCTIONS

**Purpose:** one-time whitelist-only transfer of documentary binaries into Szondi3.  
**Do not copy any source code, canonical TXT, CSV, workflow, script or project-state file.**

## Required repositories

- `danono2016/Szondi2`, branch `work/szondi-engine-master` — source DOCX and PDF evidence.
- `danono2016/szondi-`, branch `main` — 48 stimulus WebP binaries only.
- `danono2016/Szondi3`, branch `main` — destination.

## Recommended shell procedure

Run from an empty working directory:

```bash
git clone --branch work/szondi-engine-master --single-branch https://github.com/danono2016/Szondi2.git Szondi2-transfer
git clone --branch main --single-branch https://github.com/danono2016/szondi-.git szondi-legacy-transfer
git clone --branch main --single-branch https://github.com/danono2016/Szondi3.git Szondi3-transfer

mkdir -p Szondi3-transfer/sources/docx
mkdir -p Szondi3-transfer/sources/pdf
mkdir -p Szondi3-transfer/assets/stimuli

cp Szondi2-transfer/sources/text/*.docx Szondi3-transfer/sources/docx/
cp Szondi2-transfer/sources/originals/*.pdf Szondi3-transfer/sources/pdf/
cp szondi-legacy-transfer/app/baseline-v2.0.0/resources/assets/images/*.webp Szondi3-transfer/assets/stimuli/

cd Szondi3-transfer

# Safety check: expected counts before commit
printf 'DOCX: '; find sources/docx -maxdepth 1 -type f -name '*.docx' | wc -l
printf 'PDF:  '; find sources/pdf -maxdepth 1 -type f -name '*.pdf' | wc -l
printf 'WEBP: '; find assets/stimuli -maxdepth 1 -type f -name '*.webp' | wc -l

# Expected exactly: DOCX=10, PDF=8, WEBP=48

git status --short
# Inspect this output. Only sources/docx/, sources/pdf/, assets/stimuli/ should be new.

git add sources/docx sources/pdf assets/stimuli
git commit -m "Admit immutable source and stimulus binaries"
git push origin main
```

## Mandatory safety conditions

Before `git commit`, verify:

- exactly 10 `.docx` files;
- exactly 8 `.pdf` files;
- exactly 48 `.webp` files;
- no `cards.csv`;
- no `sources/canonical-text`;
- no Java/code/tests;
- no scripts/workflows;
- no `project-state.json`.

Do not rename or edit the binaries during transfer.

## What happens after the push

Do not create extraction code manually. After the binary push, the assistant will:

1. inspect the admitted files in Szondi3;
2. verify their identities against `docs/SOURCE_ASSET_MANIFEST.md` and the predecessor Git identities;
3. verify the 48-image set and mapping evidence;
4. update migration/admission status;
5. design and implement a new Szondi3 canonical extractor from zero;
6. compare newly generated canonical results with predecessor witnesses only after independent generation.

## If any count differs

Stop before committing and report the three counts. Do not compensate by copying additional predecessor folders.
