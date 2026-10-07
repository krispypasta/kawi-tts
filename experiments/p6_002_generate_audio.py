import sys
from src.acoustic.pipeline import synthesize

words = ["sĕkar", "paḍaṅ", "ghaṇṭā", "śānti", "ṣaḍguṇa", "kṛta", "sanghyang"]
espeak_exe = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

print("Generating Audio artifacts for Phase 7...")

for w in words:
    try:
        synthesize(w, profile="A", output_path=f"artifacts/validation_p6_002/{w}_A.wav", voice="id", dry_run=False, executable=espeak_exe)
        print(f"Generated Profile A for: {w}")
    except Exception as e:
        print(f"Failed Profile A for {w}: {e}")
        
    try:
        synthesize(w, profile="B", output_path=f"artifacts/validation_p6_002/{w}_B.wav", voice="id", dry_run=False, executable=espeak_exe)
        print(f"Generated Profile B for: {w}")
    except Exception as e:
        print(f"Failed Profile B for {w}: {e}")

