# Project Specification: Kawi-TTS

## 1. Executive Summary
Kawi-TTS is a research-grade speech synthesis initiative designed to accurately model and generate speech for Old Javanese (*Basa Kawi*). The system prioritizes linguistic rigor, phonetic precision, and modular design.

## 2. Goals & Non-Goals

### In-Scope Goals
- **Linguistic Grounding:** Accurate reconstruction of Old Javanese pronunciation based on documented historical phonology, comparative Austronesian linguistics, and classical Indological contact studies.
- **Robust Text Normalization:** Clean handling of standard academic Romanization schemes (e.g., Zoetmulder's *Old Javanese-English Dictionary* conventions, standard diacritics).
- **Rule-Driven G2P Engine:** Explicit, verifiable grapheme-to-phoneme conversion with IPA output.
- **Strict Data Quality Gates:** Standardized audio/text dataset manifest schemas and rigorous acoustic quality metrics before training.
- **Modular Pipeline:** Decoupled modules allowing independent verification of text processing, G2P, dataset pipelines, and acoustic/vocoder synthesis.

### Explicit Non-Goals (Initial Phase)
- Rendering or OCR of historical Kawi Brahmic scripts (focus is squarely on spoken language and phonetic reconstruction from Romanized input).
- Immediate training of heavyweight neural TTS models without audited datasets and verified G2P.
- Conflating traditional Balinese/Javanese poetic singing/chanting (*mabasan*/*tembang*) melodies with baseline spoken phonology without explicit acoustic separation.

## 3. Linguistic Requirements

### 3.1 Input Orthography
The system will accept standard Romanized Old Javanese text using unicode diacritics:
- **Vowels:** *a*, *ā*, *i*, *ī*, *u*, *ū*, *e*, *ai*, *o*, *au*, *ö*, *ě* (pepet).
- **Consonants:**
  - Velars: *k*, *kh*, *g*, *gh*, *ṅ*
  - Palatals: *c*, *ch*, *j*, *jh*, *ñ*
  - Retroflex: *ṭ*, *ṭh*, *ḍ*, *ḍh*, *ṇ*
  - Dentals: *t*, *th*, *d*, *dh*, *n*
  - Labials: *p*, *ph*, *b*, *bh*, *m*
  - Semivowels & Liquids: *y*, *r*, *l*, *w*
  - Sibilants & Aspirates: *ś* (palatal), *ṣ* (retroflex), *s* (dental), *h*

### 3.2 Distinctions to Preserve
- Distinguish native Austronesian phonology from Sanskrit loanword aspirate/retroflex series.
- Explicit tagging of uncertain/hypothetical phonetic values vs. firmly established phonemes.

## 4. Quality & Verification Standards
- Every G2P rule must be backed by a cited academic source or documented working hypothesis.
- Normalization and G2P modules must have >=90% test coverage with explicit test suites for tricky loanwords and morphological boundary cases.
