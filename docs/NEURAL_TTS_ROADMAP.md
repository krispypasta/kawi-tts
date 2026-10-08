# Kawi-TTS Neural Speech Synthesis Roadmap

**STATUS:** NEURAL TTS RESEARCH PHASE CONCLUDED. NO IMPLEMENTATION AUTHORIZED.
**CONCLUSION:** B — TECHNICALLY FEASIBLE BUT DATA / LINGUISTIC CONDITIONS ARE NOT YET SATISFIED.

This roadmap defines the minimum conditions required before Kawi-TTS can responsibly prototype a neural acoustic backend. It is designed to prevent premature model training and to ensure clear exit criteria for the research phase.

---

## 1. Current Baseline
The current Phase 4 (v1.1.0) engine uses a strictly deterministic pipeline ending in an `eSpeak` parametric synthesizer.
*   **[EVIDENCE]** Canonical phonemes are mapped deterministically based on scholarly consensus.
*   **[ENGINEERING CONVENTION]** eSpeak acts as the acoustic renderer, providing 100% predictable articulation at the cost of robotic naturalness.
*   **[PROJECT ASSUMPTION]** Deterministic rigidity is preferable to neural hallucination for preserving historical linguistic distinctions (Profile A vs. Profile B).

## 2. Why Neural TTS is Deferred
Neural TTS is currently deferred because modern end-to-end models inherently hallucinate pronunciation to achieve naturalness.
*   **[UNCERTAINTY]** There are no native speakers of Old Javanese to provide ground-truth acoustic data.
*   **[INFERENCE]** Training an end-to-end model on modern Javanese or Indonesian audio would cause the model to incorrectly apply modern phonotactics to historical Kawi texts.
*   **Conclusion:** The project must establish a secure "Neural Backend Contract" before any acoustic neural research can begin, separating the linguistic authority from the audio renderer.

## 3. Neural Backend Contract
Any future neural backend must adhere to the following architecture contract:

`Text → Normalization → Tokenization → G2P → Canonical Representation → Profile Strategy → Neural Acoustic Backend → Waveform`

*   **A. Input accepted:** The neural backend MUST accept only explicit Canonical Phonemes / IPA arrays. It MUST NOT ingest raw orthographic text.
*   **B. Deterministic components:** The entire pipeline up to the `Neural Acoustic Backend` remains 100% deterministic.
*   **C. Preserving canonical distinctions:** The backend must guarantee distinct acoustic outputs for distinct input phonemes (unless explicitly instructed to merge them by the `Profile Strategy`).
*   **D. Representing uncertainty:** The neural model must not mask linguistic uncertainty with confident audio smoothing. **[UNCERTAINTY]** must be tracked in the canonical representation layer.
*   **E. What the model may learn:** The model may learn micro-prosody (F0 jitter), duration distribution, and coarticulation.
*   **F. What the model MUST NOT learn:** The model MUST NOT learn grapheme-to-phoneme rules, syllabification, or historical pronunciation policies.
*   **G. Backend interchangeability:** The neural module must be a swappable sink. Replacing it with `eSpeak` or another vocoder must require zero changes to the linguistic frontend.

## 4. Data Readiness Gate
Before any training or fine-tuning begins, the following data checklist must be evaluated:

### REQUIRED
*   **Clear Provenance & Consent:** The data source must have a documented origin.
*   **Licensing:** Open-source compatible (CC0, MIT, or CC-BY).
*   **Phoneme Coverage:** The dataset (or base model) must cover a definable subset of the Kawi IPA inventory.
*   **Alignment:** Accurate phoneme-to-audio timestamps or a proven monotonic alignment search mechanism.

### STRONGLY PREFERRED
*   **High SNR:** Studio-quality recordings to prevent the model from learning background noise.
*   **Train/Dev/Test Split:** Established explicitly before training starts.

### OPTIONAL
*   **Multi-speaker diversity:** Single-speaker is acceptable for the MVP.

### BLOCKING CONDITIONS (NO-GO)
*   **[BLOCKER]** Base models with restrictive commercial licenses (e.g., CPML) where the project lacks clearance.
*   **[BLOCKER]** Scraping unconsented audio data (e.g., YouTube Kakawin readings without explicit permission).
*   **[BLOCKER]** Attempting to use generative AI / synthetic voices as "ground-truth historical evidence" for training.

## 5. Linguistic Readiness Gate
We can only declare "Data is defensible for training" when every phonetic mapping used to train the model falls into an accepted epistemic category.

1.  **Evidence-Backed:** Directly supported by historical linguistics / epigraphy. (Must be preserved).
2.  **Reconstruction:** Comparative linguistic derivation. (Must be preserved, but documented as reconstructed).
3.  **Engineering Approximation:** **[ENGINEERING CONVENTION]** Mapping a Kawi sound to an available acoustic proxy because the neural backend lacks the specific phoneme (e.g., falling back to a standard dental stop if a retroflex is missing). Must be explicitly logged.
4.  **Unresolved:** Contradictory evidence. The frontend must choose one based on explicit policy; the neural model simply executes the choice.

**[BLOCKER]** Modern Javanese intuition or Balinese performance norms cannot be used as substitute historical evidence.

## 6. Data Acquisition Options

### A. Qualified Scholar Recording (Zero-shot or Fine-tuning)
*   **Needs:** 15-30 mins of a scholar reading Kawi text in a studio.
*   **Pros:** Exact phonotactics; highly defensible.
*   **Cons/Risks:** Bias of the scholar's native tongue; extremely hard to secure on a zero budget.

### B. Existing Legally Reusable Speech Corpus (e.g., Mozilla CV Indonesian)
*   **Needs:** Filtering script to extract high-SNR Indonesian speech.
*   **Pros:** CC0 license; vast data.
*   **Cons/Risks:** No Kawi text. Requires cross-lingual transfer.

### C. Multilingual / Indonesian Corpus + Cross-Lingual Transfer
*   **Needs:** Pretrained Indonesian base model (e.g., Piper/VITS) + IPA mapping matrix.
*   **Pros:** Near-zero budget feasible.
*   **Cons/Risks:** Phonetic mismatch (see Section 7). High engineering risk.

### D. Synthetic / Generated Speech
*   **Needs:** eSpeak output used to train a neural vocoder.
*   **Pros:** 100% linguistic control.
*   **Cons/Risks:** Will likely inherit the robotic qualities of the source audio. **[EVIDENCE]** Synthetic speech cannot be claimed as historical evidence.

## 7. Cross-Lingual Transfer Risks
If relying on Indonesian/Javanese pretrained models (Option C), the following **[UNCERTAINTY]** gaps exist:
*   **Retroflex vs. Dental (ṭ/t, ḍ/d):** Indonesian does not natively contrast these. The base model may merge them acoustically.
*   **Aspirated Stops (bʰ, dʰ):** Absent in modern standard Indonesian.
*   **Syllabic Liquids (ṛ, ḷ):** Require strict mapping rules (e.g., mapping to schwa + consonant as per Profile A research).
*   **Rule:** What can be transferred is basic vocal tract resonance (vowels, common consonants). What must be added/approximated are Kawi-specific distinctions. We must NOT assume "Indonesian TTS + Kawi text = Kawi TTS."

## 8. Architecture Decision Tree
*   **IF** dataset is extremely small (few seconds) $\rightarrow$ **REJECT** (Zero-shot models hallucinate pronunciation).
*   **IF** qualified single-speaker Kawi dataset available (15+ mins) $\rightarrow$ Fine-tune a VITS/Piper base model using IPA inputs.
*   **IF** only Indonesian pretrained models available $\rightarrow$ Execute Cross-Lingual Transfer using strict phonetic mapping. Document engineering approximations.
*   **IF** Kawi-specific phonetic coverage is completely unmappable to the base model $\rightarrow$ **ABORT** (Remain on eSpeak).
*   **IF** only synthetic data available $\rightarrow$ Train a HiFi-GAN vocoder on eSpeak mel-spectrograms (Engineering experiment only).

## 9. Minimum Viable Neural Prototype (MVP)
If all blocking conditions clear, the first prototype shall be:
*   **Input:** Canonical IPA strings (NOT text).
*   **Model Class:** Lightweight edge model (e.g., Piper TTS / VITS).
*   **Data:** High-quality subset of Indonesian CC0 data or 15 mins of scholar audio.
*   **Output:** 22kHz+ Waveform.
*   **Success Criteria:** Model successfully reads 50 Kawi test sentences without skipping phonemes, stuttering, or hallucinating modern Indonesian vowels in place of Kawi schwas.
*   **Explicit Non-Goal:** Perfect emotional prosody, voice cloning, multi-speaker support.

## 10. Evaluation Methodology
### Engineering Quality (Objective)
*   Intelligibility (Word Error Rate via human transcription).
*   Stability & Artifact Rate.
*   Latency / Real-Time Factor (RTF).

### Linguistic Evaluation (Objective)
*   Canonical Fidelity: Does the audio distinctly separate minimal pairs defined by the frontend?
*   Documented Uncertainty: Are engineering fallbacks accurately logged?

### Human Listening (Subjective)
*   Evaluators (e.g., Abraham) assess ONLY: audibility, intelligibility, obvious synthesis failures, and consistency.
*   **[PROJECT ASSUMPTION]** Human reviewers DO NOT determine historical authenticity. If a reviewer says "it sounds wrong" but the frontend strictly followed the epigraphic evidence, the evidence wins.

## 11. Go / No-Go Gate
### GO
*   A CC0/MIT base model or dataset is secured.
*   The IPA mapping from Kawi to the model's acoustic space is documented and approved.
*   The model accepts deterministic IPA input.

### NO-GO
*   The only available models force raw text input (hallucination risk).
*   The only data available violates copyright or consent.
*   The cross-lingual base model completely fails to articulate critical Kawi distinctions (e.g., collapses all vowels into Schwa).

### CONDITIONAL GO
*   We can build a prototype using Indonesian base models that merges retroflexes, BUT it is strictly labeled as an **[ENGINEERING CONVENTION]** experiment and is explicitly excluded from the v1.x production release.

## 12. Zero-Budget Path
**Zero-Budget Feasibility:**
The only currently responsible zero-budget path is adapting an open-source Indonesian CC0/MIT model (e.g., Piper) via cross-lingual transfer, using a manually constructed IPA fallback matrix.
**[UNCERTAINTY]** If mapping Kawi phonemes to Indonesian acoustic embeddings destroys critical canonical distinctions (like aspirates), then:
> **"No responsible zero-budget path currently established for full acoustic fidelity."**

## 13. Staged Roadmap
*   **STAGE 0 — Current deterministic baseline**
    *   *Objective:* Maintain robust eSpeak output. (Currently Complete).
*   **STAGE 1 — Data readiness**
    *   *Objective:* Secure CC0/MIT dataset or pretrained base model.
    *   *Exit Criteria:* Legal and phonetic audit of the dataset passes.
*   **STAGE 2 — Linguistic readiness**
    *   *Objective:* Draft the IPA-to-Acoustic mapping matrix.
    *   *Exit Criteria:* All engineering phonetic approximations are explicitly documented.
*   **STAGE 3 — Prototype preparation**
    *   *Objective:* Build the pipeline hook between Kawi-TTS's `AcousticMapper` and the neural model's input tensor.
*   **STAGE 4 — Minimal neural prototype**
    *   *Objective:* Train/Fine-tune the model.
*   **STAGE 5 — Evaluation**
    *   *Objective:* Run the 50-sentence test suite.
    *   *Blocker:* High artifact rate or canonical collapse.
*   **STAGE 6 — Possible integration**
    *   *Objective:* Merge to a non-production experimental branch for peer review.

## 14. Open Questions
1.  How do we objectively verify the acoustic rendering of reconstructed historical retroflexes when using a base model trained on a language that lacks them?
2.  Will the neural model's implicit coarticulation smooth over syllable boundaries that historical linguistics dictate should be sharply separated?

## 15. Explicit Non-Goals
*   Emotional TTS / Expressive generation.
*   Voice cloning / Few-shot voice transfer.
*   Bypassing the deterministic G2P.
*   Production-ready cloud deployment.

## 16. Final Recommendation
The Kawi-TTS neural branch is currently blocked at the Stage 1 Data Readiness gate. We must not proceed to Stage 3 or 4 until the "Data Readiness" (Stage 1) and "Linguistic Readiness" (Stage 2) gates are definitively cleared. The risk of producing highly convincing but historically inaccurate audio is currently too high.
