import unittest
from kawi_tts.acoustic.strategies import get_strategy
from kawi_tts.acoustic.strategies.base import PolicyStatus

class TestProfileStrategies(unittest.TestCase):
    def setUp(self):
        self.strategy_a = get_strategy("A")
        self.strategy_b = get_strategy("B")

    def test_profile_b_compatibility(self):
        """Profile B must reproduce legacy pass-through behavior."""
        # Aspirate
        tok = self.strategy_b.apply("bʱ")
        self.assertEqual(tok.target_token, "bʱ")
        self.assertEqual(tok.status, PolicyStatus.PROVISIONAL_RECONSTRUCTION)
        self.assertIn("historical realization", tok.citation)

        # Sibilant
        tok = self.strategy_b.apply("ś")
        self.assertEqual(tok.target_token, "ś")
        self.assertEqual(tok.status, PolicyStatus.PRESERVED)

        # Unsupported
        tok = self.strategy_b.apply("x")
        self.assertEqual(tok.target_token, "x")
        self.assertEqual(tok.status, PolicyStatus.UNSUPPORTED)

    def test_profile_a_transformations(self):
        """Profile A must apply historical mergers."""
        # Aspirates merge to plain stops
        tok = self.strategy_a.apply("bʱ")
        self.assertEqual(tok.target_token, "b")
        self.assertEqual(tok.status, PolicyStatus.EVIDENCE_BACKED)
        self.assertEqual(tok.citation, "P5-002 / aspirate merger")
        
        # Unsupported aspirates fall back to PROVISIONAL pass-through
        tok = self.strategy_a.apply("ḍʱ")
        self.assertEqual(tok.target_token, "ḍʱ")
        self.assertEqual(tok.status, PolicyStatus.PROVISIONAL_RECONSTRUCTION)

        # Sibilants merge to native sibilant
        tok = self.strategy_a.apply("ś")
        self.assertEqual(tok.target_token, "s")
        self.assertEqual(tok.status, PolicyStatus.EVIDENCE_BACKED)
        self.assertEqual(tok.citation, "P5-002 / sibilant merger")

        # Syllabic liquids adapt provisionally
        tok = self.strategy_a.apply("r̩")
        self.assertEqual(tok.target_token, "rə")
        self.assertEqual(tok.status, PolicyStatus.PROVISIONAL_RECONSTRUCTION)
        self.assertEqual(tok.citation, "P5-002 / syllabic-liquid adaptation")

    def test_dental_retroflex_preserved(self):
        """Both profiles must preserve dental vs retroflex distinction."""
        tok_a_dent = self.strategy_a.apply("d")
        tok_a_retro = self.strategy_a.apply("ḍ")
        self.assertEqual(tok_a_dent.target_token, "d")
        self.assertEqual(tok_a_retro.target_token, "ḍ")

        tok_b_dent = self.strategy_b.apply("d")
        tok_b_retro = self.strategy_b.apply("ḍ")
        self.assertEqual(tok_b_dent.target_token, "d")
        self.assertEqual(tok_b_retro.target_token, "ḍ")

    def test_vowel_length_behavior(self):
        """Vowel length must remain unresolved but target token is preserved."""
        tok_a = self.strategy_a.apply("aː")
        self.assertEqual(tok_a.target_token, "a")
        self.assertEqual(tok_a.status, PolicyStatus.UNRESOLVED)
        self.assertEqual(tok_a.citation, "P6-003R / unresolved duration engineering fallback")

        tok_b = self.strategy_b.apply("aː")
        self.assertEqual(tok_b.target_token, "aː")
        self.assertEqual(tok_b.status, PolicyStatus.PRESERVED)
        
    def test_canonical_immutability(self):
        """Profile strategy MUST NOT mutate the canonical token."""
        tok_a = self.strategy_a.apply("bʱ")
        self.assertEqual(tok_a.canonical_token, "bʱ")
        self.assertEqual(tok_a.target_token, "b")

if __name__ == "__main__":
    unittest.main()
