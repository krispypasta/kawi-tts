import json
import numpy as np
import onnxruntime
import soundfile as sf
from typing import List

class ExperimentalPiper:
    def __init__(self, model_path: str, config_path: str):
        self.session = onnxruntime.InferenceSession(model_path)
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.loads(f.read())
        self.phoneme_id_map = self.config["phoneme_id_map"]
        self.sample_rate = self.config["audio"]["sample_rate"]
        
    def phonemes_to_ids(self, phoneme_string: str, lossy: bool = False) -> List[int]:
        ids = []
        ids.extend(self.config["phoneme_id_map"].get("^", [0])) # BOS
        
        if lossy:
            phoneme_string = phoneme_string.replace('ʈ', 't').replace('ɖ', 'd').replace('ɳ', 'n')
            phoneme_string = phoneme_string.replace('ʂ', 's').replace('ʃ', 's')
            phoneme_string = phoneme_string.replace('r̩', 'rə')
            
        for char in phoneme_string:
            if char == ' ':
                ids.extend(self.config["phoneme_id_map"].get(" ", [0]))
                continue
            
            # PROVISIONAL MAPPING: Piper id_ID model lacks voiced aspirate hook 'ʱ' (U+02B1).
            # We map it specifically in the backend to the voiceless hook 'ʰ' (U+02B0).
            if char == 'ʱ':
                char = 'ʰ'
                
            if char not in self.phoneme_id_map:
                raise ValueError(f"Unsupported phoneme character: '{char}' (U+{ord(char):04X})")
            ids.extend(self.phoneme_id_map[char])
        ids.extend(self.config["phoneme_id_map"].get("$", [0])) # EOS
        return ids
        
    def synthesize(self, phoneme_string: str, output_path: str, lossy: bool = False, length_scale: float = 1.2):
        ids = self.phonemes_to_ids(phoneme_string, lossy=lossy)
        
        # Format for Piper VITS
        phoneme_ids = np.array([ids], dtype=np.int64)
        phoneme_ids_lengths = np.array([len(ids)], dtype=np.int64)
        scales = np.array([0.667, length_scale, 0.8], dtype=np.float32) # noise_scale, length_scale, noise_w
        
        ort_inputs = {
            "input": phoneme_ids,
            "input_lengths": phoneme_ids_lengths,
            "scales": scales
        }
        
        audio = self.session.run(None, ort_inputs)[0].squeeze()
        sf.write(output_path, audio, self.sample_rate)
