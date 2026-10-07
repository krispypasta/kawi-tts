# P4-006 Acoustic Backend Research

## 1. Motivation
The Kawi-TTS system requires a natural-sounding, preferably female, acoustic backend to fulfill Profile A (reconstructed spoken Old Javanese). While the baseline backend proves the pipeline works, its robotic quality obscures the nuanced phonological reconstruction. The objective is to identify a neural TTS candidate that improves naturalness without violating the core principle of linguistic traceability.

## 2. Current eSpeak Baseline
- **Backend:** eSpeak-NG 1.52.0
- **Voice:** Indonesian (`id`) fallback (due to missing `jv` voice).
- **Status:** Functioning. It successfully reads the Kawi-TTS custom IPA tokens losslessly through the `[[ ]]` inline interface. It will be retained permanently as the structural reference baseline.

## 3. Problem Demonstrated by Human Listening
Human listening tests (mechanical verification) confirm that while the pipeline accurately transmits IPA tokens, the eSpeak `id` voice is highly robotic. It acts as an engineering prototype rather than a natural linguistic realization, making it difficult to evaluate the true auditory quality of the reconstructed Old Javanese.

## 4. Requirements for a Better Backend
- Must accept a custom phoneme/IPA input vocabulary.
- Must not require collapsing the upstream Kawi G2P internal representation.
- Must support a female speaker.
- Must have open, commercial-friendly licensing (e.g., MIT, Apache 2.0, CC-BY, CC0).
- Must have clear dataset provenance.
- Must allow local inference on consumer hardware.

## 5. Candidate Categories
- **Zero-Shot / Flow Matching:** F5-TTS
- **Lightweight Multilingual:** Kokoro-82M
- **Custom-Vocabulary Architectures:** VITS / Piper
- **Fixed-Vocabulary Multilingual:** Meta MMS, XTTS v2

## 6. Candidate Comparison Matrix

| Candidate | Language Support | Female Speaker | Naturalness | Input Type | Phoneme Control | Kawi Compatibility | Required Mapper Loss | License | Dataset Rights | Fine-Tuning | Compute | Reproducibility | Risk | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **VITS / Piper** | ID / JV models exist | Yes (OpenSLR 41) | Medium-High | Phoneme IDs | Perfect (Custom Vocab) | Perfect | None (if fine-tuned) | MIT | CC BY-SA 4.0 | Feasible (4-8h) | Low | High | Training overhead | GREEN |
| **F5-TTS** | Zero-Shot (Agnostic) | Yes (via Reference) | High (SOTA) | Text / IPA | High | High | Low | MIT | CC0 (Reference) | Optional | High (GPU) | High | Compute constraints | YELLOW |
| **Kokoro-82M** | 9 Langs (No ID/JV) | Yes (Presets) | High | IPA | High | High | Unknown acoustic drift | Apache 2.0 | Clear | Possible | Very Low | High | Cross-lingual accent | YELLOW |
| **Meta MMS** | Javanese (jav) | Mixed | Low-Medium | Fixed `uroman` | Poor | Incompatible | High (Drops features) | CC-BY-NC | Unclear | Difficult | Medium | Low | Licensing / Collapse | RED |
| **XTTS v2** | 17 Langs (No ID/JV) | Mixed | High | Fixed | Poor | Incompatible | High | CPML | Mixed | Difficult | High | Low | Forced language mapping | RED |

## 7. Female-Speaker Options
- **OpenSLR 41 (Javanese):** Contains a dedicated ~1GB high-quality female subset (`jv_id_female`).
- **Mozilla Common Voice 26.0 (Indonesian):** Contains crowdsourced female recordings.
- **Reference Audio (F5-TTS):** Any clear CC0 female Javanese/Indonesian recording can be used for zero-shot cloning.

## 8. Phoneme Compatibility
- **Piper/VITS:** Highly compatible. They use an explicit `phonemes.json` or `symbols.txt` map. The Kawi IPA inventory (including retroflexes `ṭ ḍ` and voiced aspirates `bh gh`) can be mapped directly to model token IDs.
- **Incompatible Models (MMS/XTTS):** Rely on rigid character sets or hardcoded phoneme lists. Using these would force the Acoustic Mapper to collapse Kawi's uncertain distinctions (e.g., converting `ṭ` to `t`) just to run inference, violating the project philosophy.

## 9. Licensing
- **Code/Models:** VITS, Piper, and F5-TTS are under MIT/Apache 2.0 licenses (fully permissive).
- **Datasets:** OpenSLR 41 is **CC BY-SA 4.0** (Attribution-ShareAlike). Any derivative model weights distributed publicly would inherit the ShareAlike requirement.
- **Rejected:** Meta MMS (CC-BY-NC 4.0, non-commercial restrictiveness).

## 10. Data Provenance
- OpenSLR 41 is officially sourced from Google and Universitas Gadjah Mada (UGM). High provenance and academic reliability.
- Common Voice is crowd-sourced but foundation-managed.

## 11. Compute Requirements
- **Inference:** Piper/VITS can run faster than real-time on a standard CPU. F5-TTS requires a local GPU.
- **Training (VITS/Piper):** 8GB to 24GB VRAM required for mixed-precision training.

## 12. Fine-Tuning Requirements
To achieve zero-loss phoneme transfer in VITS/Piper, fine-tuning is required. A base multi-lingual or Indonesian checkpoint would be fine-tuned on the OpenSLR 41 female dataset for approximately 4-8 GPU hours, substituting Kawi IPA labels to teach the model to articulate the specific Old Javanese phonological distinctions.

## 13. Risks
- **Acoustic Collapse:** An off-the-shelf Indonesian VITS model may ignore or mispronounce IPA symbols it wasn't trained on (e.g., `ṭ`).
- **Compute/Time:** Fine-tuning a model introduces a machine-learning engineering loop (dataset formatting, tensor shapes, GPU management) outside of the core TTS symbolic pipeline.
- **ShareAlike Contamination:** Distributing an OpenSLR-trained model requires releasing it under CC BY-SA.

## 14. Recommended Experiment
**The smallest falsifiable experiment:**
1. Download a pre-trained, lightweight Indonesian or Javanese Piper/VITS model (e.g., MIT-licensed community model).
2. Write a provisional Acoustic Mapper rule that explicitly safely degrades unsupported Kawi tokens to standard Javanese tokens *only for this backend* (e.g., `ṭ` -> `t`).
3. Run inference on the 8-word Kawi matrix.
4. Evaluate if the resulting female voice naturalness justifies proceeding to full fine-tuning.

## 15. Rejected Approaches
- **Meta MMS & XTTS:** Rejected due to fixed vocabularies that force upstream G2P collapse, and non-commercial/restrictive licensing.
- **"Drop a WAV into eSpeak":** Architecturally invalid.
- **Immediate Heavy Fine-Tuning:** Rejected. We must verify pipeline integration with a dummy/off-the-shelf model first.

## 16. Human Decisions Required
1. Accept the CC BY-SA 4.0 license implications for the future neural model artifact (using OpenSLR 41)?
2. Accept a temporary acoustic degradation in the Acoustic Mapper to test an off-the-shelf VITS model before committing to a full fine-tune?

## 17. Reproducibility Plan
All inference tests will be scripted in `tests/generate_matrix.py`, outputting to `artifacts/neural_test_X.wav`. If fine-tuning is approved later, the dataset preparation scripts and hyperparameter configs will be committed to `src/evaluation/`.

## 18. Exact Next Step
Write a Python script to initialize a Piper/VITS backend subclass, route the 8 Kawi matrix words through a neural-specific Acoustic Mapper degradation list, and generate test audio using a small public Indonesian/Javanese `.onnx` checkpoint.