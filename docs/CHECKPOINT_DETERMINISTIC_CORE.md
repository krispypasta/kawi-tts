# Checkpoint: Deterministic Core Stable

**Tag:** `deterministic-core-stable-2026-10-08`
**Date:** 2026-10-08

This checkpoint represents the formal freeze of the Kawi-TTS deterministic core engine following Phase 7 acceptance.

## What this Core guarantees:
* The pipeline from raw text to phoneme sequences is deterministic and reproducible under the pinned project/software environment.
* Preservation of the linguistic distinctions represented by the project's canonical representation layer.
* Strict structural isolation between Profile A (Historical Spoken rules: voiced aspirate merger, sibilant merger, macron strip) and Profile B (Scholarly Orthographic rules). 
* Traceable diagnostics via `kawi-trace`. 
* Immutability of the 100-form regression suite.

## What it does NOT guarantee:
* It does NOT guarantee that the acoustic output represents how ancient speakers actually sounded. (The epistemic boundary between software policy and historical reality is strictly maintained).
* It does NOT guarantee high naturalness (eSpeak-ng is explicitly robotic).

## Supported Input:
* Romanized Kawi (Zoetmulder 1982 / Acri-Damais conventions) with Unicode normalization, diacritics, and macrons.

## Acoustic Backend Status:
* `eSpeak-ng` locally required for WAV execution. 
* Neural TTS (Piper/VITS) explicitly blocked and DEFERRED to honor the $0 project mandate.
