"""Formal end-to-end integration test suite for the Kawi-TTS V1 pipeline.

Tests the complete contract between all architectural layers:
Raw Kawi text
  ↓ Normalization (src/normalization/normalizer.py)
  ↓ Tokenization (src/normalization/tokenizer.py)
  ↓ G2P Engine (src/g2p/engine.py)
  ↓ Acoustic Mapper (src/acoustic/mapper.py)
  ↓ eSpeak Backend (src/acoustic/espeak_backend.py)
  ↓ PipelineResult (src/acoustic/pipeline.py / src/tts)
"""

import os
import tempfile
import unittest
from unittest.mock import patch

from src.acoustic import ESpeakNotFoundError, MappingStatus
from src.normalization import TokenType
from src.tts import PipelineResult, synthesize


class TestEndToEndV1Integration(unittest.TestCase):
    """End-to-end V1 pipeline integration tests."""

    def test_end_to_end_contract_flow(self):
        """Verifies that all 5 stages execute in sequence and expose intermediate representations."""
        raw_text = "  Śrī\u00a0bhaṭāra  śānti! || \n"
        res = synthesize(raw_text, profile="A", dry_run=True)

        self.assertIsInstance(res, PipelineResult)

        # 1. Raw input contract
        self.assertEqual(res.input_text, raw_text)

        # 2. Normalization contract: NFC, whitespace collapsed, non-breaking space converted
        self.assertEqual(res.normalization.normalized_text, "Śrī bhaṭāra śānti! ||")

        # 3. Tokenization contract: lossless text preservation, boundary identification
        self.assertEqual(
            "".join(t.text for t in res.tokens),
            res.normalization.normalized_text,
        )
        self.assertEqual(res.words, ["Śrī", "bhaṭāra", "śānti"])

        # 4. G2P contract: case-insensitive phoneme parsing, greedy multigraph match
        self.assertEqual(res.g2p_phonemes[0], ["ś", "r", "iː"])
        self.assertEqual(res.g2p_phonemes[1], ["bʱ", "a", "ṭ", "aː", "r", "a"])
        self.assertEqual(res.g2p_phonemes[2], ["ś", "aː", "n", "t", "i"])

        # 5. Acoustic Mapper contract: eSpeak IPA mapping, provisional tracking, no G2P mutation
        self.assertEqual(res.acoustic_mapping.backend_phoneme_string, "ʃriː bʱaʈaːra ʃaːnti")
        self.assertEqual(len(res.acoustic_mapping.provisional_mappings), 1)
        self.assertEqual(res.acoustic_mapping.provisional_mappings[0].internal_token, "bʱ")
        self.assertEqual(
            res.acoustic_mapping.provisional_mappings[0].status,
            MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING,
        )

        # 6. Backend contract: deterministic CLI construction, dry-run safety
        self.assertTrue(res.synthesis.dry_run)
        self.assertIn("espeak-ng", res.synthesis.command[0])
        self.assertIn("[[ʃriː bʱaʈaːra ʃaːnti]]", res.synthesis.command[-1])

    def test_information_preservation_invariants(self):
        """Verifies that internal G2P representations never collapse uncertain distinctions."""
        test_pairs = [
            ("śānti", "santi"),         # ś ≠ s, ā ≠ a
            ("ṣaḍguṇa", "sadguna"),     # ṣ ≠ s, ḍ ≠ d, ṇ ≠ n
            ("bhaṭāra", "batara"),      # bh ≠ b, ṭ ≠ t, ā ≠ a
            ("dharma", "darma"),        # dh ≠ d
            ("pūjā", "puja"),           # ū ≠ u, ā ≠ a
            ("kṛta", "kita"),           # r̩ ≠ i / a
        ]

        for loan, collapsed in test_pairs:
            res_loan = synthesize(loan, profile="A", dry_run=True)
            res_col = synthesize(collapsed, profile="A", dry_run=True)

            # Internal G2P representations MUST be strictly distinct
            self.assertNotEqual(
                res_loan.g2p_phonemes,
                res_col.g2p_phonemes,
                f"Information collapsed for pair ({loan!r}, {collapsed!r})",
            )
            # Backend acoustic representations MUST also remain distinct
            self.assertNotEqual(
                res_loan.acoustic_mapping.backend_phoneme_string,
                res_col.acoustic_mapping.backend_phoneme_string,
                f"Acoustic backend collapsed distinction for pair ({loan!r}, {collapsed!r})",
            )

    def test_specific_phonemic_inequalities(self):
        """Explicitly assert non-equivalence of individual phoneme tokens."""
        res_long = synthesize("ā ī ū", profile="A", dry_run=True)
        res_short = synthesize("a i u", profile="A", dry_run=True)

        self.assertNotEqual(res_long.g2p_phonemes[0], res_short.g2p_phonemes[0])  # aː ≠ a
        self.assertNotEqual(res_long.g2p_phonemes[1], res_short.g2p_phonemes[1])  # iː ≠ i
        self.assertNotEqual(res_long.g2p_phonemes[2], res_short.g2p_phonemes[2])  # uː ≠ u

        res_sibilants = synthesize("s ś ṣ", profile="A", dry_run=True)
        self.assertNotEqual(res_sibilants.g2p_phonemes[0], res_sibilants.g2p_phonemes[1])  # s ≠ ś
        self.assertNotEqual(res_sibilants.g2p_phonemes[1], res_sibilants.g2p_phonemes[2])  # ś ≠ ṣ

        res_stops = synthesize("t ṭ d ḍ n ṇ", profile="A", dry_run=True)
        self.assertNotEqual(res_stops.g2p_phonemes[0], res_stops.g2p_phonemes[1])  # t ≠ ṭ
        self.assertNotEqual(res_stops.g2p_phonemes[2], res_stops.g2p_phonemes[3])  # d ≠ ḍ
        self.assertNotEqual(res_stops.g2p_phonemes[4], res_stops.g2p_phonemes[5])  # n ≠ ṇ

    def test_representative_source_citations_flow(self):
        """End-to-end integration of verified source-cited vocabulary across categories."""
        corpus_samples = [
            # Native vocabulary
            ("sĕkar", "səkar", 0),
            ("wukir", "wukir", 0),
            ("tumutupi", "tumutupi", 0),
            ("paḍaṅ", "paɖaŋ", 0),
            # Sanskrit loans with aspirates and length
            ("dharma", "dʱarma", 1),
            ("awighnam", "awigʱnam", 1),
            ("ghaṇṭā", "gʱaɳʈaː", 1),
            ("kṛta", "kr̩ta", 1),
            ("kḷpta", "kl̩pta", 1),
            # Reduplication and elision
            ("gilaṅ-gilaṅ", "gilaŋ gilaŋ", 0),
            ("liṅgira'n", "liŋgira n", 0),
            ("ri'ṅ", "ri ŋ", 0),
        ]

        for text, expected_ipa, expected_provisional_count in corpus_samples:
            res = synthesize(text, profile="A", dry_run=True)
            self.assertEqual(
                res.acoustic_mapping.backend_phoneme_string,
                expected_ipa,
                f"Unexpected backend IPA for {text!r}",
            )
            self.assertEqual(
                len(res.acoustic_mapping.provisional_mappings),
                expected_provisional_count,
                f"Unexpected provisional count for {text!r}",
            )

    def test_ascii_ambiguity_sanghyang_contrast(self):
        """Verifies integration behavior for ASCII sanghyang vs sang-hyang vs saṅhyaṅ."""
        # 1. Un-hyphenated ASCII: token flagged UNRESOLVED
        res_raw = synthesize("sanghyang", profile="A", dry_run=True)
        self.assertEqual(res_raw.tokens[0].token_type, TokenType.UNRESOLVED)
        self.assertTrue(res_raw.tokens[0].has_ambiguity)
        self.assertIn("ngh", res_raw.tokens[0].ambiguity_reason or "")

        # 2. Hyphenated: splits boundary, no false aspirate
        res_hyphen = synthesize("sang-hyang", profile="A", dry_run=True)
        self.assertEqual(res_hyphen.words, ["sang", "hyang"])
        self.assertEqual(res_hyphen.acoustic_mapping.backend_phoneme_string, "sang hjang")
        self.assertNotIn("gʱ", res_hyphen.acoustic_mapping.backend_phoneme_string)

        # 3. Canonical: saṅhyaṅ
        res_canon = synthesize("saṅhyaṅ", profile="A", dry_run=True)
        self.assertEqual(res_canon.words, ["saṅhyaṅ"])
        self.assertEqual(res_canon.acoustic_mapping.backend_phoneme_string, "saŋhjaŋ")
        self.assertFalse(res_canon.tokens[0].has_ambiguity)

    def test_error_handling_empty_and_whitespace(self):
        """Pipeline handles empty and whitespace-only inputs gracefully without crashing."""
        for empty_val in ["", "   ", "\t\t", "\n\r\n"]:
            res = synthesize(empty_val, profile="A", dry_run=True)
            self.assertEqual(res.words, [])
            self.assertEqual(res.g2p_phonemes, [])
            self.assertEqual(res.acoustic_mapping.backend_phoneme_string, "")
            self.assertEqual(res.synthesis.command[-1], "[[]]")

    def test_error_handling_punctuation_and_numbers(self):
        """Punctuation-only and number-only inputs produce structured non-lexical tokens."""
        res_punct = synthesize(", . ! ? ||", profile="A", dry_run=True)
        self.assertEqual(res_punct.words, [])
        self.assertEqual(res_punct.g2p_phonemes, [])
        self.assertEqual(res_punct.acoustic_mapping.backend_phoneme_string, "")

        res_num = synthesize("183.2", profile="A", dry_run=True)
        self.assertEqual(res_num.words, [])
        self.assertEqual(res_num.g2p_phonemes, [])

    def test_unsupported_characters_reported_explicitly(self):
        """Unsupported characters within words are reported in unsupported_tokens, not silenced."""
        res = synthesize("kawi-x-123", profile="A", dry_run=True)
        unsupported = res.acoustic_mapping.unsupported_tokens
        self.assertEqual(len(unsupported), 1)
        self.assertEqual(unsupported[0].internal_token, "x")
        self.assertEqual(unsupported[0].status, MappingStatus.UNSUPPORTED)
        self.assertIn("Unsupported token 'x'", unsupported[0].note or "")

    @patch('shutil.which', return_value=None)
    def test_espeak_unavailable_error_on_real_execution(self, mock_which):
        """Non-dry-run synthesis raises ESpeakNotFoundError with actionable message."""
        with self.assertRaises(ESpeakNotFoundError) as ctx:
            synthesize("om", profile="A", output_path="dummy.wav", dry_run=False)
        self.assertIn("eSpeak-ng executable not found in system PATH", str(ctx.exception))

    def test_dummy_wav_generation_workflow(self):
        """Dry-run with create_dummy_wav=True writes a valid 44-byte WAV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "integration_out.wav")
            res = synthesize(
                "om awighnam astu",
                profile="A",
                output_path=out_file,
                dry_run=True,
                create_dummy_wav=True,
            )
            self.assertTrue(res.synthesis.audio_generated)
            self.assertEqual(res.synthesis.bytes_written, 44)
            self.assertTrue(os.path.exists(out_file))
            with open(out_file, "rb") as f:
                header = f.read(4)
                self.assertEqual(header, b"RIFF")


if __name__ == "__main__":
    unittest.main()
