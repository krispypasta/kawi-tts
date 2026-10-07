import json
with open("artifacts/models/id_ID-news_tts-medium.onnx.json", 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
print("Keys:", list(config["phoneme_id_map"].keys()))
