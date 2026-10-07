# Phase 7-D: Core Engine Acceptance Evaluation

**Date:** 2026-10-08
**Phase:** 7-D (Core Engine Acceptance Evaluation)
**Status:** COMPLETE (Gate: ACCEPT)

## 1. Executive Summary

This report documents the final acceptance evaluation of the deterministic Kawi-TTS core engine. Following the Phase 7-003 Zero-Budget Scope Reassessment and the P7-B/P7-C linguistic hardening, this evaluation verifies that the core pipeline successfully, deterministically, and traceably translates representative continuous Kawi text into valid acoustic backend (eSpeak-ng) instructions according to strict project policy.

The core is proven to be policy-consistent, reproducible, and strictly respects the epistemic boundary between Canonical preservation, Linguistic Reconstruction (Profile A), and Scholarly Reading (Profile B).

**Conclusion:** The deterministic core is ACCEPTED. Phase 7 is closed.

## 2. Acceptance Corpus & Test Methodology

A representative four-phrase acceptance corpus was constructed from existing project data to exercise all major architectural boundaries and edge cases:

1. **ACC-01:** `om awighnam astu namas sidham` (Continuous classic invocation with spacing, voiced aspirates).
2. **ACC-02:** `sang-hyang kamahāyānikan` (Hyphen boundary bypass, ambiguity edge case, long `a` macrons).
3. **ACC-03:** `prakṛti śānti bhaṭāra` (Complex clusters, syllabic `r`, sibilants, voiced aspirate, retroflex vs dental).
4. **ACC-04:** `SANKHA ḍaṅ kṝta` (Uppercase, voiceless aspirate fall-through, retroflex plosive, long syllabic liquid).

These were run through the complete `synthesize()` pipeline (`src/acoustic/pipeline.py`), capturing Normalization, Tokenization, G2P, Canonical, Profile Target, and eSpeak IPA outputs. A dry-run dummy WAV workflow verified backend determinism.

## 3. End-to-End Results & Profile Comparison

The engine successfully processed all continuous text without failure, proving that continuous real-world input is supported.

### ACC-01: `om awighnam astu namas sidham`
*   **Canonical:** `o-m | a-w-i-gʱ-n-a-m | a-s-t-u | n-a-m-a-s | s-i-dʱ-a-m`
*   **Profile A:** `o-m | a-w-i-g-n-a-m | a-s-t-u | n-a-m-a-s | s-i-d-a-m` (EXPECTED POLICY DIVERGENCE: Voiced aspirates merged)
*   **Profile B:** `o-m | a-w-i-gʱ-n-a-m | a-s-t-u | n-a-m-a-s | s-i-dʱ-a-m` (EXPECTED POLICY DIVERGENCE: Voiced aspirates preserved)
*   **Acoustic A:** `om awignam astu namas sidam`
*   **Acoustic B:** `om awigʱnam astu namas sidʱam`

### ACC-02: `sang-hyang kamahāyānikan`
*   **Canonical:** `s-a-n-g | h-j-a-n-g | k-a-m-a-h-aː-j-aː-n-i-k-a-n`
*   **Profile A:** `s-a-n-g | h-j-a-n-g | k-a-m-a-h-a-j-a-n-i-k-a-n` (EXPECTED POLICY DIVERGENCE: Macrons stripped/unresolved)
*   **Profile B:** `s-a-n-g | h-j-a-n-g | k-a-m-a-h-aː-j-aː-n-i-k-a-n` (EXPECTED POLICY DIVERGENCE: Macrons preserved)
*   **Acoustic A:** `sang hjang kamahajanikan`
*   **Acoustic B:** `sang hjang kamahaːjaːnikan`

### ACC-03: `prakṛti śānti bhaṭāra`
*   **Canonical:** `p-r-a-k-r̩-t-i | ś-aː-n-t-i | bʱ-a-ṭ-aː-r-a`
*   **Profile A:** `p-r-a-k-rə-t-i | s-a-n-t-i | b-a-ṭ-a-r-a` (EXPECTED POLICY DIVERGENCE: Syllabic liquid fallback, sibilant merger, aspirate merger, macron strip)
*   **Profile B:** `p-r-a-k-r̩-t-i | ś-aː-n-t-i | bʱ-a-ṭ-aː-r-a` (EXPECTED POLICY DIVERGENCE: Preservation)
*   **Acoustic A:** `prakrəti santi baʈara`
*   **Acoustic B:** `prakr̩ti ʃaːnti bʱaʈaːra`

### ACC-04: `SANKHA ḍaṅ kṝta`
*   **Canonical:** `s-a-n-kʰ-a | ḍ-a-ŋ | k-r̩ː-t-a`
*   **Profile A:** `s-a-n-kʰ-a | ḍ-a-ŋ | k-r̩ː-t-a` (ENGINEERING FALLBACK / INTENTIONAL: Voiceless aspirates and long syllabics fall through to Profile B defaults as they lack explicit merger rules)
*   **Profile B:** `s-a-n-kʰ-a | ḍ-a-ŋ | k-r̩ː-t-a`
*   **Acoustic A:** `sankʰa ɖaŋ kr̩ːta`
*   **Acoustic B:** `sankʰa ɖaŋ kr̩ːta`

## 4. Determinism & Diagnostics Validation
1.  **Test Suite:** 94/94 deterministic unit tests passing cleanly.
2.  **Regression Corpus:** The 100-form regression corpus (`tests/regression_corpus.tsv`) successfully completed with zero mutations.
3.  **Trace/Coverage Tools:** Validated. `kawi-trace` matches actual E2E canonical output identically. The Coverage Reporter explicitly logs unresolved fall-throughs.
4.  **Audio Generation:** Dry-run dummy WAV headers verify that file payload structure and eSpeak binary invocations (`--voice=jv`) are mathematically reproducible given the same input string.

## 5. Failure / Issue Taxonomy & Blockers
**Zero P0/P1 defects found in the core engine logic.**
*   *UNRESOLVED / NEEDS EVIDENCE:* Vowel length contrast in Profile A (`aː`), Palatal/Retroflex Aspirate loss (`ɟʱ`, `ḍʱ`). These are correctly handled structurally (logged as UNRESOLVED/PROVISIONAL without halting the system).
*   *EXPECTED:* `sanghyang` returns `AMBIGUOUS` token type as a deliberate bypass block; hyphenation correctly circumvents it.

## 6. Important Epistemic Boundary Statement
The Kawi-TTS project maintains that **the generated audio is not authentic historical Kawi speech.**
The strongest defensible claim of this software is:
> "The implementation deterministically realizes the project's documented reconstruction policies and produces reproducible acoustic output through the selected backend (eSpeak-ng)."

## 7. Acceptance Decision & Freeze Criteria

**DECISION: ACCEPT.**
The deterministic Kawi-TTS core is sufficiently reliable and policy-consistent for its current intended scope.

**Freeze Criteria:**
The following items are now locked and constitute the stable deterministic core:
1.  Canonical representation semantics and the `g2p_word` output matrix.
2.  Current Profile A historical evidence bounds (voiceless aspirates and palatal/retroflex aspirates are explicitly NOT merged unless evidence is provided).
3.  Current Profile B strict-orthographic contract.
4.  The 100-form Regression Corpus expectations.

Future changes must use explicit research evidence, document the policy shift, and add regression tests under a new project milestone.

## 8. Phase 7 Closure & Explicitly Deferred Work
Phase 7 is officially closed.

**Explicitly Deferred Work:**
*   P7-002 Pilot Corpus Recording & Expert Speaker Recruitment (Zero-Budget constraint).
*   Neural TTS implementation (Zero-Budget constraint & dataset blocker).
*   Phase 6 Lexical Metadata / Etymological Tagging (Blocked).

Future reopening of Neural TTS or Data collection requires explicit rescinding of the P7-003 $0 Budget Constraint by the project owner.
