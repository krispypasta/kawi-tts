# P6-003: Vowel Length Strategy

[P6-003 POLICY DOCUMENT]

## 1. Scope
This document defines the Kawi-TTS architectural and linguistic policy for handling macrons and vowel-length markers (`ā`, `ī`, `ū`, `əː`/`ö`, `ṝ`, `ḹ`) across canonical G2P representation and profile-specific acoustic mappings.

## 2. Research Question
How should Kawi-TTS handle macrons / vowel-length markers when:
* Sanskrit loanword length may have been neglected in spoken Old Javanese.
* Native vocabulary may contain meaningful length/weight/stress information.
* Kakawin metrical length belongs to a separate performance context.
* The canonical representation must preserve the source distinction.

## 3. Evidence Inventory
Based on the Phase 5 Linguistic Audit:
*   **Native Compensatory Macrons:** Long vowels in inherited native words are etymological (compensatory lengthening after consonant loss) (Shmelev 2002; Kullanda 2016). *Confidence: High.*
*   **Sanskrit Loans:** Macrons were rigidly retained in writing but neglected in spoken pronunciation (Zoetmulder 1982). *Confidence: High.*
*   **Kakawin Meter:** Macrons dictated prosodic weight (*guru*) in poetry, independent of vernacular speech (Zoetmulder 1974; Hunter 2009). *Confidence: High.*
*   **Stress Shifts:** Orthographic length may have marked prosodic stress shifts rather than pure duration (Kullanda 2016). *Confidence: Medium.*
*   **Comparative Javanese:** Modern Javanese lacks phonemic vowel length entirely, suggesting Old Javanese also lacked it (Yallop 1982). *Confidence: High.*

## 4. Native vs Loanword Distinction
Sanskrit-derived loanwords utilized macrons as orthographic prescriptivism. Native Old Javanese utilized macrons for compensatory lengthening and affixation fusion. The phonetic realization of length differed drastically based on this etymological boundary.

## 5. Metrical Boundary
Kakawin poetry enforces quantitative meters (*mĕtrika*). A macron here guarantees a heavy syllable (*guru*), serving a structural, musical, and performance role rather than reflecting conversational spoken Old Javanese.

## 6. Current Data Capabilities
**Insufficient.** A lexical/data audit confirms the current project data (primarily WordNet `wn-kaw.tab`) lacks etymological tags, language-of-origin fields, or phonological descriptors. The normalization and tokenizer layers cannot currently propagate lexical flags. Therefore, Profile A **cannot safely make an etymology-dependent vowel-length decision right now.**

## 7. Decision Matrix
| Strategy | Evidence Support | Information Loss | Complexity | Required Metadata | Safe for V2? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A. Always pronounce long** | Contradicted by sources | High (falsifies spoken OJ) | Low | None | No |
| **B. Always merge (Profile A)** | Broadly true for loans | High (destroys native traits) | Low | None | No |
| **C. Preserve unresolved status** | Supported by uncertainty | None | Low | None | **Yes** |
| **D. Distinguish native vs loan** | High (Linguistically exact)| None | High | Etymological DB | Not yet |
| **E. Distinguish context (Meter)** | High (Kakawin specific) | None | High | Metrical parser | Not yet |

## 8. Recommended Policy
**Hybrid / Staged Strategy.** 
Implement **Strategy C (Preserve unresolved status)** as the immediate Profile A fallback. No universal length merger or duration rule may be implemented. In the future, once a metadata layer is built, transition to Strategy D and E. 

## 9. Canonical Invariants
Canonical G2P must remain strictly lossless. `ā` remains `aː`. No acoustic assumptions are made at this layer.

## 10. Profile A Behavior (Historical Spoken)
*   **Known Loan (Future):** Evidence-backed merger/reduction.
*   **Known Native (Future):** Unresolved or context-specific stress.
*   **Current/Unknown Provenance:** Map canonical token to target token identically (e.g., `aː` → `aː`) but explicitly flag as `PolicyStatus.UNRESOLVED`. **Do not invent length, do not invent merger.**

## 11. Profile B Behavior (Scholarly/Recitation)
*   Preserve explicit phonetic length. Map canonical token `aː` to target token `aː` with `PolicyStatus.PRESERVED` to support recitation and Sanskrit-adherent orthographic reading.

## 12. Unknown-Provenance Fallback
For any word where etymology or metrical context cannot be programmatically proven, Profile A must default to `UNRESOLVED` and preserve the canonical length token to prevent destructive assumptions.

## 13. Required Future Metadata
To safely unblock etymological vowel-length routing, the following architecture is required:
1.  **Etymological Lexicon:** Dictionary lookup mapping canonical lemmas to `[+native]`, `[+loan_sanskrit]`, or `[+unknown]`.
2.  **Token Metadata Propagation:** `Token` dataclass must support properties (e.g., `token.etymology`) that pass through G2P to `AbstractProfileStrategy`.
3.  **Metrical Context Engine:** An optional parser phase to tag *guru/laghu* syllables in Kakawin texts.

## 14. Open Research Questions
*   Did native compensatory macrons manifest as true phonetic duration, or purely as dynamic stress peaks?
*   How should the acoustic backend ultimately synthesize `UNRESOLVED` tokens to reflect epistemic uncertainty without breaking audio generation?

## 15. Implementation Implications
No changes to `src/acoustic/strategies/` are required at this time. The current fallback behavior in `ProfileAStrategy` (returning `UNRESOLVED` for `aː`, `iː`, `uː`, `əː`) already correctly implements this policy.

## 16. Stop Conditions
This strategy is fully defined. Do not implement the lexical metadata system during this phase. Do not generate V2 audio.

## 17. Source Traceability
* Shmelev, A. (2002) "Long vowels in Old Javanese: were they phonemic?"
* Kullanda, S. (2016)
* Zoetmulder, P.J. (1982) *Old Javanese-English Dictionary*
* Zoetmulder, P.J. (1974) *Kalangwan*
* Hunter, T. (2009) "Yati"
* Yallop, C. (1982) "The phonology of Javanese vowels"
