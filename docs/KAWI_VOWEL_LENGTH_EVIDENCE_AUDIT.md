# Deep Audit: Vowel Length and Long Vocalic Liquids in Profile A

## 1. Executive Summary
This audit examines the historical evidence for vowel length (`ā`, `ī`, `ū`, `ö`) and long vocalic liquids (`ṝ`/`r̩ː`, `ḹ`/`l̩ː`) in Reconstructed Historical Spoken Old Javanese (Profile A). The primary finding is that vowel duration was an orthographic and metrical feature borrowed from Sanskrit, not a phonemic feature of colloquial Old Javanese. 

Consequently, the current Profile A treatment—which strips duration markers (`ː`) but flags them as `UNRESOLVED` (engineering fallback) or maps long liquids directly to short `rə` (provisional)—contains epistemic contradictions. Historical evidence strongly supports treating long vowels as phonetically neutralized in normal Old Javanese speech, justifying an upgrade of their merger status from "engineering fallback" to "evidence-backed reconstruction".

## 2. Current Implementation
### A. Canonical G2P Mapping (`kawi_tts/g2p/engine.py`)
*   `ā, ī, ū` → `aː, iː, uː`
*   `ö` (long pepet) → `əː`
*   `ṝ, ḹ` → `r̩ː, l̩ː`

### B. Profile A Transformation (`kawi_tts/acoustic/strategies/profile_a.py`)
*   **Vowels (`aː, iː, uː, əː`):** Handled dynamically. The `ː` marker is stripped (e.g., `aː` → `a`). 
    *   **Status:** `PolicyStatus.UNRESOLVED`
    *   **Citation:** `"P6-003R / unresolved duration engineering fallback"`
*   **Long Vocalic Liquids (`r̩ː, l̩ː`):** Handled via static dictionary `_LIQUID_ADAPTATIONS` which maps them directly to `rə` and `lə`.
    *   **Status:** `PolicyStatus.PROVISIONAL_RECONSTRUCTION`
    *   **Citation:** `"P5-002 / syllabic-liquid adaptation"`

## 3. Evidence Methodology
The audit relies strictly on linguistic primary sources (Zoetmulder, Teselkin, Van der Molen, Hoogervorst, Acri) to distinguish between orthographic conventions, metrical duration in *kakawin* (poetry), and ordinary spoken phonetic duration in Old Javanese. Claims are separated strictly by phonological domain.

## 4. Old Javanese Vowel Quantity
*   **Native Inventory:** Standard comparative Austronesian reconstruction confirms that Old Javanese natively lacked phonemic vowel length. It possessed a 6-vowel system (`a`, `i`, `u`, `e`, `o`, `ə`). 
*   **Evidence Status:** Grade A.

## 5. Sanskrit Loanword Quantity
*   Sanskrit loanwords introduced orthographic characters for long vowels (`ā`, `ī`, `ū`). However, scribal evidence reveals widespread substitution (using short characters for long, and vice versa) in prose contexts where meter did not compel precise spelling.
*   **Conclusion:** The orthography preserved Sanskrit conventions, but these did not dictate native spoken length outside of specific learned chanting traditions.
*   **Evidence Status:** Grade B.

## 6. Metrical vs Spoken Quantity
*   **Metrical (*Kakawin*):** Vowel length was strictly observed for *guru* (heavy) and *laghu* (light) metrical constraints derived from Indian prosody. 
*   **Spoken (Colloquial):** As Teselkin (1972) and others note, in the ordinary speech of the Javanese, Sanskrit long vowels likely lost their phonemic relevance entirely. 
*   **Evidence Status:** Grade B.

## 7. Vocalic Liquid Evidence
*   `ṛ` (short) and `ḷ` (short) exist purely as Sanskrit loans. 
*   Morphological evidence (e.g., *rṇgö* → *rinengö* / *rumengö*) demonstrates that speakers analyzed and pronounced `ṛ` as a sequence of a consonant and a schwa (`/rə/`). 
*   **Evidence Status:** Grade A.

## 8. Long Vocalic Liquids
*   The long vocalic liquids `ṝ` and `ḹ` are extremely rare, effectively confined to theoretical Sanskrit grammatical paradigms rather than living vocabulary. 
*   Because short `ṛ` was natively unpacked to `/rə/`, a hypothetical spoken long `ṝ` would presumably resolve to `/rə/` as well, since Old Javanese lacked both syllabic liquids and phonemic vowel length. 
*   **Evidence Status:** Grade B (Reasonable reconstruction by phonetic necessity).

## 9. Negative Evidence (What We Cannot Establish)
*   **Exact Vowel Duration in Milliseconds:** Impossible to reconstruct.
*   **Exact Stress Realization:** The suprasegmental prosody of spoken Old Javanese is entirely undocumented.
*   **Exact Spoken Realization of Sanskrit Long Vowels by Elites:** We cannot prove that elite bilinguals (Kawi-Sanskrit) *never* artificially lengthened vowels in speech. 
*   **Compensatory Stress:** There is no documented proof that shortened vowels were compensated for with pitch or stress accents. 
*   **Conclusion:** "Unknown" is the most academically rigorous stance for phonetic minutiae, but phonemic merger (shortening) is structurally highly probable.

## 10. Contradictions
*   **Contradiction 1 (Liquids Status):** `docs/KAWI_PHONOLOGY_EVIDENCE_AUDIT.md` grades the `r̩` → `rə` mapping as **Grade A** (Direct scholarly support via morphology). Yet, `profile_a.py` stamps it as `PROVISIONAL_RECONSTRUCTION`.
*   **Contradiction 2 (Vowel Length Status):** `docs/KAWI_PHONOLOGY_EVIDENCE_AUDIT.md` notes that colloquial loss of vowel length is a **Grade B** historical likelihood. Yet, `profile_a.py` treats `aː` → `a` as `UNRESOLVED` (an "engineering fallback"). 
*   **Contradiction 3 (Analogical Long Liquids):** `r̩ː` maps to `rə` in `profile_a.py`. This implicitly strips length at the dictionary level before the duration-stripping logic ever sees it, masking it as an "adaptation" rather than a length merger.

## 11. Evidence Grading Matrix

| Feature | Claim | Grade |
| :--- | :--- | :--- |
| **Native OJ Length** | Native vocabulary lacked phonemic vowel length. | **A** |
| **Loanword Length** | Long vowels in Sanskrit loans were shortened in OJ speech. | **B** |
| **Metrical Length** | Long vowels were required exclusively for *kakawin* meter. | **A** |
| **Short Liquids** | `ṛ` / `ḷ` were pronounced `/rə/` / `/lə/` based on morphology. | **A** |
| **Long Liquids** | `ṝ` / `ḹ` were pronounced `/rə/` / `/lə/` in OJ speech. | **B** |

## 12. Proposed Future Policy

| Current Behavior | Evidence Status | Possible Future Policy | Confidence | Risk |
| :--- | :--- | :--- | :--- | :--- |
| `aː` → `a` (`UNRESOLVED`) | **Grade B** | Retain stripping, upgrade to `EVIDENCE_BACKED`. | High | Low |
| `iː` → `i` (`UNRESOLVED`) | **Grade B** | Retain stripping, upgrade to `EVIDENCE_BACKED`. | High | Low |
| `uː` → `u` (`UNRESOLVED`) | **Grade B** | Retain stripping, upgrade to `EVIDENCE_BACKED`. | High | Low |
| `əː` → `ə` (`UNRESOLVED`) | **Grade B** | Retain stripping, upgrade to `EVIDENCE_BACKED`. | High | Low |
| `r̩` → `rə` (`PROVISIONAL`) | **Grade A** | Retain mapping, upgrade to `EVIDENCE_BACKED`. | High | Low |
| `r̩ː` → `rə` (`PROVISIONAL`) | **Grade B** | Split into two mappings (liquid unpack + duration strip) or upgrade to `EVIDENCE_BACKED`. | Medium | Low |
| `l̩ː` → `lə` (`PROVISIONAL`) | **Grade B** | Split into two mappings or upgrade to `EVIDENCE_BACKED`. | Medium | Low |

## 13. Open Questions
*   How should Profile A document the difference between an engineering convenience (e.g., stripping unknown characters) and a historically backed phonemic merger (e.g., Old Javanese speakers ignoring Sanskrit length)?
*   Should the `PROVISIONAL_RECONSTRUCTION` status be redefined to exclude items with Grade A/B evidence?

## 14. Final Recommendation
The current G2P representation is correct in losslessly preserving `ā, ī, ū, ṝ, ḹ` as canonical duration tokens. 

However, Profile A's current behavior of treating duration removal as an `UNRESOLVED` engineering fallback underestimates the historical evidence. Comparative linguistics strongly indicates that vowel length neutralization was a real feature of spoken Old Javanese. 

**Conclusion:** The code should remain unchanged for now, but future work should strongly consider upgrading the neutralization of vowel length and vocalic liquids in Profile A from `UNRESOLVED` / `PROVISIONAL` to `EVIDENCE_BACKED`.
