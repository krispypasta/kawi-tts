"""Acoustic Mapper module for Kawi-TTS.

This module maps internal phonological representations (output from the lossless
G2P layer) to backend-compatible phonetic/IPA representations for synthesis,
using injected ProfileStrategies to determine linguistic policy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from kawi_tts.acoustic.strategies import get_strategy
from kawi_tts.acoustic.strategies.base import PolicyStatus, ProfiledToken

class MappingStatus(Enum):
    """Status classification of an acoustic token mapping. 
    Kept backward compatible for V1 tests."""
    PRESERVED = "PRESERVED"
    PROVISIONAL_ACOUSTIC_MAPPING = "PROVISIONAL_ACOUSTIC_MAPPING"
    SCHOLARLY_RECONSTRUCTION = "SCHOLARLY_RECONSTRUCTION"
    UNSUPPORTED = "UNSUPPORTED"
    UNRESOLVED = "UNRESOLVED"
    EVIDENCE_BACKED = "EVIDENCE_BACKED"


@dataclass(frozen=True)
class MappedToken:
    internal_token: str
    backend_token: str
    status: MappingStatus
    note: Optional[str] = None
    profiled_token: Optional[ProfiledToken] = None


@dataclass(frozen=True)
class AcousticMappingResult:
    original_phonemes: List[List[str]]
    mapped_words: List[List[MappedToken]]
    backend_phoneme_string: str
    provisional_mappings: List[MappedToken] = field(default_factory=list)
    unsupported_tokens: List[MappedToken] = field(default_factory=list)


# Pure backend translation layer (no linguistic policy)
_BACKEND_MAP: Dict[str, str] = {
    # Short vowels
    "a": "a", "i": "i", "u": "u", "e": "e", "o": "o", "ə": "ə",
    # Long vowels
    "aː": "aː", "iː": "iː", "uː": "uː", "əː": "əː",
    # Consonants
    "p": "p", "b": "b", "t": "t", "d": "d", "c": "c", "ɟ": "ɟ",
    "k": "k", "g": "g", "m": "m", "n": "n", "ŋ": "ŋ", "ɲ": "ɲ",
    "s": "s", "h": "h", "r": "r", "l": "l", "w": "w", "j": "j",
    # Retroflex
    "ṭ": "ʈ", "ḍ": "ɖ", "ṇ": "ɳ",
    # Sibilants
    "ś": "ʃ", "ṣ": "ʂ",
    # Aspirates (voiceless)
    "tʰ": "tʰ", "pʰ": "pʰ", "kʰ": "kʰ", "cʰ": "cʰ", "ṭʰ": "ʈʰ",
    # Aspirates (voiced - preserved for Profile B)
    "bʱ": "bʱ", "dʱ": "dʱ", "gʱ": "gʱ", "ɟʱ": "ɟʱ", "ḍʱ": "ɖʱ",
    # Syllabic liquids (preserved for Profile B)
    "r̩": "r̩", "l̩": "l̩", "r̩ː": "r̩ː", "l̩ː": "l̩ː",
    # Liquid adaptations (Profile A)
    "rə": "rə", "lə": "lə",
    # Punctuation
    ".": ".", ",": ",", ";": ";", ":": ":", "!": "!", "?": "?", "-": "-", "'": "'",
}


def _map_policy_to_legacy_status(policy: PolicyStatus) -> MappingStatus:
    """Map the new PolicyStatus to the legacy MappingStatus for test compatibility."""
    if policy == PolicyStatus.PRESERVED:
        return MappingStatus.PRESERVED
    elif policy == PolicyStatus.PROVISIONAL_RECONSTRUCTION:
        return MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING
    elif policy == PolicyStatus.SCHOLARLY_RECONSTRUCTION:
        return MappingStatus.SCHOLARLY_RECONSTRUCTION
    elif policy == PolicyStatus.UNSUPPORTED:
        return MappingStatus.UNSUPPORTED
    elif policy == PolicyStatus.UNRESOLVED:
        return MappingStatus.UNRESOLVED
    elif policy == PolicyStatus.EVIDENCE_BACKED:
        return MappingStatus.EVIDENCE_BACKED
    return MappingStatus.UNSUPPORTED


class AcousticMapper:
    """Translates internal phonological tokens into backend-compatible eSpeak-ng IPA."""

    def __init__(self, profile: str = "A"):
        self.profile = profile
        # Load strategy here
        self.strategy = get_strategy(profile)

    def map_token(self, token: str) -> MappedToken:
        # 1. Apply linguistic profile strategy
        profiled_token = self.strategy.apply(token)
        
        # 2. Pure dictionary translation to backend format
        target = profiled_token.target_token
        if target in _BACKEND_MAP:
            backend_tok = _BACKEND_MAP[target]
        else:
            # Fallback for unrecognized target tokens
            backend_tok = target

        legacy_status = _map_policy_to_legacy_status(profiled_token.status)
        note = profiled_token.citation
        
        return MappedToken(
            internal_token=token,
            backend_token=backend_tok,
            status=legacy_status,
            note=note,
            profiled_token=profiled_token
        )

    def map_phonemes(self, phoneme_words: List[List[str]]) -> AcousticMappingResult:
        mapped_words: List[List[MappedToken]] = []
        provisional: List[MappedToken] = []
        unsupported: List[MappedToken] = []
        backend_word_strings: List[str] = []

        for word in phoneme_words:
            mapped_word: List[MappedToken] = []
            backend_chars: List[str] = []

            for tok in word:
                mapped = self.map_token(tok)
                mapped_word.append(mapped)
                backend_chars.append(mapped.backend_token)

                if mapped.status == MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING:
                    provisional.append(mapped)
                elif mapped.status == MappingStatus.UNSUPPORTED:
                    unsupported.append(mapped)

            mapped_words.append(mapped_word)
            backend_word_strings.append("".join(backend_chars))

        backend_phoneme_string = " ".join(backend_word_strings)

        return AcousticMappingResult(
            original_phonemes=phoneme_words,
            mapped_words=mapped_words,
            backend_phoneme_string=backend_phoneme_string,
            provisional_mappings=provisional,
            unsupported_tokens=unsupported,
        )
