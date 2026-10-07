# Project State: Kawi-TTS

## 1. Current Project Goal
Build a research-grade Text-to-Speech (TTS) system focused on Old Javanese (*Basa Kawi*) pronunciation. The initial focus is on the language phonology, phonetic inventory, text normalization, and grapheme-to-phoneme (G2P) conversion based on documented linguistic evidence, rather than Kawi script rendering or premature acoustic model training.

## 2. Current Phase
**Phase 0: Project Inception & Research Scaffolding**
- Establishing project architecture and repository structure.
- Setting up documentation standards and research tracking.
- Defining strict boundaries between linguistic facts, working hypotheses, and engineering components.

## 3. What Has Been Verified
- Git repository setup and remote access authenticated.
- Basic repository structure and modular boundaries defined.
- Separation of concerns established across normalization, G2P, data processing, and TTS modeling.

## 4. What Is Still Unknown
- **Phonological Consensus:** Exact phonetic values for certain Old Javanese consonants in native Austronesian roots vs. Sanskrit loanwords (e.g., retroflex vs. dental series, aspirated stops in classical vs. colloquial pronunciation).
- **Vowel Length & Stress:** The exact realization of vowel length (e.g., *ā*, *ī*, *ū*) and meter (*kakawin* prosody/guru-laghu) in spoken vs. chanted contexts.
- **Dataset Availability:** Quality, licensing, phonetic accuracy, and acoustic characteristics of any existing Old Javanese / Balinese-Kawi recitation recordings.
- **Phoneme Inventory & G2P Strategy:** Whether rule-based finite-state transducers (FST) / regex mapping is sufficient for Romanized transliteration schemes (e.g., standard Zoetmulder/OJED transliteration) before machine-learning G2P is needed.

## 5. Current Blockers
- None at this stage. (Linguistic literature survey and corpus audit need to be initiated).

## 6. Next Milestones
1. **Milestone 1: Linguistic Survey & Phoneme Inventory Definition**
   - Survey authoritative Old Javanese grammars and dictionaries (Zoetmulder, Uhlenbeck, Teeuw).
   - Define canonical phoneme inventory and IPA mapping specification for Romanized Kawi.
2. **Milestone 2: Romanized Text Normalization & Rule-Based G2P Baseline**
   - Implement unicode normalization for diacritics (macrons, dots below/above).
   - Implement deterministic G2P baseline with clear test coverage.
3. **Milestone 3: Dataset Audit & Corpus Feasibility Assessment**
   - Audit available Kawi corpora (text and potential audio/recitation sources).
   - Define data acceptance criteria and validation manifests.
