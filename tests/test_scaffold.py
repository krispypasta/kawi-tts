"""Basic scaffold sanity tests for Kawi-TTS."""

import unittest
import kawi_tts
import kawi_tts.g2p
import kawi_tts.normalization
import kawi_tts.tts


class TestScaffold(unittest.TestCase):
    def test_package_imports(self):
        self.assertIsNotNone(kawi_tts.__version__)
        self.assertIsNotNone(kawi_tts.normalization)
        self.assertIsNotNone(kawi_tts.g2p)
        self.assertIsNotNone(kawi_tts.tts)


if __name__ == "__main__":
    unittest.main()
