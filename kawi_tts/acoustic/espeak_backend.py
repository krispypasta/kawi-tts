"""eSpeak-ng acoustic backend interface for Kawi-TTS.

This module invokes eSpeak-ng via its phoneme/IPA input interface to synthesize
speech from mapped phonetic tokens. It provides mock/dry-run support when eSpeak-ng
is not installed on the host machine.
"""

from __future__ import annotations

import shutil
import struct
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


class ESpeakNotFoundError(RuntimeError):
    """Raised when an attempt is made to synthesize real audio but eSpeak-ng is not installed."""


@dataclass(frozen=True)
class SynthesisResult:
    """Detailed result of an acoustic synthesis invocation.

    Attributes:
        phoneme_input: The phonetic/IPA string passed to the backend.
        voice: The voice identifier requested (e.g. 'jv', 'id').
        output_path: Target path for the output WAV file.
        command: Full CLI argument list constructed for eSpeak-ng.
        dry_run: Whether synthesis was executed in dry-run/mock mode.
        audio_generated: Whether a valid WAV file was produced on disk or in memory.
        bytes_written: Number of bytes written to output_path.
        audio_bytes: Raw WAV bytes if output_path is None.
    """

    phoneme_input: str
    voice: str
    output_path: Optional[str]
    command: List[str]
    dry_run: bool
    audio_generated: bool
    bytes_written: int = 0
    audio_bytes: Optional[bytes] = None


def create_minimal_wav_header(sample_rate: int = 22050) -> bytes:
    """Generate a canonical 44-byte RIFF/WAVE header with 0 data samples for dry-run testing."""
    num_channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = 0
    riff_chunk_size = 36 + data_size
    return struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        riff_chunk_size,
        b"WAVE",
        b"fmt ",
        16,
        1,  # PCM
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size,
    )


class ESpeakBackend:
    """Wrapper around the eSpeak-ng command-line phoneme synthesis engine."""

    _ESPEAK_ID_APPROXIMATION = {
        "ə": "@", "əː": "@",
        "ŋ": "N", "ɲ": "n^", "ɟ": "dZ",
        "aː": "a", "iː": "i", "uː": "u",
        "ʈ": "t", "ɖ": "d", "ɳ": "n",
        "ʃ": "s", "ʂ": "s",
        "tʰ": "th", "pʰ": "ph", "kʰ": "kh", "cʰ": "ch", "ʈʰ": "th",
        "bʱ": "bh", "dʱ": "dh", "gʱ": "gh", "ɟʱ": "dZh", "ḍʱ": "dh",
        "r̩": "r@", "l̩": "l@", "r̩ː": "r@", "l̩ː": "l@",
        "rə": "r@", "lə": "l@",
    }

    def __init__(self, executable: Optional[str] = None, voice: str = "jv"):
        """Initialize the eSpeak backend interface.

        Args:
            executable: Custom path to espeak-ng/espeak binary. If None, discovers via PATH.
            voice: Voice name or language code (default 'jv' for Javanese).
        """
        self.voice = voice
        self.executable_path = executable or self._find_executable()

    @property
    def is_available(self) -> bool:
        """Check whether a usable eSpeak-ng executable was located on the system."""
        return self.executable_path is not None

    @staticmethod
    def _find_executable() -> Optional[str]:
        """Discover espeak-ng or espeak in system PATH."""
        return shutil.which("espeak-ng") or shutil.which("espeak")

    def synthesize(
        self,
        phoneme_str: str,
        output_path: Optional[str] = None,
        *,
        dry_run: bool = False,
        create_dummy_wav: bool = False,
    ) -> SynthesisResult:
        """Synthesize a phonetic/IPA string to audio.

        Args:
            phoneme_str: Space-separated backend-ready phoneme string.
            output_path: File path to save output WAV file. If None, audio is returned in memory.
            dry_run: If True, simulates execution without invoking the real binary.
            create_dummy_wav: If True in dry_run mode, writes a minimal 44-byte WAV header
                to output_path to test file generation workflows.

        Returns:
            SynthesisResult object documenting the invocation.

        Raises:
            ESpeakNotFoundError: If dry_run is False but eSpeak-ng is not installed.
            subprocess.CalledProcessError: If eSpeak-ng execution fails.
        """
        target_path = str(output_path) if output_path else None
        
        # Apply backend-specific phonetic approximations if using Indonesian voice
        final_phoneme_str = phoneme_str
        if self.voice == "id":
            # Sort replacements by length descending to prevent substring collisions
            sorted_replacements = sorted(self._ESPEAK_ID_APPROXIMATION.items(), key=lambda x: len(x[0]), reverse=True)
            for k, v in sorted_replacements:
                final_phoneme_str = final_phoneme_str.replace(k, v)
        
        # Format input phoneme string inside eSpeak [[...]] brackets
        phoneme_bracketed = f"[[{final_phoneme_str}]]"

        exec_cmd = [
            self.executable_path or "espeak-ng",
            "-v",
            self.voice,
        ]
        if target_path:
            exec_cmd.extend(["-w", target_path])
        else:
            exec_cmd.append("--stdout")
            
        exec_cmd.append(phoneme_bracketed)

        if dry_run:
            bytes_written = 0
            wav_bytes = create_minimal_wav_header() if create_dummy_wav else None
            if target_path and wav_bytes:
                Path(target_path).parent.mkdir(parents=True, exist_ok=True)
                with open(target_path, "wb") as f:
                    f.write(wav_bytes)
                bytes_written = len(wav_bytes)

            return SynthesisResult(
                phoneme_input=final_phoneme_str,
                voice=self.voice,
                output_path=target_path,
                command=exec_cmd,
                dry_run=True,
                audio_generated=(create_dummy_wav),
                bytes_written=bytes_written,
                audio_bytes=wav_bytes if not target_path else None,
            )

        # Real execution requested
        if not self.is_available:
            raise ESpeakNotFoundError(
                "eSpeak-ng executable not found in system PATH. To generate real audio:\n"
                "  1. Install eSpeak-ng (e.g., via 'winget install eSpeak-ng' on Windows, "
                "'apt install espeak-ng' on Debian/Ubuntu, or from https://github.com/espeak-ng/espeak-ng/releases).\n"
                "  2. Or instantiate ESpeakBackend(executable='/path/to/espeak-ng').\n"
                "Alternatively, specify dry_run=True to verify pipeline data flow without generating audio."
            )

        if target_path:
            Path(target_path).parent.mkdir(parents=True, exist_ok=True)
            
        result = subprocess.run(
            exec_cmd,
            check=True,
            capture_output=True,
        )

        audio_bytes = None
        file_size = 0
        if target_path:
            file_size = Path(target_path).stat().st_size if Path(target_path).exists() else 0
        else:
            audio_bytes = result.stdout
            file_size = len(audio_bytes)

        return SynthesisResult(
            phoneme_input=final_phoneme_str,
            voice=self.voice,
            output_path=target_path,
            command=exec_cmd,
            dry_run=False,
            audio_generated=(file_size > 0),
            bytes_written=file_size,
            audio_bytes=audio_bytes,
        )
