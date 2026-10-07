# P4-006 Neural Backend Selection

## 1. Selected Candidate
**Piper / VITS** (Concrete Checkpoint: `id_ID-news_tts-medium.onnx`)

## 2. Evidence for Selection
- **Explicit Phonetic Control:** Piper allows bypassing its text-to-phoneme dictionary entirely via explicit `[[ phoneme ]]` injection. Unlike F5-TTS (which is a black-box text guesser), Piper can accurately render explicit phonemes dictated by the Acoustic Mapper.
- **Compute Efficiency:** The ONNX checkpoint is ~63 MB and runs faster than real-time on a standard CPU. No GPU required.
- **Architectural Safety:** It can sit cleanly beside the `ESpeakBackend` as a secondary testing output without requiring modifications to the core G2P rules.

## 3. Licensing
- **Code:** MIT (via older `rhasspy/piper` repository or raw `onnxruntime`).
- **Model / Dataset Weights:** The `id_ID-news_tts` dataset is built on **Mozilla Common Voice (Indonesian)**, which is **CC0 (Public Domain)**. 
- **ShareAlike Avoidance:** By using Common Voice rather than OpenSLR 41 for this initial test, the prototype avoids all CC BY-SA "ShareAlike" contamination. The prototype is 100% commercially and legally clear.

## 4. Speaker
The `news_tts-medium` voice is female (finetuned zero-shot from the English Lessac female dataset into Indonesian). It is a single-speaker checkpoint.

## 5. Compatibility
The model accepts explicit eSpeak-ng format phonemes via `[[ ... ]]`. However, because it is an Indonesian (`id_ID`) checkpoint, it strictly expects the phonemic inventory of modern Indonesian. Out-of-vocabulary (OOV) tokens will cause inference failures.

## 6. Mapper Strategy
The Kawi frontend will NOT change. Instead, the `AcousticMapper` will receive a new backend profile (e.g., `Profile="Neural_ID"`). This profile will explicitly enforce backend-specific collapses:
- **Aspirates:** `bʱ/dʱ/gʱ/ṭʰ/pʰ` → `b/d/g/t/p`
- **Retroflexes:** `ṭ/ḍ/ṇ/ṣ` → `t/d/n/s` (Modern Indonesian lacks the retroflex/dental contrast).
- **Vowel Length:** `aː/iː/uː` → `a/i/u`
- **Sibilants:** `ś/ʃ` → `s`
- **Vocalic Liquids:** `r̩` → `rə`

All such mappings will be logged with a new `MappingStatus.NEURAL_COLLAPSED` status to make the information loss explicit and visible, preventing it from being confused with historical fact.

## 7. Experiment Scope
The minimal prototype will:
1. Initialize the Kawi G2P pipeline.
2. Route the 8-word matrix (`sĕkar`, `paḍaṅ`, `ghaṇṭā`, `śānti`, `ṣaḍguṇa`, `kṛta`, `sanghyang`, `sang-hyang`) through the new `Neural_ID` Acoustic Mapper.
3. Validate the phoneme strings output by the Mapper.
4. Pass the collapsed strings into the Piper ONNX runtime.
5. Generate 8 corresponding `neural_test_X.wav` files alongside the eSpeak files.

## 8. Risks
- **Acoustic Drift:** The output will sound like modern Indonesian. The loss of Kawi retroflexes and aspirates will be aurally obvious. (This is acceptable, as the pipeline proves the architecture works; restoring the sounds is a future fine-tuning task).
- **GPL Contamination:** If the modern GPL-licensed `piper` binary is used directly in a distributed app, it triggers GPL constraints. (Mitigated by invoking it only in local testing or using MIT `onnxruntime` bindings).

## 9. Rejected Candidates
- **Kokoro-82M:** Rejected. Lacks an Indonesian/Javanese acoustic mapping. Feeding Kawi IPA to an English/Japanese voice preset forces heavy cross-lingual accents.
- **F5-TTS:** Rejected. Black-box Flow Matching architecture ignores explicit phonetic control, violating the project's evidence-based pronunciation traceability.
- **Meta MMS:** Rejected. CC BY-NC 4.0 license is non-commercial and restrictive. Fixed vocabulary prohibits custom mapping.

## 10. Human Decisions Required
- **Decision 1:** Approve the use of an Indonesian (`id_ID`) CC0 Piper checkpoint as the first neural integration test.
- **Decision 2:** Approve the explicit, tracked collapse of Kawi-specific phonemes (e.g., `ṭ` -> `t`) strictly within the `AcousticMapper` to satisfy the Indonesian model's vocabulary limits.

## 11. Reproducibility
The prototype will use a deterministic ONNX inference script (`src/tts/piper_backend.py`) interacting with the standard pipeline via Python. No black-box cloud APIs will be used.