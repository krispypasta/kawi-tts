"""Basic scaffold sanity tests for Kawi-TTS."""

import unittest
import src
import src.g2p
import src.normalization
import src.tts


class TestScaffold(unittest.TestCase):
    def test_package_imports(self):
        self.assertIsNotNone(src.__version__)
        self.assertIsNotNone(src.normalization)
        self.assertIsNotNone(src.g2p)
        self.assertIsNotNone(src.tts)


if __name__ == "__main__":
    unittest.main()
