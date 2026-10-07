# P7-003: ZERO-BUDGET SCOPE REASSESSMENT & FRANKENSTEIN STOP

## 1. Primary Objective & New Phase-7 Principle
This document formalizes a critical strategic constraint and scope correction for Kawi-TTS: **the project operates with effectively ZERO PROJECT BUDGET (less than USD 10).** 

The project must remain viable, technically rigorous, and actively developable without relying on proprietary data, paid experts, paid infrastructure, or neural speech training. The core identity of Kawi-TTS is a research-first reconstructed Kawi/Old Javanese pronunciation engine—not necessarily a natural-sounding neural voice. 

Neural TTS is now explicitly classified as **OPTIONAL FUTURE RESEARCH** rather than a mandatory Phase 7 requirement.

## 2. The Core $0 Deliverable
The strongest useful product that can be completed under the zero-budget constraint is the **Kawi Pronunciation & Reconstruction Engine**. 

Kawi-TTS can credibly promise:
*   **Evidence traceability**: Every phonetic rule traces back to a cited scholarly source.
*   **Explicit uncertainty**: The system knows what it does *not* know (e.g., vowel length mapping).
*   **Canonical representation**: Lossless text-to-phoneme tokenization.
*   **Profile A / B separation**: Clear software boundaries between Historical Spoken Kawi (Profile A) and Modern Scholarly Reading (Profile B).
*   **Deterministic reproducibility**: An acoustic baseline utilizing free, local, rule-based synthesizers (eSpeak-ng) to prove the pipeline without collapsing information.

## 3. Neural TTS Reclassification
*   **STATUS**: DEFERRED / OPTIONAL
*   **Reason**: A defensible Profile A neural corpus currently requires commissioning human acoustic resources (expert speakers/scholars) that the project cannot afford or guarantee. 
*   **Future Neural Reopening Criteria**: The neural branch may only reopen if:
    1.  Legally reusable (CC0/CC-BY) suitable speech data becomes available for free.
    2.  A knowledgeable collaborator volunteers to record.
    3.  Explicit project funding appears.
    *Do not create hypothetical assumptions ("we will eventually find a speaker"). The branch remains closed until a concrete dependency is satisfied.*

## 4. Frankenstein Prevention Rules
To prevent scope creep and unbound complexity, the following governance rules are active immediately:
1.  **RULE 1:** A new feature must justify why Kawi-TTS needs it.
2.  **RULE 2:** A dependency that requires money must not become mandatory without explicit project-owner approval.
3.  **RULE 3:** A human specialist must not become a hidden project dependency.
4.  **RULE 4:** Neural naturalness must not override linguistic traceability.
5.  **RULE 5:** Existing architecture must not be replaced merely because a newer technology is more impressive.
6.  **RULE 6:** Every optional subsystem must have a clear reason for existence and a clear exit condition.
7.  **RULE 7:** Do not expand the project's scope simply because an AI agent discovers another technically interesting possibility.
8.  **RULE 8:** The project owner, not the agent, decides whether increased complexity is worth it.

## 5. Zero-Cost External Data Policy
Investigating free/open resources remains allowed, but with strict epistemic and legal boundaries:
*   Openly accessible != legally reusable (e.g., YouTube audio cannot be bulk downloaded for ML training).
*   Modern Javanese/Balinese material must not be treated as historical Kawi ground truth.
*   Open data may only enter the pipeline if provenance is documented, the license is clear, and the acoustic tradition is appropriate.

## 6. Required Self-Audit
1.  **Did this plan require Abraham to become a Kawi speaker?** No. Abraham is explicitly ruled out as a pronunciation authority.
2.  **Did this plan require hiring anyone?** No. Paid experts are now explicitly excluded from the critical path.
3.  **Did this plan require paid infrastructure?** No. Cloud GPUs are excluded; local eSpeak-ng testing remains the baseline.
4.  **Did this plan require a neural model?** No. Neural models are now strictly optional and deferred.
5.  **Did this plan create any dependency that was not present in V1?** No. It removes dependencies (expert speakers, neural backends) that were threatening to block V1/V2 progress.
6.  **Can Kawi-TTS continue progressing if neural TTS never happens?** Yes. The pronunciation engine (G2P, canonical tracking, Profile A/B separation) provides immense scholarly and technical value alone.
7.  **What is the strongest useful system we can build for approximately $0?** A complete, deterministic text-to-phoneme and text-to-eSpeak engine that perfectly maps Old Javanese text into verifiable historical pronunciation schemas.
8.  **Which parts of Phase 7 should be frozen or deferred?** P7-002 (Pilot Corpus Recording) and P7-003 (Pilot Neural Experiment) are frozen/deferred.
9.  **What is the single highest-value next milestone?** Linguistic and pronunciation-engine hardening (expanding G2P rules, testing against larger text corpora, and improving diagnostic infrastructure).
10. **What should the project explicitly STOP doing?** Stop attempting to source, record, or train a neural backend dataset.

## 7. Zero-Cost Roadmap Reset
Phase 7 is restructured as follows:

*   **P7-A: Zero-budget scope reset** (Completed via this document).
*   **P7-B: Linguistic and pronunciation-engine hardening.** (Focus on normalization, G2P rules, ambiguity handling, and test coverage).
*   **P7-C: Baseline Acoustic & Evaluation infrastructure.** (Focus on eSpeak backend control, deterministic synthesis, automated canonical-output tests, and phoneme coverage reports).
*   **P7-D: Research tooling.** (Focus on bibliography management, evidence-status tracking, and uncertainty reporting).
*   **P7-E: Deferred Neural Reopening Criteria.** (Frozen until external conditions change).
