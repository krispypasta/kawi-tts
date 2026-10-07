import sys
from src.normalization.normalizer import normalize_text
from src.normalization.tokenizer import tokenize, TokenType
from src.g2p.engine import g2p_word
from src.acoustic.strategies import get_strategy
from src.acoustic.mapper import AcousticMapper

def run_trace(word_in: str):
    # 1. Normalizer
    norm = normalize_text(word_in)
    
    # 2. Tokenizer
    tokens = tokenize(norm)
    if not tokens or tokens[0].token_type != TokenType.WORD:
        print(f"[{word_in}] -> NOT A WORD OR EMPTY")
        return
    tok = tokens[0]
    is_ambig = tok.has_ambiguity
    
    # 3. G2P / Canonical
    canon = g2p_word(tok.text)
    canon_str = "-".join(canon)
    
    # 4. Profile A / B
    strat_a = get_strategy("A")
    strat_b = get_strategy("B")
    
    prof_a = [strat_a.apply(t) for t in canon]
    prof_b = [strat_b.apply(t) for t in canon]
    
    prof_a_str = "-".join([p.target_token for p in prof_a])
    prof_b_str = "-".join([p.target_token for p in prof_b])
    
    # 5. Acoustic Mapper
    map_a = AcousticMapper("A")
    map_b = AcousticMapper("B")
    
    res_a = map_a.map_phonemes([canon])
    res_b = map_b.map_phonemes([canon])
    
    print(f"Input       : {word_in}")
    if is_ambig:
        print(f"Ambiguity   : FLAG RAISED")
    print(f"Normalized  : {norm}")
    print(f"Canonical   : {canon_str}")
    print(f"Profile A   : {prof_a_str}")
    print(f"Profile B   : {prof_b_str}")
    print(f"Acoustic A  : {res_a.backend_phoneme_string}")
    print(f"Acoustic B  : {res_b.backend_phoneme_string}")
    print("-" * 50)

words = [
    "sĕkar",
    "BHAṬĀRA",
    "tĕka",
    "dharma",
    "sankha",
    "śānti",
    "kṛta",
    "kṝta",
    "rāma",
    "ḍaṅ",
    "dan",
    "tangi",
    "sang-hyang"
]

for w in words:
    run_trace(w)
