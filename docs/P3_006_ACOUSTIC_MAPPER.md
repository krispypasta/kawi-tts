# P3-006: Acoustic Mapper & eSpeak-ng Prototype Backend

**Date:** 2026-10-07
**Mode:** Engineer/Builder
**Target:** Profile A (Reconstructed Historical Spoken Old Javanese Prototype)

## 1. Purpose

This document details the implementation of the Acoustic Mapper (`src/acoustic/mapper.py`) and the eSpeak-ng prototype backend (`src/acoustic/espeak_backend.py`), fulfilling task P3-006.

The primary objective of this milestone is to establish the **first executable, end-to-end synthesis pipeline** for Kawi-TTS:
```
Kawi Text (raw)
   ↓ [src/normalization/normalizer.py]
Normalized Text (Unicode NFC, typographic cleanup)
   ↓ [src/normalization/tokenizer.py]
Structured Tokens (words, punctuation, explicit boundaries)
   ↓ [src/g2p/engine.py]
Internal Phonemes (100% lossless phonological representation)
   ↓ [src/acoustic/mapper.py]
Acoustic Representation (eSpeak-compatible IPA, provisional audit)
   ↓ [src/acoustic/espeak_backend.py]
eSpeak-ng Synthesis (CLI invocation or dry-run mock)
   ↓
Audio Output (WAV)
```

**CRITICAL PRINCIPLE:**
The Acoustic Mapper is the **only layer permitted to perform provisional backend adaptations**. The upstream normalization, tokenization, and G2P layers remain completely decoupled and lossless.

---

## 2. Interface

### 2.1 Acoustic Mapper API (`src/acoustic/mapper.py`)

```python
from src.acoustic.mapper import AcousticMapper, MappingStatus, MappedToken, AcousticMappingResult

mapper = AcousticMapper(profile="A")
result = mapper.map_phonemes(phoneme_words)
```

**Output Data Structure (`AcousticMappingResult`):**
- `original_phonemes`: `List[List[str]]` (verbatim G2P input, completely unmutated).
- `mapped_words`: `List[List[MappedToken]]` (each token classified with status and audit notes).
- `backend_phoneme_string`: `str` (space-separated, eSpeak-ready IPA string).
- `provisional_mappings`: `List[MappedToken]` (convenience list of all provisionally adapted tokens).
- `unsupported_tokens`: `List[MappedToken]` (tokens rejected or unsupported by the mapper).

### 2.2 eSpeak-ng Backend API (`src/acoustic/espeak_backend.py`)

```python
from src.acoustic.espeak_backend import ESpeakBackend, SynthesisResult

backend = ESpeakBackend(voice="jv")  # Default Javanese voice
res = backend.synthesize(phoneme_str, output_path="out.wav", dry_run=True)
```

- When `dry_run=True`: Constructs command deterministically without invoking subprocesses; optionally creates valid 44-byte WAV headers if `create_dummy_wav=True`.
- When `dry_run=False`: Invokes local `espeak-ng` binary via subprocess. If not found on `PATH`, raises `ESpeakNotFoundError` with clear installation guidance.

### 2.3 End-to-End Pipeline API (`src/acoustic/pipeline.py` & `src/tts`)

```python
from src.tts import synthesize

pipeline_res = synthesize(
    "om awighnam astu",
    profile="A",
    output_path="test.wav",
    dry_run=True,
)
```

Returns `PipelineResult` tracking intermediate outputs across all five pipeline stages.

---

## 3. Internal G2P → Acoustic Representation Flow

The mapper operates word-by-word and phoneme-by-phoneme:
1. G2P internal phoneme tokens are looked up in the mapping tables.
2. Direct phonetic equivalents are assigned `MappingStatus.PRESERVED`.
3. Categories with historical uncertainty or requiring eSpeak phoneme adaptation are assigned `MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING` with explicit diagnostic notes.
4. Unrecognized characters are tagged `MappingStatus.UNSUPPORTED`.
5. Words are joined by spaces to form an eSpeak phoneme string formatted within `[[...]]`.

---

## 4. Provisional Mappings Implemented

Every provisional mapping is explicitly documented and tracked at runtime:

| Internal Token | Mapped IPA | Mapping Status | Note / Epistemic Rationale |
| :--- | :--- | :--- | :--- |
| `bʱ` | `bʱ` | `PROVISIONAL_ACOUSTIC_MAPPING` | Voiced bilabial aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004, DEC-006). |
| `dʱ` | `dʱ` | `PROVISIONAL_ACOUSTIC_MAPPING` | Voiced dental/alveolar aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004). |
| `gʱ` | `gʱ` | `PROVISIONAL_ACOUSTIC_MAPPING` | Voiced velar aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004). |
| `ɟʱ` | `ɟʱ` | `PROVISIONAL_ACOUSTIC_MAPPING` | Voiced palatal aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004). |
| `ḍʱ` | `ḍʱ` | `PROVISIONAL_ACOUSTIC_MAPPING` | Voiced retroflex aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004). |
| `r̩` | `r̩` | `PROVISIONAL_ACOUSTIC_MAPPING` | Syllabic rhotic liquid for eSpeak-ng; historical phonetic realization remains uncertain (P3-003A). |
| `l̩` | `l̩` | `PROVISIONAL_ACOUSTIC_MAPPING` | Syllabic lateral liquid for eSpeak-ng; historical phonetic realization remains uncertain (P3-003A). |
| `r̩ː` | `r̩ː` | `PROVISIONAL_ACOUSTIC_MAPPING` | Long syllabic rhotic liquid for eSpeak-ng. |
| `l̩ː` | `l̩ː` | `PROVISIONAL_ACOUSTIC_MAPPING` | Long syllabic lateral liquid for eSpeak-ng. |
| `əː` | `əː` | `PROVISIONAL_ACOUSTIC_MAPPING` | Lengthened mid-central schwa (ö) for eSpeak-ng; phonetic status cross-linguistically rare and historically uncertain. |

---

## 5. Information-Loss Accounting

* **Zero Information Loss in Front-End:** G2P produces all phonemes losslessly.
* **Preserved Categories in eSpeak-ng IPA:**
  - Native short vowels: `a`, `i`, `u`, `e`, `o`, `ə` (`PRESERVED`).
  - Vowel length chronemes: `aː`, `iː`, `uː` (`PRESERVED`).
  - Retroflex vs dental contrast: `ʈ` (ṭ), `ɖ` (ḍ), `ɳ` (ṇ) vs `t`, `d`, `n` (`PRESERVED`).
  - Sibilants: `ʃ` (ś), `ʂ` (ṣ), `s` (s) (`PRESERVED`).
  - Voiceless aspirates: `tʰ`, `pʰ`, `kʰ`, `cʰ`, `ʈʰ` (`PRESERVED`).
* **Collapsing:** **None.** No categories are collapsed into plain stops or short vowels at this stage.

---

## 6. eSpeak-ng Integration & Installation Requirements

In this development environment, `espeak-ng` was detected as not currently present on `PATH`.
The codebase is designed so that the absence of eSpeak-ng **does not break testing or pipeline execution**:
- Tests use `dry_run=True`, verifying command line formatting and 44-byte WAV generation without external dependencies.
- Non-dry-run synthesis raises a helpful `ESpeakNotFoundError`.

### Installation Instructions for Real Audio Synthesis:
1. **Windows (using winget):**
   ```cmd
   winget install eSpeak-ng.eSpeak-ng
   ```
   Or download the official installer from [eSpeak-ng GitHub Releases](https://github.com/espeak-ng/espeak-ng/releases).
2. **Linux (Debian / Ubuntu):**
   ```bash
   sudo apt-get install espeak-ng
   ```
3. **macOS (via Homebrew):**
   ```bash
   brew install espeak-ng
   ```

---

## 7. Known Limitations

1. **Voice Quality:** eSpeak-ng is a formant synthesizer. Its vocal output sounds mechanical and robotic; it does not aim for human-like realism.
2. **Language Voice Availability:** The default voice is set to `jv` (Javanese) with fallback to `id` (Indonesian). If specific Indic phonemes (e.g. breathy voice `bʱ`) are unsupported by the host eSpeak Javanese voice table, eSpeak may fall back to approximated phoneme sounds.
3. **Tone / Prosody:** At this prototype stage, sentence-level intonation is flat/default; Old Javanese metrical scansion or pitch contour is not yet modeled.

---

## 8. Why This Prototype Does NOT Establish Historical Pronunciation

- Historical Old Javanese has no native recordings.
- The acoustic representations mapped in this module (`bʱ`, `ʈ`, `ʃ`, etc.) represent scholarly reconstructions and transliterational categories, not empirically verified 9th-century phonetics.
- The audio generated by eSpeak-ng is an **engineering validation prototype** demonstrating that the symbolic pipeline works end-to-end without data loss. It must not be cited as evidence of how Old Javanese sounded.

---

## 9. Future Replacement Path for Neural Acoustic Backend

When moving beyond the eSpeak-ng prototype (e.g. in later Phase 3/4 milestones):
1. The `AcousticMapper` interface remains the boundary between linguistic G2P and synthesis.
2. A new `NeuralBackend` (e.g., Piper ONNX or VITS fine-tuned on OpenSLR 41 Modern Javanese) can be plugged in alongside `ESpeakBackend`.
3. If the neural backend lacks support for Sanskrit aspirates or vowel length, a profile-specific mapping rule (with Abraham's explicit approval) can be enacted inside `AcousticMapper` without modifying a single line of G2P code.
