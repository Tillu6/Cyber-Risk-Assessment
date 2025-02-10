function calculateRisk() {
    const companySize = document.getElementById("companySize").value;
    const firewall = document.getElementById("firewall").value;
    const dataSensitivity = document.getElementById("dataSensitivity").value;
    const incidentResponse = document.getElementById("incidentResponse").value;
    const encryption = document.getElementById("encryption").value;

    // Improved risk calculation
    let riskScore = 0;
    
    if (companySize === "medium") riskScore += 3;
    if (companySize === "large") riskScore += 7;
    if (firewall === "no") riskScore += 5;
    if (dataSensitivity === "medium") riskScore += 6;
    if (dataSensitivity === "high") riskScore += 10;
    if (incidentResponse === "no") riskScore += 8;
    if (encryption === "no") riskScore += 4;

    // Improved premium calculation
    const basePremium = 500; // Base insurance cost
    const premium = basePremium + (riskScore * 75); // $75 per risk point

    // Smooth fade-in effect for results
    const resultsDiv = document.getElementById("results");
    resultsDiv.style.opacity = "0";
    resultsDiv.style.display = "block";

    setTimeout(() => {
        resultsDiv.style.opacity = "1";
        document.getElementById("riskScore").textContent = riskScore;
        document.getElementById("premium").textContent = "$" + premium.toLocaleString();
    }, 300);
}
