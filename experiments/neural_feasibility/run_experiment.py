import sys
import os
import time
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from kawi_tts.acoustic.pipeline import synthesize, AmbiguousTokenError

SAMPLES = [
    ("kawi", "ordinary"),
    ("bhaṭāra", "aspirate merger"),
    ("śānti", "sibilant merger"),
    ("kāraṇa", "ṇ → n"),
    ("kṛta", "vocalic liquid"),
    ("sūrya", "vowel-length neutralization"),
    ("śānti, śānti, śānti!", "punctuation"),
    ("sang-hyang bhaṭāra sūrya", "multiword/compound structure"),
    ("sang-hyang", "resolved sang-hyang"),
    ("sanghyang", "ambiguous sanghyang failure case")
]

OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_ONNX = Path(__file__).resolve().parent / "models" / "de_DE-thorsten-high.onnx"
PIPER_BIN = Path(__file__).resolve().parent / "venv" / "Scripts" / "piper"

def run_piper(text, out_wav):
    cmd = [
        str(PIPER_BIN),
        "-m", str(MODEL_ONNX),
        "-f", str(out_wav)
    ]
    start = time.perf_counter()
    # Pass text via stdin
    result = subprocess.run(cmd, input=text.encode("utf-8"), capture_output=True)
    duration = time.perf_counter() - start
    
    if result.returncode != 0:
        print(f"Piper error: {result.stderr.decode('utf-8')}")
        return False, 0.0, result.stderr.decode("utf-8")
        
    # Naive audio length using file size (16-bit 22050Hz mono = ~44100 bytes/sec)
    # Piper outputs 22050 Hz by default for Thorsten.
    size = out_wav.stat().st_size
    audio_dur = (size - 44) / 44100 if size > 44 else 0.0
    rtf = duration / audio_dur if audio_dur > 0 else 0.0
    
    return True, rtf, result.stderr.decode("utf-8")

def main():
    print("# Kawi-TTS Neural Feasibility Experiment")
    print(f"Using Model: {MODEL_ONNX.name}\n")
    
    results = []
    
    for text, label in SAMPLES:
        print(f"--- Sample: {text} ({label}) ---")
        try:
            res = synthesize(text, strict=True, dry_run=True, create_dummy_wav=True)
            ipa = res.synthesis.phoneme_input
            print(f"Deterministic IPA: {ipa}")
            
            piper_input = f"[[{ipa}]]"
            out_wav = OUT_DIR / f"{label.replace(' ', '_').replace('→', 'to').replace('/', '_')}.wav"
            
            success, rtf, stderr = run_piper(piper_input, out_wav)
            if success:
                print(f"Synthesis SUCCESS - RTF: {rtf:.3f}")
                results.append((text, label, ipa, piper_input, "SUCCESS", rtf, stderr))
            else:
                print(f"Synthesis FAILED")
                results.append((text, label, ipa, piper_input, "FAILED", 0.0, stderr))
                
        except AmbiguousTokenError as e:
            print(f"AmbiguousTokenError (EXPECTED): {e}")
            results.append((text, label, "N/A", "N/A", "EXPECTED_FAILURE", 0.0, str(e)))
        except Exception as e:
            print(f"Unexpected Error: {e}")
            results.append((text, label, "N/A", "N/A", "ERROR", 0.0, str(e)))
        
        print()
        
if __name__ == '__main__':
    main()
