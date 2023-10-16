from DLProject import logger
from DLProject.entity.config_entity import TrainingConfig
import tensorflow as tf
from pathlib import Path
import os
import shutil

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    # Load the updated base model from the specified path
    def get_base_model(self):
        # Log a message indicating the loading of the updated base model
        logger.info("Loading the updated base model from: %s", self.config.updated_base_model_path)
        self.model = tf.keras.models.load_model(
            self.config.updated_base_model_path
        )

        # Log a message indicating that the base model has been successfully loaded
        logger.info("Base model loaded successfully for model training.")

    def train_valid_generator(self):

        # Define data augmentation and validation split settings
        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=self.config.params_validation_split
        )

        # Define data flow settings
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation=self.config.params_interpolation
        )

        # Create an ImageDataGenerator for validation data
        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        # Generate a validation data generator
        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset=self.config.params_validation_data_generator_subset,
            shuffle=self.config.params_is_validation_data_generator_shuffle,
            **dataflow_kwargs
        )

        logger.info("Validation data generator created with validation split: %.2f", datagenerator_kwargs['validation_split'])

        # Check if data augmentation is enabled
        if self.config.params_is_augmentation:
            # If enabled, create an ImageDataGenerator with augmentation options
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=self.config.params_rotation_range,
                horizontal_flip=self.config.params_is_horizontal_flip,
                width_shift_range=self.config.params_width_shift_range,
                height_shift_range=self.config.params_height_shift_range,
                shear_range=self.config.params_shear_range,
                zoom_range=self.config.params_zoom_range,
                **datagenerator_kwargs
            )
        else:
            # If not enabled, use the same datagenerator as for validation
            train_datagenerator = valid_datagenerator

        # Generate a training data generator
        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset=self.config.params_training_data_generator_subset,
            shuffle=self.config.params_is_training_data_generator_shuffle,
            **dataflow_kwargs
        )

        logger.info("Training data generator created with data augmentation: %s", self.config.params_is_augmentation)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        try:
            # Save the model to the specified path
            model.save(path)
            
            # Log a message indicating that the model has been successfully saved
            logger.info("Trained Model saved successfully to: %s", path)
        except Exception as e:
            # Log an error message if there's an issue with model saving
            logger.error("Error saving trained model: %s", str(e))

    @staticmethod
    def copy_model(path: Path, artifacts_model: Path):
        try:
            # Get the directory name
            directory_name = os.path.dirname(path)
            os.makedirs(directory_name, exist_ok=True)

            # Copy the model file to the newly created folder
            shutil.copy(artifacts_model, directory_name)
            
            # Log a message indicating that the model has been successfully copied
            logger.info("Trained Model copied successfully to: %s", path)
        except Exception as e:
            # Log an error message if there's an issue with model copying
            logger.error("Error copying trained model: %s", str(e))

    def train(self):
        # Calculate the number of steps per epoch and validation steps
        self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        # Log the training parameters
        logger.info("Training for %d epochs with %d steps per epoch and %d validation steps.", 
                         self.config.params_epochs, self.steps_per_epoch, self.validation_steps)

        # Train the model using the provided generators and configuration
        self.model.fit(
            self.train_generator,
            epochs=self.config.params_epochs,
            steps_per_epoch=self.steps_per_epoch,
            validation_steps=self.validation_steps,
            validation_data=self.valid_generator
        )

        logger.info("Model Training completed.")
        
        # Save the trained model to the specified path
        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )

        # copy the trained model for further use in prediction pipeline
        self.copy_model(self.config.copy_trained_model_path, self.config.trained_model_path)