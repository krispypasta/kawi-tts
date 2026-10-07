# System Architecture: Kawi-TTS

## 1. High-Level Architectural Flow

```text
[ Raw Romanized Kawi Text ]
            │
            ▼
┌─────────────────────────┐
│ 1. Text Normalization   │  (Unicode NFC/NFD, diacritic standardization,
│    (src/normalization)  │   punctuation cleanup, sandhi/hyphen handling)
└───────────┬─────────────┘
            │ Clean Normalized Text
            ▼
┌─────────────────────────┐
│ 2. G2P Engine           │  (Syllabification, grapheme-to-phoneme rules,
│    (src/g2p)            │   stress assignment, IPA / phoneme tokenization)
└───────────┬─────────────┘
            │ Phoneme / Token Stream + Prosodic Annotations
            ▼
┌─────────────────────────┐
│ 3. Acoustic Modeling    │  (Abstract TTS interface: receives phoneme stream,
│    (src/tts)            │   outputs mel-spectrogram / latent acoustic frame)
└───────────┬─────────────┘
            │ Acoustic Features
            ▼
┌─────────────────────────┐
│ 4. Neural Vocoder       │  (Converts acoustic features to 24kHz/48kHz audio)
└───────────┬─────────────┘
            │
            ▼
     [ Audio Output ]
```

## 2. Component Decoupling & Interfaces

### 2.1 Text Normalization (`src/normalization/`)
- Pure functional transforms.
- Converts input text into a deterministic, canonical character representation.
- Independent of audio or phonetics.

### 2.2 Grapheme-to-Phoneme (`src/g2p/`)
- Maps normalized character sequences to phonetic representations (IPA or internal phoneme tokens).
- Encapsulates rule-based dictionaries, loanword overrides, and syllabification logic.
- Must be fully verifiable without loading deep learning runtimes.

### 2.3 Dataset Processing & Manifests (`data/`, `src/`)
- Manifest generator transforms audio paired with transcripts into verified training records:
  ```json
  {
    "id": "kawi_0001",
    "audio_filepath": "data/processed/kawi_0001.wav",
    "raw_text": "om awighnam astu namo siddham",
    "normalized_text": "om awighnam astu namo siddham",
    "phonemes": "oːm a.wiɡ.nam as.tu na.moː sid.dʰam",
    "duration_sec": 3.42,
    "sample_rate": 24000,
    "speaker_id": "spk_01"
  }
  ```

### 2.4 TTS Modeling Abstraction (`src/tts/`)
- Defines abstract base classes for acoustic synthesis and vocoding.
- Avoids locking the repository to any single machine-learning backend during early research phases.
