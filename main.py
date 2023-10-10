from DLProject import logger
from DLProject.pipeline.step_01_data_ingestion import DataIngestionTrainingPipeline
from DLProject.pipeline.step_02_prepare_base_model import PrepareBaseModelTrainingPipeline

class MainClass:
    
    def __init__(self):
        pass

    def callDataIngestion(self):
        try:
            data_ing = DataIngestionTrainingPipeline()
            data_ing.main()
        except Exception as e:
            logger.exception(e)
            raise e
        
    def callPrepareBaseModel(self):
        try:
            prep_model = PrepareBaseModelTrainingPipeline()
            prep_model.main()

        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    cls = MainClass()
    # cls.callDataIngestion()
    cls.callPrepareBaseModel()