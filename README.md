# Kawi-TTS

A research-grade Text-to-Speech (TTS) system focused on the phonology and pronunciation of Old Javanese (Kawi).

## Project Scope & Objectives

The primary objective of this project is to build an accurate, linguistically grounded speech synthesis pipeline for Old Javanese (*Basa Kawi*), with an initial emphasis on spoken language reconstruction and pronunciation rather than script rendering.

Key principles:
- **Linguistics First:** Ground Grapheme-to-Phoneme (G2P) mappings and phonetic inventories in established academic literature (e.g., Zoetmulder, Uhlenbeck, Teeuw, and Comparative Austronesian / Indological phonological research).
- **Separation of Concerns:** Keep text normalization, G2P rule systems, acoustic modeling, dataset curation, and evaluation strictly decoupled.
- **Evidence-Based Reconstruction:** Clearly distinguish attested historical/comparative linguistic evidence from practical acoustic synthesis assumptions.
- **Data Integrity:** Strict auditing and validation of any audio or textual corpus before inclusion in training pipelines.

## Project Structure

```text
kawi-tts/
├── README.md
├── LICENSE
├── .gitignore
├── PROJECT_STATE.md
├── TODO.md
├── docs/
│   ├── PROJECT_SPEC.md
│   ├── ARCHITECTURE.md
│   └── RESEARCH_LOG.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── manifests/
├── src/
│   ├── normalization/
│   ├── g2p/
│   └── tts/
├── experiments/
└── tests/
```

## Documentation

- [Project Specification](docs/PROJECT_SPEC.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Research Log & Bibliography](docs/RESEARCH_LOG.md)
- [Current Project State](PROJECT_STATE.md)
- [Actionable Tasks (TODO)](TODO.md)

