let pointLoads = [];

function addPointLoad() {
    const container = document.getElementById('point-loads');
    const div = document.createElement('div');
    div.className = 'point-load';
    div.innerHTML = `
        <label>Magnitude (kN): <input type="number" class="point-magnitude" step="0.1" min="0" value="10"></label>
        <label>Position (m): <input type="number" class="point-position" step="0.1" min="0" value="2.5"></label>
        <button type="button" onclick="this.parentNode.remove()">Remove</button>
    `;
    container.appendChild(div);
}

function getFormData() {
    // Get point loads
    pointLoads = [];
    document.querySelectorAll('.point-load').forEach(load => {
        pointLoads.push({
            magnitude: parseFloat(load.querySelector('.point-magnitude').value),
            position: parseFloat(load.querySelector('.point-position').value)
        });
    });

    return {
        span: parseFloat(document.getElementById('span').value),
        width: parseInt(document.getElementById('width').value),
        depth: parseInt(document.getElementById('depth').value),
        include_self_weight: document.getElementById('include_self_weight').value === 'true',
        roof_level: parseFloat(document.getElementById('roof_level').value),
        window_level: parseFloat(document.getElementById('window_level').value),
        additional_dead_load: parseFloat(document.getElementById('additional_dead_load').value),
        live_load: parseFloat(document.getElementById('live_load').value),
        point_loads: pointLoads.map(load => ({
            magnitude: load.magnitude,
            position: load.position
        }))
    };
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const resultItems = document.getElementById('result-items');
    
    resultItems.innerHTML = `
        <div class="result-item"><strong>Self Weight:</strong> ${data.self_weight.toFixed(3)} kN/m</div>
        <div class="result-item"><strong>Wall Dead Load:</strong> ${data.wall_dead_load.toFixed(3)} kN/m</div>
        <div class="result-item"><strong>Total Dead Load:</strong> ${data.total_dead_load.toFixed(3)} kN/m</div>
        <div class="result-item"><strong>Factored Dead Load:</strong> ${data.factored_dead_load.toFixed(3)} kN/m</div>
        <div class="result-item"><strong>Factored Live Load:</strong> ${data.factored_live_load.toFixed(3)} kN/m</div>
        <div class="result-item"><strong>Service Load:</strong> ${data.service_load.toFixed(3)} kN/m</div>
        <div class="result-item"><strong>Factored Load:</strong> ${data.factored_load.toFixed(3)} kN/m</div>
        <div class="result-item"><strong>Dead Load Reactions:</strong> ${data.dead_load_reactions.toFixed(3)} kN</div>
        <div class="result-item"><strong>Live Load Reactions:</strong> ${data.live_load_reactions.toFixed(3)} kN</div>
        <div class="result-item"><strong>Service Load Reactions:</strong> ${data.service_load_reactions.toFixed(3)} kN</div>
        <div class="result-item"><strong>Factored Load Reactions:</strong> ${data.factored_load_reactions.toFixed(3)} kN</div>
        <div class="result-item"><strong>Max Moment (Service):</strong> ${data.max_moment_service.toFixed(3)} kNm</div>
        <div class="result-item"><strong>Max Moment (Factored):</strong> ${data.max_moment_factored.toFixed(3)} kNm</div>
        <div class="result-item"><strong>Total Point Load:</strong> ${data.total_point_load ? data.total_point_load.toFixed(3) : '0'} kN</div>
    `;
    
    resultsDiv.style.display = 'block';
}

async function calculate() {
    const formData = getFormData();
    
    try {
        const response = await fetch('/api/beams/calculate-loads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Calculation failed: ' + error.message);
    }
}

// Add one point load by default when page loads
window.onload = addPointLoad;