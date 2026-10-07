"""Grapheme-to-Phoneme (G2P) engine for Old Javanese (Kawi).

This module translates normalized orthography into an internal
lossless phonological representation, preserving uncertain distinctions
for later acoustic mapping.
"""

from kawi_tts.g2p.engine import g2p, g2p_word

__all__ = ["g2p", "g2p_word"]
