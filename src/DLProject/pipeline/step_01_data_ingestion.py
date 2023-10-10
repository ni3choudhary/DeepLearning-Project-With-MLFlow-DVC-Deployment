from DLProject.config.configuration import ConfigurationManager
from DLProject.components.data_ingestion import DataIngestion
from DLProject import logger

class DataIngestionTrainingPipeline:
    def __init__(self, stage_name = "Data Ingestion"):
        self.stage_name = stage_name
        logger.info(f">>>>>> {self.stage_name} stage started <<<<<<")

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()
        logger.info(f">>>>>> {self.stage_name} stage completed <<<<<<")


if __name__ == "__main__":
    try:
        data_ing = DataIngestionTrainingPipeline()
        data_ing.main()
    except Exception as e:
        logger.exception(e)
        raise e


