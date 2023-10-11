# import required libraries
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int


@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    params_epochs: int
    params_batch_size: int
    params_is_augmentation: bool
    params_image_size: list
    params_validation_split: float
    params_interpolation: str
    params_validation_data_generator_subset: str
    params_training_data_generator_subset: str
    params_is_validation_data_generator_shuffle: bool
    params_is_training_data_generator_shuffle: bool
    params_rotation_range: int
    params_is_horizontal_flip: bool
    params_width_shift_range: float 
    params_height_shift_range: float
    params_shear_range: float
    params_zoom_range: float
    source_dir: Path