# Project State: Kawi-TTS

**Last updated:** 2026-10-07
**Current phase:** Phase 4 — V1 (Integration & Evaluation)
**Repository branch:** main

This file is the authoritative summary of the project's current state.
Update it at the start and end of every significant work session.

---

## Current Phase: Phase 4 — V1 Integration & Evaluation

### What Phase 4 means

With Phase 3 complete (Normalization, Tokenization, Lossless G2P, Acoustic Mapping, and Synthesis Pipeline implemented and validated on 26 authentic Old Javanese source citations across 13 linguistic categories), Phase 4 focuses on:
- End-to-end integration testing and user-facing CLI/API.
- Comprehensive G2P evaluation against larger lexicons (e.g. OJW).
- Traceable documentation connecting every synthesized utterance to research log entries.
- Production of the final V1 release artifact.

### Phase 4 entry criteria (completed)

Phase 3 is 100% complete:
- Normalization (P3-002) tested and verified.
- G2P (P3-003A/B/C) tested and verified.
- Tokenization & Text Structure (P3-004) tested and verified.
- Acoustic Backend Interface & Mapper (P3-005/P3-006) tested and verified.
- Evidence-based validation (P3-007) verified on 26 source-cited lexical items. 66 automated tests pass.

### What is blocked until Phase 4 is complete

- Final V1 Release tag and public documentation.

---

## Completed Milestones

### Phase 3 — Prototype Pipeline (completed 2026-10-07)

- Completed P3-007: Conducted comprehensive end-to-end evidence-based validation on 26 real Old Javanese source citations across 13 linguistic categories (`docs/P3_007_VALIDATION.md`). Fixed capitalization bug in G2P word parser. 66 unit tests pass.
- Completed P3-006: Implemented Acoustic Mapper (`src/acoustic/mapper.py`), eSpeak-ng backend interface (`src/acoustic/espeak_backend.py`), and end-to-end synthesis pipeline (`src/acoustic/pipeline.py`, re-exported in `src/tts`). Explicitly tracks and stamps all provisional mappings. 52 unit tests pass.
- Completed P3-005: Conducted Acoustic Backend Survey & Decision Gate (`docs/P3_005_ACOUSTIC_BACKEND_SURVEY.md`). Recommended a two-stage hybrid prototype using eSpeak-ng (for lossless acoustic verification) followed by an explicit Acoustic Mapper to a Modern Javanese neural model. Explicitly deferred lossy phonetic mappings.
- Completed P3-004: Implemented deterministic, 100% lossless text-structure / tokenization layer in `src/normalization/tokenizer.py`. Classifies words, punctuation, explicit boundaries (hyphens), elision (apostrophes), line breaks, numbers, and flags unresolved structural ambiguities (such as un-hyphenated ASCII 'sanghyang'). 38 unit tests pass.
- Completed P3-003C: Conducted G2P Validation & Edge-Case Audit. Confirmed information preservation. Documented edge cases (un-normalized ASCII `sanghyang` false aspirates) requiring boundaries in P3-004.
- Completed P3-003B: Implemented rule-based lossless G2P engine in `src/g2p/engine.py` mapping normalized orthography to an internal phonological representation preserving all distinctions.
- Completed P3-003A: Generated Profile A G2P Specification & Decision Matrix (`docs/P3_003A_G2P_SPEC.md`). Defined internal representations and formally deferred lossy acoustic mapper decisions to Abraham.
- Completed P3-002: Implemented deterministic, lossless Unicode and orthographic normalization in `src/normalization/normalizer.py`. Fully preserves all linguistic, vowel length, aspirate, and sibilant distinctions. 15 unit tests covering NFC/NFD composition, diacritics, whitespace, and invariance pass.

### Phase 2 — Data Audit (completed 2026-10-07)

Audit milestone: Audited OJW, GRETIL, and Modern Javanese speech resources (OpenSLR 41, MMS-TTS-JAV). Findings logged as RES-017 through RES-021. Established feasibility of cross-lingual transfer learning for Profile A.

### Phase 1 — Pronunciation Target Definition (completed 2026-10-07)

Documentation milestone: The Researcher completed initial audits of the core phonological inventory (RES-001 through RES-011) and compiled the Pronunciation Inventory & Uncertainty Matrix (P1-013). Based on this evidence, the Manager formally logged DEC-006: V1 targets "Reconstructed Historical Spoken Old Javanese" (Profile A), distinguishing it from Profile B (Scholarly Reading) and Profile C (Balinese Performance).

### Phase 0 — Project Foundation (completed 2026-10-07)

Documentation milestone: established the project's vision, principles, scope,
and working process before any linguistic research or technical implementation.

Files created or substantially rewritten:
- docs/PROJECT_SPEC.md — full project vision, V1 definition, core principles
- docs/ARCHITECTURE.md — provisional architecture with all provisional content
  clearly labeled; removed unverified phoneme example values
- docs/RESEARCH_LOG.md — structured research log with 21 open research questions,
  working hypothesis registry, bibliography, and entry template
- docs/AGENT_ROLES.md — three AI work mode definitions
- docs/DECISIONS.md — engineering decision log (empty, ready for use)
- AGENTS.md — top-level AI guidance for this repository
- PROJECT_STATE.md — this file
- TODO.md — prioritized task list for Phase 1

Key corrections made during Phase 0:
- The existing ARCHITECTURE.md contained an unverified phoneme transcription
  example ("om awighnam astu namo siddham" → IPA). This has been explicitly
  labeled as a structural placeholder, not a linguistic reference. See
  docs/RESEARCH_LOG.md Section 3 for details.
- The existing RESEARCH_LOG.md presented scaffold-level claims as if they were
  established findings. These have been reclassified as ASSUMPTION and registered
  in docs/RESEARCH_LOG.md Section 3 with notes on what research is needed.
- The existing PROJECT_SPEC.md contained architectural conclusions (mel-spectrogram,
  neural vocoder, IPA output) that were written before any research. These have
  been removed or marked provisional.

---

## Blocked / Waiting
 
Nothing is currently blocked. Phase 4 (V1 Integration & Evaluation) is ready to begin.

---

## Active Assumptions

These are ASSUMPTION-labeled claims being used as working project assumptions
pending Phase 1 verification. They are tracked formally in docs/RESEARCH_LOG.md
Section 3.

- ASSUMPTION-003: Zoetmulder (1982) is a primary and reliable orthographic reference.
- ASSUMPTION-004: Romanized Kawi text is the appropriate primary TTS input format.

*(Note: ASSUMPTION-001 and ASSUMPTION-002 have been addressed via RES-002 and RES-003 and are no longer blind assumptions.)*

---

## Three AI Work Modes

This project uses three scoped AI work modes. They are prompting modes within
Hermes, not separate autonomous agents. The repository is the shared source of truth.

See docs/AGENT_ROLES.md for full definitions.

- Researcher/Linguist: investigates linguistic questions; writes to RESEARCH_LOG.md
- Engineer/Builder: implements approved findings; writes to src/ and tests/
- Manager/Reviewer: maintains project state; coordinates roles; updates PROJECT_STATE.md and TODO.md

Current active mode: Manager/Reviewer (Phase 3 Milestone Checkpoint complete; ready for Phase 4)

---

## Repository Structure

    D:/code/Project-TTS-Kawi/
    |
    +-- AGENTS.md               Top-level AI guidance
    +-- PROJECT_STATE.md        This file
    +-- TODO.md                 Prioritized task list
    +-- README.md               Project overview
    |
    +-- docs/
    |   +-- PROJECT_SPEC.md     Vision, scope, V1 definition
    |   +-- ARCHITECTURE.md     Provisional architecture (not finalized)
    |   +-- RESEARCH_LOG.md     Linguistic findings, open questions, bibliography
    |   +-- AGENT_ROLES.md      Three AI work mode definitions
    |   +-- DECISIONS.md        Engineering decision log
    |   +-- P3_003A_G2P_SPEC.md G2P specification & decision matrix
    |   +-- P3_005_ACOUSTIC_BACKEND_SURVEY.md Acoustic backend survey
    |   +-- P3_006_ACOUSTIC_MAPPER.md Acoustic mapper & eSpeak backend spec
    |   +-- P3_007_VALIDATION.md Evidence-based validation report
    |
    +-- src/
    |   +-- normalization/      Unicode normalization & text tokenization
    |   +-- g2p/                Lossless grapheme-to-phoneme engine
    |   +-- acoustic/           Acoustic mapper & eSpeak-ng backend
    |   +-- tts/                High-level synthesis API
    |
    +-- data/                   Data directory
    +-- tests/                  Test suite (66 tests passing)
    +-- experiments/            Experiments directory
    +-- notebooks/              Research notebooks (empty)
