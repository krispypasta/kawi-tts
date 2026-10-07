# Engineering Decision Log: Kawi-TTS

**Last updated:** 2026-10-07

This file records significant engineering and project decisions — what was decided,
why, what alternatives were considered, and what assumptions or conditions the
decision depends on.

Decisions made before research is complete are marked [PRE-RESEARCH].
A pre-research decision may need to be revisited once Phase 1 is complete.

Decisions that depend on active research findings are marked [PENDING RESEARCH].
They should not be treated as final until the dependency is resolved.

---

## Decision Template

    DEC-XXX: [Short title]
    Date: YYYY-MM-DD
    Status: [DECIDED / PENDING RESEARCH / REVISITED / SUPERSEDED]
    Made by: [AI role / user]
    Decision: [What was decided]
    Rationale: [Why this was chosen]
    Alternatives considered: [What else was considered]
    Dependencies: [What this decision assumes or depends on]
    Review trigger: [What would cause this decision to be revisited]

---

## Decisions

### DEC-001: Research-first project structure (no implementation before Phase 1)

Date: 2026-10-07
Status: DECIDED
Made by: User (project owner)
Decision: No G2P rules, phoneme inventories, synthesis code, or architecture
choices may be finalized before Phase 1 Linguistic Research is complete.
Any such items in the existing repository scaffold are explicitly labeled
provisional or removed.
Rationale: Old Javanese is a historical language with no native-speaker recordings.
Pronunciation reconstruction requires real linguistic evidence. Implementing before
researching would produce a system whose pronunciation rules cannot be justified.
Alternatives considered: None — this is the foundational project philosophy.
Dependencies: None.
Review trigger: This decision is not subject to reversal. Individual sub-decisions
within Phase 1 may be revisited as evidence accumulates.

---

### DEC-002: Romanized Old Javanese as primary TTS input format [PRE-RESEARCH]

Date: 2026-10-07
Status: PRE-RESEARCH (provisional decision; to be confirmed after RQ-010, RQ-011)
Made by: Project planning (Manager role)
Decision: The TTS system will accept romanized Old Javanese text as primary input,
not Kawi script (Kawi aksara).
Rationale: The majority of scholarly Old Javanese materials are available in romanized
form. Kawi script recognition is explicitly out of scope for V1.
Alternatives considered:
- Kawi script input: out of scope for V1 per DEC-001 and project scope statement.
- Unicode Kawi codepoint input: could be a future extension, not V1.
Dependencies: Assumes romanized corpora are available and usable.
Review trigger: If Phase 1 research reveals that no usable romanized corpus exists
and only Kawi script materials are available, this decision must be revisited.

---

### DEC-003: Zoetmulder (1982) as primary lexicographic reference [PRE-RESEARCH]

Date: 2026-10-07
Status: PRE-RESEARCH (provisional; to be confirmed by RQ-010)
Made by: Project planning (Manager role)
Decision: The Old Javanese-English Dictionary (Zoetmulder & Robson 1982) is the
primary lexicographic and orthographic reference for the project.
Rationale: It is the most comprehensive published Old Javanese dictionary, widely
cited in the field, and the standard transliteration reference for most scholarly work.
Alternatives considered:
- Older Dutch sources: relevant for historical comparison but not primary for the
  romanization convention decision.
Dependencies: Assumes Zoetmulder (1982) uses a systematic, describable romanization
convention. Must be verified by reading the dictionary introduction (task P1-001).
Review trigger: If Phase 1 research reveals that Zoetmulder (1982) does not provide
adequate phonological information, additional primary sources must be identified.

---

### DEC-004: Three AI work modes (not autonomous agents)

Date: 2026-10-07
Status: DECIDED
Made by: User (project owner) + Manager role
Decision: The project uses three AI work modes (Researcher/Linguist, Engineer/Builder,
Manager/Reviewer) as prompting frameworks within Hermes. They are NOT implemented
as separate autonomous agents, separate processes, or multi-agent orchestration.
Rationale: Multi-agent frameworks are explicitly out of scope for this project.
The repository is the shared source of truth and the coordination mechanism.
Alternatives considered:
- Separate agent processes: rejected as unnecessary infrastructure.
- Single undifferentiated AI role: rejected because it blurs the line between
  linguistic research and implementation, which is a core epistemological concern.
Dependencies: None.
Review trigger: If the project grows to a scale where a single AI session cannot
hold the relevant context, a multi-session or delegation approach may be considered —
but only after the research phase is complete.

---

### DEC-005: V1 scope (text → audio + phoneme sequence + source citations)

Date: 2026-10-07
Status: DECIDED
Made by: User (project owner)
Decision: V1 is a system that accepts romanized Old Javanese text and produces:
(a) audio output, (b) a printable phoneme sequence, and (c) a source citation
for each pronunciation rule applied. V1 does NOT require natural-sounding speech.
Rationale: The primary V1 goal is linguistically defensible pronunciation,
not naturalness. Traceability to evidence is the success criterion.
Alternatives considered:
- High-naturalness neural TTS: out of scope for V1; requires more data and
  more architecture decisions than are appropriate before research.
Dependencies: Requires Phase 1 and Phase 2 to complete before implementation.
Review trigger: If Phase 2 data audit reveals unexpectedly rich audio resources,
the V1 naturalness goal may be revisited — but the traceability requirement stands.

---

### DEC-006: V1 Pronunciation Target (Profile A)

Date: 2026-10-07
Status: DECIDED
Made by: User (project owner) / Manager role
Decision: Kawi-TTS V1 will pursue "Reconstructed Historical Spoken Old Javanese" (Profile A).
This target explicitly means:
1. It is a linguistically evidence-based reconstruction, NOT a claim of historically proven certainty. We do not have 9th-century recordings.
2. We prioritize the reconstructed native Austronesian phoneme inventory.
3. However, uncertainties regarding how the historical elite pronounced Sanskrit loanwords (e.g., vowel length, aspirates, palatal/retroflex sibilants) must NOT be silently forced into hard G2P rules. These remain UNCERTAIN and will require explicit handling strategies.
Rationale: The project philosophy is "evidence before implementation." Producing the most defensible historical reconstruction aligns with this goal. Optimizing for modern Balinese chanting (Profile C) or artificial orthographic reading (Profile B) is reserved for future extensions.
Alternatives considered:
- Profile B (Scholarly/Orthographic Reading): Maximizes textual distinction but may simulate an artificial register. Deferred to future.
- Profile C (Balinese Kakawin Performance): Authentic to living tradition, but produces musical chanting rather than conversational speech. Deferred to future.
Dependencies: Requires Phase 1 (Linguistic Research) to establish boundaries of certainty and uncertainty.
Review trigger: None for V1. This is the foundational goal of the first release.

---

## Pending Decisions (awaiting research)

These decisions cannot be made until the indicated research questions are resolved.

PENDING-001: Which romanization convention is the primary TTS input format?
Depends on: RQ-010 (Zoetmulder romanization survey), RQ-011 (alternative conventions).
To be recorded as a formal DEC entry after P1-009 is complete.

PENDING-002: What is the phoneme inventory for the G2P system?
Depends on: RQ-001 through RQ-006 (full phoneme inventory research).
Cannot be decided until Phase 1 is substantially complete.

PENDING-003: What is the TTS synthesis backend for V1?
Depends on: RQ-018 (audio data availability), RQ-020 (TTS approach evaluation).
Cannot be decided until Phase 2 data audit is complete.
