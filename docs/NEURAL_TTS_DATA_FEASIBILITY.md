# Kawi-TTS Neural Data Feasibility Report

**MODE:** RESEARCH / FEASIBILITY ONLY (NO IMPLEMENTATION)
**OBJECTIVE:** Determine if a responsible zero-budget path exists to satisfy Stage 1 (Data Readiness).

---

## 1. Stage 1 Blockers (from Roadmap)
*   **Clear Provenance & Consent:** Data origin must be known and consented.
*   **Licensing:** Open-source compatible (CC0, CC-BY, MIT).
*   **Phoneme Coverage:** The dataset/model must cover the Kawi phoneme inventory.
*   **Alignment:** Accurate phoneme-to-audio timestamps/mechanism.

## 2. Current Status of Each Blocker
*   **Clear Provenance & Consent:** **SATISFIED** (for Indonesian/Javanese proxy data, e.g., Mozilla CV). **UNSATISFIED** (for actual Kawi data).
*   **Licensing:** **SATISFIED** (CC0 / CC-BY-SA 4.0 proxy datasets exist).
*   **Phoneme Coverage:** **UNSATISFIED** (Critical historical Kawi phonemes are missing from all candidate open datasets).
*   **Alignment:** **SATISFIED** (Piper/VITS forced alignment is technically sufficient).

## 3. Candidate Datasets
*   **Mozilla Common Voice Scripted Speech 27.0 (Indonesian)**
    *   *Language:* Indonesian (`id`)
    *   *License:* CC0
    *   *Provenance:* Crowd-sourced, explicit consent for open use.
*   **OpenSLR 41 (Javanese)**
    *   *Language:* Javanese (`jv-ID`)
    *   *License:* CC-BY-SA 4.0
    *   *Provenance:* Collected by Google & Gadjah Mada University. Professional/volunteer readers.
*   **INESCO Dataset**
    *   *Language:* Indonesian (Expressive)
    *   *License:* CC-BY 4.0 (via Mendeley Data)
    *   *Provenance:* Professional theater artists, curated sentences.

## 4. Candidate Pretrained Models
*   **Piper TTS**
    *   *Architecture:* VITS (End-to-End)
    *   *License:* MIT
    *   *Input Representation:* `espeak-ng` phonemes or raw text alphabet.
    *   *Cross-lingual:* Capable, but the acoustic space is locked to the phonemes seen during training.
*   **Kokoro / Kukuru-TTS**
    *   *Architecture:* StyleTTS2-derived
    *   *License:* Apache 2.0
    *   *Input Representation:* `espeak-ng` (via misaki/phonemizer).

## 5. Kawi-Specific Resources
*   **Old Javanese Speech Corpus:** None identified.
*   **Scholarly Pronunciation Recordings:** None available under open licenses suitable for ML training.
*   **Kakawin/Mabasan Recordings:** Exist (e.g., YouTube), but **[PROJECT ASSUMPTION]** dictates these are modern performance traditions, NOT historical spoken Kawi evidence. Scraping them violates consent and linguistic accuracy.
*   **Conclusion:** There is currently zero usable Kawi-specific speech data.

## 6. Cross-Lingual Options
To proceed with zero budget, we must use a cross-lingual base (e.g., fine-tuning an Indonesian or Javanese Piper model with Kawi text).
*   *Indonesian Base:* Has CC0 data. Lacks retroflexes, aspirates, and long vowels.
*   *Javanese Base:* Has CC-BY-SA data. Contains retroflexes (`ṭ`, `ḍ`), but still lacks aspirates and long vowels.
*   *Phoneme Support:* We can feed custom `espeak-ng` phonemes to the model, but if the pre-trained weights have never mapped an aspirated stop (e.g., `bʰ`) to audio, the model will output garbage or collapse it to `b`.

## 7. Phonetic Gap Matrix
Mapping Kawi canonical representation to an Indonesian/Javanese neural base:

| Kawi Distinction | Base Model Representation (Indo/Java) | Status | Risk |
| :--- | :--- | :--- | :--- |
| **Dental stops (`t`, `d`)** | `t`, `d` | Supported | None |
| **Retroflex stops (`ṭ`, `ḍ`)** | `t`, `d` (Indo) / `ʈ`, `ɖ` (Java) | Approximate (Java) | High (Indo base merges with dentals) |
| **Aspirated stops (`bʰ`, `dʰ`, `kʰ`, etc.)**| `b`, `d`, `k` | **UNSUPPORTED** | **[BLOCKER]** Acoustic collapse |
| **Schwa (`ĕ` / `ə`)** | `ə` | Supported | None |
| **Velar nasal (`ṅ` / `ŋ`)** | `ŋ` | Supported | None |
| **Palatal nasal (`ɲ`)** | `ɲ` | Supported | None |
| **Syllabic liquids (`ṛ`, `ḷ`)** | `rə`, `lə` | Approximate | **[ENGINEERING CONVENTION]** required |
| **Long vowels (`ā`, `ī`, `ū`)** | `a`, `i`, `u` | **UNSUPPORTED** | Duration collapse; Indonesian lacks phonemic length |
| **Sanskrit sibilants (`ś`, `ṣ`)** | `s` | **UNSUPPORTED** | **[BLOCKER]** Merges with `s` |

## 8. Licensing/Provenance Analysis
*   **Code/Model License:** MIT/Apache (Piper/Kokoro) is safe.
*   **Dataset License:** CC0 (Mozilla CV) and CC-BY-SA (OpenSLR) are safe.
*   **Consent:** Scraping YouTube Kakawin readings violates both copyright and speaker consent (they did not consent to AI voice cloning). **[EVIDENCE]** We cannot use them.
*   **Finding:** The software and proxy data are legally safe, but linguistically inappropriate.

## 9. Zero-Budget Analysis
A zero-budget path requires leveraging existing open data. Because there is no existing Kawi data, we must use an Indonesian/Javanese proxy. 
However, the Phonetic Gap Matrix reveals that a proxy model will physically collapse canonical Kawi distinctions (aspirates and long vowels). 
**[INFERENCE]** Training an Indonesian base model to magically produce aspirated stops without any audio examples of aspirated stops is impossible. Therefore, a linguistically responsible zero-budget path does not currently exist.

## 10. Risk Assessment
*   **Acoustic Collapse:** If we use an Indonesian neural TTS, `bʰaṭāra` and `batara` will sound acoustically identical. This violates the Neural Backend Contract (Section 3C of the Roadmap), which mandates preserving canonical distinctions.
*   **Hallucination:** End-to-end models will inject modern Indonesian intonation patterns into historical texts.

## 11. Decision
**C. STAGE 1 CURRENTLY BLOCKED AT DATA READINESS GATE**
No responsible path currently satisfies the Data Readiness gates. The project lacks the audio data required to train a model that preserves Kawi's canonical phonetic distinctions (specifically aspirates and long vowels). Using a proxy language base violates the core requirement to maintain historical linguistic fidelity.

## 12. Smallest Next Action
Do not write code.
The smallest realistic next action is:
**Record a targeted 15-30 minute custom audio corpus.** 
A qualified linguist or scholar must read a specifically designed Kawi phonetically balanced wordlist (emphasizing aspirates `bʰ/dʰ`, retroflexes `ṭ/ḍ`, and long vowels `ā/ī`) into a high-quality microphone, and explicitly release the audio under a CC0 license.

## 13. Open Questions
1.  Could a purely *multilingual* base model (e.g., one trained simultaneously on Hindi for aspirates/retroflexes and Indonesian for phonotactics) be prompted via zero-shot cross-lingual transfer to pronounce Kawi accurately without fine-tuning?
2.  If the 15-minute scholar recording is obtained, is that duration mathematically sufficient to fine-tune a Piper model without catastrophic forgetting of basic speech synthesis capabilities?

## 14. Sources
*   [EVIDENCE] Mozilla Common Voice Scripted Speech 27.0 - Indonesian (CC0)
*   [EVIDENCE] OpenSLR SLR41: Javanese TTS Data by Google/UGM (CC-BY-SA 4.0)
*   [EVIDENCE] INESCO: Indonesian Expressive Speech Corpus (Mendeley Data, CC-BY)
*   [ENGINEERING CONVENTION] Piper TTS Architecture and `espeak-ng` phoneme mappings (MIT)
