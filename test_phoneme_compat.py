import json
from src.g2p.engine import g2p

# Load Piper vocabulary
json_path = "artifacts/models/id_ID-news_tts-medium.onnx.json"
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
piper_phonemes = set(config.get("phoneme_id_map", {}).keys())

kawi_words = ['sĕkar', 'paḍaṅ', 'ghaṇṭā', 'śānti', 'ṣaḍguṇa', 'kṛta', 'sanghyang', 'sang-hyang']

print("=== STAGE 3: PHONEME COMPATIBILITY ===")
for w in kawi_words:
    phonemes = g2p(w)[0]
    supported = []
    unsupported = []
    
    # We must flatten the phonemes into characters to check against Piper,
    # because Piper maps single characters, not clusters like 'aː' or 'gʱ'
    for p in phonemes:
        # Check if every character in the phoneme string is in piper_phonemes
        failed_chars = [c for c in p if c not in piper_phonemes]
        if failed_chars:
            unsupported.append((p, failed_chars))
        else:
            supported.append(p)
            
    print(f"\nWord: {w}")
    print(f"G2P: {phonemes}")
    print(f"Supported: {supported}")
    if unsupported:
        print(f"UNSUPPORTED: {unsupported}")
