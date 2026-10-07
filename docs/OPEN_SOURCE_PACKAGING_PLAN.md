# Kawi-TTS Open-Source Packaging & Distribution Plan

## 1. Current Packaging State
* **Original State:** The repository was previously a flat script collection under a generic `src/` directory without a package definition (no `setup.py` or `pyproject.toml`).
* **Implementation State (New):** The `src/` directory has been successfully migrated to a formalized `kawi_tts/` Python namespace. A standard modern `pyproject.toml` using `setuptools` has been implemented.
* **Testing:** All 94 tests in the test matrix pass cleanly when the package is installed via `pip install -e .`.

## 2. Proposed Public API
The Kawi-TTS API must remain modular, exposing core processing layers so downstream tools can consume intermediate outputs (e.g. phoneme maps) without being forced to generate audio.

**Core Public Modules Exposed:**
* `kawi_tts.normalization` (for orthographic Unicode canonicalization)
* `kawi_tts.g2p` (for the lossless phonetic oracle)
* `kawi_tts.acoustic` (for Profile selection and eSpeak audio synthesis)

**Example Downstream Usage:**
```python
from kawi_tts.acoustic import synthesize, ESpeakBackend

text = "om awighnam astu namas sidham"
backend = ESpeakBackend()  # Discovers local eSpeak install
result = synthesize(
    text,
    profile="A",           # Profile A (Historical) or B (Scholarly)
    backend=backend,
    output_path="output.wav",
    dry_run=not backend.is_available
)
print(result.g2p_phonemes)
```

## 3. Proposed Package Structure
The package adopts a zero-cost, standard Python layout compliant with PEP 517:
* `pyproject.toml` (Build system, metadata, dependencies)
* `kawi_tts/` (Main module source code)
* `tests/` (Test suite)
* `docs/` (Strategic & architectural documentation)
* `scripts/` (Internal developer tools)

The metadata explicitly defines Kawi-TTS as a "Deterministic pronunciation and reconstruction engine for Old Javanese/Kawi", correctly managing expectations regarding neural TTS and naturalness.

## 4. eSpeak Dependency Strategy
Kawi-TTS requires `espeak-ng` for actual audio rendering, but it must **not** fail to install or import if eSpeak is missing. 
* **Core Processing (G2P, Normalization):** Works natively in Python with 0 external dependencies.
* **Acoustic Synthesis:** The `ESpeakBackend` gracefully checks `shutil.which("espeak-ng")`.
* **Error Handling:** If `synthesize(dry_run=False)` is invoked without eSpeak, an `ESpeakNotFoundError` is raised containing clear OS-specific installation instructions (e.g., `winget install eSpeak-ng` / `apt install espeak-ng`).

## 5. CLI Strategy
A formal console entry point has been added to `pyproject.toml`:
`kawi-trace = "kawi_tts.cli.kawi_trace:main"`

Upon `pip install`, users instantly gain access to the `kawi-trace` CLI tool from anywhere in their terminal:
```bash
kawi-trace "sanghyang kamahāyānikan"
```
This preserves the project's utility as a research and diagnostic instrument without writing new UI code.

## 6. Kawi Learn Boundary
To enforce strict decoupling from the Kawi-TTS core:
* **Kawi-TTS** will never import Kawi Learn code, UI libraries, or curriculum data.
* **Kawi Learn** will consume Kawi-TTS strictly as a standard `pip` dependency (e.g., `pip install kawi-tts`).
* **Integration Model:** Kawi Learn should utilize Ahead-of-Time (AOT) generation, passing its dictionary strings to `kawi_tts.acoustic.synthesize()` during a build step to generate static `.wav` flashcard assets.

## 7. OSS Readiness Audit
* **License:** MIT License is present and correctly scopes permissions.
* **README:** Accurately states project identity, the Phase 7 freeze constraints, Profile A limitations, and explicit non-goals (no neural claims, no native-speaker emulation).
* **Dependencies:** Clean. No heavy ML libraries (PyTorch, ONNX) bloat the installation.

## 8. Testing Plan
* **Current Status:** 94/94 tests pass locally in the new package structure.
* **Regression Corpus:** The 100-form deterministic matrix remains the gating mechanism for the package. Any public API change must pass this suite.
* **Test Isolation:** The `ESpeakBackend` handles `dry_run=True` to create a 44-byte WAV header, ensuring downstream CI pipelines can test Kawi-TTS integration without installing eSpeak-ng.

## 9. Distribution Options
* **Immediate Target:** GitHub Source Release. The repo is currently usable as `pip install git+https://github.com/...`.
* **Subsequent Target:** **PyPI Publication**. The package structure is fully PyPI compliant. Once the project owner authorizes a PyPI release, it can be distributed as `pip install kawi-tts`.

## 10. Versioning Recommendation
**Recommended Version:** `1.0.0`
* **Why:** The deterministic core is frozen at `deterministic-core-stable-2026-10-08`. All Phase 7 acceptance criteria have passed. The API provides exactly what is documented. A `1.0.0` version appropriately flags that the deterministic ruleset and package boundary are stable.
* **Rules:** We do not rewrite the historical tag. The Python package version metadata in `pyproject.toml` is set to `1.0.0`.

## 11. Minimal Implementation Plan (EXECUTED)
1. Created standard `pyproject.toml` defining package metadata, entry points, and dependencies.
2. Renamed internal generic `src/` to formal `kawi_tts/` namespace.
3. Rewrote internal relative imports to absolute `kawi_tts.*` imports.
4. Installed package locally via `pip install -e .`
5. Confirmed all 94 deterministic matrix tests pass cleanly.
6. Executed `kawi-trace` CLI entry point to confirm operability.

## 12. Remaining Blockers
* **None for Source Release.** The package is fully usable from the git repository right now.
* **PyPI Publication requires:** A project owner decision on whether to publish to the Python Package Index, and under which PyPI account credentials. No engineering blockers exist.

**FINAL GATE STATUS:** GO (Implementation executed successfully).