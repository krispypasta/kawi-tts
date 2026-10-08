# Kawi-TTS Low-Cost Neural Training Plan

**Status:** Planning Phase - Feasibility Confirmed
**Objective:** Determine if Google AI Pro (Colab 200 CCUs + GCP $10/mo) can realistically fund a neural TTS fine-tuning experiment for Kawi-TTS on a zero-to-low budget.

---

## 1. Executive Summary
This document outlines the architecture, resource allocation, and strict safety controls required to execute a neural TTS acoustic fine-tuning experiment using existing Google AI Pro benefits. The analysis confirms that **Colab's 200 Compute Units (CCUs) are more than sufficient** to fine-tune a modern, lightweight TTS architecture on a 30–60 minute Kawi dataset. 

## 2. Google AI Pro Resources
[EVIDENCE]
- **Google Colab:** Includes 200 CCUs per billing cycle.
- **Developer Premium:** Includes $10/month in Google Cloud (GCP) credits.

## 3. Colab Resources & CCU Consumption
[EVIDENCE / ENGINEERING ESTIMATE]
- **T4 GPU (16GB VRAM):** ~2 CCUs per hour.
- **L4 GPU (24GB VRAM):** ~5 CCUs per hour.
- **A100 GPU (40GB VRAM):** ~13-15 CCUs per hour.
- **Timeouts:** Colab sessions can be interrupted; training scripts must checkpoint frequently (every 1000 steps) to Google Drive.
- **Rollover:** CCUs from the monthly Pro subscription do not roll over. 

## 4. Google Cloud Credits ($10/mo)
[EVIDENCE]
- **Compute Engine (Spot T4):** ~$0.11/hour. $10 buys ~90 hours of Spot T4 compute.
- **Cloud Storage:** ~$0.02/GB/month. 
- **Recommendation:** Do not use GCP for the primary training loop due to the risk of accidental overage. Use the $10 credit exclusively for **Cloud Storage** (artifact backups) and **Vertex AI Notebooks** strictly for lightweight data preprocessing.

## 5. Model Candidates
We evaluated models strictly on low-data fine-tuning capability, deterministic IPA input, and commercial-use licensing.
- **Piper (VITS variant):** **[SELECTED]** C++ CPU inference, direct `[[ipa]]` injection bypasses internal G2P, native transfer learning scripts, MIT license. Extremely low VRAM requirements.
- **VITS (Vanilla):** Good, but requires more engineering to wrap into a deployable TTS engine.
- **Kokoro-82M:** Apache 2.0. Exceptional quality, but bypass for internal English G2P is currently undocumented/unstable for pure IPA injection.
- **XTTSv2:** Rejected. Coqui Public Model License restricts commercial use of weights.

## 6. Model Licensing
[PROJECT ASSUMPTION]
- **Piper Weights:** Pretrained base models provided by Rhasspy/Piper are typically released into the Public Domain (CC0) or MIT.
- Any model trained for Kawi-TTS must originate from a permissively licensed base model to ensure the Kawi adapter weights can be open-sourced.

## 7. Data Requirements (Reassessment)
[MODEL-SPECIFIC GUIDANCE]
- **30–45 Minute Minimum:** VITS/Piper transfer learning (fine-tuning an existing decoder) can map a new speaker and phonology with 30-60 minutes of high-quality data. 
- **Can it support a LoRA/Feasibility experiment?** YES. The acoustic base (breathing, pacing, vocal tract physics) is retained from the base model. The fine-tuning merely bends the phonetic embeddings and speaker projection to the Kawi data.
- **2–5 Hour Preferred:** Remains the standard for a production V1 model trained from scratch or heavily adapted.

## 8. Speaker Requirements
- A qualified female speaker (matching the naturalness target).
- The neural model will clone the speaker's vocal identity via fine-tuning. 
- **No scraped data, no non-consensual voice cloning.**

## 9. Low-Cost Training Architecture
```text
Frozen Kawi v1.1.1 Frontend (Profile A)
        ↓
Deterministic Phoneme Representation (IPA Array)
        ↓
Piper Transfer Learning Training Script (Colab)
        ↓
Pretrained Multilingual/English Female Base Model (MIT/CC0)
        ↓
Parameter Updates (Full fine-tune or frozen text-encoder)
        ↓
Kawi Speaker-Adapted Acoustic Model (.onnx)
```

## 10. Colab Training Plan
**Scenario A: 30-minute corpus / Feasibility Fine-tune**
- **Hardware:** T4 GPU (16GB VRAM)
- **Batch Size:** 32 (Mixed Precision)
- **Time:** ~15 wall-clock hours
- **CCU Cost:** ~30 CCUs
- **Feasibility:** HIGH. Leaves 170 CCUs for retries/hyperparameter sweeps.

**Scenario B: 60-minute corpus**
- **Time:** ~20 hours → ~40 CCUs. Feasible.

**Scenario C: 2-hour corpus**
- **Time:** ~40 hours → ~80 CCUs. Feasible.

**Scenario D: 5-hour corpus**
- **Time:** ~80 hours → ~160 CCUs. High compute pressure. Will require aggressive checkpointing due to Colab maximum session limits (usually 12-24 hours).

## 11. Google Cloud Supplementary Plan
- Allocate $2/month for 100GB of Cloud Storage (GCS) to hold the raw WAVs, alignments, and backup checkpoints.
- Allocate $8/month as a buffer for network egress.
- Do not deploy Compute Engine GPUs. 

## 12. Cost Estimates
- Colab CCUs: Included in AI Pro (effectively $0 extra).
- GCP Storage: ~$2/month (covered by $10 credit).
- **Net Out of Pocket:** $0.

## 13. $0 Extra-Spend Plan
- Primary execution environment: Google Colab.
- Artifact storage: Google Drive (15GB free tier).
- Preprocessing: Local CPU or Colab CPU (0 CCUs).

## 14. $10 Maximum-Spend Plan
- Artifact backup: Google Cloud Storage (Bucket with lifecycle retention).
- GCP Billing Budget: Set a strict $10 threshold with Pub/Sub triggers to disable the billing account if reached.

## 15. Failure Modes
1. **Phonetic Collapse (Retroflex/Dental):** Detection: Human review and spectrogram F3 analysis. Mitigation: Freeze the text encoder early; oversample minimal pairs.
2. **Colab Disconnects:** Detection: Kernel dies. Mitigation: `save_checkpoint_every: 1000` steps mapped directly to a mounted Google Drive folder.
3. **Overfitting:** Detection: Validation loss diverges. Mitigation: Stop training early.
4. **Accidental Billing:** Detection: GCP Console. Mitigation: Cloud Billing hard limits.

## 16. Evaluation Methodology
- **Success:** The model is materially more natural than eSpeak, and human evaluators verify that `ṭ`/`t`, `ḍ`/`d`, and schwa (`ə`) remain distinct.
- **Not a Goal:** Flawless historical recreation.

## 17. Reproducibility
- All Colab notebooks must be committed to `experiments/colab_training/`.
- The dataset must be version-tracked (e.g., HuggingFace datasets or DVC) prior to Colab ingestion.

## 18. Safety & Billing Controls
- **Never** put GCP service account JSONs or API keys in the repository.
- Use Colab's native `from google.colab import userdata` for secrets.
- Set a GCP Cloud Billing Budget Alert at $5.00 and $9.00.

## 19. Decision: CONDITIONAL GO
**Google AI Pro is exceptionally well-suited and fully sufficient for this experiment.** The 200 CCUs provide massive overhead for a 30-60 minute fine-tuning task. 
**Condition:** We must acquire the 30-45 minute authorized Kawi audio dataset first.

## 20. Exact Prerequisites Before First Training Run
1. [ ] 30-45 minute clean audio dataset secured and licensed.
2. [ ] MFA forced alignment completed (producing Piper-compatible `.jsonl`).
3. [ ] GCP Billing Budget ($10 hard limit) configured.
4. [ ] Colab notebook drafted and dry-run on CPU.

## 21. Step-by-Step First Experiment Plan
1. **Data Prep:** Mount Google Drive in Colab. Unzip dataset.
2. **Environment:** Install `piper-train` dependencies.
3. **Base Model:** Download `en_US-lessac-high.ckpt` (or similar permissive female base).
4. **Config:** Update `config.json` with Kawi phoneme maps.
5. **Train Loop:** Launch `python -m piper_train` on T4 GPU.
6. **Checkpointing:** Auto-save to Google Drive.
7. **Export:** Export `.onnx` model for local deterministic testing.
