import re

with open('PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Update header
text = text.replace('**Current phase:** Phase 6 — V2 Profile Implementation (Active)', '**Current phase:** Phase 7 — Acoustic Backend Research & Data Strategy (Active)')

# Section replacement for Current Phase
old_current_phase = """## Current Phase: Phase 6 — V2 Profile Implementation
 
 ### What Phase 5 accomplished
 
 P5-001 through P5-003 established the conceptual layer architecture for V2. The V1 acoustic baseline effectively produces Profile B (Scholarly Reading). Policy is now set to support evidence-backed acoustic mergers for Profile A in V2 via a `ProfileStrategy` abstraction layer without modifying the canonical lossless representation.

### Phase 6 Entry Criteria
Phase 5 is complete:
- P5-001 and P5-002: Acoustic Profile Policy defined.
- P5-003: Conceptual software architecture and Vowel Length Strategy defined.

### Phase 6 Active
P6-001 is complete: Implemented `ProfileStrategy` abstraction.
P6-002 is complete: Validated Profile A vs Profile B behavior, and applied P5-002A minimal correction to align aspirate mergers strictly with evidence.
P6-003 is complete (Reconciled via P6-003R): Authored Vowel Length Strategy (`docs/P6_003_VOWEL_LENGTH_STRATEGY.md`). Profile A explicitly drops the `ː` duration marker as an engineering fallback to prevent the backend from silently synthesizing an unsupported historical long vowel, while tagging it `UNRESOLVED`.
"""

new_current_phase = """## Current Phase: Phase 7 — Acoustic Backend Research & Data Strategy

### What Phase 6 accomplished
P6-001 through P6-004 implemented the Profile Strategy layer, isolating canonical representation from acoustic profile rules (Profile A vs B). P6-003R secured the vowel-length unresolved fallback. P6-004 evaluated the feasibility of an etymological metadata classifier, concluding it is currently BLOCKED by insufficient dataset provenance.

### Phase 7 Entry Criteria
Phase 6 implementation is stable and all tests pass (94/94). The project requires a path toward a better acoustic backend (e.g., Piper/VITS) without sacrificing explicit Profile A control.

### Phase 7 Active
- Completed P7-001: Data Acquisition & Corpus Design (`docs/P7_001_CORPUS_DESIGN.md`). Designed a minimal, targeted corpus strategy specifically to teach a neural model the Profile A `/ṭ/` vs `/t/` retroflex contrast.
- Pending P7-002: Pilot Corpus Recording.
"""

text = text.replace(old_current_phase, new_current_phase)

# Insert Phase 6 into Completed Milestones
p5_header = '### Phase 5 — Post-V1 Research (Completed)'
p6_completed = """### Phase 6 — V2 Profile Implementation (Completed)

- Completed P6-001: Implemented `ProfileStrategy` abstraction layer.
- Completed P6-002: Validated Profile A vs Profile B execution matrix. Applied P5-002A correction to strictly align aspirate rules with historical evidence.
- Completed P6-003R: Established Vowel Length Strategy. Explicitly stripped duration markers in Profile A as an engineering fallback to preserve `UNRESOLVED` status acoustically.
- Completed P6-004: Lexical Metadata Feasibility Audit. Concluded etymological classification is impossible with current Wordnet data, formally blocking P6-005.

"""

text = text.replace(p5_header, p6_completed + p5_header)

# Update Blocked section
blocked_old = "Nothing is currently blocked. Phase 4 (V1 Integration & Evaluation) is underway (P4-001 through P4-005 completed, P4-006 next)."
blocked_new = "P6-005: Etymological Metadata Implementation is explicitly BLOCKED until an etymologically tagged dictionary dataset is obtained or created."
text = text.replace(blocked_old, blocked_new)

# Update Manager mode
manager_old = "Current active mode: Manager/Reviewer (Phase 0 through P4-005 Milestone Checkpoint complete; P4-006 next)"
manager_new = "Current active mode: Manager/Reviewer (Phase 7 Active)"
text = text.replace(manager_old, manager_new)

with open('PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(text)

