> **[P5-002 POLICY AMENDMENT]**
> This document reflects the V1.0.0 historical baseline. 
> Under the finalized P5-002 Acoustic Profile Policy, the acoustic mappings described here (such as rendering distinct aspirates `[bʰ]` and sibilants `[ʃ]/[ʂ]`) have been formally reclassified as **Profile B (Scholarly/Orthographic Reading)** rather than Profile A. 
> Historical evidence confirms that spoken Old Javanese (Profile A) merged these sounds. 
> V1 remains frozen as an orthographically lossless baseline, but its acoustic output does not represent true Profile A speech. V2 will introduce an explicit `ProfileStrategy` to implement these mergers acoustically while preserving canonical distinctions. See `docs/P5_002_ACOUSTIC_PROFILE_POLICY.md` for details.

# Profile A G2P Specification & Decision Matrix

**Target:** Profile A (Reconstructed Historical Spoken Old Javanese)
**Status:** Pre-implementation specification (Task P3-003A)
**Goal:** Define the exact internal phonological representation the G2P engine will produce, ensuring no linguistically meaningful information is destroyed prematurely.

## 1. Architectural Philosophy

The G2P engine will operate as a mapping from **Normalized Orthography** (output of `src/normalization/normalizer.py`) to an **Internal Phonological Representation**.

Crucially, because Profile A relies on reconstructions with significant *uncertainty* regarding Sanskrit loanwords, the internal phonological representation must **preserve uncertain distinctions**. The mapping to a specific TTS acoustic backend (e.g., merging `bh` to `[b]`) is a *synthesis* responsibility, NOT a G2P text-processing responsibility.

- **Orthographic Input:** `bh`
- **Internal Phoneme:** `/bʱ/` (or a dedicated symbol like `B_ASP`) — *Preserves information*
- **Acoustic Realization (Backend):** `[b]` — *Collapses information for Modern Javanese synthesis*

By keeping the internal phonemes distinct, we preserve the ability to swap backends or implement Profile B (Scholarly Reading) later without rewriting the G2P engine.

---

## 2. G2P Decision Matrix

### Vowels & Vocalic Liquids

| Orthographic Input | Native/Loan | Internal Phoneme | Candidate Phonetic Realization | Evidence Status | Supporting RES | Safe to Implement? | Human Decision Required? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `a` | Both | `/a/` | `[a]`, `[ɔ]` | ESTABLISHED | RES-001 | YES | No |
| `i` | Both | `/i/` | `[i]` | ESTABLISHED | RES-001 | YES | No |
| `u` | Both | `/u/` | `[u]` | ESTABLISHED | RES-001 | YES | No |
| `e` | Both | `/e/` | `[e]`, `[ɛ]` | ESTABLISHED | RES-001 | YES | No |
| `o` | Both | `/o/` | `[o]`, `[ɔ]` | ESTABLISHED | RES-001 | YES | No |
| `ĕ` | Native | `/ə/` | `[ə]` | ESTABLISHED | RES-003 | YES | No |
| `ā`, `ī`, `ū` | Loan | `/aː/`, `/iː/`, `/uː/` | UNCERTAIN | UNCERTAIN | RES-002 | YES (preserve distinct) | Backend mapping decision deferred. |
| `ö` | Orthographic | `/əː/` | UNCERTAIN | UNCERTAIN | RES-002, RES-007 | YES (preserve distinct) | Backend mapping decision deferred. |
| `ṛ` | Loan | `/r̩/` | UNCERTAIN | UNCERTAIN | RES-020 | YES (preserve distinct) | Backend mapping decision deferred. |
| `ḷ` | Loan | `/l̩/` | UNCERTAIN | UNCERTAIN | RES-020 | YES (preserve distinct) | Backend mapping decision deferred. |
| `ṝ`, `ḹ` | Loan | `/r̩ː/`, `/l̩ː/` | UNCERTAIN | UNCERTAIN | RES-020 | YES (preserve distinct) | Backend mapping decision deferred. |

### Core Consonants (Native & Shared)

| Orthographic Input | Native/Loan | Internal Phoneme | Candidate Phonetic Realization | Evidence Status | Supporting RES | Safe to Implement? | Human Decision Required? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `p`, `b` | Both | `/p/`, `/b/` | `[p]`, `[b]` | ESTABLISHED | RES-001 | YES | No |
| `t`, `d` | Both | `/t/`, `/d/` | `[t̪]`, `[d̪]` | ESTABLISHED | RES-001 | YES | No |
| `c`, `j` | Both | `/c/`, `/j/` | `[c]`, `[ɟ]` or `[tʃ]`, `[dʒ]` | ESTABLISHED | RES-001 | YES | No |
| `k`, `g` | Both | `/k/`, `/g/` | `[k]`, `[g]` | ESTABLISHED | RES-001 | YES | No |
| `m`, `n` | Both | `/m/`, `/n/` | `[m]`, `[n]` | ESTABLISHED | RES-001 | YES | No |
| `ṅ` / `ŋ` | Both | `/ŋ/` | `[ŋ]` | ESTABLISHED | RES-007 | YES | No |
| `ñ` | Both | `/ɲ/` | `[ɲ]` | ESTABLISHED | RES-001 | YES | No |
| `s` | Both | `/s/` | `[s]` | ESTABLISHED | RES-006 | YES | No |
| `h` | Both | `/h/` | `[h]` | ESTABLISHED | RES-001 | YES | No |
| `w`, `y` | Both | `/w/`, `/y/` | `[w]`, `[j]` | ESTABLISHED | RES-001, RES-007 | YES | No |
| `r`, `l` | Both | `/r/`, `/l/` | `[r]`, `[l]` | ESTABLISHED | RES-001 | YES | No |

### Native Retroflex / Alveolar Contrast

| Orthographic Input | Native/Loan | Internal Phoneme | Candidate Phonetic Realization | Evidence Status | Supporting RES | Safe to Implement? | Human Decision Required? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ṭ`, `ḍ` | Native | `/ṭ/`, `/ḍ/` | UNCERTAIN (`[ʈ]`, `[t]`) | RECONSTRUCTED | RES-001, RES-005 | YES (preserve distinct) | No (Modern Javanese backend natively handles this contrast). |

### Sanskrit-Specific Consonants (Uncertain realization)

| Orthographic Input | Native/Loan | Internal Phoneme | Candidate Phonetic Realization | Evidence Status | Supporting RES | Safe to Implement? | Human Decision Required? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ṇ` | Loan | `/ṇ/` | UNCERTAIN (`[ɳ]`, `[n]`) | UNCERTAIN | RES-020 | YES (preserve distinct) | Backend mapping decision deferred. |
| `ś`, `ṣ` | Loan | `/ś/`, `/ṣ/` | UNCERTAIN (`[ʃ]`, `[ʂ]`) | UNCERTAIN | RES-006 | YES (preserve distinct) | Backend mapping decision deferred. |
| `bh`, `dh`, `th`, `ph`, `kh`, `gh`, `ch`, `jh`, `ṭh`, `ḍh` | Loan | `/bʱ/`, `/dʱ/`, etc. | UNCERTAIN (`[bʱ]` vs `[b]`) | UNCERTAIN | RES-004 | YES (preserve distinct) | Backend mapping decision deferred. |

---

## 3. Required Output of the G2P Module

The future `src/g2p/` module will map normalized strings to an **Internal Phoneme Sequence** list, e.g.:

*Orthography:* `bhaṭāra`
*Internal Phonemes:* `["bʱ", "a", "ṭ", "aː", "r", "a"]`

This guarantees information preservation. A separate **Acoustic Mapper** (part of the synthesis backend) will receive these internal phonemes and reduce them to the specific capabilities of the Modern Javanese TTS engine for Profile A:

*Acoustic Mapping (Profile A):* `bʱ` → `[b]`, `aː` → `[a]`, `ṭ` → `[ṭ]`
*Acoustic Output:* `[b a ṭ a r a]`

---

## 4. What Exact Tests Will Be Required Before Implementation?

Before writing the G2P logic, we must write tests verifying:
1. Native words parse correctly: `sĕkar` → `["s", "ə", "k", "a", "r"]`.
2. Native retroflexes parse correctly: `ḍaṅ` → `["ḍ", "a", "ŋ"]`.
3. Digraphs parse as single phonemes (if explicitly permitted, e.g., `ṅ` → `["ŋ"]`). Note: ASCII `ng` must parse as `["n", "g"]` per information preservation policy, and parser ambiguities such as the greedy digraph conflict in `ngh` (e.g., `sanghyang`) require explicit disambiguation to prevent false parsing into `["n", "gʱ"]`.
4. Sanskrit aspirates parse as distinct single phonemes: `dharmma` → `["dʱ", "a", "r", "m", "m", "a"]`. (They must NOT parse as `["d", "h", ...]`).
5. Long vowels parse as distinct phonemes: `ā` → `["aː"]`.
6. Sibilants parse distinctly: `śānti` → `["ś", "aː", "n", "t", "i"]`.
7. Vocalic liquids parse distinctly: `kṛta` → `["k", "r̩", "t", "a"]`.

---

## 5. Formal Questions for Abraham (RESOLVED: DEFERRED)

**Decision from Abraham:** All five acoustic mapper mergers are explicitly DEFERRED. The internal G2P representation MUST preserve these distinctions. The Acoustic Mapper will only collapse them when actually required by a specific backend later, and only after explicit human approval.

1. **Vowel Length (`ā`, `ī`, `ū`, `ö`)**: DEFER mapping. Keep distinct in G2P.
2. **Aspirates (`bh`, `dh`, `th`, etc.)**: DEFER mapping. Keep distinct in G2P.
3. **Sibilants (`ś`, `ṣ`)**: DEFER mapping. Keep distinct in G2P.
4. **Retroflex Nasal (`ṇ`)**: DEFER mapping. Keep distinct in G2P.
5. **Vocalic Liquids (`ṛ`, `ḷ`)**: DEFER mapping. Do NOT map to `rə/lə` yet; keep distinct as `/r̩/` and `/l̩/`.