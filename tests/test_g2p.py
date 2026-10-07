"""Unit tests for Old Javanese G2P engine."""

import unittest
from src.g2p import g2p, g2p_word


class TestG2P(unittest.TestCase):
    """Test suite for the lossless G2P engine."""

    def test_native_words(self):
        """Native words should parse directly to core phonemes."""
        self.assertEqual(
            g2p_word("sĕkar"),
            ["s", "ə", "k", "a", "r"]
        )
        self.assertEqual(
            g2p_word("tangi"),
            ["t", "a", "n", "g", "i"]  # Note: ASCII 'ng' parses as 'n','g'
        )
        self.assertEqual(
            g2p_word("taṅi"),
            ["t", "a", "ŋ", "i"]       # Normalized 'ṅ' parses as 'ŋ'
        )

    def test_retroflex_stops(self):
        """Retroflex stops ṭ and ḍ must be preserved."""
        self.assertEqual(
            g2p_word("ḍaṅ"),
            ["ḍ", "a", "ŋ"]
        )
        self.assertEqual(
            g2p_word("bhaṭāra"),
            ["bʱ", "a", "ṭ", "aː", "r", "a"]
        )

    def test_sanskrit_aspirates(self):
        """Sanskrit aspirates must parse as single phonemes, not stop + h."""
        self.assertEqual(
            g2p_word("dharmma"),
            ["dʱ", "a", "r", "m", "m", "a"]
        )
        self.assertEqual(
            g2p_word("phala"),
            ["pʰ", "a", "l", "a"]
        )
        # Verify greedy matching over individual letters
        self.assertNotIn("h", g2p_word("dharmma"))
        self.assertIn("dʱ", g2p_word("dharmma"))

    def test_sibilants(self):
        """ś, ṣ, and s must parse distinctly."""
        self.assertEqual(
            g2p_word("śānti"),
            ["ś", "aː", "n", "t", "i"]
        )
        self.assertEqual(
            g2p_word("ṣaḍguṇa"),
            ["ṣ", "a", "ḍ", "g", "u", "ṇ", "a"]
        )

    def test_vowel_length(self):
        """Long vowels must parse to their long representations."""
        self.assertEqual(
            g2p_word("rāmāyaṇa"),
            ["r", "aː", "m", "aː", "j", "a", "ṇ", "a"]
        )
        self.assertEqual(
            g2p_word("pūjā"),
            ["p", "uː", "ɟ", "aː"]
        )

    def test_vocalic_liquids(self):
        """Vocalic liquids must parse distinctly."""
        self.assertEqual(
            g2p_word("kṛta"),
            ["k", "r̩", "t", "a"]
        )

    def test_sentence_parsing(self):
        """Multiple words should parse to a list of lists."""
        text = "om awighnam astu"
        phonemes = g2p(text)
        self.assertEqual(len(phonemes), 3)
        self.assertEqual(phonemes[0], ["o", "m"])
        self.assertEqual(phonemes[1], ["a", "w", "i", "gʱ", "n", "a", "m"])
        self.assertEqual(phonemes[2], ["a", "s", "t", "u"])

    def test_unknown_characters_preserved(self):
        """Punctuation and unknown characters should pass through."""
        self.assertEqual(
            g2p_word("sĕkar,"),
            ["s", "ə", "k", "a", "r", ","]
        )
        self.assertEqual(
            g2p_word("123"),
            ["1", "2", "3"]
        )


if __name__ == "__main__":
    unittest.main()
