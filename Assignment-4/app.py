import re
import joblib
import numpy as np
import sklearn
from flask import Flask, request, jsonify

# Create the Flask web app
app = Flask(__name__)

# Load pre-trained classifier and text vectorizer
model = joblib.load("best_model.pkl")
vectorizer = joblib.load("vectorizer.joblib")

def preprocess_message(message: str) -> str:
    """
    Clean up the input message by removing non-alphabetic characters
    and converting to lowercase.

    Args:
        message (str): Raw input string.

    Returns:
        str: Sanitized and normalized string.
    """
    return ' '.join(re.findall(r'\b[a-zA-Z]+\b', message.lower()))

@app.route("/score", methods=["POST"])
def score():
    """
    Flask endpoint for predicting the label of a given message.
    Accepts a POST request with a JSON body containing 'text' and optional 'threshold'.
    """
    payload = request.get_json()

    if not payload or "text" not in payload:
        return jsonify({"error": "Missing 'text' field in request body"}), 400

    message = payload["text"]
    threshold = payload.get("threshold", 0.5)

    processed = preprocess_message(message)
    vectorized = vectorizer.transform([processed])
    probability = model.predict_proba(vectorized)[0][1]
    result = probability >= threshold

    return jsonify({
        "prediction": bool(result),
        "propensity": float(probability)
    })

if __name__ == "__main__":
    # Launch the app server
    app.run(host="0.0.0.0", port=5000, debug=True)
