from DLProject import logger
from DLProject.pipeline.step_01_data_ingestion import DataIngestionTrainingPipeline
from DLProject.pipeline.step_02_prepare_base_model import PrepareBaseModelTrainingPipeline
from DLProject.pipeline.step_03_model_training import ModelTrainingPipeline
from DLProject.pipeline.step_04_model_evaluation import EvaluationPipeline

class MainClass:
    
    def __init__(self):
        pass

    def callDataIngestion(self):
        try:
            # Create an instance of the DataIngestionTrainingPipeline and call its 'main' method.
            data_ing = DataIngestionTrainingPipeline()
            data_ing.main()
        except Exception as e:
            # Log any exceptions that occur and re-raise them.
            logger.exception(e)
            raise e   # Raising the exception further for error handling.
        
    def callPrepareBaseModel(self):
        try:
            # Create an instance of the PrepareBaseModelTrainingPipeline and call its 'main' method.
            prep_model = PrepareBaseModelTrainingPipeline()
            prep_model.main()

        except Exception as e:
             # Log any exceptions that occur and re-raise them.
            logger.exception(e)
            raise e
        
    def callModelTraining(self):
        try:
            # Create an instance of the ModelTrainingPipeline and call its 'main' method.
            model_trn_pipeline = ModelTrainingPipeline()
            model_trn_pipeline.main()
        except Exception as e:
            # Log any exceptions that occur and re-raise them.
            logger.exception(e)
            raise e

    def callModelEvaluation(self):
        try:
            evaluation_pipeline = EvaluationPipeline()
            evaluation_pipeline.main()
        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    cls = MainClass()
    cls.callDataIngestion()
    cls.callPrepareBaseModel()
    cls.callModelTraining()
    cls.callModelEvaluation()