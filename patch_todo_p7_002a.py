import re

with open("TODO.md", "r") as f:
    todo = f.read()

# Insert P7-002A before P7-002
p7_002a = """
- [x] **P7-002A: Existing Audio Source Audit (Correction)**
  - Rule out Abraham as ground truth.
  - Audit existing archives/YouTube for reference audio.
  - Evaluate licensing, epistemic categories, and acoustic viability.
  - Conclude GO-gate for project path.
"""

if "P7-002A" not in todo:
    todo = todo.replace("- [ ] **P7-002: Pilot Corpus Recording**", p7_002a + "\n- [ ] **P7-002: Pilot Corpus Recording**")

with open("TODO.md", "w") as f:
    f.write(todo)
