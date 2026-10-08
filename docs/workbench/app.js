const worker = new Worker('worker.js');

const els = {
    status: document.getElementById('status-text'),
    statusContainer: document.getElementById('status-container'),
    input: document.getElementById('kawi-input'),
    analyzeBtn: document.getElementById('analyze-btn'),
    clearBtn: document.getElementById('clear-btn'),
    results: document.getElementById('results-panel'),
    error: document.getElementById('error-box'),
    errorText: document.getElementById('error-text'),
    ambiguity: document.getElementById('ambiguity-box'),
    ambiguityText: document.getElementById('ambiguity-text'),
    
    // Trace elements
    norm: document.getElementById('res-norm'),
    tok: document.getElementById('res-tok'),
    canon: document.getElementById('res-canon'),
    
    profA: document.getElementById('res-prof-a'),
    acousA: document.getElementById('res-acous-a'),
    provA: document.getElementById('prov-a'),
    
    profB: document.getElementById('res-prof-b'),
    acousB: document.getElementById('res-acous-b'),
    provB: document.getElementById('prov-b'),
};

let isReady = false;
let isRunning = false;
let currentMsgId = 0;
const pendingResolvers = new Map();

function updateStatus(state, msg) {
    els.status.textContent = msg;
    els.statusContainer.className = '';
    els.statusContainer.classList.add(`status-${state}`);
    
    if (state === 'ready') {
        isReady = true;
        els.analyzeBtn.disabled = isRunning || els.input.value.trim() === '';
    } else if (state === 'error') {
        isReady = false;
        els.analyzeBtn.disabled = true;
    }
}

worker.onmessage = function(e) {
    const data = e.data;
    if (data.type === 'status') {
        if (data.status === 'Ready') {
            updateStatus('ready', 'Engine Ready (kawi-tts==1.1.2)');
        } else {
            updateStatus('loading', data.status);
        }
    } else if (data.type === 'error') {
        updateStatus('error', 'Initialization Failed');
        showError(data.error);
    } else if (data.type === 'result') {
        const resolver = pendingResolvers.get(data.id);
        if (resolver) {
            resolver(data.result);
            pendingResolvers.delete(data.id);
        }
    }
};

worker.onerror = function(err) {
    updateStatus('error', 'Worker Error');
    showError(err.message || 'Fatal Worker Error');
    for (const [id, resolve] of pendingResolvers) {
        resolve({ status: 'ERROR', error: 'Worker crashed' });
    }
    pendingResolvers.clear();
    isRunning = false;
    els.analyzeBtn.disabled = true;
    els.analyzeBtn.textContent = "Analyze";
};

function showError(msg) {
    els.errorText.textContent = msg;
    els.error.classList.remove('hidden');
    els.results.classList.add('hidden');
    els.ambiguity.classList.add('hidden');
}

function renderProvenance(container, provList) {
    container.innerHTML = '';
    if (!provList || provList.length === 0) return;
    
    provList.forEach(p => {
        const li = document.createElement('li');
        let badgeClass = 'badge-recon';
        if (p.status.includes('PROVISIONAL')) badgeClass = 'badge-prov';
        
        const badge = document.createElement('span');
        badge.className = `badge ${badgeClass}`;
        badge.textContent = p.status;
        
        const strong = document.createElement('strong');
        strong.textContent = `${p.internal} \u2192 ${p.backend}`;
        
        li.appendChild(badge);
        li.appendChild(document.createElement('br'));
        li.appendChild(strong);
        li.appendChild(document.createTextNode(`: ${p.note}`));
        container.appendChild(li);
    });
}

async function analyze() {
    const text = els.input.value.trim();
    if (!text || !isReady || isRunning) return;
    
    isRunning = true;
    els.analyzeBtn.disabled = true;
    els.analyzeBtn.textContent = "Analyzing...";
    els.error.classList.add('hidden');
    els.ambiguity.classList.add('hidden');
    els.results.classList.add('hidden');
    
    currentMsgId++;
    const msgId = currentMsgId;
    
    const promise = new Promise(resolve => {
        pendingResolvers.set(msgId, resolve);
    });
    
    worker.postMessage({ id: msgId, text });
    
    try {
        const result = await promise;
        if (msgId !== currentMsgId) return;
        
        if (result.status === 'ERROR') {
            showError(result.error || "Unknown Python Error");
        } else if (result.status === 'EMPTY') {
            showError("Input evaluated to empty tokens.");
        } else if (result.status === 'BLOCKED_AMBIGUITY') {
            els.ambiguityText.textContent = result.reasons.join(" | ");
            els.ambiguity.classList.remove('hidden');
        } else if (result.status === 'SUCCESS') {
            els.norm.textContent = result.normalized;
            els.tok.textContent = result.tokens.map(t => `[${t.type}: ${t.text}]`).join(' ');
            els.canon.textContent = result.canonical;
            
            els.profA.textContent = result.profile_a;
            els.acousA.textContent = result.acoustic_a;
            renderProvenance(els.provA, result.provisional_a);
            
            els.profB.textContent = result.profile_b;
            els.acousB.textContent = result.acoustic_b;
            renderProvenance(els.provB, result.provisional_b);
            
            els.results.classList.remove('hidden');
        }
    } catch (e) {
        if (msgId !== currentMsgId) return;
        showError(e.toString());
    } finally {
        if (msgId === currentMsgId) {
            isRunning = false;
            els.analyzeBtn.disabled = (els.input.value.trim() === '');
            els.analyzeBtn.textContent = "Analyze";
        }
    }
}

els.analyzeBtn.addEventListener('click', analyze);

els.input.addEventListener('input', () => {
    if (isReady && !isRunning) {
        els.analyzeBtn.disabled = els.input.value.trim() === '';
    }
});

els.input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        analyze();
    }
});

    els.clearBtn.addEventListener('click', () => {
    currentMsgId++;
    isRunning = false;
    els.analyzeBtn.textContent = "Analyze";
    
    els.input.value = '';
    els.analyzeBtn.disabled = true;
    els.results.classList.add('hidden');
    els.error.classList.add('hidden');
    els.ambiguity.classList.add('hidden');
    els.input.focus();
});

document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        els.input.value = btn.dataset.text;
        els.analyzeBtn.disabled = !isReady || isRunning;
        if (isReady && !isRunning) analyze();
    });
});
