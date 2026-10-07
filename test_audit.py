from src.g2p.engine import g2p
from src.acoustic.mapper import AcousticMapper

kawi_words = ['sĕkar', 'paḍaṅ', 'ghaṇṭā', 'śānti', 'ṣaḍguṇa', 'kṛta', 'sanghyang', 'sang-hyang']
m = AcousticMapper()

for w in kawi_words:
    phonemes = g2p(w)[0]
    mapped = m.map_phonemes([phonemes])
    print(f"Word: {w}")
    print(f"  G2P: {phonemes}")
    print(f"  Acoustic: {mapped.backend_phoneme_string}")
