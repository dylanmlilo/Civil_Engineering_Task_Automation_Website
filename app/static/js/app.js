// DOM Elements
const app = document.getElementById('app');

// Routes
const routes = {
    '/beam-calculator': renderBeamCalculator,
};

// Initial load
window.onload = () => {
    navigate('/home');
};

// Navigation
function navigate(path) {
    window.history.pushState({}, path, path);
    routes[path]();
}

// Beam Calculator
function loadBeamCalculator() {
    navigate('/beam-calculator');
}

function renderBeamCalculator() {
    app.innerHTML = `
        <h2>Beam Load Calculator</h2>
        <form id="beam-form">
            <label>Span (m): <input type="number" name="span" step="0.1" required></label>
            <label>Width (mm): <input type="number" name="width" required></label>
            <label>Depth (mm): <input type="number" name="depth" required></label>
            <label>Depth (mm): <input type="number" name="depth" required></label>
            <label>Depth (mm): <input type="number" name="depth" required></label>
            <label>Depth (mm): <input type="number" name="depth" required></label>
            <button type="submit">Calculate</button>
        </form>
        <div id="results"></div>
    `;

    document.getElementById('beam-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = getFormData(e.target);
        const results = await calculateBeamLoads(formData);
        displayResults(results);
    });
}

async function calculateBeamLoads(data) {
    try {
        const response = await fetch('/api/beams/calculate-loads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return { error: error.message };
    }
}

function getFormData(form) {
    return {
        span: parseFloat(form.span.value),
        width: parseInt(form.width.value),
        depth: parseInt(form.depth.value),
        include_self_weight: true,
        additional_dead_load: 0,
        live_load: 0,
        point_loads: []
    };
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    if (data.error) {
        resultsDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
    } else {
        resultsDiv.innerHTML = `
            <h3>Results</h3>
            <p>Total Dead Load: ${data.total_dead_load.toFixed(2)} kN/m</p>
            <p>Factored Load: ${data.factored_load.toFixed(2)} kN/m</p>
            <p>Max Moment: ${data.max_moment_factored.toFixed(2)} kNm</p>
        `;
    }
}