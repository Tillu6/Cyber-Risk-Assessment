from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")  # Ensure Flask looks in 'templates' folder

@app.route('/')
def home():
    return render_template('index.html')  # Serve your index.html file

@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400  # Bad Request

        company_size = data.get('companySize')
        firewall = data.get('firewall')
        data_sensitivity = data.get('dataSensitivity')
        incident_response = data.get('incidentResponse')
        encryption = data.get('encryption')

        if not all([company_size, firewall, data_sensitivity, incident_response, encryption]):
            return jsonify({'error': 'Missing risk factor data'}), 400

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

        base_premium = 500
        premium = base_premium + (risk_score * 75)

        return jsonify({'riskScore': risk_score, 'premium': premium}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred during risk calculation'}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production!
