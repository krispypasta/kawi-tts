with open("tests/test_acoustic_mapper_profile_a.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
"""
if __name__ == "__main__":
    unittest.main()

    def test_vowel_length_unresolved(self):
        res = self.mapper.map_phonemes([["aː"]])
        self.assertEqual(res.backend_phoneme_string, "a")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "aː")
        self.assertEqual(tok.backend_token, "a")
        self.assertEqual(tok.status, MappingStatus.UNRESOLVED)
        self.assertEqual(tok.note, "P6-003R / unresolved duration engineering fallback")
""",
"""
    def test_vowel_length_unresolved(self):
        res = self.mapper.map_phonemes([["aː"]])
        self.assertEqual(res.backend_phoneme_string, "a")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "aː")
        self.assertEqual(tok.backend_token, "a")
        self.assertEqual(tok.status, MappingStatus.UNRESOLVED)
        self.assertEqual(tok.note, "P6-003R / unresolved duration engineering fallback")

if __name__ == "__main__":
    unittest.main()
""")

with open("tests/test_acoustic_mapper_profile_a.py", "w", encoding="utf-8") as f:
    f.write(text)
