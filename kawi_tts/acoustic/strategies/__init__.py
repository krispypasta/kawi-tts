from kawi_tts.acoustic.strategies.base import AbstractProfileStrategy, ProfiledToken, PolicyStatus
from kawi_tts.acoustic.strategies.profile_a import ProfileAStrategy
from kawi_tts.acoustic.strategies.profile_b import ProfileBStrategy

def get_strategy(profile_name: str) -> AbstractProfileStrategy:
    if profile_name.upper() == "A":
        return ProfileAStrategy()
    elif profile_name.upper() == "B":
        return ProfileBStrategy()
    raise ValueError(f"Unknown profile: {profile_name}")
