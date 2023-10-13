from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
import yaml
from DLProject import logger
from box.exceptions import BoxValueError
import os
import json
import base64

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
        with open(path_to_yaml) as yaml_file:
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


@ensure_annotations
def get_size(path: Path) -> str:
    """Get the size of a file in KB.

    Args:
        path (Path): path to the file

    Returns:
        str: Size in KB as a string.
    """
    try:
        size_in_bytes = os.path.getsize(path)
        size_in_kb = round(size_in_bytes / 1024)
        return f"~ {size_in_kb} KB"
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error in getting size of a file in KB: {str(e)}"


@ensure_annotations
def save_json(path: Path, data: dict):
    """Save JSON data to a file.

    Args:
        path (Path): path to the JSON file
        data (dict): Data to be saved in the JSON file
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        logger.info(f"JSON file saved at: {path}")

    except (FileNotFoundError, PermissionError, OSError) as e:
        logger.error(f"Error saving JSON file: {e}")
        raise ValueError(f"Failed to save JSON file at: {path}")


def decodeImage(imgstring, fileName):
    try:
        # Decode the base64-encoded image string into binary data
        imgdata = base64.b64decode(imgstring)
        # Open the specified file in binary write mode and save the image data
        with open(fileName, 'wb') as f:
            f.write(imgdata)

        logger.info(f"Image Decoded Successfully and Saved into {fileName}")

    except Exception as e:
        logger.error(f"Failed to Decode the Image or Failed to Saved in {fileName}: {str(e)}")
        raise e