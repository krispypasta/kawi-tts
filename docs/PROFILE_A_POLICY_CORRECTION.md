# PROFILE A POLICY CORRECTION

## 1. What Was Wrong
The previous implementation in `ProfileAStrategy` mapped the canonical long vocalic liquid `r̩ː` to `rəː` (and `l̩ː` to `ləː`). This mapping attempted to preserve the duration marker `ː` on the adapted Javanese schwa, inventing a phonologically impossible "long schwa" (`əː`) reflex. This violated the boundary between linguistic reconstruction and backend engineering, functioning entirely as an engineering workaround for the eSpeak backend.

## 2. Evidence that Disproved It
The Deep Evidence Reconciliation audit (see `docs/PROFILE_A_BACKEND_EVIDENCE_RECONCILIATION.md`) demonstrated that:
- Zoetmulder (1982) transliterates these as `rĕ` / `lĕ`.
- Acri & Griffiths (2014) confirm Old Javanese speakers adapted vocalic liquids to short Javanese phonetic counterparts: Javanese `rĕ` (`rə`) and `lĕ` (`lə`).
- No scholarly source supports the invention of a "long schwa" to preserve Sanskrit `ṝ`/`ḹ` duration in everyday Old Javanese speech.

## 3. Corrected Profile A Behavior
The `ProfileAStrategy` has been updated to reflect the evidence:
*   **`r̩ː` → `rə`** (Loss of non-native duration, adaptation to native phonotactics)
*   **`l̩ː` → `lə`** (Loss of non-native duration, adaptation to native phonotactics)
These rules are correctly classified as `PROVISIONAL_RECONSTRUCTION`, adhering to Acri & Griffiths's observations of Javanese transcription.

## 4. Why the Mistake Occurred
The mistake occurred due to an analogical fallacy combined with backend-driven testing. The previous engineer observed that `r̩` became `rə`, and assumed `r̩ː` must therefore become `rəː` to prevent the token from falling through the dictionary unhandled. Because the eSpeak backend adapter subsequently stripped the duration anyway (`"rəː": "r@"`), the error was invisible in the audio output and "passed" all regression checks, hiding a severe phonological hallucination in the linguistic policy layer.

## 5. Backend Boundary Explanation
This correction restores the core architectural boundary:
*   **Canonical:** Preserves source distinctions (`r̩ː`, `l̩ː`).
*   **Profile A:** Applies linguistic/reconstruction policy (`r̩ː → rə`, `l̩ː → lə`), not what sounds good on a specific backend.
*   **AcousticMapper (eSpeak adapter):** Handles backend-specific approximations (e.g., `ʈ → t`, `bʱ → bh`, `rə → r@`).

The `AcousticMapper` correctly retains its `BACKEND_APPROXIMATION` definitions, serving as the sole quarantine layer for eSpeak constraints without altering the phonological truth encoded in the Profile layers.

## 6. Tests Changed
1.  **`tests/test_acoustic_mapper_profile_a.py`**: Updated `test_profile_a_long_vocalic_liquids_handled` to assert that long vocalic liquids (`r̩ː`, `l̩ː`) adapt to the short schwa base (`rə`, `lə`) and lose their duration, rather than retaining duration.
2.  **`tests/regression_corpus.tsv`**: Corrected the expected Profile A outputs for `kṝta` and `kḹpta` from `k-rəː-t-a` and `k-ləː-t-a` to `k-rə-t-a` and `k-lə-p-t-a` respectively.

## 7. Final Verification Results
*   **Test Suite:** 97/97 tests passing (0 regressions).
*   **Regression Corpus:** 100/100 forms passing.
*   **CLI Traces:** `kṝta`, `BHAṬĀRA`, `śānti` trace cleanly.
    *   `kṝta` canonical `k-r̩ː-t-a` -> Profile A `k-rə-t-a` -> Acoustic A `kr@ta`.
*   **Audio Generation:** `run_audio_demo.py` ran successfully. The backend adapter continues to safely proxy the approximations without glottal fallback garbage.

**STATUS:** POLICY-CORRECTION-GO
