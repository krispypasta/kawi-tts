# Kawi-TTS

An open-source deterministic pronunciation and reconstruction engine for Old Javanese (Kawi).

Kawi-TTS is **not** a natural neural TTS system, it does **not** claim to generate historically authentic speech, and it is **not** a linguistic oracle. It is a strictly deterministic pipeline that implements a documented linguistic reconstruction policy and provides reproducible acoustic output through a selected backend.

## What It Does

Kawi-TTS transforms Old Javanese text into phonetic representations and synthesizes them into audio. The pipeline is strictly deterministic:

`Text → Normalization → G2P / Tokenization → Canonical Representation → Profile A / Profile B → Acoustic Mapping → eSpeak-ng → WAV`

The engine resolves linguistic features through two distinct profiles:
* **Profile A (Reconstructed Spoken):** Represents the historical spoken target. It is explicitly evidence-scoped, includes documented spoken mergers and adaptations, and strictly preserves unresolved items as unresolved where evidence is lacking.
* **Profile B (Scholarly/Orthographic):** A scholarly reading profile that artificially preserves the intended distinctions of the scholarly orthographic representation (such as unmerged Sanskrit distinctions).

## Important Epistemic Limitation

**The generated audio is NOT claimed to reproduce exactly how historical Old Javanese speakers sounded.**

The software simply operationalizes the project's documented linguistic reconstruction and backend policy. Users must clearly distinguish between:
1. **Evidence-backed linguistic rules** (e.g., historical spoken mergers)
2. **Provisional reconstructions** (e.g., adaptation of Sanskrit vocalic liquids to native Javanese phonotactics)
3. **Engineering policy** (e.g., deferring vowel duration resolution)
4. **Backend approximations** (e.g., dropping retroflex distinctions due to eSpeak limitations)

## Current Status

* **Core:** The deterministic core is accepted and historically frozen.
* **Tests:** The current test suite passes 97/97. The 100-form regression corpus passes fully.
* **Backend:** eSpeak-ng is the current acoustic backend. The `id` (Indonesian) voice is utilized with explicit backend-scoped approximations where native eSpeak support is lacking.
* **Infrastructure:** Neural TTS is explicitly deferred. The project remains strictly zero-budget compatible. No cloud service or proprietary data is required for core operation.
* **Distribution:** The package is not yet published to PyPI.

## Quick Start

You can run the engine locally without any cloud dependencies.

```bash
# 1. Clone the repository
git clone https://github.com/krispypasta/kawi-tts.git
cd kawi-tts

# 2. Create and activate a Python virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On Linux/macOS: source venv/bin/activate

# 3. Install the package locally in editable mode
pip install -e .

# 4. Verify installation by running tests
python -m unittest discover -s tests -p "test_*.py"

# 5. Use the trace diagnostics CLI
kawi-trace "sĕkar"

# 6. Generate demo audio (requires eSpeak-ng installed on your system)
python run_audio_demo.py
```

## eSpeak Dependency

The deterministic linguistic processing (Normalization, G2P, Profiling) operates entirely independent of eSpeak. However, actual WAV synthesis requires `espeak-ng` to be installed on your system path.

If eSpeak-ng is missing, the pipeline produces an actionable error. The package will **not** silently pretend that dummy audio is real synthesis. Current acoustic mapping supports the eSpeak `id` voice, utilizing explicit `BACKEND_APPROXIMATION` rules to bypass unsupported IPA characters safely.

## Examples

* `sĕkar` — Standard Javanese lexical item. Both profiles map identically to Javanese schwa and native consonants.
* `BHAṬĀRA` — Sanskrit loan.
  * *Profile B* preserves the aspirated `bʱ`, retroflex `ṭ`, and duration `aː`.
  * *Profile A* merges the aspirate to `b`, maps the retroflex to `ṭ`, and leaves duration unresolved.
  * *Acoustic Mapper* then approximates retroflex `ṭ` to dental `t` for eSpeak compatibility.
* `śānti` — Sanskrit loan.
  * *Profile B* preserves palatal sibilant `ś`.
  * *Profile A* merges it to native `s`.
* `kṝta` — Sanskrit loan with a long vocalic liquid.
  * *Profile B* preserves canonical long `r̩ː`.
  * *Profile A* adapts it to native phonotactics as a short Javanese schwa base (`rə`), deliberately discarding non-native duration as per reconstruction policy.

## Trace / Diagnostics

The `kawi-trace` CLI utility exposes the exact transformation of every string. It traces:
`Input → Normalized → Canonical → Profile Target → Backend Target`

Backend approximations (e.g., eSpeak's inability to pronounce retroflex consonants) are visibly distinguished in the terminal output from intentional linguistic targets.

## Project Structure

```text
kawi_tts/        # Core engine (normalization, g2p, acoustic mappers)
docs/            # Project documentation, policies, and research logs
tests/           # Test suite and regression corpora
artifacts/       # Generated WAVs and manifest outputs
pyproject.toml   # Project build configuration
```

## Open-Source & Contributing

Kawi-TTS is an open-source research tool.
* **Evidence Before Code:** Research and evidence must precede any linguistic rule changes. Contributors must not invent pronunciation rules.
* **Changes:** Modifying linguistic policy requires cited evidence and corresponding regression coverage.
* **Boundaries:** Backend approximations must remain strictly backend-scoped (within the `AcousticMapper`). The canonical representation must remain protected.

Please see the `docs/` folder for architectural decisions and governance.

## Kawi Learn Relationship

**Kawi Learn** is considered a future, external educational application that may consume Kawi-TTS.
* **Kawi-TTS:** A strict pronunciation and reconstruction engine.
* **Kawi Learn:** A future end-user application.

Kawi-TTS must remain entirely independent of Kawi Learn. Kawi Learn does not currently exist as a finished product.

## Future / Deferred Work

The following items are explicitly deferred to protect the zero-budget constraint:
* Neural TTS models
* Custom recorded speech corpora
* New acoustic backends requiring unavailable computational resources

These will only be reopened if specific, resource-compatible packaging requirements are met.

## Research & Citation

Linguistic decisions, open questions, and principal references are maintained in `docs/RESEARCH_LOG.md` and the adjacent policy documents (e.g., `docs/P5_002_ACOUSTIC_PROFILE_POLICY.md`). All linguistic claims within the codebase are tied to these cited policy rules.

## License

Kawi-TTS is licensed under the MIT License. See the `LICENSE` file for details.