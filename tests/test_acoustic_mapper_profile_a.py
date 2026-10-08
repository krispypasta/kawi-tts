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

    def test_profile_a_all_aspirates_merged(self):
        """All Sanskrit aspirates must be merged to plain stops per evidence."""
        res = self.mapper.map_phonemes([["kʰ"], ["gʱ"], ["cʰ"], ["ɟʱ"], ["tʰ"], ["dʱ"], ["ṭʰ"], ["ḍʱ"], ["pʰ"], ["bʱ"]])
        self.assertEqual(res.backend_phoneme_string, "k g c ɟ t d ʈ ɖ p b")
        for i, internal in enumerate(["kʰ", "gʱ", "cʰ", "ɟʱ", "tʰ", "dʱ", "ṭʰ", "ḍʱ", "pʰ", "bʱ"]):
            tok = res.mapped_words[i][0]
            self.assertEqual(tok.internal_token, internal)
            self.assertEqual(tok.status, MappingStatus.EVIDENCE_BACKED)
            self.assertEqual(tok.note, "P5-002 / aspirate merger")

    def test_profile_a_retroflex_nasal(self):
        """Retroflex nasal must be merged to n per evidence."""
        res = self.mapper.map_phonemes([["ṇ", "a"]])
        self.assertEqual(res.backend_phoneme_string, "na")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "ṇ")
        self.assertEqual(tok.backend_token, "n")
        self.assertEqual(tok.status, MappingStatus.EVIDENCE_BACKED)
        self.assertEqual(tok.note, "P5-002 / retroflex nasal merger")
        
    def test_profile_a_long_vocalic_liquids_handled(self):
        """Long vocalic liquids adapt to schwa base and lose duration."""
        res = self.mapper.map_phonemes([["r̩ː", "a"]])
        self.assertEqual(res.backend_phoneme_string, "rəa")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "r̩ː")
        self.assertEqual(tok.backend_token, "rə")
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
