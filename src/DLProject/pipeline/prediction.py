import os
import tensorflow as tf
import numpy as np
from DLProject import logger

MODEL_PATH = os.path.join("artifacts", "training", "model.h5")
TUMOR_LABEL = 'Tumor'
NORMAL_LABEL = 'Normal'
WIDTH, HEIGHT = 224, 224

class PredictionPipeline:
    def __init__(self, filename):
        """Initialize the PredictionPipeline.

        Args:
            filename (str): Path to the image file for prediction.
        """
        self.filename = filename

    def predict(self):
        """Make a prediction based on the loaded Keras model.

        Returns:
            list: A list containing a dictionary with the prediction result.
        """
        try:
            # Load the Keras model from the specified path
            model = tf.keras.models.load_model(MODEL_PATH)
            
            imagename = self.filename
            test_image = tf.keras.preprocessing.image.load_img(imagename, target_size = (WIDTH, HEIGHT))
            test_image = tf.keras.preprocessing.image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis = 0)
            result = np.argmax(model.predict(test_image), axis=1)

            if result[0] == 1:
                prediction = TUMOR_LABEL
            else:
                prediction = NORMAL_LABEL

            logger.info(f"Prediction for {self.filename}: {prediction}")

            return [{"image": prediction}]
        
        except tf.errors.OpError as e:
            error_message = f"TensorFlow Error: {e}"
            logger.error(error_message)
            return [{"image": "Error", "details": error_message}]
        except FileNotFoundError:
            error_message = "File not found"
            logger.error(error_message)
            return [{"image": "Error", "details": error_message}]
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            logger.error(error_message)
            return [{"image": "Error", "details": error_message}]
