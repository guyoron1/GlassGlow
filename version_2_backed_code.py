from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import os

app = Flask(__name__)

# Load your pre-trained skin analysis model (Replace with actual model)
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


# Function to process the image and analyze facial features
def analyze_image(image):
    try:
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load a pre-trained face detector from OpenCV
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return {"error": "No face detected"}

        # For simplicity, analyze the first detected face
        (x, y, w, h) = faces[0]
        face_region = image[y:y + h, x:x + w]

        # Resize the face for the model
        resized_face = cv2.resize(face_region, (224, 224))
        normalized_face = resized_face / 255.0  # Normalize pixel values
        input_data = np.expand_dims(normalized_face, axis=0)  # Add batch dimension

        # Analyze the face using the model (mock example for now)
        if model:
            predictions = model.predict(input_data)
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
