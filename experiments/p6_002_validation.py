import sys
from typing import List
from src.g2p.engine import g2p
from src.acoustic.mapper import AcousticMapper
from src.acoustic.strategies import get_strategy

def generate_matrix(words: List[str]):
    print("=" * 80)
    print("PHASE 3 — GOLDEN A/B MATRIX")
    print("=" * 80)
    
    strategy_a = get_strategy("A")
    strategy_b = get_strategy("B")
    
    for word in words:
        canonical_word = g2p(word)
        # flatten canonical word
        canonical_tokens = [tok for sublist in canonical_word for tok in sublist]
        canonical_str = "".join(canonical_tokens)
        
        target_a_tokens = [strategy_a.apply(tok).target_token for tok in canonical_tokens]
        target_b_tokens = [strategy_b.apply(tok).target_token for tok in canonical_tokens]
        
        target_a_str = "".join(target_a_tokens)
        target_b_str = "".join(target_b_tokens)
        
        trace_a = [(tok, strategy_a.apply(tok).status.name) for tok in canonical_tokens]
        trace_b = [(tok, strategy_b.apply(tok).status.name) for tok in canonical_tokens]
        
        print(f"INPUT       : {word}")
        print(f"CANONICAL   : {canonical_str}")
        print(f"TARGET A    : {target_a_str}")
        print(f"TARGET B    : {target_b_str}")
        print(f"TRACE A     : {trace_a}")
        print(f"TRACE B     : {trace_b}")
        print("-" * 80)

def test_canonical_immutability():
    print("=" * 80)
    print("PHASE 6 — CANONICAL IMMUTABILITY")
    print("=" * 80)
    
    strategy_a = get_strategy("A")
    strategy_b = get_strategy("B")
    
    canonical_token_original = "bʱ"
    canonical_token_ref = canonical_token_original
    
    a_res = strategy_a.apply(canonical_token_ref)
    b_res = strategy_b.apply(canonical_token_ref)
    
    if canonical_token_ref == canonical_token_original and a_res.canonical_token == canonical_token_original and b_res.canonical_token == canonical_token_original:
        print("PASS: Canonical token is immutable and identical after A and B transforms.")
    else:
        print("FAIL: Canonical token mutated!")

if __name__ == "__main__":
    test_words = [
        "bhaṭāra",     # aspirate, retroflex
        "śānti",       # sibilant, macron
        "kṛta",        # syllabic liquid
        "paḍaṅ",       # retroflex
        "sanghyang",   # sanghyang parsing
        "sĕkar",       # ordinary word
        "ghaṇṭā",      # voiced aspirate, retroflex, macron
        "ṣaḍguṇa"      # retroflex sibilant, retroflex stops
    ]
    generate_matrix(test_words)
    test_canonical_immutability()
