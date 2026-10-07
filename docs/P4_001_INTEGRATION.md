# P4-001: End-to-End V1 Integration Test Report

**Date:** 2026-10-07
**Mode:** Engineer / Builder
**Status:** INTEGRATION TEST PASSED (P4-001 Complete)

## 1. Integration Architecture & Data Flow

The purpose of P4-001 is to formally verify the end-to-end integration contract of the Kawi-TTS V1 pipeline as a coherent, deterministic system:

```text
Raw Kawi Text Input
       ↓
[1. Normalizer]  src/normalization/normalizer.py
       ↓         → NormalizationResult (NFC, canonical chars, typographic cleanup)
[2. Tokenizer]   src/normalization/tokenizer.py
       ↓         → List[Token] (word, punctuation, boundary, elision, number, unresolved)
[3. G2P Engine]  src/g2p/engine.py
       ↓         → List[List[str]] (lossless internal phonemes per word)
[4. Mapper]      src/acoustic/mapper.py
       ↓         → AcousticMappingResult (backend IPA, provisional audit, unsupported audit)
[5. Backend]     src/acoustic/espeak_backend.py
       ↓         → SynthesisResult (deterministic CLI command, mock/real WAV output)
PipelineResult   src/acoustic/pipeline.py / src/tts
```

Integration testing focuses on the **contractual boundaries between components**, ensuring no data is dropped, corrupted, or mutated across stages.

---

## 2. Component Contracts Verified

1. **Normalization Contract:**
   - Input: Any valid Unicode string.
   - Output: `NormalizationResult` containing canonical NFC text and list of applied transformations.
   - Guarantee: Preserves source text without applying any phonological interpretations.
2. **Tokenizer Contract:**
   - Input: Normalized string.
   - Output: Ordered `List[Token]`.
   - Guarantee: 100% lossless character reconstruction (`"".join(t.text for t in tokens) == normalized_text`). Preserves character offsets (`text[t.start:t.end] == t.text`). Isolates hyphens as `TokenType.BOUNDARY` and apostrophes as `TokenType.ELISION`.
3. **G2P Engine Contract:**
   - Input: Lexical word strings.
   - Output: `List[List[str]]` containing internal phonemes.
   - Guarantee: Fully case-insensitive (handles capitalized titles like *Śrī*, *Bhaṭāra*). Greedily parses digraphs (`bh`, `dh`, `gh`, `ph`, `ṭh`, etc.) into dedicated phoneme tokens without leaking standalone `h`.
4. **Acoustic Mapper Contract:**
   - Input: `List[List[str]]` internal phonemes.
   - Output: `AcousticMappingResult`.
   - Guarantee: **Strict immutability**: never alters the caller's G2P phoneme list in-place. Maps direct phonetic equivalents with `MappingStatus.PRESERVED`. Stamps uncertain adaptations with `MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING` and attached epistemic notes.
5. **eSpeak Backend Contract:**
   - Input: Backend-compatible phoneme string.
   - Output: `SynthesisResult`.
   - Guarantee: Deterministic command generation. Fully functional dry-run mode that does not require eSpeak binary installation. Actionable error reporting (`ESpeakNotFoundError`) on non-dry-run requests when binary is absent.

---

## 3. Representative End-to-End Cases Tested

Ten integration test suites in `tests/test_integration.py` verified the following representative source citations:

| Category | Input Example | Internal Phonemes | Backend eSpeak IPA | Status Verification |
| :--- | :--- | :--- | :--- | :--- |
| **Native Root** | `sĕkar` | `['s', 'ə', 'k', 'a', 'r']` | `səkar` | All `PRESERVED` |
| **Native Root** | `wukir` | `['w', 'u', 'k', 'i', 'r']` | `wukir` | All `PRESERVED` |
| **Native Derived** | `tumutupi` | `['t', 'u', 'm', 'u', 't', 'u', 'p', 'i']` | `tumutupi` | All `PRESERVED` |
| **Native Retroflex** | `paḍaṅ` | `['p', 'a', 'ḍ', 'a', 'ŋ']` | `paɖaŋ` | All `PRESERVED` |
| **Long Vowels** | `śānti` | `['ś', 'aː', 'n', 't', 'i']` | `ʃaːnti` | All `PRESERVED` |
| **Long Vowels** | `pūjā` | `['p', 'uː', 'ɟ', 'aː']` | `puːɟaː` | All `PRESERVED` |
| **Sanskrit Aspirate** | `dharma` | `['dʱ', 'a', 'r', 'm', 'a']` | `dʱarma` | `dʱ` `PROVISIONAL` |
| **Sanskrit Aspirate** | `awighnam` | `['a', 'w', 'i', 'gʱ', 'n', 'a', 'm']` | `awigʱnam` | `gʱ` `PROVISIONAL` |
| **Sanskrit Aspirate** | `ghaṇṭā` | `['gʱ', 'a', 'ṇ', 'ṭ', 'aː']` | `gʱaɳʈaː` | `gʱ` `PROVISIONAL` |
| **Vocalic Liquid** | `kṛta` | `['k', 'r̩', 't', 'a']` | `kr̩ta` | `r̩` `PROVISIONAL` |
| **Vocalic Liquid** | `kḷpta` | `['k', 'l̩', 'p', 't', 'a']` | `kl̩pta` | `l̩` `PROVISIONAL` |
| **Reduplication** | `gilaṅ-gilaṅ` | `[['g', 'i', 'l', 'a', 'ŋ'], ['g', 'i', 'l', 'a', 'ŋ']]` | `gilaŋ gilaŋ` | Boundary split preserved |
| **Enclitic Connector** | `liṅgira'n` | `[['l', 'i', 'ŋ', 'g', 'i', 'r', 'a'], ['n']]` | `liŋgira n` | Elision isolated |
| **Elided Article** | `ri'ṅ` | `[['r', 'i'], ['ŋ']]` | `ri ŋ` | Elision isolated |
| **ASCII Ambiguity** | `sanghyang` | `[['s', 'a', 'n', 'gʱ', 'j', 'a', 'n', 'g']]` | `sangʱjang` | Flagged `UNRESOLVED` |
| **Explicit Boundary** | `sang-hyang` | `[['s', 'a', 'n', 'g'], ['h', 'j', 'a', 'n', 'g']]` | `sang hjang` | Split boundary, no false `gʱ` |
| **Canonical Form** | `saṅhyaṅ` | `[['s', 'a', 'ŋ', 'h', 'j', 'a', 'ŋ']]` | `saŋhjaŋ` | Clean canonical parse |
| **Capitalized Title** | `Śrī` | `[['ś', 'r', 'iː']]` | `ʃriː` | Case-insensitive |
| **Capitalized Deity** | `Bhaṭāra` | `[['bʱ', 'a', 'ṭ', 'aː', 'r', 'a']]` | `bʱaʈaːra` | Capitalized digraph parsed |

---

## 4. Information-Preservation Verification

The integration suite explicitly asserted non-equivalence across phonological pairs to verify that neither G2P nor Acoustic Mapper silently collapses distinctions:
- **Vowel duration:** $\text{ā} \neq \text{a}$, $\text{ī} \neq \text{i}$, $\text{ū} \neq \text{u}$.
- **Sibilants:** $\text{ś} \neq \text{s}$, $\text{ṣ} \neq \text{s}$, $\text{ś} \neq \text{ṣ}$.
- **Stops & Nasals:** $\text{ṭ} \neq \text{t}$, $\text{ḍ} \neq \text{d}$, $\text{ṇ} \neq \text{n}$.
- **Aspirates:** $\text{bh} \neq \text{b}$, $\text{dh} \neq \text{d}$, $\text{gh} \neq \text{g}$.
- **Vocalic liquids:** $\text{ṛ} \neq \text{r}$, $\text{ḷ} \neq \text{l}$.

In all cases, both the internal G2P tokens and the acoustic backend IPA strings maintain distinct representations.

---

## 5. Error Handling & Edge Cases Verified

1. **Empty / Blank Input:**
   - Input: `""`, `"   "`, `"\t\n"`.
   - Result: Handled gracefully without raising unhandled exceptions. Produces `words = []`, `g2p_phonemes = []`, `backend_phoneme_string = ""`, `command = ['espeak-ng', '-v', 'jv', '[[]]']`.
2. **Punctuation & Numbers Only:**
   - Input: `", . ! ? ||"`, `"183.2"`.
   - Result: Classified cleanly into `TokenType.PUNCTUATION` and `TokenType.NUMBER`. No false words or phonemes generated.
3. **Unsupported Characters:**
   - Input: `"kawi-x-123"`.
   - Result: Character `'x'` is parsed, detected by `AcousticMapper` as unsupported, and recorded in `unsupported_tokens` with note `"Unsupported token 'x' in acoustic mapper."` rather than crashing or mutating.
4. **Missing eSpeak Binary:**
   - Input: Non-dry-run request when binary is absent from `PATH`.
   - Result: Raises `ESpeakNotFoundError` with step-by-step installation instructions.
5. **Dry-Run Audio Emulation:**
   - Input: `dry_run=True, create_dummy_wav=True`.
   - Result: Emulates audio generation by creating a valid 44-byte RIFF/WAVE header verified by file structure tests.

---

## 6. Test Suite Status

- **Baseline Test Suite (P3-007):** 66 tests passing.
- **Integration Tests Added (P4-001):** 10 comprehensive tests in `tests/test_integration.py`.
- **Total Tests Passing:** **76 tests passing (100% pass rate, 0 errors, 0 failures)** in 0.847s.

---

## 7. Next Step

P4-001 is complete. The pipeline contract is proven end-to-end. Ready for **Task P4-002: High-throughput G2P evaluation against documented word lists from the Old Javanese Wordnet (OJW)** upon Abraham's approval.
