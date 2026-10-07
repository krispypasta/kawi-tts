import json

with open("artifacts/models/id_ID-news_tts-medium.onnx.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())
    
multi = [k for k in config["phoneme_id_map"].keys() if len(k) > 1]
print("Multi-char keys in phoneme_id_map:", multi)
