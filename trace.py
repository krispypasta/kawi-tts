from src.g2p.engine import g2p_word
from src.normalization.tokenizer import tokenize

words = ["sanghyang", "sang-hyang", "awighnam", "taṅi"]

for w in words:
    print(f"INPUT: {w}")
    tokens = tokenize(w)
    out = []
    for t in tokens:
        if t.token_type.name in ["WORD", "UNRESOLVED"]:
            out.append(g2p_word(t.text))
        else:
            out.append([t.text])
    print(f"CANONICAL TOKENS: {out}")
    print()

