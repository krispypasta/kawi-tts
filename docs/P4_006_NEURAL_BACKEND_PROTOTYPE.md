# P4-006 Neural Backend Prototype

## 1. Exact Model
- **Model Checkpoint:** `id_ID-news_tts-medium.onnx`
- **Config:** `id_ID-news_tts-medium.onnx.json`
- **Size:** 63 MB

## 2. Source
- **Repository:** `rhasspy/piper-voices` (HuggingFace)
- **Path:** `id/id_ID/news_tts/medium/`

## 3. Hashes (SHA256)
- **Model:** `ed8f02aa593f7af6b19acbdb8142e0da0dd72f46194eb33d38e0eb10a52597e8`
- **JSON:** `1ef677072668a5e172e0759b1d3871f129009d1167f093325a17607f7add5ad7`

## 4. Metadata
- **Sample Rate:** 22050 Hz
- **Quality:** medium
- **Language:** id_ID (Indonesian)

## 5. Licensing Status
- **Code:** MIT (using explicit `onnxruntime` bindings locally in Python, avoiding GPL `piper.exe`).
- **Model / Voice License:** UNKNOWN / NEEDS VERIFICATION.
- **Dataset License:** UNKNOWN / NEEDS VERIFICATION.
  - *Note:* The official `MODEL_CARD` provided by the repository incorrectly links to `indic-tts-malayalam-speech-corpus` (a Malayalam corpus), which is impossible for an Indonesian TTS model. We therefore explicitly reject the previous child agent's unverified claim that this model uses Mozilla Common Voice CC0 data until authoritative provenance is located.

## 6. Speaker Metadata
- **Speaker Count:** 1 (`num_speakers: 1` in JSON config).
- **Speaker Identity/Gender (Documented Fact):** The official metadata provides NO explicit statement on gender. It only notes the model was fine-tuned from U.S. English Lessac.
- **Human Perception:** A reference audio file `speaker_0.mp3` exists at the source. Human listening is required to subjectively classify the perceived gender.

## 7. Phoneme Vocabulary
Parsing `id_ID-news_tts-medium.onnx.json` reveals the model utilizes a broad eSpeak-ng IPA vocabulary.
- **SUPPORTED DIRECTLY:** `a`, `i`, `u`, `e`, `o`, `ə`, `ː`, `ʈ`, `ɖ`, `ɳ`, `ŋ`, `ɲ`, `ʃ`, `ʂ`, `ʰ`, `̩`, `r`, `l`, `g`, `b`, `d`, `k`, `t`, `p`
- **NOT PRESENT:** `ʱ` (voiced aspiration hook U+02B1).

## 8. Direct Injection Mechanism
- **Mechanism:** The backend is initialized using standard `onnxruntime` in Python (`src/tts/experimental_piper.py`).
- **Input formatting:** Instead of feeding Indonesian text and relying on a text-to-phoneme dictionary, we map Kawi phoneme characters directly to Piper's internal integer IDs using the `phoneme_id_map` located in the JSON config. This proves that *no upstream linguistic collapse is required to use this neural model*, bypassing Indonesian orthography limits entirely.

## 9. 8-Word Results
The Piper prototype successfully consumed the existing Kawi acoustic representations directly:
- `sĕkar` -> `səkar` -> SUCCESS
- `paḍaṅ` -> `paɖaŋ` -> SUCCESS
- `ghaṇṭā` -> `gʰaɳʈaː` -> SUCCESS (using provisional mapping `ʱ` -> `ʰ`)
- `śānti` -> `ʃaːnti` -> SUCCESS
- `ṣaḍguṇa` -> `ʂaɖguɳa` -> SUCCESS
- `kṛta` -> `kr̩ta` -> SUCCESS
- `sanghyang` -> `sangʰjang` -> SUCCESS (using provisional mapping `ʱ` -> `ʰ`)
- `sang-hyang` -> `sang-hjang` -> SUCCESS

## 10. eSpeak vs. Piper Comparison
*(eSpeak was not generated locally in this session due to a missing host binary, but the Piper output is available for user side-by-side comparison with the existing P4-005 eSpeak files)*.
- **Naturalness:** Human listening required.
- **Accent:** Human listening required.
- **Distinctions:** Piper's JSON map supports retroflexes (`ʈ ɖ ɳ ʂ`), length chronemes (`ː`), and syllabic markers (`̩`). Human listening must verify if the acoustic model actually learned to pronounce these distinctions or if it flattens them internally.

## 11. Unsupported Tokens
- `ʱ` (voiced aspiration hook U+02B1).

## 12. Provisional Mappings
Because the Piper vocabulary completely lacks `ʱ` but includes `ʰ` (voiceless aspiration hook), the following minimal backend-specific mapping was added directly to `ExperimentalPiper` (not the global `AcousticMapper`):
- `ʱ` -> `ʰ`
- *Note:* This preserves the aspirated nature of the stop and ensures the global eSpeak tests remain 100% intact. It is classified as a backend limitation work-around.

## 13. Naturalness Observations
- Requires human listening evaluation of the `artifacts/piper_prototype/` WAV files.

## 14. Accent Observations
- Requires human listening evaluation.

## 15. Limitations
- Unverified provenance and dataset license prevent this checkpoint from being shipped in a distributable V1 release without further legal clearance.
- It is unknown if the `id_ID` dataset actually contained acoustic data for retroflex sounds (despite having the symbols in the map), meaning the output may acoustically collapse retroflexes to alveolars even if the tokens are correctly injected.

## 17. P4-006D: Lossy Backend Adaptation Experiment
To evaluate if model-facing approximations improve acoustic stability, a backend-specific lossy mapping layer was introduced inside `ExperimentalPiper` (leaving canonical `AcousticMapper` untouched). This experiment was driven by P4-006C findings where `kṛta` collapsed into near silence (0.163s).

### Mappings Tested
- **Retroflexes:** `ʈ ɖ ɳ` → `t d n`
- **Sibilants:** `ʂ ʃ` → `s`
- **Syllabic Liquid:** `r̩` → `rə`
- **Vowel Length:** `ː` was preserved, as early testing showed no structural collapse.
- **Aspiration:** `ʱ` → `ʰ` (preserved from P4-006C).

### Results (Length Scale = 1.2)
- **sĕkar:** Direct=0.453s | Lossy=0.453s
- **paḍaṅ:** Direct=0.476s | Lossy=0.522s
- **ghaṇṭā:** Direct=0.441s | Lossy=0.592s
- **śānti:** Direct=0.522s | Lossy=0.441s
- **ṣaḍguṇa:** Direct=0.511s | Lossy=0.360s
- **kṛta:** Direct=0.163s | Lossy=0.488s
- **sanghyang:** Direct=0.604s | Lossy=0.604s
- **sang-hyang:** Direct=0.604s | Lossy=0.592s

**Initial Observations:**
- The severe collapse of `kṛta` was successfully rescued by approximating `r̩` as `rə` (duration increased from 0.163s to 0.488s).
- Differences in other words suggest the model responds differently to the substituted tokens, requiring human evaluation to determine whether naturalness and intelligibility genuinely improved.
- *Crucially, these substitutions are EXPERIMENTAL MODEL LIMITATIONS, not historical claims. They are isolated strictly within the Piper runtime and do not modify the canonical G2P representation.*

## 18. P4-006E: Neural Backend Evaluation & Candidate Decision
Following human perceptual review (P4-006E), the candidate model (`id_ID-news_tts-medium`) was formally evaluated against both objective and subjective metrics.

### Objective vs. Perceptual Reconciliation
While objective measurements (RMS, amplitude, duration) showed "healthy" waveforms for most words, human listening exposed catastrophic phonetic collapse across the board. The model accepts Kawi phonemes structurally but drops or mangles them acoustically.

- **`sĕkar`** → Perceived: "saa"
- **`paḍaṅ`** → Perceived: "'a"
- **`ghaṇṭā`** → Perceived: "a'ang"
- **`śānti`** → Perceived: "aying"
- **`ṣaḍguṇa`** → Perceived: "tung/dung"
- **`kṛta`** → Perceived: "krha/krtha" (The only successful rescue, via `r̩` → `rə`)
- **`sanghyang`** → Perceived: "sangnyang" / "tangyang" (Exposed an upstream G2P `gʱ` parsing bug)
- **`sang-hyang`** → Perceived: "hangang"

### Special Cases Identified
- **Vowel Length (`ː`):** Although accepted by the model conceptually, human listening (`ghaṇṭā` → "a'ang") proves it contributes to acoustic collapse.
- **Aspiration (`ʱ` → `ʰ`):** A strict backend workaround that fails to yield intelligible consonants in this checkpoint.
- **G2P Bug:** The audible difference between `sanghyang` and `sang-hyang` objectively verified that the canonical pipeline preserves inputs up to the backend, but exposed a greedy monograph/digraph bug mapping unhyphenated `gh` to `gʱ`. (This bug is isolated to G2P and must be fixed separately; it does not excuse the Piper model's failure to render the resulting tokens).

### Final Candidate Evaluation
**C. REJECT AS PRIMARY BACKEND**
Despite providing a valid structural test harness to validate the Kawi pipeline, the Indonesian model fails acoustically. It cannot reliably render non-Indonesian consonant clusters, aspirations, or complex syllabic structures, resulting in unintelligible vowel-mush ("saa", "'a"). Lossy adaptation does not rescue it enough to be useful. 

### Fine-Tuning Gate
**Not Recommended.** 
Fine-tuning this model is rejected for three reasons:
1. The baseline fails too fundamentally (dropping base consonants like `k` in `sĕkar`) to serve as a meaningful foundation.
2. The dataset provenance and licensing are unverified and likely un-releasable.
3. Synthetic Old Javanese audio data does not exist to supervise a fine-tune.

### Next Steps
- Remove `id_ID-news_tts-medium` as a candidate for the primary V1 release.
- Fix the `sanghyang` greedy G2P digraph bug.
- Return to eSpeak as the primary, highly-reliable acoustic baseline for V1 structural testing.
