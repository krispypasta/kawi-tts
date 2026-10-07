"""Acoustic mapping and backend synthesis interfaces for Kawi-TTS."""

from kawi_tts.acoustic.espeak_backend import (
    ESpeakBackend,
    ESpeakNotFoundError,
    SynthesisResult,
    create_minimal_wav_header,
)
from kawi_tts.acoustic.mapper import (
    AcousticMapper,
    AcousticMappingResult,
    MappedToken,
    MappingStatus,
)
from kawi_tts.acoustic.pipeline import PipelineResult, synthesize

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
