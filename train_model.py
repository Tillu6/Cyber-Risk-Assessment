import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

# Generate synthetic dataset
np.random.seed(42)

data_size = 500
company_size = np.random.choice([1, 2, 3], size=data_size)  # 1: Small, 2: Medium, 3: Large
firewall = np.random.choice([0, 1], size=data_size)  # 0: Yes, 1: No
data_sensitivity = np.random.choice([1, 2, 3], size=data_size)  # 1: Low, 2: Medium, 3: High
incident_response = np.random.choice([0, 1], size=data_size)  # 0: Yes, 1: No
encryption = np.random.choice([0, 1], size=data_size)  # 0: Yes, 1: No

# Define risk score formula (or adjust as needed)
risk_score = (company_size * 3) + (firewall * 5) + (data_sensitivity * 4) + (incident_response * 6) + (encryption * 3)

# Create DataFrame
df = pd.DataFrame({
    "company_size": company_size,
    "firewall": firewall,
    "data_sensitivity": data_sensitivity,
    "incident_response": incident_response,
    "encryption": encryption,
    "risk_score": risk_score
})

# Split into features and target variable
X = df.drop(columns=["risk_score"])
y = df["risk_score"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Decision Tree model
model = DecisionTreeRegressor(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Model MAE: {mae:.2f}")

# Save the trained model
with open("risk_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as risk_model.pkl")
