"""Unit tests for the end-to-end Kawi-TTS synthesis pipeline and eSpeak backend."""

import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from src.acoustic.espeak_backend import (
    ESpeakBackend,
    ESpeakNotFoundError,
    SynthesisResult,
    create_minimal_wav_header,
)
from src.acoustic.mapper import MappingStatus
from src.acoustic.pipeline import PipelineResult, synthesize


class TestSynthesisPipeline(unittest.TestCase):
    """Test suite for the end-to-end Kawi-TTS synthesis pipeline and backend."""

    @patch('shutil.which', return_value=None)
    def test_espeak_backend_availability_and_dry_run(self, mock_which):
        """Backend must support dry_run without requiring eSpeak installed."""
        backend = ESpeakBackend()
        # On this environment, eSpeak is not installed
        self.assertFalse(backend.is_available)

        # Attempting non-dry-run synthesis without eSpeak must raise ESpeakNotFoundError
        with self.assertRaises(ESpeakNotFoundError):
            backend.synthesize("om awigʱnam astu", output_path="dummy.wav", dry_run=False)

        # Dry-run synthesis must succeed without error
        res = backend.synthesize("om awigʱnam astu", output_path="dummy.wav", dry_run=True)
        self.assertTrue(res.dry_run)
        self.assertFalse(res.audio_generated)
        self.assertEqual(res.phoneme_input, "om awigʱnam astu")
        self.assertIn("espeak-ng", res.command[0])
        self.assertIn("[[om awigʱnam astu]]", res.command[-1])

    def test_dry_run_dummy_wav_generation(self):
        """Backend in dry_run mode with create_dummy_wav=True must produce a valid 44-byte WAV."""
        backend = ESpeakBackend()
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, "test.wav")
            res = backend.synthesize(
                "om",
                output_path=wav_path,
                dry_run=True,
                create_dummy_wav=True,
            )
            self.assertTrue(res.audio_generated)
            self.assertTrue(os.path.exists(wav_path))
            self.assertEqual(os.path.getsize(wav_path), 44)
            with open(wav_path, "rb") as f:
                header = f.read(4)
                self.assertEqual(header, b"RIFF")

    def test_end_to_end_synthesis_pipeline_structure(self):
        """Full pipeline must execute all 5 stages in order and preserve all data."""
        text = "om awighnam astu"
        res = synthesize(text, profile="B", dry_run=True)

        self.assertIsInstance(res, PipelineResult)
        self.assertEqual(res.input_text, text)
        self.assertEqual(res.normalization.normalized_text, "om awighnam astu")
        self.assertEqual(len(res.tokens), 5)  # om + space + awighnam + space + astu
        self.assertEqual(res.words, ["om", "awighnam", "astu"])

        # Check G2P phonemes
        self.assertEqual(res.g2p_phonemes[0], ["o", "m"])
        self.assertEqual(res.g2p_phonemes[1], ["a", "w", "i", "gʱ", "n", "a", "m"])
        self.assertEqual(res.g2p_phonemes[2], ["a", "s", "t", "u"])

        # Check Acoustic Mapper
        self.assertEqual(res.acoustic_mapping.backend_phoneme_string, "om awigʱnam astu")
        self.assertEqual(len(res.acoustic_mapping.provisional_mappings), 1)
        self.assertEqual(res.acoustic_mapping.provisional_mappings[0].internal_token, "gʱ")
        self.assertEqual(
            res.acoustic_mapping.provisional_mappings[0].status,
            MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING,
        )

        # Check Synthesis backend
        self.assertTrue(res.synthesis.dry_run)
        self.assertIn("[[om awigʱnam astu]]", res.synthesis.command[-1])

    def test_explicit_boundary_preservation(self):
        """Pipeline must preserve explicit boundaries (sang-hyang) without false aspirates."""
        text = "sang-hyang"
        res = synthesize(text, profile="B", dry_run=True)

        self.assertEqual(res.words, ["sang", "hyang"])
        self.assertEqual(res.g2p_phonemes[0], ["s", "a", "n", "g"])
        self.assertEqual(res.g2p_phonemes[1], ["h", "j", "a", "n", "g"])
        # No 'gʱ' aspirate should be created
        self.assertEqual(res.acoustic_mapping.backend_phoneme_string, "sang hjang")
        self.assertEqual(len(res.acoustic_mapping.provisional_mappings), 0)

    def test_sanskrit_loans_with_aspirates_and_long_vowels(self):
        """Pipeline must handle complex Sanskrit loans (bhaṭāra, śānti) cleanly."""
        text = "bhaṭāra śānti"
        res = synthesize(text, profile="B", dry_run=True)

        self.assertEqual(res.words, ["bhaṭāra", "śānti"])
        # G2P output
        self.assertEqual(res.g2p_phonemes[0], ["bʱ", "a", "ṭ", "aː", "r", "a"])
        self.assertEqual(res.g2p_phonemes[1], ["ś", "aː", "n", "t", "i"])

        # Acoustic Mapper output
        self.assertEqual(res.acoustic_mapping.backend_phoneme_string, "bʱaʈaːra ʃaːnti")
        self.assertEqual(len(res.acoustic_mapping.provisional_mappings), 1)  # bʱ
        self.assertEqual(res.acoustic_mapping.provisional_mappings[0].internal_token, "bʱ")


if __name__ == "__main__":
    unittest.main()
