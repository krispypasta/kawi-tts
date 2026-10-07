# P5-002: Acoustic Profile Policy

## 1. Purpose
This document establishes the formal, evidence-backed policy for handling phonological uncertainty and acoustic rendering in Kawi-TTS. It resolves the tension between preserving orthographic/linguistic distinctions (for structural accuracy) and generating historically plausible audio (where many distinctions were merged in spoken Old Javanese).

## 2. Scope
This policy applies to the **Acoustic Mapper** and backend stages of the pipeline. It strictly governs how the canonical internal representation (the output of the G2P engine) is translated into acoustic features. It does **not** alter the G2P engine, which remains responsible for producing an orthographically lossless canonical representation.

## 3. Profile Definitions
The project officially recognizes three distinct acoustic targets. The software architecture must explicitly distinguish between them.

*   **Profile A: Reconstructed Historical Spoken Old Javanese**
    Aims to replicate conversational Old Javanese as spoken by historical users. This profile assumes the adaptation of Sanskrit loanwords into native Austronesian phonotactics.
*   **Profile B: Scholarly / Orthographic Reading**
    Aims to maximize orthographic traceability. Pronounces textual distinctions (often using modern idealized Sanskritized values) even if historical speakers did not, serving philological and scholarly study.
*   **Profile C: Traditional Balinese Kakawin / Mabasan Performance**
    A separate performance and chanting tradition. This is explicitly distinct from conversational speech (Profile A) and is preserved as a conceptual boundary, but is not implemented in V1 or currently planned for V2.

## 4. Layered Architecture: Canonical vs. Profile vs. Backend
To prevent the "lossless G2P" fallacy from polluting acoustic output, the system enforces strict conceptual layers:

1.  **SOURCE / ORTHOGRAPHY:** The raw textual input (e.g., `śānti`).
2.  **CANONICAL REPRESENTATION:** The structural phoneme array parsed by G2P (e.g., `["ś", "ā", "n", "t", "i"]`). **Uncertainty is perfectly preserved here.** Canonical distinctness does *not* demand acoustic distinctness.
3.  **PROFILE-SPECIFIC INTERPRETATION:** The linguistic decision of how a specific profile treats the canonical array (e.g., Profile A interprets `ś` as `/s/`).
4.  **BACKEND REALIZATION:** The mapping of the interpreted phoneme to specific synthesizer commands (e.g., eSpeak formants or Piper embeddings). Backend limitations must never redefine the canonical layer.

## 5. Feature-by-Feature Policy Table

### A. Aspirates (`bh`, `dh`, `gh`, `ph`)
*   **Canonical Representation:** Preserved distinctly.
*   **Evidence Status:** EVIDENCE-BACKED (spoken merger). Sources (Van der Molen, Teselkin) explicitly state these signs did not represent aspirated consonants in Old Javanese speech.
*   **Profile A Acoustic Interpretation:** Merged with corresponding plain stops (`[b]`, `[d]`, `[g]`, `[p]`).
*   **Profile B Acoustic Interpretation:** Preserved as aspirated (`[bʰ]`, etc.).
*   **Confidence:** High.

### B. Sibilants (`ś`, `ṣ`)
*   **Canonical Representation:** Preserved distinctly.
*   **Evidence Status:** EVIDENCE-BACKED (spoken merger). Sources (Teselkin) confirm scribal substitutions demonstrating auditory collapse.
*   **Profile A Acoustic Interpretation:** Merged to the native dental/alveolar `/s/`.
*   **Profile B Acoustic Interpretation:** Preserved distinctly (`[ʃ]`, `[ʂ]`).
*   **Confidence:** High.

### C. Syllabic Liquids (`ṛ`, `ḷ`)
*   **Canonical Representation:** Preserved distinctly.
*   **Evidence Status:** PROVISIONAL RECONSTRUCTION (documented transcription-based adaptation). Acri & Griffiths note transcription by their phonetic counterparts `rĕ` / `lĕ`.
*   **Profile A Acoustic Interpretation:** Provisional adaptation to schwa + liquid (`[rə]`, `[lə]`). *Note: Do not describe this as certain historical phonetics; it is an evidence-backed reconstruction of adaptation.*
*   **Profile B Acoustic Interpretation:** Preserved as syllabic (`[r̩]`, `[l̩]`).
*   **Confidence:** Moderate.

### D. Vowel Length / Macrons (`ā`, `ī`, `ū`)
*   **Canonical Representation:** Preserved distinctly.
*   **Evidence Status:** UNRESOLVED / PROFILE-DEPENDENT. Sources (Van der Molen) note length in Sanskrit loans was neglected, while native macrons may have indicated a distinction.
*   **Profile A Acoustic Interpretation:** Unresolved. Pending further research into etymological handling (separating loans from native stress/duration). Do not create a universal long-vowel rule yet.
*   **Profile B Acoustic Interpretation:** Distinct duration (`[aː]`).
*   **Confidence:** Low.

### E. Dental vs. Retroflex (`t`/`ṭ`, `d`/`ḍ`)
*   **Canonical Representation:** Preserved distinct contrast.
*   **Evidence Status:** EVIDENCE-BACKED contrast. Comparative Austronesian linguistics confirm the native contrast exists.
*   **Profile A Acoustic Interpretation:** Retain acoustic distinction. *Note: The exact tongue posture/articulatory realization (apical-alveolar vs. true sub-apical retroflex) remains uncertain.*
*   **Profile B Acoustic Interpretation:** Retain acoustic distinction.
*   **Confidence:** High (for the contrast), Low (for the exact phonetic realization).

## 6. Uncertainty Handling & Backend Approximation Rules
*   **Explicit Uncertainty:** When historical realization is uncertain, the system explicitly preserves the distinction internally (canonical layer) rather than silently erasing it.
*   **Backend Quarantine:** Any necessary acoustic approximation must remain quarantined inside the `AcousticMapper` or backend-specific adaptation layer. It must be explicitly documented and reversible at the conceptual architecture level.
*   **No False Facts:** Backend-specific technical workarounds must remain backend-specific. They must never be promoted into or presented as historical reconstruction claims.

## 7. Prohibited Inference Patterns
*   **Orthography → Phonology:** Do not assume that an orthographic distinction proves a historical phonetic distinction.
*   **Transliteration → Pronunciation:** Do not upgrade a transcription convention into historical acoustic certainty.
*   **Backend Behavior → Linguistic Evidence:** Do not treat a backend technical limitation or convenience as linguistic reconstruction.
*   "Profile B is wrong" — Do not state this. Profile B is historically unrepresentative of *conversational speech*, but serves a legitimate scholarly reading purpose.

## 8. V1 Baseline vs. V2 Implications

### The V1 Baseline
Kawi-TTS v1.0.0 implements an "orthographically lossless canonical representation." However, its Acoustic Mapper explicitly synthesizes Sanskrit orthographic distinctions (aspirates, sibilants, universal macrons).
*   **Mismatch:** V1 audio output essentially implements **Profile B** (Scholarly Reading), despite earlier documentation claiming it targets Profile A.
*   **Status:** **V1.0.0 remains FROZEN.** We do not rewrite V1 history to pretend it implemented the revised policy. The V1 result is preserved as a historical baseline proving pipeline integrity.

### V2 Implications
V2 will introduce explicit software abstraction for Profiles.
*   V2 will implement a `ProfileStrategy` layer between the canonical G2P output and the backend mapper.
*   V2 Profile A will legally merge aspirates and sibilants acoustically, supported by this policy.
*   V2 will address the vowel length etymological split (P5-003).

## 9. Open Questions & Future Work (P5-003)
*   **Vowel Length Resolution:** How should V2 process etymological context to split native stress macrons from ignored Sanskrit metrical macrons? This decision is deferred to P5-003.

## 10. Source Traceability
*   **Van der Molen, Willem (2015).** *An Introduction to Old Javanese*. (Re: aspirates, vowel length in loans vs. native words).
*   **Teselkin, Avenir S. (1972).** *Old Javanese (Kawi)*. (Re: aspirates, sibilants merger).
*   **Acri, Andrea & Griffiths, Arlo (2014).** "The Romanisation of Indic Script Used in Ancient Indonesia," *BKI* 170. (Re: transliteration vs. transcription, `ṛ` adaptation).
*   **Kumar, Ann & Rose, Phil (2000).** (Re: core Austronesian/Javanese inventory constraints).
*   **Zoetmulder, P.J. (1982).** *Old Javanese-English Dictionary*. (Re: canonical transliteration mapping).
