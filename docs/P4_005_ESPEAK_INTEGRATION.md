# P4-005 eSpeak Integration

## Environment
- Host: Windows
- Installation Route: `winget install eSpeak-NG.eSpeak-NG`
- eSpeak version: 1.52.0
- Executable path: `C:\Program Files\eSpeak NG\espeak-ng.exe`

## Voice Inventory
- `jv` (Javanese) voice does NOT exist in the standard eSpeak-ng 1.52.0 Windows installation.
- `id` (Indonesian) voice exists and is functional.

## Selected Voice
- `id` (Indonesian) has been selected as the V1 fallback backend voice.
- **Note:** This choice is a backend implementation necessity and does not affect the linguistic tokenization. The G2P pipeline remains completely independent of this fallback.

## Invocation Strategy
- The integration uses the standard subprocess module to invoke `espeak-ng`.
- Command syntax: `espeak-ng -v <voice> -w <output_path> "[[<phonemes>]]"`
- No `--ipa` flag was required since raw Unicode IPA mapped tokens successfully processed via the eSpeak `[[...]]` inline phoneme argument.

## Smoke-Test Result
- Real eSpeak generation works successfully.
- Dummy WAV generation continues to function under `dry_run=True`.

## Kawi Test Matrix
A representative matrix of 8 words was selected based on linguistic and orthographic complexity:

| Input | Normalized | Internal | Acoustic | Voice | Status | Notes |
|---|---|---|---|---|---|---|
| sĕkar | sĕkar | `s ə k a r` | `səkar` | `id` | PASS | |
| paḍaṅ | paḍaṅ | `p a ḍ a ŋ` | `paɖaŋ` | `id` | PASS | |
| ghaṇṭā | ghaṇṭā | `gʱ a ṇ ṭ aː` | `gʱaɳʈaː` | `id` | PASS | Provisional mapping on `gʱ` |
| śānti | śānti | `ś aː n t i` | `ʃaːnti` | `id` | PASS | |
| ṣaḍguṇa | ṣaḍguṇa | `ṣ a ḍ g u ṇ a` | `ʂaɖguɳa` | `id` | PASS | |
| kṛta | kṛta | `k r̩ t a` | `kr̩ta` | `id` | PASS | Provisional mapping on `r̩` |
| sanghyang | sanghyang | `s a n gʱ j a n g` | `san gʱjang` | `id` | BACKEND_WARNING | ASCII ambiguity forced false `gʱ` |
| sang-hyang | sang-hyang | `s a n g - h j a n g` | `sang hjang` | `id` | PASS | Clean segmentation across explicit boundary |

### Successful Cases
All tokens generated non-empty, valid WAV files (between 29KB - 44KB in size).

### Warnings
- `sanghyang` (without hyphen) forces a greedy `gʱ` cluster which is phonologically incorrect for this compound but behaves exactly as the explicit ASCII ambiguity rule currently specifies.

### Unsupported Cases
None. All mapped tokens successfully passed through the eSpeak-ng engine using the `id` voice without fatal errors.

### Provisional Acoustic Mapper Adaptations
- Voiced aspirates (`bh`, `dh`, `gh`, `jh`, `ḍh`) map to `bʱ`, `dʱ`, `gʱ`, `ɟʱ`, `ɖʱ`.
- Syllabic liquids (`ṛ`, `ḷ`) map to `r̩`, `l̩`.
- Long schwa (`ö`) maps to `əː`.

### Reproducibility Commands
To regenerate the Kawi Test Matrix:
```bash
export PYTHONPATH=.
python tests/generate_matrix.py
```

### Limitations
- The fallback `id` voice is an acoustic approximation.
- A human evaluation test is required to determine the exact audible qualities of the generated IPA strings using this fallback voice. Currently, the generated audio has been validated mechanically (file exists, size > 0, valid WAV header).
- **Explicit Statement:** eSpeak output is an engineering prototype and does not constitute evidence of historically verified Old Javanese pronunciation.