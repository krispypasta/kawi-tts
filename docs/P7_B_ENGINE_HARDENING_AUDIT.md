# Phase 7-B: Linguistic & Pronunciation Engine Hardening Audit

**Status:** Completed
**Constraint:** Zero-Budget ($0). Local execution, no paid resources, eSpeak baseline.

This report documents the rigorous hardening audit of the deterministic Kawi-TTS pronunciation pipeline, verifying the boundaries between canonical preservation and acoustic realization.

## 1. Current Pipeline
The deterministic pronunciation pipeline executes via the following distinct stages:
1. **Normalizer (`src/normalization/normalizer.py`)**: Performs lossless Unicode NFC canonicalization and unifies typographic variants (e.g., `ŋ` -> `ṅ`, `v` -> `w`). Preserves original case and ASCII digraphs.
2. **Tokenizer (`src/normalization/tokenizer.py`)**: Identifies structural boundaries, punctuation, and lexical words. Flags sequences with unresolvable orthographic ambiguity (e.g., `ngh`).
3. **G2P Engine (`src/g2p/engine.py`)**: Lowercases input and applies greedy phoneme matching to map orthography to internal phonological representations (e.g., `dh` -> `dʱ`).
4. **Canonical Representation**: An immutable list of phoneme strings preserving all historical and orthographic distinctions (e.g., macrons, aspirates, retroflexes).
5. **ProfileStrategy (`src/acoustic/strategies/`)**: Applies linguistic policy. **Profile A** merges evidence-backed sounds (e.g., `bʱ` -> `b`, strips vowel duration). **Profile B** passes canonical representation through unmodified.
6. **AcousticMapper (`src/acoustic/mapper.py`)**: Performs 1:1 translation from the strategy's target tokens to backend-compatible eSpeak-ng IPA strings.

## 2. Normalization Findings
* **Guaranteed:** NFC normalization, removal of invisible formatting artifacts, mapping Acri/Damais `v` to `w`, mapping typographic eng `ŋ` to standard `ṅ`.
* **Accepted:** Capital letters, punctuation, numerals.
* **Rejected/Warning:** Nothing is explicitly dropped.
* **Silently Transformed:** `ě` (caron) is unified to `ĕ` (breve).
* **Engineering Policy Upheld:** ASCII `ng` is explicitly NOT converted to `ṅ`. The normalizer does NOT lowercase the text, deferring case-folding to the G2P engine to preserve source formatting. This perfectly respects the Information Preservation directive.

## 3. G2P Findings
* **Greedy Precedence:** The engine correctly prioritizes digraphs (`bh`, `dh`, `th`, `ph`, `kh`, `gh`, `ch`, `jh`, `ṭh`, `ḍh`).
* **Base Character Length:** Characters like `ṭ` (`\u1E6D`) are length 1 in Python, so the `ṭh` digraph match executes cleanly as a 2-character sequence.
* **The `ngh` Exception:** The hardcoded fallback preventing `gh` from parsing as `gʱ` when preceded by `n` correctly prevents `sanghyang` from becoming `san-gʱ-yang`.
* **BUG / FALSE ALARM (P1):** The tokenizer explicitly flags `nkh` as a structural ambiguity, claiming a "conflict between ASCII velar nasal nk and Sanskrit kh". This is linguistically invalid. `nk` is *not* a standard ASCII digraph for the velar nasal (only `ng` is). Kawi words can contain anusvara + kha (`n` + `kʱ`, e.g., `śaṅkha` written in ASCII as `sankha`). G2P handles this correctly, but the tokenizer wrongly flags it.

## 4. Canonical Representation Findings
* **Immutability:** Confirmed. Canonical data is passed as standard Python strings in lists, completely separated from acoustic policy.
* **Separation of Concerns:** No eSpeak-specific fallback notations leak into the canonical array.
* **Distinctions:** Vowel length (`aː`), aspirates (`dʱ`), and retroflexes (`ṭ`) are explicitly maintained in G2P output.

## 5. Profile A Findings
* **Evidence-Backed Mergers:** `bʱ`, `dʱ`, `gʱ`, `pʰ` correctly map to their unaspirated counterparts.
* **Evidence-Backed Sibilants:** `ś` and `ṣ` correctly map to `s`.
* **Policy Enforcement (The P5-002A Boundary):** Unsupported aspirates (`tʰ`, `kʰ`, `cʰ`, `ṭʰ`, `ɟʱ`, `ḍʱ`) correctly fall through to `PRESERVED` or `PROVISIONAL_RECONSTRUCTION`. They are **not** silently merged. This perfectly obeys the "do not expand Profile A without evidence" directive.
* **Unresolved Vowel Length:** The P6-003R engineering fallback correctly strips the `ː` duration marker from `aː`, `iː`, `uː`, `əː`.
* **Long Vocalic Liquids (`r̩ː`, `l̩ː`):** These do *not* have their duration stripped in Profile A, because the fallback logic only targeted standard vowels. Since we lack explicit evidence that spoken Old Javanese shortened these ultra-rare Sanskrit loans, leaving them as `PROVISIONAL_RECONSTRUCTION` `r̩ː` is completely aligned with project policy.

## 6. Profile B Findings
* **Integrity:** Validated. Profile B maps exactly to the V1 legacy `_PRESERVED_MAP` and `_PROVISIONAL_MAP`.
* **Leakage:** Zero leakage from Profile A. Profile B successfully preserves all macrons and aspirates.

## 7. AcousticMapper/eSpeak Findings
* **Backend Adaptation:** The mapper safely translates target strings to eSpeak IPA.
* **Liquid Translation:** Profile A target `rə` (from `r̩`) concatenates into the final backend string smoothly.
* **Determinism:** Output is 100% deterministic and contains no dynamic heuristics.

## 8. Test Coverage Gaps
1. **Profile A Policy Boundaries:** Missing assertions that unsupported aspirates (`kʰ`) and long vocalic liquids (`r̩ː`) survive Profile A merging.
2. **G2P Uppercase parsing:** Missing regression test confirming that `Sĕkar` parses exactly as `sĕkar`.
3. **Tokenizer False Alarms:** Need a test proving `sankha` does not trigger an `UNRESOLVED` ambiguity flag.
4. **Boundary markers:** Missing test asserting that explicit hyphens (`sang-hyang`) correctly bypass ambiguity logic.

## 9. Adversarial Test Matrix
A high-value conceptual matrix to add to the test suite:
* **ASCII Ambiguity:** `sanghyang` (ASCII) vs `saṅhyaṅ` (Canonical) vs `sang-hyang` (Hyphenated).
* **Valid Aspirate Sequences:** `sankha` (testing `kʰ` preservation and tokenizer).
* **Capitalized Digraphs + Macrons:** `Bhaṭāra` (capitalization, digraph, retroflex, macron).
* **Vocalic Liquid Length:** `kṛta` vs `kṝta`.
* **Noise:** `123-awighnam!` (Punctuation and numbers mixed with text).

## 10. Documentation Drift Findings
* **DOCS DRIFT:** `src/normalization/tokenizer.py` docstring and inline comments falsely define `nk` as an ASCII velar nasal digraph.
* **ACCURATE:** `docs/P3_003A_G2P_SPEC.md` correctly contains the P5-002 V2 Policy Amendment warning.

## 11. Prioritized Fixes
* **P0:** None. The engine is linguistically safe and structurally sound.
* **P1:** Remove the false `nkh` ambiguity check and documentation from `src/normalization/tokenizer.py`.
* **P2:** Add the Adversarial Test Matrix (Uppercase, Profile A fall-through assertions, `sankha` boundary) to the test suite.
* **P3:** None.

## 12. Items that should NOT be changed
* **DO NOT** add `tʰ`, `kʰ`, `cʰ`, `ṭʰ`, `ɟʱ`, `ḍʱ` to Profile A mergers. Leave them distinct until a cited source proves they merged.
* **DO NOT** strip duration from `r̩ː`. Leave it until cited.
* **DO NOT** force the normalizer to lowercase text. Information preservation requires deferring case-folding to the G2P engine.
* **DO NOT** "fix" `sanghyang` in G2P beyond the current `ngh` fallback. Resolving it perfectly requires a dictionary, which violates the deterministic scope.

## 13. Recommended Implementation Order
1. **Batch 1 (Immediate):** Execute P1 fix (Remove `nkh` false alarm from tokenizer).
2. **Batch 2 (Immediate):** Execute P2 tests (Implement Adversarial Test Matrix).

## 14. Open Evidence Questions
* **Q1:** Did spoken Old Javanese merge the unsupported voiceless aspirates (`cʰ`, `kʰ`, `tʰ`) the same way it merged voiced ones? *(Current Policy: Assume no, keep distinct until proven).*
* **Q2:** Did spoken Old Javanese shorten `ṝ` (`r̩ː`)? *(Current Policy: Assume no, keep distinct until proven).*
