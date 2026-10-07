# P7-002A: EXISTING KAWI / OLD JAVANESE AUDIO SOURCE AUDIT

## 1. Executive Summary
This audit investigates the availability and usability of existing human audio recordings of Kawi / Old Javanese. The objective is to determine if available audio can serve as a defensible pronunciation source for reference, model training, or as a pathway to commissioning a controlled corpus. **Crucially, the project owner, Abraham, is not a native speaker and cannot provide phonetic ground truth for training.**

The audit concludes that while rich historical archives and modern performance recordings of Old Javanese texts exist (primarily the Balinese *mabasan/makakawin* tradition and academic recitations), **none provide explicitly CC0/CC-BY licensed audio that isolates the specific phonological targets of Profile A (e.g., controlled apical-alveolar vs. retroflex distinctions without modern phonetic interference).**

Therefore, the project must pursue **Path C**: Commission a scholar or expert reciter to create a controlled corpus.

## 2. Search Scope and Methodology
The audit scanned for existing recordings across several domains:
*   **Archives:** PARADISEC, SEAsia-Hearing (Jaap Kunst/Christian Pelras collections), Arbiter Records (Bali 1928 collections).
*   **Public Platforms:** YouTube, Internet Archive.
*   **Target Content:** Kakawin recitation, *mabasan* (Balinese reading groups), scholarly linguistic readings, and university lectures.
*   **Evaluation Criteria:** Licensing (public domain / CC-BY for ML training), epistemic categorization (historical vs. modern reading vs. performance tradition), and acoustic usefulness (segmental phoneme realization).

## 3. Candidate Audio / Source Table

| Source Title / Text | Speaker / Performer | Date | Tradition | Provenance / Archive | License / Access | Training Reuse | Acoustic Usefulness & Relevance | Recommended Use |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bali 1928, Vol. IV (Kakawin & Palawakia)** | Ida Boda, Ni Lemon, Juru Baca | 1928–1929 | **C** (Balinese Kakawin) | Arbiter Records | Commercial / Proprietary | **NO** | Highly musical, heavy vibrato (*ombak*). Demonstrates prosody but obscures phonetic segments. (Profile C relevance) | REFERENCE |
| **Pembacaan Kakawin, 1 & 2 (Ramayana)** | Madé Rai, Gégé Gègèr | 1968 | **C** (Balinese Mabasan) | SEAsia-Hearing (Pelras) / Musée de l'Homme | Restricted Archive | **NO** | Alternating chanted Old Javanese with spoken Balinese translation. Prosodically rich, phonetically influenced by Balinese. | REFERENCE |
| **Kakawin Ramayana (Sarga 1, 1-15)** | Unlisted | Modern | **F** (Academic/Pedagogical) | YouTube | Standard YouTube License | **NO** | Clear syllable articulation. May demonstrate Sanskritized pronunciation (Profile B). Lacks CC licensing for weights. | REFERENCE |
| **Panji Tales (Leiden University)** | Academic Narrators | Modern | **B/F** (Scholarly) | YouTube / Leiden | Copyrighted Video | **NO** | English/Dutch narration describing manuscripts, sparse Kawi vocalization. | NOT USABLE |

*Legend: A = Historical spoken, B = Modern scholarly reading, C = Balinese performance, D = Modern Javanese reading, E = Indonesian reading, F = Academic reconstruction, G = Unknown.*

## 4. Expert-Speaker Candidates
To generate a CC0 training corpus, an expert speaker must be commissioned. Potential profiles to target for contact include:
1.  **Academic Philologists / Linguists:** Scholars specializing in Old Javanese phonology (e.g., affiliates of Leiden University, or Indonesian universities like UGM/UI). *Evidence of competence:* Published work on Old Javanese phonotactics.
2.  **Trained Mabasan Practitioners:** Balinese reciters capable of reading Kawi script and vocalizing texts. *Evidence of competence:* Active participation in *pesantian* (reading clubs) and ability to separate text from musical ornamentation when instructed.
3.  **Classical Gamelan/Wayang Vocalists (Sindhen/Dalang):** E.g., Darsono Hadiraharjo, Hèni Savitri. *Evidence of competence:* Familiarity with archaic Javanese vocabulary and poetic meters.

*Note: No specific individual is claimed as a perfect Profile A speaker without a formal recording protocol and phonetic review.*

## 5. Licensing and Provenance Analysis
*   **YouTube:** Almost all discovered YouTube recitations fall under the Standard YouTube License. These can be studied for reference but **cannot** be bulk-downloaded or used to train a neural network that will be released under an open license.
*   **Historical Archives:** Anthropological recordings (like the 1928 Arbiter releases or the 1968 Pelras recordings) are bound by strict institutional copyrights, ethical access frameworks, and non-commercial restrictions.
*   **Conclusion:** There is no "free" existing audio dataset of Old Javanese that legally permits unrestricted machine learning derivation and redistribution.

## 6. Acoustic Usefulness Analysis
Existing recordings (especially Balinese Kakawin) present severe acoustic limitations for training a Profile A neural model:
*   **Musical Overlays:** The *mabasan* tradition utilizes stylized singing (*mawirama*), throat constriction, and rhythmic fluctuation (*ombak*). This distorts steady-state vowel formants and consonant bursts, confusing forced aligners.
*   **Phonological Mergers:** Balinese and modern Javanese speakers naturally apply their native phonological constraints when reading Kawi. For instance, modern Javanese speakers might round open /a/ to [ɔ], and Balinese speakers might neutralize certain retroflex/dental distinctions that Profile A aims to preserve explicitly.
*   **Lack of Transcripts:** Finding time-aligned, phonemically precise transcriptions for existing archival audio is virtually impossible.

## 7. Profile A/B/C Relevance
*   **Profile A (Reconstructed Historical Spoken):** No existing audio represents this. All spoken audio of Old Javanese today is filtered through modern languages.
*   **Profile B (Scholarly/Orthographic):** Some academic recitations exist, but they are unlicensed for training and often lack phonetic consistency regarding retroflexion.
*   **Profile C (Performance/Kakawin):** Heavily represented in archives, but entirely unsuitable for training a plain-text-to-speech reading voice due to musicality and extreme pitch variation.

## 8. Candidate Project Paths
*   **Path A (Use existing audio):** Blocked by licensing and acoustic distortion.
*   **Path B (Expert corpus required, existing audio as reference):** Viable. We must use existing audio solely to understand prosody, but record fresh audio.
*   **Path C (Commission a scholar/reciter):** **Primary Path.** Requires designing a recording protocol and finding a willing participant who will release the audio CC0.
*   **Path D (Defer neural TTS):** Fallback if Path C fails.

## 9. Recommended Next-Step Gate
**GO-C: Design a commissioned expert-recording protocol.**
The evidence dictates that we cannot use existing audio for training, nor can Abraham record it. We must design a protocol to recruit, test, and commission an external expert speaker who can intentionally target Profile A phonetics and sign a CC0 release.

## 10. Open Uncertainties
*   Can a modern scholar or reciter accurately and consistently reproduce the required retroflex vs. dental contrasts (`t` vs `ṭ`, `d` vs `ḍ`) over a 50-sentence corpus without native-language interference?
*   What compensation or academic attribution is required to secure a CC0 license from an expert?

## 11. Sources/References
*   *Tembang Kuna. Bali 1928.* Herbst. Arbiter Records. (CD Notes detailing *mabasan* vocal techniques).
*   *Bali 1928, vol. IV: Music for Temple Festivals and Death Rituals.*
*   Pelras, Christian (1968). *Pembacaan Kakawin, 1 & 2*. SEAsia-Hearing Archive (Musée de l'Homme).
*   Zoetmulder, P.J. (1982). *Old Javanese–English Dictionary*. (Reference for vocabulary scope and Sanskrit influence).
