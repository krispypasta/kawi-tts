# Kawi-TTS Neural Data Acquisition Masterplan

**Status:** Research Sprint Completed (Phase 1-12)
**Objective:** Determine the most realistic path to acquire a legitimate training corpus for a future neural acoustic model, adhering strictly to Kawi-TTS's evidence-first principles and zero-budget constraint.

---

## 1. Current Blocker
The deterministic engine is FROZEN at v1.1.1. The acoustic mapping architecture is complete. The true blocker for Neural TTS is **DATA**. Specifically, the absence of a legal, phonetically defensible Kawi recording corpus and a qualified speaker to produce it.

## 2. Existing Evidence & Invariants
We have established the following non-negotiable invariants (Profile A):
- **Deterministic Pronunciation is Authority:** Neural TTS is only a downstream acoustic realization.
- **Preserved Distinctions:** Dental (`t`, `d`) vs. Retroflex (`ṭ`, `ḍ`); Schwa (`ə`) stability; Consonant clusters without epenthesis.
- **Failures to Avoid:** Western models collapse retroflexes to alveolars and swallow the schwa.

## 3. Speaker / Collaboration Landscape
[EVIDENCE / INFERENCE]
Finding a qualified Kawi speaker is highly specialized. Realistic pathways include:
1. **Universitas Udayana (Bali) - Program Studi Sastra Jawa Kuno:** High zero-budget feasibility. The only S1 program globally dedicated to Old Javanese. Students/faculty deeply understand Kawi phonology and prosody.
2. **Traditional Mabasan Communities (Bali):** High zero-budget feasibility for cultural preservation, but *low phonetic relevance* due to Balinese phonological filtering (merging of Kawi retroflexes into dentals).
3. **Universitas Gadjah Mada (UGM) & Universitas Indonesia (UI) (Sastra Nusantara):** Moderate-high feasibility. Strong academic focus on Old Javanese philology.
4. **Western Academia (Leiden, ANU):** No audio potential, but high feasibility for verifying phoneme inventories via email consultation.

## 4. Existing Dataset Landscape
[EVIDENCE]
There is **ZERO** existing CC0/CC-BY Old Javanese audio suitable for direct ML training.
- **Archival (Leiden/KITLV):** Early 20th-century cylinders. Restricted licensing, poor acoustic quality.
- **Traditional Recitation (YouTube/Spotify):** All Rights Reserved. Scraping violates copyright. Acoustically flawed (Balinese filtering).
- **Academic Readings (Internet Archive):** Fair Use educational copyright. Unsafe for open ML training.
- **Modern Javanese (Common Voice/OpenSLR):** CC0/CC-BY. Highly useful for *acoustic transfer learning* (as modern Javanese preserves the `/t/` vs `/ṭ/` distinction), but contains no Old Javanese text.

## 5. Licensing & Provenance Analysis
[EVIDENCE]
Any custom Kawi corpus must be explicitly released under **CC0** or **CC-BY 4.0** (or MIT/Apache 2.0). 
- **NC (Non-Commercial) or SA (Share-Alike)** licenses are strictly prohibited, as they poison the TTS repository's open-weights distribution model.
- **Provenance:** The identity, academic qualifications, and explicit ML-training consent of the speaker must be documented in a signed release form.

## 6. Speaker Qualification Standard
[PROJECT ASSUMPTION / ENGINEERING CONVENTION]
A "qualified speaker" for Kawi-TTS is not a "native speaker" (which does not exist), but a scholar/practitioner demonstrating:
- **Kawi Linguistic Competence:** Familiarity with Kakawin meter and text boundaries.
- **Phonetic Competence:** Ability to consistently produce the dental/retroflex contrast (`t`/`ṭ`, `d`/`ḍ`, `n`/`ṇ`) and schwa (`ě`).
- **Authorization:** Only academic consensus or strict adherence to the deterministic G2P rules can authorize pronunciation. The speaker must read the script *exactly* as normalized, without improvising modern Javanese/Balinese pronunciation habits.

## 7. Zero-Budget Pathways
[INFERENCE]
The most realistic zero-budget path is an **Academic Barter**:
- Collaborate with Universitas Udayana or UGM.
- Offer co-authorship on a digital humanities paper, or provide open-source tools/internship credits (Kampus Merdeka).
- In exchange, students/faculty curate the text, validate the pronunciation, and record the audio using their own institutional or personal dynamic microphones.

## 8. Minimum Corpus Design (Experimental)
[ENGINEERING CONVENTION]
- **Size:** 30 to 45 minutes of clean speech.
- **Goal:** Fine-tuning an existing Modern Javanese or multilingual Piper model.
- **Content:** Highly dense sentences targeting minimal pairs, schwa variations, and complex clusters.
- **Use Case:** Validates G2P mapping and basic acoustic space, though prosody may remain robotic.

## 9. Preferred Corpus Design (V1 Model)
[ENGINEERING CONVENTION]
- **Size:** 2 to 5 hours (~1,500 to 3,500 utterances).
- **Goal:** Training a robust, stable single-speaker VITS/Piper model.
- **Content:** 60% phonetically balanced sentences from Kakawin texts, 20% minimal pair carrier phrases, 20% isolated complex words.

## 10. Recording Protocol
[ENGINEERING CONVENTION]
- **Hardware:** Dynamic USB/XLR mic (e.g., Q2U) heavily preferred over condensers to reject untreated room noise.
- **Environment:** Heavy acoustic dampening (closet studio).
- **Session:** Strict 60-minute maximum to prevent vocal fatigue and phonetic sloppiness.
- **Format:** 48kHz, 24-bit mono, WAV.

## 11. Annotation & Alignment Protocol
[ENGINEERING CONVENTION]
- **Segmentation:** Split on silence >500ms.
- **Alignment:** Montreal Forced Aligner (MFA).
- **Dictionary:** Must use a strict G2P dictionary generated directly by Kawi-TTS v1.1.1. No manual pronunciation hacking.

## 12. QA Protocol
[PROJECT ASSUMPTION]
- **Acoustic:** Reject clipping or SNR < 30dB.
- **Phonetic:** Listeners must audit 10% of the corpus. 
- **Spectrogram Verification:** Use Praat to verify retroflexion on ambiguous samples (look for lowered F3 merging with F2).
- **Discard Policy:** If a speaker mispronounces a retroflex as a dental, the sample must be **discarded**. Do not map the transcription to the mistake.

## 13. Training-Eligibility Gate
[PROJECT ASSUMPTION]
A corpus moves from RAW to TRAINING-ELIGIBLE only when:
1. Audio is segmented and perfectly aligned.
2. The exact v1.1.1 deterministic IPA arrays are used as metadata.
3. Explicit CC0/CC-BY licensing is signed.
4. QA confirms retroflex/schwa preservation.

## 14. Future Neural Model Requirements
[ENGINEERING CONVENTION]
The future model (e.g., Piper/VITS) must support:
- **Deterministic Bypass:** Ability to inject `[[ipa]]` directly, bypassing internal text-to-phoneme guessing.
- **Custom Phonemes:** The ID map must exactly match Kawi-TTS's inventory.
- **Zero-Budget Compute:** Must be trainable on Google Colab T4 and inferable faster than real-time on a standard CPU.

## 15. Decision Tree
[PROJECT ASSUMPTION]
1. **IF** an academic partnership (Udayana/UGM) is secured:
   → Initiate recording workflow (Minimum Corpus).
2. **ELSE IF** an independent scholar volunteers:
   → Validate recording environment; initiate recording workflow.
3. **ELSE IF** Modern Javanese CC0 data (Common Voice) is available:
   → Determine if it can be used for acoustic pre-training (YES, but cannot synthesize actual Old Javanese words without a Kawi fine-tuning dataset).
4. **ELSE:**
   → Remain BLOCKED. Do not fabricate data.

## 16. GO / CONDITIONAL GO / NO-GO States
- **Current State:** **NO-GO.** (No Kawi audio, no identified speaker).
- **Conditional GO:** Academic partnership established, but recording pending.
- **GO:** 45+ minutes of CC0/CC-BY Kawi audio acquired, QA passed, MFA aligned.

## 17. Concrete Next Actions
**NEXT ACTION 1: Academic Outreach**
- **Objective:** Secure a zero-budget collaboration for corpus recording.
- **Owner/role:** Project Maintainer.
- **Prerequisite:** Draft a project prospectus highlighting open-source/digital humanities benefits.
- **Expected evidence:** Email threads with Universitas Udayana (Sastra Jawa Kuno) or UGM.
- **Completion condition:** A signed agreement or explicit refusal.

**NEXT ACTION 2: Minimal Pair Script Generation**
- **Objective:** Create the 30-minute recording script.
- **Owner/role:** Engineering/Linguistics AI.
- **Prerequisite:** None (can be done while waiting for speaker).
- **Expected evidence:** A `.csv` file containing text, canonical IPA, and Profile A IPA.
- **Completion condition:** Script covers all Profile A phonemes and Kawi clusters.

## 18. Unresolved Questions
[UNCERTAINTY]
- Will Indonesian academics accept a zero-budget collaboration involving open CC0 licensing?
- Can modern speakers, even scholars, maintain strict historical retroflex distinctions for 45+ minutes without slipping into modern Javanese/Indonesian habits?

## 19. Research Sources
- Leiden University Libraries / KITLV Archives
- Mozilla Common Voice / OpenSLR
- *Kakawin* / *Mabasan* community structures (Bali)
- Universitas Udayana / UGM curriculum data
- TTS corpus engineering best practices (MFA, VITS, Piper)
