function calculateRisk() {
    // Gather form data
    const companySize = document.getElementById("companySize").value;
    const firewall = document.getElementById("firewall").value;
    const dataSensitivity = document.getElementById("dataSensitivity").value;
    const incidentResponse = document.getElementById("incidentResponse").value;
    const encryption = document.getElementById("encryption").value;
  
    // Prepare data object for the backend
    const data = {
      companySize: companySize,
      firewall: firewall,
      dataSensitivity: dataSensitivity,
      incidentResponse: incidentResponse,
      encryption: encryption
    };
  
    // Call the AI-enabled endpoint to calculate risk, premium, and suggestions
    fetch("/calculate_risk_ai", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        // Extract values returned from the backend
        const riskScore = result.riskScore;
        const premium = result.premium;
        const suggestions = result.suggestions;
  
        // Build the suggestions HTML (if any)
        let suggestionsHTML = "";
        if (suggestions && suggestions.length > 0) {
          suggestionsHTML = "<ul>";
          suggestions.forEach(suggestion => {
            suggestionsHTML += `<li>${suggestion}</li>`;
          });
          suggestionsHTML += "</ul>";
        }
  
        // Smooth fade-in effect for results
        const resultsDiv = document.getElementById("results");
        resultsDiv.style.opacity = "0";
        resultsDiv.style.display = "block";
  
        setTimeout(() => {
          resultsDiv.style.opacity = "1";
          document.getElementById("riskScore").textContent = riskScore;
          document.getElementById("premium").textContent = "$" + premium.toLocaleString();
          document.getElementById("suggestions").innerHTML = suggestionsHTML;
        }, 300);
      })
      .catch(error => {
        console.error("Error:", error);
        const resultsDiv = document.getElementById("results");
        resultsDiv.style.opacity = "0";
        resultsDiv.style.display = "block";
        setTimeout(() => {
          resultsDiv.style.opacity = "1";
          resultsDiv.innerHTML = `<p class="error">An error occurred. Please try again.</p>`;
        }, 300);
      });
  }
  