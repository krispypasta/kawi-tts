from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class PolicyStatus(Enum):
    PRESERVED = "PRESERVED"
    PROVISIONAL_RECONSTRUCTION = "PROVISIONAL_RECONSTRUCTION"
    SCHOLARLY_RECONSTRUCTION = "SCHOLARLY_RECONSTRUCTION"
    EVIDENCE_BACKED = "EVIDENCE_BACKED"
    UNSUPPORTED = "UNSUPPORTED"
    UNRESOLVED = "UNRESOLVED"

@dataclass(frozen=True)
class ProfiledToken:
    """A canonical token interpreted according to a specific linguistic profile."""
    canonical_token: str
    target_token: str
    profile_name: str
    status: PolicyStatus
    citation: Optional[str] = None

class AbstractProfileStrategy(ABC):
    """Abstract base class for all pronunciation profile strategies."""
    
    @property
    @abstractmethod
    def profile_name(self) -> str:
        """Name of the profile."""
        pass

    @abstractmethod
    def apply(self, canonical_token: str) -> ProfiledToken:
        """Interpret a canonical token under this profile's rules."""
        pass
