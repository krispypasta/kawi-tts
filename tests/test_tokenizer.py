"""Unit tests for the Old Javanese text-structure and tokenization layer."""

import unittest
from kawi_tts.normalization import (
    Token,
    TokenType,
    extract_words,
    get_ambiguities,
    normalize_text,
    tokenize,
)
from kawi_tts.g2p import g2p_word


class TestTokenizer(unittest.TestCase):
    """Test suite for the deterministic text-structure / tokenization layer."""

    def test_empty_and_blank_input(self):
        """Empty input should yield empty token list."""
        self.assertEqual(tokenize(""), [])

    def test_ordinary_words_and_whitespace(self):
        """Tokens must classify simple lexical words and whitespace without alterations."""
        text = "om awighnam astu"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].token_type, TokenType.WORD)
        self.assertEqual(tokens[0].text, "om")
        self.assertEqual(tokens[1].token_type, TokenType.WHITESPACE)
        self.assertEqual(tokens[1].text, " ")
        self.assertEqual(tokens[2].token_type, TokenType.WORD)
        self.assertEqual(tokens[2].text, "awighnam")
        self.assertEqual(tokens[3].token_type, TokenType.WHITESPACE)
        self.assertEqual(tokens[3].text, " ")
        self.assertEqual(tokens[4].token_type, TokenType.WORD)
        self.assertEqual(tokens[4].text, "astu")

    def test_punctuation_and_verse_dandas(self):
        """Punctuation marks and Indic dandas must be classified as TokenType.PUNCTUATION."""
        text = "bhaṭāra, || 183.2d"
        tokens = tokenize(text)
        types = [t.token_type for t in tokens]
        texts = [t.text for t in tokens]
        self.assertIn(TokenType.PUNCTUATION, types)
        self.assertEqual(texts[1], ",")
        self.assertEqual(texts[3], "||")
        self.assertEqual(texts[5], "183")
        self.assertEqual(types[5], TokenType.NUMBER)
        self.assertEqual(texts[6], ".")
        self.assertEqual(types[6], TokenType.PUNCTUATION)

    def test_line_breaks(self):
        """Newlines must be classified as TokenType.NEWLINE."""
        text = "pāda 1\npāda 2\r\npāda 3"
        tokens = tokenize(text)
        newlines = [t for t in tokens if t.token_type == TokenType.NEWLINE]
        self.assertEqual(len(newlines), 2)
        self.assertEqual(newlines[0].text, "\n")
        self.assertEqual(newlines[1].text, "\r\n")

    def test_explicit_boundaries_hyphens(self):
        """Explicit boundary markers (hyphens) must be classified as TokenType.BOUNDARY."""
        text = "gilaṅ-gilaṅ"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].text, "gilaṅ")
        self.assertEqual(tokens[0].token_type, TokenType.WORD)
        self.assertEqual(tokens[1].text, "-")
        self.assertEqual(tokens[1].token_type, TokenType.BOUNDARY)
        self.assertEqual(tokens[2].text, "gilaṅ")
        self.assertEqual(tokens[2].token_type, TokenType.WORD)

    def test_elision_and_apostrophes(self):
        """Apostrophes marking sandhi or enclitics must be classified as TokenType.ELISION."""
        text = "lingira'n"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].text, "lingira")
        self.assertEqual(tokens[0].token_type, TokenType.WORD)
        self.assertEqual(tokens[1].text, "'")
        self.assertEqual(tokens[1].token_type, TokenType.ELISION)
        self.assertEqual(tokens[2].text, "n")
        self.assertEqual(tokens[2].token_type, TokenType.WORD)

    def test_ascii_ng_and_canonical_n_dot(self):
        """ASCII 'ng' and canonical 'ṅ' must both be preserved verbatim without mutation."""
        text_ascii = "sang hyang"
        tokens_ascii = tokenize(text_ascii)
        words_ascii = extract_words(tokens_ascii)
        self.assertEqual(words_ascii, ["sang", "hyang"])
        self.assertFalse(tokens_ascii[0].has_ambiguity)

        text_canonical = "saṅ hyaṅ"
        tokens_canonical = tokenize(text_canonical)
        words_canonical = extract_words(tokens_canonical)
        self.assertEqual(words_canonical, ["saṅ", "hyaṅ"])
        self.assertFalse(tokens_canonical[0].has_ambiguity)

    def test_ascii_ny_and_canonical_n_tilde(self):
        """ASCII 'ny' and canonical 'ñ' must both be preserved verbatim."""
        text_ascii = "kanya"
        tokens_ascii = tokenize(text_ascii)
        self.assertEqual(extract_words(tokens_ascii), ["kanya"])

        text_canonical = "kaña"
        tokens_canonical = tokenize(text_canonical)
        self.assertEqual(extract_words(tokens_canonical), ["kaña"])

    def test_aspirate_looking_sequences(self):
        """Standard Sanskrit aspirates must be classified as normal words, not ambiguous."""
        text = "dharma bhaṭāra phala chanda"
        tokens = tokenize(text)
        words = extract_words(tokens)
        self.assertEqual(words, ["dharma", "bhaṭāra", "phala", "chanda"])
        for t in tokens:
            if t.token_type == TokenType.WORD:
                self.assertFalse(t.has_ambiguity)

    def test_sanghyang_unresolved_case(self):
        """Unhyphenated ASCII 'sanghyang' must be flagged as TokenType.UNRESOLVED."""
        text = "sanghyang"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 1)
        token = tokens[0]
        self.assertEqual(token.token_type, TokenType.UNRESOLVED)
        self.assertTrue(token.has_ambiguity)
        self.assertIsNotNone(token.ambiguity_reason)
        assert token.ambiguity_reason is not None
        self.assertIn("ngh", token.ambiguity_reason)

        ambiguities = get_ambiguities(tokens)
        self.assertEqual(len(ambiguities), 1)
        self.assertEqual(ambiguities[0].text, "sanghyang")

    def test_sankha_no_false_alarm(self):
        """'nkh' sequences (like sankha) must not trigger an ambiguity warning.
        'nk' is not an ASCII digraph for the velar nasal, so 'sankha' (saṅkha)
        is unambiguously n + kʰ.
        """
        text = "sankha"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, TokenType.WORD)
        self.assertFalse(tokens[0].has_ambiguity)

    def test_sang_hyang_with_explicit_boundary(self):
        """Explicit boundary 'sang-hyang' cleanly splits the cluster, resolving ambiguity."""
        text = "sang-hyang"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].text, "sang")
        self.assertEqual(tokens[0].token_type, TokenType.WORD)
        self.assertFalse(tokens[0].has_ambiguity)
        self.assertEqual(tokens[1].text, "-")
        self.assertEqual(tokens[1].token_type, TokenType.BOUNDARY)
        self.assertEqual(tokens[2].text, "hyang")
        self.assertEqual(tokens[2].token_type, TokenType.WORD)
        self.assertFalse(tokens[2].has_ambiguity)

        # G2P integration test: verify that passing hyphenated words prevents false 'gh'
        words = extract_words(tokens)
        self.assertEqual(words, ["sang", "hyang"])
        phonemes_sang = g2p_word(words[0])
        phonemes_hyang = g2p_word(words[1])
        self.assertEqual(phonemes_sang, ["s", "a", "n", "g"])
        self.assertEqual(phonemes_hyang, ["h", "j", "a", "n", "g"])
        # Notice: neither list contains 'gʱ' (aspirate)!
        self.assertNotIn("gʱ", phonemes_sang)
        self.assertNotIn("gʱ", phonemes_hyang)

    def test_saṅhyaṅ_canonical_no_ambiguity(self):
        """Canonical orthography 'saṅhyaṅ' contains no 'ngh' cluster, so no ambiguity."""
        text = "saṅhyaṅ"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, TokenType.WORD)
        self.assertFalse(tokens[0].has_ambiguity)
        self.assertEqual(g2p_word(tokens[0].text), ["s", "a", "ŋ", "h", "j", "a", "ŋ"])

    def test_lossless_round_trip(self):
        """Reconstructing text by joining all tokens must equal the source string 100%."""
        samples = [
            "om awighnam astu",
            "saṅhyaṅ kamahāyānikan",
            "sanghyang guru",
            "sang-hyang guru",
            "lingira'n panĕmbah ri'ng bhaṭāra",
            "1. Śrī mahārāja (kakawin, canto II, v. 3) ||\n",
            "  mixed   spaces\tand\tnewlines\r\n",
            "gilaṅ-gilaṅ\n\n\n",
        ]
        for sample in samples:
            tokens = tokenize(sample)
            reconstructed = "".join(t.text for t in tokens)
            self.assertEqual(reconstructed, sample, f"Lossless round-trip failed for {sample!r}")

    def test_offset_consistency(self):
        """Every token's start and end offsets must match its slice in source text."""
        sample = "Śrī 183.2d: 'hantusakĕn-âmuruk' ||\n"
        tokens = tokenize(sample)
        for t in tokens:
            self.assertEqual(sample[t.start:t.end], t.text)

    def test_unicode_normalized_input_preservation(self):
        """Normalized Unicode with combining marks (e.g. ə̄) must not be split."""
        text = normalize_text("kavya vəlu ə̄")
        tokens = tokenize(text)
        words = extract_words(tokens)
        self.assertIn("ə̄", words)


if __name__ == "__main__":
    unittest.main()
