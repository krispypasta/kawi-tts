import unittest
from kawi_tts.acoustic.mapper import AcousticMapper, MappingStatus

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

    def test_profile_a_unsupported_aspirates_fall_through(self):
        """Unsupported aspirates must NOT be merged without cited evidence."""
        res = self.mapper.map_phonemes([["kʰ", "a"]])
        self.assertEqual(res.backend_phoneme_string, "kʰa")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "kʰ")
        self.assertEqual(tok.backend_token, "kʰ")
        # kʰ is originally a V1 Preserved token since it wasn't merged.
        self.assertEqual(tok.status, MappingStatus.PRESERVED)
        
    def test_profile_a_long_vocalic_liquids_handled(self):
        """Long vocalic liquids must keep their duration but adapt to schwa base."""
        res = self.mapper.map_phonemes([["r̩ː", "a"]])
        self.assertEqual(res.backend_phoneme_string, "rəːa")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "r̩ː")
        self.assertEqual(tok.backend_token, "rəː")
        self.assertEqual(tok.status, MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING)

    def test_vowel_length_unresolved(self):
        res = self.mapper.map_phonemes([["aː"]])
        self.assertEqual(res.backend_phoneme_string, "a")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "aː")
        self.assertEqual(tok.backend_token, "a")
        self.assertEqual(tok.status, MappingStatus.UNRESOLVED)
        self.assertEqual(tok.note, "P6-003R / unresolved duration engineering fallback")

if __name__ == "__main__":
    unittest.main()
