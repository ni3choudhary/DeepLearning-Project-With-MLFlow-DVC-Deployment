from DLProject.constants import *
from DLProject.utils.common import read_yaml, create_directories
from DLProject.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, TrainingConfig, EvaluationConfig
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_TRACKING_USERNAME = os.getenv("MLFLOW_TRACKING_USERNAME")
MLFLOW_TRACKING_PASSWORD = os.getenv("MLFLOW_TRACKING_PASSWORD")

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config
    
    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config
    
    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, training.source_dir)
        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(prepare_base_model.updated_base_model_path),
            training_data=Path(training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE,
            params_validation_split=params.VALIDATION_SPLIT,
            params_interpolation=params.INTERPOLATION,
            params_validation_data_generator_subset=params.VALIDATION_DATA_GENERATOR_SUBSET,
            params_training_data_generator_subset=params.TRAINING_DATA_GENERATOR_SUBSET,
            params_is_validation_data_generator_shuffle=params.VALIDATION_DATA_GENERATOR_SHUFFLE,
            params_is_training_data_generator_shuffle=params.TRAINING_DATA_GENERATOR_SHUFFLE,
            params_rotation_range=params.ROTATION_RANGE,
            params_is_horizontal_flip=params.HORIZONTAL_FLIP,
            params_width_shift_range=params.WIDTH_SHIFT_RANGE,
            params_height_shift_range=params.HEIGH_SHIFT_RANGE,
            params_shear_range=params.SHEAR_RANGE,
            params_zoom_range=params.ZOOM_RANGE,
            source_dir=Path(training.source_dir)
        )

        return training_config

    def get_evaluation_config(self) -> EvaluationConfig:
        training = self.config.training
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, training.source_dir)
        
        eval_config = EvaluationConfig(
            path_of_model=Path(training.trained_model_path),
            training_data=Path(training_data),
            mlflow_uri=MLFLOW_TRACKING_URI,
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return eval_config

