# Neural Acoustic Backend Feasibility Results (Female Voice)

## Model & License
- **Candidate Selected:** `en_US-ljspeech-high`
- **Engine:** Piper TTS
- **Gender:** Female
- **License:** MIT (Engine) / CC0 Public Domain (Weights and Dataset)
- **Provenance:** Trained from scratch by rhasspy on the LibriVox LJSpeech corpus (public domain).
- **Input Mechanism:** Piper natively bypasses internal G2P when text is bracketed as `[[ipa]]`. It explicitly accepts phoneme characters and maps them to internal IDs via a universal map.

## Input Path & Pipeline Isolation
The pipeline is strictly isolated from production code:
1. `Kawi text` (e.g. `bhaṭāra`)
2. → `frozen v1.1.1 canonical representation` (`bʱaṭaːra`)
3. → `Profile A` (merging aspirates)
4. → `deterministic acoustic representation` (`baʈara`)
5. → `experiment-only adapter` (`run_female_experiment.py`)
6. → `female neural model input` (`[[baʈara]]` bypassing LJSpeech G2P)
7. → `WAV output`

## Input Data & Baseline
Samples extracted directly from `v1.1.1` deterministic engine using `strict=True`.

| ID | Sample | Label | Canonical | Profile A | Neural Input (Piper) | Neural Result | RTF |
|---|---|---|---|---|---|---|---|
| 01 | `kawi` | ordinary | kawi | kawi | `[[kawi]]` | SUCCESS | ~8.0 |
| 02 | `bhaṭāra` | aspirate merger | bʱaṭaːra | baʈara | `[[baʈara]]` | SUCCESS | ~4.7 |
| 03 | `śānti` | sibilant merger | ʃaːnti | santi | `[[santi]]` | SUCCESS | ~5.4 |
| 04 | `kāraṇa` | ṇ → n | kaːraṇa | karana | `[[karana]]` | SUCCESS | ~4.8 |
| 05 | `kṛta` | vocalic liquid | kr̩ta | krəta | `[[krəta]]` | SUCCESS | ~4.7 |
| 06 | `sūrya` | vowel length | suːrja | surja | `[[surja]]` | SUCCESS | ~5.2 |
| 07 | `śānti, śānti!` | punctuation | ʃaːnti , ʃaːnti ! | santi , santi ! | `[[santi , santi !]]` | SUCCESS | ~1.8 |
| 08 | `sang-hyang bhaṭāra sūrya` | multiword | sang-hjang bʱaṭaːra suːrja | sang hjang baʈara surja | `[[sang hjang baʈara surja]]` | SUCCESS | ~2.1 |
| 09 | `sang-hyang` | resolved | sang-hjang | sang hjang | `[[sang hjang]]` | SUCCESS | ~3.2 |
| 10 | `sanghyang` | ambiguous | N/A | N/A | N/A | EXPECTED_FAILURE | N/A |

## Phonetic Collapse Audit (Comparison to eSpeak Baseline)
As predicted by the child-agent phonetic audit, while the deterministic interface functions flawlessly, the acoustic model fundamentally collapses unsupported foreign sounds:

1. **Retroflex Preservation (`ṭ` vs `t`, `ḍ` vs `d`):** Like the German male experiment, the English female model fails completely to synthesize `ṭ` (`bhaṭāra`). Piper's universal map silently routes `ʈ` to the closest sound the model knows, resulting in a standard English alveolar `/t/` or a distorted drop. **(Collapsed)**
2. **Schwa Behavior (`ə`):** The English model interprets the schwa (`krəta`) heavily through its own stress rules, making it unstable. It often sounds swallowed or artificially lengthened, destroying Kawi's natural rhythm.
3. **Consonant Clusters:** Unfamiliar clusters (e.g. `rj` in `sūrya`) cause unnatural coarticulation or epenthesis (inserting small ghost vowels to make the cluster pronounceable in English phonotactics).
4. **Punctuation:** Processed natively and cleanly.
5. **Intelligibility vs. Naturalness:** The voice itself sounds extremely smooth, natural, and human-like compared to the robotic eSpeak baseline, but it completely mangles the Kawi pronunciation intended by Profile A.

## Decision: B (FEMALE MODEL IS NATURAL BUT PHONETICALLY UNSAFE)
**Conclusion:** The experiment was a technical success—demonstrating that a completely deterministic IPA stream can be fed successfully to a modern permissive VITS architecture locally via CPU. However, linguistically, the `en_US-ljspeech` model is **phonetically unsafe** and heavily distorts Kawi invariants. 

It sounds better than eSpeak but destroys too many preserved Kawi distinctions. A future neural Kawi experiment is architecturally viable, but only when a Kawi-specific or Indo-Aryan-trained permissive model becomes available.
