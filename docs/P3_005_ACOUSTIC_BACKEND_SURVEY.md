# P3-005: Acoustic Backend Survey & Decision Gate

**Date:** 2026-10-07
**Mode:** Engineer/Builder
**Target:** Profile A (Reconstructed Historical Spoken Old Javanese)

## 1. Executive Summary

This document surveys the available acoustic text-to-speech (TTS) backends capable of synthesizing Profile A. Given the total absence of historical Kawi speech data, a purely data-driven neural TTS approach is impossible. We must use a hybrid architecture: a deterministic linguistic front-end passing structured phonemes to an acoustic backend. The survey concludes that while Modern Javanese neural models (like VITS/MMS) offer naturalness, they will force the premature loss of uncertain historical phonemes (like aspirates and vowel length). Therefore, a two-stage backend strategy is recommended: a rule-based prototype (eSpeak-ng) to validate the lossless linguistic pipeline, followed by a targeted cross-lingual neural transfer strategy.

## 2. Current Constraints

- **Research-First Pipeline:** Kawi-TTS relies on reconstructed linguistic evidence, not historical recordings.
- **Information Preservation:** The internal G2P representation currently distinguishes uncertain phonemes (`ā, ī, ū`, `ś, ṣ`, `bh, dh`, `ṛ, ḷ`). The chosen backend must either natively support these or allow an explicit **Acoustic Mapping** layer to collapse them. It must not silently erase distinctions.
- **Profile Independence:** The backend architecture must eventually support Profile A (Historical Spoken), Profile B (Scholarly Reading), and Profile C (Balinese Performance) without hard-coding assumptions.
- **No Kawi Audio:** There is absolutely no native, conversational Old Javanese training data.

## 3. Candidate Backend Survey

### Candidate A: Rule-Based / Formant Synthesis (eSpeak-ng)
- **Architecture:** Formant synthesis engine.
- **Interface:** Accepts raw text or direct IPA/Kirshenbaum phoneme strings.
- **Language Support:** Custom phoneme inventories can be defined via straightforward text files.
- **Ability to preserve distinctions:** **High**. eSpeak can natively model length (`[aː]`), aspirates (`[bʱ]`), and vocalic liquids (`[r̩]`). No information needs to be discarded.
- **Training requirements:** None. Rule compilation only.
- **Inference requirements:** Extremely low (CPU only).
- **Licensing:** GPLv3 (Open Source).
- **Advantages:** Perfectly preserves all Profile A internal representations. Highly deterministic. Excellent for debugging the G2P pipeline.
- **Disadvantages:** Highly robotic, unnatural voice quality.
- **Suitability:** **Excellent for initial prototype.**

### Candidate B: Modern Javanese Neural TTS (MMS-TTS-JAV / Piper VITS)
- **Architecture:** VITS (Variational Inference with adversarial learning for end-to-end TTS).
- **Interface:** Character or phoneme inputs mapped to a predefined dictionary.
- **Language Support:** Modern Javanese (jv-ID).
- **Ability to preserve distinctions:** **Low**. Modern Javanese models lack acoustic representations for phonemic vowel length, aspirates, and Sanskrit sibilants. These would either cause inference errors or be ignored unless explicitly collapsed by an Acoustic Mapper.
- **Training requirements:** Fine-tuning requires a CUDA GPU (e.g., 24GB VRAM) and a speech dataset.
- **Inference requirements:** Standard CPU (via ONNX) or lightweight GPU.
- **Licensing:** MMS-TTS is CC-BY-NC 4.0 (Non-Commercial). OpenSLR 41 datasets are CC-BY-SA 4.0.
- **Advantages:** Very natural, human-like voice. Natively models the Javanese dental vs. alveolar contrast (`t/ṭ`, `d/ḍ`) and the pepet (`ə`).
- **Disadvantages:** Forces the loss of historical/Sanskrit phonological distinctions. Requires an explicit Acoustic Mapper to map Kawi phonemes to Modern Javanese capabilities.
- **Suitability:** **Excellent for final V1 acoustic output, but requires lossy mapping.**

### Candidate C: Cross-Lingual / Multilingual Neural TTS
- **Architecture:** VITS / Piper trained on multiple languages (e.g., Javanese + Hindi/Sanskrit).
- **Interface:** Global IPA representation.
- **Ability to preserve distinctions:** **Moderate/High**. By leveraging Hindi/Sanskrit acoustic spaces, the model could theoretically synthesize aspirates (`bh`) and vowel length (`ā`) while maintaining Javanese prosody.
- **Training requirements:** High. Requires joint training on multiple corpora using a cloud GPU.
- **Suitability:** **A potential future research avenue, but too complex for the immediate V1 prototype.**

## 4. Data Availability

- **Available Kawi Text:** Yes (GRETIL, Old Javanese Wordnet). Suitable for G2P testing.
- **Available Kawi Speech:** **None.** No historical spoken audio exists.
- **Modern Javanese Speech:** Yes (OpenSLR 41, ~1.8 GB). Highly relevant for native Austronesian phonology.
- **Balinese Performance Speech:** Yes (Bali 1928, etc.). **CRITICAL WARNING:** This represents Profile C (chanted, metrical duration, modern phonological mergers). It is fundamentally incompatible with Profile A (conversational, historical) and must NOT be used to train Profile A models.
- **Multilingual Speech:** Yes (Common Voice, MMS corpus). Available for cross-lingual transfer.

## 5. Information-Loss Audit

If a Modern Javanese neural backend (Candidate B) is used directly, an Acoustic Mapper must bridge the internal G2P representation and the backend.

| Distinction | Internal Rep | Backend Support (Mod. Jav.) | Loss Risk | Where Mapping Should Occur |
| :--- | :--- | :--- | :--- | :--- |
| **ə** | `/ə/` | SUPPORTED | None | N/A |
| **ŋ, ɲ** | `/ŋ/, /ɲ/` | SUPPORTED | None | N/A |
| **ṭ, ḍ** | `/ṭ/, /ḍ/` | SUPPORTED | None | N/A (Mod. Jav. naturally contrasts dental/alveolar) |
| **ṇ** | `/ṇ/` | UNSUPPORTED | HIGH | Acoustic Mapper (Merge to `/n/`) |
| **ā, ī, ū** | `/aː/, /iː/, /uː/` | UNSUPPORTED | HIGH | Acoustic Mapper (Merge to `/a/, /i/, /u/`) |
| **ś, ṣ** | `/ś/, /ṣ/` | UNSUPPORTED | HIGH | Acoustic Mapper (Merge to `/s/`) |
| **Aspirates (bh, dh)**| `/bʱ/, /dʱ/` | UNSUPPORTED | HIGH | Acoustic Mapper (Merge to `/b/, /d/`) |
| **ṛ, ḷ** | `/r̩/, /l̩/` | UNSUPPORTED | HIGH | Acoustic Mapper (Map to `/rə/, /lə/`) |

## 6. Architecture Options

- **Option 1 (Rule-Based Only):** Fast, preserves all historical uncertainty, but sounds robotic.
- **Option 2 (Modern Javanese Transfer Only):** Sounds natural, but requires forcing all uncertain historical features into modern Javanese phonemes via the Acoustic Mapper.
- **Option 3 (Hybrid Prototype Pipeline):** Use a rule-based engine (eSpeak) to validate the lossless linguistic pipeline during Phase 3. Later, swap in a Modern Javanese neural model with an explicit Acoustic Mapper to generate the final V1 output.

## 7. Cloud / GPU Assessment

- **Do we need cloud GPU now?**
  **NO.** We are not currently training. Tokenization, G2P, eSpeak-ng synthesis, and ONNX-based neural inference (Piper) can run entirely on the local HP laptop.
- **Do we need cloud GPU for a future neural prototype?**
  **YES.** Fine-tuning a VITS/Piper model on the OpenSLR 41 Javanese dataset to accept custom Kawi phonemes will require a CUDA-capable GPU (a consumer 24GB VRAM card or basic cloud instance is sufficient; a VITS model will not saturate an H100).
- **What can be done entirely on the local HP laptop?**
  Text normalization, G2P engine design, Acoustic Mapper interface definition, rule-based audio synthesis, and neural model inference.

## 8. Recommendation

**The most defensible NEXT engineering path is the Hybrid Prototype Pipeline (Option 3).**

Rather than rushing to a lossy neural backend, Kawi-TTS should first integrate **eSpeak-ng** as the initial Acoustic Backend.
1. It is the only backend capable of natively synthesizing our rich, lossless internal phoneme array without forcing premature phonological mergers.
2. It proves the pipeline (Normalization → Tokenization → G2P → Audio) works end-to-end.
3. Once the pipeline is verified, we can construct the Acoustic Mapper module to explicitly collapse the unsupported phonemes and feed a Modern Javanese neural TTS model for naturalness.

## 9. Explicit Non-Decisions

- We do NOT decide the final phonetic mapping for the 5 uncertain historical categories (vowel length, aspirates, sibilants, retroflex nasal, vocalic liquids). The decision to collapse these in the Acoustic Mapper remains deferred to Abraham.
- We do NOT commit to a specific neural architecture (VITS vs FastSpeech) yet.

## 10. Proposed P3-006

**Exact Next Task:** Implement the Acoustic Mapper Interface and an eSpeak-ng prototype backend wrapper capable of generating audio directly from the lossless G2P internal phoneme arrays.