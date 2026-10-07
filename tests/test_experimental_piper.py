import unittest
from src.tts.experimental_piper import ExperimentalPiper
import json
import os
import pytest

class TestExperimentalPiper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model_path = "artifacts/models/id_ID-news_tts-medium.onnx"
        cls.config_path = "artifacts/models/id_ID-news_tts-medium.onnx.json"
        if not os.path.exists(cls.model_path):
            pytest.skip("Piper model artifacts not found.")
        cls.piper = ExperimentalPiper(cls.model_path, cls.config_path)

    def test_provisional_aspirate_mapping(self):
        """Ensure the backend-specific mapping from ʱ to ʰ works during ID conversion."""
        ids = self.piper.phonemes_to_ids("gʱa")
        # Ensure it didn't throw ValueError
        self.assertTrue(len(ids) > 0)
        
    def test_lossy_adaptation(self):
        """Ensure lossy adaptation correctly replaces tokens before ID conversion."""
        # ʈ, ɖ, ɳ, ʂ, ʃ, r̩ should be replaced
        direct_ids = self.piper.phonemes_to_ids("ʈɖɳʂʃr̩", lossy=False)
        lossy_ids = self.piper.phonemes_to_ids("ʈɖɳʂʃr̩", lossy=True)
        
        self.assertNotEqual(direct_ids, lossy_ids)
        
        # Test specific token equivalents
        equiv_ids = self.piper.phonemes_to_ids("tdnssrə", lossy=False)
        self.assertEqual(lossy_ids, equiv_ids)

    def test_lossy_preserves_vowel_length(self):
        """Ensure vowel length (ː) is preserved in lossy mode."""
        direct_ids = self.piper.phonemes_to_ids("aː", lossy=False)
        lossy_ids = self.piper.phonemes_to_ids("aː", lossy=True)
        self.assertEqual(direct_ids, lossy_ids)

    def test_unsupported_character_throws(self):
        """Ensure characters truly missing from the id_ID model throw an error."""
        with self.assertRaises(ValueError):
            self.piper.phonemes_to_ids("gZ") # Z is not in the phoneme_id_map
