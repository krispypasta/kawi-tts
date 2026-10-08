# Epistemic Distinction of Roles in Kawi-TTS Data Acquisition

**Date:** 2026-10-08

## 1. The Epistemic Problem

The Kawi-TTS project faces a data acquisition bottleneck for neural TTS training: the lack of a legal, phonetically defensible Kawi recording corpus and a qualified speaker to produce it. 

Given that Kawi has no native speakers, any acoustic realization is necessarily a reconstruction. This raises an epistemic question regarding the authority of the spoken data: *Who authorizes the correctness of the pronunciation during recording?* 

This document breaks down the process into three distinct roles to determine whether a non-specialist project member can legitimately record the acoustic data.

## 2. Role Distinctions

The production of an acoustic corpus involves three distinct steps, each with different epistemic responsibilities:

### Role 1: The Scholar (Upstream Authority)
* **Function:** Determines and reconstructs historical pronunciation.
* **Epistemic Burden:** High. Must rely on comparative linguistics, epigraphy, and cited scholarly sources (as documented in `RESEARCH_LOG.md`).
* **Output:** The deterministic V1.1.1 G2P frontend and Profile A. 
* **Authority:** Defines *what* sounds must be produced and *when*, generating an unambiguous phonetic script.

### Role 2: The Reader (Midstream Execution)
* **Function:** Reads the supplied pronunciation script aloud.
* **Epistemic Burden:** Zero. The reader is not required—and specifically not permitted—to make linguistic decisions about *what* the correct historical pronunciation should be. 
* **Output:** The physical vocalization of the provided phonetic targets.
* **Authority:** The reader has no scholarly authority. Their responsibility is strictly mechanical compliance with the phonetic prompt. They must possess the physiological control to hit target phonemes (e.g., maintaining the retroflex /ʈ/ vs dental /t/ distinction) without slipping into L1 (modern Javanese/Indonesian) pronunciation habits.

### Role 3: The Technician (Downstream Recording)
* **Function:** Captures the acoustic data.
* **Epistemic Burden:** Zero.
* **Output:** High-fidelity audio files (WAV) paired with the source transcriptions.
* **Authority:** purely technical (managing noise floors, mic placement, and signal clarity).

## 3. Conclusion and Policy Determination

**Determination: Yes, a non-specialist project member CAN legitimately occupy the downstream execution roles (Reader and Technician).**

Because the project enforces a strict boundary between scholarly evidence (upstream) and acoustic execution (downstream), the epistemic burden of "correctness" rests entirely on the deterministic G2P engine and Profile A. 

The authority of the pronunciation is encoded in the *script*, not in the *speaker*. 

Therefore, a non-specialist project member can serve as the corpus speaker provided they meet the following **execution criteria**:
1. **Phonetic Compliance:** They can be trained to reliably produce the specific phonetic targets (especially non-native distinctions like retroflexes) demanded by the script.
2. **Deterministic Submission:** They read the script *exactly* as generated, without improvising or substituting their own intuition for what Kawi "should" sound like.
3. **Rigorous QA:** Any failure to execute the script mechanically (e.g., merging dentals and retroflexes due to vocal fatigue) results in the discard of the sample, rather than adjusting the transcript to match the error.

By cleanly separating the *decision* of pronunciation from the *execution* of pronunciation, the project preserves its scholarly integrity while unlocking a practical path to corpus generation.