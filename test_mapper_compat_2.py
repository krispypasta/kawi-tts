import json
from src.g2p.engine import g2p
from src.acoustic.mapper import AcousticMapper

json_path = "artifacts/models/id_ID-news_tts-medium.onnx.json"
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
piper_phonemes = set(config.get("phoneme_id_map", {}).keys())

m = AcousticMapper()

kawi_words = ['sĕkar', 'paḍaṅ', 'ghaṇṭā', 'śānti', 'ṣaḍguṇa', 'kṛta', 'sanghyang', 'sang-hyang']

print("=== STAGE 3: PHONEME COMPATIBILITY (MAPPED TO BACKEND IPA) ===")
for w in kawi_words:
    phonemes = g2p(w)[0]
    mapped = m.map_phonemes([phonemes])
    backend_string = mapped.backend_phoneme_string
    
    unsupported = []
    for c in backend_string:
        if c not in piper_phonemes and c != ' ':
            unsupported.append(c)
            
    print(f"\nWord: {w}")
    print(f"Backend IPA: {backend_string}")
    if unsupported:
        print(f"UNSUPPORTED CHARS: {unsupported}")
    else:
        print("FULLY SUPPORTED!")
