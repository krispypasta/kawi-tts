"""Text normalization module for Old Javanese (Kawi) Romanized text.

Provides deterministic Unicode canonicalization (NFC) and orthographic cleanup
without altering linguistically meaningful phonological distinctions.
"""

from src.normalization.normalizer import (
    NormalizationResult,
    convert_transliteration_convention,
    normalize,
    normalize_text,
)
from src.normalization.tokenizer import (
    Token,
    TokenType,
    extract_words,
    get_ambiguities,
    tokenize,
)

__all__ = [
    "NormalizationResult",
    "normalize",
    "normalize_text",
    "convert_transliteration_convention",
    "Token",
    "TokenType",
    "tokenize",
    "extract_words",
    "get_ambiguities",
]
