"""Unicode and orthographic normalization for Old Javanese (Kawi) romanized texts.

This module provides deterministic, lossless Unicode canonicalization (NFC)
and standard orthographic cleanup for romanized Old Javanese texts.

Linguistic Policy (see AGENTS.md, docs/DECISIONS.md, and docs/RESEARCH_LOG.md):
- INFORMATION PRESERVATION FIRST: Normalization does NOT perform pronunciation mapping.
- Unresolved or Sanskrit-derived orthographic distinctions (e.g. aspirates 'bh', 'dh',
  vowel length 'ā', 'ī', 'ū', sibilants 'ś', 'ṣ', retroflexes 'ṭ', 'ḍ', 'ṇ',
  vocalic liquids 'ṛ', 'ḷ', and 'ö') MUST NOT be collapsed.
- ASCII digraph 'ng' is NOT converted to 'ṅ', preserving literal source characters.
- Pepet 'ĕ' is NOT converted to IPA/Damais 'ə' during default normalization; source
  romanization conventions are preserved.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class NormalizationResult:
    """Result of normalizing an input text, including provenance of transformations.

    Attributes:
        original_text: The verbatim string provided to the normalizer.
        normalized_text: The canonical normalized output string.
        steps_applied: List of descriptive tokens indicating which transformations
            were actually applied during normalization.
    """

    original_text: str
    normalized_text: str
    steps_applied: List[str] = field(default_factory=list)


# Pattern for invisible Unicode formatting characters:
# - U+FEFF: Byte Order Mark (BOM) / Zero Width No-Break Space
# - U+00AD: Soft Hyphen
# - U+200B: Zero Width Space
_INVISIBLE_CHARS_PATTERN = re.compile(r"[\ufeff\u00ad\u200b]")

# Typographic apostrophes and quotes used for sandhi elision:
# - U+2019: Right Single Quotation Mark
# - U+2018: Left Single Quotation Mark
# - U+02BC: Modifier Letter Apostrophe
# - U+02BB: Modifier Letter Turned Comma
# - U+02B9: Modifier Letter Prime
_APOSTROPHE_PATTERN = re.compile(r"[’‘ʼʻʹ]")

# Typographic eng (ŋ/Ŋ) used in older Dutch/Leiden printings of Zoetmulder (1982)
# for the velar nasal grapheme, unified to standard IAST/ISO n-dot-above (ṅ/Ṅ).
_ENG_TRANSLATION = str.maketrans({"ŋ": "ṅ", "Ŋ": "Ṅ"})

# Pepet with caron (ě/Ě) commonly typed in error due to keyboard layout limitations,
# unified to canonical Zoetmulder breve (ĕ/Ĕ).
_PEPET_CARON_TRANSLATION = str.maketrans({"ě": "ĕ", "Ě": "Ĕ"})
_ACRI_DAMAIS_TRANSLATION = str.maketrans({"v": "w"})


def normalize(
    text: str,
    *,
    normalize_whitespace: bool = True,
    canonicalize_eng: bool = True,
    canonicalize_pepet_caron: bool = True,
    canonicalize_apostrophes: bool = True,
    canonicalize_acri_damais: bool = True,
) -> NormalizationResult:
    """Normalize Old Javanese romanized text to canonical Unicode NFC and clean typography.

    This function is strictly orthographic and preserves all linguistic distinctions.
    It does NOT perform grapheme-to-phoneme conversion, aspirate merging, or vowel-length
    truncation.

    Args:
        text: Input string in romanized Old Javanese.
        normalize_whitespace: If True, collapses consecutive horizontal whitespace runs
            and non-breaking spaces into single ASCII spaces, and strips leading/trailing
            whitespace. Line breaks are preserved.
        canonicalize_eng: If True, maps typographic 'ŋ'/'Ŋ' (Latin letter eng, used in
            some Dutch printings) to standard IAST 'ṅ'/'Ṅ'. Note: ASCII 'ng' is NOT
            touched.
        canonicalize_pepet_caron: If True, maps 'ě'/'Ě' (caron) to canonical 'ĕ'/'Ĕ'
            (breve) to unify keyboard input variants of the pepet grapheme.
        canonicalize_apostrophes: If True, normalizes curly or modifier apostrophes
            (’, ‘, ʼ) to standard ASCII apostrophe (').
        canonicalize_acri_damais: If True, normalizes Acri/Damais variant 'v' to 'w'.

    Returns:
        NormalizationResult containing original text, normalized text, and recorded steps.
    """
    if not text:
        return NormalizationResult(
            original_text=text,
            normalized_text="",
            steps_applied=[],
        )

    steps: List[str] = []
    current = text

    # Step 1: Remove invisible formatting artifacts (BOM, soft hyphens, zero-width spaces)
    cleaned = _INVISIBLE_CHARS_PATTERN.sub("", current)
    if cleaned != current:
        steps.append("removed_invisible_characters")
        current = cleaned

    if canonicalize_acri_damais:
        acri_cleaned = current.translate(_ACRI_DAMAIS_TRANSLATION)
        if acri_cleaned != current:
            steps.append("canonicalized_acri_damais_v_to_w")
            current = acri_cleaned

    # Step 2: Canonicalize typographical apostrophes used in elision/sandhi
    if canonicalize_apostrophes:
        apos_cleaned = _APOSTROPHE_PATTERN.sub("'", current)
        if apos_cleaned != current:
            steps.append("canonicalized_apostrophes")
            current = apos_cleaned

    # Step 3: Unify single-grapheme typographic variants
    if canonicalize_eng:
        eng_cleaned = current.translate(_ENG_TRANSLATION)
        if eng_cleaned != current:
            steps.append("canonicalized_eng_to_n_dot_above")
            current = eng_cleaned

    if canonicalize_pepet_caron:
        caron_cleaned = current.translate(_PEPET_CARON_TRANSLATION)
        if caron_cleaned != current:
            steps.append("canonicalized_pepet_caron_to_breve")
            current = caron_cleaned

    # Step 4: Canonical Unicode Normalization (NFC)
    # Composes base letters and combining diacritics into precomposed characters
    # (e.g. a + \u0304 -> ā, t + \u0323 -> ṭ) and enforces canonical combining order.
    nfc = unicodedata.normalize("NFC", current)
    if nfc != current:
        steps.append("unicode_nfc")
        current = nfc

    # Step 5: Whitespace normalization
    if normalize_whitespace:
        # Normalize non-breaking and unusual Unicode spaces to standard space
        ws_cleaned = re.sub(r"[\u00a0\u1680\u2000-\u200a\u202f\u205f\u3000]", " ", current)
        # Collapse multiple horizontal spaces per line, stripping line extremities
        lines = ws_cleaned.splitlines()
        norm_lines = [re.sub(r"[^\S\r\n]+", " ", line).strip() for line in lines]
        # Re-join preserving line breaks, and strip overall
        ws_final = "\n".join(norm_lines).strip()
        if ws_final != current:
            steps.append("normalized_whitespace")
            current = ws_final

    return NormalizationResult(
        original_text=text,
        normalized_text=current,
        steps_applied=steps,
    )


def normalize_text(text: str, **kwargs) -> str:
    """Convenience wrapper around normalize() returning only the normalized string.

    Args:
        text: Input string in romanized Old Javanese.
        **kwargs: Optional keyword arguments forwarded to normalize().

    Returns:
        Normalized string.
    """
    return normalize(text, **kwargs).normalized_text


def convert_transliteration_convention(
    text: str,
    *,
    source_convention: str,
    target_convention: str,
) -> NormalizationResult:
    """Explicitly convert between distinct published romanization conventions.

    IMPORTANT: This function is separate from general Unicode normalization.
    Converting between scholarly conventions (e.g. Zoetmulder 1982 vs. Damais 1970 /
    Acri & Griffiths 2014) is an explicit editorial operation, not a default
    normalization step.

    Supported conventions:
    - 'zoetmulder': Uses 'ĕ' for short pepet, 'ö' for long pepet, 'w' for labial glide.
    - 'acri_damais': Uses 'ə' for short pepet, 'ə̄' for long pepet, 'v' for labial glide.

    Args:
        text: Input string to convert.
        source_convention: Source scheme ('zoetmulder' or 'acri_damais').
        target_convention: Target scheme ('zoetmulder' or 'acri_damais').

    Returns:
        NormalizationResult containing the converted string and step record.

    Raises:
        ValueError: If an unsupported convention is requested.
    """
    src = source_convention.lower()
    tgt = target_convention.lower()

    if src == tgt:
        return normalize(text)

    # First normalize input to canonical NFC
    base_res = normalize(text)
    current = base_res.normalized_text
    steps = list(base_res.steps_applied)

    if src == "acri_damais" and tgt == "zoetmulder":
        # Acri/Damais -> Zoetmulder
        # Map long schwa 'ə̄' (or 'ə' + macron) to 'ö'
        current = re.sub(r"ə[\u0304]|ə̄", "ö", current)
        current = re.sub(r"Ə[\u0304]|Ə̄", "Ö", current)
        # Map short schwa 'ə' to 'ĕ'
        current = current.replace("ə", "ĕ").replace("Ə", "Ĕ")
        # Map 'v' to 'w' (see RES-007, RES-010)
        current = current.replace("v", "w").replace("V", "W")
        steps.append("converted_acri_damais_to_zoetmulder")
    elif src == "zoetmulder" and tgt == "acri_damais":
        # Zoetmulder -> Acri/Damais
        current = current.replace("ö", "ə̄").replace("Ö", "Ə̄")
        current = current.replace("ĕ", "ə").replace("Ĕ", "Ə")
        current = current.replace("w", "v").replace("W", "V")
        steps.append("converted_zoetmulder_to_acri_damais")
    else:
        raise ValueError(
            f"Unsupported transliteration conversion from '{source_convention}' to '{target_convention}'. "
            "Supported values are 'zoetmulder' and 'acri_damais'."
        )

    # Ensure NFC on the final output
    nfc_final = unicodedata.normalize("NFC", current)
    return NormalizationResult(
        original_text=text,
        normalized_text=nfc_final,
        steps_applied=steps,
    )
