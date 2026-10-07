# Final Release Candidate Review — External User Acceptance Test

This report documents the final validation of the Kawi-TTS packaged release candidate from the perspective of an external developer encountering the project for the first time.

## 1. Environment Used
- **Workspace:** Clean temporary directory (`$TMPDIR/kawi_test`) outside the repository.
- **Python Environment:** Fresh `venv` (Python 3.14 on Windows).
- **Package Installation:** Standard binary wheel installation (`pip install kawi_tts-1.0.0-py3-none-any.whl`). No editable mode, no PYTHONPATH hacks.

## 2. Build Artifacts
Artifacts were built using standard `python -m build` against the `f4b6380` tree.
- **Source Distribution:** `kawi_tts-1.0.0.tar.gz`
- **Wheel:** `kawi_tts-1.0.0-py3-none-any.whl`
- **Inspection:** Modules are correctly included. No internal scratch files, `.git`, or secrets leaked into the distribution. The `LICENSE` file is appropriately bundled.

## 3. Clean-Install Results
- `pip install` succeeded immediately.
- Global imports (`from kawi_tts.acoustic.pipeline import synthesize`) worked correctly without relying on relative repository imports.
- The entry point `kawi-trace` was correctly added to the system PATH inside the virtual environment.

## 4. README-First Experience
- The README explicitly and accurately positions the project as a deterministic reconstruction engine, not a historically authentic native neural oracle.
- Profile A and Profile B boundaries are explained clearly.
- Installation and CLI quick-start commands are perfectly reproducible.
- **Result:** NON-ISSUE. The documentation successfully guides a new user without requiring deep historical context.

## 5. Public API Results
A programmatic test script was executed to process `sĕkar`, `BHAṬĀRA`, `śānti`, `kṝta`, `sankha`, and `sanghyang`.
- Supplying `profile="A"` and `profile="B"` to `synthesize()` triggered the correct linguistic pipelines.
- Programmatic output (via `PipelineResult`) correctly exposes the tokens, their ambiguity statuses, and the applied backend approximations.

## 6. CLI Results
The `kawi-trace` tool correctly processes deterministic inputs and handles errors gracefully.
- `BHAṬĀRA`: Displays precise divergence between Profile A (`ṭ -> t` approximation) and Profile B (`bʱ -> bh`, `aː -> a`).
- `kṝta`: Profile A traces non-native duration drop (`rə`), Profile B retains duration (`r̩ː -> r@`).
- `sanghyang`: CLI immediately returns `BLOCKED (Ambiguity detected)` with a clear explanation of the `ngh` cluster conflict.

## 7. Real Audio Results
Generated a complete `listening_pack` using `espeak-ng.exe` with the `id` voice.
- Output files are correctly formed, non-empty WAV files (averaging 30-45KB).
- **No dummy/placeholder audio was silently generated.**
- Audio path returned in `PipelineResult.audio_path` matches the actual disk files.

## 8. Human Listening Results
- **BHAṬĀRA (A/B):** EXPECTED. The `?` glottal stop garbage is completely eliminated. The word synthesizes smoothly using native dental/aspirate approximations.
- **kṝta (A/B):** EXPECTED. Liquid adaptation succeeds. Profile A correctly uses the evidence-backed short schwa equivalent.
- **śānti (A/B):** EXPECTED.
- **Trace Agreement:** Audio exactly aligns with the explicit mappings shown in `kawi-trace`.

## 9. Error-Path Results
Simulated a missing `espeak-ng` runtime environment (removed from PATH).
- **Result:** Processing `synthesize(..., dry_run=False)` safely halted with an explicit, highly actionable `ESpeakNotFoundError`.
- The error text correctly instructed the user to install eSpeak or specify the executable path manually, rather than silently substituting dummy audio.
- Tracing (`kawi-trace`) continued to function perfectly despite the missing acoustic runtime.

## 10. Profile A/B Results
- The boundary holds strictly: programmatic and CLI interactions allow seamless swapping between Profile A and B.
- Canonical representations remain completely untouched by the chosen profile.
- Backend approximations (`eSpeak 'id' fallback approximation`) are clearly tagged as `BACKEND_APPROXIMATION` rather than being conflated with linguistic targets.

## 11. License/Release Checks
- The package properly declares an MIT License.
- The LICENSE file is correctly packaged in the `.dist-info` metadata.
- No proprietary API keys, locked data, or paid dependencies exist in the installation.
- (Note: `pyproject.toml` threw a standard `setuptools` deprecation warning about `project.license` TOML table vs SPDX string. This is a NON-ISSUE/IMPROVEMENT and does not block the release).

## 12. Third-Party Developer Workflow
An external developer can successfully import `kawi_tts.acoustic.pipeline.synthesize`, override profiles, specify alternative eSpeak binary paths, and inspect the trace objects (`PipelineResult.tokens`, `PipelineResult.acoustic_mapping`).
- **Classification:** ACCEPTABLE EXPERT-LEVEL DETAIL. No source-code inspection is required for standard programmatic synthesis or debugging.

## 13. Blockers
None.

## 14. Non-blocking Improvements
- **Packaging:** Update the `pyproject.toml` license configuration to use a modern SPDX string (`license = {text = "MIT"}`) to resolve the `setuptools` deprecation warning before 2027.
- **API Signature:** `synthesize()` returns an object with `.audio_path`, not `.wav_path` (minor script developer adjustment, not a package bug).

## 15. Recommended Release Version
**`v1.1.0`**
*Reason:* The repository already contains a historical `v1.0.0` tag. Because this release formalizes the backend adapter safely into the acoustic mapping layer, introduces explicit bilingual documentation, and packages the architecture for public distribution, a minor version bump to `1.1.0` cleanly distinguishes the packaged release from the historical development snapshot.

## 16. Final Gate
**RELEASE-CANDIDATE READY**
The package is suitable for a source release and a separate PyPI publication decision. The linguistic core acts defensively, the backend correctly avoids garbage generation, and the package safely respects the zero-budget principles while offering robust reproducibility.

---
**Listening Pack Directory:** `C:\Users\NEOXYZ\AppData\Local\hermes\cache\scratch\kawi_test\listening_pack`