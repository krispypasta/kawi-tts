# Kawi-TTS

A research-first Text-to-Speech (TTS) system for Old Javanese (*Basa Kawi*).

---

## 1. Project Overview & Motivation

Old Javanese (*Basa Kawi*) is an Austronesian classical language with an extensive literary and epigraphic heritage spanning more than six centuries (c. 800–1500 CE). Kawi-TTS is an academic and cultural engineering initiative aimed at making Old Javanese texts and inscriptions accessible through speech technology, while strictly prioritizing linguistic defensibility over synthetic voice naturalness.

### V1 Target: Profile A — Reconstructed Historical Spoken Old Javanese

The primary objective for V1 is:
**Profile A: Reconstructed Historical Spoken Old Javanese**.

### Epistemic Policy & Boundaries
- **No known surviving recordings from the historical period are currently available to establish historical pronunciation directly.**
- The pronunciation synthesized by Kawi-TTS is an **evidence-grounded historical reconstruction**, NOT a claim of historically proven certainty.
- The project distinguishes attested comparative evidence from scholarly reconstruction and practical engineering assumptions.
- Uncertain linguistic distinctions (e.g., Sanskrit aspirates, historical vowel duration, and sibilant realizations) are **preserved losslessly in internal representations** rather than prematurely merged or discarded.
- No claim of production-quality speech or historical perfection is made.

---

## 2. Current Architecture & Pipeline

Kawi-TTS implements a decoupled, five-stage modular pipeline:

```
Kawi Text (raw input)
   ↓
1. Unicode & Orthographic Normalization (src/normalization/normalizer.py)
   Canonical NFC composition, typographic cleanup (ŋ → ṅ, ě → ĕ), elision normalization.
   ↓
2. Text Structure & Tokenization (src/normalization/tokenizer.py)
   Deterministic segmentation into words, punctuation, line breaks, and explicit boundary markers.
   Flags unresolved structural sequences (e.g. unsegmented ASCII 'ngh') without guessing.
   ↓
3. Lossless Grapheme-to-Phoneme Engine (src/g2p/engine.py)
   Greedy parsing of normalized orthography into an immutable internal phonological representation.
   Maintains all vowel length, aspirate, sibilant, retroflex, and vocalic liquid distinctions.
   ↓
4. Explicit Acoustic Mapper (src/acoustic/mapper.py)
   Maps internal phonemes to backend-specific representations (eSpeak-ng IPA).
   Labels and audits provisional adaptations (PROVISIONAL_ACOUSTIC_MAPPING).
   ↓
5. Acoustic Synthesis Backend (src/acoustic/espeak_backend.py)
   eSpeak-ng phoneme synthesis interface with full dry-run/mock execution and WAV output.
   ↓
Audio Output (WAV)
```

---

## 3. Project Status & Roadmap

The project follows a strict phase-gate progression:

* **[x] Phase 0 — Project Foundation:** Architecture specifications, governance policies, and engineering decision log established.
* **[x] Phase 1 — Linguistic Research:** Core phoneme inventory, vowel length, pepet, retroflexes, aspirates, and oral recitation traditions audited (RES-001 through RES-016). Formal decision DEC-006 adopted.
* **[x] Phase 2 — Data Audit:** Old Javanese Wordnet (OJW), GRETIL corpora, and Modern Javanese speech datasets (OpenSLR 41, MMS) audited for compatibility and licensing (RES-017 through RES-021).
* **[x] Phase 3 — Prototype Pipeline:**
  * Normalization (`src/normalization/normalizer.py`) implemented and tested.
  * Tokenizer (`src/normalization/tokenizer.py`) implemented and tested.
  * Lossless G2P engine (`src/g2p/engine.py`) implemented and audited.
  * Acoustic Mapper & eSpeak-ng backend interface (`src/acoustic/`) implemented.
  * Comprehensive validation audit (`docs/P3_007_VALIDATION.md`) executed on 26 authentic Old Javanese source citations across 13 linguistic categories.
* **[x] Phase 4 — V1 Integration & Evaluation (COMPLETED):**
  * End-to-end integration and user-facing CLI/API.
  * High-throughput G2P evaluation against the full OJW lexicon.
  * Public release documentation and source traceability.

---

## 4. Current Acoustic Backend & Environment Note

- **Current Prototype Backend:** Formant synthesis interface via **eSpeak-ng** using IPA input notation.
- **Host Installation Status:** `espeak-ng` (v1.52.0) is installed. The pipeline targets the `jv` (Javanese) voice but successfully falls back to `id` (Indonesian) to generate end-to-end audio. Dry-run mode is also supported for headless environments.
- **Real Audio Generation:** To synthesize audible sound, install `espeak-ng` locally (e.g., `winget install eSpeak-ng.eSpeak-ng` on Windows or `sudo apt-get install espeak-ng` on Ubuntu/Debian). The backend automatically discovers the executable in PATH without code modifications.
- **Neural TTS Status:** No neural model has been trained or fine-tuned. Cross-lingual neural transfer is planned for subsequent milestones.

---

## 5. Repository Structure

```text
Project-TTS-Kawi/
├── README.md                           # This document
├── LICENSE                             # MIT License
├── .gitignore                          # Python / build / artifact exclusions
├── PROJECT_STATE.md                    # Authoritative live project state
├── TODO.md                             # Phase-tracked actionable task list
├── AGENTS.md                           # Core guidance for AI contributors
│
├── docs/
│   ├── PROJECT_SPEC.md                 # Project vision, principles, and scope
│   ├── ARCHITECTURE.md                 # System architecture specification
│   ├── RESEARCH_LOG.md                 # Linguistic findings (RES-001 to RES-021)
│   ├── DECISIONS.md                    # Engineering decision log (DEC-001 to DEC-006)
│   ├── AGENT_ROLES.md                  # Three AI work mode definitions
│   ├── P3_003A_G2P_SPEC.md             # Profile A G2P specification
│   ├── P3_005_ACOUSTIC_BACKEND_SURVEY.md# Acoustic backend survey & decision gate
│   ├── P3_006_ACOUSTIC_MAPPER.md       # Acoustic mapper and eSpeak backend spec
│   └── P3_007_VALIDATION.md            # Evidence-based validation report
│
├── src/
│   ├── normalization/                  # Normalization & tokenization
│   │   ├── normalizer.py               # Lossless Unicode NFC canonicalizer
│   │   └── tokenizer.py                # Deterministic text-structure layer
│   ├── g2p/                            # Grapheme-to-Phoneme engine
│   │   └── engine.py                   # Lossless greedy G2P mapper
│   ├── acoustic/                       # Acoustic mapping & synthesis backend
│   │   ├── mapper.py                   # G2P → eSpeak IPA acoustic mapper
│   │   ├── espeak_backend.py           # eSpeak-ng execution wrapper & mock
│   │   └── pipeline.py                 # End-to-end synthesize() API
│   └── tts/                            # High-level synthesis exports
│
├── tests/                              # Comprehensive test suite (66 tests)
│   ├── test_scaffold.py                # Package import sanity tests
│   ├── test_normalization.py           # Unicode & diacritic composition tests
│   ├── test_tokenizer.py               # Tokenization & boundary tests
│   ├── test_g2p.py                     # Lossless G2P engine tests
│   ├── test_acoustic_mapper.py         # Acoustic mapping & immutability tests
│   ├── test_synthesis_pipeline.py      # Dry-run & pipeline execution tests
│   └── test_validation.py              # Source-cited evidence validation tests
│
└── data/                               # Data directories (raw, processed, manifests)
```

---

## 6. Testing & Verification

Run the entire test suite:

```bash
python -m unittest discover tests
```

Current test status: **66 tests passing (100% pass rate)**.


