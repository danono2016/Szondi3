# SZONDI3 — SOURCE & ASSET MANIFEST

**Status:** AUTHORITATIVE ADMISSION INVENTORY  
**Text-source predecessor:** `danono2016/Szondi2`, branch `work/szondi-engine-master`  
**Stimulus-asset predecessor:** `danono2016/szondi-`, branch `main`  
**Initial binary admission commit:** `cddacb3ecfa86e44ae58b900115548593ad5c8df`  
**Supplemental Triebpathologie PDF admission commit:** `b9ea8589bb8e6aa364b54f15e90c51775cd44960`

## Core admission rule

Szondi3 transfers documentary evidence, not predecessor implementation.

Original DOCX/PDF source files and the 48 stimulus images are admitted as source assets only after identity/provenance verification appropriate to their admission path. Generated canonical TXT from Szondi2 is NOT transferred as authoritative data. Szondi3 rebuilt canonical extraction independently from the admitted DOCX sources. Old canonical SHA-256 values remain comparison witnesses only.

The initial binary admission commit contained 10 DOCX, 8 PDFs and 48 stimulus WebP files. The authentic Triebpathologie I/II PDFs were admitted later in the supplemental commit above. The current documentary inventory is therefore **10 DOCX + 10 PDF + 48 stimulus WebP binaries**. The former eight-PDF state is a historical admission checkpoint, not a current evidence limitation.

## Authorized textual source set

| sourceId | layer | admitted DOCX | source DOCX SHA-256 witness | Szondi2 canonical SHA-256 witness | visual PDF |
|---|---|---|---|---|---|
| `SZ_SA_1948` | SZONDI_PRIMARY | `sources/text/SCHICKSALSANALYSE- Szondi.docx` | `06b24fca0ddb96659c0521786b18fb58d52a07ee4af8664f666383dd974d2a4b` | `3fbe1766dffe0460b9923ffaf23004b2cc8926ad0c8c8a992a39d724f1616a8c` | yes |
| `SZ_LEHR_1972` | SZONDI_PRIMARY | `sources/text/Szondi Lehrbuch der experimentellen Triebdiagnostik.docx` | `70e201933dd81d07005c90388947d3d30dc2d4b8d3bb05cdaa5943a3e6008f7b` | `8c6a2bb43214fcfce16146e37e7419e125ce3e989e66bfdf9a7d3de555a1e7fd` | yes |
| `SZ_IA_1956_A` | SZONDI_PRIMARY | `sources/text/Szondi Ich-Analyse 1.docx` | `e00c9a0ec985c7c5e3ec0ad5370de50236ed245b2d3b817d63131e1e77eb452b` | `76e2faa58102a532f21212ad36a1e213d090b0617c940e8733674baf9d190d13` | yes |
| `SZ_IA_1956_B` | SZONDI_PRIMARY | `sources/text/Szondi Ich-Analyse 2.docx` | `1b50dcdce9d7485faec2e5f3532bc50e03069a31e22469529ea900c31d6663db` | `5b2900b13106b26ee1fc22eb559f943ea79c7c3632f958b41d5f96febe486042` | yes |
| `SZ_THER_1963_A` | SZONDI_PRIMARY | `sources/text/Szondi Schicksalsanalytische Therapie 1.docx` | `2c092d1146f0ce20efc5b00a123b6061a9f1deb1b3201db1c131f4dc1783e26d` | `04635199a5b2467c3b2173d1b87b163bb9045f2c4651d523f3254c8af96bc4d3` | yes |
| `SZ_THER_1963_B` | SZONDI_PRIMARY | `sources/text/Szondi Schicksalsanalytische Therapie 2.docx` | `fd9aa0b70a3f54223fef6b9ad3818b44e8adb85b9e90967fdd17f36f2027c583` | `14d4a1d7409b8997b54c8c7b1f198110c9519b65dbe3bec645d4d301d86d4a14` | yes |
| `SZ_TRIEBPATH_1` | SZONDI_PRIMARY | `sources/text/Szondi Triebpathologie 1.docx` | `d40c5fa2e113c43a53a577e1bd5fc2890f0bbe132466a26326696ba1460ea776` | `e98e954f4cf76c558c743f14d7b63c14b482a08d507c9a8ea66677e852bdd26c` | yes — supplemental authentic original |
| `SZ_TRIEBPATH_2` | SZONDI_PRIMARY | `sources/text/Szondi Triebpathologie 2.docx` | `2190f4abdf2d2c080e8de76a2945c6014a6478a3b318890b803397ae3b0e8146` | `ee83b7b42c2945c969957b0e96eb1a41882db4bc12098c308d130f62c2f763d8` | yes — supplemental authentic original |
| `DERI_1949` | POST_SZONDI_TRADITION | `sources/text/Susan Deri - Szondi Introduction.docx` | `7cf062ce1f9f5a19402eeea1fa04ad9d7a8fee867a61843dfab27a77e2f4109c` | `f20cf222c20be21d1b3a194e49572e2cb8f3f46b71b4ad7bc83c233b6273ab3b` | yes |
| `MELON_1975` | POST_SZONDI_TRADITION | `sources/text/The_orie_et_pratique_du_Szondi_J_Me_lon.docx` | `fcd34deea5ccf4bdc25f00a59c3c4fcfb3e3e16460b92a1650829dccf19d67a8` | `38011edfaf8ebd34228b0211ba7d0528c279c1f429406ca765c2d4253d96f8a3` | yes |

The eight `SZ_*` entries are the primary Szondi doctrinal corpus. `DERI_1949` and `MELON_1975` are separate post-Szondian layers and never silently overwrite primary doctrine.

All 10 admitted DOCX files were verified byte-for-byte against their predecessor files by identical Git blob identity and byte size. The SHA-256 values above are retained provenance witnesses; `docs/ASSET_ADMISSION_VERIFICATION.md` records the initial transfer verification.

## Visual-arbitration PDF inventory

| admitted file | repository Git blob | bytes | admission witness |
|---|---|---:|---|
| `sources/originals/SCHICKSALSANALYSE- Szondi.pdf` | `041ecb2272690ed93503744e63474f0e8c635816` | 24,952,998 | initial transfer; predecessor identity verified |
| `sources/originals/Susan Deri - Szondi Introduction.pdf` | `d83a71da5467fc2bd3e469e988a346b7ce6839b2` | 24,007,866 | initial transfer; predecessor identity verified |
| `sources/originals/Szondi Ich-Analyse 1. Teil.pdf` | `950834b371fd01f70582257abd74bbcfc5807175` | 39,438,833 | initial transfer; predecessor identity verified |
| `sources/originals/Szondi Ich-Analyse 2. Teil.pdf` | `85022ebe103c8becf4b7e572dbc656f9f4f346c0` | 39,439,168 | initial transfer; predecessor identity verified |
| `sources/originals/Szondi Lehrbuch der experimentellen Triebdiagnostik.pdf` | `0eebce59029a1d6055e9274cbb64772247c6abf7` | 39,952,747 | initial transfer; predecessor identity verified |
| `sources/originals/Szondi Schicksalsanalytische Therapie 1. Teil.pdf` | `3860b3a215baf158dd60958e566108249197ffec` | 39,655,040 | initial transfer; predecessor identity verified |
| `sources/originals/Szondi Schicksalsanalytische Therapie 2. Teil.pdf` | `3d47f0f224bd0935fea3cace73b4dd19a4940560` | 39,655,287 | initial transfer; predecessor identity verified |
| `sources/originals/Szondi Triebpathologie 1. Teil.pdf` | `de905f28eb96b9da40bd4f6ce7e1cc852c94fe88` | 42,463,280 | supplemental authentic-original admission `b9ea8589...` |
| `sources/originals/Szondi Triebpathologie 2. Teil.pdf` | `0ed487efd94788c13651032479b2278eabde49f5` | 42,464,081 | supplemental authentic-original admission `b9ea8589...` |
| `sources/originals/The_orie_et_pratique_du_Szondi_J_Me_lon.pdf` | `ef1fec3114e65a661a316680b0cd3e3d2ead1e4e` | 12,246,079 | initial transfer; predecessor identity verified |

The initial eight PDFs were transfer-verified byte-for-byte against the predecessor by identical Git blob identity and byte size. The two Triebpathologie PDFs were admitted later as authentic originals in commit `b9ea8589bb8e6aa364b54f15e90c51775cd44960`; their repository blob identities above are the immutable binary witnesses. Their former absence is therefore closed and must not be treated as a current visual-arbitration limitation.

## Canonical-text restart rule

The restart constraints remain normative even though the implementation gate has since passed:

1. Use only the admitted DOCX sources as extraction inputs.
2. Specify Szondi3 canonical-access behavior before implementation.
3. Write a new extractor from that specification; do not copy the Szondi2 exporter.
4. Generate stable canonical access units and provenance identifiers.
5. Verify deterministic regeneration from the admitted DOCX files.
6. Only after independent generation compare new output hashes with Szondi2 witnesses.
7. Equality increases confidence but does not prove correctness by itself.
8. Difference triggers investigation; neither predecessor nor new output wins automatically.
9. PDF visual arbitration remains independent from textual extraction.

`docs/P0_CANONICAL_ACCESS_VERIFICATION.md` records `PASS — CANONICAL_ACCESS_IMPLEMENTATION_GATE`: the independent implementation was exercised against all ten admitted DOCX sources, regenerated deterministically and independently checked for structure/provenance. This does not by itself convert OCR text into infallible evidence; PDF visual arbitration remains the documentary arbiter where signs, formulas, tables, layout or typography conflict.

## Stimulus asset set

The 48 admitted WebP files live in `assets/stimuli/`.

- predecessor repository: `danono2016/szondi-`
- predecessor branch: `main`
- predecessor directory: `app/baseline-v2.0.0/resources/assets/images`
- predecessor tree SHA: `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`
- Szondi3 `assets/stimuli/` tree SHA: `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`

The identical tree SHA proves byte-for-byte and filename-for-filename identity of the complete 48-image set.

`docs/STIMULUS_MAPPING_MANIFEST.md` records the primary-source-verified series/position/factor/filename mapping from Lehrbuch printed p.357, Tabelle 19. The current mapping check is 48/48 files with 0 discrepancies and is authorized for the deterministic test layer.

Future runtime data may contain only stable card identity, series, position, factor and image identity/path. Historical photographed-person metadata stays outside runtime, Doctrine Registry, executable interpretation, Clinical Graph, integration and reports; it may exist only in isolated Help/historical documentation.

## Explicitly not admitted

The initial binary admission commit contains none of the following:
- generated canonical TXT/access derivatives;
- predecessor exporter/verifier scripts;
- `project-state.json`;
- 405-chunk historical ledger;
- Java source/tests;
- interpretive claims/guardrails/triggers;
- runtime CSV schemas;
- photograph-person metadata.

The later Triebpathologie PDF admission added only the two original PDF binaries and did not import predecessor implementation.

## Admission status

- Constitutional documents: `ADMITTED`.
- 10 DOCX textual sources: `ADMITTED_IDENTITY_VERIFIED`.
- 10 visual PDFs: `ADMITTED_IDENTITY_LOCKED` — eight initial transfer-verified PDFs plus two supplemental authentic-original Triebpathologie PDFs.
- 48 stimulus images: `ADMITTED_IDENTITY_VERIFIED`.
- Stimulus factor/series mapping: `PRIMARY_SOURCE_VERIFIED`.
- Canonical access layer: `IMPLEMENTED_AND_VERIFIED` at `CANONICAL_ACCESS_IMPLEMENTATION_GATE`.
- Executable predecessor code: `NONE_ADMITTED`.

Binary source admission remains accepted. Source identity, canonical reproducibility and semantic validity remain separate questions under `docs/VALIDATION_AND_RECOVERY.md`.
