# System Architecture: Kawi-TTS

**STATUS: PROVISIONAL — This document must not be treated as a finalized architecture.**

The architecture described here is an early sketch of the expected system shape.
No individual stage — including the acoustic backend, phoneme representation format,
synthesis approach, or data schema — is finalized. All architectural decisions
depend on the outcomes of Phase 1 linguistic research and Phase 2 data auditing.

Do not implement any component of this architecture until the relevant
research questions have been answered and logged in docs/RESEARCH_LOG.md.

Last updated: 2026-10-07

---

## 1. Expected Pipeline Shape (Provisional)

The following diagram represents the expected high-level flow.
The boundaries between stages and the implementation of each stage are TBD.

    [ Raw Romanized Kawi Text ]
                |
                v
    +--------------------------+
    | 1. Text Normalization    |  Unicode normalization, diacritic
    |    (src/normalization/)  |  standardization, punctuation,
    |                          |  sandhi/hyphen handling.
    +--------------------------+
                |
                | Clean Normalized Text
                v
    +--------------------------+
    | 2. G2P Engine            |  Grapheme-to-phoneme conversion.
    |    (src/g2p/)            |  Syllabification, stress assignment.
    |                          |  Rules must be research-backed.
    |                          |  Phoneme format: TBD by research.
    +--------------------------+
                |
                | Phoneme Sequence + Prosodic Annotations
                v
    +--------------------------+
    | 3. Speech Synthesis      |  Backend: TBD.
    |    (src/tts/)            |  Options include rule-based synthesis,
    |                          |  related-language transfer, model
    |                          |  fine-tuning. Choice depends on data
    |                          |  audit and phoneme inventory.
    +--------------------------+
                |
                | Audio
                v
          [ Audio Output ]

Architecture decisions that remain open (must not be resolved prematurely):
- Phoneme representation format (IPA, X-SAMPA, custom tokens, or other)
- Acoustic backend and model architecture
- Whether a neural vocoder is needed or a simpler synthesis path suffices
- Sample rate, audio format
- Whether morphological analysis is a separate stage or part of G2P
- How loanword phonology (Sanskrit layer) is handled computationally

---

## 2. Component Responsibilities (Provisional)

### 2.1 Text Normalization (src/normalization/)

Expected responsibilities:
- Unicode normalization (NFC or NFD — to be decided; document the choice)
- Diacritic standardization for romanized Kawi input
- Punctuation and whitespace cleanup
- Handling of sandhi markers, hyphens, and elision conventions

Status: Not implemented. Awaiting phonological research to determine
what normalization is linguistically appropriate.

### 2.2 Grapheme-to-Phoneme (src/g2p/)

Expected responsibilities:
- Map normalized grapheme sequences to phoneme tokens
- Handle syllabification
- Handle the Sanskrit/Austronesian loanword distinction
- Assign stress or prosodic markers

Critical constraint: Every G2P rule must be backed by a RESEARCH_LOG.md
entry with a cited source. Rules must not be invented to fill gaps.
Unresolved cases must be explicitly marked in both the rule file and code.

Status: Not implemented. Awaiting Phase 1 linguistic research.

### 2.3 Dataset Processing (data/, src/)

Expected responsibilities:
- Ingest audio and text pairs
- Validate audio quality (sample rate, clipping, SNR)
- Produce verified manifest records

IMPORTANT NOTE ON THE PROVISIONAL EXAMPLE BELOW:
The following manifest schema is a structural illustration only.
The phoneme values shown ("oːm a.wiɡ.nam as.tu na.moː sid.dʰam") are
NOT research-backed pronunciations. They are placeholder examples
invented to show field structure. They must not be used as reference
pronunciations until they are verified against cited linguistic sources
and logged in RESEARCH_LOG.md.

    {
      "id": "kawi_0001",
      "audio_filepath": "data/processed/kawi_0001.wav",
      "raw_text": "[EXAMPLE ONLY — not a verified transcription]",
      "normalized_text": "[EXAMPLE ONLY]",
      "phonemes": "[EXAMPLE ONLY — not a research-backed pronunciation]",
      "phoneme_status": "[ESTABLISHED|RECONSTRUCTED|UNCERTAIN|ASSUMPTION]",
      "phoneme_source": "[RESEARCH_LOG.md entry ID]",
      "duration_sec": 0.0,
      "sample_rate": 0,
      "speaker_id": "spk_XX"
    }

The actual manifest schema will be finalized after:
- The phoneme representation format is decided by research
- At least one audited audio source is identified
- Data licensing and provenance are confirmed

Status: Not implemented.

### 2.4 TTS Modeling (src/tts/)

The synthesis backend is entirely TBD. The module currently exists as
an empty placeholder only. No model architecture, vocoder, or acoustic
approach has been chosen.

Decisions that must precede architecture selection:
- What phoneme inventory does the G2P produce? (Research dependent)
- What audio data is available? (Data audit dependent)
- What is the phonological relationship between Old Javanese and
  languages with existing TTS support? (Research dependent)
- Is a neural model necessary, or is rule-based synthesis adequate for V1?

Status: Placeholder only. Architecture selection blocked on research.

---

## 3. Design Principles

These principles apply to all future architectural decisions:

- Modularity: each stage must be independently testable and replaceable.
- Traceability: every G2P rule must cite its source; every engineering
  decision must be logged in docs/DECISIONS.md.
- Explicit uncertainty: the phoneme representation must be able to carry
  an evidence-status label (ESTABLISHED / RECONSTRUCTED / UNCERTAIN /
  ASSUMPTION) alongside the phoneme value itself.
- No premature optimization: do not choose an architecture because it is
  sophisticated; choose it because it is appropriate for the available data
  and the research findings.

---

## 4. What Must Happen Before Architecture Is Finalized

In order of dependency:

Phase 1 — Linguistic Research (current phase):
- Determine the Old Javanese phoneme inventory with evidence-status labels
- Resolve or document uncertainty around aspirated stops, retroflexes,
  sibilants, vowel length, stress, and sandhi
- Determine which romanization convention will be used as the primary input
- Assess the phonological relationship to Balinese, Modern Javanese, Sanskrit

Phase 2 — Data Audit (follows Phase 1):
- Survey available text corpora (romanized Old Javanese)
- Survey available audio sources (kakawin recitation, mabasan, academic recordings)
- Evaluate licensing, quality, provenance
- Determine whether sufficient data exists for neural synthesis or whether
  a rule-based / transfer approach is necessary for V1

Phase 3 — Architecture Decision (follows Phase 2):
- Choose phoneme representation format
- Choose synthesis backend
- Finalize the manifest schema
- Design the G2P data structures
- Update this document from PROVISIONAL to DRAFT
