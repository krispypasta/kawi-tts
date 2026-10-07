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

from src.acoustic.espeak_backend import ESpeakBackend, SynthesisResult
from src.acoustic.mapper import AcousticMapper, AcousticMappingResult
from src.g2p.engine import g2p_word
from src.normalization.normalizer import NormalizationResult, normalize
from src.normalization.tokenizer import Token, extract_words, tokenize


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
    words: List[str]
    g2p_phonemes: List[List[str]]
    acoustic_mapping: AcousticMappingResult
    synthesis: SynthesisResult


def synthesize(
    text: str,
    *,
    profile: str = "A",
    output_path: Optional[str] = None,
    voice: str = "jv",
    dry_run: bool = True,
    create_dummy_wav: bool = False,
    executable: Optional[str] = None,
) -> PipelineResult:
    """Execute the complete end-to-end Kawi-TTS synthesis pipeline.

    Args:
        text: Raw Kawi text input.
        profile: Pronunciation profile identifier (default 'A' for Historical Spoken).
        output_path: Target path for output WAV file.
        voice: Voice code for eSpeak-ng (default 'jv' for Javanese).
        dry_run: If True, simulates execution without invoking the real eSpeak-ng binary.
        create_dummy_wav: If True and dry_run=True, writes a minimal 44-byte WAV header
            to output_path for testing file creation workflows.
        executable: Optional custom path to eSpeak-ng binary.

    Returns:
        PipelineResult containing outputs from all intermediate layers and synthesis.
    """
    # 1. Unicode & Orthographic Normalization
    norm_res = normalize(text)

    # 2. Text Structure & Tokenization
    tokens = tokenize(norm_res.normalized_text)
    words = extract_words(tokens)

    # 3. Lossless G2P
    g2p_phonemes = [g2p_word(w) for w in words]

    # 4. Explicit Acoustic Mapping (Profile A)
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
        words=words,
        g2p_phonemes=g2p_phonemes,
        acoustic_mapping=mapping_res,
        synthesis=synthesis_res,
    )
