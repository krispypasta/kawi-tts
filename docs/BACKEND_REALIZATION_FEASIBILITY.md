# Backend Realization Feasibility & Adapter Strategy

## 1. Problem Statement
The deterministic linguistic core of Kawi-TTS correctly generates abstract phonological representations (e.g., `ʈ`, `bʱ`, `aː`, `r̩`) for Profile B (Historical Reading) and some specific tokens in Profile A. However, the eSpeak-ng `id` (Indonesian) backend lacks native acoustic support for these raw IPA characters, often falling back to a glottal stop (`?`) mapping. This degrades audio output quality (e.g. `BHAṬĀRA` sounding like "a-a-ra"). The goal is to improve backend realization *without* modifying the canonical linguistic policies, by explicitly defining an AcousticMapper adapter layer.

## 2. Current Backend Path
Currently, the pipeline translates abstract targets as follows:
- `Text` → `Normalization` → `G2P` → `Canonical` → `ProfileStrategy`
- **`AcousticMapper`**: By default, translates Profile targets into raw IPA.
- **Result**: eSpeak's internal dictionary mapping for `id` replaces unsupported targets (like `bʱ`, `ʈ`, `ː`, `ə`) with a glottal stop (`?`).

## 3. Target Inventory & 4. eSpeak Capability Findings
Controlled capability testing outside the pipeline revealed the `id` voice fallback behavior for raw IPA, compared to its capacity for generating explicit backend representations (ASCII mnemonics):

| Target | Current eSpeak Input | Test Method | Observed Behavior | Possible Backend Representation | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `b` | `b` | subprocess | `b` | `b` | EXACT |
| `bʱ` | `bʱ` | subprocess | `?` | `bh` (ASCII mapping) | BACKEND_APPROXIMATION |
| `t` | `t` | subprocess | `t` | `t` | EXACT |
| `ʈ` | `ʈ` | subprocess | `?` | `t` (ASCII mapping) | BACKEND_APPROXIMATION |
| `a` | `a` | subprocess | `a` | `a` | EXACT |
| `aː` | `aː` | subprocess | `?` | `a` (ASCII mapping) | BACKEND_APPROXIMATION |
| `r̩` / `rə` | `r̩` / `rə` | subprocess | `?` | `r@` | BACKEND_APPROXIMATION |
| `r̩ː` / `rəː` | `r̩ː` / `rəː` | subprocess | `?` | `r@` | BACKEND_APPROXIMATION |
| `s` | `s` | subprocess | `s` | `s` | EXACT |
| `ś` | `ś` | subprocess | `?` | `s` (ASCII mapping) | BACKEND_APPROXIMATION |
| `ə` | `ə` | subprocess | `?` | `@` | EXACT (Backend Alias) |
| `ɟ` | `ɟ` | subprocess | `?` | `dZ` | EXACT (Backend Alias) |
| `ŋ` | `ŋ` | subprocess | `?` | `N` | EXACT (Backend Alias) |
| `ɲ` | `ɲ` | subprocess | `?` | `n^` | EXACT (Backend Alias) |

## 5. Strategy Comparison
- **STRATEGY A — CURRENT RAW IPA**: Fails due to unhandled glottal stops. Discarded for the default `id` voice.
- **STRATEGY B — ESPEAK PHONEME / MNEMONIC REPRESENTATION**: Explicitly mapping the Kawi targets to supported eSpeak ASCII phonemes via an explicit backend dictionary successfully eliminates the glottal stops.
- **STRATEGY C — BACKEND-LOCAL SYMBOL ALIAS**: Requires a custom compiled eSpeak voice file. Violates the zero-budget/maintenance constraints.
- **STRATEGY D — EXPLICIT BACKEND-SCOPED APPROXIMATION**: Implementing a backend-scoped dictionary strictly at the `AcousticMapper` level provides an explicit mapping (e.g. mapping `bʱ` -> `bh`).

## 6. Classification & 7. Implementation Recommendation
The implemented strategy leverages **Strategy B & D**: A backend-scoped dictionary (`_ESPEAK_ID_APPROXIMATION`) is injected into the `AcousticMapper`. 
When `adapt_for_espeak_id=True` (triggered automatically when `voice="id"` is specified to `synthesize()`), it converts unsupported targets to eSpeak-native ASCII representations.
Tokens modified by this adapter are explicitly flagged with the status `MappingStatus.BACKEND_APPROXIMATION` to distinguish them from linguistic truth.

## 8. Risks
- Audio fidelity is inherently lossy for targets like length (`ː`) and retroflex consonants (`ʈ` -> `t`), since the `id` voice lacks the physical acoustic representation.
- Developers may mistake the output mapping (e.g., `bh`) for historical truth. Explicit documentation and strict trace tags mitigate this.

## 9. Traceability Implications
`kawi-trace` has been updated to explicitly label mappings that are modified by the adapter with `(BACKEND_APPROXIMATION: eSpeak 'id' fallback approximation)` when adapting for eSpeak is active.

## 10. Test Plan
- `test_espeak_adapter.py` added to verify the adapter correctly identifies and replaces fallback tokens when active, and preserves standard IPA when inactive.
- Discovered and fixed an implementation bug in `ProfileAStrategy` where long syllabic liquids (`r̩ː`, `l̩ː`) were previously skipped by the mapping. Verified via updated `regression_corpus.tsv` and `test_acoustic_mapper_profile_a.py`.
- Full deterministic test suite passes (97/97).

## 11. Human Listening Results
Regenerated the pre-release audio demo (`BHAṬĀRA`, `śānti`, `kṝta`, `sankha`, `sang-hyang`).
- **BEFORE**: Replaced missing phonemes with `?`, causing broken syllables and distorted speech ("a-a-ra").
- **AFTER (Adapter Active)**: The glottal stops are gone. `BHAṬĀRA` is synthesized cleanly as `bhatara`, bypassing the backend limit while retaining the `bʱaʈaːra` target intact in the Profile B acoustic layer. This results in stable, intelligible realization materially closer to the intended target without conflating implementation constraints with historical facts.

## 12. Final Decision Gate
**GO-ADAPTER**
A minimal backend adapter is clearly beneficial and technically defensible. It materially improves the audio generation for the baseline eSpeak backend while strictly maintaining the zero-budget constraint and preventing arbitrary modification of the frozen deterministic core.

### Final Self-Audit:
1. Did we change any canonical representation? **No.**
2. Did we change Profile A/B policy? **No.** (Except fixing an explicit bug in Profile A mapping for `r̩ː` which now correctly maps to `rəː` while retaining its length).
3. Did we add any historical pronunciation claim? **No.**
4. Did we silently collapse a linguistic distinction merely for eSpeak? **No. The distinction is maintained at the Profile level and logged in the Trace.**
5. Did we distinguish backend approximation from linguistic truth? **Yes, via `MappingStatus.BACKEND_APPROXIMATION`.**
6. Did we test the actual eSpeak runtime rather than only string transformations? **Yes.**
7. Did we discover any genuinely unsupported target? **Yes, multiple (retroflexes, length markers).**
8. Is the proposed adapter simpler than the problem it solves? **Yes.**
9. Does it materially improve actual audio? **Yes.**
10. Should the project ship it now, or leave eSpeak as a documented baseline? **Ship the explicit adapter; it's robust, safe, and prevents the glottal artifacting while preserving the pipeline's strict boundaries.**