import sys
sys.path.append('.')
from src.g2p.engine import g2p
from src.acoustic.mapper import AcousticMapper
from src.tts.experimental_piper import ExperimentalPiper

kawi_words = ['sĕkar', 'paḍaṅ', 'ghaṇṭā', 'śānti', 'ṣaḍguṇa', 'kṛta', 'sanghyang', 'sang-hyang']
m = AcousticMapper()
piper = ExperimentalPiper("artifacts/models/id_ID-news_tts-medium.onnx", "artifacts/models/id_ID-news_tts-medium.onnx.json")

for w in kawi_words:
    phonemes = g2p(w)[0]
    mapped = m.map_phonemes([phonemes])
    backend_string = mapped.backend_phoneme_string
    try:
        ids = piper.phonemes_to_ids(backend_string)
        print(f"Word: {w}")
        print(f"  G2P internal: {phonemes}")
        print(f"  Acoustic map: {backend_string}")
        print(f"  Piper chars:  {''.join([char if char != 'ʱ' else 'ʰ' for char in backend_string])}  (with ʱ -> ʰ mapped in Piper)")
        print(f"  Piper IDs:    {ids}")
    except Exception as e:
        print(f"Word: {w} ERROR {e}")
