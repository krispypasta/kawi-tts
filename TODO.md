# TODO: Kawi-TTS

**Last updated:** 2026-10-07
**Current phase:** Phase 7 — Acoustic Backend Research & Data Strategy

This file tracks all prioritized tasks for the Kawi-TTS project.
Tasks are grouped by phase. Within each phase, tasks are ordered by priority.
Do not add tasks from a later phase until the prerequisites from earlier phases
are complete. Completed tasks are moved to the Archive section at the bottom.

---

## Phase 1: Linguistic Research (COMPLETED)

These tasks must be completed before any implementation work begins.
All research must be logged in docs/RESEARCH_LOG.md with cited sources
and evidence-status labels.

Priority 1: Phoneme inventory foundation (blocks everything else)

- [x] P1-001: Obtain and read Zoetmulder (1982) Old Javanese-English Dictionary
      introduction. Extract: romanization conventions, phoneme descriptions,
      any explicit phonological statements. Log findings for RQ-001, RQ-002, RQ-010.

- [x] P1-002: Identify and read at least one dedicated Old Javanese phonology
      or grammar source (candidate: Uhlenbeck 1949, or Hunter papers).
      Log findings for RQ-001 through RQ-006.

- [x] P1-003: Investigate the pepet (schwa / e-tailing) specifically.
      What phonemic status do sources assign to it? Is it allophonic? Orthographic?
      Log findings for RQ-003.

- [x] P1-004: Investigate aspirated stops. Are they phonemic in native Kawi vocabulary
      or only in Sanskrit loans? What comparative evidence exists?
      Log findings for RQ-004.

- [x] P1-005: Investigate retroflex consonants. Were they phonetically retroflex
      in Old Javanese, or were they dental/alveolar in actual realization?
      Log findings for RQ-005.

- [x] P1-006: Investigate sibilant distinctions (s / palatal-s / retroflex-s).
      Document the scholarly consensus, or the fact that no consensus exists.
      Log findings for RQ-006.

Priority 2: Orthography and romanization (blocks input format decision)

- [x] P1-007: Systematically document the romanization convention used in
      Zoetmulder (1982). Identify any characters, diacritics, or conventions
      that are ambiguous or not described in the dictionary itself.
      Log findings for RQ-010.

- [x] P1-008: Survey whether other romanization conventions are in common
      scholarly use (e.g., older Dutch Leiden conventions, ISO 15919).
      Document differences. Log findings for RQ-011.

- [x] P1-009: After completing P1-007 and P1-008, make and document
      the project decision: which romanization convention will be used
      as the primary TTS input format? Record the decision in docs/DECISIONS.md.
      Log findings for RQ-012.

Priority 3: Pronunciation traditions (informs synthesis decisions)

- [x] P1-010: Research the Balinese Kawi recitation tradition (mabasan).
      What is the relationship between the recited pronunciation and the
      scholarly reconstruction of Old Javanese phonology?
      Log findings for RQ-013.

- [x] P1-011: Search for publicly accessible audio recordings of Kawi
      recitation (mabasan, kakawin chanting). Document source, provenance,
      accessibility, and any known licensing conditions.
      Log findings for RQ-014.

Priority 4: Corpus and computational resources survey (COMPLETED)

- [x] P1-012: Survey digitally available romanized Old Javanese text corpora.
      Check GRETIL, KITLV, SEALang, and institutional repositories.
      Document what exists, its scope, and its license status.
      Log findings for RQ-016, RQ-017.

- [x] P1-013: Search for prior computational-linguistic work on Old Javanese:
      G2P tools, morphological analyzers, digital dictionaries with phonemic
      annotation, NLP datasets.
      Log findings for RQ-019.

---

## Phase 2: Data Audit (COMPLETED)

Do not begin these tasks until Phase 1 research questions RQ-001 through
RQ-014 have findings logged in RESEARCH_LOG.md.

- [x] P2-001: Evaluate available text corpora for size, quality, and TTS suitability (e.g. GRETIL Old Javanese texts).
- [x] P2-002: Evaluate OJW (Old Javanese Wordnet) for use as a lexical validation list.
- [x] P2-003: Assess modern Javanese acoustic models (e.g., MMS-TTS-JAV, OpenSLR 41) for cross-lingual transfer suitability against Profile A phonemes.
- [x] P2-004: Write a data feasibility assessment report to finalize the architecture.

---

## Phase 3: Prototype Pipeline (COMPLETED)

Do not begin these tasks until Phase 2 is complete and a data feasibility
decision has been made.

- [x] P3-001: Choose the romanization input format — Completed via DEC-002, DEC-003, and P3-002 (Zoetmulder 1982 canonical, with Acri/Damais conversion).
- [x] P3-002: Implement Unicode normalization for the chosen romanization scheme.
- [x] P3-003A: Produce formal G2P specification and decision matrix for Profile A.
- [x] P3-003B: Implement rule-based G2P based on P3-003A specification.
      Every G2P rule must cite its source from RESEARCH_LOG.md.
- [x] P3-003C: G2P Validation & Edge-Case Audit.
- [x] P3-004: Implement text-structure / tokenization layer (punctuation, boundary markers, numbers).
- [x] P3-005: Set up basic TTS synthesis backend (choice to be made after Phase 2) — Completed via P3-005 Acoustic Backend Survey.
- [x] P3-006: Implement Acoustic Mapper stub and eSpeak-ng prototype backend (phoneme-to-audio pipeline).
- [x] P3-007: Write tests for G2P rules using cited word examples from sources (Completed via P3-007 Validation Audit).

---

## Phase 5: Post-V1 Research & Architecture (COMPLETED)

- [x] P5-001: Post-V1 Evidence & Feasibility Audit.
- [x] P5-002: Evidence-Based Acoustic Profile Policy. Formally defined Profile A vs Profile B, and authorized evidence-backed acoustic mergers (aspirates, sibilants) for Profile A while keeping canonical representation distinct.
- [x] P5-003: Profile Architecture Design & Vowel Length Strategy. Design the software layer separating Profile A and Profile B, and determine etymological/metrical vowel length handling.

## Phase 6: V2 Profile Implementation (COMPLETED)

- [x] P6-001: Implement `ProfileStrategy` abstraction. Extract V1 legacy acoustic mappings into `ProfileBStrategy`.
- [x] P6-002: Implement `ProfileAStrategy` applying historical mergers with `ProfiledToken` citations.
- [x] P6-003: Vowel Length Strategy (Research & Policy Document). Establish etymological constraints and fallback mechanism.
- [x] P6-004: Lexical/Etymological Metadata Feasibility Audit. Concluded metadata classifier is blocked by data.
- [ ] P6-005: [BLOCKED] Etymological Metadata Implementation. Requires provenance-tagged lexicon.

## Phase 7: Zero-Budget Reassessment & Engine Hardening (ACTIVE)

- [x] P7-001: [DEFERRED/BLOCKED] Data Acquisition & Corpus Design (Superseded by P7-003 constraint).
- [x] P7-002A: Existing Audio Source Audit (Concluded Path C required, which is now blocked).
- [ ] P7-002: [BLOCKED] Pilot Corpus Recording. Deferred by zero-budget constraint.
- [x] P7-003: Zero-Budget Scope Reassessment & Frankenstein Stop. Redefined project to $0 core deliverable.

**Revised Zero-Cost Roadmap:**
- [x] P7-B: Linguistic and pronunciation-engine hardening (normalization, G2P rules, ambiguity handling, test coverage).
- [x] P7-C: Baseline Acoustic & Evaluation infrastructure (ACTIVE) (eSpeak backend control, deterministic synthesis, automated tests).
- [ ] P7-D: Research tooling (bibliography management, evidence-status tracking).
- [ ] P7-E: [OPTIONAL/FROZEN] Neural Reopening Criteria.

## Phase 4: V1 (COMPLETED)

V1 deliverable: romanized Old Javanese text in, audio + phoneme sequence + source
citations out. Pronunciation must be traceable to cited research log entries.

- [x] P4-001: End-to-end pipeline integration test (Completed via P4-001 Integration Suite, 76 tests).
- [x] P4-002: G2P evaluation against documented word examples from scholarly sources (Completed: 99.90% coverage across 4,192 OJW lexical forms).
- [x] P4-003: Basic documentation of the pronunciation system (what rules, what sources) (Completed: PRONUNCIATION_SYSTEM.md).
- [x] P4-004: User-facing README with example and source citations (Completed in Phase 3 checkpoint).
- [x] P4-005: Real eSpeak Integration (Completed: P4_005_ESPEAK_INTEGRATION.md).
- [x] P4-006: V1 Evaluation & Release Readiness
      Evaluate symbolic frontend coverage, real backend execution, representative audio results,
      backend warnings, unsupported/provisional mappings, and human listening results.
      Produce docs/P4_006_V1_EVALUATION.md. State limitations and define exactly what V1 proves
      and does NOT prove. Final release happens only after P4-006 is fully approved.
- [x] P4-006F: Fix G2P greedy digraph bug. The `gh` digraph is correctly a voiced aspirate `gʱ` in Sanskrit borrowings, but in unhyphenated `sanghyang`, the `ng` + `h` sequence is falsely merged into `n` + `gʱ`. Implement morphological or sequence-based boundary protection in `src/g2p/engine.py`.

---

## Infrastructure (can be done any time, low priority)

- [ ] INF-001: Set up pytest configuration and CI check for the test suite.
- [ ] INF-002: Configure linting (flake8 or ruff) for src/.
- [ ] INF-003: Confirm test_scaffold.py passes (it is currently a scaffold test).

---

## Explicitly Out of Scope (do not add tasks for these)

- Chatbot functionality
- Machine translation
- Kawi OCR / manuscript recognition
- Kawi script rendering
- Voice cloning
- Multi-speaker synthesis
- Emotional speech
- Training a foundation model from scratch
- Unnecessary multi-agent frameworks
- Any infrastructure beyond what a single researcher needs

---

## Archive (completed tasks)

### Phase 3: Prototype Pipeline (completed 2026-10-07)

- [x] P3-001: Choose the romanization input format (DEC-002, DEC-003, P3-002).
- [x] P3-002: Unicode & orthographic normalization (NFC, character canonicalization).
- [x] P3-003A: G2P specification & decision matrix for Profile A.
- [x] P3-003B: Lossless G2P engine implementation.
- [x] P3-003C: G2P edge-case validation audit.
- [x] P3-004: Text-structure & tokenization layer.
- [x] P3-005: Acoustic backend survey & decision gate.
- [x] P3-006: Acoustic mapper & eSpeak-ng prototype backend interface.
- [x] P3-007: Evidence-based end-to-end validation on 26 real Old Javanese examples (66 tests passing).

### Phase 2: Data Audit (completed 2026-10-07)

- [x] P2-001 through P2-004: Audited OJW, GRETIL, and Modern Javanese TTS models (MMS, OpenSLR 41) for feasibility and phonemic compatibility with Profile A. Findings logged as RES-017 through RES-021.

### Phase 1: Linguistic Research (completed 2026-10-07)

- [x] P1-001 through P1-011: Core phoneme inventory, orthography, and pronunciation traditions researched. Findings logged as RES-001 through RES-012.
- [x] P1-012, P1-013: Corpus, Licensing, and Computational Resource Survey. Findings logged as RES-013 through RES-016.
- [x] DEC-006: V1 Pronunciation Target decided as Profile A (Historical Spoken).

### Phase 0: Project Foundation (completed 2026-10-07)

- [x] P0-001: Write full project vision and scope (docs/PROJECT_SPEC.md).
- [x] P0-002: Write provisional architecture document (docs/ARCHITECTURE.md).
- [x] P0-003: Create structured research log with Phase 1 question agenda
              (docs/RESEARCH_LOG.md).
- [x] P0-004: Create AI work mode definitions (docs/AGENT_ROLES.md).
- [x] P0-005: Create engineering decision log (docs/DECISIONS.md).
- [x] P0-006: Create top-level AI guidance file (AGENTS.md).
- [x] P0-007: Write project state file (PROJECT_STATE.md).
- [x] P0-008: Write this task file (TODO.md).
