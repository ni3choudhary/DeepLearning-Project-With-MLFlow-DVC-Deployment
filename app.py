from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from DLProject.pipeline.prediction import PredictionPipeline
import os
from DLProject.utils.common import decodeImage
from DLProject import logger

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        # Define the default input image filename
        self.filename = "inputImage.jpg"
        # Create an instance of the PredictionPipeline for making predictions
        self.classifier = PredictionPipeline(self.filename)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    # Render the homepage for the web application
    return render_template('index.html')

@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    # Execute the main process when the /train route is accessed
    os.system("python main.py")
    # os.system("dvc repro")
    logger.info("Training done successfully!")
    return "Training done successfully!"

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        # Get the image data from the request and decode it
        image = request.json['image']
        decodeImage(image, client.filename)
        # Make a prediction using the classifier
        result = client.classifier.predict()
        return jsonify(result)
    
    except Exception as e:
        # Log Exceptions occurs during exceptions
        logger.error("Prediction error: %s", str(e))
        return jsonify({'error': 'An error occurred during prediction.'})


if __name__ == "__main__":
    client = ClientApp()
    logger.info("Starting the Flask application...")
    app.run(host='0.0.0.0', port=8080, debug=True) #for AWS