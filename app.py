from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

def predict_crime_risk(data):
    score = 5  # Base risk
    
    # Map frontend fields to backend logic
    age_group = data.get("ageGroup", "adult")
    education = data.get("education", "high")
    employment = data.get("employment", "employed")
    environment = data.get("environment", "safe")
    history = data.get("history", False)
    substance = data.get("substance", False)

    
    # Rule 1: Age group
    if age_group == "teen":
        score += 15
    elif age_group == "adult":
        score += 5
    
    # Rule 2: Education
    if education == "none":
        score += 20
    elif education == "low":
        score += 10
    
    # Rule 3: Employment
    if employment == "unemployed":
        score += 25
    elif employment == "unstable":
        score += 15
    
    # Rule 4: Environment
    if environment == "high_risk":
        score += 20
    elif environment == "moderate":
        score += 10
    
    # Rule 5: Criminal history
    if history:
        score += 25
    
    # Rule 6: Substance abuse
    if substance:
        score += 30
    
    # Cap at 98%
    if score > 98:
        score = 98
    
    return score


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    result = predict_crime_risk(data)
    
    # Determine risk level
    if result >= 70:
        level = "NGUY HIỂM (CAO)"
    elif result >= 40:
        level = "CẢNH BÁO (TRUNG BÌNH)"
    else:
        level = "THẤP"

    return jsonify({
        "risk": result,
        "level": level
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)