# AGENTS.md — AI Guidance for Kawi-TTS

This file governs how AI assistants (Hermes or any other AI tool) should
work within this repository. Read this before beginning any session.

---

## Project Summary

Kawi-TTS is a research-first Text-to-Speech system for Old Javanese (Basa Kawi).

The primary V1 goal is linguistically defensible pronunciation traceable to
cited linguistic sources — NOT naturalness, vocal quality, or audio realism.

Old Javanese is a historical language. No native-speaker recordings exist.
Pronunciation must be reconstructed from written sources, comparative linguistics,
and scholarly research. This reconstruction requires evidence, not guesswork.

---

## Before You Do Anything

1. Read docs/PROJECT_SPEC.md — project vision, scope, V1 definition.
2. Read PROJECT_STATE.md — current phase and what is blocked.
3. Read TODO.md — current task list and priorities.
4. Determine which AI work mode applies to your session: see docs/AGENT_ROLES.md.

If you are starting a new session, state explicitly which mode you are working in
and what the task is.

---

## Core Rules (non-negotiable)

1. EVIDENCE BEFORE IMPLEMENTATION.
   Do not write G2P rules, phoneme inventories, or pronunciation mappings before
   the relevant research questions in docs/RESEARCH_LOG.md have entries with
   cited sources and evidence-status labels.

2. EVIDENCE-STATUS LABELS ARE MANDATORY.
   Every linguistic claim must be labeled with one of:
     ESTABLISHED / RECONSTRUCTED / UNCERTAIN / ASSUMPTION
   Never state a reconstructed pronunciation as if it were established fact.

3. AI-GENERATED CLAIMS ARE NOT LINGUISTIC EVIDENCE.
   A claim produced by an AI system — including this one — is not a citable source.
   It may suggest a direction for research, but it must never appear in RESEARCH_LOG.md
   as a finding. Sources must be real academic publications or citable scholarly work.

4. CONFLICTING SOURCES ARE DOCUMENTED, NOT SILENTLY RESOLVED.
   When sources disagree about a phonological feature, record both positions
   and note the conflict in RESEARCH_LOG.md. Do not choose one silently.

5. UNCERTAINTY IS DOCUMENTED, NOT HIDDEN.
   If the evidence for a pronunciation is thin, say so explicitly.
   UNCERTAIN is a valid and important evidence-status label.

6. DO NOT IMPLEMENT BEFORE THE PHASE IS READY.
   Check PROJECT_STATE.md and TODO.md for the current phase.
   Phase 4 = V1 Integration & Evaluation (Code authorized).
   Phase 2 = Data Audit only. No G2P rules.
   Phase 3 = Implementation of verified findings only.

7. DO NOT COMMIT OR PUSH UNLESS THE USER EXPLICITLY ASKS.

---

## Current Phase

See PROJECT_STATE.md for the authoritative current phase.

At the time this file was written: Phase 4 — V1 (Integration & Evaluation).

---

## Work Modes

See docs/AGENT_ROLES.md for full definitions. Summary:

    Researcher / Linguist
      Investigates linguistic questions. Writes to docs/RESEARCH_LOG.md.
      Does not write code. Does not invent rules.

    Engineer / Builder
      Implements only approved, cited findings. Writes to src/ and tests/.
      Does not invent linguistic rules. Cites RESEARCH_LOG.md entries in code.

    Manager / Reviewer
      Maintains project state. Writes to PROJECT_STATE.md, TODO.md, docs/DECISIONS.md.
      Does not invent conclusions. Enforces phase gate criteria.

---

## Explicitly Out of Scope

Do not add, suggest, or implement any of the following:

- Chatbot functionality
- Machine translation
- Kawi OCR or Kawi script recognition
- Kawi script rendering or display
- Voice cloning
- Multi-speaker synthesis
- Emotional speech synthesis
- Training a foundation language model from scratch
- Autonomous multi-agent frameworks
- Unnecessary infrastructure

---

## What to Do When You Are Unsure

If you are unsure whether a pronunciation claim is linguistically supported,
err on the side of labeling it UNCERTAIN or ASSUMPTION and noting what research
is needed to resolve it.

If you are unsure whether an implementation task is appropriate for the current
phase, check PROJECT_STATE.md and TODO.md. If it is listed as BLOCKED, do not
proceed.

If a source conflicts with another source, document the conflict — do not choose.

When in doubt about whether to write a piece of code, ask: does a RESEARCH_LOG.md
entry with a cited source justify this specific rule? If not, do not write it.

---

## Repository Source of Truth

The following files are the authoritative state of the project:

    PROJECT_STATE.md      current phase, active assumptions, completed milestones
    TODO.md               prioritized task list by phase
    docs/RESEARCH_LOG.md  all linguistic findings, open questions, bibliography
    docs/PROJECT_SPEC.md  vision, scope, V1 definition, core principles
    docs/ARCHITECTURE.md  provisional architecture (marked clearly as provisional)
    docs/DECISIONS.md     engineering decision log
    docs/AGENT_ROLES.md   work mode definitions

If any of the above files has not been read in the current session, read it before
doing work that depends on it.
