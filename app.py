from flask import Flask, request, jsonify, render_template
import logging
import os
import pickle

app = Flask(__name__, template_folder="templates")

# Set up logging for debugging purposes
logging.basicConfig(level=logging.INFO)

# Attempt to load your AI model (if available)
MODEL_PATH = "risk_model.pkl"
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        ai_model = pickle.load(f)
    logging.info("AI model loaded successfully.")
else:
    ai_model = None
    logging.info("AI model not found. Falling back to the rule-based system.")

def rule_based_risk(company_size, firewall, data_sensitivity, incident_response, encryption):
    """Calculate risk score using rule-based logic."""
    risk_score = 0
    if company_size == "medium":
        risk_score += 3
    elif company_size == "large":
        risk_score += 7
    if firewall == "no":
        risk_score += 5
    if data_sensitivity == "medium":
        risk_score += 6
    elif data_sensitivity == "high":
        risk_score += 10
    if incident_response == "no":
        risk_score += 8
    if encryption == "no":
        risk_score += 4
    return risk_score

def encode_features(company_size, firewall, data_sensitivity, incident_response, encryption):
    """
    Encode features to numerical values for the AI model.
      - company_size: small=1, medium=2, large=3
      - data_sensitivity: low=1, medium=2, high=3
      - For binary options: "yes" -> 0, "no" -> 1
    """
    company_size_map = {"small": 1, "medium": 2, "large": 3}
    data_sensitivity_map = {"low": 1, "medium": 2, "high": 3}
    features = [
        company_size_map.get(company_size.lower(), 1),
        0 if firewall.lower() == "yes" else 1,
        data_sensitivity_map.get(data_sensitivity.lower(), 1),
        0 if incident_response.lower() == "yes" else 1,
        0 if encryption.lower() == "yes" else 1,
    ]
    return features

def ai_based_risk(features):
    """Predict risk score using the AI model; fall back to rule-based logic if no model is loaded."""
    if ai_model:
        # The model expects a 2D array
        prediction = ai_model.predict([features])
        risk_score = prediction[0]
    else:
        # Fallback: decode features back to string values and use rule-based calculation
        company_size_map = {1: "small", 2: "medium", 3: "large"}
        data_sensitivity_map = {1: "low", 2: "medium", 3: "high"}
        company_size_str = company_size_map.get(features[0], "small")
        data_sensitivity_str = data_sensitivity_map.get(features[2], "low")
        firewall_str = "yes" if features[1] == 0 else "no"
        incident_response_str = "yes" if features[3] == 0 else "no"
        encryption_str = "yes" if features[4] == 0 else "no"
        risk_score = rule_based_risk(company_size_str, firewall_str, data_sensitivity_str,
                                     incident_response_str, encryption_str)
    return risk_score

def get_security_suggestions(company_size, firewall, data_sensitivity, incident_response, encryption):
    """Return security improvement suggestions based on the input parameters."""
    suggestions = []
    if firewall.lower() == "no":
        suggestions.append("Install a robust firewall solution to block unauthorized access.")
    if encryption.lower() == "no":
        suggestions.append("Enable data encryption to protect sensitive information.")
    if incident_response.lower() == "no":
        suggestions.append("Develop and maintain an incident response plan for cyber attacks.")
    if data_sensitivity.lower() in ["medium", "high"]:
        suggestions.append("Review your data classification and protection measures.")
    if company_size.lower() in ["medium", "large"]:
        suggestions.append("Consider investing in dedicated cybersecurity resources.")
    if not suggestions:
        suggestions.append("Your security measures appear robust. Keep up the good work!")
    return suggestions

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate_risk_ai", methods=["POST"])
def calculate_risk_ai():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        company_size = data.get("companySize")
        firewall = data.get("firewall")
        data_sensitivity = data.get("dataSensitivity")
        incident_response = data.get("incidentResponse")
        encryption = data.get("encryption")

        if not all([company_size, firewall, data_sensitivity, incident_response, encryption]):
            return jsonify({"error": "Missing risk factor data"}), 400

        features = encode_features(company_size, firewall, data_sensitivity, incident_response, encryption)
        risk_score = ai_based_risk(features)
        base_premium = 500
        premium = base_premium + (risk_score * 75)
        suggestions = get_security_suggestions(company_size, firewall, data_sensitivity, incident_response, encryption)

        return jsonify({
            "riskScore": risk_score,
            "premium": premium,
            "suggestions": suggestions,
            "aiUsed": bool(ai_model)
        }), 200

    except Exception as e:
        app.logger.error(f"Error in calculate_risk_ai: {e}")
        return jsonify({"error": "An error occurred during risk calculation"}), 500

if __name__ == "__main__":
    app.run(debug=True)
