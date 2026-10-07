# Pre-Release Pronunciation Reality Check

## 1. Executive Summary
A diagnostic investigation was conducted on the synthesized audio for `BHAṬĀRA` and `kṝta`. The objective was to determine why the output sounded broken or phonetically unexpected, isolating whether the fault lies in the linguistic policy, the Python implementation, or the eSpeak-ng backend realization. 

**Conclusion:** The perceived phonetic errors are overwhelmingly **backend realization artifacts** caused by the Indonesian (`id`) voice's inability to process specific IPA characters (such as `ʈ`, `ʱ`, `ː`, and `r̩`). Instead of ignoring them or mapping them to nearest neighbors, eSpeak-ng replaces them with glottal stops (`?`), completely destroying the word's acoustic structure. 

Additionally, a genuine **Implementation Mismatch** was discovered for `kṝta` in Profile A: the code fails to apply the documented syllabic-liquid merger for the *long* variant `ṝ`, accidentally passing the unsupported `r̩ː` through to the backend.

## 2. BHAṬĀRA Analysis

**Observation:** Output sounds like "a-a-ra" or has an unclear initial consonant.
**Question:** Is the expected linguistic target actually `/b/` for Profile A and `/bʱ/` for Profile B? 
**Answer:** Yes. The documented project policy explicitly mandates `[b]` for Profile A (merging the aspirate) and `[bʱ]` for Profile B. 

*   **Policy Target:** Profile A: `[b]`, `[ṭ]`, `[a]`. Profile B: `[bʱ]`, `[ṭ]`, `[aː]`.
*   **Implementation:** The code correctly translates the canonical `bʱ-a-ṭ-aː-r-a` to Profile A (`b-a-ṭ-a-r-a`) and Profile B (`bʱ-a-ṭ-aː-r-a`).
*   **Acoustic Mapper:** Correctly sends `[[baʈara]]` (A) and `[[bʱaʈaːra]]` (B).
*   **Backend Behavior:** The `id` voice in eSpeak-ng **lacks support** for `ʈ`, `ʱ`, and `ː`. When it encounters these IPA symbols, it replaces them with internal `?` phonemes (glottal stops).
    *   `[[baʈara]]` becomes `ba?ar'a`.
    *   `[[bʱaʈaːra]]` becomes `b?a?a?r'a`.
*   **Diagnosis:** The stuttering "a-a-ra" sound is the listener hearing `b` followed by multiple glottal stops. This is purely an eSpeak-ng fallback failure, not a policy error.

## 3. KṚTA / KṜTA-like Analysis

**Observation:** A/B output sounds roughly like "kurta".
**Question:** What is the exact linguistic target, and is "kurta" faithful to it?
**Answer:** The policy (P5-002 section 5.C) states that for Profile A, syllabic liquids (`ṛ`, `ḷ`) should adapt to `[rə]` / `[lə]`. Profile B should preserve `[r̩]` / `[l̩]`. The system is *not* claiming a historical pronunciation of `/kurta/`; "kurta" is an acoustic artifact of the backend struggling with unsupported phonemes.

*   **Policy Target:** Profile A should target `[rə]` (or `[rəː]`). Profile B targets `[r̩ː]`.
*   **Implementation (Bug Detected):** The canonical representation is `k-r̩ː-t-a`. `ProfileAStrategy` successfully adapts short `r̩` to `rə`, but forgets to handle the long variant `r̩ː`. As a result, `r̩ː` leaks through untouched into Profile A.
*   **Acoustic Mapper:** Sends `[[kr̩ːta]]` for *both* Profile A and Profile B.
*   **Backend Behavior:** The `id` voice does not support `r̩` or `ː`. It falls back to `kr??t'a` (inserting glottal stops). 
*   **Diagnosis:** "Kurta" is the listener's ear interpreting the glottalized, broken consonant cluster `kr??t`. Profile A suffers from an **Implementation Mismatch**, while Profile B suffers from a **Backend Limitation**.

## 4. Policy vs. Implementation vs. Backend Comparison

| Input | Canonical | Profile A Target | Profile B Target | eSpeak String (A) | eSpeak String (B) | eSpeak `id` Realization | Diagnosis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BHAṬĀRA** | `bʱ-a-ṭ-aː-r-a` | `b-a-ṭ-a-r-a` | `bʱ-a-ṭ-aː-r-a` | `[[baʈara]]` | `[[bʱaʈaːra]]` | `ba?ar'a` / `b?a?a?r'a` | **POLICY CORRECT, BACKEND LIMITATION** |
| **kṝta** | `k-r̩ː-t-a` | `k-rə-t-a` (Policy) | `k-r̩ː-t-a` | `[[kr̩ːta]]` | `[[kr̩ːta]]` | `kr??t'a` (Both) | **IMPLEMENTATION MISMATCH** (Profile A) & **BACKEND LIMITATION** (Profile B) |

## 5. Direct eSpeak-ng Findings

Executing eSpeak-ng locally with diagnostic trace flags (`-x` / `-X`) confirms the translation breakdown:
*   `espeak-ng -v id -q -x "[[bʱaʈaːra]]"` exactly yields `b?a?a?r'a`
*   `espeak-ng -v id -q -x "[[kr̩ːta]]"` exactly yields `kr??t'a`

This isolates the failure strictly to the synthesizer's acoustic rendering layer. The Kawi-TTS phonological pipeline is outputting the correct structural strings (excluding the Profile A long-liquid bug), but the synthesizer drops any IPA phone not mapped in its active voice dictionary.

## 6. Decision & Recommended Actions

**Decision:** 
*   **BHAṬĀRA:** POLICY CORRECT, BACKEND LIMITATION
*   **kṝta:** IMPLEMENTATION MISMATCH (Profile A) and BACKEND LIMITATION (Profile B)

**Are we hearing the pronunciation our policy intends?**
No. We are hearing eSpeak's emergency fallback (inserting glottal stops for unknown characters). The audio is an engineering artifact, not a representation of the project's linguistic policy.

**Recommended Future Actions (For V2):**
1.  **Code Fix:** Update `_LIQUID_ADAPTATIONS` in `kawi_tts/acoustic/strategies/profile_a.py` to map `r̩ː` to `rə` (or `rəː`) to fix the `kṝta` Profile A leak.
2.  **Backend Mapping Fix:** The `AcousticMapper` should intercept IPA characters known to be unsupported by the target voice (e.g., stripping `ː` for `id`, falling back `ʈ` to `t`) *before* sending them to eSpeak, preventing the glottal-stop corruption.
3.  **Voice Configuration:** Consider explicitly defining a custom Kawi phoneme dictionary for eSpeak or switching to a voice that supports Indic retroflexes and aspirates (like `hi` or a custom `jv`).