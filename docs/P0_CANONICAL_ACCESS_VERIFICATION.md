# SZONDI3 — P0 CANONICAL ACCESS VERIFICATION

**Status:** `PASS — CANONICAL_ACCESS_IMPLEMENTATION_GATE`  
**Phase:** `P0 — Constitution + Sources`  
**Change class:** `SOURCE_ACCESS`  
**P0 overall gate:** `IN_PROGRESS` — **`P0_SOURCES_PASS` is NOT declared**

## 1. Scope of this verification

This record establishes that the independent Szondi3 canonical-access implementation required by `docs/CANONICAL_ACCESS_SPEC.md` has been implemented, exercised against all ten admitted DOCX sources, regenerated deterministically and independently checked for source structure/provenance.

It does **not** establish OCR correctness, doctrinal correctness, stimulus factor mapping, scoring, interpretation, or completion of P0.

No Szondi2 exporter, executable code, old canonical TXT or predecessor canonical output was consulted before or during the independent Szondi3 implementation, generation or verification described here.

## 2. Implementation milestone

PR **#6** — `Implement P0 canonical access gate`

- final PR head: `46587f75d494ef896ae99482bcb73c102631abbf`
- merged to `main` as: `f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`
- integrated extractor: `scripts/canonical_access.py`
- extractor blob on final PR head: `cf394843c6c2f05c72e49f89d933890d74e34d5c`
- independent verifier: `scripts/verify_canonical_access.py`
- spec-derived test plan: `docs/P0_CANONICAL_ACCESS_TEST_PLAN.md`

The final implementation is a single extractor. The temporary stream-extension wrapper used while investigating real-corpus field behavior was removed before merge; stream-spanning field state and reviewed `w:tblPrEx` structural preservation are integrated directly into `scripts/canonical_access.py`.

## 3. Verified behavior

The merged gate verifies, at minimum:

- admitted DOCX input identity against `config/source_catalog.json`;
- explicit `word/*.xml` part classification and fail-closed handling of unknown possibly meaningful parts;
- body paragraph/table order and hierarchical tables;
- merge metadata and reviewed row structural metadata including `w:tblPrEx`;
- visible tab/break controls without conflating paragraph tab-stop definitions with visible tabs;
- footnote/endnote identity and body-reference linkage;
- separate header/footer story preservation, including empty story parts;
- complex fields across paragraph/table boundaries, field events and displayed results;
- simple fields;
- hyperlink target provenance and bookmark metadata;
- drawings, legacy pictures, embedded objects, text boxes and `mc:AlternateContent` with visual-arbitration markers;
- stable source-local `U######` unit IDs;
- deterministic UTF-8/LF serialization;
- two complete clean generations with byte-identical outputs;
- independent source-structure/provenance verification without reusing extractor traversal helpers.

## 4. Test and CI witnesses

Final PR-head CI on `46587f75d494ef896ae99482bcb73c102631abbf`:

- Foundation verification run `32794255407` — `SUCCESS`
- P0 source inspection run `32794255405` — `SUCCESS`
- P0 canonical access run `32794255408` — `SUCCESS`
- canonical job `97642137093` — all steps `SUCCESS`

Post-merge `main` CI on `f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`:

- Foundation verification run `32794400019` — `SUCCESS`
- P0 source inspection run `32794400074` — `SUCCESS`
- P0 canonical access run `32794400061` — `SUCCESS`
- canonical job `97642566458` — all steps `SUCCESS`

The main canonical job ran **20 tests**, all passing. The two real-corpus regressions added after fail-closed investigation were:

- `test_field_can_span_paragraph_boundaries`
- `test_table_property_exceptions_are_preserved_as_structural_metadata`

Both complete canonical generations on `main` passed `diff -ru` with no differences. The independent verifier returned `"verification": "PASS"` for all ten sources.

## 5. Canonical artifact identity

Final PR artifact:

- artifact ID: `9544260129`
- name: `p0-canonical-access`
- ZIP size: `5,498,294` bytes
- GitHub artifact ZIP digest: `sha256:dbb735efed342f67ab985821fad172cec1bdd6bf2f31691e53f4f170e3bc89fd`

Post-merge `main` artifact:

- artifact ID: `9544306267`
- name: `p0-canonical-access`
- ZIP size: `5,498,294` bytes
- GitHub artifact ZIP digest: `sha256:df8804fc0c4a10d226818327c8c6ad793e4719c1db7ac4c6dbd8c915592871dd`

ZIP-package digests differ because GitHub artifact packaging metadata is not the canonical content identity. The unpacked canonical contents of the final cleaned PR artifact and the post-merge `main` artifact were compared file-for-file and are byte-identical. They also match the previous independently green canonical artifact used during PR investigation.

SHA-256 of canonical content manifest `canonical-hashes.json`:

`4629e5730f298043cfd42c541d0d319fecb6da45ec6cb9f8b5a807e91dc59479`

The canonical artifact contains exactly 21 files: 10 JSONL source records, 10 source inventory JSON files and the manifest.

## 6. Canonical output hash inventory

| Source | JSONL SHA-256 | Inventory SHA-256 |
|---|---|---|
| `DERI_1949` | `6d452ac913172d76ec79f0a8916dfe280d741e74237813506b451e4d9dce4319` | `02dfdcbb2e42d626233310057c9d518197e5a4649606bf31ee4ad16093d81a51` |
| `MELON_1975` | `ad458a802f8b618b2b3263a98ffd0c092bddb30b5b32b1711bec186f6581cd95` | `e57366623d52744d0e712a086eab5e6c901f8d8403c85a06e7060d5b90400fab` |
| `SZ_IA_1956_A` | `6c01a36bf66a1c42d29a654b4da329a9db4d887c02c8ec2fe1116252c6d13b33` | `9466544be60bc5290ccedf8e1e550dc26ce456eb6eee774343c5c84cada64c1d` |
| `SZ_IA_1956_B` | `7e1b530666d92644aae99ec53831cccdcfba25df425fbb17ba6447f88d348b7b` | `dff9f0627ab3562ef359804552b57d530bbf011deb15a8b9a124ad4f0727533a` |
| `SZ_LEHR_1972` | `568f14f6fa2805d5e045febd8ab80fd3852a4106429eea66727ac205a3bf48e3` | `216697bdc49aa64bd7eef077ab9d110f77dfb3a6c6f8cc292d4557f89d472d99` |
| `SZ_SA_1948` | `c5a0abc75aff24d7fba1f53f958878bc7805ae474f81f35af60cc71ece81f968` | `a72f8060cb522e85cc730b34b80f99755e24f7e5ae6403fbdd39a768bdeabf9e` |
| `SZ_THER_1963_A` | `76133a2f3668c137187731f9b1f824376ce424d4fb963489e52ea21740b674d3` | `4c40f03ea194cf3d3691d0ef2156de9c0451f1c6105053d85833babb84f5a9e5` |
| `SZ_THER_1963_B` | `ce594ab1c368517b56a98bacc2d5db8b4f0ef0e60478c4ca83ed80c67a8ac859` | `e0010fdfd509a459f766bad1b128e6e1571e367406466008bf0a37214f0760c3` |
| `SZ_TRIEBPATH_1` | `3468980b18573b5fcf5a4975ace7acd1712557b2530e3a78166b1ad90b288ac0` | `24820a6f5c4acc8fae8b878794b20cdccb95d8e480bbf4e82fbda5f850890d31` |
| `SZ_TRIEBPATH_2` | `d67b31df843d490b9e70b6423732f497b8d06d6eb07bbdd917ed0f4e8c6def33` | `f6ffc5e3c00b09e030cd1b269fabce15cedb5c5abb997adb11b9bcf94b906db6` |

These hashes identify generated derivatives only. They do not elevate generated output above admitted source evidence.

## 7. Independent real-corpus witness summary

The independent verifier on post-merge `main` observed the following source record counts:

| Source | Total records | Streams |
|---|---:|---|
| `DERI_1949` | 3,258 | BODY 2,172; FOOTER 539; FOOTNOTE 10; HEADER 537 |
| `MELON_1975` | 2,652 | BODY 2,307; FOOTER 169; FOOTNOTE 4; HEADER 172 |
| `SZ_IA_1956_A` | 3,843 | BODY 3,200; FOOTER 95; FOOTNOTE 449; HEADER 99 |
| `SZ_IA_1956_B` | 4,196 | BODY 3,722; FOOTER 136; FOOTNOTE 204; HEADER 134 |
| `SZ_LEHR_1972` | 9,167 | BODY 8,416; FOOTER 230; FOOTNOTE 287; HEADER 234 |
| `SZ_SA_1948` | 4,096 | BODY 3,692; ENDNOTE 2; FOOTER 155; FOOTNOTE 13; HEADER 234 |
| `SZ_THER_1963_A` | 2,926 | BODY 2,355; FOOTER 107; FOOTNOTE 353; HEADER 111 |
| `SZ_THER_1963_B` | 3,871 | BODY 3,304; FOOTER 100; FOOTNOTE 411; HEADER 56 |
| `SZ_TRIEBPATH_1` | 4,199 | BODY 3,686; FOOTER 202; FOOTNOTE 109; HEADER 202 |
| `SZ_TRIEBPATH_2` | 10,243 | BODY 9,385; FOOTER 366; FOOTNOTE 130; HEADER 362 |

These are structural witnesses, not doctrinal or semantic counts.

## 8. What remains before `P0_SOURCES_PASS`

This gate closes the independent canonical implementation/regeneration requirement only. P0 remains open. The remaining source work must proceed in repository order:

1. perform real-source DOCX/PDF spot arbitration where visual/layout fidelity matters;
2. treat the canonical hash inventory above as derivative identity evidence, not authority;
3. only after independent generation and source arbitration, compare Szondi3 canonical output with Szondi2 witness hashes/text as `ORACLE_ONLY`;
4. investigate and classify every predecessor difference rather than making equality a target;
5. independently revalidate the 48-card series/position/factor mapping from authorized primary source evidence;
6. record residual limitations, especially the absence of paired admitted PDFs for `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`.

`P0_SOURCES_PASS` may be considered only after those remaining requirements are resolved. P1 administration/scoring work remains prohibited until that explicit gate is declared.

## Final verification statement

> The independent Szondi3 canonical-access implementation gate is reproducibly PASS on `main`. This is a source-access milestone only; it neither makes generated canonical data authoritative nor completes P0.
