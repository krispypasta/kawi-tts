# Phase 7-C: Evaluation & Diagnostics Infrastructure Report

**Date:** 2026-10-08
**Phase:** 7-C (Evaluation & Diagnostics Infrastructure)
**Status:** COMPLETE (Gate: GO)

## 1. Executive Summary

In accordance with the **Zero-Budget Scope Reassessment (P7-003)**, the Kawi-TTS project has implemented its foundational observability and diagnostic tools without altering the underlying linguistic pipeline. This P7-C implementation provides transparency into the deterministic phonological transformations across profiles, confirming strict preservation boundaries and highlighting any unsupported fall-throughs.

The tools implemented are strictly observational and rely entirely on the existing normalizer, tokenizer, G2P, and acoustic mappers.

## 2. Deliverables Implemented

### 2.1 Trace CLI (`kawi-trace.py`)
A command-line diagnostic tool that accepts one or more Kawi words and traces them through the five stages of the pipeline:
1.  **Normalization** (Uppercase preservation, structural cleanup)
2.  **Tokenization** (Word boundaries, punctuation, ambiguity flagging)
3.  **Canonical Representation** (G2P, information-preservation)
4.  **Profile Output** (Profile A vs Profile B linguistic targets)
5.  **Acoustic Backend Mapping** (eSpeak-ng backend rendering string)

**Status:** Completed. Resides in `src/cli/kawi_trace.py`. No pipeline behavior was modified.

### 2.2 Phoneme Coverage Reporter (`coverage_report.py`)
A comprehensive reporter that cross-references the canonical phoneme inventories (`_MONOGRAPH_MAP`, `_DIGRAPH_MAP`) against the implementations of `ProfileAStrategy` and `ProfileBStrategy`.

**Status:** Completed. Resides in `src/cli/coverage_report.py`.
It classifies all tokens into explicit states:
-   `SUPPORTED`: Explicitly mapped and preserved by the profile.
-   `SUPPORTED (Merged)`: Explicitly merged to a different historical target (e.g. Profile A aspirate loss).
-   `PROVISIONAL`: Handled by an engineered fallback with no strict historical claim.
-   `UNRESOLVED`: Structurally deferred due to open architectural questions (e.g., macron length stripping).
-   `UNSUPPORTED`: Falls through without explicit handling (unsafe).

### 2.3 Deterministic Regression Corpus (`regression_corpus.tsv`)
A 100-word targeted regression corpus that tests known edge cases, Profile A/B divergence, ambiguity traps, and normalization limits.

**Status:** Completed. Resides in `tests/regression_corpus.tsv`, paired with `tests/test_regression_corpus.py`.
-   **Size:** 100 high-value entries.
-   **Tested areas:** Native baselines, Uppercase preservation, Voiced aspirate mergers, Voiceless aspirate preservation, Sibilant divergence, Retroflex vs dental plosives, Vowel length deferment (macrons), Syllabic liquids, Hyphen boundary protection, Ambiguity blocks (`sanghyang`), and special diacritic forms.
-   All 100 forms cleanly pass the P7-B hardened pipeline.

## 3. Findings & Validation

### 3.1 Trace Examples
Example traces confirm that the pipeline resolves edge cases exactly as per policy:

**Example: `BHAṬĀRA`** (Uppercase, Aspirate, Retroflex, Macron)
```text
[1] Normalized  : BHAṬĀRA
[2] Tokenizer   : 1 token(s)
    - WORD: 'BHAṬĀRA'
[3] Canonical   : bʱ-a-ṭ-aː-r-a
[4] Profile A   : b-a-ṭ-a-r-a       <-- Aspirate merged (bʱ->b), Macron stripped (aː->a)
[4] Profile B   : bʱ-a-ṭ-aː-r-a      <-- Aspirate preserved, Macron preserved
[5] Acoustic A  : 'baʈara'
[5] Acoustic B  : 'bʱaʈaːra'
```

**Example: `sanghyang` vs `sang-hyang`** (Ambiguity Protection)
```text
TRACE: sanghyang
[1] Normalized  : sanghyang
[2] Tokenizer   : BLOCKED (Ambiguity detected)
    -> Token 'sanghyang': Ambiguous cluster 'ngh' ...

TRACE: sang-hyang
[1] Normalized  : sang-hyang
[2] Tokenizer   : 3 token(s)
    - WORD: 'sang'
    - BOUNDARY: '-'
    - WORD: 'hyang'
[3] Canonical   : s-a-n-g | h-j-a-n-g
...
```

### 3.2 Phoneme Coverage Findings
The reporter confirmed that no canonical phonemes currently fall through to `UNSUPPORTED`. However, the following dependencies were observed:
-   **Unresolved Vowel Length:** `aː`, `iː`, `uː`, `əː` accurately flag as `UNRESOLVED` in Profile A (where they map to `a`, `i`, `u`, `ə`), but `SUPPORTED`/`PROVISIONAL` in Profile B.
-   **Voiced Aspirates:** `bʱ`, `dʱ`, `gʱ` are successfully `SUPPORTED (Merged)` in Profile A (merged to `b`, `d`, `g`).
-   **Palatal/Retroflex Aspirates:** `ɟʱ`, `ḍʱ` remain `PROVISIONAL` across both profiles due to historical uncertainty (P5-002A).
-   **Voiceless Aspirates:** `cʰ`, `kʰ`, `tʰ`, `ṭʰ` are explicitly `SUPPORTED` in both profiles (the backend supports them, and no merger policy has yet targeted them). `pʰ` is an exception, having an explicit merger rule (`pʰ -> p`) in Profile A.
-   **Syllabic Liquids:** `r̩`, `l̩`, `r̩ː`, `l̩ː` remain `PROVISIONAL` in both profiles.

### 3.3 Test Suite Status
-   **Pre-P7-C Test Count:** 93 tests passing.
-   **Post-P7-C Test Count:** 94 tests passing (the new Regression Corpus test suite executes ~100 forms via `subTest`, acting as a single large unified integration test).
-   **New Files:** 4 (`src/cli/kawi_trace.py`, `src/cli/coverage_report.py`, `tests/regression_corpus.tsv`, `tests/test_regression_corpus.py`)
-   **Changed Files:** None of the core linguistic pipeline files (`normalizer.py`, `tokenizer.py`, `g2p/engine.py`, `acoustic/mapper.py`, or `strategies/*`) were changed. Behavior is 100% frozen.

## 4. Phase 7-C Gate Decision

**RECOMMENDATION:** GO.

**Justification:** The evaluation infrastructure adheres strictly to the constraints. It is purely observational and did not require any modification to the pipeline to "look clean." The deterministic regression corpus proves that the pipeline's information-preservation and profile-divergence invariants are actively upheld across 100 high-value linguistic edges.

We are ready to close out P7-C and conclude the Phase 7 engineering milestones.
