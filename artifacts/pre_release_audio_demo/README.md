# Pre-Release Audio Demonstration: Human Listening Pack

This directory contains actual eSpeak-ng generated WAV files using the frozen `kawi-tts` deterministic core engine (v1.0.0 / pre-release).

## Purpose
The purpose of this listening pack is to verify that the **actual audio** corresponds to the **documented implementation behavior** of the engine. Do not judge the audio against commercial TTS naturalness. The primary question is: *Does the engine produce the phonemic contrasts and policies dictated by Profile A and Profile B?*

## Manifest
A machine-readable `manifest.json` is provided in this directory with the full normalization trace, canonical phonemes, target phonemes, and final eSpeak backend string for every sample.

## Sample Explanations & Listening Notes

### 1. `sĕkar`
* **Input:** `sĕkar`
* **Profiles:** A and B (No difference)
* **Expected Transformation:** The schwa `ĕ` maps to canonical `ə`.
* **Listening Note:** Listen for the schwa sound in the first syllable. Both profiles should sound identical (`səkar`).

### 2. `BHAṬĀRA`
* **Input:** `BHAṬĀRA`
* **Profile A:** `b-a-ṭ-a-r-a` (Backend: `baʈara`)
* **Profile B:** `bʱ-a-ṭ-aː-r-a` (Backend: `bʱaʈaːra`)
* **Expected Transformation:** 
  * Profile A merges the voiced aspirate `bh` into `b` and strips the long vowel `ā` to `a`.
  * Profile B preserves the voiced aspirate `bʱ` and the long vowel `aː`.
* **Listening Note:** Compare the two files. Profile B should have a distinctly aspirated "b" and a longer second "a" sound.

### 3. `śānti`
* **Input:** `śānti`
* **Profile A:** `s-a-n-t-i` (Backend: `santi`)
* **Profile B:** `ś-aː-n-t-i` (Backend: `ʃaːnti`)
* **Expected Transformation:**
  * Profile A merges the palatal sibilant `ś` into plain `s` and strips the long vowel `ā` to `a`.
  * Profile B preserves the palatal sibilant `ś` (mapped to backend `ʃ`) and the long vowel `aː`.
* **Listening Note:** Profile B should begin with an "sh" sound and have a longer "a". Profile A should sound like "santi".

### 4. `kṝta`
* **Input:** `kṝta`
* **Profiles:** A and B (No difference)
* **Expected Transformation:** The long vocalic r `ṝ` maps to canonical `r̩ː` in both profiles. Profile A currently does not strip the length from `ṝ` (as it only targets specific long vowels).
* **Listening Note:** Listen for the syllabic "r" sound. Confirm whether the backend actually produces a distinct syllabic liquid or if it struggles to render `r̩ː`.

### 5. `sankha`
* **Input:** `sankha`
* **Profiles:** A and B (No difference)
* **Expected Transformation:** The digraph `kh` is greedily matched as `kʰ`. The `n` remains plain `n`. Output is `s-a-n-kʰ-a`.
* **Listening Note:** Listen to verify the sequence is treated as "n" + aspirated "k", rather than an ambiguous "nk" + "h". (Backend: `sankʰa`).

### 6. `sang-hyang`
* **Input:** `sang-hyang`
* **Profiles:** A and B (No difference)
* **Expected Transformation (Important Discrepancy Observation):** 
  * The explicit hyphen safely breaks the `gh` aspirate digraph rule.
  * *Discrepancy:* The engine currently processes ASCII `ng` strictly as `n` + `g`, **not** as the velar nasal `ŋ`. Therefore, the output is `s-a-n-g | h-j-a-n-g` (Backend: `sang hjang`).
  * If a velar nasal is desired, the user must strictly input `saṅ-hyaṅ` using the canonical `ṅ` character.
* **Listening Note:** Listen for a hard "g" sound after "n" before the "h" (`s-a-n-g-h`).

### 7. `sanghyang`
* **Input:** `sanghyang`
* **Profiles:** None
* **Expected Transformation:** EXPECTED BLOCKED.
* **Reason:** The tokenizer detects the `ngh` sequence as a true ambiguity (is it `n`+`gh` or `ng`+`h`?). Because no explicit boundary is provided and `ṅ` was not used, it blocks processing to prevent silent data corruption.
* **Listening Note:** No audio generated. This strictly enforces the "fail-fast on ambiguity" rule.

## Release Gate Status: AUDIO-DEMO-GO
The actual backend execution cleanly mirrors the documented behavior of the `kawi-tts` Python deterministic codebase. The eSpeak API boundary strictly adheres to the provided phonemes.

**Note to Project Owner:** 
There is a documented discrepancy in earlier architectural discussions regarding ASCII `ng`. The actual frozen code maps `ng` to `n-g`, reserving `ŋ` exclusively for explicit `ṅ` input. This matches the regression matrix (`wong` -> `w-o-n-g`). If this is working as intended for V1, we remain a GO.