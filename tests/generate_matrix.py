import os
import shutil
from pathlib import Path
from src.acoustic.pipeline import synthesize
from src.acoustic.espeak_backend import ESpeakBackend

# 1. Check executable
executable = shutil.which("espeak-ng")
if not executable:
    executable = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

print(f"eSpeak Executable: {executable}")

# 2. Check voice
backend_jv = ESpeakBackend(executable=executable, voice="jv")
# eSpeak-ng will fail if voice doesn't exist, let's verify via subprocess
import subprocess
try:
    subprocess.run([executable, "-v", "jv", "[[a]]"], check=True, capture_output=True)
    voice = "jv"
except subprocess.CalledProcessError:
    print("Voice 'jv' failed or does not exist. Falling back to 'id'.")
    voice = "id"

test_matrix = [
    "sĕkar",
    "paḍaṅ",
    "ghaṇṭā",
    "śānti",
    "ṣaḍguṇa",
    "kṛta",
    "sanghyang",
    "sang-hyang"
]

artifacts_dir = Path("artifacts")
artifacts_dir.mkdir(exist_ok=True)

results = []

for i, word in enumerate(test_matrix):
    out_path = artifacts_dir / f"test_{i}.wav"
    res = synthesize(
        word,
        profile="A",
        output_path=str(out_path),
        voice=voice,
        dry_run=False,
        executable=executable
    )
    
    # Store result for report
    stat = out_path.stat() if out_path.exists() else None
    size = stat.st_size if stat else 0
    results.append({
        "input": res.input_text,
        "normalized": res.normalization.normalized_text,
        "internal": res.g2p_phonemes,
        "acoustic": res.acoustic_mapping.backend_phoneme_string,
        "provisional": [m.internal_token for m in res.acoustic_mapping.provisional_mappings],
        "voice": voice,
        "output_path": str(out_path),
        "size": size
    })

for r in results:
    print(f"Input: {r['input']}")
    print(f"  Normalized: {r['normalized']}")
    print(f"  Internal: {r['internal']}")
    print(f"  Acoustic: {r['acoustic']}")
    print(f"  Provisional: {bool(r['provisional'])}")
    print(f"  Output Size: {r['size']} bytes")
    print("-" * 40)
