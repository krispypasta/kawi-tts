# Research Log: Kawi-TTS

**Last updated:** 2026-10-07
**Current phase:** Phase 0 — Project Foundation (complete). Phase 1 — Linguistic Research (beginning).

This document is the authoritative record of all linguistic research conducted for the Kawi-TTS project.
Every finding must be cited. Every claim must carry an evidence-status label.
AI-generated claims without a verifiable source are not evidence.

---

## Evidence-Status Labels

Every finding in this log must be labeled with one of:

- ESTABLISHED — supported by multiple concordant reliable sources; well-accepted in the field.
- RECONSTRUCTED — inferred or reconstructed from indirect historical or comparative evidence.
- UNCERTAIN — evidence is conflicting, ambiguous, or insufficient.
- ASSUMPTION — a temporary working assumption not yet supported by investigated sources.

---

## Section 1: Open Research Questions (Phase 1 Agenda)

These are questions, not answers. Each must be investigated using actual sources before
any implementation decision is made that depends on it.

### 1.1 Phoneme Inventory

- RQ-001: What is the generally accepted consonant inventory of Old Javanese?
  Do sources agree on the inventory, or are there significant disagreements?
  (Key sources to check: Zoetmulder 1982, Uhlenbeck 1949, Casparis 1975, Hunter various)

- RQ-002: What is the generally accepted vowel inventory of Old Javanese?
  Are short/long vowel pairs (a/aa, i/ii, u/uu) treated as distinct phonemes
  by all major sources, or is length primarily a metrical/scribal convention?

- RQ-003: What is the linguistic status of the pepet (e-tailing, schwa, written e or ě)?
  Is it a phoneme, an allophone of /a/, or an orthographic convention?
  How does it differ from the front vowel /e/?

- RQ-004: Were the aspirated stop series (kh, gh, th, dh, ph, bh, ch, jh)
  phonemically distinct in native Kawi vocabulary, or are they exclusively
  a Sanskrit-loanword feature? What is the evidence?

- RQ-005: Were the retroflex stops (t-underdot, d-underdot, etc.) and retroflex nasal
  genuinely retroflex in phonetic realization, or were they dental or
  post-dental in Old Javanese? What comparative evidence exists?

- RQ-006: What is the phonemic status of the three sibilants?
  Is there evidence that s (dental), s-with-acute (palatal), and s-with-underdot
  (retroflex) were phonemically distinct in Old Javanese pronunciation, or did they merge?

- RQ-007: What evidence exists for syllable structure in Old Javanese?
  What are the attested consonant cluster types? Are there restrictions?

- RQ-008: What evidence exists for stress placement in Old Javanese?
  Is stress documented in any grammar or inferred from metrical evidence?

- RQ-009: What is the role and extent of sandhi in Old Javanese?
  Does sandhi apply across word boundaries in a way that affects TTS?

### 1.2 Orthography and Romanization

- RQ-010: What romanization convention is used in the Old Javanese-English
  Dictionary (Zoetmulder 1982)? Is it fully described in a systematic way
  in any published source?

- RQ-011: Are there other romanization conventions in scholarly use for
  Old Javanese (e.g., Leiden conventions, ISO 15919, Dutch orthographic
  conventions in older sources)? How do they differ from Zoetmulder?

- RQ-012: Which romanization convention should be chosen as the primary
  input format for the TTS system, and on what basis?
  (Cannot be resolved without first answering RQ-010 and RQ-011.)

### 1.3 Historical and Modern Pronunciation Traditions

- RQ-013: What is the relationship between reconstructed Old Javanese
  phonology and the Balinese-inflected Kawi recitation tradition (mabasan)?
  Do scholars treat these as the same phonology, closely related, or distinct?

- RQ-014: Are there any audio recordings of Kawi recitation (mabasan,
  kakawin performance) that are publicly accessible? If so, what is their
  provenance, and can they be used as pronunciation reference material
  or as TTS training data?

- RQ-015: How did Old Javanese evolve into Middle Javanese and Modern
  Javanese? Are any Modern Javanese features relevant to Kawi pronunciation
  reconstruction?

### 1.4 Corpus and Data

- RQ-016: What romanized Old Javanese text corpora are digitally available?
  (Check GRETIL, Uli Kozok's materials, KITLV archives, institutional
  repositories, and recent digital humanities projects.)

- RQ-017: What is the licensing situation for available Old Javanese text
  corpora? Can they be used for TTS training purposes?

- RQ-018: What audio data exists that is phonologically related to Old
  Javanese and might be usable for transfer learning or acoustic modeling?
  (Candidates: Balinese TTS, Modern Javanese TTS, Sanskrit TTS.)

- RQ-019: Has any prior computational-linguistic or NLP work been done
  on Old Javanese? (Check for G2P tools, morphological analyzers,
  computational grammars, digital dictionaries with phonemic annotation.)

### 1.5 TTS Approach

- RQ-020: Given the data situation likely to be found in Phase 2, what
  TTS approaches are realistically available?
  (Cannot be answered until RQ-016 through RQ-019 are addressed.)

- RQ-021: What language(s) are phonologically closest to Old Javanese
  among languages that currently have TTS model support?
  Is phonological proximity sufficient to justify acoustic transfer?

---

## Section 2: Research Findings

    Entry ID: RES-001
    Date: 2026-10-07
    Research question(s) addressed: RQ-001, RQ-007
    Finding: The indigenous Old Javanese consonant inventory contrasts dental stops (t, d) with a second series conventionally transcribed as retroflex (ṭ, ḍ), though their exact phonetic realization (true retroflex vs. apical alveolar as in modern Javanese) remains debated. Kumar & Rose (2000) reconstruct a 6-vowel system (/i, u, e, o, a, ə/) and treat prenasalized stops as unit phonemes.
    Evidence status: RECONSTRUCTED (phonemic inventory) / UNCERTAIN (exact phonetic realization of ṭ/ḍ and unit status of prenasalized stops)
    Sources:
      - Kumar & Rose (2000), Oceanic Linguistics 39(2), p. 227.
    Conflicting evidence: Some linguists treat prenasalized stops as clusters. The "retroflex" label may simply reflect orthographic borrowing for a native Javanese apical-alveolar contrast.
    Open questions remaining: What was the exact phonetic realization of ṭ and ḍ? How were Sanskrit-specific consonants mapped?
    TTS implication: V1 G2P must handle the native t/ṭ and d/ḍ contrast.
    Investigated by: Researcher
    Reviewed by: Pending

    Entry ID: RES-002
    Date: 2026-10-07
    Research question(s) addressed: RQ-002, RQ-004
    Finding: Orthography uses length marks (ā, ī, ū) and long pepet (ö). However, standard Austronesian reconstruction (reflected in Kumar & Rose 2000) does not reconstruct phonemic vowel length for indigenous vocabulary. Length was metrically fundamental in poetry (*kakawin*), but whether it was phonemic in normal spoken Old Javanese—or merely an orthographic/metrical convention—remains unresolved.
    Evidence status: ESTABLISHED (absent in native reconstruction) / UNCERTAIN (phonemic status in spoken OJ)
    Sources:
      - Kumar & Rose (2000).
    Conflicting evidence: Universal presence in transliterated orthography vs. absence in historical reconstruction of the native lexicon.
    Open questions remaining: Did bilingual elites pronounce length in Sanskrit loans in normal speech?
    TTS implication: G2P will require a project decision on whether to map macron vowels to short phonemes (for colloquial speech) or retain them (for chanted/learned styles).

    Entry ID: RES-003
    Date: 2026-10-07
    Research question(s) addressed: RQ-003
    Finding: The pepet is phonemically a mid-central vowel /ə/. It is transliterated as *ĕ* by Zoetmulder (1982) and *ə* by Damais (1970) and Acri & Griffiths (2014).
    Evidence status: ESTABLISHED
    Sources:
      - Kumar & Rose (2000); Acri & Griffiths (2014), p. 366.
    Conflicting evidence: None regarding its phonetic quality.
    Open questions remaining: None.
    TTS implication: Must map to IPA [ə].

    Entry ID: RES-004
    Date: 2026-10-07
    Research question(s) addressed: RQ-004
    Finding: Aspirated consonants (kh, gh, th, dh, ph, bh) are absent from the indigenous Old Javanese phoneme inventory. They appear in the script exclusively for Sanskrit loanwords. Their actual pronunciation in historical spoken Old Javanese is unknown.
    Evidence status: ESTABLISHED (absent in native vocab) / UNCERTAIN (phonetic realization in OJ period)
    Sources:
      - Kumar & Rose (2000).
    Conflicting evidence: Orthography distinguishes them, but there is no proof they were spoken with aspiration outside of artificial learned contexts.
    Open questions remaining: Did the elite pronounce them with aspiration?
    TTS implication: G2P requires a project decision on whether to merge them with unaspirated equivalents.

    Entry ID: RES-005
    Date: 2026-10-07
    Research question(s) addressed: RQ-005
    Finding: The contrast between dental /t, d/ and a second series /ṭ, ḍ/ is a native feature of Javanese, not just an orthographic borrowing from Sanskrit.
    Evidence status: RECONSTRUCTED
    Sources:
      - Kumar & Rose (2000), p. 227.
    Conflicting evidence: None regarding the existence of the contrast.
    Open questions remaining: Phonetic realization (true retroflex vs alveolar).
    TTS implication: G2P must preserve the contrast.

    Entry ID: RES-006
    Date: 2026-10-07
    Research question(s) addressed: RQ-006
    Finding: Only the alveolar/dental fricative /s/ is reconstructed for indigenous Old Javanese. The palatal *ś* and retroflex *ṣ* are orthographic characters used for Sanskrit loanwords. Whether they merged with /s/ in historical speech is highly probable but lacks direct acoustic proof.
    Evidence status: ESTABLISHED (only /s/ native) / UNCERTAIN (realization in loans)
    Sources:
      - Kumar & Rose (2000).
    Conflicting evidence: Epigraphic hypercorrections suggest merger, but orthography maintains the distinction.
    Open questions remaining: Did learned recitation preserve them?
    TTS implication: G2P requires a project decision on whether to merge *ś*, *ṣ*, and *s*.

    Entry ID: RES-007
    Date: 2026-10-07
    Research question(s) addressed: RQ-010, RQ-011, RQ-012
    Finding: Zoetmulder (1982) uses a transliteration system based on IAST but with specific deviations: *ĕ* for short pepet, *ö* for long pepet, *w* instead of *v*, and *ṅ* or *ŋ* for the velar nasal. This system transliterates the Indic script rather than providing a phonemic transcription. Acri & Griffiths (2014) argue for strict Indic transliteration (*ə*, *v*), which critics note obscures Old Javanese phonology (e.g., OJ has no /v/ phoneme).
    Evidence status: ESTABLISHED
    Sources:
      - Acri & Griffiths (2014), pp. 365-378.
    Conflicting evidence: Disagreement on whether to prioritize strict script transliteration vs. phonologically informed orthography.
    Open questions remaining: Decide on input format for TTS.
    TTS implication: Input text symbols (*w*, *ĕ*, *ś*, etc.) are transliteration artifacts, not 1:1 phoneme markers.

    Entry ID: RES-008
    Date: 2026-10-07
    Research question(s) addressed: RQ-017, RQ-018
    Finding: Mabasan / makakawin / mawirama refers to the traditional Balinese practice of singing and interpreting Old Javanese texts. *Guru* (heavy) and *laghu* (light) are metrical categories of syllable weight derived from Sanskrit prosody, where *guru* includes both long vowels and short vowels followed by consonant clusters. They define metrical quantity, not phonemic vowel duration.
    Evidence status: ESTABLISHED
    Evidence type: TRADITIONAL / ORTHOGRAPHIC
    Sources:
      - Robson, S. O. (1983). BKI 139.
      - Schumacher, R. (1995). BKI 151(4).
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: If targeting a chanted style, TTS must parse syllable weight for timing.

    Entry ID: RES-009
    Date: 2026-10-07
    Research question(s) addressed: RQ-019, RQ-020, RQ-021
    Finding: In Balinese performance, a *guru* syllable is realized acoustically with longer musical duration/melisma, while a *laghu* syllable is sung shorter. This musical duration is applied to *all* metrically heavy syllables (even short vowels before clusters). Therefore, the chanted duration is a musical realization of written metrical rules, not proof of phonemic vowel length in spoken Old Javanese.
    Evidence status: ESTABLISHED
    Evidence type: MUSICAL / PHONETIC
    Sources:
      - Schumacher, R. (1995).
    Conflicting evidence: None.
    Open questions remaining: Should the TTS replicate this musical timing?
    TTS implication: Audio data from *mabasan* features lengthened vowels for all *guru* syllables. An ML model would learn a chanted rhythm, not natural speech.

    Entry ID: RES-010
    Date: 2026-10-07
    Research question(s) addressed: RQ-022, RQ-023, RQ-024
    Finding: In traditional Balinese *mabasan* performance, Sanskrit aspirates (bh, dh) and palatal/retroflex sibilants (ś, ṣ) are typically merged with unaspirated, dental/alveolar counterparts. Crucially, Balinese merges written Old Javanese retroflex stops (ṭ, ḍ) with dentals because Balinese phonology itself lacks the Javanese dental/alveolar contrast. This merger reflects modern Balinese phonological constraints, not proof that historical Old Javanese merged them.
    Evidence status: ESTABLISHED
    Evidence type: TRADITIONAL / PHONETIC
    Sources:
      - Robson (1983); Herbst (2016); general Indonesian comparative linguistics.
    Conflicting evidence: Highly learned priests occasionally artificially re-introduce Sanskrit phonetics.
    Open questions remaining: None.
    TTS implication: Balinese performance merges contrasts based on Balinese phonology. G2P must not blindly adopt this merger if the target is historical Javanese.

    Entry ID: RES-011
    Date: 2026-10-07
    Research question(s) addressed: RQ-025
    Finding: There is a strict cascade in *kakawin* performance: orthography defines metrical classification (guru/laghu), which dictates musical realization (duration/melisma). This cascade bypasses historical Javanese spoken phonology entirely and is filtered through modern Balinese phonology.
    Evidence status: ESTABLISHED
    Evidence type: MUSICAL / ORTHOGRAPHIC
    Sources:
      - Schumacher, R. (1995).
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: Chanted TTS must parse metrical structure; spoken TTS must ignore it.

    Entry ID: RES-012
    Date: 2026-10-07
    Research question(s) addressed: RQ-026, RQ-027
    Finding: Modern Balinese *kakawin* recordings exist and contain acoustic data for pitch, F0, and syllable duration (e.g., Herbst's Bali 1928 restorations). However, this data cannot be used to reconstruct the historical *spoken* pronunciation of Old Javanese. It serves only as evidence for prosody, rhythm, and the chant structure of the performance tradition.
    Evidence status: ESTABLISHED
    Evidence type: TRADITIONAL / MUSICAL
    Sources:
      - Herbst, E. (2016). *Bali 1928* volume on Tembang Kuna.
      - Robson (1983).
    Conflicting evidence: None.
    Open questions remaining: Will V1 target historical spoken Old Javanese or the Balinese chanted tradition?
    TTS implication: Audio from *mabasan* cannot be used as training data for a conversational/spoken Kawi TTS.

    Entry ID: RES-013
    Date: 2026-10-07
    Research question(s) addressed: RQ-016, RQ-017
    Finding: Romanized Old Javanese text corpora are limited but available. The GRETIL (Göttingen Register of Electronic Texts in Indian Languages) repository hosts several transliterated Old Javanese texts (e.g., *Gaṇapatitattwa*). The SEACrowd / Old Javanese Wordnet (OJW) by Moeljadi & Aminullah (2020) provides a CC-BY-SA-4.0 licensed lexical database mapping Zoetmulder's dictionary to Princeton Wordnet.
    Evidence status: ESTABLISHED
    Evidence type: TRADITIONAL / ORTHOGRAPHIC
    Sources:
      - Moeljadi, D. & Aminullah, Z. P. (2020). "Building the Old Javanese Wordnet." LREC.
      - GRETIL / TextGrid Repository.
    Conflicting evidence: None.
    Open questions remaining: Are the GRETIL texts large enough for language modeling or extensive G2P testing?
    TTS implication: Wordnet provides a lexical validation list for G2P rules. GRETIL provides sentence-level text for testing normalization and G2P, but neither provides audio alignment.

    Entry ID: RES-014
    Date: 2026-10-07
    Research question(s) addressed: RQ-018
    Finding: No suitable historical-period speech corpus for Old Javanese was identified in the surveyed sources. There are no recordings of "Reconstructed Historical Spoken Old Javanese" (Profile A target). Available audio consists strictly of traditional chanted performance (Profile C) or modern scholarly reading (Profile B).
    Evidence status: ESTABLISHED
    Evidence type: HISTORICAL
    Sources:
      - Survey of public speech datasets (OpenSLR, Mozilla Common Voice, Hugging Face).
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: It is impossible to train an end-to-end Old Javanese TTS model from scratch for Profile A. The system must use a rule-based G2P pipeline paired with either synthetic rules or cross-lingual acoustic transfer.

    Entry ID: RES-015
    Date: 2026-10-07
    Research question(s) addressed: RQ-018, RQ-026, RQ-027
    Finding: Extensive audio recordings of Balinese *mabasan* / *kakawin* chanting exist (e.g., Herbst's *Bali 1928* restorations, contemporary ethnographic recordings). However, this data represents Profile C (Balinese Performance) and cannot be used as training data for Profile A because its metrical/musical duration and phonological mergers contradict historical reconstructed speech.
    Evidence status: ESTABLISHED
    Evidence type: MUSICAL / TRADITIONAL
    Sources:
      - Herbst, E. (2016). *Bali 1928, Vol. II*.
      - Decision DEC-006.
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: Balinese chanted audio must be explicitly excluded from any V1 training or acoustic transfer data to avoid contaminating the Profile A target with Profile C rhythm and phonology.

    Entry ID: RES-016
    Date: 2026-10-07
    Research question(s) addressed: RQ-019
    Finding: Computational and TTS resources for *Modern Javanese* exist and are potentially transferable. Datasets such as OpenSLR 41 (Javanese speech corpus) and pre-trained models like Facebook's MMS-TTS-JAV exist. These resources natively model the Javanese dental/alveolar contrast (/t/ vs /ṭ/, /d/ vs /ḍ/) which is critical for Profile A.
    Evidence status: ESTABLISHED
    Evidence type: COMPARATIVE
    Sources:
      - OpenSLR Dataset 41.
      - Facebook/Meta Massively Multilingual Speech (MMS).
    Conflicting evidence: None.
    Open questions remaining: Will a modern Javanese acoustic model mispronounce certain historical clusters or the pepet (/ə/) if fed Old Javanese phoneme strings?
    TTS implication: Modern Javanese provides the most viable acoustic backend (via transfer learning or phoneme-mapping to an existing TTS model) for synthesizing Profile A, circumventing the lack of Old Javanese audio.

---

## Section 3: Working Hypotheses Inherited From Project Scaffold

The following claims were present in earlier project scaffold files.
They have been preserved here and labeled ASSUMPTION to make their epistemic
status explicit. None should be treated as established facts. Each must be
verified or revised during Phase 1 before it influences any implementation.

ASSUMPTION-001 (from scaffold): Pepet is an established central vowel,
mid-central /schwa/. Attributed to: "Universal in Javanese historical phonology."
Status: ASSUMPTION. The claim lacks a specific cited source for Old Javanese.
Must be addressed by: RQ-003.
Note: The original scaffold entry presented this as "Established" — this label
has been downgraded to ASSUMPTION because no specific source was cited.

ASSUMPTION-002 (from scaffold): Long vowels (aa, ii, uu) are distinct in
duration in formal recitation; quality distinction also possible.
Attributed to: Zoetmulder (1974).
Status: ASSUMPTION — the source has not yet been read for this project.
The claim has not been verified against the source.
Must be addressed by: RQ-002.

ASSUMPTION-003 (from scaffold): Retroflex stops are distinct from dentals;
"true retroflex [ʈ, ɖ] vs dental [t, d] or alveolar" (unresolved).
Status: ASSUMPTION — source basis is described only as "Sanskrit loanword
phonology vs native retroflex," which is not a specific cited finding.
Must be addressed by: RQ-005.

ASSUMPTION-004 (from scaffold): Aspirated stops are "realized as aspirated
in scholastic reading; neutralized in colloquial speech."
Attributed to: Hunter; comparative Austronesian (non-specific).
Status: ASSUMPTION — no specific source or page cited.
Must be addressed by: RQ-004.

---

## Section 4: Dataset Audit Log

No datasets have been audited yet. Phase 2 (Data Audit) follows Phase 1 research.

| Dataset / Source | Type | License | Duration/Size | Quality | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| (Phase 2 task) | | | | | |

---

## Section 5: Bibliography

Sources planned for consultation are listed here. Sources that have been
read and cited in findings are marked [READ] with the entry date.

### Primary Grammars and Dictionaries

- [ZOETMULDER-1982] Zoetmulder, P.J., with S.O. Robson. Old Javanese-English
  Dictionary. 2 vols. The Hague: Martinus Nijhoff, 1982. [NOT YET READ]

- [ZOETMULDER-1974] Zoetmulder, P.J. Kalangwan: A Survey of Old Javanese
  Literature. The Hague: Martinus Nijhoff, 1974. [NOT YET READ]
  (Kakawin prosody, meter, vowel length.)

- [UHLENBECK-1949] Uhlenbeck, E.M. De Structuur van het Javaanse Morpheem.
  Bandung: A.C. Nix, 1949. [NOT YET READ]

- [TEEUW-1969] Teeuw, A. et al. Siwaratrikalpa of Mpu Tanakung.
  The Hague: Martinus Nijhoff, 1969. [NOT YET READ]
  (Textual transmission, editorial standards for Old Javanese texts.)

### Phonology and Linguistics

- [HUNTER-VARIOUS] Hunter, Thomas M. Various papers on Sanskritization
  in Old Javanese and Old Javanese linguistics. [NOT YET READ —
  specific titles and years to be identified during Phase 1 research.]

- [NOTHOFER-1975] Nothofer, Bernd. The Reconstruction of Proto-Malayo-Javanic.
  The Hague: Martinus Nijhoff, 1975. [NOT YET READ]
  (Comparative/historical context for phonological reconstruction.)

- [CASPARIS-1975] de Casparis, J.G. Indonesian Palaeography. Leiden/Koln:
  Brill, 1975. [NOT YET READ] (Script, romanization conventions.)

### Digital Resources

- [GRETIL] Gottingen Register of Electronic Texts in Indian Languages.
  https://gretil.sub.uni-goettingen.de [NOT YET SURVEYED]
  (May contain relevant Old Javanese or Sanskrit texts.)

---

## Section 6: P1-013 — Pronunciation Inventory & Uncertainty Matrix

This matrix synthesizes Phase 1 research findings into a structured map of the relationship between orthography, phonology, and phonetics in Old Javanese.

**Crucial Note on Evidence Status:**
- Many phonemic distinctions exist in the *script* (derived from Sanskrit) and are preserved in scholarly *transliteration* (e.g., Zoetmulder 1982).
- The *historical phonetic realization* of Sanskrit loans by Old Javanese speakers is frequently **UNCERTAIN**.
- Distinctions marked as **UNCERTAIN** must NOT be blindly implemented as distinct phonemes in V1 without a formal human project decision defining the target performance style.

### Vowels & Liquids

| Translit / Grapheme | Native / Loan | Phonological Reconstruction (Kumar & Rose) | Evidence Status | Evidence Type | Candidate Phonetic Realization | V1 Readiness / Uncertainty |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **a** | Both | /a/ | ESTABLISHED | COMPARATIVE | [a], possibly [ɔ] in open syllables | Safe to implement as /a/. |
| **i** | Both | /i/ | ESTABLISHED | COMPARATIVE | [i] | Safe to implement as /i/. |
| **u** | Both | /u/ | ESTABLISHED | COMPARATIVE | [u] | Safe to implement as /u/. |
| **e** | Both | /e/ | ESTABLISHED | COMPARATIVE | [e], [ɛ] | Safe to implement as /e/. |
| **o** | Both | /o/ | ESTABLISHED | COMPARATIVE | [o], [ɔ] | Safe to implement as /o/. |
| **ĕ / ə** | Native | /ə/ (schwa) | ESTABLISHED | COMPARATIVE | [ə] | Safe to implement as /ə/. |
| **ā, ī, ū** | Loan | Absent in native reconstruction | UNCERTAIN (Phonemic) / ESTABLISHED (Metrical) | HISTORICAL / ORTHOGRAPHIC | [aː], [iː], [uː] | **Human Decision Required.** Metrical in text, but did historical speakers use duration? |
| **ö** | Orthographic | Absent | UNCERTAIN | ORTHOGRAPHIC | [əː] | **Human Decision Required.** Long schwa is highly unusual cross-linguistically. |
| **ṛ / r̥** | Loan | Absent | UNCERTAIN | ORTHOGRAPHIC | [rə] (Traditional) | **Human Decision Required.** Syllabic /r/. Likely mapped to /rə/ in speech. |
| **ḷ / l̥** | Loan | Absent | UNCERTAIN | ORTHOGRAPHIC | [lə] (Traditional) | **Human Decision Required.** Syllabic /l/. Likely mapped to /lə/ in speech. |

### Consonants: Stops & Affricates

| Translit / Grapheme | Native / Loan | Phonological Reconstruction | Evidence Status | Evidence Type | Candidate Phonetic Realization | V1 Readiness / Uncertainty |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **p, b** | Both | /p/, /b/ | ESTABLISHED | COMPARATIVE | [p], [b] | Safe to implement. |
| **t, d** | Both | /t/, /d/ (dental) | ESTABLISHED | COMPARATIVE | [t̪], [d̪] | Safe to implement. |
| **ṭ, ḍ** | Native | /ṭ/, /ḍ/ (retroflex) | RECONSTRUCTED | COMPARATIVE | [ʈ, ɖ] or [t, d] (alveolar) | Safe to implement as distinct from t/d, but exact phonetics uncertain. |
| **c, j** | Both | /c/, /j/ (palatal) | ESTABLISHED | COMPARATIVE | [tʃ, dʒ] or [c, ɟ] | Safe to implement. |
| **k, g** | Both | /k/, /g/ | ESTABLISHED | COMPARATIVE | [k], [g] | Safe to implement. |
| **ph, bh** | Loan | Absent natively | UNCERTAIN | ORTHOGRAPHIC | [pʰ, bʱ] vs [p, b] | **Human Decision Required.** Merged in modern Bali, but historical OJ status unknown. |
| **th, dh** | Loan | Absent natively | UNCERTAIN | ORTHOGRAPHIC | [t̪ʰ, d̪ʱ] vs [t̪, d̪] | **Human Decision Required.** |
| **ṭh, ḍh** | Loan | Absent natively | UNCERTAIN | ORTHOGRAPHIC | [ʈʰ, ɖʱ] vs [ṭ, ḍ] | **Human Decision Required.** |
| **kh, gh** | Loan | Absent natively | UNCERTAIN | ORTHOGRAPHIC | [kʰ, gʱ] vs [k, g] | **Human Decision Required.** |
| **ch, jh** | Loan | Absent natively | UNCERTAIN | ORTHOGRAPHIC | [cʰ, ɟʱ] vs [c, j] | **Human Decision Required.** |

### Consonants: Nasals, Fricatives, Liquids, Glides

| Translit / Grapheme | Native / Loan | Phonological Reconstruction | Evidence Status | Evidence Type | Candidate Phonetic Realization | V1 Readiness / Uncertainty |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **m, n** | Both | /m/, /n/ | ESTABLISHED | COMPARATIVE | [m], [n] | Safe to implement. |
| **ṅ / ŋ** | Both | /ŋ/ | ESTABLISHED | COMPARATIVE | [ŋ] | Safe to implement. |
| **ñ / ny** | Both | /ɲ/ | ESTABLISHED | COMPARATIVE | [ɲ] | Safe to implement. |
| **ṇ** | Loan | Absent natively | UNCERTAIN | ORTHOGRAPHIC | [ɳ] vs [n] | **Human Decision Required.** Retroflex nasal is a Sanskrit artifact. |
| **s** | Both | /s/ | ESTABLISHED | COMPARATIVE | [s] | Safe to implement. |
| **ś, ṣ** | Loan | Absent natively | UNCERTAIN | ORTHOGRAPHIC | [ʃ], [ʂ] vs [s] | **Human Decision Required.** Historical phonetic preservation vs. merger to /s/. |
| **h** | Both | /h/ | ESTABLISHED | COMPARATIVE | [h] | Safe to implement. |
| **w / v** | Both | /w/ | ESTABLISHED | COMPARATIVE | [w] | Safe to implement as /w/. Zoetmulder uses 'w', Acri/Griffiths use 'v', but phoneme is /w/. |
| **y** | Both | /y/ | ESTABLISHED | COMPARATIVE | [j] | Safe to implement. |
| **r, l** | Both | /r/, /l/ | ESTABLISHED | COMPARATIVE | [r], [l] | Safe to implement. |

### Structural & Prosodic Elements

| Feature | Evidence Status | Evidence Type | Notes |
| :--- | :--- | :--- | :--- |
| **Guru / Laghu** | ESTABLISHED | METRICAL | Strict metrical weight rules define verse structure and modern sung duration, but are NOT phonemic. |
| **Consonant Clusters** | ESTABLISHED | ORTHOGRAPHIC / PHONOLOGICAL | Native vocabulary contains primarily medial clusters (esp. homorganic nasal+stop). Sanskrit loans introduce complex initial/medial clusters. |
| **Prenasalized Stops** | UNCERTAIN | COMPARATIVE | Kumar & Rose (2000) reconstruct them as unit phonemes (e.g. /mb/, /nd/); others treat them as nasal+stop clusters. Implementation must choose a strategy. |

---

### Unresolved Project-Level Decisions (Requiring Human Input)

The following distinctions cannot be resolved purely by linguistic evidence, because the evidence points to a divergence between *Sanskrit-influenced Orthography* and *Native Spoken Javanese Phonology*. 

Before the Engineer can write G2P rules, Abraham must decide which of the following three **Pronunciation Targets** the V1 TTS system should emulate:

**Target A: Historical Spoken Old Javanese (Conversational / Native-centric)**
- Merges orthographic long vowels (ā, ī, ū, ö) to short phonemes.
- Merges Sanskrit aspirates (bh, dh, etc.) to unaspirated equivalents (b, d).
- Merges Sanskrit sibilants (ś, ṣ) to /s/.
- Merges Sanskrit retroflex nasal (ṇ) to /n/.
- *Consequence*: Highly authentic to Austronesian linguistic reality, but destroys the acoustic realization of Sanskrit loans and poetic meter.

**Target B: Scholarly / Artificial Reading (Orthography-centric)**
- Forces distinct pronunciation of long vowels, aspirates, and sibilants based purely on their presence in the text.
- *Consequence*: Synthesizes a "perfect" Sanskritized Kawi that perhaps no human actually spoke colloquially, but which maximally preserves textual information in the audio.

**Target C: Traditional Balinese Performance (Chanted / Mabasan)**
- Merges aspirates, sibilants, and retroflexes due to Balinese phonological constraints.
- Applies extreme duration to *guru* syllables (long vowels AND short vowels before clusters).
- *Consequence*: Authentic to modern traditional practice, but produces a singing/chanting rhythm rather than spoken TTS, and introduces modern Balinese phonological mergers.

**Abraham:** Please review these targets and advise which one V1 should pursue. This is a project-design choice, not a linguistic fact to be discovered.

---

## Section 8: P3-003C G2P Edge-Case Audit

**Date:** 2026-10-07
**Mode:** Engineer/Builder
**Task:** P3-003C (Audit of Lossless G2P Implementation)

An audit of `src/g2p/engine.py` was conducted against realistic Old Javanese forms.

### A. PASSING CASES
- **Nasals:** `ṅ` correctly parses as `["ŋ"]`; `ñ` as `["ɲ"]`.
- **ASCII Protections:** `ng` parses as `["n", "g"]` and `ny` as `["n", "j"]`. This strictly obeys the policy NOT to silently assume ASCII digraphs are single phonemes.
- **Aspirates:** `bh`, `dh`, `ṭh`, etc., greedily parse to dedicated internal phonemes (`bʱ`, `dʱ`, `ṭʰ`), strictly preventing merger with native stops.
- **Vowels & Length:** `ā`, `ī`, `ū`, and `ö` parse to `aː`, `iː`, `uː`, and `əː`, preserving all metrical/historical information.
- **Sibilants & Retroflexes:** `ś`, `ṣ`, `s`, `ṭ`, `ḍ`, `ṇ` all map uniquely and distinctively.
- **Vocalic Liquids:** `ṛ` and `ḷ` map to `r̩` and `l̩`, which are structural encodings that avoid premature phonetic claims like `[rə]`.

### B. FAILING CASES
- **Un-normalized ASCII `sanghyang`:** If a user inputs un-normalized ASCII `sanghyang` (instead of canonical `saṅhyaṅ`), the greedy parser matches `gh` and outputs `["s", "a", "n", "gʱ", "j", "a", "n", "g"]`. This falsely injects a Sanskrit aspirate (`gʱ`) into a native Javanese word. 

### C. AMBIGUOUS CASES
- **Morpheme Boundary Stops + `h`:** If a native compound has a stop abutting an `h` (e.g., hypothetically `sab-ha`), the greedy parser will merge it to `bʱ`. (Very rare in Kawi due to phonotactics, but structurally possible).
- **Acri/Damais `ə̄`:** The `ə` parses correctly, but the combining macron `\u0304` parses as a standalone unknown token `["\u0304"]`. 

### D. INFORMATION-LOSS RISKS
- None within the G2P engine itself. It is perfectly lossless for canonical Zoetmulder input. The only risk is users feeding it un-normalized ASCII.

### E. REQUIRED FIXES
- No changes required to `src/g2p/engine.py`. The greedy parser operates exactly as specified. The fix for `sanghyang` and boundary issues belongs in the P3-004 Text-Structure layer (e.g., supporting hyphens to block digraph formation: `sang-hyang`).

### F. CASES WAITING FOR DECISION
- The 5 Acoustic Mapper reductions (vowel length, aspirates, sibilants, retroflex nasal, vocalic liquids) remain safely deferred.

### G. RECOMMENDATION
- P3-004 (Text Normalization: punctuation, sandhi, word boundaries) is safe to begin. It will provide the necessary structural boundary markers to protect the G2P engine from edge cases like `sanghyang`.

    Entry ID: RES-017
    Date: 2026-10-07
    Research question(s) addressed: P2-002, RQ-016
    Finding: Old Javanese Wordnet (OJW) by Moeljadi & Aminullah (2020) provides 5,911 senses and 2,054 synsets mapped to Princeton WordNet 3.0. It uses Zoetmulder (1982) romanization. It is licensed under CC BY 4.0, permitting modification, redistribution, and commercial use. 
    Evidence status: ESTABLISHED
    Evidence type: ORTHOGRAPHIC
    Sources:
      - GitHub: davidmoeljadi/OJW (README.md)
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: OJW is highly suitable and legally cleared as a lexical validation list for the G2P engine, though it lacks phonetic transcriptions.

    Entry ID: RES-018
    Date: 2026-10-07
    Research question(s) addressed: P2-001, RQ-016, RQ-017
    Finding: GRETIL provides a small corpus of romanized Old Javanese texts (e.g., 9 files including *Gaṇapatitattwa*). The texts use a modified IAST romanization. They are derived from mid-20th-century scholarly editions.
    Evidence status: ESTABLISHED
    Evidence type: ORTHOGRAPHIC
    Sources:
      - GRETIL (TextGrid Repository).
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: Usable for sentence-level G2P and normalization testing.

    Entry ID: RES-019
    Date: 2026-10-07
    Research question(s) addressed: P2-003, RQ-019
    Finding: OpenSLR 41 is a multi-speaker Modern Javanese TTS speech corpus (~1.8 GB, audio + transcripts) licensed under CC-BY-SA 4.0. Facebook/Meta's MMS-TTS-JAV is a pre-trained VITS model for Modern Javanese licensed under CC-BY-NC 4.0 (Non-Commercial). 
    Evidence status: ESTABLISHED
    Evidence type: COMPARATIVE
    Sources:
      - OpenSLR 41 repository.
      - Hugging Face model card for `facebook/mms-tts-jav`.
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: OpenSLR 41 provides fully permissible acoustic training data for transfer learning. MMS-TTS-JAV provides a baseline model architecture but is restricted from commercial deployment.

    Entry ID: RES-020
    Date: 2026-10-07
    Research question(s) addressed: P2-003
    Finding: Phoneme compatibility between Profile A (Reconstructed Historical Spoken Old Javanese) and Modern Javanese TTS models:
      - SUPPORTED: /a, i, u, e, o, ə/, /p, b, t, d, ṭ, ḍ, c, j, k, g/, /m, n, ŋ, ɲ/, /w, j, l, r, s, h/. Crucially, Modern Javanese models natively support the Javanese dental/alveolar stop contrast (/t,d/ vs /ṭ,ḍ/).
      - UNSUPPORTED / UNKNOWN: Phonemic long vowels (ā, ī, ū), Sanskrit aspirates (bh, dh, etc.), palatal/retroflex sibilants (ś, ṣ), syllabic liquids (ṛ, ḷ). Modern Javanese lacks these phonemically.
    Evidence status: ESTABLISHED
    Evidence type: COMPARATIVE / PHONOLOGICAL
    Sources:
      - Linguistic comparison of Old Javanese native inventory vs Modern Javanese phonology.
    Conflicting evidence: None.
    Open questions remaining: How will an acoustic model trained on Modern Javanese handle dense, unadapted Sanskrit consonant clusters?
    TTS implication: Modern Javanese TTS architectures or datasets can synthesize the entire native Kawi phoneme inventory perfectly, but any Sanskrit-specific distinctions preserved in the text MUST be merged or mapped by the G2P rules before synthesis.

    Entry ID: RES-021
    Date: 2026-10-07
    Research question(s) addressed: P2-004
    Finding: Data Gap Assessment: 
      - Usable Kawi Text Corpus: YES (GRETIL, OJW).
      - Usable Kawi Speech Corpus: NO.
      - Usable Modern Javanese Transfer Corpus: YES (OpenSLR 41).
    Evidence status: ESTABLISHED
    Evidence type: HISTORICAL
    Sources:
      - Phase 2 Data Audit.
    Conflicting evidence: None.
    Open questions remaining: None.
    TTS implication: The project MUST implement a hybrid architecture: a custom Old Javanese text-normalization and G2P frontend mapping into a Modern Javanese acoustic TTS backend (either zero-shot inference or fine-tuned transfer learning).
