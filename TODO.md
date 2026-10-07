# Actionable Tasks (TODO)

## 1. Linguistic Research & Documentation
- [ ] Compile bibliography of Old Javanese phonology and grammar (Zoetmulder & Robson, Uhlenbeck, Teeuw, Hunter).
- [ ] Document attested phonetic inventory (consonants, vowels, diphthongs) in `docs/RESEARCH_LOG.md`.
- [ ] Document treatment of Sanskrit loanwords vs. native Austronesian vocabulary in Kawi phonology.
- [ ] Specify standard Romanization schemes (e.g., ISO 15919 / OJED standard diacritics: ā, ī, ū, ö, ě, ḍ, ṭ, ṇ, ś, ṣ, ñ, ṅ).
- [ ] Draft phoneme-to-IPA mapping document in `docs/`.

## 2. Text Normalization (`src/normalization/`)
- [ ] Implement Unicode normalization (NFC/NFD standardization) for Romanized Kawi diacritics.
- [ ] Implement punctuation and whitespace normalization.
- [ ] Implement handling for hyphenation, sandhi markers, and elision in Romanized texts.
- [ ] Add unit tests for text normalization with edge cases (macrons, underdots, breves).

## 3. Grapheme-to-Phoneme (G2P) (`src/g2p/`)
- [ ] Define data structures for phonemes and phonetic features (IPA, X-SAMPA, or ARPABET-style).
- [ ] Implement deterministic rule-based G2P converter for standard Romanized Kawi.
- [ ] Implement syllable boundary parsing / syllabification rules.
- [ ] Add unit tests verifying G2P mappings against curated reference word lists from academic dictionaries.

## 4. Dataset Auditing & Corpus Tooling (`data/`, `src/`)
- [ ] Audit publicly available Old Javanese textual corpora (e.g., SEALang Old Javanese, OJED, digitized manuscripts).
- [ ] Assess available audio sources (e.g., traditional Balinese/Javanese *mabasan* / *kakawin* chanting vs. spoken recitation) and document acoustic/phonetic suitability.
- [ ] Define manifest schema (JSON/CSV) for training/evaluation pairs (audio path, raw text, normalized text, phoneme sequence, speaker ID, duration).
- [ ] Implement dataset validation scripts (audio sample rate, SNR, clipping, phoneme coverage verification).

## 5. Architecture & Testing
- [ ] Set up testing framework and CI checks (pytest, linting).
- [ ] Define TTS acoustic model interface abstractions in `src/tts/` without binding to a premature model implementation.
