"""Text-structure and tokenization layer for Old Javanese (Kawi) texts.

This module provides deterministic, lossless text tokenization that classifies
words, punctuation, line breaks, explicit boundaries (hyphens), elision marks,
and numbers, while detecting unresolved structural ambiguities (such as 'sanghyang')
without performing phonological interpretation or sandhi assimilation.

Linguistic Policy (see AGENTS.md, docs/DECISIONS.md, and docs/RESEARCH_LOG.md):
- INFORMATION PRESERVATION FIRST: Source text is never discarded or mutated.
- TEXT STRUCTURE MUST NOT INVENT PRONUNCIATION: Word boundaries are not guessed.
- Ambiguous sequences (e.g. ASCII 'ngh' in un-hyphenated 'sanghyang') are flagged
  as UNRESOLVED rather than silently resolved with arbitrary heuristics.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TokenType(Enum):
    """Classification of text tokens in Old Javanese orthography."""

    WORD = "word"                  # Unambiguous lexical word token (e.g., "sĕkar", "bhaṭāra")
    PUNCTUATION = "punctuation"    # Punctuation mark (e.g., ",", ".", "!", "?", ";", danda "||")
    BOUNDARY = "boundary"          # Explicit structural / compound boundary (e.g., "-")
    ELISION = "elision"            # Apostrophe / sandhi elision marker (e.g., "'")
    NUMBER = "number"              # Numerical string (e.g., "183", "2")
    WHITESPACE = "whitespace"      # Horizontal whitespace (spaces, tabs)
    NEWLINE = "newline"            # Line breaks ("\n", "\r\n")
    UNRESOLVED = "unresolved"      # Token with unresolved structural ambiguity (e.g., "sanghyang")


@dataclass(frozen=True)
class Token:
    """Represents a discrete structural unit in the text with provenance and offset bounds.

    Attributes:
        text: Verbatim substring from the source text.
        token_type: Structural classification of the token.
        start: Zero-based start character offset in the source text.
        end: Zero-based end character offset in the source text.
        has_ambiguity: Boolean flag indicating if the token contains unresolved ambiguities.
        ambiguity_reason: Descriptive diagnosis if the token is structurally ambiguous.
    """

    text: str
    token_type: TokenType
    start: int
    end: int
    has_ambiguity: bool = False
    ambiguity_reason: Optional[str] = None


def is_word_codepoint(char: str) -> bool:
    """Check if a character is a Unicode letter or combining mark."""
    cat = unicodedata.category(char)
    return cat.startswith("L") or cat.startswith("M")


def is_boundary_codepoint(char: str) -> bool:
    """Check if a character is an explicit compound or morpheme boundary marker."""
    return char in "-·‐‑"


def is_elision_codepoint(char: str) -> bool:
    """Check if a character is an apostrophe or elision marker."""
    return char in "'’‘ʼʻʹ"


def check_word_ambiguity(word: str) -> tuple[bool, Optional[str]]:
    """Inspect a lexical token for structural ambiguities.

    Specifically flags clusters like 'ngh' where ASCII digraph representations
    (e.g., 'ng' for /ŋ/) conflict with Sanskrit aspirates (e.g., 'gh' for /gʱ/) in the
    absence of explicit boundary markers (hyphens) or canonical orthography ('saṅhyaṅ').
    """
    w_lower = word.lower()
    if "ngh" in w_lower:
        return (
            True,
            "Ambiguous cluster 'ngh': conflict between ASCII velar nasal 'ng' and "
            "Sanskrit aspirate 'gh' without explicit boundary or canonical 'ṅ'.",
        )
    return False, None


def tokenize(text: str) -> List[Token]:
    """Deterministically segment text into structured tokens without altering content.

    Guarantees:
    - 100% lossless: "".join(t.text for t in tokens) == text
    - Exact character offsets: text[t.start:t.end] == t.text
    - Explicit boundaries (e.g. hyphens) split compound words so G2P does not
      falsely merge characters across boundary lines.
    - Structural ambiguities (e.g., 'sanghyang') are flagged as TokenType.UNRESOLVED.

    Args:
        text: Source text (normalized or raw).

    Returns:
        List of Token objects in left-to-right reading order.
    """
    tokens: List[Token] = []
    i = 0
    n = len(text)

    while i < n:
        c = text[i]
        start = i

        # 1. Line boundaries
        if c == "\r":
            if i + 1 < n and text[i + 1] == "\n":
                tokens.append(Token(text="\r\n", token_type=TokenType.NEWLINE, start=start, end=i + 2))
                i += 2
            else:
                tokens.append(Token(text="\r", token_type=TokenType.NEWLINE, start=start, end=i + 1))
                i += 1
            continue
        if c == "\n":
            tokens.append(Token(text="\n", token_type=TokenType.NEWLINE, start=start, end=i + 1))
            i += 1
            continue

        # 2. Horizontal whitespace
        if c in " \t\v\f" or unicodedata.category(c) == "Zs":
            while i < n and (text[i] in " \t\v\f" or unicodedata.category(text[i]) == "Zs"):
                i += 1
            tokens.append(Token(text=text[start:i], token_type=TokenType.WHITESPACE, start=start, end=i))
            continue

        # 3. Explicit boundary markers (hyphens, middle dots)
        if is_boundary_codepoint(c):
            tokens.append(Token(text=c, token_type=TokenType.BOUNDARY, start=start, end=i + 1))
            i += 1
            continue

        # 4. Elision / apostrophe markers
        if is_elision_codepoint(c):
            tokens.append(Token(text=c, token_type=TokenType.ELISION, start=start, end=i + 1))
            i += 1
            continue

        # 5. Numerals
        if c.isdigit() or unicodedata.category(c).startswith("N"):
            while i < n and (text[i].isdigit() or unicodedata.category(text[i]).startswith("N")):
                i += 1
            tokens.append(Token(text=text[start:i], token_type=TokenType.NUMBER, start=start, end=i))
            continue

        # 6. Lexical words and unresolved sequences
        if is_word_codepoint(c):
            while i < n and is_word_codepoint(text[i]):
                i += 1
            word_str = text[start:i]
            is_ambig, reason = check_word_ambiguity(word_str)
            t_type = TokenType.UNRESOLVED if is_ambig else TokenType.WORD
            tokens.append(
                Token(
                    text=word_str,
                    token_type=t_type,
                    start=start,
                    end=i,
                    has_ambiguity=is_ambig,
                    ambiguity_reason=reason,
                )
            )
            continue

        # 7. Punctuation / danda / symbols
        # Group adjacent dandas (e.g. '||') into single punctuation token
        if c == "|":
            while i < n and text[i] == "|":
                i += 1
            tokens.append(Token(text=text[start:i], token_type=TokenType.PUNCTUATION, start=start, end=i))
            continue

        tokens.append(Token(text=c, token_type=TokenType.PUNCTUATION, start=start, end=i + 1))
        i += 1

    return tokens


def extract_words(tokens: List[Token], *, include_unresolved: bool = True) -> List[str]:
    """Convenience utility to extract text strings of words for downstream processing.

    Args:
        tokens: Sequence of Token objects.
        include_unresolved: If True, includes tokens classified as UNRESOLVED.

    Returns:
        List of lexical word strings.
    """
    valid_types = {TokenType.WORD, TokenType.UNRESOLVED} if include_unresolved else {TokenType.WORD}
    return [t.text for t in tokens if t.token_type in valid_types]


def get_ambiguities(tokens: List[Token]) -> List[Token]:
    """Filter and return all tokens containing structural ambiguities.

    Args:
        tokens: Sequence of Token objects.

    Returns:
        List of Token objects where has_ambiguity is True.
    """
    return [t for t in tokens if t.has_ambiguity]
