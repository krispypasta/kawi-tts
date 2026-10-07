import csv
import os
import unittest

from kawi_tts.normalization.normalizer import normalize_text
from kawi_tts.normalization.tokenizer import tokenize, TokenType
from kawi_tts.g2p.engine import g2p_word
from kawi_tts.acoustic.strategies import get_strategy

class TestRegressionCorpus(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        corpus_path = os.path.join(os.path.dirname(__file__), 'regression_corpus.tsv')
        cls.corpus = []
        with open(corpus_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                cls.corpus.append(row)
                
        cls.strat_a = get_strategy("A")
        cls.strat_b = get_strategy("B")

    def test_regression_corpus(self):
        for idx, row in enumerate(self.corpus):
            input_word = row["Input"]
            expected_canon = row["Canonical"]
            expected_pa = row["ProfileA"]
            expected_pb = row["ProfileB"]
            
            with self.subTest(word=input_word, idx=idx):
                # 1. Normalization
                norm = normalize_text(input_word)
                
                # 2. Tokenization
                tokens = tokenize(norm)
                ambig_flag = any(t.has_ambiguity for t in tokens)
                
                if ambig_flag:
                    self.assertEqual("AMBIGUOUS", expected_canon, f"Expected AMBIGUOUS but got {expected_canon}")
                    self.assertEqual("AMBIGUOUS", expected_pa, f"Expected AMBIGUOUS but got {expected_pa}")
                    self.assertEqual("AMBIGUOUS", expected_pb, f"Expected AMBIGUOUS but got {expected_pb}")
                    continue
                else:
                    self.assertNotEqual("AMBIGUOUS", expected_canon, f"Did not expect AMBIGUOUS for {input_word}")
                
                canon_lists = []
                pa_lists = []
                pb_lists = []
                
                for t in tokens:
                    # We skip punctuation for this comparison to match the TSV easily, 
                    # except the hyphens are dropped by the tokenizer, leaving WORDs
                    if t.token_type == TokenType.WORD:
                        canon = g2p_word(t.text)
                        canon_lists.append(canon)
                        
                        pa_str = "-".join([self.strat_a.apply(p).target_token for p in canon])
                        pb_str = "-".join([self.strat_b.apply(p).target_token for p in canon])
                        
                        pa_lists.append(pa_str)
                        pb_lists.append(pb_str)
                        
                canon_str = "-".join(["-".join(c) for c in canon_lists])
                pa_final = "-".join(pa_lists)
                pb_final = "-".join(pb_lists)
                
                self.assertEqual(expected_canon, canon_str, f"Canonical mismatch for '{input_word}'")
                self.assertEqual(expected_pa, pa_final, f"Profile A mismatch for '{input_word}'")
                self.assertEqual(expected_pb, pb_final, f"Profile B mismatch for '{input_word}'")
                
if __name__ == '__main__':
    unittest.main()
