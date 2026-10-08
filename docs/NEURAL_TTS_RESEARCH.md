# Kawi-TTS Neural Speech Synthesis Research Report

## 1. Executive Summary
This document investigates the feasibility of transitioning Kawi-TTS from a deterministic, parametric synthesizer (eSpeak) to a modern, natural-sounding neural backend. Research indicates that while neural TTS is technically feasible for zero-native-speaker languages via fine-tuning and cross-lingual transfer, it poses severe linguistic risks. End-to-end models inherently hallucinate pronunciation, which violates the project's strict "evidence before implementation" mandate. The future path requires retaining the deterministic linguistic frontend while replacing only the acoustic generation backend, treating the neural model as a strict "voice actor" interpreting explicit IPA instructions.

## 2. Current Kawi-TTS Baseline
The current Phase 4 implementation relies on:
`Text -> Deterministic G2P -> Canonical Representation -> Acoustic Mapper -> eSpeak`
This approach grants 100% control over reconstructed historical phonology (Profile A) and scholarly reading norms (Profile B). However, it produces rigid, robotic audio because parametric synthesis lacks the micro-variations found in human vocal folds.

## 3. What Makes TTS Sound Natural
Achieving human-like synthesis requires balancing macro-level structure with micro-level stochasticity. Modern TTS achieves this via:
* **Learned Coarticulation:** Neural networks naturally blur phoneme boundaries, mimicking vocal tract inertia.
* **Stochastic Duration & Rhythm:** Human speech is not perfectly metronomic. Modern models sample duration from a probability distribution rather than enforcing a rigid length.
* **Micro-prosody (F0 Jitter):** Real pitch fluctuates continuously.
* **High-Frequency Texture:** Adversarial discriminators (GANs) force generators to produce realistic breathiness and high-frequency noise, preventing "muffled" artifacts.

## 4. Modern TTS Architecture Survey
* **Tacotron 2:** Autoregressive; highly expressive but slow, suffers from attention-alignment failures.
* **FastSpeech 1/2:** Non-autoregressive; uses explicit predictors for duration, pitch, and energy. Highly controllable but can sound stiff due to deterministic averaging.
* **VITS:** State-of-the-art for naturalness. Uses Conditional VAEs, normalizing flows, and adversarial learning to treat speech as a stochastic distribution. Generates varying, highly natural delivery.
* **StyleTTS 2:** Uses style diffusion and Speech Language Model (SLM) discriminators to achieve human-level naturalness and zero-shot voice cloning.
* **Vocoders (HiFi-GAN):** Generates waveforms from mel-spectrograms using Multi-Period Discriminators (MPD) to ensure realistic harmonic periodicity.

## 5. Training Data Requirements
* **From Scratch:** 10–24 hours of high-quality, single-speaker studio recordings.
* **Fine-Tuning / Transfer Learning:** 15–30 minutes of target speaker data.
* **Few-Shot / Zero-Shot:** < 8 minutes to 3 seconds, but heavily reliant on the base model's pre-trained phonological knowledge.

## 6. Kawi-Specific Constraints
Kawi is a historical language with no native speakers. No historical recordings exist.
Any end-to-end neural system (text-to-waveform) will attempt to guess pronunciation based on its multilingual training data (e.g., modern Indonesian or English), creating indefensible, hallucinated pronunciations that violate project constraints.

## 7. Candidate Data Strategies
* **Human Scholar Recording:** 15-30 minutes of a scholar reading Kawi. Highly defensible, but introduces modern speaker bias and is hard to achieve on a zero budget.
* **Indonesian Base + Kawi Phonemes (Cross-Lingual Transfer):** Use an Indonesian CC0/MIT model and map Kawi phonemes to its acoustic space. Highly feasible, but introduces gaps for unique Kawi phonemes (e.g., retroflex stops).
* **Zero-Shot Prompting (XTTS):** Feed 3 seconds of audio to a prompt model. Fails project guidelines due to unpredictable phonetic hallucination.

## 8. Candidate Neural Architectures
* **VITS / Piper TTS:** Piper is explicitly designed to accept `espeak-ng` phonemes as input. Because the current Kawi architecture already maps to eSpeak, integrating Piper as the neural backend provides the path of least resistance. It supports custom integer-mapped phoneme vocabularies.

## 9. Engineering Integration Strategy
The architecture must remain conceptually:
`Kawi Text -> Deterministic Linguistic Frontend -> Canonical Phonemes/IPA -> Neural Acoustic Model -> Neural Vocoder -> Waveform`
The frontend remains the absolute source of truth. The neural backend must only ingest the deterministic phoneme sequences, removing its ability to "guess" grapheme-to-phoneme rules.

## 10. Compute Requirements
* **Training/Fine-tuning:** Requires a consumer GPU (RTX 3060/4090, 8GB+ VRAM) for 12-48 hours. Can be done via cheap cloud rental if needed.
* **Inference (Deployment):** Highly feasible on CPU-only. Exporting to ONNX yields a 15–50MB model capable of >3x real-time generation on basic consumer hardware.

## 11. Licensing / Provenance
* **Datasets:** Mozilla Common Voice (Indonesian) is CC0-1.0. FLEURS is CC-BY 4.0.
* **Models:** Edge models like Piper/VITS are typically MIT/Apache 2.0. We must strictly avoid base models with restrictive commercial licenses (e.g., Coqui CPML).

## 12. Naturalness Failure Modes
**Why does eSpeak sound robotic while modern neural TTS can sound natural?**
* **eSpeak:** Explicitly controls duration, F0, and phoneme transitions using parametric math. It lacks stochastic micro-variance, resulting in rigid rhythm and metallic periodicity.
* **Modern Neural:** Learns coarticulation implicitly, uses generative adversarial networks to reconstruct organic harmonic noise, and models prosody as a varying distribution.
* **What Kawi Controls:** Kawi-TTS currently controls exact phoneme sequences, explicit duration, and macro-prosody (via eSpeak rules). It completely lacks learned coarticulation and high-frequency texture generation.

## 13. Future Architecture
`Text -> Normalization -> Deterministic G2P -> Canonical Representation -> Profile Strategy -> Piper/VITS ONNX Backend -> Audio`

## 14. Staged Roadmap
* **STAGE 0:** Current deterministic Kawi-TTS + eSpeak baseline (Completed v1.1.0).
* **STAGE 1:** Naturalness research / acoustic experimentation (Current Phase).
* **STAGE 2:** Small neural prototype. (Fine-tune a Piper Indonesian base using 15 mins of scholar audio).
* **STAGE 3:** Higher-quality natural synthesis. (Refine cross-lingual IPA mappings for missing retroflexes).
* **STAGE 4:** Potential production neural backend.

## 15. Risk Analysis
* **Technical Risk:** Securing high-SNR, consistent scholar recordings on a zero budget.
* **Linguistic Risk:** The neural model overriding reconstructed phonology to "smooth" audio based on its Indonesian/Javanese pre-training base.

## 16. Open Research Questions
* How can we forcefully teach a pre-trained Indonesian model to properly articulate Old Javanese retroflex stops and aspirated consonants without thousands of hours of native audio?

## 17. Final Recommendation
Neural TTS is an excellent long-term goal, provided the deterministic frontend isolates the linguistic truth from the acoustic renderer. However, proceeding requires either high-quality scholar recordings or heavily verified cross-lingual IPA mappings.

## 18. References
* FastSpeech 2 (Ren et al., 2020)
* VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech (Kim et al., 2021)
* StyleTTS 2: Towards Human-Level Text-to-Speech through Style Diffusion (Li et al., 2023)
* Piper TTS Documentation
* Mozilla Common Voice / FLEURS Datasets

==================================================
NEURAL TTS STATUS:

B. TECHNICALLY FEASIBLE BUT DATA / LINGUISTIC CONDITIONS ARE NOT YET SATISFIED
==================================================
