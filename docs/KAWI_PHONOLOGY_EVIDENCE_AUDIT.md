# Deep Historical Kawi Phonology Evidence Audit

**MODE:** STRICT READ / RESEARCH / AUDIT ONLY

## 1. Executive Summary
This document provides a comprehensive evidence audit of the phonological assumptions underpinning Kawi-TTS's canonical representation and Profile A (Historical Spoken Old Javanese). By strictly reviewing authoritative scholarly sources and filtering out modern performance (Mabasan) biases, the audit confirms that Profile A's core mergers (aspirate and sibilant collapse) are **historically accurate and heavily supported** by comparative Austronesian linguistics and scribal evidence. However, the audit also identified critical omissions in the current codebase (e.g., missing aspirate mergers) and confirmed that vowel length was not phonemic in spoken Old Javanese. 

## 2. Current Pronunciation Model
Kawi-TTS V1 currently operates a lossless G2P engine mapping Zoetmulder’s Romanization to an internal phonological representation. Profile A (the historical spoken profile) applies targeted mergers to this canonical sequence:
*   `bʱ, dʱ, gʱ, pʰ` → `b, d, g, p` (Aspirates)
*   `ś, ṣ` → `s` (Sibilants)
*   `r̩, l̩` → `rə, lə` (Vocalic liquids)
*   Stripping of long vowel markers (`aː, iː, uː, əː` → `a, i, u, ə`)

## 3. Evidence Methodology
The audit prioritized primary scholarly literature and comparative Indonesian historical linguistics. 
Evidence is graded into four strict categories:
*   **A** — DIRECT / STRONG SCHOLARLY SUPPORT
*   **B** — REASONABLE SCHOLARLY RECONSTRUCTION
*   **C** — ENGINEERING / INTERPRETIVE INFERENCE
*   **D** — UNRESOLVED

## 4. Source Inventory
*   **Zoetmulder, P.J. (1982)**, *Old Javanese-English Dictionary* (Orthographic baseline).
*   **Teselkin, A.S. (1972)**, *Old Javanese (Kawi)* (Phonology and script limitations).
*   **Van der Molen, W. (2015)**, *An Introduction to Old Javanese* (Historical pronunciation).
*   **Hoogervorst, T. (2017)** (Comparative Austronesian and Javanese phonology).
*   **Zurbuchen, M. (1976/2020)** & **Acri, A. (2013)** (Mabasan limitations).

## 5. Vowel Audit
*   **Inventory:** Native 6-vowel system (`a`, `i`, `u`, `e`, `o`, `ə`). **[Grade A]**
*   **Vowel Length:** Vowel duration (`ā`, `ī`, `ū`) was strictly an orthographic convention for unadapted Sanskrit loanwords or a metrical requirement for *kakawin* poetry. In colloquial Old Javanese speech, long graphemes were realized as their short equivalents. **[Grade B]**
*   **Schwa (`ĕ` / `ə`):** A distinct phoneme in Old Javanese, universally reconstructed as a mid-central schwa. **[Grade A]**

## 6. Vocalic Liquid Audit
*   **Vocalic `ṛ` / `ḷ`:** Though written with specific Brahmic graphemes in Sanskrit loans, Old Javanese morphology proves they were pronounced as the consonant-vowel sequences `/rə/` and `/lə/`. 
*   **Evidence:** The root *rṇgö* generates the infixed forms *rinengö* / *rumengö*, which is only possible if the underlying root was phonologically */rəŋə/*. 
*   **Grade:** **A** (Strongly supported by morphology, not just a modern Javanese approximation).

## 7. Consonant Audit
*   **Dental vs. Retroflex Stops (`t` vs `ṭ`, `d` vs `ḍ`):** These were distinctly pronounced. Unlike aspiration, the retroflex vs. dental distinction is native to Javanese phonology (Austronesian apical vs laminal). They must not be merged. **[Grade A]**
*   **Sanskrit Consonants:** Spoken Old Javanese completely collapsed Sanskrit consonants that didn't align with the native inventory while preserving those that did. **[Grade A]**

## 8. Aspiration Audit
*   **Aspirated Stops (`bh`, `dh`, `kh`, `th`, `ph`, etc.):** Aspiration was alien to Javanese phonology. Sanskrit loanwords with aspirated stops merged entirely with unaspirated native stops in speech. This is proven by frequent spelling errors in manuscripts where scribes interchange aspirated and unaspirated characters (e.g., *bhaṭāra* vs *baṭara*). 
*   **Grade:** **A**

## 9. Sibilant Audit
*   **Sibilants (`ś`, `ṣ`, `s`):** The three-way Sanskrit distinction collapsed into the single native alveolar/dental `/s/`. Scribes frequently confused them in writing, proving they sounded identical. Zoetmulder explicitly ignores these variants in alphabetization.
*   **Grade:** **A**

## 10. Nasal Audit
*   **Retroflex Nasal (`ṇ`):** Merged into dental `/n/`. **[Grade A]**
*   **Velar/Palatal Nasals (`ṅ`, `ñ`):** Preserved as distinct phonemes, native to Javanese. **[Grade A]**

## 11. Orthography vs Phonology
*   **Over-representation:** The Kawi script (a Brahmic descendant) was designed to accommodate Sanskrit and vastly over-represents native Old Javanese phonology. 
*   **Mabasan Invalidity:** Modern *seka mabasan* (reading groups) apply contemporary Balinese phonological rules and vowel shifts to ancient texts. Using this audio to reconstruct 9th-century phonetics is historically invalid. **[Grade A]**

## 12. Profile A Audit
*   `bʱ, dʱ, gʱ, pʰ → b, d, g, p`: **Evidence-backed [Grade A]**. (However, `kʰ, ṭʰ, ḍʱ, cʰ, ɟʱ` are currently missing from the codebase rule `_ASPIRATE_MERGERS`!).
*   `ś, ṣ → s`: **Evidence-backed [Grade A]**.
*   `r̩, l̩ → rə, lə`: **Evidence-backed [Grade A]**. (Currently marked in code as `PROVISIONAL_RECONSTRUCTION`, which under-sells the morphological evidence).
*   Retention of Dental/Retroflex: **Evidence-backed [Grade A]**.
*   Long-liquid fallback / length stripping: **Reasonable Reconstruction [Grade B]**.

## 13. Negative Evidence (What the sources DO NOT establish)
*   **Exact tongue posture:** Whether Old Javanese retroflexes were truly sub-apical retroflex or just alveolar (like modern Javanese) cannot be definitively proven.
*   **Exact schwa quality:** The precise phonetic realization (e.g., [ə] vs [ɤ]) in the 9th century is unrecoverable.
*   **Stress and Intonation:** No direct historical acoustic evidence exists for stress placement or sentence-level intonation.

## 14. Contradictions Found
*   **CODE VS LINGUISTICS:** The `_ASPIRATE_MERGERS` dictionary in `profile_a.py` only merges `bʱ, dʱ, gʱ, pʰ`. It entirely misses `tʰ, kʰ, cʰ, ɟʱ, ṭʰ, ḍʱ`. If all aspirates merged in spoken Kawi (as literature strongly dictates), the code is currently leaking Sanskrit aspirates into Profile A.
*   **CODE VS EVIDENCE STATUS:** `r̩ → rə` is coded as `PROVISIONAL_RECONSTRUCTION` in `profile_a.py`, but morphological evidence (infixation behavior) makes this a historically `ESTABLISHED` fact.

## 15. Evidence Grading Matrix

| Feature | Current Kawi-TTS Assumption | Evidence | Evidence Strength | Type |
| :--- | :--- | :--- | :--- | :--- |
| 6-Vowel System | Native vowels are a,i,u,e,o,ə | Teselkin, Zoetmulder | A (Strong) | Established |
| Vowel Length | Stripped in Profile A | Metrical texts, spoken constraints | B (Reasonable) | Reconstruction |
| Vocalic Liquids | Fallback to rə, lə | Morphology (rṇgö -> rumengö) | A (Strong) | Established |
| Dental vs Retroflex | Distinctly preserved | Austronesian contrast | A (Strong) | Established |
| Aspirate Merger | Merged to unaspirated | Manuscript spelling errors | A (Strong) | Established |
| Sibilant Merger | ś, ṣ merge to s | Manuscript spelling errors | A (Strong) | Established |
| Retroflex Nasal | ṇ merges to n | Sanskrit collapse | A (Strong) | Established |

## 16. Recommended Documentation Corrections
*   `PROPOSED FUTURE CHANGE`: Update `profile_a.py` citation for `_LIQUID_ADAPTATIONS` from `PROVISIONAL_RECONSTRUCTION` to `EVIDENCE_BACKED`.
*   `PROPOSED FUTURE CHANGE`: Document the historical merging of `ṇ` to `n`. 

## 17. Proposed Future Research
*   Investigate the exact implementation of `_ASPIRATE_MERGERS` to ensure all digraph aspirates are covered, not just the voiced/labial ones.

## 18. Open Questions
*   How did sandhi operate in spoken Old Javanese across word boundaries, and did it preserve any Sanskrit phonetic traits that were otherwise lost?
*   How should the retroflex nasal `ṇ` be handled in Profile A if it merged to `n`, given it isn't currently listed in the merger dictionary?

## 19. What Can Be Claimed
*   Profile A's sibilant and aspirate mergers are historically accurate for spoken Old Javanese.
*   Kawi script was an orthographic over-representation of the spoken language.
*   Vocalic liquids functioned as `/rə/` and `/lə/` in native morphology.

## 20. What Cannot Be Claimed
*   Kakawin or Mabasan audio cannot be claimed as representative of historical 9th-century Kawi phonology.
*   We cannot claim to know the exact phonetic realization of Old Javanese stress or intonation.
