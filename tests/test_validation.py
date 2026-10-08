"""Evidence-based end-to-end pipeline validation tests.

Validates the full Kawi-TTS pipeline on authentic, source-cited Old Javanese
lexical and textual examples from Zoetmulder (1982), the Old Javanese Wordnet (OJW),
and GRETIL digitized texts.
"""

import unittest
from kawi_tts.acoustic.mapper import MappingStatus
from kawi_tts.acoustic.pipeline import PipelineResult, synthesize
from kawi_tts.normalization.tokenizer import TokenType


class TestEvidenceBasedValidation(unittest.TestCase):
    """Validation test suite executing authentic Old Javanese source citations."""

    def test_native_austronesian_vocabulary(self):
        """Native Austronesian vocabulary (sĕkar Z1728, wukir Z2322, tumutupi OJW/Z2084)."""
        # sĕkar (flower, Zoetmulder 1982:1728)
        res_sekar = synthesize("sĕkar", profile="B", dry_run=True)
        self.assertEqual(res_sekar.synthesis_chunks, ["sĕkar"])
        self.assertEqual(res_sekar.g2p_phonemes[0], ["s", "ə", "k", "a", "r"])
        self.assertEqual(res_sekar.acoustic_mapping.backend_phoneme_string, "səkar")
        self.assertEqual(len(res_sekar.acoustic_mapping.provisional_mappings), 0)

        # wukir (mountain, Zoetmulder 1982:2322)
        res_wukir = synthesize("wukir", profile="B", dry_run=True)
        self.assertEqual(res_wukir.g2p_phonemes[0], ["w", "u", "k", "i", "r"])
        self.assertEqual(res_wukir.acoustic_mapping.backend_phoneme_string, "wukir")

        # tumutupi (cover, infixed root with -um- and -i, OJW / Zoetmulder 1982:2084)
        res_tutup = synthesize("tumutupi", profile="B", dry_run=True)
        self.assertEqual(res_tutup.g2p_phonemes[0], ["t", "u", "m", "u", "t", "u", "p", "i"])
        self.assertEqual(res_tutup.acoustic_mapping.backend_phoneme_string, "tumutupi")

    def test_native_vowel_inventory(self):
        """Native vowels a, i, u, e, o, ĕ/ə (sosok Z1808, lĕsuṅ Z1016)."""
        # sosok (pour out, Zoetmulder 1982:1808)
        res_sosok = synthesize("sosok", profile="B", dry_run=True)
        self.assertEqual(res_sosok.g2p_phonemes[0], ["s", "o", "s", "o", "k"])
        self.assertEqual(res_sosok.acoustic_mapping.backend_phoneme_string, "sosok")

        # lĕsuṅ (rice mortar, Zoetmulder 1982:1016)
        res_lesung = synthesize("lĕsuṅ", profile="B", dry_run=True)
        self.assertEqual(res_lesung.g2p_phonemes[0], ["l", "ə", "s", "u", "ŋ"])
        self.assertEqual(res_lesung.acoustic_mapping.backend_phoneme_string, "ləsuŋ")

    def test_long_vowels(self):
        """Sanskrit loans with long vowels ā, ī, ū (śānti GRETIL, pūjā Z1429)."""
        # śānti (peace, GRETIL / Zoetmulder 1982:1697)
        res_santi = synthesize("śānti", profile="B", dry_run=True)
        self.assertEqual(res_santi.g2p_phonemes[0], ["ś", "aː", "n", "t", "i"])
        self.assertEqual(res_santi.acoustic_mapping.backend_phoneme_string, "ʃaːnti")
        self.assertIn("ː", res_santi.acoustic_mapping.backend_phoneme_string)

        # pūjā (worship, Zoetmulder 1982:1429)
        res_puja = synthesize("pūjā", profile="B", dry_run=True)
        self.assertEqual(res_puja.g2p_phonemes[0], ["p", "uː", "ɟ", "aː"])
        self.assertEqual(res_puja.acoustic_mapping.backend_phoneme_string, "puːɟaː")

    def test_retroflex_stops_native_and_loans(self):
        """Retroflex/second-series stops ṭ and ḍ (paḍaṅ Z1225, bhaṭāra Z214)."""
        # paḍaṅ (cleared field, native Austronesian root, Zoetmulder 1982:1225)
        res_padang = synthesize("paḍaṅ", profile="B", dry_run=True)
        self.assertEqual(res_padang.g2p_phonemes[0], ["p", "a", "ḍ", "a", "ŋ"])
        self.assertEqual(res_padang.acoustic_mapping.backend_phoneme_string, "paɖaŋ")

        # bhaṭāra (deity, Sanskrit loan, Zoetmulder 1982:214)
        res_bhatara = synthesize("bhaṭāra", profile="B", dry_run=True)
        self.assertEqual(res_bhatara.g2p_phonemes[0], ["bʱ", "a", "ṭ", "aː", "r", "a"])
        self.assertEqual(res_bhatara.acoustic_mapping.backend_phoneme_string, "bʱaʈaːra")

    def test_retroflex_nasal(self):
        """Retroflex nasal ṇ (ghaṇṭā Z523, rāmāyaṇa GRETIL)."""
        # ghaṇṭā (bell, Zoetmulder 1982:523)
        res_ghanta = synthesize("ghaṇṭā", profile="B", dry_run=True)
        self.assertEqual(res_ghanta.g2p_phonemes[0], ["gʱ", "a", "ṇ", "ṭ", "aː"])
        self.assertEqual(res_ghanta.acoustic_mapping.backend_phoneme_string, "gʱaɳʈaː")

        # rāmāyaṇa (proper name, GRETIL)
        res_rama = synthesize("rāmāyaṇa", profile="B", dry_run=True)
        self.assertEqual(res_rama.g2p_phonemes[0], ["r", "aː", "m", "aː", "j", "a", "ṇ", "a"])
        self.assertEqual(res_rama.acoustic_mapping.backend_phoneme_string, "raːmaːjaɳa")

    def test_sibilant_distinctions(self):
        """Sibilants s, ś, and ṣ remain distinct (sawah Z1715, śānti, ṣaḍguṇa Z1603)."""
        res_sawah = synthesize("sawah", profile="B", dry_run=True)
        self.assertEqual(res_sawah.g2p_phonemes[0][0], "s")
        self.assertEqual(res_sawah.acoustic_mapping.backend_phoneme_string, "sawah")

        res_sadguna = synthesize("ṣaḍguṇa", profile="B", dry_run=True)
        self.assertEqual(res_sadguna.g2p_phonemes[0][0], "ṣ")
        self.assertEqual(res_sadguna.acoustic_mapping.backend_phoneme_string, "ʂaɖguɳa")

    def test_aspirates_and_provisional_labeling(self):
        """Aspirates (dharma Z392, awighnam GRETIL, phala Z1354)."""
        res_dharma = synthesize("dharma", profile="B", dry_run=True)
        self.assertEqual(res_dharma.g2p_phonemes[0], ["dʱ", "a", "r", "m", "a"])
        self.assertEqual(res_dharma.acoustic_mapping.backend_phoneme_string, "dʱarma")
        self.assertEqual(len(res_dharma.acoustic_mapping.provisional_mappings), 1)
        self.assertEqual(res_dharma.acoustic_mapping.provisional_mappings[0].internal_token, "dʱ")
        self.assertEqual(
            res_dharma.acoustic_mapping.provisional_mappings[0].status,
            MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING,
        )

        res_phala = synthesize("phala", profile="B", dry_run=True)
        self.assertEqual(res_phala.g2p_phonemes[0], ["pʰ", "a", "l", "a"])
        self.assertEqual(res_phala.acoustic_mapping.backend_phoneme_string, "pʰala")

    def test_vocalic_liquids(self):
        """Vocalic liquids ṛ and ḷ (kṛta Z903, pariwṛta OJW, kḷpta Z879)."""
        # kṛta (done, order, Zoetmulder 1982:903)
        res_krta = synthesize("kṛta", profile="B", dry_run=True)
        self.assertEqual(res_krta.g2p_phonemes[0], ["k", "r̩", "t", "a"])
        self.assertEqual(res_krta.acoustic_mapping.backend_phoneme_string, "kr̩ta")
        self.assertEqual(len(res_krta.acoustic_mapping.provisional_mappings), 1)
        self.assertEqual(res_krta.acoustic_mapping.provisional_mappings[0].internal_token, "r̩")

        # pariwṛta (surrounded, OJW / Zoetmulder 1982:1296)
        res_pari = synthesize("pariwṛta", profile="B", dry_run=True)
        self.assertEqual(res_pari.g2p_phonemes[0], ["p", "a", "r", "i", "w", "r̩", "t", "a"])

        # kḷpta (fixed, Zoetmulder 1982:879)
        res_klpta = synthesize("kḷpta", profile="B", dry_run=True)
        self.assertEqual(res_klpta.g2p_phonemes[0], ["k", "l̩", "p", "t", "a"])
        self.assertEqual(res_klpta.acoustic_mapping.backend_phoneme_string, "kl̩pta")

    def test_velar_nasal_normalization_and_palatal(self):
        """Typographic ŋ (Zoetmulder 1982 print) normalizes to ṅ; palatal ñ preserved."""
        # saŋ -> normalized to saṅ -> G2P /ŋ/
        res_sang_dutch = synthesize("saŋ", profile="B", dry_run=True)
        self.assertEqual(res_sang_dutch.normalization.normalized_text, "saṅ")
        self.assertEqual(res_sang_dutch.g2p_phonemes[0], ["s", "a", "ŋ"])
        self.assertEqual(res_sang_dutch.acoustic_mapping.backend_phoneme_string, "saŋ")

        # kaña (Zoetmulder 1982:785)
        res_kana = synthesize("kaña", profile="B", dry_run=True)
        self.assertEqual(res_kana.g2p_phonemes[0], ["k", "a", "ɲ", "a"])
        self.assertEqual(res_kana.acoustic_mapping.backend_phoneme_string, "kaɲa")

    def test_ascii_ambiguity_sanghyang(self):
        """ASCII sanghyang triggers UNRESOLVED, while sang-hyang and saṅhyaṅ resolve cleanly."""
        # Un-hyphenated ASCII sanghyang: flagged as UNRESOLVED
        res_raw = synthesize("sanghyang", profile="B", dry_run=True, strict=False)
        self.assertEqual(res_raw.tokens[0].token_type, TokenType.UNRESOLVED)
        self.assertTrue(res_raw.tokens[0].has_ambiguity)

        # Disambiguated by boundary: sang-hyang
        res_hyphen = synthesize("sang-hyang", profile="B", dry_run=True)
        self.assertEqual(res_hyphen.synthesis_chunks, ["sang", "hyang"])
        self.assertEqual(res_hyphen.g2p_phonemes, [["s", "a", "n", "g"], ["h", "j", "a", "n", "g"]])
        self.assertEqual(res_hyphen.acoustic_mapping.backend_phoneme_string, "sang hjang")
        self.assertNotIn("gʱ", res_hyphen.acoustic_mapping.backend_phoneme_string)

        # Canonical orthography: saṅhyaṅ (Zoetmulder 1982:663)
        res_canon = synthesize("saṅhyaṅ", profile="B", dry_run=True)
        self.assertEqual(res_canon.g2p_phonemes[0], ["s", "a", "ŋ", "h", "j", "a", "ŋ"])
        self.assertEqual(res_canon.acoustic_mapping.backend_phoneme_string, "saŋhjaŋ")
        self.assertFalse(res_canon.tokens[0].has_ambiguity)

    def test_reduplication(self):
        """Reduplicated forms with boundary hyphen (gilaṅ-gilaṅ Z525)."""
        res_redup = synthesize("gilaṅ-gilaṅ", profile="B", dry_run=True)
        self.assertEqual(res_redup.synthesis_chunks, ["gilaṅ", "gilaṅ"])
        self.assertEqual(res_redup.g2p_phonemes, [["g", "i", "l", "a", "ŋ"], ["g", "i", "l", "a", "ŋ"]])
        self.assertEqual(res_redup.acoustic_mapping.backend_phoneme_string, "gilaŋ gilaŋ")

    def test_sandhi_and_clitic_elisions(self):
        """Enclitic connector 'n (lingira'n Z1034) and article 'ng (ri'ng Z1546)."""
        # lingira'n (Zoetmulder 1982:1034)
        res_lingira = synthesize("liṅgira'n", profile="B", dry_run=True)
        self.assertEqual(res_lingira.synthesis_chunks, ["liṅgira", "n"])
        self.assertEqual(res_lingira.g2p_phonemes, [["l", "i", "ŋ", "g", "i", "r", "a"], ["n"]])
        self.assertEqual(res_lingira.acoustic_mapping.backend_phoneme_string, "liŋgira n")

        # ri'ng (Zoetmulder 1982:1546)
        res_ring = synthesize("ri'ṅ", profile="B", dry_run=True)
        self.assertEqual(res_ring.synthesis_chunks, ["ri", "ṅ"])
        self.assertEqual(res_ring.g2p_phonemes, [["r", "i"], ["ŋ"]])
        self.assertEqual(res_ring.acoustic_mapping.backend_phoneme_string, "ri ŋ")

    def test_capitalized_proper_nouns_and_titles(self):
        """Capitalized words (Śrī, Bhaṭāra, Gaṇapati) must parse correctly into phonemes."""
        # Śrī (honorable prefix, Mpu Tanakung / Inscriptions)
        res_sri = synthesize("Śrī", profile="B", dry_run=True)
        self.assertEqual(res_sri.g2p_phonemes[0], ["ś", "r", "iː"])
        self.assertEqual(res_sri.acoustic_mapping.backend_phoneme_string, "ʃriː")

        # Bhaṭāra (capitalized Sanskrit deity title)
        res_bhatara = synthesize("Bhaṭāra", profile="B", dry_run=True)
        self.assertEqual(res_bhatara.g2p_phonemes[0], ["bʱ", "a", "ṭ", "aː", "r", "a"])
        self.assertEqual(res_bhatara.acoustic_mapping.backend_phoneme_string, "bʱaʈaːra")

        # Gaṇapati (GRETIL title)
        res_ganapati = synthesize("Gaṇapati", profile="B", dry_run=True)
        self.assertEqual(res_ganapati.g2p_phonemes[0], ["g", "a", "ṇ", "a", "p", "a", "t", "i"])
        self.assertEqual(res_ganapati.acoustic_mapping.backend_phoneme_string, "gaɳapati")

    def test_g2p_immutability_through_mapper(self):
        """G2P phoneme lists must NOT be mutated during acoustic mapping."""
        res = synthesize("bhaṭāra śānti", profile="B", dry_run=True)
        # Verify internal G2P tokens are untouched
        self.assertEqual(res.g2p_phonemes[0], ["bʱ", "a", "ṭ", "aː", "r", "a"])
        self.assertEqual(res.g2p_phonemes[1], ["ś", "aː", "n", "t", "i"])
        # Verify mapped tokens are separate
        self.assertEqual(res.acoustic_mapping.mapped_words[0][0].internal_token, "bʱ")
        self.assertEqual(res.acoustic_mapping.mapped_words[0][0].backend_token, "bʱ")
        self.assertEqual(res.acoustic_mapping.mapped_words[0][2].internal_token, "ṭ")
        self.assertEqual(res.acoustic_mapping.mapped_words[0][2].backend_token, "ʈ")
        self.assertEqual(res.acoustic_mapping.mapped_words[1][0].internal_token, "ś")
        self.assertEqual(res.acoustic_mapping.mapped_words[1][0].backend_token, "ʃ")


if __name__ == "__main__":
    unittest.main()
