# P5-003: Profile Architecture Design & Vowel Length Strategy

## 1. Rationale
The P5-002 Acoustic Profile Policy established that Kawi-TTS must support multiple distinct acoustic realizations of the same canonical text: **Profile A** (Historical Spoken, containing evidence-backed acoustic mergers) and **Profile B** (Scholarly/Orthographic Reading, preserving textual distinctions). 

V1 implementation tightly coupled canonical mapping to a single set of backend acoustic mappings, effectively forcing the system into Profile B. P5-003 designs the necessary architectural abstraction to support Profile A without violating the losslessness of the G2P engine or destroying V1 backward compatibility. It also addresses the etymological ambiguity of vowel length (macrons).

## 2. Conceptual Architecture Diagram

```text
[Input Text: "śānti"]
      ↓
[Normalizer & Tokenizer]
      ↓
[G2P Engine (Lossless)]
  Outputs Canonical Representation (Profile-Independent)
  e.g., ["ś", "ā", "n", "t", "i"]
      ↓
=========================================================
[Profile Strategy Layer] (NEW ABSTRACTION)
  Selects linguistic interpretation rules.
  
  → ProfileAStrategy: Merges historical phonemes.
    ["s", "ā", "n", "t", "i"] (citation: P5-002 Sibilant Merger)
    
  → ProfileBStrategy: Passes through text unchanged.
    ["ś", "ā", "n", "t", "i"] (citation: P5-002 Scholarly Reading)
=========================================================
      ↓
[Acoustic Mapper]
  Translates interpreted phonemes into exact backend format.
  e.g., Profile A "s" -> eSpeak [s]
  e.g., Profile B "ś" -> eSpeak [ʃ]
      ↓
[Backend Synthesizer (eSpeak/Neural)]
```

## 3. Layer Responsibilities

*   **Canonical Representation (`g2p.engine`):** Must remain strictly lossless and profile-ignorant. It emits a canonical array that preserves all orthographic distinctions.
*   **Profile Strategy Layer (`AbstractProfileStrategy`):** A new linguistic routing layer. It transforms canonical tokens based on the active historical profile, emitting `ProfiledToken`s that carry the original canonical phoneme, the realized phoneme, and the policy citation justifying the transformation.
*   **Acoustic Mapper (`AcousticMapper`):** Acts as a pure dictionary translation layer. It is ignorant of whether an upstream merger occurred. It merely maps the realized phonemes from the Strategy Layer into backend-specific formats (e.g., eSpeak IPA).
*   **Pipeline Result (`PipelineResult`):** Records both the untouched canonical `g2p_phonemes` and the transformed `backend_phoneme_string`, preventing uncertainty or downstream backend limitations from destroying the true structural audit trail.

## 4. Profile Behavior Matrices

### Profile A: Reconstructed Historical Spoken
*   **Aspirates (`bʱ`, `dʱ`, etc.):** Merged to plain stops (`b`, `d`). Citation: P5-002 (Van der Molen, Teselkin).
*   **Sibilants (`ś`, `ṣ`):** Merged to native sibilant (`s`). Citation: P5-002 (Teselkin).
*   **Syllabic Liquids (`r̩`, `l̩`):** Provisionally adapted to schwa + liquid (`rə`, `lə`). Citation: P5-002 (Acri & Griffiths).
*   **Dental vs. Retroflex:** Preserved as distinct.
*   **Vowel Length:** Deferred (see Section 6).

### Profile B: Scholarly / Orthographic Reading
*   **Aspirates (`bʱ`, `dʱ`, etc.):** Preserved distinctly.
*   **Sibilants (`ś`, `ṣ`):** Preserved distinctly.
*   **Syllabic Liquids (`r̩`, `l̩`):** Preserved as syllabic.
*   **Dental vs. Retroflex:** Preserved as distinct.
*   **Vowel Length:** Preserved as distinct duration.

## 5. Architectural Invariants
1.  **G2P Losslessness:** `g2p.engine` must not know about Profiles. It cannot delete information.
2.  **Traceability:** Every phoneme altered by a Profile Strategy must be encapsulated in a `ProfiledToken` containing a strict `rule_citation`. No silent deletions are permitted.
3.  **Backend Ignorance:** The Acoustic Mapper cannot contain linguistic reconstruction logic. It only executes 1:1 format conversions for the synthesizer.

## 6. Vowel Length Strategy

Old Javanese orthography uses macrons (`ā`, `ī`, `ū`) for both Sanskrit metrical length (e.g., *śānti*) and native Austronesian contractions/stress. 
*   **Problem:** At the canonical string level, the two origins are indistinguishable.
*   **Profile B Strategy:** Safely implemented immediately. Profile B maximizes orthographic reflection, thus all macrons map to phonemic duration (e.g., `[aː]`).
*   **Profile A Strategy:** Structurally deferred. P5-002 prohibits a universal rule because Sanskrit loanword macrons were historically neglected, while native macrons carried phonetic reality. A universal reduction destroys native speech, while universal preservation falsifies loans.
*   **Resolution:** Vowel length realization in Profile A remains unresolved until V2 introduces an **Etymological Tagging / Lexical Metadata Layer** (e.g., using OJW dictionary lookups to flag tokens as `[+loan]` vs. `[+native]`). The G2P will continue emitting `/aː/`, and Profile A will currently pass it through unreduced until the tagging layer is available to make token-aware reductions.

## 7. V1 Compatibility & Safety Assessment

The introduction of the `ProfileStrategy` layer **will not break the V1.0.0 frozen baseline**.
*   **Safety Proof:** Currently, `AcousticMapper(profile="A")` accepts a parameter but relies on hardcoded `_PRESERVED_MAP` and `_PROVISIONAL_MAP` dictionaries that enforce Profile B behavior. In V2, these hardcoded maps will be extracted directly into a `ProfileBStrategy` class. 
*   Existing V1 tests will be updated to explicitly invoke `profile="B"`. Because `ProfileBStrategy` passes canonical tokens through identically to the old mapping dictionaries, the V1 pipeline's inputs, internal tracking, and eSpeak IPA outputs will remain mathematically identical. 

## 8. Future Implementation Plan (V2 Roadmap)

The transition to V2 will execute the following technical plan without modifying G2P:
1.  **Extract Strategies:** Move `_PROVISIONAL_MAP` logic from `src/acoustic/mapper.py` into a new `src/acoustic/strategies/profile_b.py`.
2.  **Implement Profile A:** Create `src/acoustic/strategies/profile_a.py` implementing the aggressive merger rules with `ProfiledToken` citations.
3.  **Refactor Mapper:** Convert `AcousticMapper` into a context object that routes `map_token()` calls to the injected strategy.
4.  **Test Matrix:** Add `test_profile_a_strategy.py`, `test_profile_b_strategy.py`, and update `test_integration.py` to assert that identical input text produces identical `PipelineResult.g2p_phonemes` but diverges in `backend_phoneme_string`.
5.  **Lexical Tagger (Post-V2.0):** Design the dictionary lookup system required to unblock the Profile A Vowel Length strategy.