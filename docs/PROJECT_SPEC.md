# Project Specification: Kawi-TTS

**Status:** ACTIVE — Phase 0 complete, entering Phase 1 (Linguistic Research)
**Last updated:** 2026-10-07
**Authoritative project state:** See PROJECT_STATE.md

---

## 1. Vision and Motivation

Kawi-TTS is a research-first Text-to-Speech project for Old Javanese (*Basa Kawi*). The motivation is personal and cultural: to demonstrate appreciation for Javanese language and culture, and to make Kawi more accessible through technology.

Old Javanese is a historical language. No recordings of native Old Javanese speakers from the period when the language was actively spoken are known to exist. This is a fundamental epistemic constraint: we cannot claim that any pronunciation produced by this system is "exactly how Old Javanese sounded." We can only claim that it is consistent with the best available linguistic evidence and scholarly reconstruction.

**The primary goal of V1 is linguistically defensible pronunciation, not naturalness.**

---

## 2. Core Principles

### 2.1 Evidence Comes Before Implementation

No G2P rule, phoneme assignment, normalization heuristic, or TTS architecture decision should be finalized before the relevant linguistic questions have been investigated using real academic sources.

The order is always:
1. Identify the research question.
2. Investigate using primary sources (grammars, dictionaries, papers, comparative data).
3. Record the finding with source citations and an evidence-status label.
4. Have the Manager review the finding.
5. Only then may the Engineer implement based on it.

### 2.2 Evidence-Status Labels

Every linguistic claim in this project must carry one of the following labels:

- **ESTABLISHED** — supported by multiple concordant reliable sources; well-accepted in the field.
- **RECONSTRUCTED** — inferred or reconstructed from indirect historical or comparative evidence; may be the best available answer but is not directly attested.
- **UNCERTAIN** — evidence is conflicting, ambiguous, or insufficient; genuine scholarly disagreement exists.
- **ASSUMPTION** — a temporary engineering or project working assumption made in the absence of adequate evidence; must be revisited when better evidence is found.

These labels appear in RESEARCH_LOG.md entries and in code comments for any rule derived from linguistic research.

### 2.3 Conflicting Sources Must Be Compared

When two or more sources disagree on a phonological claim, the project must not silently pick one. The investigation should address:

1. Who produced the source, and when?
2. What linguistic methodology was used?
3. What evidence supports the claim?
4. Do other sources corroborate or contradict it?
5. Is the disagreement genuine, or caused by different notation conventions?
6. Is one position more defensible given the evidence?
7. Is the question genuinely unresolved?

The outcome — including any remaining uncertainty — must be documented in RESEARCH_LOG.md.

### 2.4 AI-Generated Claims Are Not Linguistic Evidence

When an AI assistant is used for research, it must search for and read actual sources. An AI producing a phonological claim from its training data, without citing a specific verifiable source, is not providing linguistic evidence. Such output must be labeled ASSUMPTION at best and investigated further before use.

### 2.5 The Repository Is the Source of Truth

This is intended to be a long-running project over multiple months. Conversation memory cannot be trusted as a durable record. All important decisions, findings, open questions, and assumptions must be written into the repository files listed in section 6.

---

## 3. Project Scope

### 3.1 In Scope (V1)

- Old Javanese (Kawi) pronunciation research and reconstruction.
- Romanized Kawi text normalization.
- Grapheme-to-Phoneme (G2P) conversion based on researched phonological rules.
- Synthesis backend sufficient to produce audible speech from the G2P output.
- Documentation of all linguistic assumptions behind the pronunciation.
- Clear separation of established evidence from reconstruction from uncertainty.
- A system that allows individual pronunciation rules to be improved without rebuilding the whole project.

### 3.2 Explicitly Out of Scope (Initial Version)

The following are excluded from V1. They may be reconsidered later but must not distract from the core problem:

- Chatbot or conversational AI
- Machine translation into or out of Old Javanese
- OCR or automatic recognition of Kawi manuscript script
- Kawi script (Brahmic) rendering as a primary goal
- Voice cloning
- Multi-speaker synthesis
- Emotional or expressive speech
- Training a foundation model from scratch
- Unnecessary infrastructure or multi-agent frameworks
- Multilingual TTS support beyond the minimum needed for synthesis approach

---

## 4. V1 Definition

### 4.1 V1 Success Criteria

A meaningful V1 prototype should be able to:

1. Accept romanized Old Javanese text as input.
2. Normalize the text to a canonical form appropriate for phonological analysis.
3. Apply a G2P system that converts the normalized text to a phoneme sequence.
4. Produce audible speech from the phoneme sequence.
5. Print, on request, the phoneme sequence and the linguistic justification for each rule applied.
6. Distinguish — in its output documentation — which phonological decisions are ESTABLISHED, RECONSTRUCTED, UNCERTAIN, or ASSUMPTION.
7. Allow a future researcher or developer to update an individual pronunciation rule without rebuilding the pipeline from scratch.

Naturalness is explicitly secondary for V1.

### 4.2 V1 Minimum Example

Given the input text of a well-documented Old Javanese phrase, the system should be able to:
- Produce audio.
- Print the phoneme sequence used.
- Point to the source entry in RESEARCH_LOG.md that justifies that phoneme sequence.

### 4.3 What V1 Does Not Require

- Perfectly accurate historical pronunciation (unachievable without native recordings)
- Highly natural or expressive speech
- Complete coverage of all Old Javanese phonological edge cases
- A trained neural model (if a simpler synthesis approach is sufficient)
- Any of the items listed as out of scope in section 3.2

### 4.4 V1 Pronunciation Target (Profile A)

Based on DEC-006, the project conceptually separates three pronunciation profiles. V1 targets Profile A.

**PROFILE A — V1: Reconstructed Historical Spoken Old Javanese**
*Goal*: Produce the most defensible reconstruction of historical *spoken* Kawi that current evidence permits.
*Constraint*: This is an evidence-based *reconstruction*, NOT a claim of direct historical certainty.
*Implication*: We prioritize the native Austronesian phoneme inventory. Uncertainties regarding the phonetic realization of Sanskrit loanwords (e.g., vowel length, aspirates, palatal/retroflex sibilants) must NOT be silently forced into hard G2P rules.

**PROFILE B — FUTURE: Scholarly / Learned / Orthographic Reading**
*Goal*: Preserve more of the distinctions represented in scholarly romanization and Sanskrit-derived orthography. (Not V1).

**PROFILE C — FUTURE: Balinese Kakawin Performance / Mabasan**
*Goal*: Model the traditional chanted performance tradition, including metrical and musical realization. (Not V1).

### 4.5 V1 Epistemic Policy

The core philosophy of Kawi-TTS is: **"Evidence before implementation."**
The system will not optimize for sounding maximally Sanskrit, sounding maximally Balinese, blindly reproducing romanization symbols, inventing certainty, or producing natural-sounding speech at the expense of linguistic defensibility.

Evidence status must remain explicit:
- **ESTABLISHED**: May be treated as a strong V1 foundation.
- **RECONSTRUCTED**: May be used in V1 when necessary, but must be documented as reconstruction rather than fact.
- **UNCERTAIN**: Must NOT be silently converted into a definitive pronunciation rule. The project should preserve the uncertainty and determine an explicit handling strategy later.
- **ASSUMPTION**: Must never be presented as linguistic evidence. Requires an explicit project decision. The Engineer must never invent a pronunciation mapping simply because the TTS pipeline requires one.

---

## 5. Provisional Pipeline

**WARNING: PROVISIONAL — Do not treat this as a finalized architecture.**
The pipeline shape is expected; the technical implementation of each stage must be
determined after linguistic research and data auditing are complete.

    Kawi Text (romanized)
        |
        v
    Text Normalization
    (unicode normalization, diacritic standardization,
     punctuation, sandhi markers)
        |
        v
    Linguistic Analysis
    (morphological boundaries, loanword tagging,
     register identification — scope TBD by research)
        |
        v
    G2P / Pronunciation Representation
    (grapheme-to-phoneme rules, syllabification,
     stress assignment — rules derived from research findings only)
        |
        v
    Speech Synthesis
    (backend TBD: rule-based synthesis, phonologically-related-language
     transfer, model fine-tuning — choice depends on data audit)
        |
        v
    Audio Output

The synthesis backend must not be chosen until:
- The G2P phoneme inventory is defined by research.
- The data availability situation is understood.
- The phonological relationship between Old Javanese and candidate related
  languages (Balinese, Modern Javanese, Sanskrit) has been assessed.

---

## 6. Repository Documentation Standards

The following files collectively constitute the project's source of truth:

| File | Purpose |
| :--- | :--- |
| PROJECT_STATE.md | Current phase, what is done, what is blocked, next milestone |
| TODO.md | Prioritized actionable task list, organized by phase |
| docs/PROJECT_SPEC.md | This file: vision, scope, V1 definition, principles |
| docs/ARCHITECTURE.md | Provisional technical architecture; not final until research complete |
| docs/RESEARCH_LOG.md | All research findings, open questions, bibliography, dataset audit |
| docs/AGENT_ROLES.md | Definitions of the three AI work modes used in this project |
| docs/P3_003A_G2P_SPEC.md | G2P Internal Representation Specification (Phase 3) |
| docs/DECISIONS.md | Log of engineering and architectural decisions with rationale |
| AGENTS.md | Top-level guidance for any AI working in this repository |

Git history should represent meaningful milestones, not every file save.

---

## 7. Quality Standards

- Every G2P rule that reaches implementation must cite a specific entry in RESEARCH_LOG.md.
- Every RESEARCH_LOG.md entry must cite a specific source (author, title, year; page or section when available).
- Findings labeled ESTABLISHED must be supported by multiple concordant sources or a consensus position in the field.
- Findings labeled UNCERTAIN must document the nature of the disagreement and what would resolve it.
- Findings labeled ASSUMPTION must note what research would be needed to promote them to RECONSTRUCTED or ESTABLISHED.
- Engineering decisions that go beyond what research findings directly specify must be logged in docs/DECISIONS.md.

---

## 8. Linguistic Scope (Preliminary — Research Required)

The following is a list of linguistic features the system will need to handle.
This is NOT a phoneme inventory or a set of pronunciation rules.
It is a list of features that must be researched. All phonological conclusions
must come from Phase 1 research, not from this list.

Features to be investigated:
- Vowel inventory: a, i, u, e, o and their long counterparts; pepet (schwa); diphthongs
- Consonant inventory: stops (plain, aspirated, voiced, retroflex), nasals, fricatives, liquids, semivowels
- Place of articulation distinctions: velar, palatal, retroflex, dental, labial
- Aspirated series: status in native vs. Sanskrit-loan vocabulary
- Retroflex series: status and phonetic realization
- Sibilant distinctions: s, s-with-acute (palatal), s-with-underdot (retroflex)
- Syllable structure and consonant clusters
- Vowel length and its phonemic vs. metrical status
- Stress and prosody
- Sandhi (vowel and consonant junction rules at morpheme/word boundaries)
- Romanization conventions and how they map to the underlying phonology

These features must not be assigned phoneme values or IPA mappings until
the Phase 1 research produces evidence-backed answers.
