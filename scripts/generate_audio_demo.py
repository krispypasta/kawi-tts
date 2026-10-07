import os
import json
import traceback
from kawi_tts.acoustic.pipeline import synthesize
from kawi_tts.normalization.tokenizer import extract_words
from kawi_tts.acoustic.espeak_backend import ESpeakNotFoundError

OUT_DIR = "artifacts/pre_release_audio_demo"
ESPEAK_EXE = "C:/Program Files/eSpeak NG/espeak-ng.exe"

inputs = [
    "sĕkar",
    "BHAṬĀRA",
    "śānti",
    "kṝta",
    "sankha",
    "sang-hyang",
    "sanghyang"
]

manifest = []

def generate(text, profile):
    base_name = text.replace("ĕ", "e").replace("Ṭ", "T").replace("Ā", "A").replace("ś", "s").replace("ā", "a").replace("ṝ", "r").replace("-", "_")
    output_wav = os.path.join(OUT_DIR, f"{base_name}_{profile}.wav")
    
    try:
        res = synthesize(
            text,
            profile=profile,
            output_path=output_wav,
            dry_run=False,
            create_dummy_wav=False,
            executable=ESPEAK_EXE
        )
        
        # Check if tokenizer blocked it
        ambiguous = any(t.has_ambiguity for t in res.tokens)
        if ambiguous:
            reason = next((t.ambiguity_reason for t in res.tokens if t.has_ambiguity), "Unknown")
            manifest.append({
                "input": text,
                "profile": profile,
                "status": "EXPECTED BLOCKED",
                "reason": reason,
                "wav_path": None
            })
            return
            
        canonical = " | ".join("-".join(p.canonical_token for p in w) for w in res.acoustic_mapping.profile_canonical)
        target = " | ".join("-".join(p.target_token for p in w) for w in res.acoustic_mapping.profile_canonical)
        espeak_str = res.acoustic_mapping.backend_phoneme_string
        
        manifest.append({
            "input": text,
            "profile": profile,
            "normalized": res.normalized_text,
            "canonical": canonical,
            "target": target,
            "espeak_string": espeak_str,
            "status": "SUCCESS",
            "wav_path": output_wav
        })
    except Exception as e:
        manifest.append({
            "input": text,
            "profile": profile,
            "status": "ERROR",
            "reason": str(e),
            "wav_path": None
        })

for t in inputs:
    generate(t, "A")
    generate(t, "B")

with open(os.path.join(OUT_DIR, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("Demo generation complete.")
