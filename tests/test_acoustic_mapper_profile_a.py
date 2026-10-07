import unittest
from src.acoustic.mapper import AcousticMapper, MappingStatus

class TestAcousticMapperProfileA(unittest.TestCase):
    def setUp(self):
        self.mapper = AcousticMapper(profile="A")

    def test_profile_a_mapping(self):
        # Aspirates mapped to plain stops and then formatted
        res = self.mapper.map_phonemes([["bʱ", "a"], ["dʱ", "a"]])
        self.assertEqual(res.backend_phoneme_string, "ba da")
        # Check mapping status and note
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "bʱ")
        self.assertEqual(tok.backend_token, "b")
        self.assertEqual(tok.status, MappingStatus.EVIDENCE_BACKED)
        self.assertEqual(tok.note, "P5-002 / aspirate merger")
        
    def test_profile_a_sibilants(self):
        # Sibilants mapped to 's'
        res = self.mapper.map_phonemes([["s", "a"], ["ś", "a"], ["ṣ", "a"]])
        self.assertEqual(res.backend_phoneme_string, "sa sa sa")
        tok = res.mapped_words[1][0] # ś
        self.assertEqual(tok.internal_token, "ś")
        self.assertEqual(tok.backend_token, "s")
        self.assertEqual(tok.status, MappingStatus.EVIDENCE_BACKED)
        
    def test_profile_a_liquids(self):
        res = self.mapper.map_phonemes([["r̩", "a"]])
        self.assertEqual(res.backend_phoneme_string, "rəa")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.backend_token, "rə")
        self.assertEqual(tok.status, MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING)

if __name__ == "__main__":
    unittest.main()
