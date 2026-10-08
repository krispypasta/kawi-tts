# Neural Acoustic Feasibility: Listening Pack

This document cross-references the deterministic eSpeak baseline (v1.1.1) with the Neural Feasibility output (Piper `de_DE-thorsten`).

## Reviewer Instructions
- Listen to the eSpeak baseline (from `docs/listening_pack_v1.1.1/wavs/`).
- Listen to the Piper Neural output (from `experiments/neural_feasibility/outputs/`).
- **Do not judge historical authenticity.** The Piper model is German and will sound like a German speaker reading Kawi phonemes.
- Judge: Intelligibility, synthesis artifacts, and phonetic collapse (can you still hear the retroflex in `bhaṭāra`?).

## Samples

### 01. Ordinary
- **eSpeak:** `docs/listening_pack_v1.1.1/wavs/01_ordinary.wav`
- **Neural:** `experiments/neural_feasibility/outputs/ordinary.wav`
- *Listen for:* Clarity of vowels.

### 02. Aspirate Merger & Retroflex
- **eSpeak:** `docs/listening_pack_v1.1.1/wavs/02_aspirate_merger.wav`
- **Neural:** `experiments/neural_feasibility/outputs/aspirate_merger.wav`
- *Listen for:* Did the retroflex `ʈ` in `bhaṭāra` collapse into a normal `t` in the neural version?

### 05. Vocalic Liquid
- **eSpeak:** `docs/listening_pack_v1.1.1/wavs/05_vocalic_liquid.wav`
- **Neural:** `experiments/neural_feasibility/outputs/vocalic_liquid.wav`
- *Listen for:* Stability of the schwa `ə` in `kṛta` (`krəta`).

### 08. Multiword / Compound
- **eSpeak:** `docs/listening_pack_v1.1.1/wavs/08_multiword.wav`
- **Neural:** `experiments/neural_feasibility/outputs/multiword_compound_structure.wav`
- *Listen for:* Pacing and pauses between words.
