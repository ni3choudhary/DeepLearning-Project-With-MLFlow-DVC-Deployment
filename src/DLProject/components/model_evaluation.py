from DLProject import logger
from DLProject.entity.config_entity import EvaluationConfig
import tensorflow as tf
from pathlib import Path
from DLProject.utils.common import save_json
import mlflow
import mlflow.keras
from urllib.parse import urlparse

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def _valid_generator(self):
        # Define data augmentation and validation split settings
        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=self.config.all_params['VALIDATION_SPLIT']
        )

        # Define data flow settings
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation=self.config.all_params['INTERPOLATION']
        )

        # Create an ImageDataGenerator for validation data
        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        # Generate a validation data generator
        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset=self.config.all_params['VALIDATION_DATA_GENERATOR_SUBSET'],
            shuffle=self.config.all_params['VALIDATION_DATA_GENERATOR_SHUFFLE'],
            **dataflow_kwargs
        )

        # Log messages for data generator setup
        logger.info("Validation data generator created with validation split: %.2f", datagenerator_kwargs['validation_split'])

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        """
        Load a TensorFlow Keras model from a specified file path.

        Args:
            path (Path): The file path where the model is saved.

        Returns:
            tf.keras.Model: The loaded Keras model.
        """
        try:
            # Load the Keras model from the specified path
            loaded_model = tf.keras.models.load_model(path)
            
            # Log a message indicating that the model has been successfully saved
            logger.info("Trained Model loaded successfully to: %s", path)

            return loaded_model
        except Exception as e:
            # Log an error message if there's an issue with model loading
            logger.error("Error loading trained model: %s", str(e))

    def evaluation(self):
        # Load the model for evaluation from the specified path
        self.model = self.load_model(self.config.path_of_model)

        # Set up the validation data generator
        self._valid_generator()

        # Evaluate the model on the validation dataset
        self.score = self.model.evaluate(self.valid_generator)

        # Log the evaluation score
        logger.info("Evaluation score: %s", self.score)
        # Save the evaluation score
        self.save_score()

    def save_score(self):
        # Create a dictionary containing the evaluation scores
        scores = {"loss": self.score[0], "accuracy": self.score[1]}

        # Save the scores to a JSON file
        save_json(path=Path("scores.json"), data=scores)

        # Log a message indicating that the scores have been saved
        logger.info("Evaluation scores saved to 'scores.json'.")

    def log_into_mlflow(self):
        # Set the MLflow registry URI
        mlflow.set_registry_uri(self.config.mlflow_uri)

        # Get the tracking URL type from the tracking URI
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
        # Start an MLflow run
        with mlflow.start_run():
            # Log model parameters
            mlflow.log_params(self.config.all_params)
            # Log evaluation metrics
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )
            # Model registry does not work with file store
            # Check if the tracking URL type is not "file" (i.e. not using a file store)
            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model") #  Replace "VGG16Model" with an appropriate model name
            else:
                # Log the model without registering it
                mlflow.keras.log_model(self.model, "model")

        # Log a message indicating that the model and metrics have been logged into MLflow
        logger.info("Model and metrics have been logged into MLflow.")