import re

with open('TODO.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Update header
text = text.replace('**Current phase:** Phase 6 — V2 Profile Implementation', '**Current phase:** Phase 7 — Acoustic Backend Research & Data Strategy')

# Mark Phase 6 as COMPLETED and add missing tasks
p6_active = '## Phase 6: V2 Profile Implementation (ACTIVE)'
p6_completed = '## Phase 6: V2 Profile Implementation (COMPLETED)'
text = text.replace(p6_active, p6_completed)

# Add P6-004 and P6-005 to Phase 6
p6_003_line = '- [x] P6-003: Vowel Length Strategy (Research & Policy Document). Establish etymological constraints and fallback mechanism.'
p6_additions = p6_003_line + '\n- [x] P6-004: Lexical/Etymological Metadata Feasibility Audit. Concluded metadata classifier is blocked by data.\n- [ ] P6-005: [BLOCKED] Etymological Metadata Implementation. Requires provenance-tagged lexicon.'
text = text.replace(p6_003_line, p6_additions)

# Insert Phase 7 before Phase 4
p4_header = '## Phase 4: V1 (COMPLETED)'
p7_content = """## Phase 7: Acoustic Backend Research & Data Strategy (ACTIVE)

- [x] P7-001: Data Acquisition & Corpus Design. Design the minimal custom corpus to train/evaluate a future Kawi-TTS neural backend.
- [ ] P7-002: Pilot Corpus Recording. Record and annotate 50 sentences prioritizing dental/retroflex contrast.
- [ ] P7-003: Pilot Neural Experiment. Train Piper/VITS on pilot data and evaluate /ṭ/ synthesis.
- [ ] P7-004: Scale-up Decision. Go/No-go for 1-2 hour corpus recording based on P7-003.

"""
text = text.replace(p4_header, p7_content + p4_header)

with open('TODO.md', 'w', encoding='utf-8') as f:
    f.write(text)

