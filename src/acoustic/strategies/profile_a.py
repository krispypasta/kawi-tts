from src.acoustic.strategies.base import AbstractProfileStrategy, ProfiledToken, PolicyStatus
from src.acoustic.strategies.profile_b import _V1_PRESERVED, _V1_PROVISIONAL

_ASPIRATE_MERGERS = {
    "bʱ": "b",
    "dʱ": "d",
    "gʱ": "g",
    "ɟʱ": "ɟ",
    "ḍʱ": "ḍ", # Voiced retroflex plain stop
    "pʰ": "p",
    "tʰ": "t",
    "kʰ": "k",
    "cʰ": "c",
    "ṭʰ": "ṭ", # Voiceless retroflex plain stop
}

_SIBILANT_MERGERS = {
    "ś": "s",
    "ṣ": "s",
}

_LIQUID_ADAPTATIONS = {
    "r̩": "rə",
    "l̩": "lə",
    "r̩ː": "rəː",
    "l̩ː": "ləː",
}

class ProfileAStrategy(AbstractProfileStrategy):
    """Profile A Strategy: Reconstructed Historical Spoken Old Javanese.
    
    Applies evidence-backed historical mergers to canonical tokens.
    """

    @property
    def profile_name(self) -> str:
        return "A"

    def apply(self, canonical_token: str) -> ProfiledToken:
        # Vowel length unresolved
        # Wait, if we pass macron through, it goes to preserved?
        
        if canonical_token in _ASPIRATE_MERGERS:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=_ASPIRATE_MERGERS[canonical_token],
                profile_name=self.profile_name,
                status=PolicyStatus.EVIDENCE_BACKED,
                citation="P5-002 / aspirate merger"
            )
            
        if canonical_token in _SIBILANT_MERGERS:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=_SIBILANT_MERGERS[canonical_token],
                profile_name=self.profile_name,
                status=PolicyStatus.EVIDENCE_BACKED,
                citation="P5-002 / sibilant merger"
            )
            
        if canonical_token in _LIQUID_ADAPTATIONS:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=_LIQUID_ADAPTATIONS[canonical_token],
                profile_name=self.profile_name,
                status=PolicyStatus.PROVISIONAL_RECONSTRUCTION,
                citation="P5-002 / syllabic-liquid adaptation"
            )
            
        # Vowel length is structurally deferred (UNRESOLVED policy, but target token remains)
        if canonical_token in {"aː", "iː", "uː", "əː"}:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=canonical_token,
                profile_name=self.profile_name,
                status=PolicyStatus.UNRESOLVED,
                citation="P5-003 / deferred vowel length reduction"
            )

        # Fallback to standard preservation if no historical merger applies
        if canonical_token in _V1_PRESERVED:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=canonical_token,
                profile_name=self.profile_name,
                status=PolicyStatus.PRESERVED,
                citation="V1 Preserved"
            )
        
        # If it was provisional in V1 but not explicitly handled by Profile A, it might be unsupported or we just mark it
        # Actually wait, `əː` is in _V1_PROVISIONAL. We handled it above.
        
        return ProfiledToken(
            canonical_token=canonical_token,
            target_token=canonical_token,
            profile_name=self.profile_name,
            status=PolicyStatus.UNSUPPORTED,
            citation=f"Unsupported canonical token '{canonical_token}'"
        )
