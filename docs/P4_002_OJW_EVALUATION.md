# P4-002: High-Throughput G2P Lexical Evaluation Report (Old Javanese Wordnet)

**Date:** 2026-10-07
**Mode:** Engineer / Builder
**Evaluation Dataset:** Old Javanese Wordnet (`wn-kaw.tab`)
**Status:** EVALUATION COMPLETE — 99.90% Representation Coverage

---

## 1. Dataset Provenance & Metadata

* **Repository:** `https://github.com/davidmoeljadi/OJW`
* **Commit SHA:** `e87a6102baaedd190f2f3a81b7d63c4c6722118f`
* **File Path (Raw):** `data/raw/wn-kaw.tab`
* **File SHA-256:** `fc208d9f8f8a005b9e4d4529e313c365ec469104736ba2586e045769889c4ade`
* **File Size:** 157,520 bytes
* **Retrieval Date:** 2026-10-07
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Scholarly Citation:**
  > David Moeljadi and Zakariya Pamuji Aminullah (2020). *Building the Old Javanese Wordnet*. In *Proceedings of the 12th Language Resources and Evaluation Conference (LREC 2020)*, pages 2940–2946. European Language Resources Association (ELRA).
* **Lexicographic Base:** Digitized version of P.J. Zoetmulder & S.O. Robson (1982), *Old Javanese–English Dictionary* (OJED).

---

## 1.1 Epistemic Scope: Representation Coverage vs. Pronunciation Certainty

This evaluation strictly measures **symbolic front-end representation coverage**.
It does **NOT** measure or establish:
1. **Pronunciation Correctness:** No historical spoken recordings survive from the classical period. The internal phonemes represent an evidence-grounded reconstruction (Profile A), not proven historical fact.
2. **Real Acoustic Synthesis Coverage:** eSpeak-ng is not installed on this host environment; synthesis was verified via deterministic mock/dry-run execution. Real acoustic quality has not been evaluated.
3. Successful parsing of a word (e.g., *bhaṭāra* $\to$ `['bʱ', 'a', 'ṭ', 'aː', 'r', 'a']`) demonstrates that our normalization, tokenization, G2P, and acoustic mapper can **losslessly represent and process** the word without crashing or dropping distinctions. It does not prove that 9th-century speakers pronounced aspirates or vowel length identically to the backend IPA representation.

---

## 2. Actual Measured Dataset Counts

The raw dataset structure was parsed directly. Counting rules distinguish Princeton WordNet sense mappings from unique Old Javanese lexical vocabulary:

```text
Row Format: synset_id <TAB> relation_tag <TAB> lemma <TAB> [variants]
```

| Metric | Measured Value | Methodology / Counting Rule |
| :--- | :--- | :--- |
| **Total Raw Lines** | **5,020** | Total lines in `wn-kaw.tab` (1 header comment line + 5,019 data rows). |
| **Data Rows (Senses)** | **5,019** | Non-header tab-delimited records mapping a synset to a lemma. |
| **Unique Synsets** | **2,032** | Distinct Princeton WordNet 3.0 synset IDs (Column 0). |
| **Unique Lemmas** | **3,632** | Distinct primary headwords (Column 2). |
| **Unique Variants** | **569** | Distinct alternative spellings split by comma (Column 3). |
| **Total Unique Lexical Forms** | **4,192** | Deduplicated set union of all unique lemmas and unique variants ($\text{Lemmas} \cup \text{Variants}$). |

*Note on earlier estimates:* The 2020 paper reports 5,911 senses and 2,054 synsets; the pinned repository release evaluated here contains 5,019 data rows and 2,032 unique synsets (yielding **4,192 unique Old Javanese lexical strings**). This evaluation uses the pinned repository release as the reproducibility target.

---

## 3. High-Throughput Evaluation Metrics

Every one of the **4,192 unique Old Javanese lexical forms** was evaluated through the complete front-end pipeline:
$$\text{Raw Form} \xrightarrow{\text{P3-002}} \text{normalize()} \xrightarrow{\text{P3-004}} \text{tokenize()} \xrightarrow{\text{P3-003B}} \text{g2p\_word()} \xrightarrow{\text{P3-006}} \text{map\_phonemes()}$$

### Summary Scorecard

| Evaluation Metric | Measured Count | Percentage | Status |
| :--- | :--- | :--- | :--- |
| **Total Evaluated Forms** | 4,192 | 100.00% | Complete |
| **Normalization Success** | 4,192 | 100.00% | PASS |
| **Tokenization Success** | 4,192 | 100.00% | PASS |
| **Single-Word Tokens** | 3,977 | 94.87% | PASS |
| **Multi-Word / Compounds** | 215 | 5.13% | PASS (cleanly segmented) |
| **Structural Ambiguities** | 0 | 0.00% | Zero unresolved trigraphs |
| **G2P Engine Success** | 4,192 | 100.00% | PASS (0 crashes) |
| **Acoustic Mapping Success** | 4,192 | 100.00% | PASS (0 crashes) |
| **Forms with Unsupported Chars** | 4 | 0.095% | 4 rare philological characters |
| **Fully Supported Lexical Forms** | **4,188** | **99.90%** | **PASS (Exceeds Target)** |
| **Forms with Provisional Mappings**| 409 | 9.76% | Stamped & audited |
| **Total Provisional Tokens** | 430 | — | Audited |
| **Runtime Exceptions / Crashes** | 0 | 0.00% | Zero errors |

---

## 4. Failure Categories & Unsupported Character Inventory

Across 4,192 vocabulary items, exactly **4 words (0.095%)** encountered unsupported characters. Every failure was audited:

| Form | Unsupported Grapheme | Linguistic / Philological Context | Failure Category |
| :--- | :--- | :--- | :--- |
| **tīrthâṅga** | `â` (U+00E2) | Circumflex marking vowel crasis / sandhi coalescence ($a + a \to \hat{a}$). | `UNSUPPORTED_GRAPHEME` |
| **aṅipîpi** | `î` (U+00EE) | Circumflex marking internal vowel fusion / coalescence ($i + i \to \hat{i}$). | `UNSUPPORTED_GRAPHEME` |
| **bhraṃśa** | `ṃ` (U+1E43) | Indic Anusvara representing homorganic nasal in Sanskrit loan. | `UNSUPPORTED_GRAPHEME` |
| **āśiḥ** | `ḥ` (U+1E25) | Indic Visarga representing unvoiced glottal aspiration in Sanskrit loan. | `UNSUPPORTED_GRAPHEME` |

### Architectural Handling of Unsupported Characters
Per project policy (**Information Preservation First**):
* The G2P engine and Acoustic Mapper do **not** crash or silently delete these characters.
* The character is preserved as itself and flagged under `unsupported_tokens` on the resulting mapping structure with the diagnostic note: `"Unsupported token '<char>' in acoustic mapper."`
* Because this affects fewer than 0.1% of lexical forms, resolving them does not block Phase 4 and is deferred to normalizer/sandhi enhancement.

---

## 5. Information-Preservation Audit across OJW

The evaluation verified that no phonological distinctions are collapsed or erased across the entire lexicon. The table below documents the distribution of distinctive features successfully preserved across the 4,192 words:

| Linguistic Category | Forms in OJW | % of OJW | Preservation Behavior |
| :--- | :--- | :--- | :--- |
| **Long Vowels ($\bar{a}, \bar{i}, \bar{u}$)** | 729 | 17.39% | Preserved distinctly with chroneme `ː` ($aː, iː, uː \neq a, i, u$). |
| **Pepet ($\breve{e} / \text{ə}$)** | 678 | 16.17% | Preserved distinctly as mid-central schwa $/ə/$. |
| **Long Pepet ($\ddot{o}$)** | 30 | 0.72% | Preserved distinctly as $/əː/$; flagged `PROVISIONAL`. |
| **Sibilants ($\text{ś}, \text{ṣ}$)** | 366 | 8.73% | Preserved distinctly as postalveolar $/ʃ/$ and retroflex $/ʂ/$ ($\neq s$). |
| **Aspirates ($bh, dh, gh, ph, kh$, etc.)** | 353 | 8.42% | Preserved greedily as single phoneme units ($\neq \text{plain stop}$). Voiced aspirates flagged `PROVISIONAL`. |
| **Retroflex Stops ($\text{ṭ}, \text{ḍ}$)** | 251 | 5.99% | Preserved distinctly as retroflex $/ʈ/, /ɖ/$ ($\neq t, d$). |
| **Retroflex Nasal ($\text{ṇ}$)** | 200 | 4.77% | Preserved distinctly as retroflex $/ɳ/$ ($\neq n$). |
| **Vocalic Liquids ($\text{ṛ}, \text{ḷ}$)** | 86 | 2.05% | Preserved distinctly as $/r̩/, /l̩/$; flagged `PROVISIONAL`. |
| **Velar Nasal ($\text{ṅ} / \text{ŋ}$)** | 880 | 20.99% | Normalized and parsed cleanly to $/ŋ/$. |
| **Palatal Nasal ($\text{ñ}$)** | 113 | 2.70% | Parsed cleanly to $/ɲ/$. |

---

## 6. Multi-Word Lemmas & Compounds

215 entries (5.13%) in OJW contain multiple words, spaces, or hyphens:
- **Reduplications & Hyphenated Compounds:** e.g. *acala-calan*, *adal-adal*, *akĕla-kĕlan*, *alaku-laku*.
- **Phrasal Entries:** e.g. *abaṅ wetan* ("eastern red").
- The tokenizer correctly segments hyphens as `TokenType.BOUNDARY` and spaces as `TokenType.WHITESPACE`, isolating word units cleanly and passing each to G2P without false cross-boundary character fusion.

---

## 7. Machine-Readable Artifact

The full evaluation data structure was exported to:
`data/processed/ojw_coverage_report.json`

The JSON report includes all raw counts, percentages, rule frequency dictionaries, lists of multi-word forms, and failure records.

---

## 8. Reproducibility

To re-run the evaluation harness and regenerate the report at any time:

```bash
python -m src.evaluation.evaluate_ojw
```

Automated regression tests verify the dataset stats and coverage thresholds:

```bash
python -m unittest tests/test_evaluation.py
```

---

## 9. Conclusion

Task **P4-002 is COMPLETE**. The Kawi-TTS front-end successfully demonstrated **99.90% current symbolic representation / acoustic-mapper execution coverage for the pinned lexical inventory** across all unique lexical forms in the Old Javanese Wordnet, with zero runtime exceptions and zero information loss in the internal representation. Real acoustic synthesis and historical pronunciation accuracy remain separate, unverified dimensions.
