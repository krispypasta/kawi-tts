importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");

let pyodideReadyPromise;
let traceKawiFn;

async function initPyodide() {
    postMessage({ type: 'status', status: 'Loading Pyodide...' });
    let pyodide = await loadPyodide();

    postMessage({ type: 'status', status: 'Loading micropip...' });
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");

    postMessage({ type: 'status', status: 'Installing kawi-tts==1.1.2...' });
    await micropip.install("kawi-tts==1.1.2");

    postMessage({ type: 'status', status: 'Initializing engine...' });
    await pyodide.runPythonAsync(`
import json
from kawi_tts.normalization.normalizer import normalize_text
from kawi_tts.normalization.tokenizer import tokenize, TokenType
from kawi_tts.g2p.engine import g2p_word
from kawi_tts.acoustic.strategies import get_strategy
from kawi_tts.acoustic.mapper import AcousticMapper

def trace_kawi(text_in):
    try:
        norm = normalize_text(text_in)
        tokens = tokenize(norm)
        if not tokens:
            return json.dumps({"status": "EMPTY", "input": text_in})
        
        if any(t.has_ambiguity for t in tokens):
            reasons = [t.ambiguity_reason for t in tokens if t.has_ambiguity]
            return json.dumps({
                "status": "BLOCKED_AMBIGUITY",
                "input": text_in,
                "normalized": norm,
                "reasons": reasons
            })
        
        words = [t for t in tokens if t.token_type == TokenType.WORD]
        canon_list = [g2p_word(w.text) for w in words]
        canon_str = " | ".join(["-".join(c) for c in canon_list])
        
        strat_a = get_strategy("A")
        strat_b = get_strategy("B")
        
        prof_a = " | ".join(["-".join([strat_a.apply(t).target_token for t in c]) for c in canon_list])
        prof_b = " | ".join(["-".join([strat_b.apply(t).target_token for t in c]) for c in canon_list])
        
        map_a = AcousticMapper("A")
        map_b = AcousticMapper("B")
        
        res_a = map_a.map_phonemes(canon_list)
        res_b = map_b.map_phonemes(canon_list)
        
        return json.dumps({
            "status": "SUCCESS",
            "input": text_in,
            "normalized": norm,
            "tokens_count": len(tokens),
            "tokens": [{"type": t.token_type.name, "text": t.text} for t in tokens],
            "canonical": canon_str,
            "profile_a": prof_a,
            "profile_b": prof_b,
            "acoustic_a": res_a.backend_phoneme_string,
            "acoustic_b": res_b.backend_phoneme_string,
            "provisional_a": [
                {"internal": t.internal_token, "backend": t.backend_token, "status": t.status.name, "note": t.note}
                for w in res_a.mapped_words for t in w
                if t.status.name not in ("PRESERVED", "EVIDENCE_BACKED") and t.profiled_token
            ],
            "provisional_b": [
                {"internal": t.internal_token, "backend": t.backend_token, "status": t.status.name, "note": t.note}
                for w in res_b.mapped_words for t in w
                if t.status.name not in ("PRESERVED", "EVIDENCE_BACKED") and t.profiled_token
            ]
        })
    except Exception as e:
        import traceback
        return json.dumps({"status": "ERROR", "input": text_in, "error": str(e), "traceback": traceback.format_exc()})
    `);
    
    traceKawiFn = pyodide.globals.get("trace_kawi");
    postMessage({ type: 'status', status: 'Ready' });
}

pyodideReadyPromise = initPyodide().catch(err => {
    postMessage({ type: 'error', error: err.toString() });
    throw err;
});

self.onmessage = async (event) => {
    const { id, text } = event.data;
    try {
        await pyodideReadyPromise;
        if (!traceKawiFn) throw new Error("Trace function not initialized");
        
        const resultJson = traceKawiFn(text);
        const result = JSON.parse(resultJson);
        postMessage({ type: 'result', id, result });
    } catch (err) {
        postMessage({ type: 'result', id, result: { status: 'ERROR', error: err.toString(), input: text } });
    }
};
