import unittest
from pathlib import Path
from kawi_tts.acoustic.espeak_backend import ESpeakBackend

class TestESpeakBackendDecoupling(unittest.TestCase):
    def test_espeak_id_approximations_applied_in_backend(self):
        """Backend correctly applies eSpeak 'id' replacements, keeping mapper pure."""
        backend = ESpeakBackend(voice="id")
        
        # Retroflex ʈ -> t, bʱ -> bh
        res1 = backend.synthesize("bʱaʈaːra", dry_run=True, create_dummy_wav=False)
        self.assertEqual(res1.phoneme_input, "bhatara")
        
    def test_espeak_jv_leaves_ipa_intact(self):
        """Backend leaves standard IPA intact when not targeting 'id' voice."""
        backend = ESpeakBackend(voice="jv")
        
        res = backend.synthesize("bʱaʈaːra", dry_run=True, create_dummy_wav=False)
        self.assertEqual(res.phoneme_input, "bʱaʈaːra")
        
    def test_espeak_native_ascii_mnemonics(self):
        """Backend converts special phonemes to eSpeak ascii mappings."""
        backend = ESpeakBackend(voice="id")
        
        res = backend.synthesize("ŋəɟa", dry_run=True, create_dummy_wav=False)
        # ŋ -> N, ə -> @, ɟ -> dZ
        self.assertEqual(res.phoneme_input, "N@dZa")

if __name__ == "__main__":
    unittest.main()
