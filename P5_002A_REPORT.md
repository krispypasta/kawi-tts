# P5-002A POLICY SCOPE RECONCILIATION REPORT

## 1. Current implementation scope
**Profile A transforms:**
- **Voiced aspirates:** `bʱ`, `dʱ`, `gʱ`, `ɟʱ`, `ḍʱ` → merged to plain stops
- **Voiceless aspirates:** `pʰ`, `tʰ`, `kʰ`, `cʰ`, `ṭʰ` → merged to plain stops
- **Sibilants:** `ś`, `ṣ` → merged to `s`
- **Syllabic liquids:** `r̩`, `l̩` → adapted to `rə`, `lə`
- **Long syllabic liquids:** `r̩ː`, `l̩ː` → adapted to `rəː`, `ləː`
- **Vowels:** `aː`, `iː`, `uː`, `əː` → deferred (unresolved)

## 2. Current P5-002 policy scope
- **Aspirates:** explicitly lists only `bh`, `dh`, `gh`, `ph` for merger.
- **Sibilants:** explicitly lists `ś`, `ṣ` for merger.
- **Syllabic liquids:** explicitly lists `ṛ`, `ḷ` for adaptation.
- **Vowels:** explicitly lists `ā`, `ī`, `ū` as unresolved.

## 3. Aspirate class audit
- **`bh`, `dh`, `gh`, `ph`:** EVIDENCE-BACKED. Explicitly supported by Van der Molen (2015) and Teselkin (1972) as not representing aspirated consonants in spoken Old Javanese.
- **`kh`, `th`, `ch`, `jh`, `ṭh`, `ḍh`:** UNRESOLVED. No cited source explicitly documents their merger in spoken Kawi. While inferred absent from the native inventory, applying a blanket merger is a "Project Inference", not direct evidence.

## 4. Liquid class audit
- **`ṛ`, `ḷ`:** PROVISIONAL. Acri & Griffiths (2014) explicitly note their phonetic adaptation as `rĕ`/`lĕ` (`[rə]`, `[lə]`).
- **`ṝ`, `ḹ`:** UNRESOLVED. Theoretical extrapolations based on Sanskrit/Unicode patterns. No independent evidentiary support exists in the repository for their usage or adaptation in Old Javanese.

## 5. Vowel-length class audit
- **`ā`, `ī`, `ū`:** UNRESOLVED. Van der Molen notes length in Sanskrit loans was likely neglected, while native macrons may have sometimes indicated a phonetic distinction.
- **`əː` (ö):** UNRESOLVED. Orthographic transliteration of a specific Indic script sign (Damais 1970; Acri & Griffiths 2014). Phonetic reality of a sustained duration `[əː]` is unsupported.

## 6. Full scope matrix

| TOKEN / CLASS | CURRENT IMPLEMENTATION | P5-002 CURRENT POLICY | EVIDENCE SUPPORT | PROFILE A RECOMMENDATION | STATUS | ACTION |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `bh`, `dh`, `gh`, `ph` | Merged (`b`, `d`, `g`, `p`) | Merge | Yes (Van der Molen, Teselkin) | Merge | EVIDENCE-BACKED | KEEP |
| `kh`, `th`, `ch`, `jh`, `ṭh`, `ḍh`| Merged | Not Listed | None cited for phonetic realization | Pass-through / Fallback | UNRESOLVED | NARROW IMPLEMENTATION |
| `ś`, `ṣ` | Merged (`s`) | Merge | Yes (Teselkin) | Merge | EVIDENCE-BACKED | KEEP |
| `ṛ`, `ḷ` | Adapted (`rə`, `lə`) | Adapt | Yes (Acri & Griffiths) | Adapt | PROVISIONAL | KEEP |
| `ṝ`, `ḹ` | Adapted (`rəː`, `ləː`) | Not Listed | No (Theoretical Unicode pattern) | Pass-through / Fallback | UNRESOLVED | NARROW IMPLEMENTATION |
| `ā`, `ī`, `ū` | Deferred | Deferred | Yes (Van der Molen) | Deferred | UNRESOLVED | KEEP |
| `əː` | Deferred | Not Listed | Yes (Acri & Griffiths, Damais) | Deferred | UNRESOLVED | EXPAND POLICY |

## 7. Evidence verification
- **SOURCE EXPLICITLY SAYS:** `bh, dh, gh, ph` merged (Van der Molen, Teselkin); `ś, ṣ` merged (Teselkin); `ṛ, ḷ` adapted to `rĕ, lĕ` (Acri & Griffiths).
- **PROJECT INFERENCE:** That all other Sanskrit aspirates (`kh`, `th`, etc.) merged identically.
- **ENGINEERING POLICY:** That Unicode long syllabic liquids (`ṝ`, `ḹ`) adapt identically to their short counterparts.

## 8. Unsupported extrapolations
1. Merging un-cited Sanskrit aspirates (`kh, th, ch, jh, ṭh, ḍh`) into plain stops without explicit source evidence.
2. Adapting theoretical extended liquids (`ṝ, ḹ`) into `rəː, ləː` without textual/historical evidence of their occurrence or adaptation in Old Javanese.

## 9. Human decisions required
None. The PRIMARY RULE dictates that without explicit evidence, the narrower policy must be preserved. The expanded implementation must be rolled back to match the evidence.

## 10. Minimal correction recommendation
**OUTCOME B:** Keep P5-002 narrow for aspirates and liquids, and reduce Profile A implementation to match it. Treat the un-cited aspirates and extended liquids as `UNRESOLVED` (they will correctly fall through to `PRESERVED` or `PROVISIONAL` legacy handling, exposing the lack of Profile A policy).
**OUTCOME A (Partial):** Expand P5-002 policy to explicitly include `əː` under the Vowel Length/Macrons section as an unresolved orthographic transliteration, since evidence confirms it functions similarly to the other macrons.

## 11. Exact code/doc changes proposed
**`src/acoustic/strategies/profile_a.py`:**
- Remove `ɟʱ`, `ḍʱ`, `tʰ`, `kʰ`, `cʰ`, `ṭʰ` from `_ASPIRATE_MERGERS` (leaving only `bʱ`, `dʱ`, `gʱ`, `pʰ`).
- Remove `r̩ː`, `l̩ː` from `_LIQUID_ADAPTATIONS` (leaving only `r̩`, `l̩`).

**`docs/P5_002_ACOUSTIC_PROFILE_POLICY.md`:**
- Add `əː` (ö) to Section 5.D as UNRESOLVED (Evidence Status: Orthographic transliteration marker without proven phonetic duration).

## 12. Regression risks
**Zero.** V1 and Profile B remain completely untouched. Profile A will simply sound "less adapted" for unsupported Sanskrit loanwords containing `kh, th, ṭh` etc., which correctly reflects our current epistemic uncertainty. No test coverage relies on Profile A merging these un-cited aspirates except one A-specific matrix row we can easily adjust.

## 13. Whether P6-003 is now unblocked
**Yes.** Once this minimal correction is applied, the Profile A implementation will strictly match the evidence limit, clearing the path to begin P6-003 (Vowel Length Strategy) with a clean epistemic foundation.

## 14. Exact next action
Wait for user authorization to execute the proposed changes to `profile_a.py` and `P5_002_ACOUSTIC_PROFILE_POLICY.md`.
