"""Unit tests for the Kawi-TTS Acoustic Mapper."""

import unittest
from src.acoustic.mapper import (
    AcousticMapper,
    AcousticMappingResult,
    MappedToken,
    MappingStatus,
)


class TestAcousticMapper(unittest.TestCase):
    """Test suite for internal G2P to backend acoustic phoneme mapping."""

    def setUp(self):
        self.mapper = AcousticMapper(profile="B")

    def test_native_vowels_and_consonants_preserved(self):
        """Native vowels and consonants must be mapped with status PRESERVED."""
        native_phonemes = [["p", "a"], ["s", "ə", "k", "a", "r"]]
        res = self.mapper.map_phonemes(native_phonemes)

        self.assertEqual(res.backend_phoneme_string, "pa səkar")
        for word in res.mapped_words:
            for tok in word:
                self.assertEqual(tok.status, MappingStatus.PRESERVED)

    def test_velar_and_palatal_nasals(self):
        """ŋ and ɲ must map cleanly to standard IPA and be PRESERVED."""
        nasals = [["ŋ", "a"], ["ɲ", "a"]]
        res = self.mapper.map_phonemes(nasals)
        self.assertEqual(res.backend_phoneme_string, "ŋa ɲa")
        self.assertEqual(res.mapped_words[0][0].backend_token, "ŋ")
        self.assertEqual(res.mapped_words[0][0].status, MappingStatus.PRESERVED)
        self.assertEqual(res.mapped_words[1][0].backend_token, "ɲ")
        self.assertEqual(res.mapped_words[1][0].status, MappingStatus.PRESERVED)

    def test_retroflex_stops(self):
        """Internal ṭ and ḍ must map to IPA retroflexes ʈ and ɖ with PRESERVED status."""
        retroflexes = [["ʈ", "a"], ["ɖ", "a"]]  # wait, internal tokens from G2P are "ṭ", "ḍ"
        retroflexes_internal = [["ṭ", "a"], ["ḍ", "a"]]
        res = self.mapper.map_phonemes(retroflexes_internal)
        self.assertEqual(res.backend_phoneme_string, "ʈa ɖa")
        self.assertEqual(res.mapped_words[0][0].backend_token, "ʈ")
        self.assertEqual(res.mapped_words[0][0].status, MappingStatus.PRESERVED)
        self.assertEqual(res.mapped_words[1][0].backend_token, "ɖ")
        self.assertEqual(res.mapped_words[1][0].status, MappingStatus.PRESERVED)

    def test_long_vowels(self):
        """Vowel length (ā, ī, ū -> aː, iː, uː) must preserve the IPA length mark."""
        long_vowels = [["aː"], ["iː"], ["uː"]]
        res = self.mapper.map_phonemes(long_vowels)
        self.assertEqual(res.backend_phoneme_string, "aː iː uː")
        for word in res.mapped_words:
            self.assertEqual(word[0].status, MappingStatus.PRESERVED)
            self.assertIn("ː", word[0].backend_token)

    def test_sibilants_mapped_distinctly(self):
        """Internal sibilants (s, ś, ṣ) must map to distinct IPA fricatives (s, ʃ, ʂ)."""
        sibilants = [["s", "a"], ["ś", "a"], ["ṣ", "a"]]
        res = self.mapper.map_phonemes(sibilants)
        self.assertEqual(res.backend_phoneme_string, "sa ʃa ʂa")
        self.assertEqual(res.mapped_words[0][0].backend_token, "s")
        self.assertEqual(res.mapped_words[1][0].backend_token, "ʃ")
        self.assertEqual(res.mapped_words[2][0].backend_token, "ʂ")
        for word in res.mapped_words:
            self.assertEqual(word[0].status, MappingStatus.PRESERVED)

    def test_aspirates_labeled_provisional(self):
        """Voiced aspirates must be explicitly stamped PROVISIONAL_ACOUSTIC_MAPPING."""
        voiced_aspirates = [["bʱ", "a"], ["dʱ", "a"], ["gʱ", "a"]]
        res = self.mapper.map_phonemes(voiced_aspirates)
        self.assertEqual(len(res.provisional_mappings), 3)
        for tok in res.provisional_mappings:
            self.assertEqual(tok.status, MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING)
            self.assertIsNotNone(tok.note)
            assert tok.note is not None
            self.assertIn("PROVISIONAL_ACOUSTIC_MAPPING", tok.note)

    def test_vocalic_liquids_labeled_provisional(self):
        """Syllabic liquids (r̩, l̩) must be explicitly stamped PROVISIONAL_ACOUSTIC_MAPPING."""
        liquids = [["k", "r̩", "t", "a"]]
        res = self.mapper.map_phonemes(liquids)
        r_tok = res.mapped_words[0][1]
        self.assertEqual(r_tok.internal_token, "r̩")
        self.assertEqual(r_tok.status, MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING)
        self.assertIsNotNone(r_tok.note)
        assert r_tok.note is not None
        self.assertIn("PROVISIONAL_ACOUSTIC_MAPPING", r_tok.note)

    def test_unsupported_tokens_handled_safely(self):
        """Unrecognized tokens must be marked UNSUPPORTED and reported, not silently erased."""
        unsupported = [["x", "a", "@"]]
        res = self.mapper.map_phonemes(unsupported)
        unsupported_tokens = res.unsupported_tokens
        self.assertEqual(len(unsupported_tokens), 2)
        self.assertEqual(unsupported_tokens[0].internal_token, "x")
        self.assertEqual(unsupported_tokens[0].status, MappingStatus.UNSUPPORTED)
        self.assertEqual(unsupported_tokens[1].internal_token, "@")
        self.assertEqual(unsupported_tokens[1].status, MappingStatus.UNSUPPORTED)

    def test_immutability_of_input_phonemes(self):
        """AcousticMapper must NOT mutate the original list of G2P phonemes."""
        input_phonemes = [["bʱ", "a", "ṭ", "aː", "r", "a"]]
        input_copy = [list(word) for word in input_phonemes]

        res = self.mapper.map_phonemes(input_phonemes)

        # Ensure input list was not modified
        self.assertEqual(input_phonemes, input_copy)
        self.assertEqual(res.original_phonemes, input_copy)


if __name__ == "__main__":
    unittest.main()
