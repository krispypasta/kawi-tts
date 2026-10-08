import sys
import os
import time
import wave
import subprocess
from pathlib import Path

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
MODEL_ONNX = Path(__file__).resolve().parent / "models" / "en_US-ljspeech-high.onnx"
PIPER_BIN = Path(__file__).resolve().parent / "venv" / "Scripts" / "piper"

def run_piper(text, out_wav):
    cmd = [
        str(PIPER_BIN),
        "-m", str(MODEL_ONNX),
        "-f", str(out_wav)
    ]
    start = time.perf_counter()
    result = subprocess.run(cmd, input=text.encode("utf-8"), capture_output=True)
    duration = time.perf_counter() - start
    
    if result.returncode != 0:
        return False, 0.0, result.stderr.decode("utf-8")
        
    try:
        with wave.open(str(out_wav), 'r') as w:
            frames = w.getnframes()
            rate = w.getframerate()
            audio_dur = frames / float(rate)
    except Exception:
        audio_dur = 0.0
        
    rtf = duration / audio_dur if audio_dur > 0 else 0.0
    return True, rtf, result.stderr.decode("utf-8")

def main():
    print("# Kawi-TTS Female Neural Feasibility Experiment")
    print(f"Using Model: {MODEL_ONNX.name}\n")
    
    for text, label in SAMPLES:
        safe_label = label.replace(' ', '_').replace('→', 'to').replace('/', '_')
        print(f"--- Sample: {text} ({label}) ---")
        try:
            res = synthesize(text, strict=True, dry_run=True, create_dummy_wav=True)
            ipa = res.synthesis.phoneme_input
            print(f"Deterministic IPA: {ipa}")
            
            piper_input = f"[[{ipa}]]"
            out_wav = OUT_DIR / f"{safe_label}.wav"
            
            success, rtf, stderr = run_piper(piper_input, out_wav)
            if success:
                print(f"Synthesis SUCCESS - RTF: {rtf:.3f}")
            else:
                print(f"Synthesis FAILED: {stderr}")
                
        except AmbiguousTokenError as e:
            print(f"AmbiguousTokenError (EXPECTED): {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        print()
        
if __name__ == '__main__':
    main()
