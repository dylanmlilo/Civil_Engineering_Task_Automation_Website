(function() {
    document.addEventListener("DOMContentLoaded", function() {
        console.log("DOMContentLoaded event fired for sewer page.");

        const sewerForm = document.getElementById("sewer-calculator-form");
        if (!sewerForm) {
            console.error("Sewer form element with ID 'sewer-calculator-form' not found!");
            return;
        }

        console.log("Sewer form element found. Attaching submit listener.");

        sewerForm.addEventListener("submit", async function(e) {
            console.log("Submit event triggered on sewer form.");
            e.preventDefault();
            console.log("preventDefault() called.");

            const submitBtn = e.target.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = "Calculating...";

            try {
                const population = parseFloat(document.getElementById("sewer-population").value);
                const perCapitaFlow = parseFloat(document.getElementById("sewer-per-capita-flow").value);
                const slope = parseFloat(document.getElementById("sewer-slope").value);
                const diameter = parseFloat(document.getElementById("sewer-diameter").value);
                const flowRatio = parseFloat(document.getElementById("sewer-flow-ratio").value);

                if (isNaN(population) || isNaN(perCapitaFlow) || isNaN(slope) || isNaN(diameter) || isNaN(flowRatio)) {
                    throw new Error("Please enter valid numbers in all fields");
                }

                const formData = {
                    population: population,
                    per_capita_flow: perCapitaFlow,
                    slope: slope,
                    pipe_type: document.getElementById("sewer-pipe-type").value,
                    n: parseFloat(document.getElementById("sewer-mannings-coeff").value),
                    diameter: diameter,
                    flow_ratio: flowRatio
                };

                console.log("Sending sewer calculation request:", formData);

                const response = await fetch("/api/sewer/sewer_pipe_sizing", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    let errorText = await response.text();
                    try {
                        const errorData = JSON.parse(errorText);
                        throw new Error(errorData.message || response.statusText || "Calculation failed");
                    } catch (parseError) {
                        throw new Error(errorText || response.statusText || "Calculation failed");
                    }
                }

                const data = await response.json();
                console.log("Received sewer calculation results:", data);
                displayResults(data);

            } catch (error) {
                console.error("Sewer calculation error:", error);
                alert("Error: " + error.message);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            }
        });

        function displayResults(data) {
            console.log("Displaying sewer results:", data);
            const resultsDiv = document.getElementById("sewer-results");
            const resultItems = document.getElementById("sewer-result-items");

            if (!resultsDiv || !resultItems) {
                console.error("Sewer results display elements not found");
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
                    <span class="result-value">${(data.demand_ms ?? 0).toFixed(3)}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Pipe Capacity (m³/s):</span>
                    <span class="result-value">${(data.capacity ?? 0).toFixed(3)}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Velocity (m/s):</span>
                    <span class="result-value">${(data.velocity ?? 0).toFixed(3)}</span>
                </div>
                ${data.additional_results ? `
                <div class="result-item">
                    <span class="result-label">Additional Results:</span>
                    <span class="result-value">${data.additional_results}</span>
                </div>
                ` : ''}
            `;

            resultsDiv.style.display = "block";
            console.log("Sewer results displayed successfully");
        }
    });
})();