import unittest
from kawi_tts.g2p.engine import g2p_word

class TestG2P_Sanghyang(unittest.TestCase):
    def test_sanghyang_regression(self):
        # 1. sanghyang (The fix target) Ensures it no longer yields /gʱ/.
        self.assertEqual(
            g2p_word("sanghyang"),
            ['s', 'a', 'n', 'g', 'h', 'j', 'a', 'n', 'g']
        )
        # 2. awighnam (Ensures true Sanskrit gh still yields /gʱ/)
        self.assertEqual(
            g2p_word("awighnam"),
            ['a', 'w', 'i', 'gʱ', 'n', 'a', 'm']
        )
        # 3. tangi (Ensures ASCII ng still yields /n/ + /g/)
        self.assertEqual(
            g2p_word("tangi"),
            ['t', 'a', 'n', 'g', 'i']
        )
        # 4. saṅhyaṅ (Ensures canonical spelling yields /ŋ/ + /h/)
        self.assertEqual(
            g2p_word("saṅhyaṅ"),
            ['s', 'a', 'ŋ', 'h', 'j', 'a', 'ŋ']
        )
        # 5. sang-hyang (Ensures hyphen respects boundaries)
        self.assertEqual(
            g2p_word("sang-hyang"),
            ['s', 'a', 'n', 'g', '-', 'h', 'j', 'a', 'n', 'g']
        )

if __name__ == "__main__":
    unittest.main()
