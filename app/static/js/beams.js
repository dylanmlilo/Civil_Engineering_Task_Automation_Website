(function() {
    document.addEventListener("DOMContentLoaded", function() {
        
        const beamForm = document.getElementById("beam-form");
        if (!beamForm) {
            return;
        }

        // Check for required browser features
        if (!window.fetch || !window.Promise) {
            alert("This browser doesn't support required features. Please use a modern browser.");
            return;
        }

        beamForm.addEventListener("submit", async function(e) {
            e.preventDefault();

            // Show loading state
            const submitBtn = e.target.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = "Calculating...";

            try {
                // Validate form inputs before processing
                const span = parseFloat(document.getElementById("span").value);
                const width = parseFloat(document.getElementById("width").value);
                const depth = parseFloat(document.getElementById("depth").value);
                const roofLevel = parseFloat(document.getElementById("roof_level").value);
                const windowLevel = parseFloat(document.getElementById("window_level").value);
                const additionalDeadLoad = parseFloat(document.getElementById("additional_dead_load").value);
                const liveLoad = parseFloat(document.getElementById("live_load").value);

                if (isNaN(span) || isNaN(width) || isNaN(depth) || 
                    isNaN(roofLevel) || isNaN(windowLevel) || 
                    isNaN(additionalDeadLoad) || isNaN(liveLoad)) {
                    throw new Error("Please enter valid numbers in all fields");
                }

                const formData = {
                    span: span,
                    width: width,
                    depth: depth,
                    include_self_weight: document.getElementById("include_self_weight").value === "true",
                    roof_level: roofLevel,
                    window_level: windowLevel,
                    additional_dead_load: additionalDeadLoad,
                    live_load: liveLoad,
                    point_loads: [] // Future feature
                };

                
                const response = await fetch("/api/beams/calculate-loads", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(formData)
                });
                
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText || "Calculation failed");
                }
                
                const results = await response.json();
                console.log("Received beam calculation results:", results);
                
                // Validate response structure
                if (!results || typeof results !== "object") {
                    throw new Error("Invalid response format from server");
                }

                // Display results
                displayResults(results);

            } catch (error) {
                console.error("Beam calculation error:", error);
                alert("Error: " + error.message);
            } finally {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            }
        });

        function displayResults(data) {
            console.log("Displaying beam results:", data);
            
            const resultsDiv = document.getElementById("results");
            const resultItems = document.getElementById("result-items");
            
            if (!resultsDiv || !resultItems) {
                console.error("Beam results display elements not found");
                alert("Error: Cannot display results. Page elements missing.");
                return;
            }
            
            // Safely display results with fallback values
            resultItems.innerHTML = `
                <div class="result-item">
                    <span class="result-label">Self Weight:</span>
                    <span class="result-value">${(data.self_weight ?? 0).toFixed(3)} kN/m</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Total Dead Load:</span>
                    <span class="result-value">${(data.total_dead_load ?? 0).toFixed(3)} kN/m</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Factored Load:</span>
                    <span class="result-value">${(data.factored_load ?? 0).toFixed(3)} kN/m</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Max Moment:</span>
                    <span class="result-value">${(data.max_moment_factored ?? 0).toFixed(3)} kNm</span>
                </div>
                ${data.additional_results ? `
                <div class="result-item">
                    <span class="result-label">Additional Results:</span>
                    <span class="result-value">${data.additional_results}</span>
                </div>
                ` : ''}
            `;
            
            resultsDiv.style.display = "block";
            console.log("Beam results displayed successfully");
        }
    });
})();