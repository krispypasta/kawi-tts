import os
from src.g2p.engine import g2p
from src.acoustic.mapper import AcousticMapper
from src.tts.experimental_piper import ExperimentalPiper

# Check model exists
model_path = "artifacts/models/id_ID-news_tts-medium.onnx"
config_path = "artifacts/models/id_ID-news_tts-medium.onnx.json"
out_dir = "artifacts/piper_prototype"
lossy_dir = "artifacts/piper_lossy_prototype"
os.makedirs(out_dir, exist_ok=True)
os.makedirs(lossy_dir, exist_ok=True)

piper = ExperimentalPiper(model_path, config_path)
m = AcousticMapper()

kawi_words = ['sĕkar', 'paḍaṅ', 'ghaṇṭā', 'śānti', 'ṣaḍguṇa', 'kṛta', 'sanghyang', 'sang-hyang']

print("=== STAGE 4: DIRECT PHONEME PROTOTYPE ===")

for i, w in enumerate(kawi_words):
    print(f"\nWord: {w}")
    try:
        phonemes = g2p(w)[0]
        mapped = m.map_phonemes([phonemes])
        backend_string = mapped.backend_phoneme_string
        
        print(f"  G2P: {phonemes}")
        print(f"  Acoustic (Direct): {backend_string}")
        
        # Direct Injection
        out_wav = os.path.join(out_dir, f"neural_test_{i}.wav")
        piper.synthesize(backend_string, out_wav, lossy=False, length_scale=1.2)
        
        # Lossy Adaptation
        out_wav_lossy = os.path.join(lossy_dir, f"neural_test_lossy_{i}.wav")
        piper.synthesize(backend_string, out_wav_lossy, lossy=True, length_scale=1.2)
        print(f"  Result Direct: SUCCESS -> {out_wav}")
        print(f"  Result Lossy: SUCCESS -> {out_wav_lossy}")
    except ValueError as e:
        print(f"  Result: FAILURE -> {e}")
    except Exception as e:
        print(f"  Result: ERROR -> {e}")
