from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import os

app = Flask(__name__)

# Load the pre-trained skin analysis model
MODEL_PATH = "skin_analysis_model.h5"
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    model = None  # Log this or handle properly in production

# Function to get skincare recommendations based on detected features
def get_recommendations(features):
    recommendations = []
    if features.get("dryness"):
        recommendations.append("Moisturizer with Hyaluronic Acid")
    if features.get("wrinkles"):
        recommendations.append("Anti-aging cream with Retinol")
    if features.get("blemishes"):
        recommendations.append("Vitamin C serum for dark spots")
    if features.get("oily_skin"):
        recommendations.append("Oil-free cleanser and lightweight moisturizer")
    return recommendations

# Function to preprocess the image before feeding it to the model
def preprocess_image(image):
    try:
        img = Image.open(image).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = (img_array - 0.5) / 0.5  # Normalization example
        return np.expand_dims(img_array, axis=0)
    except Exception as e:
        raise ValueError("Error preprocessing image: " + str(e))

# Analyze the image and return recommendations
def analyze_image(image):
    try:
        preprocessed_image = preprocess_image(image)

        if model:
            predictions = model.predict(preprocessed_image)
            features = {
                "dryness": predictions[0][0] > 0.5,
                "wrinkles": predictions[0][1] > 0.5,
                "blemishes": predictions[0][2] > 0.5,
                "oily_skin": predictions[0][3] > 0.5,
            }
        else:
            features = {  # Mock features for testing
                "dryness": True,
                "wrinkles": False,
                "blemishes": True,
                "oily_skin": False,
            }

        recommendations = get_recommendations(features)
        return {"features": features, "recommendations": recommendations}

    except Exception as e:
        return {"error": str(e)}

# Define the Flask API endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    try:
        result = analyze_image(file.stream)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
