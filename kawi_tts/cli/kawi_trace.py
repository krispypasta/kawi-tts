import argparse
import sys
from typing import List

from kawi_tts.normalization.normalizer import normalize_text
from kawi_tts.normalization.tokenizer import tokenize, TokenType
from kawi_tts.g2p.engine import g2p_word
from kawi_tts.acoustic.strategies import get_strategy
from kawi_tts.acoustic.mapper import AcousticMapper

def run_trace(word_in: str):
    print(f"{'='*60}")
    print(f"TRACE: {word_in}")
    print(f"{'='*60}")
    
    # 1. Normalizer
    norm = normalize_text(word_in)
    print(f"[1] Normalized  : {norm}")
    
    # 2. Tokenizer
    tokens = tokenize(norm)
    if not tokens:
        print(f"[2] Tokenizer   : EMPTY")
        return
        
    ambig_flag = any(t.has_ambiguity for t in tokens)
    if ambig_flag:
        print(f"[2] Tokenizer   : BLOCKED (Ambiguity detected)")
        for t in tokens:
            if t.has_ambiguity:
                print(f"    -> Token '{t.text}': {t.ambiguity_reason}")
        return
        
    print(f"[2] Tokenizer   : {len(tokens)} token(s)")
    for i, t in enumerate(tokens):
        print(f"    - {t.token_type.name}: '{t.text}'")
        
    # 3. G2P / Canonical
    canon_list = []
    for t in tokens:
        if t.token_type == TokenType.WORD:
            canon_list.append(g2p_word(t.text))
            
    canon_str = " | ".join(["-".join(c) for c in canon_list])
    print(f"[3] Canonical   : {canon_str}")
    
    # 4. Profile A / B
    strat_a = get_strategy("A")
    strat_b = get_strategy("B")
    
    prof_a_str_list = []
    prof_b_str_list = []
    for canon in canon_list:
        prof_a_str_list.append("-".join([strat_a.apply(t).target_token for t in canon]))
        prof_b_str_list.append("-".join([strat_b.apply(t).target_token for t in canon]))
        
    print(f"[4] Profile A   : {' | '.join(prof_a_str_list)}")
    print(f"[4] Profile B   : {' | '.join(prof_b_str_list)}")
    
    # 5. Acoustic Mapper
    map_a = AcousticMapper("A", adapt_for_espeak_id=True)
    map_b = AcousticMapper("B", adapt_for_espeak_id=True)
    
    res_a = map_a.map_phonemes(canon_list)
    res_b = map_b.map_phonemes(canon_list)
    
    print(f"[5] Acoustic A  : '{res_a.backend_phoneme_string}'")
    for w in res_a.mapped_words:
        for t in w:
            if t.status.name == "BACKEND_APPROXIMATION" and t.profiled_token:
                print(f"    - {t.profiled_token.target_token} -> {t.backend_token} (BACKEND_APPROXIMATION: {t.note})")

    print(f"[5] Acoustic B  : '{res_b.backend_phoneme_string}'")
    for w in res_b.mapped_words:
        for t in w:
            if t.status.name == "BACKEND_APPROXIMATION" and t.profiled_token:
                print(f"    - {t.profiled_token.target_token} -> {t.backend_token} (BACKEND_APPROXIMATION: {t.note})")

    print(f"{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(description="Kawi-TTS Trace CLI - Observational Pipeline Diagnostics")
    parser.add_argument("words", nargs="+", help="One or more words to trace through the pipeline")
    args = parser.parse_args()
    
    for w in args.words:
        run_trace(w)

if __name__ == "__main__":
    main()
