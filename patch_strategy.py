with open("docs/P6_003_VOWEL_LENGTH_STRATEGY.md", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
"""## 10. Profile A Behavior (Historical Spoken)
*   **Known Loan (Future):** Evidence-backed merger/reduction.
*   **Known Native (Future):** Unresolved or context-specific stress.
*   **Current/Unknown Provenance:** Map canonical token to target token identically (e.g., `aː` → `aː`) but explicitly flag as `PolicyStatus.UNRESOLVED`. **Do not invent length, do not invent merger.**""",
"""## 10. Profile A Behavior (Historical Spoken)
*   **Known Loan (Future):** Evidence-backed merger/reduction.
*   **Known Native (Future):** Unresolved or context-specific stress.
*   **Current/Unknown Provenance:** Profile A preserves the canonical vowel-length distinction in metadata but does not currently claim a historical acoustic duration. As an explicit engineering fallback, the duration marker `ː` is stripped before hitting the backend (`aː` → `a`) to prevent the TTS engine from silently committing to an unverified long-duration feature, while tagging the status as `PolicyStatus.UNRESOLVED`."""
)

text = text.replace(
"""## 12. Unknown-Provenance Fallback
For any word where etymology or metrical context cannot be programmatically proven, Profile A must default to `UNRESOLVED` and preserve the canonical length token to prevent destructive assumptions.""",
"""## 12. Unknown-Provenance Fallback
For any word where etymology or metrical context cannot be programmatically proven, Profile A must default to `UNRESOLVED`. To satisfy backend execution without making a false historical claim, Profile A strips the acoustic duration marker. This is strictly an engineering fallback, not a claim that all vowels were short."""
)

text = text.replace(
"""## 15. Implementation Implications
No changes to `src/acoustic/strategies/` are required at this time. The current fallback behavior in `ProfileAStrategy` (returning `UNRESOLVED` for `aː`, `iː`, `uː`, `əː`) already correctly implements this policy.""",
"""## 15. Implementation Implications
During P6-003R, `src/acoustic/strategies/profile_a.py` was updated so that unresolved macrons (`aː`, `iː`, `uː`, `əː`) drop the `ː` in their `target_token` to avoid silently committing to a long vowel at the acoustic backend. `AcousticMapper` was also updated to truly propagate `MappingStatus.UNRESOLVED` rather than concealing it."""
)

with open("docs/P6_003_VOWEL_LENGTH_STRATEGY.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Docs patched.")
