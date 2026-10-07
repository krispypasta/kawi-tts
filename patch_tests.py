import re

with open("tests/test_profile_strategy.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace(
    'self.assertEqual(tok_a.target_token, "aː")',
    'self.assertEqual(tok_a.target_token, "a")'
)
code = code.replace(
    'self.assertEqual(tok_a.citation, "P5-003 / deferred vowel length reduction")',
    'self.assertEqual(tok_a.citation, "P6-003R / unresolved duration engineering fallback")'
)

with open("tests/test_profile_strategy.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("tests/test_acoustic_mapper_profile_a.py", "r", encoding="utf-8") as f:
    code2 = f.read()

if "test_vowel_length_unresolved" not in code2:
    code2 += """
    def test_vowel_length_unresolved(self):
        res = self.mapper.map_phonemes([["aː"]])
        self.assertEqual(res.backend_phoneme_string, "a")
        tok = res.mapped_words[0][0]
        self.assertEqual(tok.internal_token, "aː")
        self.assertEqual(tok.backend_token, "a")
        self.assertEqual(tok.status, MappingStatus.UNRESOLVED)
        self.assertEqual(tok.note, "P6-003R / unresolved duration engineering fallback")
"""

with open("tests/test_acoustic_mapper_profile_a.py", "w", encoding="utf-8") as f:
    f.write(code2)

print("Tests patched.")
