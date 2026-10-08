# Kawi-TTS Project Speaker Data Acquisition Feasibility

**Status:** Feasibility Audit Completed
**Objective:** Determine if a non-specialist project member can be trained to serve as the controlled pronunciation speaker for the Kawi-TTS neural corpus without violating the project's evidence-first principles.

---

## 1. Executive Summary
This audit confirms that an internal project member **can** legitimately produce the foundational acoustic training corpus, provided the process strictly separates *epistemic authority* from *mechanical acoustic execution*. The approach (Model B) is highly practical for zero-budget development. However, the speaker must pass an objective "Blind Acoustic Gate" overseen by an external reviewer before any data is considered training-eligible.

## 2. Speaker Role Definitions
We must distinctly separate the following roles:
- **A. Historical Pronunciation Authority:** (Held by the v1.1.1 Deterministic Engine & Profile A).
- **B. Kawi Philologist:** (Not required for speech execution).
- **D. Controlled Pronunciation Performer:** Executes the specified phonemes exactly as written.
- **E. Recording Speaker:** Operates the microphone and ensures acoustic consistency.

The project member only needs to fulfill roles **D** and **E**. They carry zero epistemic burden for historical correctness.

## 3. Required Knowledge
### MUST KNOW
- Deterministic Profile A representation (canonical IPA).
- Articulatory mechanics of the dental/retroflex contrast (`t`/`ṭ`, `d`/`ḍ`, `n`/`ṇ`).
- Consistent production of schwa (`ə`).
- Execution of consonant clusters *without* vowel epenthesis.

### SHOULD KNOW
- Syllable boundaries and basic Kawi transliteration conventions.
- Operation of spectrogram software (Praat) for self-correction.

### NOT REQUIRED
- Kawi grammar, syntax, or vocabulary translation.
- Manuscript reading/philology.
- Knowledge of modern Javanese or Balinese performance traditions.

## 4. Learning Path for Controlled Pronunciation
[EVIDENCE: Child Agent 1]
Adult phonetic acquisition of non-native contrasts (like retroflexes) cannot rely on listening alone. The path must include:
1. **Explicit Articulatory Cues:** Mapping tongue tip elevation and dorsum lowering.
2. **Visual Biofeedback:** Using sagittal diagrams and spectrograms to see acoustic targets (e.g., lowered F3 for retroflexes).
3. **Motor Drills:** Non-speech oral motor exercises to build articulatory muscle memory.
4. **Cold Listen-Backs:** Bypassing native-language categorical perception by listening to self-recordings hours later.

## 5. Self-Training Feasibility
Self-training is feasible **if and only if** objective acoustic tools (spectrograms) are used. 
- **Epenthesis Suppression:** Adults default to inserting schwa between clusters. This must be monitored via spectrograms (checking for the absence of periodic F2/F3 structures between consonants) rather than relying on the speaker's own hearing.

## 6. Certification / QA Gate
[EVIDENCE: Child Agent 2]
Before any training data is accepted, the speaker must pass a strict quality-control gate:
1. **Baseline Creation:** Record isolated minimal pairs to establish an acoustic template.
2. **Blind Acoustic Gate:** An external reviewer is given isolated audio snippets *without* the script. They must correctly identify the phoneme. If they cannot identify it blindly, the execution fails.
3. **Forced Alignment Strictness:** The corpus must be processed by a GMM-HMM aligner (like Montreal Forced Aligner). If phonetic boundaries deviate from expected temporal norms, the take is discarded.

## 7. External Scholarly Validation
This architecture cleanly separates *competence* from *authorization*.
The project member performs the bulk recording. The external scholar performs periodic **Blind Transcription Audits**. This eliminates the need for the scholar to spend 40 hours in a recording booth, drastically reducing collaboration friction and cost while maintaining scientific defensibility.

## 8. Corpus Design for a Non-Specialist
A non-specialist cannot reliably sight-read complex historical *Kakawin* passages without cognitive overload causing phonetic drift.
- **Design:** The 30-45 minute pilot corpus must consist of short, phonemically balanced controlled sentences, isolated difficult words, and minimal pairs. 
- **Script:** The speaker reads from the Canonical IPA / Profile A output, *not* the raw Kawi text, to prevent guessing.

## 9. Meaning / Grammar Requirement
**Does the speaker need to understand the meaning? NO.**
For Kawi, true historical prosody is permanently lost. Attempting to inject "natural" prosody based on meaning risks bleeding modern Javanese/Indonesian intonation patterns into the data. A mechanical, highly controlled, and consistent reading style is actually *preferable* for the baseline acoustic model to ensure phonetic clarity.

## 10. Self-Training Risks
- **Risk:** Unnoticed Cluster Epenthesis. **Mitigation:** Spectrogram validation.
- **Risk:** Retroflex Drift (reverting to dentals). **Mitigation:** Blind external review; strict 60-90 minute recording session limits to prevent articulatory fatigue.
- **Risk:** Modern L1 Interference. **Mitigation:** Rely entirely on the deterministic G2P output.

## 11. Model A (External Scholar) vs. Model B (Trained Project Member)
- **Model A:** Highly defensible, but exceptionally high friction, expensive, difficult to schedule, and vulnerable to the scholar accidentally applying modern performance habits rather than strict reconstruction.
- **Model B:** Zero-budget, infinitely scalable, highly iterative, strictly controllable. 
- **Winner:** Model B, provided the Epistemic Boundary and Blind Gates are strictly enforced.

## 12. Minimum Viable Speaker Path
- **Stage 1:** Phoneme Inventory & Motor Drills.
- **Stage 2:** Praat Self-Recording & Spectrogram Validation.
- **Stage 3:** The Blind Pronunciation Gate (External Reviewer Audit).
- **Stage 4:** Record 30-45 minute Pilot Corpus.
- **Stage 5:** Montreal Forced Alignment (MFA) temporal filtering.
- **Stage 6:** Training-Eligible Data.

## 13. Future Training Implications
A 30-45 minute corpus generated by the project speaker is strictly **DATA USABLE FOR** an experimental LoRA/transfer-learning acoustic adaptation to verify architectural viability. It is **NOT SUFFICIENT FOR** a robust, V1 production voice. If the pilot succeeds, the same speaker will proceed to record the 2-5 hour V1 corpus.

## 14. Important Epistemic Boundary
All resulting datasets and models must carry the exact label:
*"Speech recordings produced by a trained project speaker following the project's reconstructed pronunciation specification."*
They must never be labeled as "authentic historical Kawi speech."

## 15. Decision: CONDITIONAL GO
The project member data acquisition strategy is **APPROVED**, conditionally gated by the passing of the external Blind Acoustic Check.

## 16. Concrete Next Actions
1. Compile the phonetic drill script (Minimal pairs for `ṭ`/`t`, `ḍ`/`d`, and clusters).
2. Project member begins articulatory motor drills and Praat self-monitoring.
3. Design the exact Blind Acoustic Gate protocol for the external reviewer.
