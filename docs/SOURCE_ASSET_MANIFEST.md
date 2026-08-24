# SZONDI3 — SOURCE & ASSET MANIFEST

**Status:** AUTHORITATIVE ADMISSION INVENTORY  
**Predecessor evidence repository:** `danono2016/Szondi2`  
**Predecessor branch inspected:** `work/szondi-engine-master`

## Core admission rule

Szondi3 transfers documentary evidence, not predecessor implementation.

The original DOCX/PDF source files and the 48 stimulus images are admissible as `SOURCE_ASSET_TRANSFER` after identity verification. Generated canonical TXT from Szondi2 is NOT transferred as authoritative data. Szondi3 will rebuild canonical extraction independently from the admitted DOCX sources. Old canonical SHA-256 values are retained below only as comparison witnesses.

## Authorized textual source set

| sourceId | layer | predecessor DOCX | source DOCX SHA-256 | Szondi2 canonical SHA-256 witness | visual PDF |
|---|---|---|---|---|---|
| `SZ_SA_1948` | SZONDI_PRIMARY | `sources/text/SCHICKSALSANALYSE- Szondi.docx` | `06b24fca0ddb96659c0521786b18fb58d52a07ee4af8664f666383dd974d2a4b` | `3fbe1766dffe0460b9923ffaf23004b2cc8926ad0c8c8a992a39d724f1616a8c` | yes |
| `SZ_LEHR_1972` | SZONDI_PRIMARY | `sources/text/Szondi Lehrbuch der experimentellen Triebdiagnostik.docx` | `70e201933dd81d07005c90388947d3d30dc2d4b8d3bb05cdaa5943a3e6008f7b` | `8c6a2bb43214fcfce16146e37e7419e125ce3e989e66bfdf9a7d3de555a1e7fd` | yes |
| `SZ_IA_1956_A` | SZONDI_PRIMARY | `sources/text/Szondi Ich-Analyse 1.docx` | `e00c9a0ec985c7c5e3ec0ad5370de50236ed245b2d3b817d63131e1e77eb452b` | `76e2faa58102a532f21212ad36a1e213d090b0617c940e8733674baf9d190d13` | yes |
| `SZ_IA_1956_B` | SZONDI_PRIMARY | `sources/text/Szondi Ich-Analyse 2.docx` | `1b50dcdce9d7485faec2e5f3532bc50e03069a31e22469529ea900c31d6663db` | `5b2900b13106b26ee1fc22eb559f943ea79c7c3632f958b41d5f96febe486042` | yes |
| `SZ_THER_1963_A` | SZONDI_PRIMARY | `sources/text/Szondi Schicksalsanalytische Therapie 1.docx` | `2c092d1146f0ce20efc5b00a123b6061a9f1deb1b3201db1c131f4dc1783e26d` | `04635199a5b2467c3b2173d1b87b163bb9045f2c4651d523f3254c8af96bc4d3` | yes |
| `SZ_THER_1963_B` | SZONDI_PRIMARY | `sources/text/Szondi Schicksalsanalytische Therapie 2.docx` | `fd9aa0b70a3f54223fef6b9ad3818b44e8adb85b9e90967fdd17f36f2027c583` | `14d4a1d7409b8997b54c8c7b1f198110c9519b65dbe3bec645d4d301d86d4a14` | yes |
| `SZ_TRIEBPATH_1` | SZONDI_PRIMARY | `sources/text/Szondi Triebpathologie 1.docx` | `d40c5fa2e113c43a53a577e1bd5fc2890f0bbe132466a26326696ba1460ea776` | `e98e954f4cf76c558c743f14d7b63c14b482a08d507c9a8ea66677e852bdd26c` | no admitted predecessor PDF |
| `SZ_TRIEBPATH_2` | SZONDI_PRIMARY | `sources/text/Szondi Triebpathologie 2.docx` | `2190f4abdf2d2c080e8de76a2945c6014a6478a3b318890b803397ae3b0e8146` | `ee83b7b42c2945c969957b0e96eb1a41882db4bc12098c308d130f62c2f763d8` | no admitted predecessor PDF |
| `DERI_1949` | POST_SZONDI_TRADITION | `sources/text/Susan Deri - Szondi Introduction.docx` | `7cf062ce1f9f5a19402eeea1fa04ad9d7a8fee867a61843dfab27a77e2f4109c` | `f20cf222c20be21d1b3a194e49572e2cb8f3f46b71b4ad7bc83c233b6273ab3b` | yes |
| `MELON_1975` | POST_SZONDI_TRADITION | `sources/text/The_orie_et_pratique_du_Szondi_J_Me_lon.docx` | `fcd34deea5ccf4bdc25f00a59c3c4fcfb3e3e16460b92a1650829dccf19d67a8` | `38011edfaf8ebd34228b0211ba7d0528c279c1f429406ca765c2d4253d96f8a3` | yes |

The eight `SZ_*` entries are the primary Szondi doctrinal corpus. `DERI_1949` and `MELON_1975` are separate post-Szondian layers and must never silently overwrite primary doctrine.

## Visual-arbitration PDF inventory

The predecessor repository contains these eight original PDF assets eligible for documentary transfer:

| file | predecessor Git blob | bytes |
|---|---|---:|
| `SCHICKSALSANALYSE- Szondi.pdf` | `041ecb2272690ed93503744e63474f0e8c635816` | 24,952,998 |
| `Susan Deri - Szondi Introduction.pdf` | `d83a71da5467fc2bd3e469e988a346b7ce6839b2` | 24,007,866 |
| `Szondi Ich-Analyse 1. Teil.pdf` | `950834b371fd01f70582257abd74bbcfc5807175` | 39,438,833 |
| `Szondi Ich-Analyse 2. Teil.pdf` | `85022ebe103c8becf4b7e572dbc656f9f4f346c0` | 39,439,168 |
| `Szondi Lehrbuch der experimentellen Triebdiagnostik.pdf` | `0eebce59029a1d6055e9274cbb64772247c6abf7` | 39,952,747 |
| `Szondi Schicksalsanalytische Therapie 1. Teil.pdf` | `3860b3a215baf158dd60958e566108249197ffec` | 39,655,040 |
| `Szondi Schicksalsanalytische Therapie 2. Teil.pdf` | `3d47f0f224bd0935fea3cace73b4dd19a4940560` | 39,655,287 |
| `The_orie_et_pratique_du_Szondi_J_Me_lon.pdf` | `ef1fec3114e65a661a316680b0cd3e3d2ead1e4e` | 12,246,079 |

Absence of a paired PDF for the two `Triebpathologie` DOCX sources is a known evidence limitation, not permission to guess visual/OCR ambiguities.

## Canonical-text restart rule

1. Admit and hash-verify original DOCX sources.
2. Write a new Szondi3 extractor from source requirements; do not copy the Szondi2 exporter.
3. Generate new stable canonical text and provenance identifiers.
4. Verify deterministic regeneration from the DOCX sources.
5. Only then compare the newly generated SHA-256 values with the Szondi2 witness hashes above.
6. Equality increases confidence but does not prove doctrinal correctness by itself.
7. Difference triggers investigation of extractor/source handling; neither predecessor nor new output wins automatically.
8. PDF visual arbitration remains independent of canonical TXT extraction.

## Stimulus assets

Exactly 48 stimulus images are admissible as `SOURCE_ASSET_TRANSFER`.

The future runtime mapping may contain only:
- stable card identity;
- series;
- position;
- factor;
- image path/identity.

Historical metadata about photographed persons is excluded from runtime, Doctrine Registry, executable interpretation, Clinical Graph, integration and reports. It may exist only in isolated Help/historical documentation.

The 48-image identity manifest will be created before any administration code is written.

## Explicitly not admitted as source assets

The following predecessor artifacts are not copied as authoritative Szondi3 inputs:
- `sources/canonical-text/**` generated TXT/access derivatives;
- old exporter/verifier scripts;
- `project-state.json`;
- 405-chunk historical ledger;
- Java source/tests;
- interpretive claims/guardrails/triggers;
- runtime CSV schemas from predecessor software.

## Admission status

- Constitutional documents: `ADMITTED`.
- Textual source identities: `INVENTORIED`, binary transfer pending.
- Visual PDF identities: `INVENTORIED`, binary transfer pending.
- 48 stimulus images: `PENDING_IDENTITY_MANIFEST`.
- Canonical text: `NOT_YET_REBUILT_IN_SZONDI3`.
- Executable code: `NONE_ADMITTED_FROM_PREDECESSOR`.
