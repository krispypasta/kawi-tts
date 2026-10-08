"""End-to-end Kawi-TTS synthesis pipeline prototype.

Orchestrates the complete flow:
Kawi text
→ Unicode normalization (src/normalization/normalizer.py)
→ text structure & tokenization (src/normalization/tokenizer.py)
→ lossless G2P (src/g2p/engine.py)
→ acoustic mapping (src/acoustic/mapper.py)
→ eSpeak-ng backend (src/acoustic/espeak_backend.py)
→ audio output
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from kawi_tts.acoustic.espeak_backend import ESpeakBackend, SynthesisResult
from kawi_tts.acoustic.mapper import AcousticMapper, AcousticMappingResult
from kawi_tts.g2p.engine import g2p_word
from kawi_tts.normalization.normalizer import NormalizationResult, normalize
from kawi_tts.normalization.tokenizer import Token, TokenType, extract_words, tokenize


class AmbiguousTokenError(ValueError):
    """Raised when strict=True and unresolved tokens are present."""

@dataclass(frozen=True)
class PipelineResult:
    """Complete provenance and execution log of an end-to-end synthesis invocation.

    Attributes:
        input_text: Verbatim raw input string.
        normalization: Output of the Unicode normalization stage.
        tokens: Tokens segmented by the text structure stage.
        words: Lexical word strings passed to G2P.
        g2p_phonemes: Lossless internal phonemes produced by G2P.
        acoustic_mapping: Mapped tokens, eSpeak IPA string, and provisional audit.
        synthesis: Invocation details and WAV generation result from backend.
    """

    input_text: str
    normalization: NormalizationResult
    tokens: List[Token]
    synthesis_chunks: List[str]
    g2p_phonemes: List[List[str]]
    acoustic_mapping: AcousticMappingResult
    synthesis: SynthesisResult


def synthesize(
    text: str,
    *,
    profile: str = "A",
    output_path: Optional[str] = None,
    voice: str = "jv",
    dry_run: bool = False,
    create_dummy_wav: bool = False,
    executable: Optional[str] = None,
    strict: bool = True,
) -> PipelineResult:
    """Execute the complete end-to-end Kawi-TTS synthesis pipeline.

    Args:
        text: Raw Kawi text input.
        profile: Pronunciation profile identifier (default 'A' for Historical Spoken).
        output_path: Target path for output WAV file. If None, audio is stored in memory.
        voice: Voice code for eSpeak-ng (default 'jv' for Javanese).
        dry_run: If True, simulates execution without invoking the real eSpeak-ng binary.
        create_dummy_wav: If True and dry_run=True, writes a minimal 44-byte WAV header
            to output_path for testing file creation workflows.
        executable: Optional custom path to eSpeak-ng binary.
        strict: If True, raises AmbiguousTokenError for unresolved tokens.

    Returns:
        PipelineResult containing outputs from all intermediate layers and synthesis.
        
    Raises:
        AmbiguousTokenError: If strict is True and an unresolved token is present.
    """
    # 1. Unicode & Orthographic Normalization
    norm_res = normalize(text)

    # 2. Text Structure & Tokenization
    tokens = tokenize(norm_res.normalized_text)
    if strict:
        for t in tokens:
            if t.token_type == TokenType.UNRESOLVED:
                raise AmbiguousTokenError(f"Ambiguous/Unresolved token detected in strict mode: '{t.text}'")

    valid_types = {TokenType.WORD, TokenType.UNRESOLVED, TokenType.PUNCTUATION}
    synthesis_chunks = [t.text for t in tokens if t.token_type in valid_types]

    # 3. Lossless G2P
    g2p_phonemes = [g2p_word(w) for w in synthesis_chunks]

    # 4. Explicit Acoustic Mapping (Profile A)
    # The AcousticMapper no longer handles espeak-id fallback; it maps to pure IPA.
    mapper = AcousticMapper(profile=profile)
    mapping_res = mapper.map_phonemes(g2p_phonemes)

    # 5. Acoustic Backend Synthesis (eSpeak-ng)
    backend = ESpeakBackend(executable=executable, voice=voice)
    synthesis_res = backend.synthesize(
        mapping_res.backend_phoneme_string,
        output_path=output_path,
        dry_run=dry_run,
        create_dummy_wav=create_dummy_wav,
    )

    return PipelineResult(
        input_text=text,
        normalization=norm_res,
        tokens=tokens,
        synthesis_chunks=synthesis_chunks,
        g2p_phonemes=g2p_phonemes,
        acoustic_mapping=mapping_res,
        synthesis=synthesis_res,
    )
