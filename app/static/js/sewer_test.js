document.addEventListener('DOMContentLoaded', () => {
    console.log("Inline JS working");
    
    // Test button handler
    document.getElementById("test-js").addEventListener("click", () => {
        console.log("button clicked");
    });

    // Form submission handler
    document.getElementById("sewer-test-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        
        try {
            // Show loading state
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = "Calculating...";

            // Get form data
            const formData = {
                population: parseFloat(document.getElementById("sewer-population").value),
                diameter: parseFloat(document.getElementById("sewer-diameter").value),
                slope: parseFloat(document.getElementById("sewer-slope").value),
                flow_ratio: parseFloat(document.getElementById("sewer-flow-ratio").value)
            };

            console.log("Submitting:", formData);

            // Send to API
            const response = await fetch("/api/sewer/test_sewer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const results = await response.json();
            console.log("Received results:", results);

            // Display results
            const resultsContainer = document.getElementById("sewer-test-results");
            const resultsGrid = document.getElementById("sewer-result-items");
            
            // Clear previous results
            resultsGrid.innerHTML = '';
            
            // Add each result to the grid
            for (const [key, value] of Object.entries(results)) {
                const resultItem = document.createElement("div");
                resultItem.className = "result-item";
                
                const label = document.createElement("span");
                label.className = "result-label";
                label.textContent = `${key}:`;
                
                const val = document.createElement("span");
                val.className = "result-value";
                val.textContent = typeof value === 'number' ? value.toFixed(3) : value;
                
                resultItem.appendChild(label);
                resultItem.appendChild(val);
                resultsGrid.appendChild(resultItem);
            }
            
            // Show results section
            resultsContainer.style.display = "block";
            
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred during calculation. Please check the console for details.");
        } finally {
            // Reset button state
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = "Calculate";
        }
    });
});