# DEEP EVIDENCE RECONCILIATION: PROFILE A & BACKEND ADAPTER

## 1. Executive Summary
An audit was conducted to evaluate the recent modification of `ProfileAStrategy` (mapping `r̩ː → rəː`) and the new eSpeak `id` backend adapter. The audit confirms that while the backend adapter successfully quarantines acoustic fallback logic, the change to `ProfileAStrategy` introduces a historically unsupported linguistic claim (a "long schwa" `rəː`). The apparent success of this implementation relies on the backend adapter silently erasing the length (`"rəː": "r@"`).

**Final Verdict:** POLICY-CORRECTION-REQUIRED. The `r̩ː → rəː` transformation exceeds available evidence and must be corrected.

## 2. Historical Policy Reconstruction
*   **P5-002 (Acoustic Profile Policy):** Explicitly states: "Provisional adaptation to schwa + liquid (`[rə]`, `[lə]`)." Regarding vowel length, it states: "No Profile A duration claim is being made for `əː`. Do not create a universal long-vowel rule yet."
*   **P6-003R (Vowel Length Resolution):** Concluded that vowel length duration is structurally deferred and unresolved in Profile A, defaulting to stripping length marks for native vowels unless specifically preserved.
*   **P7-B (Engine Hardening Audit):** Explicitly commanded: "DO NOT strip duration from `r̩ː`. Leave it until cited."
*   **Recent Implementation:** `r̩ː` was bypassing the dictionary in `ProfileAStrategy`, leaving it as `r̩ː`. A recent commit patched `_LIQUID_ADAPTATIONS` to map `"r̩ː": "rəː"`, immediately resolving it as a `PROVISIONAL_RECONSTRUCTION`. This bypassed the vowel length stripping block and sent `rəː` to the acoustic mapper.

## 3. Primary-Source Evidence
*   **Zoetmulder (1982), *Old Javanese-English Dictionary*:** Transliterates vocalic liquids as `rĕ` / `lĕ` (or `rö` / `lö` depending on specific sandhi/etymological contexts). No systemic "long `rĕ`" is posited for long Sanskrit `ṝ`.
*   **Acri & Griffiths (2014), "The Romanisation of Indic Script Used in Ancient Indonesia":** "The vocalic r̥ (or ṛ) and l ̥ (or ḷ) tend to be transcribed, rather than transliterated, by their Old Javanese phonetic counterparts, viz. the clusters rĕ (r + schwa) and lĕ (l + schwa)." (p. 372).
*   **Analysis:** No primary source provides evidence for a phonological long schwa (`əː`) as the spoken reflex of Sanskrit `ṝ` in Old Javanese. Javanese speakers did not natively maintain Sanskrit vowel duration, and certainly did not invent a long schwa to do so. The adaptation was simply to `rĕ` (`rə`).

## 4. Long Syllabic-Liquid Analysis
*   Are long syllabic liquids evidenced? Yes, but almost exclusively as orthographic features in Sanskrit loans (e.g., `kṝta`, `nṝpa`).
*   Is the schwa adaptation valid for the long form? The qualitative adaptation (`r` + schwa) is valid, but the quantitative preservation (`ː`) is not.
*   By mapping `r̩ː → rəː`, the code creates an analogical fallacy: it assumes that because `r̩` becomes `rə`, `r̩ː` must become `rəː`. This conflates orthographic length with historical phonetic reality, which contradicts the core premise of Profile A (Reconstructed Spoken).

## 5. Profile A Transformation Table

| Transformation | Current Status | Historical Evidence | Confidence | Allowed Policy | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `bʱ → b` | EVIDENCE-BACKED | Teselkin, Van der Molen | High | KEEP | Spoken merger |
| `dʱ → d` | EVIDENCE-BACKED | Teselkin, Van der Molen | High | KEEP | Spoken merger |
| `gʱ → g` | EVIDENCE-BACKED | Teselkin, Van der Molen | High | KEEP | Spoken merger |
| `pʰ → p` | EVIDENCE-BACKED | Teselkin, Van der Molen | High | KEEP | Spoken merger |
| `ś → s` | EVIDENCE-BACKED | Teselkin | High | KEEP | Spoken merger |
| `ṣ → s` | EVIDENCE-BACKED | Teselkin | High | KEEP | Spoken merger |
| `r̩ → rə` | PROVISIONAL | Acri & Griffiths (2014) | Mod | KEEP | Adaptation to native phonotactics |
| `r̩ː → rəː` | PROVISIONAL | **NONE** | **ZERO** | **REVERT** | Unsupported analogical extension |
| `l̩ → lə` | PROVISIONAL | Acri & Griffiths (2014) | Mod | KEEP | Adaptation to native phonotactics |
| `l̩ː → ləː` | PROVISIONAL | **NONE** | **ZERO** | **REVERT** | Unsupported analogical extension |

## 6. Backend Adapter Analysis
The `AcousticMapper` (`_ESPEAK_ID_APPROXIMATION`) correctly functions as a backend-specific quarantine layer.
*   **Target:** `ʈ` (retroflex)
*   **eSpeak Input:** `t` (dental/alveolar)
*   **Status:** `BACKEND_APPROXIMATION`
*   **Analysis:** This successfully quarantines a backend limitation. It drops the retroflex distinction in audio, but because it occurs *after* the linguistic Profile layer, it does not alter the canonical data or linguistic policy claims. This is excellent engineering.

## 7. Profile/Backend Boundary Analysis
The `r̩ː → rəː` mapping in `ProfileAStrategy` violates the boundary. It invents a linguistic form (`rəː`) simply to provide a mapping target. The fact that the backend adapter subsequently maps `"rəː": "r@"` (stripping the length entirely) demonstrates that `rəː` was merely an engineering bridge, not a linguistic reality. Engineering bridges belong in the backend adapter, not in the Profile layer.

## 8. Adversarial Question Result
**"Would we still implement r̩ː → rəː if eSpeak did not exist?"**
**NO.** If eSpeak did not exist, we would map `r̩ː` to `rə` (because spoken Old Javanese collapsed Sanskrit vowel duration and adapted vocalic liquids to short schwa forms), or we would leave it `UNRESOLVED`. We would never invent a phonologically anomalous "long schwa" (`rəː`) just to maintain parity with a duration marker.

## 9. Conflicts Found
1.  `ProfileAStrategy` claims `r̩ː → rəː` is a `PROVISIONAL_RECONSTRUCTION` cited to "P5-002", but P5-002 explicitly forbids creating a duration claim for `əː`.
2.  The apparent acoustic success of `kṝta` is a false positive: the Profile layer creates `rəː`, and the backend adapter immediately destroys it to `r@`, hiding the phonological error from the listener.

## 10. Recommended Disposition
1.  **Modify `ProfileAStrategy`:** Change `_LIQUID_ADAPTATIONS` to map `"r̩ː": "rə"` and `"l̩ː": "lə"`. This correctly reflects the spoken Old Javanese reality (adaptation to schwa, loss of non-native duration).
2.  **Maintain `AcousticMapper`:** The eSpeak adapter is architecturally sound and should be kept as-is.

## 11. Final Self-Audit
1. **Did we find primary-source support for r̩ː → rəː?** No.
2. **Did we find primary-source support for l̩ː → ləː?** No.
3. **Did we accidentally infer long-form behavior from short-form behavior?** The previous implementation did exactly this.
4. **Did we confuse transcription with pronunciation?** Yes, by trying to map a transliterated length macron (`ṝ`) directly onto an adapted phonetic schwa (`rəː`).
5. **Did eSpeak limitations influence linguistic policy?** Yes, the `rəː` mapping was implicitly accepted because eSpeak's subsequent fallback masked the phonological impossibility.
6. **Does `ʈ → t` remain explicitly backend-scoped?** Yes, it is safely quarantined in `AcousticMapper`.
7. **Does the current Profile A layer contain any backend workaround?** Yes, `rəː` acts as one.
8. **Should the current 97-test implementation be preserved?** No. It must be partially reverted/modified. The tests expecting `rəː` must be updated to expect `rə`.

**FINAL VERDICT:** POLICY-CORRECTION-REQUIRED
