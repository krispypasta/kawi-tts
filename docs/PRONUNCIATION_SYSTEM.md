# Kawi-TTS V1 Pronunciation System

## 1. Scope and Target
The V1 system targets **Profile A: Reconstructed Historical Spoken Old Javanese**. It models conversational Old Javanese phonology. It explicitly does *not* target modern Balinese chanting (*mabasan* / Profile C) or modern artificial scholarly reading (Profile B). 

## 2. Canonical Input Convention
The canonical input convention is the romanized orthography defined by Zoetmulder (1982).
*   **Velar Nasal:** Exclusively represented by `ṅ` (or `ŋ`).
*   **Palatal Nasal:** Exclusively represented by `ñ`.
*   **ASCII Fallbacks:** The digraphs `ng` and `ny` are **NOT** automatically treated as canonical digraph phonemes. `ng` parses as `["n", "g"]` and `ny` parses as `["n", "j"]` to preserve information, unless passed through an explicit convention-conversion mechanism.

## 3. Evidence Status Framework
Every phonological rule is bound by the project's epistemic evidence framework:
*   **ESTABLISHED:** Supported by comparative historical linguistics and primary philology.
*   **RECONSTRUCTED:** Historically modeled but lacking direct acoustic proof.
*   **UNCERTAIN:** Lacking consensus; historical spoken phonetic realization is unknown.
*   **ASSUMPTION:** A legacy project placeholder pending formal validation.

## 4. Current Frontend Pipeline
The pronunciation generation is a deterministic, information-preserving pipeline:
1.  **Raw Text:** Ingested Romanized string.
2.  **Normalization:** Typographic cleanup and variant unification (e.g., lowercase `v` → `w`).
3.  **Tokenization:** Segmentation into structural tokens and word boundaries.
4.  **G2P (Grapheme-to-Phoneme):** Lossless mapping from orthography to the internal pronunciation token sequence.
5.  **Acoustic Mapping:** Adapting the internal representation into backend-compatible IPA.
6.  **Acoustic Backend:** Generation of audio via eSpeak-ng.

## 5. Native Vowel System
*   **Input Representation:** `a`, `i`, `u`, `e`, `o`, `ĕ`
*   **Current Internal Representation:** `/a/`, `/i/`, `/u/`, `/e/`, `/o/`, `/ə/`
*   **Evidence Status:** ESTABLISHED
*   **RES Reference:** RES-001, RES-003
*   **Notes:** The native 6-vowel system includes the pepet (`ĕ`), represented internally as the mid-central schwa `/ə/`.

## 6. Native Consonant System
*   **Input Representation:** `p, b, c, j, k, g, m, n, ṅ, ñ, s, h, w, y, r, l`
*   **Current Internal Representation:** `/p, b, c, ɟ, k, g, m, n, ŋ, ɲ, s, h, w, j, r, l/`
*   **Evidence Status:** ESTABLISHED
*   **RES Reference:** RES-001, RES-006, RES-007
*   **Notes:** Distinct palatal (`ñ` `/ɲ/`) and velar (`ṅ` `/ŋ/`) nasals are fully established native phonemes.

## 7. t/ṭ and d/ḍ
*   **Input Representation:** `t`, `d` vs. `ṭ`, `ḍ`
*   **Current Internal Representation:** `/t/, /d/` vs. `/ṭ/, /ḍ/`
*   **Evidence Status:** RECONSTRUCTED
*   **RES Reference:** RES-001, RES-005
*   **Notes:** The contrast between dental and retroflex/alveolar stops is reconstructed as natively contrastive in Old Javanese. Phonetic realization of the retroflex series remains UNCERTAIN.

## 8. Sanskrit-Derived Orthographic Distinctions
*   **Input Representation:** Vowel length (`ā`, `ī`, `ū`, `ö`), Aspirates (`bh`, `dh`, `ṭh`, etc.), Sibilants (`ś`, `ṣ`), Retroflex Nasal (`ṇ`), Vocalic Liquids (`ṛ`, `ḷ`).
*   **Current Internal Representation:** Preserved losslessly as distinct tokens (e.g., `/aː/`, `/bʱ/`, `/ś/`, `/ṇ/`, `/r̩/`).
*   **Evidence Status:** UNCERTAIN
*   **RES Reference:** RES-002, RES-004, RES-006, RES-020
*   **Notes:** These features exist orthographically due to Sanskrit loans. Their phonemic and phonetic existence in spoken historical Old Javanese is highly uncertain.

## 9. Internal Pronunciation Representation
The G2P engine's internal tokens are strictly **phonological and lossless**. It preserves uncertain Sanskrit-derived orthographic distinctions exactly as written. The G2P engine does not collapse or merge uncertain internal pronunciation tokens.

## 10. Acoustic Mapping Status
The Acoustic Mapper translates the internal lossless tokens to the eSpeak-ng backend format.
*   **Status:** All five major reduction policies for Sanskrit loans (merging aspirates, merging sibilants, truncating vowel length, mapping vocalic liquids, mapping retroflex nasals) remain **DEFERRED**.
*   Mappings for these uncertain tokens are explicitly tagged in the codebase as `PROVISIONAL_ACOUSTIC_MAPPING`.

## 11. Prosody, Stress, and Sandhi Limitations
*   **Stress:** Undocumented for conversational Old Javanese. Unmodeled in V1.
*   **Sandhi:** Syntactic and morphological sandhi rules across word boundaries are not automatically resolved by the G2P engine.
*   **Guru/Laghu:** The metrical weight system (heavy/light syllables) dictates duration in Balinese musical performance. It is **not** a reflection of spoken vowel length and is excluded from Profile A. (RES-008, RES-009).

## 12. Representative Examples

| Feature | Input | Internal Tokens (G2P) | eSpeak IPA (Mapper) | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Native Vowel** | `wukir` | `['w', 'u', 'k', 'i', 'r']` | `wukir` | 1:1 mapping, established |
| **Pepet** | `sĕkar` | `['s', 'ə', 'k', 'a', 'r']` | `səkar` | Handled as mid-central schwa |
| **t/ṭ Contrast** | `ghaṇṭā` | `['gʱ', 'a', 'ṇ', 'ṭ', 'aː']` | `gʱaɳʈaː` | Retroflexes strictly preserved |
| **Sanskrit Aspirate**| `dharma` | `['dʱ', 'a', 'r', 'm', 'a']` | `dʱarma` | Digraph preserved losslessly |
| **Sibilant** | `śānti` | `['ś', 'aː', 'n', 't', 'i']` | `ʃaːnti` | Sibilants not merged to /s/ |
| **Vocalic Liquid** | `kṛta` | `['k', 'r̩', 't', 'a']` | `kr̩ta` | Mapped as syllabic liquid |
| **ASCII Ambiguity** | `sanghyang` | `[['s', 'a', 'n', 'gʱ', 'j', 'a', 'n', 'g']]` | `sangʱjang` | Flagged as structural ambiguity |
| **Explicit Boundary**| `sang-hyang` | `[['s', 'a', 'n', 'g'], ['h', 'j', 'a', 'n', 'g']]` | `sang hjang` | Hyphen prevents false digraph `gʱ` |

## 13. Known Uncertainties
The exact historical phonetic realization of Sanskrit-derived orthographic features (aspirates, sibilants, vowel length) by native Old Javanese speakers is unknown. They are preserved structurally in V1 to avoid data loss.

## 14. What V1 Does NOT Claim
*   **Historically proven pronunciation:** V1 is an evidence-grounded reconstruction, not an acoustic fact.
*   **Real historical acoustic validation:** No 9th-century recordings exist to validate the output.
*   **Verified neural transfer:** Neural transfer to Modern Javanese is a future concept, not currently verified.
*   **Pronunciation accuracy:** 99.90% represents *symbolic pipeline coverage* over the OJW lexicon, NOT historical "pronunciation accuracy".
*   **Scientific necessity of hybrid backend:** eSpeak-ng is an engineering strategy for rapid iteration, not a scientifically mandated backend.

## 15. Future Profiles / Future Work
*   **Profile B (Scholarly Reading):** Lossy mappings mirroring how modern philologists read Kawi text.
*   **Profile C (Balinese Performance):** Implementation of traditional chanting (*mabasan*), including guru/laghu duration rules and Balinese phonological mergers (e.g., merging retroflex stops to dentals).
*   **Stage 2 Neural TTS:** Modern Javanese VITS cross-lingual acoustic transfer to replace eSpeak-ng.

## 16. Sources and Traceability
Key sources establishing the Kawi-TTS linguistic framework:
*   **Kumar & Rose (2000):** Native reconstructed phoneme inventory.
*   **Zoetmulder (1982) / Zoetmulder & Robson:** Canonical orthography/romanization and lexicography.
*   **Acri & Griffiths (2014):** Pepet transliteration (`ə`) and Indic script mapping.
*   **Schumacher (1995) & Robson (1983):** Balinese metrical realization (guru/laghu) and chanting traditions.
*   **Moeljadi & Aminullah (2020):** Old Javanese Wordnet (OJW) lexical dataset.
