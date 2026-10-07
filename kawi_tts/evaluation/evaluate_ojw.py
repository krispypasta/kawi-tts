"""Evaluation harness for testing Kawi-TTS front-end coverage against Old Javanese Wordnet (OJW).

Evaluates normalization, tokenization, G2P representation, and acoustic mapping
across all unique lexical items in OJW (wn-kaw.tab).

Produces comprehensive machine-readable metrics (JSON) and diagnostic reports.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from kawi_tts.acoustic.mapper import AcousticMapper, MappingStatus
from kawi_tts.g2p.engine import g2p_word
from kawi_tts.normalization.normalizer import normalize
from kawi_tts.normalization.tokenizer import TokenType, extract_words, tokenize


@dataclass
class OJWDatasetStats:
    """Raw counts and metrics for the parsed OJW dataset."""

    source_path: str
    sha256: str
    total_raw_lines: int
    header_lines: int
    data_rows: int
    unique_synsets: int
    unique_lemmas: int
    unique_variants: int
    unique_lexical_forms: int


@dataclass
class LexicalEvaluationResult:
    """Evaluation result for a single unique lexical form."""

    raw_form: str
    normalized_text: str
    normalization_steps: List[str]
    word_tokens: List[str]
    has_structural_ambiguity: bool
    ambiguity_reasons: List[str]
    is_multiword: bool
    g2p_phonemes: List[List[str]]
    backend_phoneme_string: str
    provisional_tokens: List[str]
    unsupported_tokens: List[str]
    failure_category: str  # "NONE", "UNSUPPORTED_GRAPHEME", "STRUCTURAL_AMBIGUITY", etc.


@dataclass
class OJWCoverageReport:
    """Comprehensive evaluation report covering all metrics and diagnostics."""

    dataset_stats: OJWDatasetStats
    total_evaluated: int
    normalization_success_count: int
    normalization_success_pct: float
    normalization_rule_frequencies: Dict[str, int]
    tokenization_clean_count: int
    tokenization_clean_pct: float
    multiword_count: int
    structural_ambiguity_count: int
    g2p_success_count: int
    g2p_success_pct: float
    acoustic_mapping_success_count: int
    acoustic_mapping_success_pct: float
    fully_supported_count: int
    fully_supported_pct: float
    forms_with_unsupported_chars: int
    unsupported_char_frequencies: Dict[str, int]
    forms_with_provisional_mappings: int
    provisional_token_count: int
    runtime_exceptions_count: int
    failure_categories_count: Dict[str, int]
    representative_failures: Dict[str, List[Dict[str, Any]]]
    feature_frequencies: Dict[str, int]


def load_ojw_dataset(file_path: str | Path) -> Tuple[OJWDatasetStats, List[str]]:
    """Parse wn-kaw.tab and extract unique deduplicated lexical forms.

    Args:
        file_path: Path to wn-kaw.tab file.

    Returns:
        Tuple of (OJWDatasetStats, sorted List of unique lexical form strings).
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"OJW dataset file not found at: {path}")

    content = path.read_bytes()
    file_sha256 = hashlib.sha256(content).hexdigest()

    lines = content.decode("utf-8").splitlines()
    header_count = 0
    data_rows = 0

    synsets: Set[str] = set()
    lemmas: Set[str] = set()
    variants: Set[str] = set()
    unique_forms: Set[str] = set()

    for line in lines:
        if line.startswith("#") or not line.strip():
            header_count += 1
            continue

        parts = line.split("\t")
        if len(parts) < 3:
            continue

        data_rows += 1
        synset_id = parts[0].strip()
        synsets.add(synset_id)

        lemma = parts[2].strip()
        if lemma:
            lemmas.add(lemma)
            unique_forms.add(lemma)

        if len(parts) >= 4 and parts[3].strip():
            for var in parts[3].split(","):
                clean_var = var.strip()
                if clean_var:
                    variants.add(clean_var)
                    unique_forms.add(clean_var)

    stats = OJWDatasetStats(
        source_path=str(path),
        sha256=file_sha256,
        total_raw_lines=len(lines),
        header_lines=header_count,
        data_rows=data_rows,
        unique_synsets=len(synsets),
        unique_lemmas=len(lemmas),
        unique_variants=len(variants),
        unique_lexical_forms=len(unique_forms),
    )

    return stats, sorted(unique_forms)


def evaluate_ojw(
    file_path: str | Path = "data/raw/wn-kaw.tab",
    output_json: str | Path = "data/processed/ojw_coverage_report.json",
) -> OJWCoverageReport:
    """Run full evaluation over all lexical forms in the OJW dataset.

    Args:
        file_path: Path to wn-kaw.tab.
        output_json: Path to save machine-readable JSON report.

    Returns:
        OJWCoverageReport instance.
    """
    stats, lexical_forms = load_ojw_dataset(file_path)
    mapper = AcousticMapper(profile="A")

    norm_success = 0
    norm_rule_freqs: Dict[str, int] = {}
    tok_clean = 0
    multiword_count = 0
    ambiguity_count = 0
    g2p_success = 0
    mapping_success = 0
    unsupported_char_freqs: Dict[str, int] = {}
    forms_with_unsupported = 0
    forms_with_provisional = 0
    total_provisional_tokens = 0
    runtime_exceptions = 0

    structural_buckets: Dict[str, List[Dict[str, Any]]] = {
        "MULTIWORD_OR_COMPOUND": [],
    }
    failure_buckets: Dict[str, List[Dict[str, Any]]] = {
        "UNSUPPORTED_GRAPHEME": [],
        "STRUCTURAL_AMBIGUITY": [],
        
        "DATA_NOISE_OR_MALFORMED": [],
        "PARSER_ERROR": [],
    }

    feature_counts: Dict[str, int] = {
        "long_vowels_ā_ī_ū": 0,
        "long_pepet_ö": 0,
        "pepet_ĕ_ə": 0,
        "retroflex_stops_ṭ_ḍ": 0,
        "retroflex_nasal_ṇ": 0,
        "sibilants_ś_ṣ": 0,
        "aspirates": 0,
        "vocalic_liquids_ṛ_ḷ": 0,
        "velar_nasal_ṅ_ŋ": 0,
        "palatal_nasal_ñ": 0,
    }

    aspirate_markers = ["bh", "dh", "gh", "ph", "kh", "ch", "jh", "ṭh", "ḍh"]

    for form in lexical_forms:
        fl = form.lower()
        if any(c in fl for c in "āīū"):
            feature_counts["long_vowels_ā_ī_ū"] += 1
        if "ö" in fl:
            feature_counts["long_pepet_ö"] += 1
        if "ĕ" in fl or "ə" in fl:
            feature_counts["pepet_ĕ_ə"] += 1
        if "ṭ" in fl or "ḍ" in fl:
            feature_counts["retroflex_stops_ṭ_ḍ"] += 1
        if "ṇ" in fl:
            feature_counts["retroflex_nasal_ṇ"] += 1
        if "ś" in fl or "ṣ" in fl:
            feature_counts["sibilants_ś_ṣ"] += 1
        if any(asp in fl for asp in aspirate_markers):
            feature_counts["aspirates"] += 1
        if "ṛ" in fl or "ḷ" in fl:
            feature_counts["vocalic_liquids_ṛ_ḷ"] += 1
        if "ṅ" in fl or "ŋ" in fl:
            feature_counts["velar_nasal_ṅ_ŋ"] += 1
        if "ñ" in fl:
            feature_counts["palatal_nasal_ñ"] += 1

        # 1. Normalization
        try:
            norm_res = normalize(form)
            norm_success += 1
            for step in norm_res.steps_applied:
                norm_rule_freqs[step] = norm_rule_freqs.get(step, 0) + 1
        except Exception as e:
            runtime_exceptions += 1
            failure_buckets["PARSER_ERROR"].append({"form": form, "stage": "normalization", "error": str(e)})
            continue

        # 2. Tokenization
        try:
            tokens = tokenize(norm_res.normalized_text)
            has_ambig = any(t.has_ambiguity for t in tokens)
            words = extract_words(tokens)

            if has_ambig:
                ambiguity_count += 1
                reasons = [t.ambiguity_reason for t in tokens if t.has_ambiguity and t.ambiguity_reason]
                failure_buckets["STRUCTURAL_AMBIGUITY"].append({"form": form, "reasons": reasons})
            else:
                tok_clean += 1

            if len(words) > 1:
                multiword_count += 1
                structural_buckets["MULTIWORD_OR_COMPOUND"].append({"form": form, "words": words})
        except Exception as e:
            runtime_exceptions += 1
            failure_buckets["PARSER_ERROR"].append({"form": form, "stage": "tokenization", "error": str(e)})
            continue

        # 3. G2P
        try:
            phonemes_per_word = [g2p_word(w) for w in words]
            g2p_success += 1
        except Exception as e:
            runtime_exceptions += 1
            failure_buckets["PARSER_ERROR"].append({"form": form, "stage": "g2p", "error": str(e)})
            continue

        # 4. Acoustic Mapping
        try:
            map_res = mapper.map_phonemes(phonemes_per_word)
            mapping_success += 1

            if map_res.provisional_mappings:
                forms_with_provisional += 1
                total_provisional_tokens += len(map_res.provisional_mappings)

            if map_res.unsupported_tokens:
                forms_with_unsupported += 1
                unsupp_tokens = [u.internal_token for u in map_res.unsupported_tokens]
                for u in unsupp_tokens:
                    unsupported_char_freqs[u] = unsupported_char_freqs.get(u, 0) + 1
                failure_buckets["UNSUPPORTED_GRAPHEME"].append({
                    "form": form,
                    "unsupported_tokens": unsupp_tokens,
                })
        except Exception as e:
            runtime_exceptions += 1
            failure_buckets["PARSER_ERROR"].append({"form": form, "stage": "acoustic_mapping", "error": str(e)})
            continue

    total_forms = len(lexical_forms)
    fully_supported = total_forms - forms_with_unsupported

    # Representative failures (capped at 10 items per category)
    rep_failures = {
        cat: items[:10] for cat, items in failure_buckets.items() if items
    }

    report = OJWCoverageReport(
        dataset_stats=stats,
        total_evaluated=total_forms,
        normalization_success_count=norm_success,
        normalization_success_pct=(norm_success / total_forms * 100) if total_forms else 0.0,
        normalization_rule_frequencies=norm_rule_freqs,
        tokenization_clean_count=tok_clean,
        tokenization_clean_pct=(tok_clean / total_forms * 100) if total_forms else 0.0,
        multiword_count=multiword_count,
        structural_ambiguity_count=ambiguity_count,
        g2p_success_count=g2p_success,
        g2p_success_pct=(g2p_success / total_forms * 100) if total_forms else 0.0,
        acoustic_mapping_success_count=mapping_success,
        acoustic_mapping_success_pct=(mapping_success / total_forms * 100) if total_forms else 0.0,
        fully_supported_count=fully_supported,
        fully_supported_pct=(fully_supported / total_forms * 100) if total_forms else 0.0,
        forms_with_unsupported_chars=forms_with_unsupported,
        unsupported_char_frequencies=unsupported_char_freqs,
        forms_with_provisional_mappings=forms_with_provisional,
        provisional_token_count=total_provisional_tokens,
        runtime_exceptions_count=runtime_exceptions,
        failure_categories_count={cat: len(items) for cat, items in failure_buckets.items()},
        representative_failures=rep_failures,
        feature_frequencies=feature_counts,
    )

    out_path = Path(output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)

    return report


if __name__ == "__main__":
    report = evaluate_ojw()
    print("OJW Evaluation Complete.")
    print(f"Total Unique Lexical Forms: {report.total_evaluated}")
    print(f"Fully Supported: {report.fully_supported_count} ({report.fully_supported_pct:.2f}%)")
    print(f"Forms with Unsupported Chars: {report.forms_with_unsupported_chars}")
    print(f"Unsupported Characters: {report.unsupported_char_frequencies}")
    print(f"Provisional Forms: {report.forms_with_provisional_mappings}")
    print(f"Runtime Exceptions: {report.runtime_exceptions_count}")
