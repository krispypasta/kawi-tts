import re

with open("TODO.md", "r") as f:
    todo = f.read()

todo_new = todo.replace("## Phase 7: Acoustic Backend Research & Data Strategy (ACTIVE)", "## Phase 7: Zero-Budget Reassessment & Engine Hardening (ACTIVE)")

# Replace the old P7 tasks
old_p7_pattern = r"- \[x\] P7-001: Data Acquisition & Corpus Design.*?Scale-up Decision\. Go/No-go for 1-2 hour corpus recording based on P7-003\."
new_p7 = """- [x] P7-001: [DEFERRED/BLOCKED] Data Acquisition & Corpus Design (Superseded by P7-003 constraint).
- [x] P7-002A: Existing Audio Source Audit (Concluded Path C required, which is now blocked).
- [ ] P7-002: [BLOCKED] Pilot Corpus Recording. Deferred by zero-budget constraint.
- [x] P7-003: Zero-Budget Scope Reassessment & Frankenstein Stop. Redefined project to $0 core deliverable.

**Revised Zero-Cost Roadmap:**
- [ ] P7-B: Linguistic and pronunciation-engine hardening (normalization, G2P rules, ambiguity handling, test coverage).
- [ ] P7-C: Baseline Acoustic & Evaluation infrastructure (eSpeak backend control, deterministic synthesis, automated tests).
- [ ] P7-D: Research tooling (bibliography management, evidence-status tracking).
- [ ] P7-E: [OPTIONAL/FROZEN] Neural Reopening Criteria."""

todo_new = re.sub(old_p7_pattern, new_p7, todo_new, flags=re.DOTALL)

with open("TODO.md", "w") as f:
    f.write(todo_new)

with open("PROJECT_STATE.md", "r") as f:
    state = f.read()

state_new = state.replace("## Current Phase: Phase 7 — Acoustic Backend Research & Data Strategy", "## Current Phase: Phase 7 — Zero-Budget Reassessment & Engine Hardening")
state_new = state_new.replace("Phase 7 — Acoustic Backend Research & Data Strategy (Active)", "Phase 7 — Zero-Budget Reassessment & Engine Hardening (Active)")

active_replace = """### Phase 7 Active
- Completed P7-001: Data Acquisition & Corpus Design (`docs/P7_001_CORPUS_DESIGN.md`). Designed a minimal, targeted corpus strategy specifically to teach a neural model the Profile A `/ṭ/` vs `/t/` retroflex contrast.
- Pending P7-002: Pilot Corpus Recording."""

active_new = """### Phase 7 Active (Scope Reset)
- **FRANKENSTEIN STOP APPLIED**: The project operates on a strictly $0 budget. Neural TTS and paid expert corpora are now DEFERRED / OPTIONAL. 
- Completed P7-001 & P7-002A: Corpus design and existing audio audits proved a paid/commissioned expert speaker is required. 
- Completed P7-003: Zero-Budget Scope Reassessment (`docs/P7_003_ZERO_BUDGET_SCOPE_REASSESSMENT.md`). Reoriented project to focus on the core "Kawi Pronunciation & Reconstruction Engine" leveraging local, zero-cost eSpeak synthesis.
- Pending P7-B: Linguistic and pronunciation-engine hardening."""

state_new = state_new.replace(active_replace, active_new)

blocked_replace = """## Blocked / Waiting
 
P6-005: Etymological Metadata Implementation is explicitly BLOCKED until an etymologically tagged dictionary dataset is obtained or created."""

blocked_new = """## Blocked / Waiting

- **Neural TTS & Custom Corpora**: Explicitly BLOCKED/DEFERRED by the zero-budget constraint.
- **P6-005**: Etymological Metadata Implementation is explicitly BLOCKED until an etymologically tagged dictionary dataset is obtained or created."""

state_new = state_new.replace(blocked_replace, blocked_new)

with open("PROJECT_STATE.md", "w") as f:
    f.write(state_new)

