# Release Notes: Kawi-TTS v1.1.0

This release formalizes the deterministic open-source core of Kawi-TTS into a standalone Python package. It bridges the gap between historical linguistic reconstruction and reproducible acoustic prototyping, operating strictly within zero-budget open-source constraints.

## WHAT'S NEW

* **Formal `kawi_tts` Python package layout:** The repository has been packaged using standard `pyproject.toml` (PEP 621), enabling clean `pip install` without repository-relative hacks.
* **Public CLI entry point (`kawi-trace`):** A new deterministic tracer that visualizes the pipeline (normalization -> tokenization -> G2P -> acoustic mapping).
* **eSpeak `id` backend approximation layer:** Safely maps unsupported canonical IPA targets (e.g., retroflexes, aspirates) into native eSpeak Indonesian (`id`) mnemonics, bypassing the backend's default glottal-stop (`?`) garbage generation.
* **Improved real acoustic output:** Audio generation now works robustly out-of-the-box using the eSpeak `id` voice, producing cleaner approximations compared to raw unsupported-IPA fallbacks.
* **Profile A long vocalic-liquid policy correction:** Corrected a bug where long syllabic liquids (`r̩ː`, `l̩ː`) incorrectly generated long schwas (`rəː`) to appease backend requirements. Profile A now strictly enforces evidence-backed short schwas (`rə`, `lə`), explicitly pushing all unhistorical phonetic adjustments into the backend approximation layer.
* **Expanded regression/diagnostic coverage:** Added `kawi_trace.py` and a 100-form regression corpus.
* **Bilingual README:** Complete English (`README.md`) and Indonesian (`README.id.md`) canonical documentation defining the exact boundaries and capabilities of the engine.

## STABILITY

* **97 deterministic tests passing:** 100% pass rate across the full pipeline.
* **100-form regression corpus passing:** Validated across Profile A and Profile B.
* **Deterministic core frozen:** The linguistic rules, canonical tokenization, and architecture boundaries are considered stable and accepted.

## LIMITATIONS

* **eSpeak remains robotic:** The current backend produces highly synthetic, robotic audio. No naturalness optimization has been attempted in this release.
* **Backend approximations are not historical phonetic evidence:** When `kawi-trace` lists a `BACKEND_APPROXIMATION` (e.g., `ṭ -> t`), this is an engineering fallback to make eSpeak function, not a claim that Old Javanese speakers neutralized the distinction.
* **No claim of historical acoustic authenticity:** The audio output is a reproducible rendering of a documented linguistic policy, not a native recording or neural recreation of historical speech.
* **Neural TTS remains deferred:** High-quality neural vocoding remains explicitly blocked by zero-budget constraints and lack of provenance-safe expert corpora.
