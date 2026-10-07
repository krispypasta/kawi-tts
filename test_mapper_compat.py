import json
from src.normalization.normalizer import Normalizer
from src.tokenization.tokenizer import Tokenizer
from src.g2p.engine import G2PEngine
from src.acoustic.mapper import AcousticMapper

json_path = "artifacts/models/id_ID-news_tts-medium.onnx.json"
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
piper_phonemes = set(config.get("phoneme_id_map", {}).keys())

n = Normalizer()
t = Tokenizer()
g = G2PEngine()
m = AcousticMapper()

kawi_words = ['sĕkar', 'paḍaṅ', 'ghaṇṭā', 'śānti', 'ṣaḍguṇa', 'kṛta', 'sanghyang', 'sang-hyang']

print("=== STAGE 3: PHONEME COMPATIBILITY (MAPPED TO BACKEND IPA) ===")
for w in kawi_words:
    norm = n.normalize(w)
    toks = t.tokenize(norm)
    phonemes = g.process(toks)
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
