"""Rule-based Grapheme-to-Phoneme (G2P) engine for Old Javanese (Kawi).

This module parses normalized Old Javanese romanization into a lossless
internal phonological representation (Profile A). It explicitly defers
acoustic mapping (e.g., merging aspirates or vowel length) to preserve
linguistically meaningful distinctions as decided in DEC-006.
"""

from typing import List

# Mapping for multi-character sequences (digraphs).
# These must be evaluated before single characters to ensure greedy matching.
_DIGRAPH_MAP = {
    "bh": "bʱ",
    "dh": "dʱ",
    "th": "tʰ",
    "ph": "pʰ",
    "kh": "kʰ",
    "gh": "gʱ",
    "ch": "cʰ",
    "jh": "ɟʱ",
    "ṭh": "ṭʰ",
    "ḍh": "ḍʱ",
}

# Mapping for single characters.
_MONOGRAPH_MAP = {
    # Vowels
    "a": "a",
    "i": "i",
    "u": "u",
    "e": "e",
    "o": "o",
    "ĕ": "ə",
    
    # Long Vowels (Sanskrit/Metrical)
    "ā": "aː",
    "ī": "iː",
    "ū": "uː",
    "ö": "əː",
    
    # Vocalic Liquids (Sanskrit)
    "ṛ": "r̩",
    "ḷ": "l̩",
    "ṝ": "r̩ː",
    "ḹ": "l̩ː",

    # Consonants
    "p": "p",
    "b": "b",
    "t": "t",
    "d": "d",
    "ṭ": "ṭ",
    "ḍ": "ḍ",
    "c": "c",
    "j": "ɟ",
    "k": "k",
    "g": "g",
    
    # Nasals
    "m": "m",
    "n": "n",
    "ṇ": "ṇ",
    "ṅ": "ŋ",
    "ñ": "ɲ",
    
    # Fricatives
    "s": "s",
    "ś": "ś",
    "ṣ": "ṣ",
    "h": "h",
    
    # Liquids & Glides
    "r": "r",
    "l": "l",
    "w": "w",
    "y": "j",
    
    # Additional explicit mapping for Acri/Damais variants if passed through
    # (Though typically normalization should be handled prior)
    "ə": "ə",
    "v": "w",
}


def g2p_word(word: str) -> List[str]:
    """Convert a single normalized Old Javanese word to internal phonemes.
    
    This function uses a greedy matching approach to ensure digraphs (like 'bh')
    are parsed as single phonological units rather than split into 'b' and 'h'.
    
    Args:
        word: Normalized Old Javanese word.
        
    Returns:
        List of internal phonemes.
    """
    word = word.lower()
    phonemes = []
    i = 0
    length = len(word)
    
    while i < length:
        # Check for digraphs first (greedy match)
        if i < length - 1:
            digraph = word[i:i+2]
            if digraph in _DIGRAPH_MAP:
                phonemes.append(_DIGRAPH_MAP[digraph])
                i += 2
                continue
        
        # Check for monographs
        char = word[i]
        if char in _MONOGRAPH_MAP:
            phonemes.append(_MONOGRAPH_MAP[char])
        else:
            # Preserve unknown characters (punctuation, digits, etc.) as themselves
            phonemes.append(char)
        i += 1
        
    return phonemes


def g2p(text: str) -> List[List[str]]:
    """Convert normalized Old Javanese text into lists of phonemes per word.
    
    Args:
        text: Normalized Old Javanese text.
        
    Returns:
        A list of words, where each word is a list of internal phonemes.
    """
    # Lowercase the text as phonemic representation is case-insensitive
    text = text.lower()
    
    # Split by whitespace to get words
    words = text.split()
    
    return [g2p_word(word) for word in words]
