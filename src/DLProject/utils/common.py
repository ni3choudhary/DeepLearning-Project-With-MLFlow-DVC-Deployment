from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
import yaml
from DLProject import logger
from box.exceptions import BoxValueError
import os

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns a ConfigBox.

    Args:
        path_to_yaml (str): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty.
        e: empty file

    Returns:
        ConfigBox: ConfigBox containing the YAML content.
    """
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {path_to_yaml}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error loading YAML file {path_to_yaml}: {e}")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create a list of directories

    Args:
        path_to_directories (list): list of path to directories
        verbose (bool, optional): Whether to log the created directories. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")