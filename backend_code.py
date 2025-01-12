from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load pre-trained model
model = load_model('skin_analysis_model.h5')


def analyze_image(image_path):
    # Load image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Preprocess image
    resized = cv2.resize(gray, (224, 224)).reshape(1, 224, 224, 1) / 255.0

    # Predict features
    features = model.predict(resized)
    recommendations = {"skincare": "Recommended product based on features"}  # Placeholder
    return recommendations


@app.route('/analyze', methods=['POST'])
def analyze():
    image = request.files['image']
    # Save the uploaded image temporarily
    image_path = 'temp_image.jpg'
    image.save(image_path)

    # Get recommendations after analysis
    recommendations = analyze_image(image_path)
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)
