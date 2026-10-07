from src.acoustic.strategies.base import AbstractProfileStrategy, ProfiledToken, PolicyStatus

# Extracted from V1 _PRESERVED_MAP
_V1_PRESERVED = {
    "a", "i", "u", "e", "o", "ə",
    "aː", "iː", "uː",
    "p", "b", "t", "d", "c", "ɟ", "k", "g",
    "m", "n", "ŋ", "ɲ",
    "s", "h", "r", "l", "w", "j",
    "ṭ", "ḍ", "ṇ",
    "ś", "ṣ",
    "tʰ", "pʰ", "kʰ", "cʰ", "ṭʰ",
    ".", ",", ";", ":", "!", "?", "-", "'"
}

# Extracted from V1 _PROVISIONAL_MAP
_V1_PROVISIONAL = {
    "bʱ": "PROVISIONAL_ACOUSTIC_MAPPING: Voiced bilabial aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004).",
    "dʱ": "PROVISIONAL_ACOUSTIC_MAPPING: Voiced dental/alveolar aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004).",
    "gʱ": "PROVISIONAL_ACOUSTIC_MAPPING: Voiced velar aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004).",
    "ɟʱ": "PROVISIONAL_ACOUSTIC_MAPPING: Voiced palatal aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004).",
    "ḍʱ": "PROVISIONAL_ACOUSTIC_MAPPING: Voiced retroflex aspirate for eSpeak-ng; historical realization in spoken Kawi remains uncertain (RES-004).",
    "r̩": "PROVISIONAL_ACOUSTIC_MAPPING: Syllabic rhotic liquid for eSpeak-ng; historical phonetic realization remains uncertain (P3-003A).",
    "l̩": "PROVISIONAL_ACOUSTIC_MAPPING: Syllabic lateral liquid for eSpeak-ng; historical phonetic realization remains uncertain (P3-003A).",
    "r̩ː": "PROVISIONAL_ACOUSTIC_MAPPING: Long syllabic rhotic liquid for eSpeak-ng.",
    "l̩ː": "PROVISIONAL_ACOUSTIC_MAPPING: Long syllabic lateral liquid for eSpeak-ng.",
    "əː": "PROVISIONAL_ACOUSTIC_MAPPING: Lengthened mid-central schwa for eSpeak-ng; phonetic status cross-linguistically rare and historically uncertain.",
}

class ProfileBStrategy(AbstractProfileStrategy):
    """Profile B Strategy: Scholarly / Orthographic Reading.
    
    Passes canonical representations through as closely as possible to
    maximize orthographic traceability, preserving historical distinctions
    (aspirates, sibilants, syllabic liquids) rather than applying speech mergers.
    Reproduces V1 legacy behavior.
    """

    @property
    def profile_name(self) -> str:
        return "B"

    def apply(self, canonical_token: str) -> ProfiledToken:
        if canonical_token in _V1_PRESERVED:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=canonical_token,
                profile_name=self.profile_name,
                status=PolicyStatus.PRESERVED,
                citation="V1 Preserved"
            )
        elif canonical_token in _V1_PROVISIONAL:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=canonical_token,
                profile_name=self.profile_name,
                status=PolicyStatus.PROVISIONAL_RECONSTRUCTION,
                citation=_V1_PROVISIONAL[canonical_token]
            )
        else:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=canonical_token,
                profile_name=self.profile_name,
                status=PolicyStatus.UNSUPPORTED,
                citation=f"Unsupported token '{canonical_token}' in acoustic mapper."
            )
