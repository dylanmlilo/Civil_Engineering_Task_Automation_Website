(function() {
    document.addEventListener('DOMContentLoaded', function() {

        const sewerForm = document.getElementById("sewer_pipe_size_calculator-form");
        if (!sewerForm) {
            return;
        }

        if (!window.fetch || !window.Promise) {
            alert("This browser doesn't support required features. Please use a modern browser.");
            return;
        }

        sewerForm.addEventListener("submit", async function(e) {
            e.preventDefault();
        
            const submitBtn = e.target.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = "Calculating...";
        
            try {
                // Validate inputs
                const population = parseFloat(document.getElementById("sewer-population").value);
                const per_capita_flow = parseFloat(document.getElementById("sewer-per-capita-flow").value);
                const slope = parseFloat(document.getElementById("sewer-slope").value);
                const n = parseFloat(document.getElementById("sewer-pipe-type").value);
                const diameter = parseFloat(document.getElementById("sewer-diameter").value);
                const flow_ratio = parseFloat(document.getElementById("sewer-flow-ratio").value);
        
                if (isNaN(population) || isNaN(per_capita_flow) || 
                   isNaN(slope) || isNaN(n) || isNaN(diameter) || isNaN(flow_ratio)) {
                    throw new Error("Please enter valid numbers in all fields");
                }
        
                const formData = {
                    population,
                    per_capita_flow,
                    slope,
                    n,
                    diameter,
                    flow_ratio
                };
        
                // Single API call
                const response = await fetch("/api/sewer/sewer_pipe_sizing", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(formData)
                });
        
                // Validate response ONCE
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText || "Calculation failed");
                }
        
                const results = await response.json();
                
                // Validate results structure
                if (!results || typeof results !== "object") {
                    throw new Error("Invalid response format");
                }
        
                // Single display call
                displayResults(results);
        
            } catch (error) {
                console.error("Error:", error);
                alert("Calculation failed: " + error.message);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            }
        });
    
        function displayResults(data) {
            console.log("Displaying sewer pipe size results:", data);
            const resultsDiv = document.getElementById("sewer-results");
            const resultItems = document.getElementById("sewer-result-items");
            
            if (!resultsDiv || !resultItems) {
                console.error("Results display elements not found");
                alert("Error: Cannot display results. Page elements missing.");
                return;
            }
            
            resultItems.innerHTML = `
            <div class="result-item">
                <span class="result-label">Peak Factor:</span>
                <span class="result-value">${(data.peak_factor ?? 0).toFixed(3)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Demand (m³/s):</span>
                <span class="result-value">${(data.demand_ms ?? 0).toFixed(5)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Pipe Capacity (m³/s):</span>
                <span class="result-value">${(data.capacity ?? 0).toFixed(5)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Velocity (m/s):</span>
                <span class="result-value">${(data.velocity ?? 0).toFixed(3)}</span>
            </div>
            <div class="result notes">
                {{if }}
            </div>
            `;

            resultItems.innerHTML = `
            <div class="result-item">
                <span class="result-label">Peak Factor:</span>
                <span class="result-value">${(data.peak_factor ?? 0).toFixed(3)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Demand (m³/s):</span>
                <span class="result-value">${(data.demand_ms ?? 0).toFixed(5)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Pipe Capacity (m³/s):</span>
                <span class="result-value">${(data.capacity ?? 0).toFixed(5)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Velocity (m/s):</span>
                <span class="result-value">${(data.velocity ?? 0).toFixed(3)}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Flow Depth (m):</span>
                <span class="result-value">${(data.flow_depth ?? 0).toFixed(3)}</span>
                <span class="result-note ${data.flow_depth/data.diameter > 0.81 ? 'warning' : ''}">
                    ${data.flow_depth/data.diameter > 0.81 ? '⚠️ Exceeds 80% depth - risk of surcharge' : '✓ ' + (data.flow_depth/data.diameter).toFixed(2) + ' of pipe height'}
                </span>
            </div>
            <div class="design-notes">
                <h4>Design Checks:</h4>
                <ul>
                    <li class="${data.velocity < 0.6 ? 'warning' : 'pass'}">
                        Self-cleansing: ${data.velocity < 0.6 ? 'FAIL (V < 0.6 m/s)' : 'PASS'}
                    </li>
                    <li class="${data.velocity > 3.0 ? 'warning' : 'pass'}">
                        Erosion check: ${data.velocity > 3.0 ? 'FAIL (V > 3.0 m/s)' : 'PASS'}
                    </li>
                    <li class="${(data.demand_ms/data.capacity) > 0.8 ? 'warning' : 'pass'}">
                        Capacity: ${(data.demand_ms/data.capacity) > 0.8 ? '>80% utilized' : 'Adequate'}
                    </li>
                </ul>
            </div>
            `;

            
            resultsDiv.style.display = "block";
        }
    });
})();