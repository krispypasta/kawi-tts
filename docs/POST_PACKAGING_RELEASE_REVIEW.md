# POST-PACKAGING RELEASE REVIEW

**Date:** 2026-10-08
**Review Stage:** Release-Readiness Gate
**Target:** `kawi-tts` Python Package (Frozen Deterministic Core)

## 1. Executive Summary
This review evaluates the readiness of the `kawi-tts` deterministic core for open-source distribution. The engine was audited against packaging best practices, public API surface constraints, licensing, security, and Kawi Learn integration boundaries. A minor release-safety patch was applied to the public acoustic API to prevent silent dry-run behavior. The package is completely decoupled from any downstream application UI and enforces a strict zero-dependency policy for linguistic generation.

**FINAL GATE STATUS:** **READY**

## 2. Package Metadata Findings
**Classification:** IMPROVEMENT
- The `pyproject.toml` metadata correctly defines `kawi-tts`, authors, and `kawi-trace` entry points.
- The build backend correctly uses `setuptools.build_meta`.
- **Finding:** The declared version is `1.0.0`. However, the repository contains a historical `v1.0.0` tag prior to the deterministic engine freeze. 
- **Recommendation:** Bump the package version to `1.0.1` or `1.1.0` prior to public PyPI distribution to avoid git tagging conflicts.

## 3. Public API Findings
**Classification:** RELEASE-SAFETY (Fixed)
- **Finding:** The public synthesis function `kawi_tts.acoustic.pipeline.synthesize()` defaulted to `dry_run=True`. If an external application called this function without explicitly disabling `dry_run`, the function would silently execute and return success without generating the requested `.wav` file (or generate a dummy 44-byte WAV if explicitly configured).
- **Fix Applied:** Changed the default signature in `kawi_tts/acoustic/pipeline.py` to `dry_run=False`. A standard call now demands output generation and safely traps missing dependencies, rather than appearing silently successful.
- The public modules (`normalization`, `g2p`, `acoustic`) correctly expose the deterministic processing pipeline.

## 4. eSpeak & Missing-Dependency Behavior
**Classification:** NON-ISSUE
- **Finding:** Importing `kawi_tts` does not trigger any subprocess calls. 
- **Finding:** Invoking G2P/Normalization functions independently does not trigger eSpeak.
- **Finding:** When `dry_run=False`, missing `espeak-ng` gracefully throws a highly descriptive `ESpeakNotFoundError` with actionable installation instructions. No dummy/placeholder WAV files are silently injected into normal user workloads.

## 5. Clean Installation Results
**Classification:** NON-ISSUE
- Created a pristine Python virtual environment and successfully built and installed the package (`python -m build`, `pip install .`).
- Verified that the source layout (`kawi_tts/` namespace) successfully maps to the `site-packages` distribution. The package installs cleanly and works immediately.

## 6. CLI Results
**Classification:** NON-ISSUE
- The `kawi-trace` console script registers cleanly in `Scripts/` (or `bin/` on Unix).
- Running `kawi-trace "om awighnam astu"` in the clean environment successfully produced the Profile A / Profile B diagnostic trace. It relies on no local relative paths.

## 7. Test Results
**Classification:** NON-ISSUE
- 94/94 tests passed reliably.
- Neural experimental backend tests (e.g., `test_experimental_piper.py`) remain explicitly disabled (`.disabled` extension) to honor the zero-budget constraint.
- The A/B Profile regression corpus is strictly enforced.

## 8. Documentation Findings
**Classification:** NON-ISSUE
- Documentation accurately frames the engine as "an open-source deterministic pronunciation and reconstruction engine for Old Javanese/Kawi".
- It successfully avoids making any scientifically unsupported claims of absolute historical acoustic authenticity, naturalness, or neural generation.

## 9. Kawi Learn Compatibility
**Classification:** NON-ISSUE
- `kawi-tts` exposes a strict, predictable A/B Profile pipeline suitable for Ahead-Of-Time (AOT) static generation.
- The package is entirely uncoupled from Kawi Learn's UI, spacing-repetition logic, or translation domains.

## 10. Distribution & Source-Tree Findings
**Classification:** NON-ISSUE
- Untracked repository scratch scripts (`scripts/sanity_test.py`, `patch_state_p7.py`) exist in the working directory.
- `setuptools` correctly targets only the `kawi_tts` namespace. `python -m build` verification confirmed that these untracked scratch files do not leak into the `.whl` or `.tar.gz` distribution files.

## 11. Reproducibility Findings
**Classification:** NON-ISSUE
- Text normalization, tokenization, and canonical/profile mapping are mathematically deterministic across platforms.
- Final WAV output remains dependent on the underlying host OS `espeak-ng` compilation, meaning binary bit-for-bit WAV equivalency is not guaranteed globally, though the phonetic instruction set is.

## 12. License & Provenance Findings
**Classification:** NON-ISSUE
- Zero third-party Python dependencies (`dependencies = []`).
- Zero compiled native extensions.
- The repository's `LICENSE` file supports the `MIT` declaration in `pyproject.toml`.

## 13. Security & Hygiene Findings
**Classification:** NON-ISSUE
- Codebase grep audits confirm no API keys, tokens, hardcoded developer directories, or credentials exist in the source or tests.

## 14. Blockers
None.

## 15. Minimal Fixes Applied
- **RELEASE-SAFETY FIX:** Patched `kawi_tts/acoustic/pipeline.py` to change `synthesize(dry_run=True)` to `dry_run=False`. Verified via clean install and full test suite (`python -m unittest discover -s tests`). 

## 16. Final Release Gate
**READY**
The package is safe for local and community release. The software architecture satisfies all constraints of Phase 7 (zero-budget, deterministic, profile-isolated).

## 17. PyPI Readiness Assessment
Do **NOT** publish to PyPI immediately. 

**Recommended Action Plan for PyPI:**
1. Update `pyproject.toml` version to `1.1.0` to avoid conflict with the repository's legacy `v1.0.0` tag.
2. Commit the packaging directory (`kawi_tts/`), `pyproject.toml`, and this review report.
3. Tag the finalized packaging commit (e.g., `v1.1.0`).
4. Execute PyPI release via standard `twine upload dist/*`.