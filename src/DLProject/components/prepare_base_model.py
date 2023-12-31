import tensorflow as tf
from pathlib import Path
from DLProject import logger
from DLProject.entity.config_entity import PrepareBaseModelConfig

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    def get_base_model(self):
        '''
        Create a VGG16 base model based on the configuration
        '''
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )

        # Save the base model to a specified path
        self.save_model(path=self.config.base_model_path, model=self.model)

        # Log a message indicating that the base model has been created and saved
        logger.info("Base model created and saved at: %s", self.config.base_model_path)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        # Freeze all layers in the model if 'freeze_all' is set to True
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
            logger.info("Freezing all layers in the model.")
        # Freeze layers until a specified index if 'freeze_till' is a positive integer
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False
            logger.info("Freezing layers until layer index: %d", freeze_till)

        # Add a Flatten layer to the model's output
        flatten_in = tf.keras.layers.Flatten()(model.output)

        # Add a Dense layer for classification with 'classes' units and softmax activation
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(flatten_in)

        # Create a new full model with the modified architecture
        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )

        # Compile the full model with specified optimizer, loss function and metrics
        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        # Log a summary of the full model's architecture
        logger.info("Full model summary:\n%s", full_model.summary())
        return full_model  # Return the compiled full model
    
    
    def update_base_model(self):
        # Create a new updated base model
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate
        )

        # Save the updated full model to a specified path
        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

        # Log a message indicating that the base model has been updated and saved
        logger.info("Updated base model created and saved at: %s", self.config.updated_base_model_path)