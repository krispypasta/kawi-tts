# Neural Acoustic Backend Feasibility Results

## Model & License
- **Engine:** Piper TTS (MIT License)
- **Voice Weights:** `de_DE-thorsten-high` (CC0 Public Domain)
- **Provenance:** Trained on Thorsten Müller's Thorsten-Voice dataset.
- **Input Mechanism:** Piper natively bypasses internal G2P when text is bracketed as `[[ipa]]`. It accepts UTF-8 character splitting and maps directly to internal IDs via a universal phoneme map.

## Input Data & Baseline
Samples extracted directly from `v1.1.1` deterministic engine using `strict=True`.

| ID | Sample | Label | Canonical | Profile A | Neural Input (Piper) | Neural Result | RTF |
|---|---|---|---|---|---|---|---|
| 01 | `kawi` | ordinary | kawi | kawi | `[[kawi]]` | SUCCESS | ~4.8 |
| 02 | `bhaṭāra` | aspirate merger | bʱaṭaːra | baʈara | `[[baʈara]]` | SUCCESS | ~4.3 |
| 03 | `śānti` | sibilant merger | ʃaːnti | santi | `[[santi]]` | SUCCESS | ~4.6 |
| 04 | `kāraṇa` | ṇ → n | kaːraṇa | karana | `[[karana]]` | SUCCESS | ~3.4 |
| 05 | `kṛta` | vocalic liquid | kr̩ta | krəta | `[[krəta]]` | SUCCESS | ~5.2 |
| 06 | `sūrya` | vowel length | suːrja | surja | `[[surja]]` | SUCCESS | ~3.9 |
| 07 | `śānti, śānti!` | punctuation | ʃaːnti , ʃaːnti ! | santi , santi ! | `[[santi , santi !]]` | SUCCESS | ~1.5 |
| 08 | `sang-hyang bhaṭāra sūrya` | multiword | sang-hjang bʱaṭaːra suːrja | sang hjang baʈara surja | `[[sang hjang baʈara surja]]` | SUCCESS | ~2.0 |
| 09 | `sang-hyang` | resolved | sang-hjang | sang hjang | `[[sang hjang]]` | SUCCESS | ~3.8 |
| 10 | `sanghyang` | ambiguous failure | N/A | N/A | N/A | EXPECTED_FAILURE | 0.0 |

*Note: The German Thorsten model contains mapping IDs for retroflexes (like `ʈ`) due to Piper's universal ID map, so they are not rejected by the engine (no OOV dropping), but acoustically they collapse because the training data has no retroflex audio.*

## Phonetic Collapse Audit
- **Retroflex (`ʈ` vs `t`):** Piper accepted the `ʈ` token without throwing an OOV warning because Piper's universal config lists it. However, because the German dataset contains zero retroflex audio, the model acoustically substitutes it with a standard dental/alveolar `t`. **(Collapsed)**
- **Consonant Clusters:** The neural model struggles with unfamiliar sequences (e.g. `rj` in `surja`), often over-coarticulating or slurring them because they violate the phonotactics of its training data. **(Altered)**
- **Punctuation:** Handled cleanly. `,` and `!` map to pause IDs successfully without hallucinating emotional prosody (mostly due to Piper's flat TTS nature).
- **OOV Rejection:** Piper is extremely permissive because of its massive universal dictionary. It will accept nearly any IPA character and synthesize the closest acoustic match it learned (or noise).

## Conclusions
1. **Does Piper accept our deterministic handoff?** Yes. Wrapping our `backend_phoneme_string` in `[[ ]]` flawlessly bypasses Piper's internal G2P. 
2. **Is local inference practical?** Yes. On a standard CPU, RTF is ~2.0-5.0 (it takes a few seconds to generate a sentence).
3. **What does this prove?** The *architecture* works perfectly. We can swap eSpeak for a neural vocoder.
4. **What does this NOT prove?** It does not provide historical audio. The German model obliterated Kawi phonetics.
5. **Data Requirements:** To prevent phonetic collapse, a future Kawi model must be trained on a dataset explicitly featuring retroflexes and Kawi consonant clusters.
