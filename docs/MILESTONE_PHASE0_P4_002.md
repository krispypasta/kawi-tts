# Kawi-TTS Project Milestone Snapshot: Phase 0 through P4-002

**Date:** 2026-10-07
**Milestone:** Phase 0–3 Complete; Phase 4 Integration (P4-001) & Lexical Evaluation (P4-002) Complete
**Current Branch:** `main` (commit `57cc12d` + local Phase 4 additions)
**Test Suite Status:** 79 tests passing (100% pass rate)

---

## 1. Project Goal

Kawi-TTS is an academic, research-first Text-to-Speech (TTS) initiative for Old Javanese (*Basa Kawi*). Its primary purpose is to make classical Old Javanese literary, historical, and epigraphic texts accessible through speech synthesis, while strictly prioritizing **linguistic defensibility and evidentiary traceability over synthetic vocal naturalness**.

---

## 2. V1 Target: Profile A — Reconstructed Historical Spoken Old Javanese

Per formal decision **DEC-006**, the V1 target is:
**Profile A: Reconstructed Historical Spoken Old Javanese**.

* **Scope:** Reconstructs the spoken pronunciation of Old Javanese based on comparative Austronesian historical phonology and epigraphic research.
* **Separation from other profiles:**
  * **Profile B (Future):** Scholarly / Orthographic Reading (preserving full Sanskrit loanword orthography in speech).
  * **Profile C (Future):** Balinese *Kakawin* / *Mabasan* performance (modeling living traditional metrical and musical chanting).

---

## 3. Epistemic Policy & Boundaries

* **No known surviving recordings from the historical period are currently available to establish historical pronunciation directly.**
* The synthesized speech is an **evidence-based reconstruction**, NOT a claim of historically proven certainty.
* Every substantive linguistic claim must carry an auditable label:
  * `ESTABLISHED`: Strongly supported by reliable, concordant linguistic evidence.
  * `RECONSTRUCTED`: Inferred from comparative/historical evidence rather than directly attested.
  * `UNCERTAIN`: Evidence is insufficient, ambiguous, or conflicting.
  * `ASSUMPTION`: Temporary engineering/project assumption; never linguistic evidence.
* **Information Preservation First:** Linguistic uncertainty is preserved losslessly in the front-end (G2P) representation and must never be silently collapsed to satisfy backend constraints.
* Acoustic adaptations are strictly segregated to the downstream **Acoustic Mapper** and labeled `PROVISIONAL_ACOUSTIC_MAPPING`.

---

## 4. Phase 0 — Foundation (Completed 2026-10-07)

* Established repository governance, scope, and quality gates (`AGENTS.md`, `docs/AGENT_ROLES.md`, `docs/PROJECT_SPEC.md`).
* Marked system architecture as explicitly provisional (`docs/ARCHITECTURE.md`).
* Audited repository scaffold: removed unverified phonetic claims (e.g. ungrounded transcription of *om awighnam astu*) and downgraded unverified claims to `ASSUMPTION` in `docs/RESEARCH_LOG.md`.
* Established engineering decision log (`docs/DECISIONS.md`, DEC-001 through DEC-005).

---

## 5. Phase 1 — Linguistic Research (Completed 2026-10-07)

* Audited primary phonological and philological literature: Zoetmulder (1974, 1982), Kumar & Rose (2000), Acri & Griffiths (2014), Robson (1983), Schumacher (1995), Ardiansyah & Fitriana (2024).
* Logged research findings RES-001 through RES-016:
  * Established the indigenous 6-vowel system (/a, i, u, e, o, ə/).
  * Reconstructed the native dental vs. retroflex stop contrast (/t, d/ vs. /ṭ, ḍ/).
  * Established that Sanskrit aspirates, sibilants (ś, ṣ), and vowel length are orthographic in native vocabulary, with spoken loan realization remaining uncertain.
  * Audited Balinese *mabasan* chanting: established that *guru-laghu* governs musical duration and metrical weight, not phonemic vowel length.
* Compiled the **Pronunciation Inventory & Uncertainty Matrix** (P1-013 / Section 6 of `docs/RESEARCH_LOG.md`).
* Formally adopted DEC-006 (Profile A target).

---

## 6. Phase 2 — Data Audit (Completed 2026-10-07)

* Audited text and speech resources (RES-017 through RES-021):
  * **Old Javanese Wordnet (OJW):** Audited CC BY 4.0 license, TSV structure, and 4,192 unique lexical items based on Zoetmulder.
  * **GRETIL Corpora:** Audited 9 digitized Old Javanese texts for sentence-level testing.
  * **Modern Javanese Speech Resources:** Audited OpenSLR 41 (CC-BY-SA 4.0) and Facebook MMS-TTS-JAV (CC-BY-NC 4.0).
  * **Acoustic Reality:** Established that **no historical spoken speech corpus exists**, ruling out training an end-to-end Kawi model from scratch.
  * Confirmed that Modern Javanese natively models the required dental/retroflex stop contrast (/t, d/ vs /ṭ, ḍ/) and schwa (/ə/), establishing the viability of a two-stage hybrid cross-lingual transfer approach.

---

## 7. Phase 3 — Prototype Pipeline (Completed 2026-10-07, Git Commit `57cc12d`)

* **P3-002 Normalizer (`src/normalization/normalizer.py`):** Lossless Unicode NFC canonicalizer, typographic cleanup (ŋ $\to$ ṅ, ě $\to$ ĕ), and elision preservation.
* **P3-003A/B/C G2P Engine (`src/g2p/engine.py`):** Lossless greedy G2P parser mapping normalized text to internal phonological tokens without collapsing distinctions. Audited against edge cases.
* **P3-004 Tokenizer (`src/normalization/tokenizer.py`):** Deterministic text-structure layer isolating words, punctuation, line breaks, hyphens (`TokenType.BOUNDARY`), and elision marks (`TokenType.ELISION`). Flags unsegmented ASCII ambiguities (e.g. `sanghyang`) as `TokenType.UNRESOLVED`.
* **P3-005 Backend Survey (`docs/P3_005_ACOUSTIC_BACKEND_SURVEY.md`):** Surveyed backends and adopted a two-stage hybrid roadmap: eSpeak-ng prototype first, neural transfer later.
* **P3-006 Acoustic Mapper & Backend (`src/acoustic/`):** Implemented `AcousticMapper` (mapping G2P tokens to eSpeak IPA while stamping provisional adaptations) and `ESpeakBackend` (CLI runner with dry-run/mock execution).
* **P3-007 Evidence Validation (`docs/P3_007_VALIDATION.md`):** Verified end-to-end pipeline across 26 authentic Old Javanese source citations in 13 linguistic categories. Fixed G2P word-parser capitalization bug. 66 automated unit tests passing.

---

## 8. P4-001 — Integration Testing (Completed 2026-10-07)

* Authored `tests/test_integration.py` (10 comprehensive end-to-end integration tests).
* Verified component contracts, raw input recovery, non-mutation of G2P structures by the Acoustic Mapper, and error handling for empty, whitespace, and non-lexical inputs.
* Verified that non-dry-run execution without local `espeak-ng` raises an actionable `ESpeakNotFoundError`.
* Expanded test suite from 66 to 76 tests passing. Documented in `docs/P4_001_INTEGRATION.md`.

---

## 9. P4-002 — OJW Lexical Coverage Evaluation (Completed 2026-10-07)

* Acquired unmodified raw dataset `data/raw/wn-kaw.tab` from `davidmoeljadi/OJW` (SHA-256: `fc208d9f...`).
* Computed exact dataset metrics: 5,020 total lines, 5,019 data rows (senses), 2,032 synsets, 3,632 unique lemmas, 569 unique variants, and **4,192 unique deduplicated lexical forms**.
* Implemented evaluation harness (`src/evaluation/evaluate_ojw.py`) and automated regression tests (`tests/test_evaluation.py`).
* Evaluated all 4,192 unique lexical forms:
  * **99.90% symbolic representation coverage (4,188 / 4,192 forms fully supported).**
  * Zero runtime crashes or exceptions.
  * Exactly 4 forms (0.095%) contained rare philological characters (`â`, `î`, `ṃ`, `ḥ`), safely preserved and flagged without crashing.
  * 409 forms (9.76%) contained provisional acoustic tokens (voiced aspirates, vocalic liquids, long pepet).
  * Generated machine-readable artifact `data/processed/ojw_coverage_report.json` and report `docs/P4_002_OJW_EVALUATION.md`.
  * Expanded test suite to **79 tests passing**.

---

## 10. Current Pipeline Architecture

```text
Raw Kawi Text Input
       ↓
[1. Normalizer]      src/normalization/normalizer.py       [IMPLEMENTED & TESTED]
       ↓             NFC composition, ŋ → ṅ, ě → ĕ, elision canonicalization
[2. Tokenizer]       src/normalization/tokenizer.py        [IMPLEMENTED & TESTED]
       ↓             Words, punctuation, hyphens (BOUNDARY), apostrophes (ELISION), UNRESOLVED
[3. G2P Engine]      src/g2p/engine.py                     [IMPLEMENTED & TESTED]
       ↓             Lossless internal phonemes per word (no collapsed distinctions)
[4. Acoustic Mapper] src/acoustic/mapper.py                [IMPLEMENTED & TESTED]
       ↓             Backend IPA mapping, PROVISIONAL_ACOUSTIC_MAPPING stamping, audit trail
[5. eSpeak Backend]  src/acoustic/espeak_backend.py        [IMPLEMENTED; MOCK/DRY-RUN VERIFIED]
       ↓             Deterministic CLI wrapper; dry-run WAV generation; real audio requires local binary
Audio Output (WAV)   [MOCK VERIFIED ON HOST; REAL SYNTHESIS NOT YET DEMONSTRATED ON HOST]
```

---

## 11. Current Research Conclusions

1. **Old Javanese is a historical language without surviving native audio.** Reconstruction must be guided by philology, epigraphy, and comparative Austronesian linguistics.
2. **Orthography $\neq$ Phonology $\neq$ Phonetics.** The presence of Sanskrit characters in Indic inscriptions does not prove that historical speakers realized all Indian phonemic distinctions.
3. **Balinese *kakawin* chanting is not conversational Old Javanese.** *Guru-laghu* operates as a metrical constraint in poetry, not evidence of lexical vowel duration in everyday speech.
4. **Information must be preserved losslessly in the front-end.** Uncertain distinctions must remain visible to callers and downstream layers.
5. **No end-to-end Kawi speech training data exists.** The project must use a hybrid rule-based G2P front-end paired with an acoustic synthesis engine or cross-lingual transfer backend.

---

## 12. Established Findings

* **Native 6-Vowel Inventory:** /a, i, u, e, o, ə/ (ESTABLISHED; RES-001, Kumar & Rose 2000).
* **Pepet Status:** Mid-central schwa /ə/ (ESTABLISHED; RES-003, Damais 1970, Acri & Griffiths 2014).
* **Native Consonants:** Core stops (/p, b, t, d, c, ɟ, k, g/), nasals (/m, n, ŋ, ɲ/), glides/liquids (/w, j, r, l/), and fricatives (/s, h/) (ESTABLISHED; RES-001).
* **Orthographic Romanization Baseline:** Zoetmulder (1982) convention with Acri/Damais equivalence (ESTABLISHED; RES-007, DEC-007).
* **Living Recitation Metrics:** *Guru* and *laghu* represent metrical weight and musical melisma in Balinese performance, not phonemic spoken duration (ESTABLISHED; RES-008, RES-009, Schumacher 1995).

---

## 13. Reconstructed Findings

* **Dental vs. Retroflex Stop Contrast:** /t, d/ vs. /ṭ, ḍ/ is a native Javanese feature, not merely an orthographic borrowing (RECONSTRUCTED; RES-001, RES-005, Kumar & Rose 2000).
* **Absence of Native Aspirates:** Aspirated stops did not exist in indigenous Austronesian vocabulary (RECONSTRUCTED; RES-004).
* **Absence of Native Palatal/Retroflex Sibilants:** Indigenous Old Javanese possessed only /s/ (RECONSTRUCTED; RES-006).

---

## 14. Uncertain Findings

* **Spoken Realization of Sanskrit Aspirates:** Whether bilingual elites in the classical period pronounced aspiration in Sanskrit loanwords in everyday speech (UNCERTAIN; RES-004).
* **Spoken Realization of Sanskrit Sibilants:** Whether ś and ṣ were distinguished from /s/ in spoken loanwords (UNCERTAIN; RES-006).
* **Spoken Vowel Length in Loans:** Whether long vowels (ā, ī, ū) possessed phonemic duration in colloquial speech outside metrical recitation (UNCERTAIN; RES-002).
* **Exact Phonetics of ṭ/ḍ:** True retroflexes [ʈ, ɖ] vs. apical alveolars [t, d] (UNCERTAIN; RES-001, RES-005).
* **Status of Vocalic Liquids (ṛ, ḷ), Retroflex Nasal (ṇ), and Long Pepet (ö):** Realization in spoken registers remains unresolved (UNCERTAIN; RES-020).

---

## 15. Engineering Decisions (DEC-001 through DEC-009)

* **DEC-001 (Decided):** Research-first structure; no code before linguistic justification.
* **DEC-002 (Decided):** Romanized Old Javanese as primary input format.
* **DEC-003 (Decided):** Zoetmulder (1982) as primary lexicographic reference.
* **DEC-004 (Decided):** Three AI work modes within Hermes sharing the repository as truth (no autonomous agent framework).
* **DEC-005 (Decided):** V1 deliverable scope: text in $\to$ audio + phonemes + rule citations out. Naturalness is secondary.
* **DEC-006 (Decided):** V1 target = Profile A (Reconstructed Historical Spoken Old Javanese).
* **DEC-007 (Decided):** Canonical romanization is Zoetmulder (1982), with explicit Acri/Damais converter.
* **DEC-008 (Decided):** Lossless internal G2P representation; zero phonological collapsing in the front-end.
* **DEC-009 (Decided):** Two-stage hybrid acoustic backend: eSpeak-ng prototype first, neural transfer later.

---

## 16. Decisions Explicitly NOT Made

* We have NOT decided to collapse Sanskrit aspirates into plain stops.
* We have NOT decided to truncate vowel length in the G2P engine.
* We have NOT decided to merge ś and ṣ into /s/.
* We have NOT decided to map ṛ and ḷ to /rə/ and /lə/.
* We have NOT decided to merge ṭ and ḍ into dental /t/ and /d/.
* We have NOT selected a final neural TTS architecture or vocoder.

---

## 17. Current Dataset / Resource Status

* **Raw Text Corpus:**
  * `data/raw/wn-kaw.tab`: Present, verified, SHA-256 audited (157.5 KB, 4,192 unique lexical forms).
  * GRETIL Texts: Available online for sentence testing; not yet downloaded locally.
* **Processed Evaluations:**
  * `data/processed/ojw_coverage_report.json`: Present, machine-readable metrics generated.
* **Speech Corpora:**
  * No historical Kawi speech exists.
  * OpenSLR 41 Modern Javanese speech audited for potential future transfer learning; not yet downloaded.
  * Bali 1928 performance recordings audited and classified as Profile C only.

---

## 18. Current Test Status

* Total automated unit and integration tests: **79 tests passing (100% pass rate)**.
* Execution time: ~0.97s.
* Test suite structure:
  * `tests/test_scaffold.py`: 1 test
  * `tests/test_normalization.py`: 15 tests
  * `tests/test_tokenizer.py`: 15 tests
  * `tests/test_g2p.py`: 8 tests
  * `tests/test_acoustic_mapper.py`: 9 tests
  * `tests/test_synthesis_pipeline.py`: 4 tests
  * `tests/test_validation.py`: 14 tests
  * `tests/test_evaluation.py`: 3 tests

---

## 19. Known Limitations

1. **eSpeak Binary Absent on Host:** Real audio generation is not yet demonstrated on this development machine because `espeak-ng` is not installed on PATH. The pipeline executes deterministically in mock/dry-run mode.
2. **Synthetic Naturalness:** eSpeak-ng is a formant synthesizer. Its vocal output will sound mechanical and is intended for pipeline verification, not human realism.
3. **Four Unsupported Philological Forms in OJW:** `tīrthâṅga` (â), `aṅipîpi` (î), `bhraṃśa` (ṃ), `āśiḥ` (ḥ). Affects 0.095% of vocabulary; handled without crashing, but graphemes are not yet mapped.
4. **Sentence Prosody:** Intonation and metrical scansion (*guru-laghu* prosody) are not yet modeled at the sentence level.

---

## 20. Current Blockers

* **None.** The project has met all entry criteria for Phase 4.

---

## 21. Next Planned Tasks (Phase 4 Roadmap)

1. **P4-003 (NEXT):** Basic documentation of the pronunciation system (`docs/V1_PRONUNCIATION_GUIDE.md`), mapping every rule to research log entries and citations.
2. **P4-004:** User-facing README with example and source citations (Completed in Phase 3 checkpoint).
3. **P4-005 (CLI / Integration):** Implement user-facing command-line interface (`python -m src.cli`) exposing normalization, G2P inspection, and synthesis.
4. **V1 Release Checkpoint:** Tag V1 prototype.
