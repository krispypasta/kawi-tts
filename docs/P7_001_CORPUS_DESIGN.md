# P7-001: Data Acquisition & Corpus Design

## 1. Corpus Purpose
This corpus is an engineering vehicle designed strictly to train a neural acoustic model for Kawi-TTS. 

It is critical to explicitly distinguish between three concepts:
*   **A. Historical Evidence:** The scholarly sources and comparative linguistics proving what Old Javanese sounded like (e.g., evidence that aspirates merged).
*   **B. Reconstructed Linguistic Target:** The Profile A policy, which dictates the specific phoneme sequence the TTS must output (e.g., mapping orthographic `bh` to phonetic `/b/`).
*   **C. Project Engineering Training Data:** The actual modern audio recordings (this corpus) used to teach a neural network how to synthesize the Profile A targets.

**Explicit Disclaimer:** This corpus **cannot** and **does not** prove historically what Old Javanese sounded like. It is a modern acoustic artifact artificially constructed to fulfill the engineering requirements of the P5-002 Profile A policy. 

## 2. Phonetic Coverage
Coverage is derived **strictly** from the current accepted Profile A policy.

**A. Mandatory (Must be recorded distinctly):**
*   Base Austronesian inventory: `/a, i, u, e, o, ə, p, t, k, b, d, g, m, n, ɲ, ŋ, j, r, l, w, s, h/`.
*   **Critical Contrast:** Dental vs. Retroflex stops (`/t/` vs. `/ṭ/`, `/d/` vs. `/ḍ/`). Profile A strictly preserves this contrast. Because modern Indonesian neural models collapse this, it is the highest-priority acoustic feature the corpus must teach the backend.

**B. Useful (Contextual combinations):**
*   Provisional liquid adaptations: `/rə/` (from `ṛ`), `/lə/` (from `ḷ`). While these use base phonemes, recording them in their native phonotactic contexts ensures smooth neural synthesis.

**C. Unresolved / Should Not Be Forced (Excluded from Profile A targets):**
*   **Aspirates (`bh, dh, gh, ph`):** Profile A merges these to plain stops. The speaker must record them as plain stops.
*   **Sibilants (`ś, ṣ`):** Profile A merges these to `/s/`. The speaker must record them as `/s/`.
*   **Vowel Length / Macrons (`ā, ī, ū, əː`):** Profile A treats these as unresolved and strips duration markers as an engineering fallback. The speaker must read them with standard short duration. Do not force artificial lengthening.

*Note: Because this corpus trains strictly for Profile A, the resulting neural model will lack the acoustic embeddings required to synthesize Profile B (which requires actual aspirates and macrons). A separate or expanded dataset would be required later if neural Profile B is authorized.*

## 3. Minimal Corpus Design
Neural models like Piper (VITS) do not automatically require 5 hours of data, especially for single-speaker phonetic fine-tuning.

*   **Pilot Corpus:**
    *   **Scale:** ~50 to 100 utterances (approx. 10–15 minutes of audio).
    *   **Goal:** Prove the model can learn the retroflex vs. dental contrast.
    *   **Speaker Count:** 1 (Single speaker is mandatory for baseline stability).
*   **Production Corpus (If Pilot Succeeds):**
    *   **Scale:** ~1,000 to 1,500 utterances (approx. 1 to 2 hours of audio).
    *   **Goal:** Full diphone coverage and prosodic stability.
    *   **Speaker Count:** 1.

## 4. Sentence Design
Random lexical sampling is insufficient because retroflex consonants (`ṭ`, `ḍ`) appear disproportionately in specific loanwords and restricted native roots. 

*   **Targeted Oversampling:** Sentences must be intentionally constructed or selected to feature `ṭ` and `ḍ` in varied vowel contexts (e.g., `aṭa`, `iṭi`, `uḍu`).
*   **Contrastive Material:** Include minimal or near-minimal pairs in the script (e.g., words containing `t` alongside words containing `ṭ` in the same sentence) to force the neural model to learn the distinct embeddings rather than generalizing them away.
*   **Profile A Enforcement:** The script must explicitly write out the Profile A target (e.g., writing *bhasa* as *basa*) to prevent the human speaker from accidentally applying Profile B (Sanskritized) pronunciation habits.

## 5. Annotation Design
Every recorded `.wav` file must be accompanied by strict metadata in a structured format (e.g., CSV/JSON Lines), capturing:
1.  **Source Text:** The original Old Javanese orthography.
2.  **Normalized Text:** Expanded abbreviations and normalized spelling.
3.  **Canonical Representation:** The exact G2P output array (lossless).
4.  **Profile A Target Representation:** The exact IPA array sent to the backend (the actual ground truth the neural model will train on).
5.  **Speaker/Session Metadata:** ID of the speaker, date, and hardware used.
6.  **Recording Conditions:** Estimated SNR or room descriptor.
7.  **Take Number:** To track revisions.
8.  **Annotation Status:** E.g., `verified`, `needs_review`.
9.  **Evidence/Reference Linkage:** Pointers to the rule dictating the target.
10. **Uncertainty Flags:** E.g., tagging sentences that contain `UNRESOLVED` vowel lengths.

## 6. Licensing
To maintain the project's reproducibility and permissive distribution goals, strict licensing boundaries must be established:
*   **Raw Audio:** Must be explicitly licensed as **CC0 (Public Domain)** or **CC-BY 4.0** by the human speaker via a signed release.
*   **Transcripts & Annotations:** CC0 / CC-BY 4.0.
*   **Trained Weights:** The final neural model weights should explicitly inherit a permissive open-data license (like OpenRAIL or CC-BY), separate from the TTS engine code (which may be GPLv3 if using Piper). 
*   **Verification:** Before any audio is pushed to the repository or a dataset hub, the project owner (Abraham) must explicitly sign the voice release.

## 7. Recording Protocol
*   **Hardware:** Condenser microphone or high-quality dynamic microphone, pop filter, acoustically treated or very quiet room.
*   **Format:** 22.05 kHz (matches VITS/Piper native sample rate), 16-bit, Mono, WAV format.
*   **Loudness Consistency:** All files must be RMS normalized to -23 LUFS to prevent volume-jumping during training.
*   **Speaking Style:** Flat, consistent, declarative reading. Emotive fluctuations will confuse a small dataset.
*   **Retakes:** Any stumble, pop, or breath in the middle of a word requires a full sentence retake.
*   **File Naming:** Deterministic (e.g., `kawi_pilot_0001.wav`), matching the ID in `metadata.csv`.

## 8. Pilot Experiment
Design a 10–20 minute pilot to validate the architecture before committing to a 2-hour recording session.

*   **Target Sentences:** 50 sentences heavily loaded with `/t/`, `/ṭ/`, `/d/`, and `/ḍ/`.
*   **Expected Phonetic Coverage:** Baseline vowels + dental/retroflex stops.
*   **Training Experiment:** Overfit a Piper model (train for 1,000+ epochs on just the 50 sentences) using the Profile A target phoneme IDs.
*   **Evaluation Criteria:** Synthesize a novel, unseen word containing `/ṭ/`. Does the output cleanly articulate the retroflex, distinct from `/t/`?
*   **Failure Conditions:** The model outputs a dental `/t/` instead of `/ṭ/`, or produces severe audio artifacting/buzzing around the retroflex embedding.

## 9. Neural Backend Requirements
Any future backend selected must satisfy these criteria:
1.  **Explicit Phoneme Bypass:** Must accept raw integer IDs or explicit phonetic symbols directly, completely bypassing internal text-to-speech guessing.
2.  **Custom Vocabularies:** Must allow the injection of new phoneme embeddings (e.g., `/ṭ/`) that do not exist in the base (e.g., Indonesian) model.
3.  **CPU Inference:** Must compile to ONNX or a similarly optimized runtime for fast, local CPU generation. 
*Note: Piper perfectly fits these requirements, but the dataset must remain backend-agnostic (pure WAV + IPA) so we can swap to FastSpeech2 or future architectures without re-recording.*

## 10. Human Decisions (Abraham)
Only two decisions require project owner approval to proceed:
1.  **Voice Licensing:** Do you agree to record the pilot corpus and explicitly release your voice audio under a CC0 or CC-BY license?
2.  **Phonetic Capability:** Are you confident in your ability to consistently and distinctly articulate the apical-alveolar vs. sub-apical retroflex contrast (`t` vs. `ṭ`) required by Profile A during a recording session?

## 11. Recommended Milestone Sequence
I recommend the following phase sequence for P7:

*   **P7-001: Corpus Design** (This document) -> *GO criterion: Abraham approves decisions in Section 10.*
*   **P7-002: Pilot Corpus** -> *Record and annotate 50 sentences.*
*   **P7-003: Pilot Neural Experiment** -> *Train and evaluate the retroflex contrast. GO criterion: Successful distinct synthesis of unseen `/ṭ/`.*
*   **P7-004: Scale-up Decision** -> *Authorize the full 1-2 hour recording session.*
