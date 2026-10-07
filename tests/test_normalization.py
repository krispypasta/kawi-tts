"""Unit tests for Old Javanese Unicode and orthographic normalization."""

import unittest
from kawi_tts.normalization import (
    NormalizationResult,
    convert_transliteration_convention,
    normalize,
    normalize_text,
)


class TestNormalization(unittest.TestCase):

    """Test suite for Unicode and orthographic normalization."""

    def test_canonicalize_acri_damais_v_to_w(self):
        """Verify Acri/Damais variant 'v' normalizes to 'w', but Roman numeral 'V' is unaffected."""
        self.assertEqual(normalize("viṣṇu").normalized_text, "wiṣṇu")
        # Ensure uppercase V is NOT changed
        self.assertEqual(normalize("Bab V").normalized_text, "Bab V")
        self.assertEqual(normalize("Vīra").normalized_text, "Vīra")

        # Verify it can be disabled
        self.assertEqual(
            normalize("viṣṇu", canonicalize_acri_damais=False).normalized_text,
            "viṣṇu"
        )

    def test_nfc_nfd_composition(self):
        """Decomposed characters (NFD) must compose to canonical NFC equivalents."""
        # Decomposed a + combining macron
        decomposed_a_macron = "a\u0304"
        self.assertEqual(normalize_text(decomposed_a_macron), "ā")

        # Decomposed t + combining dot below
        decomposed_t_dot = "t\u0323"
        self.assertEqual(normalize_text(decomposed_t_dot), "ṭ")

        # Decomposed d + combining dot below
        decomposed_d_dot = "d\u0323"
        self.assertEqual(normalize_text(decomposed_d_dot), "ḍ")

        # Decomposed s + combining acute (ś) and s + combining dot below (ṣ)
        self.assertEqual(normalize_text("s\u0301"), "ś")
        self.assertEqual(normalize_text("s\u0323"), "ṣ")

        # Decomposed e + combining breve (ĕ)
        self.assertEqual(normalize_text("e\u0306"), "ĕ")

        # Decomposed o + combining diaeresis (ö)
        self.assertEqual(normalize_text("o\u0308"), "ö")

        # Decomposed n + combining dot above (ṅ)
        self.assertEqual(normalize_text("n\u0307"), "ṅ")

        # Decomposed n + combining tilde (ñ)
        self.assertEqual(normalize_text("n\u0303"), "ñ")

        # Decomposed n + combining dot below (ṇ)
        self.assertEqual(normalize_text("n\u0323"), "ṇ")

        # Decomposed r + dot below (ṛ) and double diacritic r + dot below + macron (ṝ)
        self.assertEqual(normalize_text("r\u0323"), "ṛ")
        self.assertEqual(normalize_text("r\u0323\u0304"), "ṝ")

        # Decomposed l + dot below (ḷ)
        self.assertEqual(normalize_text("l\u0323"), "ḷ")

    def test_macrons_preserved(self):
        """Vowel length macrons (ā, ī, ū) must be strictly preserved, never stripped."""
        text = "bāpā śrī mahārāja"
        self.assertEqual(normalize_text(text), "bāpā śrī mahārāja")
        self.assertIn("ā", normalize_text(text))
        self.assertIn("ī", normalize_text(text))

        # Distinctness invariant: ā must not equal a
        self.assertNotEqual(normalize_text("ā"), normalize_text("a"))
        self.assertNotEqual(normalize_text("ī"), normalize_text("i"))
        self.assertNotEqual(normalize_text("ū"), normalize_text("u"))

    def test_underdots_preserved(self):
        """Retroflex/alveolar consonants and underdot symbols must be preserved."""
        text = "bhaṭāra saṅ hyang ḍaṅ hyang"
        self.assertEqual(normalize_text(text), "bhaṭāra saṅ hyang ḍaṅ hyang")

        # Distinctness invariant: ṭ != t, ḍ != d, ṇ != n, ṣ != s
        self.assertNotEqual(normalize_text("ṭ"), normalize_text("t"))
        self.assertNotEqual(normalize_text("ḍ"), normalize_text("d"))
        self.assertNotEqual(normalize_text("ṇ"), normalize_text("n"))
        self.assertNotEqual(normalize_text("ṣ"), normalize_text("s"))

    def test_sibilants_preserved(self):
        """Distinctions between dental (s), palatal (ś), and retroflex (ṣ) must be preserved."""
        # Neither ś nor ṣ may be collapsed into s
        self.assertEqual(normalize_text("śānti"), "śānti")
        self.assertEqual(normalize_text("ṣaḍguṇa"), "ṣaḍguṇa")
        self.assertEqual(normalize_text("sarwa"), "sarwa")

        self.assertNotEqual(normalize_text("ś"), normalize_text("s"))
        self.assertNotEqual(normalize_text("ṣ"), normalize_text("s"))
        self.assertNotEqual(normalize_text("ś"), normalize_text("ṣ"))

    def test_aspirates_preserved(self):
        """Aspirated sequences (bh, dh, th, ph, kh, gh, etc.) must remain distinguishable."""
        # No aspirate-merging at normalization time
        aspirates = ["bhaṭāra", "dharmma", "artha", "phala", "khecara", "ghaṇṭā", "chanda", "jhala"]
        for word in aspirates:
            self.assertEqual(normalize_text(word), word)

        # Invariant: bhaṭāra must not become baṭāra
        self.assertNotEqual(normalize_text("bhaṭāra"), "baṭāra")
        self.assertNotEqual(normalize_text("dharma"), "darma")

    def test_ng_vs_n_dot_above(self):
        """ASCII 'ng' must NOT be converted to 'ṅ'; typographic 'ŋ' MUST become 'ṅ'."""
        # ASCII 'ng' is preserved verbatim
        self.assertEqual(normalize_text("sang hyang"), "sang hyang")
        self.assertEqual(normalize_text("tangi"), "tangi")

        # Typographic 'ŋ' (eng) from Dutch printings is unified to 'ṅ'
        self.assertEqual(normalize_text("saŋ hyaŋ"), "saṅ hyaṅ")
        self.assertEqual(normalize_text("taŋi"), "taṅi")

        # Uppercase Ŋ -> Ṅ
        self.assertEqual(normalize_text("Ŋwaṅ"), "Ṅwaṅ")

    def test_pepet_and_diaeresis(self):
        """ĕ (breve) and ö (diaeresis) must be preserved; ě (caron) normalized to ĕ."""
        self.assertEqual(normalize_text("sĕkar"), "sĕkar")
        self.assertEqual(normalize_text("böt"), "böt")

        # Keyboard mistake with caron (ě) unifies to breve (ĕ)
        self.assertEqual(normalize_text("sěkar"), "sĕkar")
        self.assertEqual(normalize_text("Ĕndas"), "Ĕndas")
        self.assertEqual(normalize_text("Ěndas"), "Ĕndas")

        # Default normalization must NOT map ĕ -> ə or vice versa
        self.assertEqual(normalize_text("sĕkar"), "sĕkar")
        self.assertEqual(normalize_text("səkar"), "səkar")
        self.assertNotEqual(normalize_text("sĕkar"), normalize_text("səkar"))

    def test_vocalic_liquids_preserved(self):
        """Vocalic liquids ṛ and ḷ must be preserved."""
        self.assertEqual(normalize_text("kṛta"), "kṛta")
        self.assertEqual(normalize_text("kḷpta"), "kḷpta")
        self.assertNotEqual(normalize_text("ṛ"), "r")
        self.assertNotEqual(normalize_text("ḷ"), "l")

    def test_apostrophes_and_sandhi_markers(self):
        """Typographic/curly quotes must be normalized to standard apostrophe."""
        self.assertEqual(normalize_text("hantusakĕn’âmuruk"), "hantusakĕn'âmuruk")
        self.assertEqual(normalize_text("hantusakĕn‘âmuruk"), "hantusakĕn'âmuruk")
        self.assertEqual(normalize_text("’n"), "'n")

    def test_invisible_characters_removed(self):
        """Invisible formatting artifacts (BOM, soft hyphen, ZWS) must be cleanly removed."""
        bom_text = "\ufeffom awighnam\u00ad astu\u200b"
        self.assertEqual(normalize_text(bom_text), "om awighnam astu")

    def test_whitespace_handling(self):
        """Whitespace runs and non-breaking spaces must be collapsed; lines preserved."""
        self.assertEqual(
            normalize_text("  om\u00a0awighnam   astu  \n  namo   siddham  "),
            "om awighnam astu\nnamo siddham",
        )

        # Empty and blank strings
        self.assertEqual(normalize_text(""), "")
        self.assertEqual(normalize_text("   \t  \n  "), "")

    def test_punctuation_and_ordinary_text(self):
        """Standard punctuation, numerals, and ASCII letters must pass through untouched."""
        text = "1. Om, awighnam astu! (Kawi-TTS 2026)."
        self.assertEqual(normalize_text(text), text)

    def test_provenance_steps(self):
        """NormalizationResult must accurately record which steps were applied."""
        res_noop = normalize("dharma")
        self.assertEqual(res_noop.steps_applied, [])

        res_nfc = normalize("a\u0304")
        self.assertIn("unicode_nfc", res_nfc.steps_applied)
        self.assertEqual(res_nfc.normalized_text, "ā")

        res_eng = normalize("saŋa")
        self.assertIn("canonicalized_eng_to_n_dot_above", res_eng.steps_applied)
        self.assertEqual(res_eng.normalized_text, "saṅa")

        res_caron = normalize("sěkar")
        self.assertIn("canonicalized_pepet_caron_to_breve", res_caron.steps_applied)
        self.assertEqual(res_caron.normalized_text, "sĕkar")

        res_apos = normalize("’n")
        self.assertIn("canonicalized_apostrophes", res_apos.steps_applied)
        self.assertEqual(res_apos.normalized_text, "'n")

        res_ws = normalize("  a   b  ")
        self.assertIn("normalized_whitespace", res_ws.steps_applied)
        self.assertEqual(res_ws.normalized_text, "a b")

    def test_transliteration_convention_conversion(self):
        """Explicit transliteration conversion between Zoetmulder and Acri/Damais."""
        # Acri/Damais to Zoetmulder
        acri_text = "kavya vəlu ə̄"
        zoet_res = convert_transliteration_convention(
            acri_text,
            source_convention="acri_damais",
            target_convention="zoetmulder",
        )
        self.assertEqual(zoet_res.normalized_text, "kawya wĕlu ö")
        self.assertIn("converted_acri_damais_to_zoetmulder", zoet_res.steps_applied)

        # Zoetmulder to Acri/Damais
        zoet_text = "kawya wĕlu ö"
        acri_res = convert_transliteration_convention(
            zoet_text,
            source_convention="zoetmulder",
            target_convention="acri_damais",
        )
        self.assertEqual(acri_res.normalized_text, "kavya vəlu ə̄")
        self.assertIn("converted_zoetmulder_to_acri_damais", acri_res.steps_applied)

        # Same scheme is a no-op
        same_res = convert_transliteration_convention(
            "kawya",
            source_convention="zoetmulder",
            target_convention="zoetmulder",
        )
        self.assertEqual(same_res.normalized_text, "kawya")

        # Unsupported scheme raises ValueError
        with self.assertRaises(ValueError):
            convert_transliteration_convention(
                "kawya",
                source_convention="zoetmulder",
                target_convention="unknown_scheme",
            )


if __name__ == "__main__":
    unittest.main()
