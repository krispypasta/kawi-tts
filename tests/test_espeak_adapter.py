import unittest

from kawi_tts.acoustic.mapper import AcousticMapper, MappingStatus


class TestESpeakAdapter(unittest.TestCase):
    def test_espeak_id_adapter_active(self):
        """Adapter correctly swaps unsupported IPA for eSpeak 'id' voice mnemonics."""
        mapper = AcousticMapper(profile="B", adapt_for_espeak_id=True)
        
        # Retroflex ʈ -> t
        res1 = mapper.map_phonemes([["bʱ", "a", "ʈ", "aː", "r", "a"]])
        self.assertEqual(res1.backend_phoneme_string, "bhatara")
        
        # Verify status tags
        bha = res1.mapped_words[0][0]
        self.assertEqual(bha.backend_token, "bh")
        self.assertEqual(bha.status, MappingStatus.BACKEND_APPROXIMATION)
        self.assertEqual(bha.note, "eSpeak 'id' fallback approximation")

        ta = res1.mapped_words[0][2]
        self.assertEqual(ta.backend_token, "t")
        self.assertEqual(ta.status, MappingStatus.BACKEND_APPROXIMATION)

    def test_espeak_id_adapter_inactive(self):
        """Adapter leaves standard IPA intact when not targeting 'id' voice."""
        mapper = AcousticMapper(profile="B", adapt_for_espeak_id=False)
        
        res = mapper.map_phonemes([["bʱ", "a", "ʈ", "aː", "r", "a"]])
        self.assertEqual(res.backend_phoneme_string, "bʱaʈaːra")
        
        bha = res.mapped_words[0][0]
        self.assertEqual(bha.backend_token, "bʱ")
        self.assertEqual(bha.status, MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING)

    def test_espeak_native_ascii_mnemonics(self):
        """Adapter converts special phonemes to eSpeak ascii mappings."""
        mapper = AcousticMapper(profile="B", adapt_for_espeak_id=True)
        
        res = mapper.map_phonemes([["ŋ", "ə", "ɟ", "a"]])
        # ŋ -> N, ə -> @, ɟ -> dZ
        self.assertEqual(res.backend_phoneme_string, "N@dZa")


if __name__ == "__main__":
    unittest.main()
