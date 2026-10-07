import argparse
import sys

from kawi_tts.g2p.engine import _MONOGRAPH_MAP, _DIGRAPH_MAP
from kawi_tts.acoustic.strategies import get_strategy
from kawi_tts.acoustic.strategies.base import PolicyStatus

def run_coverage_report():
    print("=" * 60)
    print("KAWI-TTS PHONEME COVERAGE REPORT")
    print("=" * 60)
    
    # Collect all canonical phonemes
    canonical_phonemes = set(_MONOGRAPH_MAP.values()).union(set(_DIGRAPH_MAP.values()))
    
    # Sort them for deterministic output
    canonical_phonemes = sorted(list(canonical_phonemes))
    
    strat_a = get_strategy("A")
    strat_b = get_strategy("B")
    
    def status_to_str(status: PolicyStatus) -> str:
        if status == PolicyStatus.PRESERVED:
            return "SUPPORTED"
        elif status == PolicyStatus.PROVISIONAL_RECONSTRUCTION:
            return "PROVISIONAL"
        elif status == PolicyStatus.UNRESOLVED:
            return "UNRESOLVED"
        elif status == PolicyStatus.UNSUPPORTED:
            return "UNSUPPORTED"
        elif status == PolicyStatus.EVIDENCE_BACKED:
            return "SUPPORTED (Merged)"
        return "UNKNOWN"
        
    print(f"{'Canonical':<12} | {'Profile A Target':<18} | {'Profile A Status':<20} | {'Profile B Target':<18} | {'Profile B Status'}")
    print("-" * 95)
    
    for cp in canonical_phonemes:
        pa = strat_a.apply(cp)
        pb = strat_b.apply(cp)
        
        sa_str = status_to_str(pa.status)
        sb_str = status_to_str(pb.status)
        
        print(f"{cp:<12} | {pa.target_token:<18} | {sa_str:<20} | {pb.target_token:<18} | {sb_str}")
        
    print("-" * 95)
    print("Note: 'SUPPORTED' indicates the backend explicitly handles the token.")
    print("      'PROVISIONAL' indicates an engineered fallback (no historical claim).")
    print("      'UNSUPPORTED' indicates the token falls through untouched (unsafe).")
    print("      'UNRESOLVED' indicates architectural deferment (e.g. vowel length).")
    print("=" * 60)

if __name__ == "__main__":
    run_coverage_report()
