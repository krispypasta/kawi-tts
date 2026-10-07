# Project State: Kawi-TTS

**Last updated:** 2026-10-07
**Current phase:** Phase 7 — Zero-Budget Reassessment & Engine Hardening (Active)
**Repository branch:** main

This file is the authoritative summary of the project's current state.
Update it at the start and end of every significant work session.

---

## Current Phase: Phase 7 — Zero-Budget Reassessment & Engine Hardening

### What Phase 6 accomplished
P6-001 through P6-004 implemented the Profile Strategy layer, isolating canonical representation from acoustic profile rules (Profile A vs B). P6-003R secured the vowel-length unresolved fallback. P6-004 evaluated the feasibility of an etymological metadata classifier, concluding it is currently BLOCKED by insufficient dataset provenance.

### Phase 7 Entry Criteria
Phase 6 implementation is stable and all tests pass (94/94). The project requires a path toward a better acoustic backend (e.g., Piper/VITS) without sacrificing explicit Profile A control.

### Phase 7 Active (Scope Reset)
- **FRANKENSTEIN STOP APPLIED**: The project operates on a strictly $0 budget. Neural TTS and paid expert corpora are now DEFERRED / OPTIONAL. 
- Completed P7-001 & P7-002A: Corpus design and existing audio audits proved a paid/commissioned expert speaker is required. 
- Completed P7-003: Zero-Budget Scope Reassessment (`docs/P7_003_ZERO_BUDGET_SCOPE_REASSESSMENT.md`). Reoriented project to focus on the core "Kawi Pronunciation & Reconstruction Engine" leveraging local, zero-cost eSpeak synthesis.
- Pending P7-B: Linguistic and pronunciation-engine hardening.

---

## Completed Milestones

### Phase 6 — V2 Profile Implementation (Completed)

- Completed P6-001: Implemented `ProfileStrategy` abstraction layer.
- Completed P6-002: Validated Profile A vs Profile B execution matrix. Applied P5-002A correction to strictly align aspirate rules with historical evidence.
- Completed P6-003R: Established Vowel Length Strategy. Explicitly stripped duration markers in Profile A as an engineering fallback to preserve `UNRESOLVED` status acoustically.
- Completed P6-004: Lexical Metadata Feasibility Audit. Concluded etymological classification is impossible with current Wordnet data, formally blocking P6-005.

### Phase 5 — Post-V1 Research (Completed)
 
 - Completed P5-001: Post-V1 Evidence & Feasibility Audit. Identified the conflation between orthographic reading and historical speech.
 - Completed P5-002: Evidence-Based Acoustic Profile Policy (`docs/P5_002_ACOUSTIC_PROFILE_POLICY.md`). Formalized the separation of Canonical Representation from Acoustic Realization. Authorized Profile A to merge aspirates and sibilants based on historical evidence. Appended mismatch warnings to V1 docs.
 - Completed P5-003: Profile Architecture Design & Vowel Length Strategy (`docs/P5_003_PROFILE_ARCHITECTURE.md`). Designed software layer separating Profile A and Profile B. Determined etymological/metrical vowel length handling.

### Phase 4 — V1 Integration & Evaluation (Completed)

- Completed P4-005: Real eSpeak Integration (`docs/P4_005_ESPEAK_INTEGRATION.md`). Verified executable pipeline, `id` fallback voice selection, and successful generation of representative Kawi matrix without information collapse. 80 automated tests pass.
- Completed P4-006F: Fixed G2P greedy digraph conflict for unhyphenated `sanghyang`. Introduced explicit disambiguation in `src/g2p/engine.py` to prevent false mapping of the ASCII `ngh` sequence to a Sanskrit aspirate (`gʱ`), ensuring canonical tokenization while preserving legitimate Sanskrit `gh` parsing. 85 tests pass.
- Completed P4-006E: Neural Backend Evaluation & Candidate Decision. Formally evaluated the Piper id_ID model against objective measurements and human perceptual reports. The model was rejected as the primary V1 backend due to catastrophic acoustic collapse of non-Indonesian consonants (e.g. `sĕkar` perceived as "saa"). Fine-tuning was also rejected due to unknown dataset licensing and baseline failure. Validated the experimental test harness and confirmed that the canonical pipeline successfully preserved all linguistic data up to the failed backend.
- Completed P4-003: Authored and finalized `docs/PRONUNCIATION_SYSTEM.md` detailing the linguistic rules, sources, and epistemic boundaries of the V1 pipeline.
- Completed P4-002: Executed high-throughput G2P lexical evaluation against all 4,192 unique lexical forms of the Old Javanese Wordnet (`docs/P4_002_OJW_EVALUATION.md`, `data/processed/ojw_coverage_report.json`). Achieved 99.90% full representation coverage with zero runtime crashes or silent information collapse. 79 automated tests pass.
- Completed P4-001: Executed formal end-to-end V1 integration test suite across all 5 decoupled stages (`docs/P4_001_INTEGRATION.md`). Verified input contracts, information preservation invariants, error handling for empty/punctuation/unsupported inputs, and dry-run execution. 76 unit and integration tests pass.

### Phase 3 — Prototype Pipeline (completed 2026-10-07)

- Completed P3-007: Conducted comprehensive end-to-end evidence-based validation on 26 real Old Javanese source citations across 13 linguistic categories (`docs/P3_007_VALIDATION.md`). Fixed capitalization bug in G2P word parser. 66 unit tests pass.
- Completed P3-006: Implemented Acoustic Mapper (`src/acoustic/mapper.py`), eSpeak-ng backend interface (`src/acoustic/espeak_backend.py`), and end-to-end synthesis pipeline (`src/acoustic/pipeline.py`, re-exported in `src/tts`). Explicitly tracks and stamps all provisional mappings. 52 unit tests pass.
- Completed P3-005: Conducted Acoustic Backend Survey & Decision Gate (`docs/P3_005_ACOUSTIC_BACKEND_SURVEY.md`). Recommended a two-stage hybrid prototype using eSpeak-ng (for lossless structural/pipeline verification) followed by an explicit Acoustic Mapper to a Modern Javanese neural model. Explicitly deferred lossy phonetic mappings.
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

- **Neural TTS & Custom Corpora**: Explicitly BLOCKED/DEFERRED by the zero-budget constraint.
- **P6-005**: Etymological Metadata Implementation is explicitly BLOCKED until an etymologically tagged dictionary dataset is obtained or created.

---

## Active Assumptions

*(All initial Phase 0 blind assumptions have been addressed via formal linguistic research findings or engineering decisions. See `docs/RESEARCH_LOG.md` and `docs/DECISIONS.md` for the established sources.)*

---

## Three AI Work Modes

This project uses three scoped AI work modes. They are prompting modes within
Hermes, not separate autonomous agents. The repository is the shared source of truth.

See docs/AGENT_ROLES.md for full definitions.

- Researcher/Linguist: investigates linguistic questions; writes to RESEARCH_LOG.md
- Engineer/Builder: implements approved findings; writes to src/ and tests/
- Manager/Reviewer: maintains project state; coordinates roles; updates PROJECT_STATE.md and TODO.md

Current active mode: Manager/Reviewer (Phase 7 Active)

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
    |   +-- P4_001_INTEGRATION.md End-to-end integration test report
    |   +-- P4_002_OJW_EVALUATION.md OJW lexical coverage evaluation report
    |   +-- P4_005_ESPEAK_INTEGRATION.md Real eSpeak integration test matrix
    |   +-- MILESTONE_PHASE0_P4_002.md Comprehensive milestone snapshot report
    |
    +-- src/
    |   +-- normalization/      Unicode normalization & text tokenization
    |   +-- g2p/                Lossless grapheme-to-phoneme engine
    |   +-- acoustic/           Acoustic mapper & eSpeak-ng backend
    |   +-- evaluation/         Evaluation harnesses & OJW benchmark
    |   +-- tts/                High-level synthesis API
    |
    +-- data/                   Data directory
    +-- tests/                  Test suite (80 tests passing)
    +-- experiments/            Experiments directory
    +-- notebooks/              Research notebooks (empty)
