# Kawi-TTS v1.1.1 Release Notes

This release finalizes the deterministic TTS engine improvements accumulated since v1.1.0. It solidifies the acoustic backend boundaries, strict ambiguity handling, and evidence-backed Profile A phonology updates.

## What's Changed
- **Evidence-Backed Profile A Mergers:**
  - Applied scholarly consensus for aspirate mergers (`kʰ` → `k`, `gʱ` → `g`, etc.) based on historical Old Javanese pronunciation evidence.
  - Implemented the retroflex nasal merger (`ṇ` → `n`).
  - Corrected long vocalic liquid policies (e.g. `r̩ː`, `l̩ː`) to their historically supported schwa forms.
- **Epistemic Taxonomy Separation:**
  - Introduced the `SCHOLARLY_RECONSTRUCTION` (Grade B) policy status, separating well-supported reconstructed phonemes from explicitly `EVIDENCE_BACKED` (Grade A) tokens.
- **Punctuation & Prosody:**
  - Sentence-boundary and punctuation tokens are now preserved and properly propagated down to the acoustic pipeline for synthesizer prosody mapping.
- **Backend Architecture Separation:**
  - Removed eSpeak-specific fallbacks (`_ESPEAK_ID_APPROXIMATION`) from the generic `AcousticMapper`. The mapper now outputs pure, engine-agnostic IPA.
  - Safely integrated `id` voice ID fallback approximations directly into the `ESpeakBackend`, utilizing safe descending-length string replacement.
- **Stricter Synthesis Pipeline:**
  - Added strict ambiguous-input handling (`AmbiguousTokenError`), ensuring the TTS engine fails explicitly on unresolved forms rather than silently inventing a pronunciation.

*Note on Linguistic Certainty:* Kawi-TTS outputs represent specific combinations of historical evidence, scholarly reconstructions, and engineering approximations. We explicitly DO NOT claim historical audio authenticity or neural naturalness; these outputs are deterministic acoustic models of reconstructed linguistic theories.
