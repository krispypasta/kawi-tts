"""Acoustic Mapper module for Kawi-TTS.

This module maps internal phonological representations (output from the lossless
G2P layer) to backend-compatible phonetic/IPA representations for synthesis.

CRITICAL PROJECT POLICY (see AGENTS.md, docs/DECISIONS.md, and docs/P3_005_ACOUSTIC_BACKEND_SURVEY.md):
- The G2P layer preserves all linguistic distinctions.
- The Acoustic Mapper is the ONLY layer permitted to perform provisional backend
  adaptations.
- Every provisional adaptation is explicitly stamped as PROVISIONAL_ACOUSTIC_MAPPING.
- No provisional mapping is claimed as proven historical pronunciation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class MappingStatus(Enum):
    """Status classification of an acoustic token mapping."""

    PRESERVED = "PRESERVED"
    PROVISIONAL_ACOUSTIC_MAPPING = "PROVISIONAL_ACOUSTIC_MAPPING"
    UNSUPPORTED = "UNSUPPORTED"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class MappedToken:
    """Represents a single phoneme mapped from internal representation to backend format.

    Attributes:
        internal_token: The verbatim phonological token from the G2P engine.
        backend_token: The target symbol formatted for the acoustic backend (e.g. eSpeak-ng IPA).
        status: Classification of the mapping (PRESERVED, PROVISIONAL_ACOUSTIC_MAPPING, etc.).
        note: Explanatory note or citation regarding provisional adaptation.
    """

    internal_token: str
    backend_token: str
    status: MappingStatus
    note: Optional[str] = None


@dataclass(frozen=True)
class AcousticMappingResult:
    """Result of mapping a sequence of phoneme words to acoustic backend representation.

    Attributes:
        original_phonemes: Verbatim list of words (lists of internal phonemes) from G2P.
        mapped_words: Nested list of MappedToken objects corresponding to the input.
        backend_phoneme_string: Space-separated, backend-ready phonetic/IPA string.
        provisional_mappings: List of all tokens that required provisional acoustic adaptation.
        unsupported_tokens: List of tokens that could not be mapped.
    """

    original_phonemes: List[List[str]]
    mapped_words: List[List[MappedToken]]
    backend_phoneme_string: str
    provisional_mappings: List[MappedToken] = field(default_factory=list)
    unsupported_tokens: List[MappedToken] = field(default_factory=list)


# Direct, lossless 1:1 mappings from internal phonological representation to eSpeak-ng IPA.
_PRESERVED_MAP: Dict[str, Tuple[str, Optional[str]]] = {
    # Native short vowels (RES-001)
    "a": ("a", None),
    "i": ("i", None),
    "u": ("u", None),
    "e": ("e", None),
    "o": ("o", None),
    "ə": ("ə", None),
    # Vowel length: eSpeak IPA natively supports the length chroneme ː (U+02D0)
    "aː": ("aː", "Preserving vowel length chroneme in IPA for eSpeak duration."),
    "iː": ("iː", "Preserving vowel length chroneme in IPA for eSpeak duration."),
    "uː": ("uː", "Preserving vowel length chroneme in IPA for eSpeak duration."),
    # Core consonants (RES-001)
    "p": ("p", None),
    "b": ("b", None),
    "t": ("t", None),
    "d": ("d", None),
    "c": ("c", None),
    "ɟ": ("ɟ", None),
    "k": ("k", None),
    "g": ("g", None),
    "m": ("m", None),
    "n": ("n", None),
    "ŋ": ("ŋ", None),
    "ɲ": ("ɲ", None),
    "s": ("s", None),
    "h": ("h", None),
    "r": ("r", None),
    "l": ("l", None),
    "w": ("w", None),
    "j": ("j", None),
    # Retroflex series (RES-001, RES-005): mapped to standard IPA retroflex plosives / nasal
    "ṭ": ("ʈ", "Mapped internal ṭ to IPA voiceless retroflex plosive ʈ."),
    "ḍ": ("ɖ", "Mapped internal ḍ to IPA voiced retroflex plosive ɖ."),
    "ṇ": ("ɳ", "Mapped internal ṇ to IPA retroflex nasal ɳ."),
    # Sibilants (RES-006): mapped to standard IPA postalveolar / retroflex fricatives
    "ś": ("ʃ", "Mapped internal ś to IPA voiceless postalveolar fricative ʃ."),
    "ṣ": ("ʂ", "Mapped internal ṣ to IPA voiceless retroflex fricative ʂ."),
    # Voiceless aspirates: eSpeak-ng natively handles aspirated plosives with ʰ
    "tʰ": ("tʰ", "IPA voiceless dental/alveolar aspirated plosive."),
    "pʰ": ("pʰ", "IPA voiceless bilabial aspirated plosive."),
    "kʰ": ("kʰ", "IPA voiceless velar aspirated plosive."),
    "cʰ": ("cʰ", "IPA voiceless palatal aspirated plosive."),
    "ṭʰ": ("ʈʰ", "IPA voiceless retroflex aspirated plosive."),
    # Punctuation / boundaries
    ".": (".", None),
    ",": (",", None),
    ";": (";", None),
    ":": (":", None),
    "!": ("!", None),
    "?": ("?", None),
    "-": ("-", None),
    "'": ("'", None),
}

# Provisional acoustic mappings: phonological categories that require explicit
# provisional phonetic adaptation for eSpeak-ng synthesis.
# Every entry here MUST be stamped MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING.
_PROVISIONAL_MAP: Dict[str, Tuple[str, str]] = {
    # Voiced aspirates (breathy voice): eSpeak IPA handles voiced stops with aspiration
    # via [Cʱ] or [Ch]. Historical realization in colloquial Kawi is uncertain (RES-004, DEC-006).
    "bʱ": (
        "bʱ",
        "PROVISIONAL_ACOUSTIC_MAPPING: Voiced bilabial aspirate for eSpeak-ng; "
        "historical realization in spoken Kawi remains uncertain (RES-004).",
    ),
    "dʱ": (
        "dʱ",
        "PROVISIONAL_ACOUSTIC_MAPPING: Voiced dental/alveolar aspirate for eSpeak-ng; "
        "historical realization in spoken Kawi remains uncertain (RES-004).",
    ),
    "gʱ": (
        "gʱ",
        "PROVISIONAL_ACOUSTIC_MAPPING: Voiced velar aspirate for eSpeak-ng; "
        "historical realization in spoken Kawi remains uncertain (RES-004).",
    ),
    "ɟʱ": (
        "ɟʱ",
        "PROVISIONAL_ACOUSTIC_MAPPING: Voiced palatal aspirate for eSpeak-ng; "
        "historical realization in spoken Kawi remains uncertain (RES-004).",
    ),
    "ḍʱ": (
        "ɖʱ",
        "PROVISIONAL_ACOUSTIC_MAPPING: Voiced retroflex aspirate for eSpeak-ng; "
        "historical realization in spoken Kawi remains uncertain (RES-004).",
    ),
    # Vocalic liquids: syllabic liquids are Sanskrit features. In eSpeak IPA, represented
    # as syllabic [r̩] and [l̩]. Does NOT assert spoken Kawi had [r̩] vs [rə].
    "r̩": (
        "r̩",
        "PROVISIONAL_ACOUSTIC_MAPPING: Syllabic rhotic liquid for eSpeak-ng; "
        "historical phonetic realization remains uncertain (P3-003A).",
    ),
    "l̩": (
        "l̩",
        "PROVISIONAL_ACOUSTIC_MAPPING: Syllabic lateral liquid for eSpeak-ng; "
        "historical phonetic realization remains uncertain (P3-003A).",
    ),
    "r̩ː": (
        "r̩ː",
        "PROVISIONAL_ACOUSTIC_MAPPING: Long syllabic rhotic liquid for eSpeak-ng.",
    ),
    "l̩ː": (
        "l̩ː",
        "PROVISIONAL_ACOUSTIC_MAPPING: Long syllabic lateral liquid for eSpeak-ng.",
    ),
    # Long pepet / ö (RES-002, RES-007)
    "əː": (
        "əː",
        "PROVISIONAL_ACOUSTIC_MAPPING: Lengthened mid-central schwa for eSpeak-ng; "
        "phonetic status cross-linguistically rare and historically uncertain.",
    ),
}


class AcousticMapper:
    """Translates internal phonological tokens into backend-compatible eSpeak-ng IPA."""

    def __init__(self, profile: str = "A"):
        """Initialize the mapper for a specific pronunciation profile.

        Args:
            profile: Pronunciation profile identifier ('A' for Reconstructed Historical Spoken).
        """
        self.profile = profile

    def map_token(self, token: str) -> MappedToken:
        """Map a single internal phoneme token to a MappedToken.

        Args:
            token: Verbatim internal phoneme token from G2P.

        Returns:
            MappedToken object with status classification.
        """
        # 1. Check preserved 1:1 mappings
        if token in _PRESERVED_MAP:
            backend_tok, note = _PRESERVED_MAP[token]
            return MappedToken(
                internal_token=token,
                backend_token=backend_tok,
                status=MappingStatus.PRESERVED,
                note=note,
            )

        # 2. Check provisional mappings
        if token in _PROVISIONAL_MAP:
            backend_tok, note = _PROVISIONAL_MAP[token]
            return MappedToken(
                internal_token=token,
                backend_token=backend_tok,
                status=MappingStatus.PROVISIONAL_ACOUSTIC_MAPPING,
                note=note,
            )

        # 3. Fallback for unrecognized tokens
        return MappedToken(
            internal_token=token,
            backend_token=token,
            status=MappingStatus.UNSUPPORTED,
            note=f"Unsupported token '{token}' in acoustic mapper.",
        )

    def map_phonemes(self, phoneme_words: List[List[str]]) -> AcousticMappingResult:
        """Map a nested list of words and internal phonemes to backend IPA representation.

        Args:
            phoneme_words: List of words, where each word is a list of internal phonemes.

        Returns:
            AcousticMappingResult containing mapped tokens, full backend string, and audits.
        """
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
