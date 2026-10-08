# Kawi-TTS Neural Training Readiness Specification

This document defines the strict prerequisites and architectural protocols required before initiating training for a legitimate Kawi-TTS Neural Acoustic Model. 

It is informed by the deterministic architecture of Kawi-TTS v1.1.1, the Kawi phonology audits, and the phonetic collapse observed during the `de_DE-thorsten` and `en_US-ljspeech` neural feasibility experiments.

**Project Phase Status:** Neural TTS training remains strictly **BLOCKED** at the Stage 1 Data Readiness gate until these conditions are met.

---

## I. Data & Speaker Prerequisites

### 1. Training-Data Requirements
Audio must be studio-quality or clean-room quality (low noise floor, no reverb, no background artifacts). The dataset must consist of short, sentence-level utterances (2–10 seconds) with exact, verbatim textual transcriptions. 

### 2. Qualified-Speaker Requirements
The speaker must be a trained linguist, philologist, or highly proficient practitioner of Old Javanese (Kawi). 
- **Consistency is critical:** The speaker must naturally and consistently articulate Kawi phonotactics without reverting to modern Indonesian/Javanese reduction patterns.
- **Do not assume oracle status:** A modern speaker’s performance is an acoustic approximation, not a historical oracle. The goal is to capture the *phonemic distinctions* intended by Profile A.

### 3. Recording Protocol
- Uncompressed WAV format (16-bit or 24-bit PCM).
- Mono channel.
- Minimum 22.05 kHz sample rate (44.1 kHz preferred).
- Consistent microphone placement and gain staging across all sessions.
- Emotional neutrality (flat, clear reading style preferred for V1).

### 4. Licensing / Consent / Provenance
- **Dataset License:** Must be explicitly released under CC0, CC-BY, MIT, or Apache 2.0. 
- **Consent:** The speaker must provide documented, irrevocable consent for their voice to be used to train open-weights neural models.
- **Commercial Restrictions:** Datasets with Non-Commercial (NC) or Share-Alike (SA) clauses are strictly prohibited, as they would poison the Kawi-TTS repository license.
- **Provenance:** The origin of the text corpus and the identity/qualifications of the speaker must be documented.

---

## II. Phonetic & Transcription Specifications

### 5. Phoneme Inventory Coverage
The recording script must be phonetically balanced and exhaustively cover the Profile A deterministic phoneme output map. This includes all consonants, vowels, and valid consonant clusters defined in the frozen v1.1.1 engine.

### 6. Kawi-Specific Distinctions That MUST Survive
The dataset design and speaker execution must rigorously preserve:
- **Dental vs. Retroflex:** `t` vs `ṭ` (`/t/` vs `/ʈ/`), and `d` vs `ḍ` (`/d/` vs `/ɖ/`). *Failure to distinctively record these will result in acoustic collapse.*
- **Schwa Stability:** The schwa `ĕ` (`/ə/`) must be articulated clearly and must not be swallowed or arbitrarily shifted to `/a/` or `/u/`.
- **Vocalic Liquids:** `ṛ` (`/rə/` or `/r/`) must be consistent with Profile A's rules.
- **Consonant Clusters:** Complex onsets/codas (e.g., `rj`, `mw`, `ngh`) must be pronounced without inserting epenthetic (ghost) vowels.

### 7. Dataset Format
Standard LJSpeech format is required for seamless ecosystem compatibility:
`metadata.csv` structured as `ID|Transcription|Normalized Transcription`.

### 8. Transcription Format
Transcriptions must perfectly match the Kawi-TTS v1.1.1 `synthesize(strict=True)` ingestion pipeline. 
- **Format:** The final metadata must contain the *exact* deterministic Profile A IPA arrays (e.g., `sang hjang baʈara`) to completely bypass the neural model's internal G2P.

### 9. Alignment Requirements
The training architecture must support internal monotonic alignment (e.g., VITS/Piper monotonic alignment search). If external alignment is required, a Kawi-specific Montreal Forced Aligner (MFA) dictionary must be generated directly from the v1.1.1 deterministic engine.

### 10. Train/Dev/Test Split
- **Train:** 90%
- **Dev (Validation):** 5%
- **Test (Holdout):** 5%
Holdout sentences must contain complex clusters and retroflexes to evaluate phonetic collapse accurately.

### 11. Minimum and Preferred Corpus Characteristics
- **Empirical Minimum:** ~2 to 5 hours of clean audio for a fine-tuned single-speaker model.
- **Preferred:** ~10+ hours for a model trained from scratch.
*(These are TTS industry empirical baselines, not historical rules).*

### 12. Speaker Strategy
**Single Speaker.** Multi-speaker datasets introduce severe complexities in phonetic alignment and risk diluting the strict pronunciation invariants required by Profile A. 

---

## III. Architecture & Engineering Requirements

### 13. Model Architecture Candidates
Must be a permissive, modern architecture capable of real-time CPU inference:
- **VITS (Piper):** Highly preferred due to proven bypass mechanisms (`[[ipa]]`), CPU efficiency, and MIT licensing.
- **Kokoro TTS:** Excellent lightweight alternative.
- **Sherpa-ONNX:** Viable for deployment.

### 14. Phoneme Encoder Requirements
The neural architecture must expose a direct phoneme/ID injection API. 
**No hidden G2P:** The model must not attempt to guess Old Javanese pronunciation from Latin text. It must accept the v1.1.1 output arrays deterministically.

### 15. Handling of Unfamiliar Phonemes
The phoneme ID map used during training must be explicitly constrained to the Kawi-TTS inventory. Out-of-vocabulary (OOV) phonemes during inference should raise a hard error (handled by Kawi-TTS `AmbiguousTokenError`), not fail silently.

### 16. Prosody / Punctuation Handling
Punctuation tokens (`,`, `.`, `!`, `?`) emitted by v1.1.1 must be mapped to distinct pause/silence IDs in the neural map. Emotional prosody prediction is out of scope.

### 17. Vocoder Requirements
Must be integrated (e.g., HiFi-GAN natively inside VITS) and lightweight enough to maintain a Real-Time Factor (RTF) of < 1.0 on standard consumer CPUs.

---

## IV. Evaluation, Constraints, & Gates

### 18. Evaluation Metrics
- **RTF (Real-Time Factor):** Must run faster than real-time on CPU.
- **MCD (Mel Cepstral Distortion):** To measure acoustic fidelity against the holdout set.
- **Phoneme Error Rate:** Measured via ASR (if a Kawi ASR ever exists) or human evaluation.

### 19. Human Listening Protocol
Human evaluation evaluates **engineering fidelity**, not historical truth. 
Reviewers must evaluate:
1. Did the neural model preserve the retroflex/dental distinction?
2. Did it swallow the schwa?
3. Did it hallucinate epenthetic vowels in clusters?
4. Is it intelligible?

### 20. Failure Criteria
The trained model must be discarded if it:
- Acoustically merges `ṭ` into `t` (Phonetic Collapse).
- Randomly varies vowel length in violation of Profile A's neutralization policy.
- Introduces severe artifacts, static, or robotic degradation worse than eSpeak.

### 21. Reproducibility Requirements
All training scripts, dataset processing scripts, and final ONNX weights must be version-controlled, open-source, and fully reproducible from the raw audio directory.

### 22. Zero-Budget Constraints
Core development must remain viable on a $0 budget. 
- The dataset must be crowdsourced, donated, or public domain.
- Training must be achievable on free tiers (e.g., Google Colab T4 GPUs) or consumer hardware within reasonable timeframes (under 72 hours).

### 23. Exact GO / NO-GO Conditions for Starting Training

**NO-GO (Current State):**
- No Kawi acoustic dataset exists.
- No legal/permissive audio exists.
- The pipeline relies on foreign models that collapse retroflexes.

**GO (Authorization to Train):**
Training may only commence when:
1. [ ] A minimum 2-hour, single-speaker, clean Kawi audio dataset is secured.
2. [ ] The audio has explicit CC0, MIT, or Apache 2.0 licensing.
3. [ ] Transcriptions are verified to cleanly map to Profile A phonemes without `AmbiguousTokenError`.
4. [ ] The speaker successfully articulated the `t` vs `ṭ` / `d` vs `ḍ` distinctions in the source audio.
5. [ ] The compute environment (local or free cloud) is provisioned.

*Do not begin neural training until all GO conditions are strictly satisfied.*
