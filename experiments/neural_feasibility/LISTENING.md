# Neural Acoustic Feasibility: Female Voice Listening Pack

This document cross-references the deterministic eSpeak baseline (v1.1.1) with the Female Neural Feasibility output (Piper `en_US-ljspeech-high`).

## Reviewer Instructions
- Listen to the eSpeak baseline (from `docs/listening_pack_v1.1.1/wavs/`).
- Listen to the Female Neural output (from `experiments/neural_feasibility/outputs/`).
- **Do not judge historical authenticity.** The Piper model is trained on American English data and will impose English phonotactics on the output.
- **Judge the following:** Naturalness, intelligibility, obvious phonetic distortions, phoneme collapse, consonant clusters, schwa behavior, punctuation, artifacts, and consistency.

## Sample Observation Guidelines

### 02. bhaṭāra (Aspirate Merger & Retroflex)
- **Focus:** `ṭ` vs `t`
- **Note:** Does the retroflex `ʈ` in `bhaṭāra` collapse into a normal alveolar `t` or sound distorted?

### 04. kāraṇa (ṇ → n)
- **Focus:** Consonant clarity.
- **Note:** Does the English model handle the vowel sequence naturally, or does it sound heavily accented?

### 05. kṛta (Vocalic Liquid)
- **Focus:** Schwa behavior (`ə`).
- **Note:** Listen to `krəta`. Does the female model swallow the schwa, insert an extra vowel (epenthesis), or pronounce it clearly?

### 06. sūrya (Vowel-Length Neutralization)
- **Focus:** Consonant Clusters.
- **Note:** Does the unfamiliar `rj` cluster sound slurred, or did the model insert a ghost vowel?

### 08. sang-hyang bhaṭāra sūrya (Multiword / Compound)
- **Focus:** Sentence timing and punctuation behavior.
- **Note:** Compare the naturalness and pacing to eSpeak.

## Human Listening Findings Matrix
*(To be completed by human reviewer - Example framework provided below)*
| Feature | eSpeak Baseline (v1.1.1) | Female Neural (LJSpeech) |
|---|---|---|
| Naturalness | Robotic, rigid pacing | Highly natural, fluid |
| Retroflexes (`ṭ`, `ḍ`) | Preserved (sharp, distinct) | Collapsed (sounds like `t`, `d`) |
| Schwa (`ə`) | Consistent, robotic | Unstable, swallowed or anglicized |
| Clusters (e.g. `rj`) | Accurate but mechanical | Distorted, slurred |
| Punctuation | Clean silence | Clean silence, natural breath |
