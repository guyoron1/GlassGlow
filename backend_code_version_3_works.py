from flask import Flask, request, jsonify
import cv2
import numpy as np
#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
from tensorflow.python.keras.models import load_model
#from tensorflow.python.keras.preprocessing.image import img_to_array

from PIL import Image
import os

app = Flask(__name__)

# Load your pre-trained skin analysis model
MODEL_PATH = "skin_analysis_model.h5"
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    model = None  # Replace this with a proper mock or a real model


# Mock recommendations based on features
def get_recommendations(features):
    recommendations = []
    if features["dryness"]:
        recommendations.append("Moisturizer with Hyaluronic Acid")
    if features["wrinkles"]:
        recommendations.append("Anti-aging cream with Retinol")
    if features["blemishes"]:
        recommendations.append("Vitamin C serum for dark spots")
    if features["oily_skin"]:
        recommendations.append("Oil-free cleanser and lightweight moisturizer")
    return recommendations

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")  # Open the image and convert it to RGB format
    img = img.resize((224, 224))  # Resize the image to the model's expected input size (224x224)
    img_array = np.array(img) / 255.0  # Normalize pixel values to the range [0, 1]
    return np.expand_dims(img_array, axis=0)  # Add a batch dimension for prediction

# Function to process the image and analyze facial features
def analyze_image(image):
    try:
        # Preprocess the image
        preprocessed_image = preprocess_image(image)

        # Analyze the face using the model (mock example for now)
        if model:
            predictions = model.predict(preprocessed_image)
            features = {
                "dryness": predictions[0][0] > 0.5,
                "wrinkles": predictions[0][1] > 0.5,
                "blemishes": predictions[0][2] > 0.5,
                "oily_skin": predictions[0][3] > 0.5,
            }
        else:
            # Mock feature detection
            features = {
                "dryness": True,
                "wrinkles": False,
                "blemishes": True,
                "oily_skin": False,
            }

        # Generate skincare recommendations based on features
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
        # Load the image
        image = Image.open(file.stream).convert("RGB")
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR for OpenCV

        # Analyze the image
        result = analyze_image(open_cv_image)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
