"""Acoustic mapping and backend synthesis interfaces for Kawi-TTS."""

from src.acoustic.espeak_backend import (
    ESpeakBackend,
    ESpeakNotFoundError,
    SynthesisResult,
    create_minimal_wav_header,
)
from src.acoustic.mapper import (
    AcousticMapper,
    AcousticMappingResult,
    MappedToken,
    MappingStatus,
)
from src.acoustic.pipeline import PipelineResult, synthesize

__all__ = [
    "AcousticMapper",
    "AcousticMappingResult",
    "MappedToken",
    "MappingStatus",
    "ESpeakBackend",
    "ESpeakNotFoundError",
    "SynthesisResult",
    "create_minimal_wav_header",
    "PipelineResult",
    "synthesize",
]
