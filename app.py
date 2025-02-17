from flask import Flask, request, jsonify, render_template
import logging
import os
import pickle

app = Flask(__name__, template_folder="templates")

# Setup logging for debugging and error messages
logging.basicConfig(level=logging.INFO)

# Attempt to load a pre-trained AI model for risk prediction.
MODEL_PATH = "risk_model.pkl"
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        ai_model = pickle.load(f)
    logging.info("AI model loaded successfully.")
else:
    ai_model = None
    logging.info("AI model not found. Falling back to the rule-based system.")


def rule_based_risk(company_size, firewall, data_sensitivity, incident_response, encryption):
    """
    Calculate the risk score using the rule-based approach.
    """
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
    Encode input features into numerical values for the AI model.
    Mappings:
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
    """
    Predict risk score using the AI model.
    If no model is loaded, fall back to the rule-based approach by decoding the features.
    """
    if ai_model:
        # The model expects a 2D array
        prediction = ai_model.predict([features])
        risk_score = prediction[0]
    else:
        # Fallback: decode features and apply rule-based logic
        company_size_map = {1: "small", 2: "medium", 3: "large"}
        data_sensitivity_map = {1: "low", 2: "medium", 3: "high"}

        company_size_str = company_size_map.get(features[0], "small")
        data_sensitivity_str = data_sensitivity_map.get(features[2], "low")
        firewall_str = "yes" if features[1] == 0 else "no"
        incident_response_str = "yes" if features[3] == 0 else "no"
        encryption_str = "yes" if features[4] == 0 else "no"

        risk_score = rule_based_risk(company_size_str, firewall_str, data_sensitivity_str, incident_response_str, encryption_str)
    return risk_score


def get_security_suggestions(company_size, firewall, data_sensitivity, incident_response, encryption):
    """
    Provide security improvement suggestions based on the user inputs.
    """
    suggestions = []
    if firewall.lower() == "no":
        suggestions.append("Install a robust firewall solution to help block unauthorized access.")
    if encryption.lower() == "no":
        suggestions.append("Enable data encryption to protect sensitive information.")
    if incident_response.lower() == "no":
        suggestions.append("Develop and maintain an incident response plan to quickly address breaches.")
    if data_sensitivity.lower() in ["medium", "high"]:
        suggestions.append("Review your data classification policies and implement enhanced data protection measures.")
    if company_size.lower() in ["medium", "large"]:
        suggestions.append("Consider investing in a dedicated cybersecurity team or managed security services.")
    if not suggestions:
        suggestions.append("Your security measures appear robust. Keep up the great work!")
    return suggestions


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
    """
    Endpoint to calculate risk and premium using the rule-based approach.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        company_size = data.get('companySize')
        firewall = data.get('firewall')
        data_sensitivity = data.get('dataSensitivity')
        incident_response = data.get('incidentResponse')
        encryption = data.get('encryption')

        if not all([company_size, firewall, data_sensitivity, incident_response, encryption]):
            return jsonify({'error': 'Missing risk factor data'}), 400

        risk_score = rule_based_risk(company_size.lower(),
                                     firewall.lower(),
                                     data_sensitivity.lower(),
                                     incident_response.lower(),
                                     encryption.lower())

        base_premium = 500
        premium = base_premium + (risk_score * 75)
        suggestions = get_security_suggestions(company_size, firewall, data_sensitivity, incident_response, encryption)

        return jsonify({
            'riskScore': risk_score,
            'premium': premium,
            'suggestions': suggestions,
            'aiUsed': False
        }), 200

    except Exception as e:
        app.logger.error(f"Error in calculate_risk: {e}")
        return jsonify({'error': 'An error occurred during risk calculation'}), 500


@app.route('/calculate_risk_ai', methods=['POST'])
def calculate_risk_ai():
    """
    Endpoint to calculate risk and premium using AI-based prediction.
    If the AI model is not available, the rule-based approach is used.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        company_size = data.get('companySize')
        firewall = data.get('firewall')
        data_sensitivity = data.get('dataSensitivity')
        incident_response = data.get('incidentResponse')
        encryption = data.get('encryption')

        if not all([company_size, firewall, data_sensitivity, incident_response, encryption]):
            return jsonify({'error': 'Missing risk factor data'}), 400

        features = encode_features(company_size, firewall, data_sensitivity, incident_response, encryption)
        risk_score = ai_based_risk(features)

        base_premium = 500
        premium = base_premium + (risk_score * 75)
        suggestions = get_security_suggestions(company_size, firewall, data_sensitivity, incident_response, encryption)

        return jsonify({
            'riskScore': risk_score,
            'premium': premium,
            'suggestions': suggestions,
            'aiUsed': bool(ai_model)
        }), 200

    except Exception as e:
        app.logger.error(f"Error in calculate_risk_ai: {e}")
        return jsonify({'error': 'An error occurred during AI risk calculation'}), 500


if __name__ == '__main__':
    app.run(debug=True)  # Remember to set debug=False in production!
