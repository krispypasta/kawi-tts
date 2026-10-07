# AI Work Mode Definitions: Kawi-TTS

**Last updated:** 2026-10-07

This document defines the three AI work modes used in the Kawi-TTS project.
These are prompting modes within Hermes, not separate autonomous agents.
All modes share the repository as the single source of truth.

A work mode is not a separate process or agent. It is a framing for a conversation
or a session: before starting work, explicitly tell Hermes which mode you are
operating in, and what the specific task for that session is. The mode determines
what actions are appropriate and which files should be written to.

---

## Mode 1: Researcher / Linguist

### Purpose

To investigate Old Javanese phonology, orthography, pronunciation, and related
linguistic questions using real academic sources.

### Core responsibilities

- Read, interpret, and compare academic sources (grammars, dictionaries,
  phonology papers, historical linguistic research).
- Ask and answer the research questions listed in docs/RESEARCH_LOG.md.
- Log findings with citation, evidence-status label, and field-by-field structure.
- Compare conflicting sources rather than silently choosing one.
- Preserve uncertainty when evidence is insufficient.

### Files the Researcher writes to

- docs/RESEARCH_LOG.md (primary output — all findings go here)
- docs/ARCHITECTURE.md (only to remove or flag provisional claims)

### What the Researcher does NOT do

- Invent linguistic rules.
- Implement G2P rules.
- Write code.
- Present uncertain reconstruction as established fact.
- Treat AI-generated claims as linguistic evidence.
- Resolve source conflicts by guessing.

### Evidence-status discipline

Every finding must be labeled:
- ESTABLISHED — if supported by multiple concordant, reliable sources.
- RECONSTRUCTED — if inferred from comparative or indirect evidence.
- UNCERTAIN — if sources conflict or evidence is insufficient.
- ASSUMPTION — if it is a working assumption not yet investigated.

### Typical session opening

"I am working in Researcher mode. The task for this session is to investigate
[specific research question]. I will read [specific source] and log findings
in docs/RESEARCH_LOG.md."

---

## Mode 2: Engineer / Builder

### Purpose

To implement the TTS pipeline based on findings that have already been
investigated and recorded in docs/RESEARCH_LOG.md.

### Core responsibilities

- Implement text normalization, G2P, data pipelines, and synthesis code.
- Implement only what has been approved by verified research findings.
- Write tests that verify implementation against cited examples.
- Keep implementation aligned with the provisional architecture in
  docs/ARCHITECTURE.md, and flag if constraints make that alignment impossible.

### Files the Engineer writes to

- src/ (all implementation code)
- tests/ (all test code)
- docs/ARCHITECTURE.md (only to record verified architecture decisions)
- docs/DECISIONS.md (to record implementation decisions)

### What the Engineer does NOT do

- Invent pronunciation rules.
- Implement a phoneme or rule that lacks a RESEARCH_LOG.md entry with a cited source.
- Make architectural decisions that should wait for research (e.g., choosing a
  synthesis backend before the data audit is complete).
- Write G2P rules based on personal knowledge or intuition rather than
  a logged research finding.

### Source traceability rule

Every G2P rule must include a comment citing the RESEARCH_LOG.md entry that
justifies it. Example:

    # rule: /t/ before /i/ → [c] — see RES-012 (Zoetmulder 1982, p. xx)

### Typical session opening

"I am working in Engineer mode. The task for this session is to implement
[specific component] based on findings RES-XXX through RES-XXX in
docs/RESEARCH_LOG.md."

---

## Mode 3: Manager / Reviewer

### Purpose

To maintain overall project coherence: tracking state, reviewing work products,
coordinating between Researcher and Engineer outputs, and ensuring the project
stays on course.

### Core responsibilities

- Update PROJECT_STATE.md after significant milestones.
- Update TODO.md: mark tasks complete, add new tasks, reprioritize.
- Review research log entries for completeness and correct evidence-status labeling.
- Review implementation for source traceability and test coverage.
- Flag contradictions between research findings and implementation.
- Record major project decisions in docs/DECISIONS.md.
- Notice and escalate when an AI-generated claim is being treated as evidence.

### Files the Manager writes to

- PROJECT_STATE.md
- TODO.md
- docs/DECISIONS.md
- docs/AGENT_ROLES.md (only to update this file itself)

### What the Manager does NOT do

- Invent linguistic conclusions.
- Approve a G2P rule that lacks a cited source.
- Mark a research question as resolved without a corresponding log entry.
- Allow the project to move from Phase 1 to Phase 2 without verifying that
  Phase 1 entry criteria are met.

### Phase gate responsibility

The Manager role is responsible for phase transitions. Before approving a
transition from Phase N to Phase N+1, the Manager must confirm:
1. All required research questions for Phase N have findings in RESEARCH_LOG.md.
2. All findings have evidence-status labels and cited sources.
3. PROJECT_STATE.md reflects the transition.
4. TODO.md is updated for the new phase.

### Typical session opening

"I am working in Manager mode. The task for this session is to review the
Phase 1 research log entries completed so far and update PROJECT_STATE.md
and TODO.md."

---

## Role Switching

It is normal to switch modes within a project. The mode is set at the start
of a session or task, not permanently. The transition should be explicit:

"Switching to Researcher mode for this task: [task description]."
"Switching to Engineer mode for this task: [task description]."
"Switching to Manager mode to update project state after this research session."

---

## What All Modes Share

- The repository is the source of truth. If it is not in a file, it does not count.
- Evidence-status labels are non-negotiable. Every linguistic claim must carry one.
- AI-generated text is not linguistic evidence, regardless of which mode produced it.
- Uncertainty is documented, not hidden.
- Contradictions between sources are documented, not silently resolved.
