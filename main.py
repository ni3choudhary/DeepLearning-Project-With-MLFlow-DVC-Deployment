from DLProject import logger
from DLProject.pipeline.step_01_data_ingestion import DataIngestionTrainingPipeline

try:
    data_ing = DataIngestionTrainingPipeline()
    data_ing.main()
except Exception as e:
    logger.exception(e)
    raise e

