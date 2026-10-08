from kawi_tts.acoustic.strategies.base import AbstractProfileStrategy, ProfiledToken, PolicyStatus
from kawi_tts.acoustic.strategies.profile_b import _V1_PRESERVED, _V1_PROVISIONAL

_ASPIRATE_MERGERS = {
    "bʱ": "b",
    "dʱ": "d",
    "gʱ": "g",
    "pʰ": "p",
    "tʰ": "t",
    "kʰ": "k",
    "cʰ": "c",
    "ɟʱ": "ɟ",
    "ṭʰ": "ṭ",
    "ḍʱ": "ḍ",
}

_NASAL_MERGERS = {
    "ṇ": "n",
}

_SIBILANT_MERGERS = {
    "ś": "s",
    "ṣ": "s",
}

_LIQUID_ADAPTATIONS = {
    "r̩": "rə",
    "l̩": "lə",
    "r̩ː": "rə",
    "l̩ː": "lə",
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
            
        if canonical_token in _NASAL_MERGERS:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=_NASAL_MERGERS[canonical_token],
                profile_name=self.profile_name,
                status=PolicyStatus.EVIDENCE_BACKED,
                citation="P5-002 / retroflex nasal merger"
            )
            
        if canonical_token in _LIQUID_ADAPTATIONS:
            if "ː" in canonical_token:
                status = PolicyStatus.SCHOLARLY_RECONSTRUCTION
                citation = "P5-002B / scholarly reconstruction of long syllabic-liquid adaptation"
            else:
                status = PolicyStatus.EVIDENCE_BACKED
                citation = "P5-002A / evidence-backed short syllabic-liquid adaptation"
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=_LIQUID_ADAPTATIONS[canonical_token],
                profile_name=self.profile_name,
                status=status,
                citation=citation
            )
            
        # Vowel length neutralization (Scholarly Reconstruction Grade B)
        if canonical_token in {"aː", "iː", "uː", "əː"}:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=canonical_token.replace("ː", ""),
                profile_name=self.profile_name,
                status=PolicyStatus.SCHOLARLY_RECONSTRUCTION,
                citation="P6-003R / scholarly reconstruction of duration neutralization"
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
        
        if canonical_token in _V1_PROVISIONAL:
            return ProfiledToken(
                canonical_token=canonical_token,
                target_token=canonical_token,
                profile_name=self.profile_name,
                status=PolicyStatus.PROVISIONAL_RECONSTRUCTION,
                citation=_V1_PROVISIONAL[canonical_token]
            )
        
        return ProfiledToken(
            canonical_token=canonical_token,
            target_token=canonical_token,
            profile_name=self.profile_name,
            status=PolicyStatus.UNSUPPORTED,
            citation=f"Unsupported canonical token '{canonical_token}'"
        )
