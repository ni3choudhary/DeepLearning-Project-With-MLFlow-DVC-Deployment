import os
import zipfile
import gdown
from DLProject import logger
from DLProject.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    
    def download_file(self)-> str:
        '''
        Fetch data from the url
        '''

        dataset_url = self.config.source_URL
        zip_download_dir = self.config.local_data_file
        root_download_dir = self.config.root_dir

        os.makedirs(root_download_dir, exist_ok=True)
        logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

        FILE_ID = dataset_url.split("/")[-2]
        PREFIX_URL = "https://drive.google.com/uc?/export=download&id="

        DOWNLOAD_URL = f'{PREFIX_URL}{FILE_ID}'
        try:
            gdown.download(DOWNLOAD_URL,  zip_download_dir)
            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            logger.error(f"Error downloading data from {dataset_url}: {e}")
            raise ValueError(f"Failed to download data from {dataset_url}")

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory.

        Returns:
            None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        zip_file_path = self.config.local_data_file

        if not os.path.exists(zip_file_path):
            raise FileNotFoundError(f"Zip file not found at {zip_file_path}")
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
                logger.info(f"Extracted zip file to {unzip_path}")
                
        except zipfile.BadZipFile as e:
            logger.error(f"Error extracting zip file: {e}")
            raise ValueError("Failed to extract zip file")